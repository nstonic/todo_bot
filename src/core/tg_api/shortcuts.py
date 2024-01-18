from types import NoneType
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

InlineKeyboardSchema = list[list[InlineKeyboardButton | dict[str, str] | tuple[str, str]]]
ReplyKeyboardSchema = list[list[KeyboardButton | dict[str, str] | str]]
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
            reply_markup = generate_reply_markup(keyboard)

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


def generate_reply_markup(keyboard: KeyboardMarkup | KeyboardSchema | None = None) -> KeyboardMarkup | None:
    """Generate InlineKeyboardMarkup or KeyboardMarkup automatically.

    @param keyboard: Keyboard given as:
        list of lists of Button instances:
            [[InlineKeyboardButton(text='Hello!', callback_data='hello')]] -> InlineKeyboadMarkup
            [[KeyboardButton(text='Hello!')]] -> ReplyKeyboardMarkup
        list of lists of dictonaries:
            [[{'text': 'Hello!', 'callback_data': 'hello', **kwargs}]] -> InlineKeyboadMarkup
            [[{'text': 'Hello!', **kwargs}]] -> ReplyKeyboardMarkup
        list of lists of tuples. Only text and callback_data arguments is using:
            [[('Hello!', 'hello')]] -> InlineKeyboadMarkup
        list of lists of strings. Only text argument is using:
            [['Hello!']] -> ReplyKeyboardMarkup
    """
    inline_buttons_kwargs = {
        'url',
        'callback_data',
        'web_app',
        'login_url',
        'switch_inline_query',
        'switch_inline_query_current_chat',
        'switch_inline_query_chosen_chat',
        'callback_game',
        'pay',
    }
    reply_buttons_kwargs = {
        'request_users',
        'request_chat',
        'request_contact',
        'request_location',
        'request_poll',
        'web_app',
    }
    match keyboard:
        case InlineKeyboardMarkup() | ReplyKeyboardMarkup() | None:
            return keyboard

        case [[InlineKeyboardButton(), *_], *_]:
            return InlineKeyboardMarkup(keyboard)
        case [[{'text': str(), **kwargs}, *_], *_] if set(kwargs.keys()) & inline_buttons_kwargs:
            return InlineKeyboardMarkup(keyboard)
        case [[(str(), str()), *_], *_]:
            buttons = []
            for line in keyboard:
                buttons_line = []
                for text, callback_data in line:
                    buttons_line.append(InlineKeyboardButton(text=text, callback_data=callback_data))
                buttons.append(buttons_line)
            return InlineKeyboardMarkup(buttons)

        case [[KeyboardButton(), *_], *_]:
            return ReplyKeyboardMarkup(keyboard)
        case [[{'text': str(), **kwargs}, *_], *_] if not kwargs or set(kwargs.keys()) & reply_buttons_kwargs:
            return ReplyKeyboardMarkup(keyboard)
        case [[str(), *_], *_]:
            buttons = []
            for line in keyboard:
                buttons_line = []
                for text in line:
                    buttons_line.append(KeyboardButton(text=text))
                buttons.append(buttons_line)
            return ReplyKeyboardMarkup(buttons)

        case keyboard if keyboard == [[]]:
            return
        case _:
            raise ValueError('Wrong keyboard format')
