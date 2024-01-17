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
    def exit_state(self, update: Update) -> None:
        if update.message:
            edit_inline_keyboard(
                chat_id=self.chat_id,
                message_id=update.message.message_id,
                keyboard=None,
            )
        elif update.callback_query:
            edit_inline_keyboard(
                chat_id=self.chat_id,
                message_id=update.callback_query.message.message_id,
                keyboard=None,
            )
