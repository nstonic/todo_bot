import textwrap
from typing import Literal

import more_itertools

from core import (
    StateRouter,
    StateMachine,
    Locator,
    Paginator,
    BaseState,
)
from core.tg_api import (
    Update,
    InlineKeyboardButton,
    EditMessageTextRequest,
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
class StartState(BaseState):
    page_number: int = 1
    show_done: bool = False
    edit_message_id: int | None = None
    page_size: int = 6

    def enter_state(self, update: Update) -> Locator | None:  # noqa
        if self.show_done:
            todos = Todo.get_all_for_user(self.chat_id)
            show_done_button = InlineKeyboardButton('Скрыть сделанные', callback_data='show_active')
        else:
            todos = Todo.get_active_for_user(self.chat_id)
            show_done_button = InlineKeyboardButton('Показать все', callback_data='show_done')

        if not todos:
            text = 'Привет!\nУ тебя еще нет задач. Добавь первую.'
            keyboard = []
        else:
            text = 'Привет!\nВот список твоих текущих задач:'
            keyboard = Paginator(
                todos,
                button_text_getter=lambda todo: textwrap.shorten(
                    str(todo), 40,
                    placeholder='...',
                ),
                button_callback_data_getter=lambda todo: todo.id,
                page_size=self.page_size,
            ).get_keyboard(self.page_number)

        keyboard.append([
            InlineKeyboardButton('Добавить', callback_data='add'),
            show_done_button,
        ])

        if self.edit_message_id:
            edit_inline_keyboard(
                self.chat_id,
                self.edit_message_id,
                keyboard,
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
                return Locator('/todo/title/')
            case 'show_done':
                return Locator('/', {'show_done': True})
            case 'show_active':
                return Locator('/')
            case callback_data if 'page#' in callback_data:
                params = {
                    'edit_message_id': update.callback_query.message.message_id,
                    'show_done': self.show_done,
                }
                _, page_number = callback_data.rsplit('#', 1)
                if page_number.isdigit():
                    params['page_number'] = int(page_number)
                else:
                    params['page_number'] = 1
                return Locator('/', params)
            case callback_data if callback_data.isdigit():
                return Locator('/todo/', {'todo_id': int(callback_data)})
            case _:
                return Locator('/', {'switch_page': True})

    def exit_state(self, update: Update) -> None:
        if not update.callback_query:
            return

        if self.show_done:
            todos = Todo.get_all_for_user(self.chat_id)
        else:
            todos = Todo.get_active_for_user(self.chat_id)

        if not todos:
            edit_inline_keyboard(
                chat_id=self.chat_id,
                message_id=update.callback_query.message.message_id,
                keyboard=None
            )
            return
        else:
            text = 'Привет!\nВот список твоих текущих задач:\n\n'
            pages = list(more_itertools.chunked(
                [str(todo) for todo in todos],
                self.page_size,
            ))
            text += '\n'.join(pages[self.page_number - 1])

        EditMessageTextRequest(
            text=text,
            chat_id=self.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=None,
        ).send()


@router.register('/todo/title/')
class AddTodoTitleState(DestroyInlineKeyboardMixin, ClassicState):

    def enter_state(self, update: Update) -> Locator | None:  # noqa
        message = send_text_message(
            text='Как назовем задачу?',
            chat_id=self.chat_id,
            keyboard=[[InlineKeyboardButton('Отмена', callback_data='cancel')]],
        )
        context = session_repository.get_user_context(update.chat_id)
        context['last_message_id'] = message.message_id

    def handle_text_message(self, message_text: str) -> Locator:
        return Locator('/todo/content/', {'title': message_text})

    def handle_inline_buttons(self, callback_data: str) -> Locator | None:
        if callback_data == 'cancel':
            return Locator('/')

    def exit_state(self, update: Update) -> None:
        super().exit_state(update)
        context = session_repository.get_user_context(update.chat_id)
        if message_id := context.pop('last_message_id', None):
            edit_inline_keyboard(
                update.chat_id,
                message_id,  # noqa
                keyboard=None,
            )


@router.register('/todo/content/')
class AddTodoContentState(DestroyInlineKeyboardMixin, ClassicState):
    title: str

    def enter_state(self, update: Update) -> Locator | None:  # noqa
        message = send_text_message(
            text='ОК. Опиши суть задачи.',
            chat_id=self.chat_id,
            keyboard=[[InlineKeyboardButton('Отмена', callback_data='cancel')]],
        )
        context = session_repository.get_user_context(update.chat_id)
        context['last_message_id'] = message.message_id

    def handle_text_message(self, message_text: str) -> Locator:
        Todo.create_for_user(
            user_id=self.chat_id,
            title=self.title,
            content=message_text
        )
        send_text_message(
            text='ОК. Сохранил задачу',
            chat_id=self.chat_id,
        )
        return Locator('/')

    def handle_inline_buttons(self, callback_data: str) -> Locator | None:
        if callback_data == 'cancel':
            return Locator('/')

    def exit_state(self, update: Update) -> None:
        super().exit_state(update)
        context = session_repository.get_user_context(update.chat_id)
        if message_id := context.pop('last_message_id', None):
            edit_inline_keyboard(
                update.chat_id,
                message_id,  # noqa
                keyboard=None,
            )


@router.register('/todo/')
class TodoState(DestroyInlineKeyboardMixin, BaseState):
    todo_id: int

    def enter_state(self, update: Update) -> Locator | None:
        todo = Todo.get_by_id(self.todo_id)
        if not todo:
            return Locator('/')

        text = f'<b>{todo}</b>\n\n{todo.content}'
        keyboard_modes = ('normal', 'done')
        send_text_message(
            text,
            update.chat_id,
            self.get_keyboard(keyboard_modes[todo.is_done]),
            parse_mode='HTML'
        )

    def mark_todo_as_done(self, is_done: bool) -> Locator:
        Todo.update(self.todo_id, is_done=is_done)
        return Locator('/')

    def delete_todo(self) -> Locator:
        Todo.delete(self.todo_id)
        return Locator('/')

    @staticmethod
    def get_keyboard(mode: Literal['normal', 'edit', 'done']):
        if mode == 'edit':
            return [
                [('Редактировать название', 'edit_title'), ('Редактировать содержимое', 'edit_content')],
                [('Отмена', 'cancel_edit')],
            ]

        elif mode == 'done':
            return [
                [('Не сделано', 'undone')],
                [('Редактировать', 'edit'), ('Удалить', 'delete')],
                [('Вернуться к списку', 'back')],
            ]
        else:
            return [
                [('Сделано', 'done')],
                [('Редактировать', 'edit'), ('Удалить', 'delete')],
                [('Вернуться к списку', 'back')],
            ]

    def switch_keyboard_to_edit_mode(self, update: Update):
        edit_inline_keyboard(
            update.chat_id,
            update.callback_query.message.message_id,
            self.get_keyboard('edit'),
        )

    def switch_keyboard_to_normal_mode(self, update: Update):
        edit_inline_keyboard(
            update.chat_id,
            update.callback_query.message.message_id,
            self.get_keyboard('normal'),
        )

    def process(self, update: Update) -> Locator | None:
        if not update.callback_query:
            return

        match update.callback_query.data:
            case 'done':
                return self.mark_todo_as_done(True)
            case 'undone':
                return self.mark_todo_as_done(False)
            case 'edit':
                self.switch_keyboard_to_edit_mode(update)
            case 'edit_title':
                return Locator('/todo/edit/title/', {'todo_id': self.todo_id})
            case 'edit_content':
                return Locator('/todo/edit/content/', {'todo_id': self.todo_id})
            case 'cancel_edit':
                self.switch_keyboard_to_normal_mode(update)
            case 'delete':
                return self.delete_todo()
            case 'back':
                return Locator('/')


@router.register('/todo/edit/title/')
class EditTodoTitleState(DestroyInlineKeyboardMixin, ClassicState):
    todo_id: int

    def enter_state(self, update: Update) -> Locator | None:  # noqa
        message = send_text_message(
            'Как переименовать задачу?',
            update.chat_id,
            keyboard=[[InlineKeyboardButton('Отмена', callback_data='cancel')]],
        )
        context = session_repository.get_user_context(update.chat_id)
        context['last_message_id'] = message.message_id

    def handle_text_message(self, message_text: str) -> Locator | None:
        Todo.update(todo_id=self.todo_id, title=message_text)
        return Locator('/todo/', {'todo_id': self.todo_id})

    def handle_inline_buttons(self, callback_data: str) -> Locator | None:
        if callback_data == 'cancel':
            return Locator('/todo/', {'todo_id': self.todo_id})

    def exit_state(self, update: Update) -> None:
        super().exit_state(update)
        context = session_repository.get_user_context(update.chat_id)
        if message_id := context.pop('last_message_id', None):
            edit_inline_keyboard(
                update.chat_id,
                message_id,  # noqa
                keyboard=None,
            )


@router.register('/todo/edit/content/')
class EditTodoContentState(DestroyInlineKeyboardMixin, ClassicState):
    todo_id: int

    def enter_state(self, update: Update) -> Locator | None:  # noqa
        message = send_text_message(
            'Пришли новое описание',
            update.chat_id,
            keyboard=[[InlineKeyboardButton('Отмена', callback_data='cancel')]],
        )
        context = session_repository.get_user_context(update.chat_id)
        context['last_message_id'] = message.message_id

    def handle_text_message(self, message_text: str) -> Locator | None:
        Todo.update(todo_id=self.todo_id, content=message_text)
        return Locator('/todo/', {'todo_id': self.todo_id})

    def handle_inline_buttons(self, callback_data: str) -> Locator | None:
        if callback_data == 'cancel':
            return Locator('/todo/', {'todo_id': self.todo_id})

    def exit_state(self, update: Update) -> None:
        super().exit_state(update)
        context = session_repository.get_user_context(update.chat_id)
        if message_id := context.pop('last_message_id', None):
            edit_inline_keyboard(
                update.chat_id,
                message_id,  # noqa
                keyboard=None,
            )
