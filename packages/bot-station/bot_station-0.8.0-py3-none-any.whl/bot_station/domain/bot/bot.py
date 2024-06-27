from abc import abstractmethod, ABC

from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot.model.lm_call_result import CallResult
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage


class Bot(ABC):
    meta: BotMetaInfo

    @abstractmethod
    async def call(self, question: LMUserMessage) -> CallResult:
        pass
