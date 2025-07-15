
from playwright.sync_api import Page, Locator, sync_playwright, expect

from module.BasePageNew import PageObject
from module.base_query_page_new import BaseQueryPage


class PageAreaMesh(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.输入框_网格描述 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入网格描述']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_居委会 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择居委会']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_网格名称 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择网格']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
    def 获取新增表单最上层定位(self):
        return self.page.locator('//div[@aria-label="新增"]').locator("visible=true")

    def 填写表单_新增片区(self):
        loc_可选片区 = self.page.locator(".areaCanSelect").locator("visible=true").first
        assert loc_可选片区.count() > 0, "无可选片区，需要手动添加"
        loc_可选片区.click()
        loc_可选楼栋 = self.page.locator(".el-checkbox-group .el-checkbox__input:not(.is-disabled)").locator("visible=true").first
        expect(loc_可选楼栋).to_be_visible(), "无可选楼栋，需要手动添加"
        loc_可选楼栋.click()
        self.click_button("确定", 按钮的父元素=self.page.locator(".el-dialog-div-area"))

    def 查询数据库中的数据量(self, db_connection):
        self.get_db_data(db_connection, "select count(*) from ")

    def 输入查询条件(self, **kwargs):
        # 在页面对象中定义映射关系
        定位器到输入值 = {
            self.输入框_网格描述: kwargs.get("网格描述"),
            self.输入框_居委会: kwargs.get("居委会"),
            self.输入框_网格名称: kwargs.get("网格名称"),
        }
        self.快捷操作_填写表单_传入定位器(kwargs=定位器到输入值)


    def 校验查询条件成功修改(self, **kwargs):
        定位器到输入值 = {
            self.输入框_网格描述: kwargs.get("网格描述"),
            self.输入框_居委会:kwargs.get("居委会"),
            self.输入框_网格名称: kwargs.get("网格名称"),
        }
        self.校验表单中数据成功修改_传入定位器(kwargs=定位器到输入值)

    def loc_按钮_片区名称(self, 片区名称: str):
        return self.page.locator("button", has_text=片区名称).locator("visible=true")

    def loc_标签_楼栋名称(self, 楼栋名称: str):
        return self.page.locator(".el-checkbox-group .el-checkbox__label", has_text=楼栋名称).locator("visible=true")



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
        page = PageAreaMesh(page)
        page.填写表单_新增片区()



