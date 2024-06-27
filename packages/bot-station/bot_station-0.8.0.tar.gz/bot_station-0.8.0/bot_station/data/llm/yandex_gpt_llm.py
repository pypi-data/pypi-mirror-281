from langchain_community.chat_models import ChatYandexGPT
from langchain_core.tracers import langchain

from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.domain.llm.llm import LLM


class YandexGPTLLM(LLM):

    def __init__(self, yandex_cloud_config: YandexCloudConfig):
        langchain.debug = False
        self.yandex_cloud_config = yandex_cloud_config

    async def call(self, query: str, temperature: float = 0.6) -> str:
        gpt = ChatYandexGPT(
            api_key=self.yandex_cloud_config.api_key,
            folder_id=self.yandex_cloud_config.folder_id,
            temperature=temperature,
            model_name=self.yandex_cloud_config.model_name,
            model_version=self.yandex_cloud_config.model_version,
            verbose=True,
        )
        return gpt.invoke(query).content
