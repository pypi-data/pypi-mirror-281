import logging
import os
import typing as t

from langchain_anthropic import ChatAnthropic
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from rich.logging import RichHandler


def setup_logger():
    handler = RichHandler(show_time=False, show_path=False)
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger("local_workspace")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = setup_logger()


def get_llm() -> t.Union[ChatOpenAI, AzureChatOpenAI, ChatAnthropic]:
    helicone_api_key = os.environ.get("HELICONE_API_KEY")
    if os.environ.get("ANTHROPIC_API_KEY"):
        # if helicone_api_key:
        #     return ChatAnthropic(
        #         model_name="claude-3-5-sonnet-20240620",
        #         anthropic_api_url="https://anthropic.helicone.ai/v1",
        #         default_headers={
        #             "Helicone-Auth": f"Bearer {helicone_api_key}",
        #         },
        #         timeout=10,
        #         api_key=os.environ.get("ANTHROPIC_API_KEY"),
        #     )
        return ChatAnthropic(model_name="claude-3-5-sonnet-20240620")
    if os.environ.get("OPENAI_API_KEY"):
        if helicone_api_key:
            return ChatOpenAI(
                model="gpt-4-turbo",
                base_url="https://oai.helicone.ai/v1",
                default_headers={
                    "Helicone-Auth": f"Bearer {helicone_api_key}",
                },
            )
        return ChatOpenAI(model="gpt-4-turbo")
    if os.environ.get("AZURE_OPENAI_API_KEY"):
        return AzureChatOpenAI(model="test")
    raise ValueError("no model is found")
