import pandas as pd
import numpy as np
import sys
import os
import openai
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

class Agent:
    def __init__(self, client, name, sysprompt):
        #the url endpoint
        self.client = client

        #The Name in the conversation.  User, Oracle, Journalist
        self.name = name
        
        #the persona (system prompt)
        self.sysprompt = sysprompt
        
        self.memory = []

        self.documents = []

        self.prompt = """These Are you attributes:\n
        Personality:
            {sysprompt}

        These are your Reference Documents, everybody can see them but you should never mention them directly. Only use their information when responding:
            {documents}

        Past Internal Memory, only you can see your internal memory nobody else can:
            {memory}

        Conversation History, everyone can see the Conversation History:
            {conversation}

        User Instruction to respond to:
            {instruction}
        [/INST]
        """

    def get_memory(self):
        format_mems = ["Memory " + str(i) + ":\n" + str(mem or "") for i,mem in enumerate(self.memory)]

        txt = "\n".join(format_mems)

        return txt

    # generating prompt for agent, filling out necessary params
    def get_prompt(self, instruction, group):
        
        txt = self.prompt.format(sysprompt = self.sysprompt, documents = self.get_documents(), conversation = group.get_conv(), memory = self.get_memory(), instruction = instruction)

        return txt

    def instruct(self, instruction, group, max_length = 200, append_prompt = ""):
        
        txt = self.prompt.format(sysprompt = self.sysprompt, documents = self.get_documents(), conversation = group.get_conv(), memory = self.get_memory(), instruction = instruction)
        
        messages = [
            {"role": "system", "content": txt + append_prompt}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.9, 
            max_tokens=max_length
        )
        
        return response.choices[0].message.content.strip().replace('\n', '')

    def get_documents(self):
        format_docs = ["Document " + str(i) + ":\n" + str(mem or "") for i,mem in enumerate(self.documents)]

        return "\n".join(format_docs)
        
    # retrieves most relevant documents
    def get_relevant_documents(self, group, k = 3, max_length = 200):
        instruction = "What information do you want to get from relevant documents. Your response here will be embedded and used to search a vector database for relevant text. The new documents will replace all of the old documents. Only state the information you want from available documents do not write anything else."

        response = self.instruct(instruction, group, max_length)
        
        docs = group.get_documents(response,k)

        self.documents = [doc.page_content for doc in docs]
        
    # updates agent's memory
    def update_memory(self, group, max_length = 200):
        self.get_relevant_documents(group)
        
        instruction = "You are not talking to anyone or responding to the conversation. Think to yourself and reflect on what has been said, the task and your future plans. Nobody else can see your Internal Memory."
        new_memory = self.instruct(instruction, group, max_length, append_prompt="New Memory: ")

        self.memory.append(new_memory)

    # called per round for agent to reply to conversation
    def reply(self, group, max_length = 300):
        instruction = "Reply to previous messages in the conversation. DO NOT send more than one message. DO NOT send a message with another name. Send ONE message and no others."
        
        repl = self.instruct(instruction, group, max_length, append_prompt = self.name + ":\n")
        
        return self.name + ":\n" + repl


class Group:
    def __init__(self, task, agents, documents = []):
        
        # list of agents
        # order of agents is order of conversation
        self.agents = agents
        
        # conversation of agents contained in a list
        self.conversation = []

        # task to be discussed from user for agents
        self.task = task

        # documents retrieved, stored as list
        self.documents = documents

        # embedding documents for retrieval
        if len(documents) != 0:
            self.db = Chroma.from_documents(documents=documents, embedding=HuggingFaceEmbeddings())
        else:
            self.db = None
            
    # method to grab the conversation of group
    def get_conv(self):
        str = "Task: " + self.task + "\n"
        for round in self.conversation:
            for i, agent in enumerate(self.agents):
                str += round[i] + "\n\n"
        return str

    # returns list of k most relevant snippets, do .page_content to get text
    def get_documents(self, query, k = 3):
        if(len(self.documents) == 0):
            return []
        return self.db.similarity_search(query, k)

    # round of conversation between agents
    # return tuple of responses per round
    def round(self, max_mem_length = 200, max_reply_length = 200):
        curr = []
        for i, agent in enumerate(self.agents):
            agent.update_memory(self, max_mem_length)
            curr += [agent.reply(self, max_reply_length)]
        self.conversation.append(curr)