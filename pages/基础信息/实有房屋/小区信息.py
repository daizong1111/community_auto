from playwright.sync_api import Page

from module.BasePage import PageObject
from module.base_query_page import BaseQueryPage


class PageCommunity(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)
        # self.table = Table(page)

    def 获取新增按钮(self):
        return self.page.locator("//span[text()=' 新增 ']")

    def 点击新增按钮(self):
        self.获取新增按钮().click()

    def 获取物业新增按钮(self):
        return self.page.locator("//span[text()='+ 新增']")

    def 点击物业新增按钮(self):
        self.获取物业新增按钮().click()

    def 统计数据库表中的记录数(self, connection):
        sql = """select count(*) as count from base_village"""
        db_data = self.get_db_data(connection, sql)
        return db_data[0]["count"]

    def 验证新增的物业存在于下拉选项中(self, 物业名称):
        最上级div_物业名称 = self.locators.表单项中包含操作元素的最上级div("物业名称", self.page.locator(
            '//div[@aria-label="新增小区信息"]'))
        下拉框_物业名称 = 最上级div_物业名称.locator("input,textarea").locator("visible=true").last
        下拉框_物业名称.click()
        下拉列表_物业名称 = self.page.locator(".el-select-dropdown").locator("visible=true")
        下拉列表_物业名称.wait_for(state="visible")
        # 新增的物业名称在下拉列表中存在
        assert 下拉列表_物业名称.get_by_text(物业名称, exact=True).is_visible()

    def 验证新增物业信息_失败_必填项缺失(self):
        对话框_新增物业信息 = self.page.locator('//div[@aria-label="新增物业信息"]')
        assert 对话框_新增物业信息.get_by_text("请输入").count() > 0 or 对话框_新增物业信息.get_by_text(
            "请选择").count() > 0

    def 获取新增物业信息对话框(self):
        return self.page.locator('//div[@aria-label="新增物业信息"]')

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
        内容_搜索框_小区类型 = self.locators.表单项中包含操作元素的最上级div("小区类型").locator('input').input_value()
        内容_搜索框_管理类别 = self.locators.表单项中包含操作元素的最上级div("管理类别").locator('input').input_value()
        内容_搜索框_小区名称 = self.locators.表单项中包含操作元素的最上级div("小区名称").locator('input').input_value()
        assert 内容_搜索框_小区类型 == "全部" and 内容_搜索框_管理类别 == "全部" and 内容_搜索框_小区名称 == ""

    def 获取提示弹窗(self):
        return self.page.locator(".el-message-box")
    def 获取提示弹窗中的确定按钮(self):
        return self.获取提示弹窗().locator("button", has_text="确定")

    def 点击提示弹窗中的确定按钮(self):
        self.获取提示弹窗中的确定按钮().click()

    def 统计数据库表中的记录数_修改后(self, connection, 小区名称):
        sql = """select count(*) as count from base_village where xqmc = %(小区名称)s"""
        db_data = self.get_db_data(connection, sql, {"小区名称": 小区名称})
        return db_data[0]["count"]

    def 定位器_编辑表单(self):
        return self.page.locator('//div[@aria-label="编辑小区信息"]')
