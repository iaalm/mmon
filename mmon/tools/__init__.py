from os import environ

from langchain.agents import Tool, initialize_agent
from langchain.chains import LLMMathChain
from langchain.utilities import BingSearchAPIWrapper
from loguru import logger


def load_tools(llm, verbose_level=0):
    tools = [
        Tool(
            name="Calculator",
            func=LLMMathChain.from_llm(llm=llm, verbose=verbose_level >= 3).run,
            description="useful for when you need to answer questions about math",
        ),
    ]

    if "BING_SUBSCRIPTION_KEY" in environ:
        url = environ.get(
            "BING_SEARCH_URL", "https://api.bing.microsoft.com/v7.0/search"
        )
        key = environ["BING_SUBSCRIPTION_KEY"]
        search = BingSearchAPIWrapper(bing_subscription_key=key, bing_search_url=url)
        tools.append(
            Tool(
                name="BingSearch",
                description="Search Bing for recent results.",
                func=search.run,
            )
        )

    logger.info("Loaded tools: {}", [tool.name for tool in tools])
    return tools
