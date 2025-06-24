import re

from playwright.sync_api import Page, Locator, expect

from module.base_query_page import BaseQueryPage


class PageSpecialPeople(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)

    def 获取提示弹窗(self):
        return self.page.locator(".el-message-box")
    def 获取提示弹窗中的确定按钮(self):
        return self.获取提示弹窗().locator("button", has_text="确定")

    def 点击提示弹窗中的确定按钮(self):
        self.获取提示弹窗中的确定按钮().click()

    # 该页面的下拉框属于多选框，需要重新编写逻辑
    def 表单_下拉框选择(self, 表单项名称: str, 需要选择的项: list, 表单最上层定位: Locator = None,
                        timeout: float = None):
        if 需要选择的项 is None:
            return

        if 表单最上层定位:
            表单项 = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                "visible=true")
            # 清空内容
            # 下拉箭头_下拉框 = 表单项.locator("i.el-select__caret").locator("visible=true")
            try:
                表单项.locator("i.el-select__caret").locator("visible=true").hover(timeout=1000)
            except:
                pass
            # 将鼠标悬停到下拉箭头_下拉框上面
            # box = 下拉箭头_下拉框.first.bounding_box()
            # self.page.mouse.move(100, 100, steps=100)
            #
            # self.page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2, steps=100)
            # 下拉箭头_下拉框.hover(force=True)
            关闭按钮 = 表单项.locator(".el-icon-circle-close").locator("visible=true")
            expect(关闭按钮).to_be_visible()
            if 关闭按钮.count() > 0:
                关闭按钮.click()

            表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                "visible=true").click(timeout=timeout)
            for 当前要选的项 in 需要选择的项:
                if 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                        '//input[@type="search"]').count():
                    表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                        '//input[@type="search"]').fill(当前要选的项, timeout=timeout)
                # self.page.locator(".ant-select-dropdown").locator("visible=true").get_by_text(需要选择的项).click(timeout=timeout)
                选择面板 = self.page.locator(".el-select-dropdown").locator("visible=true")
                选择面板.get_by_text(当前要选的项, exact=True).first.click(timeout=timeout)
        else:
            表单项 = self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("visible=true")
            下拉箭头_下拉框 = 表单项.locator("i.el-select__caret").locator("visible=true")
            # 清空内容
            # 将鼠标悬停到下拉箭头_下拉框上面
            box = 下拉箭头_下拉框.first.bounding_box()
            self.page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
            # 表单项.hover()
            关闭按钮 = 表单项.locator(".el-icon-circle-close").locator("visible=true")
            expect(关闭按钮).to_be_visible()
            if 关闭按钮.count() > 0:
                关闭按钮.click()
            self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("visible=true").click(timeout=timeout)
            for 当前要选的项 in 需要选择的项:
                # self.page.locator(".ant-select-dropdown").locator()
                if self.locators.表单项中包含操作元素的最上级div(表单项名称).locator('//input[@type="search"]').count():
                    self.locators.表单项中包含操作元素的最上级div(表单项名称).locator('//input[@type="search"]').fill(
                        需要选择的项, timeout=timeout)
                选择面板 = self.page.locator(".el-select-dropdown").locator("visible=true")
                # self.page.locator(".ant-select-dropdown").locator("visible=true").get_by_text(需要选择的项).click(timeout=timeout)
                选择面板.get_by_text(当前要选的项, exact=True).first.click(timeout=timeout)

        表单项的标签 = 表单最上层定位.locator("label",has_text=表单项名称).locator("visible=true")
        表单项的标签.click()

    def 检查人口标签是否修改成功(self, 修改后的标签名:list):
        loc_人口标签 = self.page.locator("//label[text()='人口标签']/following-sibling::div//span[@class='el-select__tags-text']")
        # 获取所有满足条件的 Locator 元素列表
        # loc_list = loc_人口标签.all().element_handles()

        # 使用 enumerate 遍历并获取当前下标
        for index, element_handle in enumerate(loc_人口标签.all()):
            # 获取输入框的值
            标签内容 = element_handle.inner_text()
            print(标签内容)
            print(修改后的标签名[index])
            assert 标签内容 == 修改后的标签名[index], f"第{index}个标签内容修改失败，期望：{修改后的标签名[index]}，实际：{标签内容}"
            # print(f"下标 {index} 的标签内容: {标签内容}")





