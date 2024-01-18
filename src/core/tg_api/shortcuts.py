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

InlineKeyboardSchema = list[list[InlineKeyboardButton | dict[str, str]]]
ReplyKeyboardSchema = list[list[KeyboardButton | dict[str, str]]]
KeyboardMarkup = InlineKeyboardMarkup | ReplyKeyboardMarkup
KeyboardSchema = InlineKeyboardSchema | ReplyKeyboardSchema


def send_text_message(
        text: str,
        chat_id: int,
        keyboard: KeyboardMarkup | KeyboardSchema | None = None,
        *,
        parse_mode: Literal['Markdown', 'MarkdownV2', 'HTML'] | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_thread_id: bool | None = None,
        allow_sending_without_reply: bool | None = None,
) -> Message:
    return SendMessageRequest(
        text=text,
        chat_id=chat_id,
        reply_markup=generate_reply_markup(keyboard),
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
        keyboard: InlineKeyboardSchema | InlineKeyboardMarkup | None,
        *,
        inline_message_id: int | None = None,
        ignore_to_old_message=True,
) -> Message | None:
    match keyboard:
        case InlineKeyboardMarkup():
            reply_markup = keyboard
        case None:
            reply_markup = InlineKeyboardMarkup([[]])
        case _:
            reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        message = EditMessageReplyMarkupRequest(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
            inline_message_id=inline_message_id,
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
        keyboard: KeyboardMarkup | KeyboardSchema | None = None,
        *,
        parse_mode: Literal['Markdown', 'MarkdownV2', 'HTML'] | None = None,
        inline_message_id: str | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        ignore_exactly_the_same: bool = True,
        ignore_to_old_message: bool = True,
) -> Message | None:
    try:
        message = EditMessageTextRequest(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=generate_reply_markup(keyboard),
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


def generate_reply_markup(keyboard: KeyboardMarkup | KeyboardSchema | None = None) -> KeyboardMarkup:
    match keyboard:
        case InlineKeyboardMarkup() | ReplyKeyboardMarkup() | None:
            reply_markup = keyboard
        #  Задача следующих паттернов - распознать, какую клавиатуру нужно создать.
        #  Валидацией самих кнопок займутся модели маркапов.
        case [[{'text': str(), 'callback_data': str()}, *_], *_] | [[InlineKeyboardButton(), *_], *_]:
            reply_markup = InlineKeyboardMarkup(keyboard)
        case [[{'text': str()}, *_], *_] | [[KeyboardButton(), *_], *_]:
            reply_markup = ReplyKeyboardMarkup(keyboard)
        case keyboard if keyboard == [[]]:  # Ни под один из паттернов не подходит, но и на ошибку не тянет
            reply_markup = None  # Надо подумать
        case _:
            raise ValueError('Wrong keyboard format')
    return reply_markup
