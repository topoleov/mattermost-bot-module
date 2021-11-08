from typing import List
from enum import Enum
from collections import ChainMap

from api.mattermost.v4.models import Post
from core.sqllib.sql_mattermost import SQLMattermost
import config

# Список функций-обработчиков событий типа 'posted'
processors = []
_ACTIVATED_PROCESSORS: List[str] = []


class MessageProcessorsKinds(Enum):
    """Названия доступных обработчиков сообщений
    Ожидается что в настройках процессоры событий типа `posted`
    перечислены именно под этими именами
    """
    # Сохранить сообщение
    SAVE = 'save'
    # Ответить на сообщение
    RESPONSE = 'response'


def _save_message_event_processor(event, ws=None):
    """Обработчик сообщения.
    Сохраняет переданный пост в базе.
    """

    post = event['data']['post']

    if config.MATTERMOST_FILTER_MESSAGES_CONTAINS in post['event']:
        mm_db_connect = SQLMattermost(
            db_name=config.DATABASE_NAME,
            db_username=config.DATABASE_USERNAME,
            db_password=config.DATABASE_PASSWORD,
            db_host=config.DATABASE_HOST,
            db_port=config.DATABASE_PORT,
        )
        mm_db_connect.save_message(
            Post(
                id=post['id'],
                filter_key=config.MATTERMOST_FILTER_MESSAGES_CONTAINS,  # filter_key,
                channel_id=post['channel_id'],
                channel_display_name=event['data']['channel_display_name'],
                user_id=post['user_id'],
                sender_name=event['data']['sender_name'],
                create_at=post['create_at'],
                message=post['message'],
            )
        )


def _response_to_sender_event_processor(event, ws=None):
    """Обработчик сообщений.
    Отвечает отправителю .
    """


# Проверяем указаны ли в настройках события типа 'posted'
__current_module = __name__.split('.')[-1]
_PROCESSORS_FOR_EVENTS_MAP = ChainMap(*config.MATTERMOST_TARGET_EVENTS)

# Если да то активируем процессоры указынные для этого типа событий
if __current_module in config.MATTERMOST_TARGET_EVENTS:
    _ACTIVATED_PROCESSORS = config.MATTERMOST_TARGET_EVENTS[__current_module]

# Регистрируем процессоры обеспечивающие логику сохранения
if MessageProcessorsKinds.SAVE.value in _ACTIVATED_PROCESSORS:
    processors.append(_save_message_event_processor)

# Регистрируем процессоры обеспечивающие логику требующую ответов на сообщения
if MessageProcessorsKinds.RESPONSE.value in _ACTIVATED_PROCESSORS:
    processors.append(_response_to_sender_event_processor)

