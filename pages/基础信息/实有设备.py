from playwright.sync_api import Page

from module.base_query_page_new import BaseQueryPage


class PageRealEquipment(BaseQueryPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.输入框_选择小区 = self.page.locator(
            "//input[@placeholder='请选择小区']//ancestor::div[@class='el-form-item__content']").locator("visible=true")
        self.输入框_设备名称或编码 = self.page.locator(
            "//input[@placeholder='请输入设备名称或编码']//ancestor::div[@class='el-form-item__content']").locator("visible=true")
        self.输入框_设备状态 = self.page.locator(
            "//input[@placeholder='请选择设备状态']//ancestor::div[@class='el-form-item__content']").locator("visible=true")
        self.输入框_使用场景 = self.page.locator(
            "//input[@placeholder='请选择使用场景']//ancestor::div[@class='el-form-item__content']").locator("visible=true")

    def 输入查询条件(self, **kwargs):
         # 在页面对象中定义映射关系
        定位器到输入值 = {
            self.输入框_选择小区: kwargs.get("选择小区"),
            self.输入框_设备名称或编码: kwargs.get("设备名称或编码"),
            self.输入框_设备状态: kwargs.get("设备状态"),
            self.输入框_使用场景: kwargs.get("使用场景")
        }
        self.快捷操作_填写表单_传入定位器(kwargs=定位器到输入值)

    def 校验查询条件成功修改(self, **kwargs):
        定位器到输入值 = {
            self.输入框_选择小区: kwargs.get("选择小区"),
            self.输入框_设备名称或编码: kwargs.get("设备名称或编码"),
            self.输入框_设备状态: kwargs.get("设备状态"),
            self.输入框_使用场景: kwargs.get("使用场景")
        }
        self.校验表单中数据成功修改_传入定位器(kwargs=定位器到输入值)




