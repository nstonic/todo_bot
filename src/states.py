from engine.state_machine import (
    StateRouter,
    StateMachine,
    BaseLocatorsRepository,
    Locator,
    BaseState,
)
from engine.tg_api import Update, send_text_message


class LocatorsRepository(BaseLocatorsRepository):
    locators = {}

    def restore_locator_by_user_id(self, user_id: int) -> Locator:
        return self.locators[user_id]

    def save_user_locator(self, user_id: int, locator: Locator):
        self.locators[user_id] = locator


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
class StartState(BaseState):

    def enter_state(self, update: Update) -> Locator | None:
        send_text_message(
            text='Привет!',
            chat_id=self.user_id,
        )
