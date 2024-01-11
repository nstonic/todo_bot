from typing import Union

from .tg_types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
)
from .tg_methods import (
    SendMessageRequest,
    SendMessageResponse, GetUpdatesRequest,
)

ReplyMarkup = Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
]


def send_text_message(
        text: str,
        chat_id: int,
        reply_markup: ReplyMarkup = None,
        **message_sending_kwargs,
) -> SendMessageResponse:
    return SendMessageRequest(
        text=text,
        chat_id=chat_id,
        reply_markup=reply_markup,
        **message_sending_kwargs,
    ).send()
