
from playwright.sync_api import Page, Locator, sync_playwright, expect
from typing import List

from module.BasePageNew import PageObject
from module.base_query_page_new import BaseQueryPage
import re


class PageManualInspection(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.输入框_居委会 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择居委会']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_网格 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择网格']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_项目名称 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入走访项目名称']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_商铺类型 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择商铺类型']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_商铺等级 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择商铺等级']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_日期 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='开始日期']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_商铺名称 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入商铺名称']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_单位名称 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入单位名称']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_任务状态 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择任务状态']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_单位类型 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择单位类型']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")

        self.选项卡_单位走访 = self.page.locator("//div[text()='单位走访']")

    def 查询数据库中的数据量(self, db_connection):
        self.get_db_data(db_connection, "select count(*) from ")

    def 输入查询条件(self, **kwargs):
        # 在页面对象中定义映射关系
        定位器到输入值 = {
            self.输入框_项目名称: kwargs.get("项目名称"),
            self.输入框_居委会: kwargs.get("居委会"),
            self.输入框_网格: kwargs.get("网格"),
            self.输入框_商铺类型: kwargs.get("商铺类型"),
            self.输入框_商铺等级: kwargs.get("商铺等级"),
            self.输入框_日期: kwargs.get("日期"),
            self.输入框_商铺名称: kwargs.get("商铺名称"),
            self.输入框_单位名称: kwargs.get("单位名称"),
            self.输入框_任务状态: kwargs.get("任务状态"),
            self.输入框_单位类型: kwargs.get("单位类型"),

        }
        self.快捷操作_填写表单_传入定位器(kwargs=定位器到输入值)

    def 校验查询条件成功修改(self, **kwargs):
        定位器到输入值 = {
            self.输入框_项目名称: kwargs.get("项目名称"),
            self.输入框_居委会: kwargs.get("居委会"),
            self.输入框_网格: kwargs.get("网格"),
            self.输入框_商铺类型: kwargs.get("商铺类型"),
            self.输入框_商铺等级: kwargs.get("商铺等级"),
            self.输入框_日期: kwargs.get("日期"),
            self.输入框_商铺名称: kwargs.get("商铺名称"),
            self.输入框_单位名称: kwargs.get("单位名称"),
            self.输入框_任务状态: kwargs.get("任务状态"),
            self.输入框_单位类型: kwargs.get("单位类型"),

        }
        self.校验表单中数据成功修改_传入定位器(kwargs=定位器到输入值)

    def 校验表单中项目时间成功修改(self, 开始日期: str, 结束日期: str):
        项目开始时间_表单项内容 = self.locators.表单项中包含操作元素的最上级div("项目时间").locator(
            "xpath=//input[@placeholder='开始日期']").input_value()
        项目结束时间_表单项内容 = self.locators.表单项中包含操作元素的最上级div("项目时间").locator(
            "xpath=//input[@placeholder='结束日期']").input_value()
        # print(项目开始时间_表单项内容, 项目结束时间_表单项内容)
        assert 项目开始时间_表单项内容 == 开始日期 and 项目结束时间_表单项内容 == 结束日期, f"项目时间修改失败,项目开始时间_表单项内容:{项目开始时间_表单项内容},项目结束时间_表单项内容:{项目结束时间_表单项内容}"

    def 获取任务负责人字符串(self):
        res = []
        loc_任务负责人列表 = self.locators.表单项中包含操作元素的最上级div("任务负责人").locator("div.item .el-tooltip")
        for 任务负责人 in loc_任务负责人列表.all():
            res.append(任务负责人.text_content().split("---")[0])
        return ",".join(res)

    def 校验查询条件_日期(self, 开始日期: str, 结束日期: str):
        开始日期_表单项内容 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='开始日期']").locator("visible=true").input_value()
        结束日期_表单项内容 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='结束日期']").locator("visible=true").input_value()
        assert 开始日期_表单项内容 == 开始日期 and 结束日期_表单项内容 == 结束日期, f"日期修改失败,开始日期_表单项内容:{开始日期_表单项内容},结束日期_表单项内容:{结束日期_表单项内容}"

    def 获取被访商铺列表(self, res)->list:
        self.等待表格加载完成()
        res.clear()
        loc_被访商铺 = self.locators.表单项中包含操作元素的最上级div("被访商铺").locator(".item .el-tooltip")
        for loc in loc_被访商铺.all():
            res.append(loc.text_content())
        return res

    def 获取被访单位列表(self, res)->list:
        self.等待表格加载完成()
        res.clear()
        loc_被访单位 = self.locators.表单项中包含操作元素的最上级div("被访单位").locator(".item .el-tooltip")
        for loc in loc_被访单位.all():
            res.append(loc.text_content())
        return res

    def 获取任务总数(self):
        return self.page.locator("//div[text()='任务总数']/following-sibling::*[position()=1]").text_content()

    def 获取已完成任务数(self):
        return self.page.locator("//div[text()='完成任务']/following-sibling::*[position()=1]").text_content()











if __name__ == '__main__':
    with sync_playwright() as playwright:
        # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        # 通过ip和端口连接到已经打开的chromium浏览器
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(3000)  # 设置默认超时时间为 3000 毫秒
        page = PageGridderManage(page)


        # 表单数据_修改后 = {"网格员图片": r"C:\Users\Administrator\Pictures\111.png", "上级领导": "金雨菲",
        #                    "选择责任网格": ["788", "测试网格5"],
        #                    }
        # page.填写新增或编辑表单(表单数据_修改后)



