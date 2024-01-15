from abc import ABC, abstractmethod
from typing import Type, NamedTuple, ClassVar, final

from pydantic import BaseModel, Field

from core.tg_api import Update
from core.state_machine.errors import StateRouterError

MAX_STATES_CHAIN_LEN = 10


class Locator(NamedTuple):
    state_name: str
    params: dict = dict()


class BaseState(BaseModel):
    chat_id: int
    _state_name: ClassVar

    model_config = {'arbitrary_types_allowed': True}

    def enter_state(self, update: Update) -> Locator | None:
        pass

    def exit_state(self, update: Update) -> None:
        pass

    def process(self, update) -> Locator | None:
        pass


@final
class StateRouter(dict[str, Type[BaseState]]):
    def register(self, state_name: str):
        def decorator(cls: Type[BaseState]):
            cls._state_name = state_name
            self[state_name] = cls

        return decorator

    def restore_state(self, locator: Locator, chat_id: int) -> BaseState:
        state_class = self[locator.state_name]
        state_params = locator.params | {'chat_id': chat_id}
        return state_class.parse_obj(state_params)

    @classmethod
    def create_by_merging(cls, *routers):
        router = cls()
        for r in routers:
            router.update(r)
        return router

    def __setitem__(self, key, value):
        if key in self:
            raise StateRouterError(f'State locator {key} already registered')
        return super().__setitem__(key, value)

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            raise StateRouterError(f'State locator {item} is not registered') from None


class BaseLocatorsRepository(ABC):

    @abstractmethod
    def restore_locator_by_user_id(self, user_id: int) -> Locator:
        pass

    @abstractmethod
    def save_user_locator(self, user_id: int, locator: Locator):
        pass


@final
class StateMachine(BaseModel):
    router: StateRouter
    locators_repository: BaseLocatorsRepository
    start_state_locator: Locator
    commands_map: dict[str, Locator] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def process(self, update: Update):
        chat_id = update.chat_id

        if update.message and update.message.text in self.commands_map:
            print(f'Processing command "{update.message.text}"')
            state_locator = self.commands_map[update.message.text]
            self.switch_state(state_locator, update, chat_id)
            return

        locator = self.locators_repository.restore_locator_by_user_id(chat_id)

        if not locator:
            print(f'Locator not found. Redirecting to the start state.')
            self.switch_state(self.start_state_locator, update, chat_id)
            return
        else:
            state = self.router.restore_state(locator, chat_id)
            next_state_locator = state.process(update)

        if not next_state_locator:
            return

        if locator != next_state_locator:
            state.exit_state(update)

        states_chain_counter = 0
        while next_state_locator:
            if states_chain_counter >= MAX_STATES_CHAIN_LEN:
                print(f'Maximum states chain length reached: {MAX_STATES_CHAIN_LEN}')
                self.locators_repository.save_user_locator(chat_id, locator)
                break
            next_state_locator = self.switch_state(next_state_locator, update, chat_id)
            states_chain_counter += 1

    def switch_state(self, next_state_locator: Locator, update: Update, chat_id: int) -> Locator | None:
        print(f'Switching to state with locator: {next_state_locator}')
        next_state = self.router.restore_state(next_state_locator, chat_id)
        print(f'State: {next_state.__class__.__name__}')
        next_next_state_locator = next_state.enter_state(update)
        self.locators_repository.save_user_locator(chat_id, next_state_locator)
        return next_next_state_locator
