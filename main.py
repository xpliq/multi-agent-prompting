import asyncio
from dotenv import load_dotenv
import os
from openai import OpenAI, AsyncOpenAI
from Agents import Agent, Group


    
async def main():

    load_dotenv()
    api_key = os.getenv('OPEN_API_KEY')

    client = AsyncOpenAI(api_key = api_key)
    
    # Initialize agents
    agents = []
    
    user_prompt = "Make a recipe for a cheeseburger and fries"

    agent_0 = Agent(client ,"Agent 0", "", False)
    expanded_prompt, topics_list, roles = await agent_0.process_prompt_to_roles(user_prompt)
    print(expanded_prompt, "\n")
    print(topics_list, "\n")
    print(roles)
    
#     task = f"""
# "You will be tasked to collaborate with another Agent, one at a time, about a given prompt. This means that you will converse with agents one at a time to further develop and refine your thoughts and knowledge about the given prompt. You are only knowledgeable in your expertise and you are curious to learn from the other experts about the given prompt. You are in a group with other your coworkers. Introduce yourself and your specialty/expertise. You all will be given a request from your Boss. You all are to collaborate with each other, sharing your expertise, to accomplish the task that the boss provided. Once you begin collaborating, you are all to stay on task and work towards the given prompt from your Boss. Do not respond in furture tense. Your responses should assist with the prompt given your expertise, it should not be your future plans. Your boss will read your conversation history, so ensure that your responses are detailed. Remember to ask questions and look for answers within the conversation history. You are not answering the task, you are collaborating with other experts to gain insight on how to complete the given task.

# Here is the assigned prompt: {expanded_prompt}.
# """
    
#     for i, role in enumerate(roles, start=1):
#         agents.append(Agent(client, f"Agent {i}", role, task))

#     # create agent collaboration path
#     agent_names = [agent.name for agent in agents]
#     for agent in agents:
#         agent.generate_path(agent_names)
    
#     group = Group(task, agents)
    
#     await group.conduct_collaborations()  # Specify the number of rounds

    
if __name__ == "__main__":
    asyncio.run(main())