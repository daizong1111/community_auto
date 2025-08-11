
from playwright.sync_api import Page, Locator, sync_playwright

from module.base_query_page_new import BaseQueryPage


class PageIncidentManage(BaseQueryPage):
    # 类属性初始化为 None
    输入框_类型 = None
    输入框_社区 = "loc:(//form[contains(@class,'query-form')]//input[@placeholder='请选择社区']//ancestor::div[@class='el-form-item__content'])[2]"
    输入框_小区 = "loc://form[contains(@class,'query-form')]//input[@placeholder='请选择小区']//ancestor::div[@class='el-form-item__content']"
    输入框_日期 = "loc://form[contains(@class,'query-form')]//input[@placeholder='发起日期']//ancestor::div[@class='el-form-item__content']"
    输入框_事件类型 = "loc://form[contains(@class,'query-form')]//input[@placeholder='请选择事件类型']//ancestor::div[@class='el-form-item__content']"
    输入框_处理状态 = "loc://form[contains(@class,'query-form')]//input[@placeholder='请选择处理状态']//ancestor::div[@class='el-form-item__content']"
    输入框_评价状态 = None
    输入框_上报人 = "loc://form[contains(@class,'query-form')]//input[@placeholder='请输入上报人']//ancestor::div[@class='el-form-item__content']"
    输入框_网格 = None
    输入框_处理人 = "loc://form[contains(@class,'query-form')]//input[@placeholder='请输入当前处理人']//ancestor::div[@class='el-form-item__content']"
    输入框_开始日期 = None
    输入框_结束日期 = None
    表单_处理 = None
    处理记录节点_最新 = None

    def __init__(self, page: Page):
        super().__init__(page)

    def 填写表单项_传入定位器(self, **kwargs):
        # 在页面对象中定义映射关系
        定位器到输入值 = {
            self.输入框_类型: kwargs.get("类型"),
            self.输入框_社区: kwargs.get("社区"),
            self.输入框_小区: kwargs.get("小区"),
            self.输入框_日期: kwargs.get("日期"),
            self.输入框_事件类型: kwargs.get("事件类型"),
            self.输入框_处理状态: kwargs.get("处理状态"),
            self.输入框_评价状态: kwargs.get("评价状态"),
            self.输入框_上报人: kwargs.get("上报人"),
            self.输入框_网格: kwargs.get("网格"),
            self.输入框_处理人: kwargs.get("处理人"),

        }
        self.快捷操作_填写表单_传入定位器(kwargs=定位器到输入值)

    def 校验定位器中数据成功修改(self, **kwargs):
        定位器到输入值 = {
            self.输入框_类型: kwargs.get("类型"),
            self.输入框_社区: kwargs.get("社区"),
            self.输入框_小区: kwargs.get("小区"),
            self.输入框_日期: kwargs.get("日期"),
            self.输入框_事件类型: kwargs.get("事件类型"),
            self.输入框_处理状态: kwargs.get("处理状态"),
            self.输入框_评价状态: kwargs.get("评价状态"),
            self.输入框_上报人: kwargs.get("上报人"),
            self.输入框_网格: kwargs.get("网格"),
            self.输入框_处理人: kwargs.get("处理人"),

        }
        self.校验表单中数据成功修改_传入定位器(kwargs=定位器到输入值)

    def 校验表单中数据成功修改_申请时间段(self, 开始时间_预期值: str, 结束时间_预期值: str):
        assert self.输入框_开始日期.input_value() == 开始时间_预期值 and self.输入框_结束日期.input_value() == 结束时间_预期值

    def 处理最新事件(self, 表单数据_工单处理:dict):
        self.点击表格中某行按钮(行号=1,按钮名="处理")
        self.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_工单处理,表单最上层定位=self.表单_处理)
        self.click_button("确定")









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
        page = PageIncidentManage(page)
        page.处理最新事件({"处理方式":"下发","指定处理人":"石**","处理意见":"同意","图片":r"C:\Users\Administrator\Pictures\111.png"})




