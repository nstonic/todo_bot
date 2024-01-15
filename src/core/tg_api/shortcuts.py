from typing import Union

from . import TgHttpStatusError
from .tg_types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply, Message,
)
from .tg_methods import (
    SendMessageRequest,
    EditMessageTextRequest,
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
) -> Message:
    return SendMessageRequest(
        text=text,
        chat_id=chat_id,
        reply_markup=reply_markup,
        **message_sending_kwargs,
    ).send().result


def edit_text_message(
        chat_id: int,
        message_id: int,
        text: str,
        reply_markup: ReplyMarkup = None,
        **message_sending_kwargs,
) -> Message | None:
    try:
        message = EditMessageTextRequest(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
            **message_sending_kwargs,
        ).send().result
    except TgHttpStatusError as ex:
        if 'exactly the same' in str(ex):
            pass
    else:
        return message
