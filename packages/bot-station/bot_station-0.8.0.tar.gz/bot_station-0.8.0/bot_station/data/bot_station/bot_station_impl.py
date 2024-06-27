import logging
from typing import List

from bot_station.data.bot.chat_message_storage_impl import ChatMessageStorageImpl
from bot_station.data.bot.model.qdrant_config import QdrantConfig
from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.data.bot.rag_bot_impl import RAGBot
from bot_station.data.bot_station.bot_registry_impl import BotRegistryImpl
from bot_station.data.docs.qdrant_docs_library import QdrantDocsLibrary
from bot_station.data.llm.yandex_gpt_llm import YandexGPTLLM
from bot_station.domain.base.const import message_history_path
from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot_station.bot_station import BotStation
from bot_station.domain.docs.docs_library import DocsLibrary


class BotStationImpl(BotStation):
    __in_memory_bots: dict[str, RAGBot] = {}

    def __init__(self,
                 yandex_cloud_config: YandexCloudConfig,
                 qdrant_config: QdrantConfig,
                 ):
        self.bot_registry = BotRegistryImpl()
        self.yandex_cloud_config = yandex_cloud_config
        self.llm = YandexGPTLLM(yandex_cloud_config=self.yandex_cloud_config)
        self.qdrant_config = qdrant_config

    async def create(self, bot_info: BotMetaInfo):
        logging.debug(f"create {bot_info}")
        bot_with_same_id = await self.bot_registry.get(bot_id=bot_info.id)
        if bot_with_same_id is None:
            meta_info = await self.bot_registry.create(bot_info)
            return meta_info
        else:
            raise Exception(f"Bot with id '{bot_info.id}' already exists!")

    async def get_bot(self, bot_id: str) -> Bot | None:
        logging.debug(f"Get {bot_id})")
        if bot_id is None:
            raise Exception("Bot id is None!")
        bot = self.__in_memory_bots.get(bot_id, None)
        if bot is not None:
            return bot

        meta = await self.bot_registry.get(bot_id)
        if meta is None:
            logging.warning(f"No {bot_id} in registry!")
            return None
        else:
            docs_library = QdrantDocsLibrary(
                collection_name=meta.id,
                qdrant_config=self.qdrant_config
            )
            bot = RAGBot(
                message_storage=ChatMessageStorageImpl(root_message_history_path=message_history_path),
                llm=self.llm,
                docs_source=docs_library,
                meta=meta
            )
            await docs_library.load()
            self.__in_memory_bots[bot_id] = bot
            return bot

    async def get_bots_list(self) -> List[BotMetaInfo]:
        logging.debug("get_bots_list")
        return await self.bot_registry.get_all()

    async def delete(self, bot_id: str) -> bool:
        logging.debug(f"Delete {bot_id}")
        bot: RAGBot | None = await self.get_bot(bot_id=bot_id)
        logging.debug(f"Delete bot {bot}")
        if bot is not None:
            if isinstance(bot, RAGBot) and isinstance(bot.docs_source, DocsLibrary):
                logging.debug(f"Clear library {bot_id}")
                await bot.docs_source.load()
                await bot.docs_source.clear()
                await bot.docs_source.close()
            await self.bot_registry.delete(bot_id=bot_id)
            self.__in_memory_bots.pop(bot_id, None)
            return True
        else:
            logging.warning(f"No {bot_id} in registry")
            return False

    async def update(self, info: BotMetaInfo):
        logging.debug(f"Update {info}")
        await self.bot_registry.update(info)
        # reload bot
        bot = self.__in_memory_bots.pop(info.id, None)
        if bot is not None:
            logging.debug(f"Close {bot.meta}")
            await bot.docs_source.close()
