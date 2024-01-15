from core import BaseState, Locator


class ClassicState(BaseState):
    def process(self, update) -> Locator | None:
        if update.callback_query:
            return self.handle_inline_buttons(update.callback_query.data)
        if update.message:
            return self.handle_text_message(update.message.text)

    def handle_inline_buttons(self, callback_data: str):
        pass

    def handle_text_message(self, message_text: str):
        pass
