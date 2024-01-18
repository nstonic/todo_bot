from collections.abc import Sequence

from core.tg_api import InlineKeyboardButton


def generate_inline_buttons(*buttons: Sequence[Sequence[str, str]]) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for line in buttons:
        buttons_line = []
        for text, callback_data in line:
            buttons_line.append(InlineKeyboardButton(text, callback_data=callback_data))
        keyboard.append(buttons_line)
    return keyboard
