import logging
from typing import List

from bot_station.data.bot.rag_prompt_samples import RAGPromptSamples
from bot_station.domain.bot.bot import Bot
from bot_station.domain.bot.chat_message_storage import ChatMessageStorage
from bot_station.domain.bot.model.bot_meta_info import BotMetaInfo
from bot_station.domain.bot.model.lm_call_result import CallResult
from bot_station.domain.bot.model.lm_chat_message import LMBotMessage, LmChatMessage
from bot_station.domain.bot.model.lm_chat_message import LMUserMessage
from bot_station.domain.docs.docs_source import DocsSource
from bot_station.domain.docs.model.document import Document
from bot_station.domain.docs.model.documents_search_result import DocumentsSearchResult
from bot_station.domain.llm.llm import LLM


class RAGBot(Bot):

    def __init__(
            self,
            meta: BotMetaInfo,
            llm: LLM,
            docs_source: DocsSource,
            message_storage: ChatMessageStorage = None,
            prompt_samples: RAGPromptSamples = RAGPromptSamples()
    ):
        self.message_storage = message_storage
        self.docs_source = docs_source
        self.llm = llm
        self.meta = meta
        self.prompt_samples = prompt_samples
        self.__is_loaded = False

    async def call(self, question: LMUserMessage) -> CallResult:
        logging.debug(f"call({question})")

        prompt_with_question = self.meta.prompt_intro + "\n"

        # 1. Add previous messages to prompt
        if self.meta.add_messages_history_to_prompt and self.message_storage is not None:
            message_history: List[LmChatMessage] = \
                await self.message_storage.get_history(chat_id=question.chat_id, limit=10)
            if len(message_history) >= 2:
                prompt_with_question = prompt_with_question + f"\n{self.prompt_samples.message_history_title}\n"
                for m in message_history:
                    prompt_with_question = prompt_with_question + "- " + m.text + "\n"

        # 2. Add context to prompt
        relevant_docs: List[Document] = []
        if self.meta.add_external_context_to_prompt:
            await self.docs_source.load()
            search_docs_result: DocumentsSearchResult = await self.docs_source.get_relevant_docs(
                query=question.text,
                min_score=self.meta.min_extract_relevant_docs_score,
                limit=self.meta.limit_extract_relevant_docs,
            )
            relevant_docs: List[Document] = [search_docs_result.docs[key] for key in search_docs_result.docs]
            await self.docs_source.close()
            if len(relevant_docs) > 0:
                prompt_with_question = (
                        prompt_with_question
                        + f"\n{self.prompt_samples.relevant_docs_title}\n"
                )
                for d in relevant_docs:
                    prompt_with_question = prompt_with_question + f"\n{d.data}"

        prompt_with_question = (prompt_with_question + f"\n{self.prompt_samples.user_message_title}" + question.text)

        response = await self.llm.call(prompt_with_question)

        answer = LMBotMessage(text=response, chat_id=question.chat_id)

        if self.message_storage is not None:
            await self.message_storage.add_user_message(chat_id=question.chat_id, message=question)
            await self.message_storage.add_bot_message(chat_id=question.chat_id, message=answer)

        return CallResult(answer=answer, relevant_docs=relevant_docs)
