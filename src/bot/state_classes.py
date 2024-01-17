from core import BaseState, Locator
from core.tg_api import Update
from core.tg_api.shortcuts import edit_inline_keyboard


class ClassicState(BaseState):
    def process(self, update: Update) -> Locator | None:
        if update.callback_query:
            return self.handle_inline_buttons(update.callback_query.data)
        if update.message:
            return self.handle_text_message(update.message.text)

    def handle_inline_buttons(self, callback_data: str) -> Locator | None:
        pass

    def handle_text_message(self, message_text: str) -> Locator | None:
        pass


class DestroyInlineKeyboardMixin:
    """Удаляет клавиатуру при выходе из состояния при нажатии на кнопку"""
    def exit_state(self, update: Update) -> None:
        if update.callback_query:
            message_id = update.callback_query.message.message_id
            edit_inline_keyboard(
                chat_id=update.chat_id,
                message_id=message_id,
                keyboard=None,
            )
