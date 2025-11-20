from playwright.sync_api import Page

from module.BasePage import PageObject
class 小区信息(PageObject):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/sqaq/syfw/xqxx"
        self.抽屉_新增 = page.locator(".el-drawer__body").locator("visible=true")

    def 填写表单项_小区名称(self, 小区名称):
        loc_小区名称 = self.page.get_by_placeholder("请输入名称模糊搜索")
        loc_小区名称.press_sequentially(小区名称)
        loc_小区名称.blur(timeout=1000)