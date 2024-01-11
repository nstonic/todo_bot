from pydantic import BaseSettings, Field

from engine.tg_api import GetUpdatesRequest, SyncTgClient
from states import state_machine


class Settings(BaseSettings):
    tg_bot_token: str = Field(..., env='TG_BOT_TOKEN')


def run_bot():
    with SyncTgClient.setup(Settings().tg_bot_token):
        GetUpdatesRequest().run_polling(state_machine.process)


if __name__ == '__main__':
    run_bot()
