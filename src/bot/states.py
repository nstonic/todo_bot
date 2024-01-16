from core import (
    StateRouter,
    StateMachine,
    Locator,
    Paginator,
    BaseState,
)
from core.tg_api import Update, InlineKeyboardButton
from core.tg_api.shortcuts import (
    send_text_message,
    edit_inline_keyboard,
)
from .repositories import Todo, MemorySessionRepository
from .state_classes import ClassicState, DestroyInlineKeyboardMixin

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
class StartState(BaseState, DestroyInlineKeyboardMixin):
    page_number: int = 1
    show_done: bool = False
    edit_message_id: int | None = None

    def enter_state(self, update: Update) -> Locator | None:
        if self.show_done:
            todos = Todo.get_all_for_user(self.chat_id)
            show_done_button = InlineKeyboardButton(text='Скрыть сделанные', callback_data='show_active')
        else:
            todos = Todo.get_active_for_user(self.chat_id)
            show_done_button = InlineKeyboardButton(text='Показать все', callback_data='show_done')

        if not todos:
            text = 'Привет!\nУ тебя еще нет задач. Добавь первую.'
            keyboard = []
        else:
            text = 'Привет!\nВот список твоих текущих задач:'
            keyboard = Paginator(
                todos,
                button_text_getter=lambda todo: todo.title,
                button_callback_data_getter=lambda todo: todo.id,
                page_size=6,
            ).get_keyboard(self.page_number)

        keyboard.append([
            InlineKeyboardButton(text='Добавить', callback_data='add'),
            show_done_button,
        ])

        if self.edit_message_id:
            edit_inline_keyboard(
                self.chat_id,
                self.edit_message_id,
                keyboard,
                ignore_exactly_the_same=True,
            )
        else:
            send_text_message(
                text,
                self.chat_id,
                keyboard,
            )

    def process(self, update: Update) -> Locator | None:
        if not update.callback_query:
            return 
        
        match update.callback_query.data:
            case 'add':
                return Locator('/add_todo/title/')
            case 'show_done':
                return Locator('/', {'show_done': True})
            case 'show_active':
                return Locator('/')
            case callback_data if 'page#' in callback_data:
                params = {
                    'edit_message_id': update.callback_query.message.message_id,
                }
                _, page_number = callback_data.rsplit('#', 1)
                if page_number.isdigit():
                    params['page_number'] = int(page_number)
                else:
                    params['page_number'] = 1
                return Locator('/', params)
            case callback_data if callback_data.isdigit():
                return Locator('/todo/edit/', {'todo_id': int(callback_data)})
            case _:
                return Locator('/', {'switch_page': True})


@router.register('/add_todo/title/')
class AddTodoTitleState(ClassicState):

    def enter_state(self, update: Update) -> Locator | None:
        send_text_message(
            text='Как назовем задачу?',
            chat_id=self.chat_id,
        )

    def handle_text_message(self, message_text: str) -> Locator:
        return Locator('/add_todo/content/', {'title': message_text})


@router.register('/add_todo/content/')
class AddTodoContentState(ClassicState):
    title: str

    def enter_state(self, update: Update) -> Locator | None:
        send_text_message(
            text='ОК. Опиши суть задачи.',
            chat_id=self.chat_id,
        )

    def handle_text_message(self, message_text: str) -> Locator:
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


@router.register('/todo/edit/')
class ShowTodoState(ClassicState, DestroyInlineKeyboardMixin):
    todo_id: int

    def enter_state(self, update: Update) -> Locator | None:
        todo = Todo.get_by_id(self.todo_id)
        if not todo:
            return Locator('/')

        text = f'<b>{todo.title}</b>\n\n{todo.content}'
        keyboard = [
            [
                InlineKeyboardButton(text='Сделано', callback_data='done'),
            ],
            [
                InlineKeyboardButton(text='Редактировать', callback_data='edit'),
                InlineKeyboardButton(text='Удалить', callback_data='delete'),
            ],
            [
                InlineKeyboardButton(text='Вернуться к списку', callback_data='back'),
            ],

        ]
        send_text_message(
            text,
            update.chat_id,
            keyboard,
            parse_mode='HTML'
        )

    def mark_todo_as_done(self) -> Locator:
        Todo.mark_todo_as_done(self.todo_id)
        return Locator('/')

    def delete_todo(self) -> Locator:
        Todo.delete(self.todo_id)
        return Locator('/')

    def handle_inline_buttons(self, callback_data: str) -> Locator | None:
        match callback_data:
            case 'done':
                return self.mark_todo_as_done()
            case 'edit':
                return Locator('/todo/edit/', {'todo_id': self.todo_id})
            case 'delete':
                return self.delete_todo()
            case 'back':
                return Locator('/')