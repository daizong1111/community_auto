
from playwright.sync_api import Page, Locator, sync_playwright

from module.base_query_page_new import BaseQueryPage


class PageDeleteApproval(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.输入框_网格 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择所属网格']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_开始日期 = self.page.locator("//input[@placeholder='开始日期' and @class='el-range-input']")
        self.输入框_结束日期 = self.page.locator("//input[@placeholder='结束日期' and @class='el-range-input']")

    def 填写表单项_传入定位器(self, **kwargs):
        # 在页面对象中定义映射关系
        定位器到输入值 = {
            self.输入框_网格: kwargs.get("所属网格"),
        }
        self.快捷操作_填写表单_传入定位器(kwargs=定位器到输入值)
    def 选择所属网格(self, 网格名称: str):
        self.表单_下拉框选择(定位器=self.输入框_网格, 需要选择的项=网格名称)

    def 校验表单中数据成功修改_申请时间段(self, 开始时间_预期值:str, 结束时间_预期值:str):
        assert self.输入框_开始日期.input_value() == 开始时间_预期值 and self.输入框_结束日期.input_value() == 结束时间_预期值

    def 获取新增表单最上层定位(self):
        return self.page.locator('//div[@aria-label="新增"]').locator("visible=true")


    def 获取包含某文本内容的span标签(self, text: str):
        return self.page.locator(f"//span[contains(text(),'{text}')]").locator("visible=true")

    def 获取某span标签的相邻兄弟下的某标签中的内容(self, text_span:str, loc_type: str):
        """text_span:span标签内的文本内容
            loc_type:要在span标签的相邻兄弟下寻找的元素的类型
        """
        if loc_type == "span":
            return self.获取包含某文本内容的span标签(text_span).locator(f'xpath=./following-sibling::span').inner_html()
        elif loc_type == "textarea":
            return self.获取包含某文本内容的span标签(text_span).locator(f'xpath=./following-sibling::span//{loc_type}').input_value()
        else:
            raise ValueError("loc_type参数错误")

    def 校验详情页中内容(self, 详情页_span标签内容: dict):
        self.page.wait_for_timeout(2000)
        for key, value in 详情页_span标签内容.items():
            if key == "申请事由":
                内容_实际值 = self.获取某span标签的相邻兄弟下的某标签中的内容(key, "textarea")
                内容_预期值 = value

            else:
                内容_实际值 = self.获取某span标签的相邻兄弟下的某标签中的内容(key, "span")
                内容_预期值 = value.replace('\n',' ')

            assert 内容_实际值 == 内容_预期值, f"内容预期值与实际值不一致，预期值：{内容_预期值}，实际值：{内容_实际值}"

    def 获取表格中第i个审批按钮(self,i):
        return self.get_table_rows().locator("button",has_text="审批").nth(i-1)

    def 点击表格中第i个审批按钮(self,i):
        self.获取表格中第i个审批按钮(i).evaluate("el => el.click()")

    def 获取审批意见选项(self, 审批意见:str):
        """审批意见只可为通过或不通过"""
        return self.page.locator(f"//span[text()='{审批意见}']//preceding-sibling::span")

    def 获取不通过原因文本框(self):
        return self.page.locator("//textarea[@placeholder='请输入不通过原因']")

    def 获取审批弹窗(self):
        return self.page.locator("//div[@aria-label='审批']")

    def 提交审批表单(self, flag:bool, 不通过原因:str=None):
        """flag代表是否通过"""
        if flag == True:
            self.获取审批意见选项("通过").click()
        else:
            self.获取审批意见选项("不通过").click()
            self.获取不通过原因文本框().fill(不通过原因)
        self.click_button("确定", 按钮的父元素=self.获取审批弹窗())
        self.点击提示弹窗中的确定按钮()


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
        page = PageDeleteApproval(page)

        # print(page.获取某span标签的相邻兄弟下的某标签中的内容("申请时间", "span"))
        # print(page.获取某span标签的相邻兄弟下的某标签中的内容("申请事由", "textarea"))
        page.点击表格中第i个审批按钮(2)


