from abc import abstractmethod, ABC
from typing import List

from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo


class BotStation(ABC):

    @abstractmethod
    async def create(self, config: BotMetaInfo):
        pass

    @abstractmethod
    async def get_bot(self, bot_id: str) -> Bot | None:
        pass

    @abstractmethod
    async def get_bots_list(self) -> List[BotMetaInfo]:
        pass

    @abstractmethod
    async def delete(self, bot_id: str) -> bool:
        pass

    @abstractmethod
    async def update(self, info: BotMetaInfo):
        pass
