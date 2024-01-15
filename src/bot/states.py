from core import (
    StateRouter,
    StateMachine,
    Locator,
    send_text_message,
    Paginator,
)
from .repositories import Todo, LocatorsRepository
from .state_classes import ClassicState
from core.tg_api import Update, InlineKeyboardMarkup, InlineKeyboardButton

router = StateRouter()
start_state_locator = Locator('/')

state_machine = StateMachine(
    router=router,
    locators_repository=LocatorsRepository(),
    start_state_locator=start_state_locator,
    commands_map={
        '/start': start_state_locator,
    }
)


@router.register('/')
class StartState(ClassicState):
    page_number: int = 1

    def enter_state(self, update: Update) -> Locator | None:
        active_todos = Todo.get_active_for_user(update.chat_id)

        if not active_todos:
            text = 'Привет!\nУ тебя еще нет дел. Добавь первое:'
            keyboard = []
        else:
            text = 'Привет!\nВот список твоих текущих дел:'
            keyboard = Paginator(
                active_todos,
                button_text_getter=lambda todo: todo.title,
                button_callback_data_getter=lambda todo: todo.id,
                page_size=2,
            ).get_keyboard(self.page_number)

        keyboard.append([
            InlineKeyboardButton(text='Добавить', callback_data='add'),
            InlineKeyboardButton(text='Показать сделанные', callback_data='show_done'),
        ])

        send_text_message(
            text=text,
            chat_id=self.chat_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )

    def handle_inline_buttons(self, callback_data: str):
        match callback_data:
            case 'add':
                return Locator('/add_todo/')
            case callback_data if 'page#' in callback_data:
                _, page_number = callback_data.rsplit('#', 1)
                if page_number.isdigit():
                    page_number = int(page_number)
                else:
                    page_number = 1
                return Locator('/', {'page_number': page_number})
            case _:
                return Locator('/show_todo/' + callback_data)
