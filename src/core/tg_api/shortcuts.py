from collections.abc import Sequence
from typing import Literal

from .exceptions import TgHttpStatusError
from .tg_methods import (
    SendMessageRequest,
    EditMessageReplyMarkupRequest, EditMessageTextRequest,
)
from .tg_types import (
    KeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Message,
    InlineKeyboardButton,
    MessageEntity,
)

InlineKeyboard = Sequence[Sequence[InlineKeyboardButton | dict[str, str]]]
ReplyKeyboard = Sequence[Sequence[KeyboardButton | dict[str, str]]]


def generate_inline_buttons(*buttons: Sequence[Sequence[str, str]]) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for line in buttons:
        buttons_line = []
        for text, callback_data in line:
            buttons_line.append(InlineKeyboardButton(text, callback_data=callback_data))
        keyboard.append(buttons_line)
    return keyboard


def generate_reply_buttons(*buttons: Sequence[str]) -> list[list[KeyboardButton]]:
    keyboard = []
    for line in buttons:
        buttons_line = []
        for text, callback_data in line:
            buttons_line.append(KeyboardButton(text))
        keyboard.append(buttons_line)
    return keyboard


def send_text_message(
        text: str,
        chat_id: int,
        keyboard: InlineKeyboard | ReplyKeyboard | None = None,
        parse_mode: Literal['Markdown', 'MarkdownV2', 'HTML'] | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_thread_id: bool | None = None,
        allow_sending_without_reply: bool | None = None,
) -> Message:
    match keyboard:
        case [[InlineKeyboardButton(), *_], *_]:
            reply_markup = InlineKeyboardMarkup(keyboard)
        case [[KeyboardButton(), *_], *_]:
            reply_markup = ReplyKeyboardMarkup(keyboard)
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
        ignore_to_old_message=True,
) -> Message | None:
    if keyboard is None:
        reply_markup = InlineKeyboardMarkup([[]])
    else:
        reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        message = EditMessageReplyMarkupRequest(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
        ).send().result
    except TgHttpStatusError as ex:
        if ignore_to_old_message and 'too much time has passed since its creation' in str(ex):
            return
    else:
        return message


def edit_text_message(
        chat_id: int,
        message_id: int,
        text: str,
        keyboard: Sequence[Sequence[InlineKeyboardButton]] | Sequence[Sequence[KeyboardButton]] | None = None,
        parse_mode: Literal['Markdown', 'MarkdownV2', 'HTML'] | None = None,
        inline_message_id: str | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        *,
        ignore_exactly_the_same=True,
        ignore_to_old_message=True,
) -> Message | None:
    match keyboard:
        case [[InlineKeyboardButton(), *_], *_]:
            reply_markup = InlineKeyboardMarkup(keyboard)
        case [[KeyboardButton(), *_], *_]:
            reply_markup = ReplyKeyboardMarkup(keyboard)
        case _:
            reply_markup = None

    try:
        message = EditMessageTextRequest(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            inline_message_id=inline_message_id,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
        ).send().result
    except TgHttpStatusError as ex:
        if ignore_exactly_the_same and 'exactly the same' in str(ex):
            return
        if ignore_to_old_message and 'too much time has passed since its creation' in str(ex):
            return
    else:
        return message
