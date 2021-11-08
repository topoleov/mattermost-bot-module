#!/usr/bin/env python
"""
mattermost - модуль для работы с http-api месенджера mattermost
"""

from api.mattermost.v4 import MattermostHttpApiV4


def get_api_client_for_version(version: int = 4):
    """
    Возвращает соотв. клас для апи указнной версии
    """

    try:
        return {
            4: MattermostHttpApiV4
        }[int(version)]
    except KeyError:
        raise NotImplementedError(f"Клас для хттп апи версии {version} не реализован!")
    except ValueError:
        raise ValueError("Версия АПИ должна быть цифрой")

