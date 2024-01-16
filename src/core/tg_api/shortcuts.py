from typing import Union, Literal

from .exceptions import TgHttpStatusError
from .tg_types import (
    KeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    Message,
    InlineKeyboardButton,
    MessageEntity,
)
from .tg_methods import (
    SendMessageRequest,
    EditMessageReplyMarkupRequest,
)

ReplyMarkup = Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
]

Keyboard = Union[
    list[list[InlineKeyboardButton]],
    list[list[KeyboardButton]]
]


def send_text_message(
        text: str,
        chat_id: int,
        keyboard: Keyboard | None = None,
        parse_mode: Literal['MarkdownV2', 'HTML', 'Markdown'] | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_thread_id: bool | None = None,
        allow_sending_without_reply: bool | None = None,
) -> Message:
    match keyboard:
        case [[InlineKeyboardButton(), *_], *_]:
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        case [[KeyboardButton(), *_], *_]:
            reply_markup = ReplyKeyboardMarkup(inline_keyboard=keyboard)
        case _:
            reply_markup = None
    return SendMessageRequest(
        text=text,
        chat_id=chat_id,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
        entities=entities,
        disable_web_page_preview=disable_web_page_preview,
        disable_notification=disable_notification,
        protect_content=protect_content,
        message_thread_id=message_thread_id,
        allow_sending_without_reply=allow_sending_without_reply,
    ).send().result


def edit_inline_keyboard(
        chat_id: int,
        message_id: int,
        keyboard: list[list[InlineKeyboardButton]] | None,
        *,
        ignore_exactly_the_same=False,
) -> Message | None:
    if keyboard is None:
        reply_markup = InlineKeyboardMarkup(inline_keyboard=[[]])
    else:
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    try:
        message = EditMessageReplyMarkupRequest(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
        ).send().result
    except TgHttpStatusError as ex:
        if ignore_exactly_the_same and 'exactly the same' in str(ex):
            return
        if 'Message is not modified' in str(ex):
            return
    else:
        return message
