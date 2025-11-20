from playwright.sync_api import Page

from module.BasePage import PageObject
class 一房一档(PageObject):
    def __init__(self, page: Page):
        super().__init__(page)

