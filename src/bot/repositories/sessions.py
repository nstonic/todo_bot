from typing import Any

from core.state_machine import BaseSessionRepository, Locator


class MemorySessionRepository(BaseSessionRepository):

    def save_user_locator(self, user_id: int, locator: Locator):
        if user_id not in self:
            self[user_id] = {
                'locator': locator,
                'history': [],
                'context': {},
            }

    def restore_locator_by_user_id(self, user_id: int) -> Locator | None:
        return self.get(user_id, {}).get('locator')

    def save_user_history(self, user_id: int, locator: Locator):
        if user_id in self:
            self[user_id]['history'].append(locator)

    def get_user_history(self, user_id: int) -> list[Locator]:
        return self.get(user_id, {}).get('history', [])

    def save_context_data(self, user_id: int, **kwargs):
        if user_id in self:
            self[user_id]['context'].update(kwargs)

    def get_context_data(self, user_id: int, key: str = None) -> Any:
        if key:
            return self.get(user_id, {}).get('context', {}).get(key)
        return self.get(user_id, {}).get('context', {})
