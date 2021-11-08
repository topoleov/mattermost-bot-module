import abc


class MattermostHttpApiVersion(metaclass=abc.ABCMeta):
    """Абстрактный класс-интерфейс для работы с разными версиями Mattermost API
    """
    @classmethod
    @abc.abstractmethod
    def get_all_messages_from_channel(
            cls,
            channel_id: str = None,
            per_page: int = 60,
            page: int = 0,
    ):
        ...

    @classmethod
    @abc.abstractmethod
    def send_message(
        cls,
        channel_id: str = None,
        message: str = None,
        root_id: str = ""
    ):
        ...
