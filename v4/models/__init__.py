from api.response import ResponseObject
from api.response.fields import (
    IntegerField,
    StringField,
    SqlSafeStringField,
)


class Post(ResponseObject):
    """Модель Пост
    """
    id: int = StringField(required=True, nullable=False)
    filter_key: str = StringField(required=False, nullable=True)
    channel_id: str = StringField(required=True, nullable=False)
    channel_display_name: str = StringField(required=False, nullable=True)
    user_id: str = StringField(required=True, nullable=False)
    sender_name: str = StringField(required=False, nullable=True)
    create_at: str = IntegerField(required=False, nullable=True)
    message: str = StringField(required=True, nullable=False)
    # message: str = SqlSafeStringField(required=True, nullable=False)
