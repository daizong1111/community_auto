from playwright.sync_api import Page, Locator, sync_playwright, expect

from module.BasePageNew import PageObject
from module.base_query_page_new import BaseQueryPage


class PageSpecialCare(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.输入框_姓名 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入姓名']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_处理状态 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择处理状态']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_日期 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='开始日期']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")

        self.输入框_项目名称 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入走访项目名称']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_人员标签 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择人员标签']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_任务来源 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择任务来源']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")


    def 填写表单_新增片区(self):
        loc_可选片区 = self.page.locator(".areaCanSelect").locator("visible=true").first
        assert loc_可选片区.count() > 0, "无可选片区，需要手动添加"
        loc_可选片区.click()
        loc_可选楼栋 = self.page.locator(".el-checkbox-group .el-checkbox__input:not(.is-disabled)").locator(
            "visible=true").first
        expect(loc_可选楼栋).to_be_visible(), "无可选楼栋，需要手动添加"
        loc_可选楼栋.click()
        self.click_button("确定", 按钮的父元素=self.page.locator(".el-dialog-div-area"))

    def 查询数据库中的数据量(self, db_connection):
        self.get_db_data(db_connection, "select count(*) from ")

    def 输入查询条件(self, **kwargs):
        # 在页面对象中定义映射关系
        定位器到输入值 = {
            self.输入框_姓名: kwargs.get("姓名"),
            self.输入框_处理状态: kwargs.get("处理状态"),
            self.输入框_日期: kwargs.get("日期"),
            self.输入框_项目名称: kwargs.get("项目名称"),
            self.输入框_人员标签: kwargs.get("人员标签"),
            self.输入框_任务来源:kwargs.get("任务来源")
        }
        self.快捷操作_填写表单_传入定位器(kwargs=定位器到输入值)

    def 校验查询条件成功修改(self, **kwargs):
        定位器到输入值 = {
            self.输入框_姓名: kwargs.get("姓名"),
            self.输入框_处理状态: kwargs.get("处理状态"),
            # self.输入框_日期: kwargs.get("日期"),
            self.输入框_项目名称: kwargs.get("项目名称"),
            self.输入框_人员标签: kwargs.get("人员标签"),
            self.输入框_任务来源: kwargs.get("任务来源")
        }
        self.校验表单中数据成功修改_传入定位器(kwargs=定位器到输入值)
        日期_列表 = kwargs.get("日期").split(",")
        if len(日期_列表) == 2:
            self.校验查询条件_日期(日期_列表[0], 日期_列表[1])
        else:
            self.校验查询条件_日期("", "")

    def 校验查询条件_日期(self, 开始日期: str, 结束日期: str):
        开始日期_表单项内容 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='开始日期']").input_value()
        结束日期_表单项内容 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='结束日期']").input_value()
        assert 开始日期_表单项内容 == 开始日期 and 结束日期_表单项内容 == 结束日期, f"日期修改失败,开始日期_表单项内容:{开始日期_表单项内容},结束日期_表单项内容:{结束日期_表单项内容}"

    def loc_按钮_片区名称(self, 片区名称: str):
        return self.page.locator("button", has_text=片区名称).locator("visible=true")

    def loc_标签_楼栋名称(self, 楼栋名称: str):
        return self.page.locator(".el-checkbox-group .el-checkbox__label", has_text=楼栋名称).locator("visible=true")

    def 校验表单中无待选人员表单项(self):
        div_被访人员 = self.locators.表单项中包含操作元素的最上级div("选择被访人员")
        expect(div_被访人员.locator("div.item")).to_have_count(1)
        div_任务负责人 = self.locators.表单项中包含操作元素的最上级div("选择被访人员")
        expect(div_任务负责人.locator("div.item")).to_have_count(1)

    def 校验表单中位置成功修改(self, 位置: str):
        位置_表单项内容 = self.locators.表单项中包含操作元素的最上级div("位置").locator("input").input_value()
        # print(位置_表单项内容)
        assert 位置 in 位置_表单项内容, "位置修改失败"

    def 校验表单中项目时间成功修改(self, 开始日期: str, 结束日期: str):
        项目开始时间_表单项内容 = self.locators.表单项中包含操作元素的最上级div("项目时间").locator(
            "xpath=//input[@placeholder='开始日期']").input_value()
        项目结束时间_表单项内容 = self.locators.表单项中包含操作元素的最上级div("项目时间").locator(
            "xpath=//input[@placeholder='结束日期']").input_value()
        # print(项目开始时间_表单项内容, 项目结束时间_表单项内容)
        assert 项目开始时间_表单项内容 == 开始日期 and 项目结束时间_表单项内容 == 结束日期, f"项目时间修改失败,项目开始时间_表单项内容:{项目开始时间_表单项内容},项目结束时间_表单项内容:{项目结束时间_表单项内容}"

    def 获取被访人员列表(self):
        res = []
        loc_被访人员列表 = self.locators.表单项中包含操作元素的最上级div("选择被访人员").locator("div.item .el-tooltip")
        for 被访人员 in loc_被访人员列表.all():
            res.append(被访人员.text_content().split("__")[0])
        return res

    def 核对被访人员列表(self, 被访人员列表: list):
        列表_姓名 = self.get_column_values_by_name("姓名")
        assert 列表_姓名 == 被访人员列表, f"被访人员列表不一致, 预期值{被访人员列表}, 实际值{列表_姓名}"

    def 获取任务负责人列表(self):
        res = []
        loc_任务负责人列表 = self.locators.表单项中包含操作元素的最上级div("任务负责人").locator("div.item .el-tooltip")
        for 任务负责人 in loc_任务负责人列表.all():
            res.append(任务负责人.text_content())
        return res

    def 核对任务负责人列表(self, 任务负责人列表: list):
        列表_任务负责人 = self.get_column_values_by_name("任务负责人")
        任务负责人字符串 = ",".join(任务负责人列表)
        assert all(任务负责人 == 任务负责人字符串 for 任务负责人 in
                   列表_任务负责人), f"任务负责人列表不一致, 预期值{任务负责人字符串}, 实际值{列表_任务负责人}"


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
