import pytest

from ..tg_api import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from ..tg_api.shortcuts import generate_reply_markup

inline_buttons_kwargs = (
    {'url': 'https://my-site.com'},
    {'callback_data': 'hello'},
    {'web_app': {'test': 'https://my-site.com'}},
    {'login_url': {'test': True}},
    {'switch_inline_query': 'hello'},
    {'switch_inline_query_current_chat': 'hello'},
    {'switch_inline_query_chosen_chat': {'test': True}},
    {'callback_game': 'hello'},
    {'pay': True},
)
reply_buttons_kwargs = (
    {'request_users': {'test': True}},
    {'request_chat': {'test': True}},
    {'request_contact': True},
    {'request_location': True},
    {'request_poll': {'test': 'test'}},
    {'web_app': {'test': 'https://my-site.com'}},
)


def test_main_types():
    for argument in inline_buttons_kwargs:
        button = InlineKeyboardButton(text='hello', **argument)
        keyboard = InlineKeyboardMarkup([[button]])
        assert generate_reply_markup(keyboard) == keyboard

    for argument in reply_buttons_kwargs:
        button = KeyboardButton(text='hello', **argument)
        keyboard = ReplyKeyboardMarkup([[button]])
        assert generate_reply_markup(keyboard) == keyboard

    assert generate_reply_markup(None) is None
    assert generate_reply_markup([[]]) is None

    with pytest.raises(ValueError, match='Wrong keyboard format'):
        generate_reply_markup([[False]])


def test_dicts():
    for argument in inline_buttons_kwargs:
        button = {'text': 'hello', **argument}
        keyboard = InlineKeyboardMarkup([[button]])
        assert generate_reply_markup([[button]]) == keyboard

    for argument in reply_buttons_kwargs:
        button = {'text': 'hello', **argument}
        keyboard = ReplyKeyboardMarkup([[button]])
        assert generate_reply_markup(keyboard) == keyboard

    button = {'text': 'hello', 'garbage': True}
    with pytest.raises(ValueError, match='Wrong keyboard format'):
        generate_reply_markup([[button]])


def test_tuples():
    button = InlineKeyboardButton(text='Hello', callback_data='hello')
    keyboard = InlineKeyboardMarkup([[button]])
    assert generate_reply_markup([[('Hello', 'hello')]]) == keyboard

    button = KeyboardButton(text='Hello')
    keyboard = ReplyKeyboardMarkup([[button]])
    assert generate_reply_markup([['Hello']]) == keyboard
