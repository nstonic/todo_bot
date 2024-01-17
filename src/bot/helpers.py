from typing import Union

from core.tg_api import InlineKeyboardButton

ButtonsSchema = Union[
    list[list[str, str]],
    tuple[list[str, str]],
    list[tuple[str, str]],
    tuple[tuple[str, str]]
]


def generate_inline_buttons(*buttons: ButtonsSchema) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for line in buttons:
        buttons_line = []
        for text, callback_data in line:
            buttons_line.append(InlineKeyboardButton(text=text, callback_data=callback_data))
        keyboard.append(buttons_line)
    return keyboard
