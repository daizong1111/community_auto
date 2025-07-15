
from playwright.sync_api import Page, Locator, sync_playwright, expect
from typing import List

from module.base_query_page_new import BaseQueryPage
import re


class PageUserManage(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)
        # self.输入框_居委会 = self.page.locator(
        #     "//form[contains(@class,'query-form')]//input[@placeholder='请选择居委会']//ancestor::div[@class='el-form-item__content']").locator(
        #     "visible=true")

    def 获取新增表单最上层定位(self):
        return self.page.locator('//div[@aria-label="新增"]').locator("visible=true")

    def 查询数据库中的数据量(self, db_connection):
        self.get_db_data(db_connection, "select count(*) from ")








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
        page = PageUserManage(page)

        # print(page.locators.表单项中包含操作元素的最上级div("手机号码:").count())
        page.点击表格中某行按钮(行号=1, 按钮名="编辑")
        page.快捷操作_填写表单_增加根据数据类确定唯一表单版(**{"用户真实姓名:":"里蠢猪", "手机号码:":"15055419272", "关联区域":"中电数智社区（测试）"})



