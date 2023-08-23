from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from os import environ
from wwwml.tools import load_tools
import openai


INIT_PROMPT = "My Linux server is slow. Use providered function to check the server."

if __name__ == "__main__":
    if "OPENAI_API_MODEL" in environ:
        llm = ChatOpenAI(temperature=0, model=environ["OPENAI_API_MODEL"])
    elif "OPENAI_API_DEPLOYMENT" in environ:
        llm = ChatOpenAI(temperature=0, deployment_id=environ["OPENAI_API_DEPLOYMENT"])
    else:
        raise ValueError("Need to specify OPENAI_API_MODEL or OPENAI_API_DEPLOYMENT")
    agent = initialize_agent(
        load_tools(llm), llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
    )
    agent.run(INIT_PROMPT)
