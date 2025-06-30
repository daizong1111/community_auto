
from playwright.sync_api import Page, Locator, sync_playwright, expect

from module.BasePageNew import PageObject
from module.base_query_page_new import BaseQueryPage


class PageUnitInfo(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.输入框_区域 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择区域']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_网格 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择所属网格']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_所属部门 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入归属部门']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_单位名称 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入单位名称']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_单位类型 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择单位类型']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        
    def 获取新增表单最上层定位(self):
        return self.page.locator('//div[@aria-label="新增"]').locator("visible=true")

    def 输入查询条件(self, **kwargs):
        # 在页面对象中定义映射关系
        定位器到输入值 = {
            self.输入框_区域: kwargs.get("区域"),
            self.输入框_网格: kwargs.get("所属网格"),
            self.输入框_所属部门: kwargs.get("归属部门"),
            self.输入框_单位名称: kwargs.get("单位名称"),
            self.输入框_单位类型: kwargs.get("单位类型"),
        }
        self.快捷操作_填写表单_传入定位器(kwargs=定位器到输入值)


    def 校验查询条件成功修改(self, **kwargs):
        定位器到输入值 = {
            self.输入框_区域: kwargs.get("区域"),
            self.输入框_网格: kwargs.get("所属网格"),
            self.输入框_所属部门: kwargs.get("归属部门"),
            self.输入框_单位名称: kwargs.get("单位名称"),
            self.输入框_单位类型: kwargs.get("单位类型"),
        }
        self.校验表单中数据成功修改_传入定位器(kwargs=定位器到输入值)

    def 获取弹窗_删除申请(self):
        return self.page.locator('//div[@aria-label="删除申请"]')

    def 获取输入框_删除原因(self):
        return self.获取弹窗_删除申请().locator("xpath=//textarea[@placeholder='请输入删除原因']").locator("visible=true")

    def 填写输入框_删除原因(self, 删除原因: str):
        输入框_删除原因 = self.获取输入框_删除原因()
        # 输入框_删除原因.fill(删除原因,timeout=3000)
        输入框_删除原因.click()
        输入框_删除原因.clear()
        输入框_删除原因.focus()
        输入框_删除原因.press_sequentially(删除原因,delay=0)
        输入框_删除原因.blur()
        expect(self.获取输入框_删除原因()).to_have_value(删除原因)

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
        page = PageUnitInfo(page)

        page.填写输入框_删除原因("123123123213")


