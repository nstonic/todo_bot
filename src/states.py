from core import (
    StateRouter,
    StateMachine,
    Locator,
    BaseState,
    LocatorsRepository,
    send_text_message,
)
from core.tg_api import Update

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
            chat_id=self.chat_id,
        )
