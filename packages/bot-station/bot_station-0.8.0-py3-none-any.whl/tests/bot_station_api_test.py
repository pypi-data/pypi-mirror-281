import logging
import unittest

from fastapi.testclient import TestClient

from bot_station.api.rest.api import BotStationWebApp
from bot_station.api.rest.model.web_app_config import WebAppConfig
from bot_station.data.bot.model.qdrant_config import QdrantConfig
from bot_station.data.bot.model.yandex_cloud_config import YandexCloudConfig
from bot_station.data.bot_station.bot_station_impl import BotStationImpl
from bot_station.data.docs.qdrant_docs_library import QdrantDocsLibrary
from bot_station.domain.bot_station.bot_station import BotStation
from mock_llm import MockLLM

logging.basicConfig(
    format="%(asctime)s.%(msecs)06f %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%d-%m-%Y:%H:%M:%S",
    level=logging.DEBUG,
)


def launch_test_web_app(llm: MockLLM):
    yandex_cloud_config = YandexCloudConfig(
        api_key="",
        folder_id="",
        model_name="",
        model_version=""
    )
    qdrant_config = QdrantConfig(
        qdrant_url=None,
        qdrant_db_path=".data/qdrant",
    )

    bot_station: BotStation = BotStationImpl(yandex_cloud_config=yandex_cloud_config,
                                             qdrant_config=qdrant_config)
    bot_station.llm = llm
    BotStationWebApp.prepare(bot_station=bot_station, config=WebAppConfig())


class BotStationApiTest(unittest.TestCase):
    bot_station_test_client: TestClient
    docs_library = QdrantDocsLibrary(
        collection_name="",
        qdrant_config=QdrantConfig(
            qdrant_url=None,
            qdrant_db_path="./.data/qdrant")
    )
    llm = MockLLM()

    def setUp(self):
        launch_test_web_app(llm=self.llm)
        self.bot_station_test_client = TestClient(BotStationWebApp.api)

    def create(self, bot_id: str, check_response: bool = False):
        response = self.bot_station_test_client.post(
            url="/create",
            json={
                "id": bot_id,
                "name": "name",
                "description": "description",
                "prompt_intro": "You are programmer's assistant",
                "add_external_context_to_prompt": "true",
                "add_messages_history_to_prompt": "true",
                "temperature": 0.6
            }
        )
        logging.debug(f"Response = {response.content}")
        if check_response:
            self.assertEqual(200, response.status_code)

    def delete(self, bot_id: str, check_response: bool = False):
        response = self.bot_station_test_client.delete(url=f"/admin/{bot_id}")
        logging.debug(f"response = {response.content}")
        if check_response:
            self.assertEqual(200, response.status_code)

    def test_train(self):
        bot_id = "test_train"
        self.create(bot_id=bot_id, check_response=False)
        response = self.bot_station_test_client.post(
            url="/train",
            json={
                "bot_id": bot_id,
                "data": "FastAPI is a modern, fast, web framework for building APIs with Python.",
                "source_link": "https://aaa.ru"
            }
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.content) > 0)
        self.delete(bot_id=bot_id, check_response=True)

    def test_train_with_metadata(self):
        bot_id = "test_train_with_metadata"
        self.create(bot_id=bot_id, check_response=False)
        response = self.bot_station_test_client.post(
            url="/train",
            json={
                "bot_id": bot_id,
                "data": "FastAPI is a modern, fast, web framework for building APIs with Python.",
                "source_link": "https://aaa.ru",
                "metadata": {"a": "b"}
            }
        )
        self.assertEqual(200, response.status_code)
        self.delete(bot_id=bot_id, check_response=True)

    def test_train_incorrect_id(self):
        response = self.bot_station_test_client.post(
            url="/train",
            json={
                "bot_id": "-",
                "id": "1",
                "data": "FastAPI is a modern, fast, web framework for building APIs with Python.",
                "source_link": "https://aaa.ru"
            }
        )
        self.assertEqual(404, response.status_code)

    def test_call(self):
        answer = "FastAPI is a modern, web framework"

        bot_id = "test_call"
        self.create(bot_id=bot_id, check_response=False)
        self.llm.set_next_answer(answer)
        response = self.bot_station_test_client.post(
            url="/call",
            json={
                "bot_id": bot_id,
                "chat_id": 1,
                "data": "What is FastAPI?"
            }
        )
        logging.debug(f"response = {response.content}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(answer, response.json()["text"])
        self.delete(bot_id=bot_id, check_response=True)

    def test_update(self):
        bot_id = "test_update"
        self.create(bot_id=bot_id, check_response=False)

        response = self.bot_station_test_client.post(
            url="/update",
            json={
                "id": bot_id,
                "name": "name",
                "description": "description",
                "prompt_intro": "You are programmer's assistant",
                "add_external_context_to_prompt": "true",
                "add_messages_history_to_prompt": "true",
                "temperature": 0.6
            }
        )
        logging.debug(f"response = {response.content}")
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
