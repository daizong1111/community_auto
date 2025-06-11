from playwright.sync_api import Page

from module.BasePage import PageObject
from module.base_query_page import BaseQueryPage


class PageFloor(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)

    def 获取新增按钮(self):
        return self.page.locator("//span[text()=' 新增 ']")

    def 点击新增按钮(self):
        self.获取新增按钮().click()

    def 统计数据库表中的记录数(self, connection):
        sql = """select count(*) as count from ybds_building;"""
        db_data = self.get_db_data(connection, sql)
        return db_data[0]["count"]

    def 定位器_新增表单(self):
        return self.page.locator('//div[@aria-label="楼栋信息"]')

    def get_first_page_button(self):
        # 首页按钮
        return self.page.locator("//ul[@class='el-pager']/li[text()='1']")

    def get_next_button(self):
        # 下一页按钮
        return self.page.locator('.btn-next')

    def get_table_rows(self):
        # 定位表格中的所有行
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody/tr")

    def 验证搜索框内容被重置(self):
        内容_搜索框_选择小区 = self.locators.表单项中包含操作元素的最上级div("选择小区").locator('input').input_value()
        内容_搜索框_楼栋号 = self.locators.表单项中包含操作元素的最上级div("楼栋号").locator('input').input_value()
        内容_搜索框_楼栋名称 = self.locators.表单项中包含操作元素的最上级div("楼栋名称").locator('input').input_value()
        assert 内容_搜索框_选择小区 == "" and 内容_搜索框_楼栋号 == "" and 内容_搜索框_楼栋名称 == ""

    def 获取楼栋信息表单(self):
        return self.page.locator('//div[@aria-label="楼栋信息"]')

    def 验证编辑表单的可交互性(self):
        表单项_小区名称 = self.locators.表单项中包含操作元素的最上级div("小区名称", 处理后的表单最上层定位=self.获取楼栋信息表单()).locator("input,textarea")
        表单项_楼栋号 = self.locators.表单项中包含操作元素的最上级div("楼栋号", 处理后的表单最上层定位=self.获取楼栋信息表单()).locator("input,textarea")
        # 断言输入框不可交互
        assert not 表单项_小区名称.is_editable() and not 表单项_楼栋号.is_editable()

    def 获取提示弹窗(self):
        return self.page.locator(".el-message-box")
    def 获取提示弹窗中的确定按钮(self):
        return self.获取提示弹窗().locator("button", has_text="确定")

    def 点击提示弹窗中的确定按钮(self):
        self.获取提示弹窗中的确定按钮().click()





