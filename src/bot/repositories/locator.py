from core.state_machine import BaseLocatorsRepository, Locator


class LocatorsRepository(BaseLocatorsRepository):
    locators = {}

    def restore_locator_by_user_id(self, user_id: int) -> Locator | None:
        return self.locators.get(user_id)

    def save_user_locator(self, user_id: int, locator: Locator):
        self.locators[user_id] = locator
