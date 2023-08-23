from langchain.agents import initialize_agent, Tool
from langchain import LLMMathChain, OpenAI
from wwwml.tools.sysstat import free, iostat, mpstat


def load_tools(llm, verbose=False):
    return [
        Tool(
            name="Calculator",
            func=LLMMathChain.from_llm(llm=llm, verbose=verbose).run,
            description="useful for when you need to answer questions about math",
        ),
        # free,
        iostat,
        # mpstat,
    ]
