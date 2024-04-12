import asyncio
from dotenv import load_dotenv
import os
from openai import OpenAI, AsyncOpenAI
from Agents import Agent, Group

# method to write the entire conversation between group of agents to a file
def write_conversations_to_file(agents, topics, filename = "conversation_histories.txt"):
    with open(filename, 'w') as file:
        for agent, topic in zip(agents, topics):
            conversation_history = agent.get_conversation_history()
            file.write(f"Conversation History for {agent.name}, and expert in {topic}:\n")
            file.write(conversation_history)
    
    
async def main():

    load_dotenv()
    api_key = os.getenv('OPEN_API_KEY')
    client = AsyncOpenAI(api_key = api_key)
    
    # Initialize agent list
    agents = []
    
    user_prompt = "Give me a recipe for a cheeseburger and fries"

    # creating an agent 0 to perform initial tasks of generating roles for agents
    agent_0 = Agent(client ,"Agent 0", "", False)
    expanded_prompt, topics_list, roles = await agent_0.process_prompt_to_roles(user_prompt)
    print(expanded_prompt, "\n")
    print(topics_list, "\n")
    print(roles)
    
    # structured task
    # todo : I think I should place this somewhere in the Agents library. for now, this stays
    task = f"""
You will be tasked to collaborate with another Agent, one at a time, about a given prompt. This means that you will converse with agents one at a time to further develop and refine your thoughts and knowledge about the given prompt. You are only knowledgeable in your expertise and you are curious to learn from the other experts about the given prompt. You are in a group with other your coworkers. Introduce yourself and your specialty/expertise. You all will be given a request from your Boss. You all are to collaborate with each other, sharing your expertise, to accomplish the task that the boss provided. Once you begin collaborating, you are all to stay on task and work towards the given prompt from your Boss. Do not respond in furture tense. Your responses should assist with the prompt given your expertise, it should not be your future plans. Your boss will read your conversation history, so ensure that your responses are detailed. Remember to ask questions and look for answers within the conversation history. You are not answering the task, you are collaborating with other experts to gain insight on how to complete the given task.

Here is the assigned prompt: {expanded_prompt}.
"""
    # generating agents given a list of roles generated from agent 0
    for i, role in enumerate(roles, start=1):
        agents.append(Agent(client, f"Agent {i}", role, task))

    # create agent collaboration path
    agent_names = [agent.name for agent in agents]
    for agent in agents:
        agent.generate_path(agent_names)
    
    # create group of agents to collaborate within
    group = Group(task, agents)
    # starts collaboration
    await group.conduct_collaborations() 
    # saving this for possible RAG usage
    await write_conversations_to_file(agents, topics_list)
    
if __name__ == "__main__":
    asyncio.run(main())