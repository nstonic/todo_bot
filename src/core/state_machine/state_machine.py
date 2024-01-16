from abc import ABC, abstractmethod
from typing import Type, NamedTuple, ClassVar, final, Any

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


class BaseSessionRepository(dict, ABC):

    @abstractmethod
    def save_user_locator(self, user_id: int, locator: Locator) -> None:
        pass

    @abstractmethod
    def get_locator_by_user_id(self, user_id: int) -> Locator | None:
        pass

    @abstractmethod
    def save_user_history(self, user_id: int, locator: Locator) -> None:
        pass

    @abstractmethod
    def get_user_history(self, user_id: int) -> list[Locator]:
        pass

    @abstractmethod
    def save_context_data(self, user_id: int, **kwargs) -> None:
        pass

    @abstractmethod
    def get_context_data(self, user_id: int, key: str) -> Any:
        pass


@final
class StateMachine(BaseModel):
    state_router: StateRouter
    session_repository: BaseSessionRepository
    start_state_locator: Locator
    commands_map: dict[str, Locator] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def process(self, update: Update):
        if locator := self.get_locator_from_command(update):
            self.switch_state(locator, update)
            return

        locator = self.session_repository.get_locator_by_user_id(update.chat_id)
        if not locator:
            self.switch_state(self.start_state_locator, update)
            return

        state = self.state_router.restore_state(locator, update.chat_id)
        next_locator = state.process(update)

        if next_locator and locator.state_name != next_locator.state_name:
            state.exit_state(update)

        states_chain_length = 0
        while next_locator:
            states_chain_length += 1
            if states_chain_length >= MAX_STATES_CHAIN_LEN:
                break
            next_locator = self.switch_state(next_locator, update)

    def get_locator_from_command(self, update) -> Locator | None:
        if not update.message:
            return
        if locator := self.commands_map.get(update.message.text):
            return locator

    def switch_state(self, state_locator: Locator, update: Update) -> Locator | None:
        self.session_repository.save_user_locator(update.chat_id, state_locator)
        self.session_repository.save_user_history(update.chat_id, state_locator)
        print(f'Switching to state with locator: {state_locator}')
        state = self.state_router.restore_state(state_locator, update.chat_id)
        print(f'State: {state.__class__.__name__}')
        next_state_locator = state.enter_state(update)
        return next_state_locator
