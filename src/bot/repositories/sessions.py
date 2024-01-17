from core.state_machine import BaseSessionRepository, Locator


class MemorySessionRepository(BaseSessionRepository):

    def __init__(self, *, max_history_length: int = 50):
        super().__init__()
        self.max_history_length = max_history_length

    def save_user_locator(self, user_id: int, locator: Locator):
        if user_id not in self:
            self[user_id] = {
                'locator': locator,
                'history': [],
            }
        else:
            self[user_id]['locator'] = locator
        self.save_user_history(user_id, locator)

    def get_locator_by_user_id(self, user_id: int) -> Locator | None:
        return self.get(user_id, {}).get('locator')

    def save_user_history(self, user_id: int, locator: Locator):
        if user_id in self:
            self[user_id]['history'].append(locator)
            if len(self[user_id]['history']) > self.max_history_length:
                self[user_id]['history'] = self[user_id]['history'][:self.max_history_length]

    def get_user_history(self, user_id: int) -> list[Locator]:
        return self.get(user_id, {}).get('history', [])
