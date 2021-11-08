from typing import Dict
from urllib.error import HTTPError

import requests

import config
from core.utils import retry_w_jitter
from api.mattermost.abc import MattermostHttpApiVersion


class MattermostHttpApiV4(MattermostHttpApiVersion):
    """Предоставляет основные используемые методы для работы с HTTP API MatterMost v4
    """
    headers = {"Authorization": f"Bearer {config.MATTERMOST_TOKEN}"}

    # Исключения для ожидаемых ошибок
    expected_exceptions = TimeoutError, HTTPError, ConnectionError,

    class URLS:
        """Коллекция используемых урлов Mattermost API v4
        """
        _http_host = config.MATTERMOST_HTTP_HOST
        _api_location = _http_host + config.MATTERMOST_API_LOCATION

        # Routes
        messages_from_channel: str = _api_location + "/channels/{}/posts"
        send_message: str = _api_location + '/posts'

    @classmethod
    @retry_w_jitter(exception_classes=expected_exceptions)
    def get_all_messages_from_channel(
            cls,
            channel_id: str = None,
            per_page: int = 60,
            page: int = 0,
    ) -> Dict:
        """
        Запрашивает из апишки mattermost историю сообщений указанного канала.
        """
        resp = requests.get(
            url=cls.URLS.messages_from_channel.format(channel_id),
            params={'per_page': per_page, 'page': page},
            headers=cls.headers,
        )
        return resp.json()

    @classmethod
    @retry_w_jitter(exception_classes=expected_exceptions)
    def send_message(
            cls,
            channel_id: str = None,
            message: str = None,
            root_id: str = ""
    ) -> Dict:
        """
        Отправить сообщение
        """
        upload_file_ids = []

        # отправка сообщения
        data = {
            "channel_id": channel_id,
            "message": message,
            "root_id": root_id,
            "file_ids": upload_file_ids,
            "props": {
            }
        }

        resp = requests.post(
            url=cls.URLS.send_message, json=data, headers=cls.headers
        )
        return resp.json()
