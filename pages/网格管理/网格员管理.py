
from playwright.sync_api import Page, Locator, sync_playwright, expect
from typing import List

from module.BasePageNew import PageObject
from module.base_query_page_new import BaseQueryPage
import re


class PageGridderManage(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.输入框_居委会 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择居委会']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_网格 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择网格']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_姓名 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入姓名']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_手机号码 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入手机号码']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
    def 获取新增表单最上层定位(self):
        return self.page.locator('//div[@aria-label="新增"]').locator("visible=true")

    def 查询数据库中的数据量(self, db_connection):
        self.get_db_data(db_connection, "select count(*) from ")

    def 输入查询条件(self, **kwargs):
        # 在页面对象中定义映射关系
        定位器到输入值 = {
            self.输入框_居委会: kwargs.get("居委会"),
            self.输入框_网格: kwargs.get("网格"),
            self.输入框_姓名: kwargs.get("姓名"),
            self.输入框_手机号码: kwargs.get("手机号码"),

        }
        self.快捷操作_填写表单_传入定位器(kwargs=定位器到输入值)

    def 校验查询条件成功修改(self, **kwargs):
        定位器到输入值 = {
            self.输入框_居委会: kwargs.get("居委会"),
            self.输入框_网格:kwargs.get("网格"),
            self.输入框_姓名: kwargs.get("姓名"),
            self.输入框_手机号码: kwargs.get("手机号码"),

        }
        self.校验表单中数据成功修改_传入定位器(kwargs=定位器到输入值)

    def 校验选择责任网格成功修改(self, 网格名称:List[str]):
        for 网格名称 in 网格名称:
            expect(self.page.locator(".el-checkbox-group .el-checkbox", has=self.page.get_by_text(网格名称, exact=True))).to_be_checked()


    def 选择责任网格(self, 网格名称: List[str]):
        if 网格名称 is None:
            return
        # 若需要选择网格，就先清空，再选择
        loc_已选中的责任网格 = self.page.locator(".el-checkbox-group .el-checkbox.is-checked")
        for i in range(loc_已选中的责任网格.count()):
            loc_已选中的责任网格.first.click()
        if 网格名称 == "":
            return
        for 网格名称 in 网格名称:
            self.page.locator(".el-checkbox-group .el-checkbox").get_by_text(网格名称,exact=True).click()


    def 填写新增或编辑表单(self, 表单数据:dict):
        self.快捷操作_填写表单_增加根据数据类确定唯一表单版(**{"手机号":表单数据.get("手机号"),"网格员图片":表单数据.get("网格员图片")})
        if 表单数据.get("手机号") is not None:
            self.click_button("检测账号")
            # 出现消息弹窗
            expect(self.page.locator(".el-message-box", has_text="该手机号已绑定账号")).to_be_visible()
            self.点击提示弹窗中的确定按钮()
        else:
            assert self.locators.表单项中包含操作元素的最上级div("手机号").locator("input").is_disabled()
        assert self.locators.表单项中包含操作元素的最上级div("网格员姓名").locator("input").is_disabled() and self.locators.表单项中包含操作元素的最上级div("登录账号").locator("input").is_disabled()
        self.click_button("保存到下一步")
        assert self.locators.表单项中包含操作元素的最上级div("网格员标识").locator("input").is_disabled() and self.locators.表单项中包含操作元素的最上级div("所属居委会").locator("input").is_disabled()
        self.快捷操作_填写表单_增加根据数据类确定唯一表单版(**{"上级领导":表单数据.get("上级领导")})
        self.选择责任网格(表单数据.get("选择责任网格"))




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



