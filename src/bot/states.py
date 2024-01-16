from core import (
    StateRouter,
    StateMachine,
    Locator,
    Paginator,
)
from core.tg_api.shortcuts import edit_text_message, send_text_message
from .repositories import Todo, MemorySessionRepository
from .state_classes import ClassicState
from core.tg_api import Update, InlineKeyboardMarkup, InlineKeyboardButton, EditMessageReplyMarkupRequest

router = StateRouter()
start_state_locator = Locator('/')
session_repository = MemorySessionRepository()

state_machine = StateMachine(
    state_router=router,
    session_repository=session_repository,
    start_state_locator=start_state_locator,
    commands_map={
        '/start': start_state_locator,
    }
)


@router.register('/')
class StartState(ClassicState):
    page_number: int = 1
    switch_page: bool = False

    def enter_state(self, update: Update) -> Locator | None:
        active_todos = Todo.get_active_for_user(self.chat_id)

        if not active_todos:
            text = 'Привет!\nУ тебя еще нет задач. Добавь первую.'
            keyboard = []
        else:
            text = 'Привет!\nВот список твоих текущих задач:'
            keyboard = Paginator(
                active_todos,
                button_text_getter=lambda todo: todo.title,
                button_callback_data_getter=lambda todo: todo.id,
                page_size=2,
            ).get_keyboard(self.page_number)

        keyboard.append([
            InlineKeyboardButton(text='Добавить', callback_data='add'),
            InlineKeyboardButton(text='Сделанные', callback_data='show_done'),
        ])

        last_message_id = session_repository.get_context_data(self.chat_id, 'last_message_id')
        if self.switch_page and last_message_id:
            edit_text_message(
                self.chat_id,
                last_message_id,
                text=text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                ignore_no_changes=True,
            )
        else:
            sent_message = send_text_message(
                text=text,
                chat_id=self.chat_id,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
            )
            session_repository.save_context_data(
                self.chat_id,
                last_message_id=sent_message.message_id,
            )

    def handle_inline_buttons(self, callback_data: str):
        match callback_data:
            case 'add':
                return Locator('/add-todo/title/')
            case callback_data if 'page#' in callback_data:
                params = {
                    'switch_page': True,
                }
                _, page_number = callback_data.rsplit('#', 1)
                if page_number.isdigit():
                    params['page_number'] = int(page_number)
                else:
                    params['page_number'] = 1
                return Locator('/', params)
            case callback_data if callback_data.isdigit():
                return Locator('/show_todo/' + callback_data)

    def exit_state(self, update: Update) -> None:
        if last_message_id := session_repository.get_context_data(self.chat_id, 'last_message_id'):
            EditMessageReplyMarkupRequest(
                chat_id=self.chat_id,
                message_id=last_message_id,
                reply_markup=None,
            )


@router.register('/add-todo/title/')
class AddTodoTitleState(ClassicState):

    def enter_state(self, update: Update) -> Locator | None:
        send_text_message(
            text='Как назовем задачу?',
            chat_id=self.chat_id,
        )

    def handle_text_message(self, message_text: str):
        print(message_text)
        return Locator('/add-todo/content/', {'title': message_text})


@router.register('/add-todo/content/')
class AddTodoContentState(ClassicState):
    title: str

    def enter_state(self, update: Update) -> Locator | None:
        send_text_message(
            text='ОК. Опиши суть задачи.',
            chat_id=self.chat_id,
        )

    def handle_text_message(self, message_text: str):
        if len(self.title) > 30:
            title = self.title[:30]
        else:
            title = self.title
        Todo.create_for_user(
            user_id=self.chat_id,
            title=title,
            content=message_text
        )
        send_text_message(
            text='ОК. Сохранил задачу',
            chat_id=self.chat_id,
        )
        return Locator('/')
