import websockets
import json

import config
from logger import logger
from core.messengers.mattermost import event_processors
from core.utils import import_by_string


async def handle_events():
    """
    Диспатчер слушает события транслируемые по ws-api mattermost.
    На указанные в конфиге типы событий активируются процессоры
    соответствующих типов из модуля `core.messengers.mattermost.event_processors`
    :raises:
        websockets.exceptions.InvalidStatusCode: скорее всего 404, не правильно указан url в конфиге
        websockets.exceptions.ConnectionClosedError: Скорее всего не пускает по указанному токену.
    """
    logger.info('Подключаюсь к MatterMost по ws...')
    async with websockets.connect(config.MATTERMOST_WS_URL) as ws:
        logger.info('Успешно')
        logger.info('Авторизуюсь в MatterMost...')
        message = json.dumps({
            "seq": 1,
            "action": "authentication_challenge",
            "data":
                {
                    "token": config.MATTERMOST_TOKEN
                }
        })
        await ws.send(message)
        logger.info('Успешно')

        while not ws.closed:
            event = await ws.recv()
            # добавлен .encode("utf8", errors="ignore") из-за ошибок кодировки latin-1
            event = json.loads(event.encode("utf8", errors="ignore"))
            if 'data' in event and 'post' in event['data']:
                # `post` в объекте `data` приходит строкой
                event['data']['post'] = post = json.loads(event['data']['post'])

                # слушаем только указанные каналы
                if post['channel_id'] not in config.MATTERMOST_LISTEN_CHANNELS:
                    continue

            # загружаем процессоры соответствующие типу события
            event_type = event.get('event', '_')
            try:
                target_event_processors_module_path = '.'.join([event_processors.__spec__.name, event_type])
                target_event_processors_module = import_by_string(target_event_processors_module_path)
            except AttributeError:
                # Обработка событий такого типа не предусмотрена
                continue
            processors = getattr(target_event_processors_module, 'processors', [])
            # прогоняем событие через каждый из них
            for event_proc in processors:
                event_proc(event, ws)


