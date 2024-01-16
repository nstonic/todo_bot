import os
from typing import NoReturn

from bot import state_machine
from core import SyncTgClient, GetUpdatesRequest


def run_bot() -> NoReturn:
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    with SyncTgClient.setup(tg_bot_token):
        for update in GetUpdatesRequest().listen_updates():
            state_machine.process(update)


if __name__ == '__main__':
    run_bot()
