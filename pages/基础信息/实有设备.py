import pytest
from playwright.sync_api import Page, Locator

from module.base_query_page_new import BaseQueryPage


class PageRealEquipment(BaseQueryPage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.输入框_选择小区 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择小区']//ancestor::div[@class='el-form-item__content']").locator("visible=true")
        self.输入框_设备名称或编码 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请输入设备名称或编码']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_设备状态 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择设备状态']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")
        self.输入框_使用场景 = self.page.locator(
            "//form[contains(@class,'query-form')]//input[@placeholder='请选择使用场景']//ancestor::div[@class='el-form-item__content']").locator(
            "visible=true")

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

    def 填写安装位置(self):
        loc_地图 = self.page.locator(".mapcontainer .amap-container")
        bound = loc_地图.bounding_box()
        self.page.mouse.click(bound["x"]+bound["width"]/4, bound["y"]+bound["height"]/4)

    def 填写建设单位表单(self, timeout=None, 表单最上层定位: Locator = None, **kwargs):
        self.locators.表单项中包含操作元素的最上级div("选择小区")
        # 该函数要添加等待，等待所有的表单加载完成
        self.page.wait_for_timeout(1000)
        # 因为有些表单是选中了某些表单项后，会弹出一些新的表单项，所以需要处理
        页面上已有的表单项列表 = []
        已经有唯一表单项 = False
        if 表单最上层定位:
            # 这个判断逻辑的最终目的是得到一个处理后的表单最上层定位，可以通过代码自动寻找，但是有些情况下就是不大好找，可以手动传递到入参里
            处理后的表单最上层定位 = 表单最上层定位
        else:
            # 查询所有的el-form
            form_list = self.page.locator('.el-form').locator("visible=true")
            # 标记当前是否已经找到表单最上层定位
            flag = False
            # 遍历出所有的el-form
            for form in form_list.all():
                # 提取当前 form 中可见的文本内容
                form_text = form.text_content().strip()

                # 判断是否包含所有 kwargs 中的表单项名称
                missing_items = [item for item in kwargs.keys() if item not in form_text]

                if not missing_items:
                    处理后的表单最上层定位 = form
                    flag = True
                    # highlight_elements(self.page, [处理后的表单最上层定位])
                    break

            if not flag:
                raise Exception(f"未找到包含所有指定表单项的表单，缺失字段: {', '.join(missing_items)}")

        for 表单项, 内容 in kwargs.items():
            表单项中包含操作元素的最上级div = self.locators.表单项中包含操作元素的最上级div(表单项,
                                                                                            处理后的表单最上层定位).first

            assert 表单项中包含操作元素的最上级div.count() > 0, f"表单项: {表单项} 的最上级div未找到"

            if 内容 is None:  # 校验是否为 disabled 或 readonly 状态
                # 定位到 input 或 textarea 元素
                输入框 = 表单项中包含操作元素的最上级div.locator("input,textarea").first
                assert 输入框.is_disabled() or 输入框.get_attribute("readonly") is not None, \
                    f"表单项 '{表单项}' 应为只读或禁用状态，实际可编辑"
                continue

            # if 表单项中包含操作元素的最上级div.locator(
            #         ".el-input").count():
            #     self.表单_文本框填写(表单项名称=表单项, 需要填写的文本=内容, 表单最上层定位=处理后的表单最上层定位,
            #                          timeout=timeout)
            if 表单项中包含操作元素的最上级div.locator(
                    ">.el-input, .el-textarea").count() and 表单项中包含操作元素的最上级div.locator(
                ".el-icon-date").count() == 0:
                # if 表单项中包含操作元素的最上级div.locator(">.el-input, .el-textarea:not(.el-select):not(.el-cascader):not(.el-date-editor--date):not(.el-date-editor--datetime):not(.el-date-editor--datetimerange):not(.el-upload)").count():
                self.表单_文本框填写(定位器=表单项中包含操作元素的最上级div, 需要填写的文本=内容,
                                     表单最上层定位=处理后的表单最上层定位,
                                     timeout=8000)
            elif 表单项中包含操作元素的最上级div.locator(".el-select").count():
                self.表单_下拉框选择(定位器=表单项中包含操作元素的最上级div, 需要选择的项=内容,
                                     表单最上层定位=处理后的表单最上层定位,
                                     timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-cascader").count():
                self.表单_级联选择器选择(定位器=表单项中包含操作元素的最上级div, 路径=内容,
                                         表单最上层定位=处理后的表单最上层定位,
                                         timeout=timeout)
            # elif 表单项中包含操作元素的最上级div.locator(".ant-radio-group").count():
            #     self.表单_radio选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位,
            #                         timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-date-editor--date, .el-date-editor--datetime").count():
                self.表单_日期时间选择器(定位器=表单项中包含操作元素的最上级div, 日期=内容,
                                         表单最上层定位=处理后的表单最上层定位,
                                         timeout=timeout)
            # elif 表单项中包含操作元素的最上级div.get_by_role("switch").count():
            #     self.表单_switch开关(表单项名称=表单项, 开关状态=内容, 表单最上层定位=处理后的表单最上层定位,
            #                          timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-date-editor--datetimerange").count():
                self.表单_日期时间范围选择器_左右面板联动(定位器=表单项中包含操作元素的最上级div, 日期=内容,
                                                          表单最上层定位=处理后的表单最上层定位,
                                                          timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-upload").count():
                self.表单_文件上传(定位器=表单项中包含操作元素的最上级div, 文件路径=内容,
                                   表单最上层定位=处理后的表单最上层定位,
                                   timeout=timeout)
            else:
                pytest.fail(f"不支持的快捷表单填写:\n{表单项}:{内容}")

    def 填写运维厂商表单(self, timeout=None, 表单最上层定位: Locator = None, **kwargs):
        self.locators.表单项中包含操作元素的最上级div("选择小区")
        # 该函数要添加等待，等待所有的表单加载完成
        self.page.wait_for_timeout(1000)
        # 因为有些表单是选中了某些表单项后，会弹出一些新的表单项，所以需要处理
        页面上已有的表单项列表 = []
        已经有唯一表单项 = False
        if 表单最上层定位:
            # 这个判断逻辑的最终目的是得到一个处理后的表单最上层定位，可以通过代码自动寻找，但是有些情况下就是不大好找，可以手动传递到入参里
            处理后的表单最上层定位 = 表单最上层定位
        else:
            # 查询所有的el-form
            form_list = self.page.locator('.el-form').locator("visible=true")
            # 标记当前是否已经找到表单最上层定位
            flag = False
            # 遍历出所有的el-form
            for form in form_list.all():
                # 提取当前 form 中可见的文本内容
                form_text = form.text_content().strip()

                # 判断是否包含所有 kwargs 中的表单项名称
                missing_items = [item for item in kwargs.keys() if item not in form_text]

                if not missing_items:
                    处理后的表单最上层定位 = form
                    flag = True
                    # highlight_elements(self.page, [处理后的表单最上层定位])
                    break

            if not flag:
                raise Exception(f"未找到包含所有指定表单项的表单，缺失字段: {', '.join(missing_items)}")

        for 表单项, 内容 in kwargs.items():
            表单项中包含操作元素的最上级div = self.locators.表单项中包含操作元素的最上级div(表单项,处理后的表单最上层定位).nth(-1)


            assert 表单项中包含操作元素的最上级div.count() > 0, f"表单项: {表单项} 的最上级div未找到"

            if 内容 is None:  # 校验是否为 disabled 或 readonly 状态
                # 定位到 input 或 textarea 元素
                输入框 = 表单项中包含操作元素的最上级div.locator("input,textarea").first
                assert 输入框.is_disabled() or 输入框.get_attribute("readonly") is not None, \
                    f"表单项 '{表单项}' 应为只读或禁用状态，实际可编辑"
                continue

            # if 表单项中包含操作元素的最上级div.locator(
            #         ".el-input").count():
            #     self.表单_文本框填写(表单项名称=表单项, 需要填写的文本=内容, 表单最上层定位=处理后的表单最上层定位,
            #                          timeout=timeout)
            if 表单项中包含操作元素的最上级div.locator(
                    ">.el-input, .el-textarea").count() and 表单项中包含操作元素的最上级div.locator(
                ".el-icon-date").count() == 0:
                # if 表单项中包含操作元素的最上级div.locator(">.el-input, .el-textarea:not(.el-select):not(.el-cascader):not(.el-date-editor--date):not(.el-date-editor--datetime):not(.el-date-editor--datetimerange):not(.el-upload)").count():
                self.表单_文本框填写(定位器=表单项中包含操作元素的最上级div, 需要填写的文本=内容,
                                     表单最上层定位=处理后的表单最上层定位,
                                     timeout=8000)
            elif 表单项中包含操作元素的最上级div.locator(".el-select").count():
                self.表单_下拉框选择(定位器=表单项中包含操作元素的最上级div, 需要选择的项=内容,
                                     表单最上层定位=处理后的表单最上层定位,
                                     timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-cascader").count():
                self.表单_级联选择器选择(定位器=表单项中包含操作元素的最上级div, 路径=内容,
                                         表单最上层定位=处理后的表单最上层定位,
                                         timeout=timeout)
            # elif 表单项中包含操作元素的最上级div.locator(".ant-radio-group").count():
            #     self.表单_radio选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位,
            #                         timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-date-editor--date, .el-date-editor--datetime").count():
                self.表单_日期时间选择器(定位器=表单项中包含操作元素的最上级div, 日期=内容,
                                         表单最上层定位=处理后的表单最上层定位,
                                         timeout=timeout)
            # elif 表单项中包含操作元素的最上级div.get_by_role("switch").count():
            #     self.表单_switch开关(表单项名称=表单项, 开关状态=内容, 表单最上层定位=处理后的表单最上层定位,
            #                          timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(
                    ".el-date-editor--datetimerange,.el-date-editor--daterange").count():
                self.表单_日期时间范围选择器_左右面板联动(表单项名称=表单项, 日期=内容,
                                                          表单最上层定位=处理后的表单最上层定位,
                                                          timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-upload").count():
                self.表单_文件上传(定位器=表单项中包含操作元素的最上级div, 文件路径=内容,
                                   表单最上层定位=处理后的表单最上层定位,
                                   timeout=timeout)
            else:
                pytest.fail(f"不支持的快捷表单填写:\n{表单项}:{内容}")

    def 校验在线状态(self, 状态: str):
        assert self.page.locator(".onLine").inner_text() == 状态