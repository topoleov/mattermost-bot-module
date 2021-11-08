from typing import List
from enum import Enum
from collections import ChainMap

import config
from logger import logger

# Список функций-обработчиков событий типа 'posted'
processors = []
_ACTIVATED_PROCESSORS: List[str] = []


class HelloProcessorsKinds(Enum):
    """Названия доступных обработчиков события `hello`
    Ожидается что в настройках процессоры событий типа `posted`
    перечислены именно под этими именами
    """
    # Записываем подключившихся/отключившихся к вебсокет апи
    LOG = 'log'


def _log_connected_users(event, ws=None):
    user_id = event.get('broadcast', {}).get('user_id')
    logger.info(f"Новое соединение к вэбсокету mattermost, user_id={user_id}")


# Проверяем указаны ли в настройках события типа 'hello'
__current_module = __name__.split('.')[-1]
_PROCESSORS_FOR_EVENTS_MAP = ChainMap(*config.MATTERMOST_TARGET_EVENTS)

# Если да то активируем процессоры указынные для этого типа событий
if __current_module in _PROCESSORS_FOR_EVENTS_MAP:
    _ACTIVATED_PROCESSORS = _PROCESSORS_FOR_EVENTS_MAP[__current_module]

# Регистрируем нужные процессоры
if HelloProcessorsKinds.LOG.value in _ACTIVATED_PROCESSORS:
    processors.append(_log_connected_users)
