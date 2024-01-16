from core import BaseState, Locator
from core.tg_api import Update


class ClassicState(BaseState):
    def process(self, update: Update) -> Locator | None:
        print(update.message)
        print(self.__class__)
        if update.callback_query:
            return self.handle_inline_buttons(update.callback_query.data)
        if update.message:
            return self.handle_text_message(update.message.text)

    def handle_inline_buttons(self, callback_data: str) -> Locator | None:
        pass

    def handle_text_message(self, message_text: str) -> Locator | None:
        pass
