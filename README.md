# 🗺 ️Multi Agent Prompting for LLMs 🗺️
##### _A multi agent approach to prompt engineering_ 


![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

Multi-Agent Prompting (MAP) is a system that can be leveraged by developers to effectively expand and structure existing content or information. 

- Specialized LLM Agents
- Multi-Agent Collaboration and Feedback
- Prompt Engineering

## Process

- User query/prompt is given
```
User: "Create a plan to make wind turbines in Spokane Washington. Include the necessary math and formulas needed."
```
- Roles are generated and Agents are initialized
```
Expanded Prompt: "Create a detailed plan for the design, construction, and implementation of wind turbines in Spokane, Washington, including specific calculations, measurements, and numerical data. Consider the average wind speed in Spokane, the optimal height and size for the turbines, and the number of turbines needed to generate a significant amount of power. Additionally, outline the necessary permits and environmental considerations for the project."

Topics: ["Wind speed in Spokane", "Optimal height and size of turbines", "Number of turbines needed", "Power generation calculations", "Specific measurements for design", "Numerical data", "Permits for the project", "Environmental considerations."]

Roles: ["You are Agent 1. You are an expert in Wind speed in Spokane.", "You are Agent 2. You are an expert in Optimal height and size of turbines.", "You are Agent 3. You are an expert in Number of turbines needed.", "You are Agent 4. You are an expert in Power generation calculations.", "You are Agent 5. You are an expert in Specific measurements for design.", "You are Agent 6. You are an expert in Numerical data.", "You are Agent 7. You are an expert in Permits for the project.", "You are Agent 8. You are an expert in Environmental considerations."]
```
- Agent collaboration is conducted
```
Agent 2: Greetings, I am an expert in Optimal height and size of turbines...
Agent 5: Greetings, I am an expert in Specific measurements for design...

Agent 1: Hello, I am an expert in Wind speed in Spokane...
Agent 7: Greetings, I am an expert in Permits for the project...
```


The collaboration between the agents is saved as their conversation history in which could be used for things such as retrieval augmented generation (RAG) for response generation. 


## FAQ
**Why is there a separate implementation(s) for the Agents library?**
I used a different model (Mixtral) for the RAG implementation as well as most of my testing. The Agents file was mainly tested using OpenAI and it ended up just being a proof of concept.

## Paper
*A research paper was written for this project however, it is not publically published/available
