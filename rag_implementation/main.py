from dotenv import load_dotenv
import os
from openai import OpenAI
from AgentsRAG import Agent, Group
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

def main():

    load_dotenv()
    api_key = os.getenv('OPEN_API_KEY')
    client = OpenAI(api_key = api_key)
    
    # testing LLM to RAG a document (conversation history from agents)
    loader = TextLoader("./conv_histories/10agentWindTurbines.txt")
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    agent_1 = Agent(client, "Richard", "You are Richard, a ChatBot. You will be provided a reference of resources for you to use. You will be asked to respond to a user prompt. Using your reference documents, respond to the prompt. Do not mention anything about the reference documents in your response.")
    
    group_of_agents = Group("How can we develop Wind Turbines?", [agent_1], documents=splits)
    
    group_of_agents.round(max_mem_length=256, max_reply_length=512)
    
    print(group_of_agents.get_conv())
    
if __name__ == "__main__":
    main()