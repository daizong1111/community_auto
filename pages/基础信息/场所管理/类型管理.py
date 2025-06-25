
from playwright.sync_api import Page, Locator

from module.base_query_page_new import BaseQueryPage


class PageTypeManage(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)

    def 获取输入框_检查指引维护(self):
        return self.page.locator("//input[@placeholder='请输入指引内容']")

    def 检查指引维护_输入(self, 输入内容:str):
        for loc in self.获取输入框_检查指引维护().all():
            if loc.is_visible():
                loc.fill(输入内容)
        # self.获取输入框_检查指引维护().fill(输入内容)

    def 获取类型状态列(self):
        return [row.locator("button span").first.inner_html() for row in self.get_table_rows().all()]

    def 获取开关状态列的class属性(self):
        return [row.locator(".el-switch").get_attribute("class") for row in self.get_table_rows().all()]

    def 获取任务频率和任务处理时效不为空的行(self):
        # 查找表格中第四列和第八列都不为空的行
        rows = self.get_table_rows().all()
        for row in rows:
            第四列内容 = row.locator("td").nth(3).inner_text().strip()  # nth 是 0-based，第4列是索引3
            第八列内容 = row.locator("td").nth(7).inner_text().strip()  # 第8列是索引7
            if 第四列内容 and 第八列内容:
                return row
        return None

    def 获取任务频率和任务处理时效为空的行(self):
        # 查找表格中第四列和第八列都不为空的行
        rows = self.get_table_rows().all()
        for row in rows:
            第四列内容 = row.locator("td").nth(3).inner_text().strip()  # nth 是 0-based，第4列是索引3
            第八列内容 = row.locator("td").nth(7).inner_text().strip()  # 第8列是索引7
            if 第四列内容 == "" and 第八列内容 == "":
                return row
        return None

    def 获取自动下发任务开关(self, loc_目标行)->Locator:
        return loc_目标行.locator(".el-switch")
    def 点击自动下发任务开关(self, loc_目标行):
        self.获取自动下发任务开关(loc_目标行).click()

    def 获取类型状态按钮(self, loc_目标行)->Locator:
        return loc_目标行.locator("button").first

    def 点击类型状态按钮(self, loc_目标行):
        self.获取类型状态按钮(loc_目标行).evaluate("(el) => el.click()")

    def 获取新增表单最上层定位(self):
        return self.page.locator('//div[@aria-label="新增"]').locator("visible=true")


