from playwright.sync_api import Page

from module.BasePage import PageObject
class 特殊人群(PageObject):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/sqaq/syrk/tsrq"
        self.抽屉_新增 = page.locator(".el-drawer__body").locator("visible=true")

