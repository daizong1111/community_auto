from playwright.sync_api import Page

from module.BasePage import PageObject
class 楼栋管理(PageObject):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/sqaq/syfw/ldgl"
        # self.对话框_批量导入房屋 = page.locator("div[aria-label='批量导入房屋']")

