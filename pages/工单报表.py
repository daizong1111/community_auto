from playwright.sync_api import Page

from module.BasePage import PageObject


class 工单报表(PageObject):
    def __init__(self, page: Page):
        super().__init__(page)
        self.loc_button_导出明细 = page.locator("button", has_text="导出明细")