from playwright.sync_api import Page

from module.BasePage import PageObject
class 场所信息(PageObject):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/sqaq/csgl/csxx"
        self.商铺名称_搜索框 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入商铺名称']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")

    def 输入查询条件(self, **kwargs):
        # 在页面对象中定义映射关系
        定位器到输入值 = {
            self.商铺名称_搜索框: kwargs.get("商铺名称"),
        }
        self.快捷操作_填写表单_传入定位器(kwargs=定位器到输入值)


