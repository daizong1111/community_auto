from playwright.sync_api import Page

from module.BasePage import PageObject
class 类型管理(PageObject):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/sqaq/csgl/lxgl"

