from playwright.sync_api import Page

from module.base_query_page import BaseQueryPage


class PageCarBlackList(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)

    def 获取开始时间输入框(self):
        return self.page.locator("//input[@placeholder='到期时间日期']")

    def 获取结束时间输入框(self):
        return self.page.locator("//input[@placeholder='生效时间']")

    def 校验表单中时间成功修改(self, 表单数据_时间):
        list_时间 = 表单数据_时间.split(",")
        开始时间 = list_时间[0]
        结束时间 = list_时间[1]
        assert self.获取开始时间输入框().input_value() == 开始时间 and self.获取结束时间输入框().input_value() == 结束时间


