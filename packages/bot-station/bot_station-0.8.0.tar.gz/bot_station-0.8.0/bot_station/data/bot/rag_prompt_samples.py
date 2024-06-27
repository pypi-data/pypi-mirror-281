from dataclasses import dataclass


@dataclass
class RAGPromptSamples:
    message_history_title: str = "Переписка с пользователем: "
    relevant_docs_title: str = "Для ответа используй следующую информацию: "
    user_message_title: str = "Сообщение пользователя: "
