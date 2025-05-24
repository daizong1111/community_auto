import time

import pytest
from playwright.sync_api import Locator, Page, expect, sync_playwright

from module import *
from module.table import Table
from module.locators import Locators
from utils.my_date import *

def 数字月份转中文(month: int) -> str:
    月份映射 = {
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
        10: "十",
        11: "十一",
        12: "十二"
    }
    return 月份映射.get(month, str(month))


class PageObject:
    def __init__(self, page: Page):
        self.page = page
        self.url = ""
        self.locators = Locators(self.page)

    def navigate(self):
        self.page.goto(self.url)

    def table(self, 唯一文字, 表格序号=-1):
        return Table(self.page, 唯一文字, 表格序号)

    def click_button(self, button_name, timeout=30_000):
        button_loc = self.page.locator("button")
        for 单字符 in button_name:
            button_loc = button_loc.filter(has_text=单字符)
        button_loc.click(timeout=timeout)

    def search(self, 搜索内容: str, placeholder=None):
        if placeholder:
            self.page.locator(
                f"//span[@class='ant-input-affix-wrapper']//input[contains(@placeholder,'{placeholder}')]").fill(
                搜索内容)
        else:
            self.page.locator(".ant-input-affix-wrapper input").fill(搜索内容)
        self.page.wait_for_load_state("networkidle")

    # 该函数在会议室管理系统中测试通过
    def 表单_文本框填写(self, 表单项名称: str, 需要填写的文本: str, 表单最上层定位: Locator = None,
                        timeout: float = None):
        if 表单最上层定位:
            表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                "input,textarea").locator("visible=true").last.fill(需要填写的文本, timeout=timeout)
        else:
            self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("input,textarea").locator(
                "visible=true").last.fill(需要填写的文本, timeout=timeout)

    # 该函数在会议室管理系统中测试通过
    def 表单_下拉框选择(self, 表单项名称: str, 需要选择的项: str, 表单最上层定位: Locator = None,
                        timeout: float = None):
        if 表单最上层定位:
            表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                "visible=true").click(timeout=timeout)
            if 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                    '//input[@type="search"]').count():
                表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                    '//input[@type="search"]').fill(需要选择的项, timeout=timeout)
            # self.page.locator(".ant-select-dropdown").locator("visible=true").get_by_text(需要选择的项).click(timeout=timeout)
            self.page.locator(".el-select-dropdown").locator("visible=true").get_by_text(需要选择的项).click(
                timeout=timeout)
        else:
            self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("visible=true").click(timeout=timeout)
            if self.locators.表单项中包含操作元素的最上级div(表单项名称).locator('//input[@type="search"]').count():
                self.locators.表单项中包含操作元素的最上级div(表单项名称).locator('//input[@type="search"]').fill(
                    需要选择的项, timeout=timeout)
            # self.page.locator(".ant-select-dropdown").locator("visible=true").get_by_text(需要选择的项).click(timeout=timeout)
            self.page.locator(".el-select-dropdown").locator("visible=true").get_by_text(需要选择的项).click(
                timeout=timeout)
        expect(self.page.locator(".el-select-dropdown")).to_be_hidden(timeout=timeout)

    def 表单_级联选择器选择(self, 表单项名称: str, 路径: str, 表单最上层定位: Locator = None, timeout: float = None):
        """
        在 Element Plus 的级联选择器中选择指定路径的项。

        :param 表单项名称: 表单项标签名，如 "所属区域"
        :param 路径: 级联路径，如 "北京/朝阳区" 或 "一级分类/二级分类/三级分类"
        :param 表单最上层定位: 如果在弹窗或嵌套容器中，传入该容器的 Locator
        :param timeout: 操作超时时间
        """
        分段路径 = 路径.split("/")

        if 表单最上层定位:
            # 定位到当前表单项并点击打开级联选择器
            表单元素 = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称))
        else:
            表单元素 = self.locators.表单项中包含操作元素的最上级div(表单项名称)

        # 打开级联选择器
        表单元素.locator("input.el-input__inner").click(timeout=timeout)

        # 获取当前显示的级联面板
        dropdown = self.page.locator(".el-cascader__dropdown").locator("visible=true")

        # 遍历分段路径中的每个节点，为每个节点找到对应的菜单项并点击
        for index, 节点 in enumerate(分段路径):
            # 定位到当前层级的菜单列表
            menu_list = dropdown.locator(f".el-cascader-menu:nth-child({index + 1}) .el-cascader-menu__list")
            # 在当前菜单列表中找到含有指定节点文本的第一个菜单项
            item_locator = menu_list.locator(".el-cascader-node", has_text=节点).first
            # item_locator = menu_list.get_by_role("menuitem", exact=True).filter(has_text=节点).first
            # 先尝试找 checkbox/radio
            checkbox = item_locator.locator("label").first
            if checkbox.count() > 0:
                checkbox.check(timeout=timeout)
            else:
                # 点击找到的菜单项，带有超时设置
                item_locator.click(timeout=timeout)
        self.page.mouse.click(x=10, y=10)
        # 等待级联选择面板关闭
        expect(dropdown).to_be_hidden(timeout=timeout or 5000)

    # def 表单_日期_element(self, 表单项名称: str, 日期: str, 表单最上层定位: Locator = None, timeout: float = None):
    #     """
    #     填写基于 Element Plus 的 el-date-picker 控件的日期表单项。
    #
    #     :param 表单项名称: 表单项标签名，例如 "开始时间"
    #     :param 日期: 日期字符串，支持如下格式：
    #                  - 单个日期："2025-04-05" 或 "2025-04-05 14:30"
    #                  - 范围日期："2025-04-05,2025-04-10" 或 "2025-04-05 14:30,2025-04-10 18:00"
    #     :param 表单最上层定位: 如果在弹窗或嵌套容器中，传入该容器的 Locator
    #     :param timeout: 超时时间（毫秒）
    #     """
    #
    #     if 表单最上层定位:
    #         date_picker = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称))
    #     else:
    #         date_picker = self.locators.表单项中包含操作元素的最上级div(表单项名称)
    #
    #     # 点击打开日期选择面板
    #     date_picker.locator("input").first.click(timeout=timeout)
    #
    #     # 获取当前显示的日期面板
    #     picker_panel = self.page.locator(".el-picker-panel").locator("visible=true")
    #
    #     # 解析输入日期
    #     日期列表 = 日期.split(",")
    #
    #     for index, 单日期 in enumerate(日期列表):
    #         try:
    #             days_offset = int(单日期)
    #             格式化后的日期 = 返回当前时间xxxx_xx_xx加N天(days_offset)
    #         except ValueError:
    #             格式化后的日期 = 单日期
    #
    #         # 定位到对应的日期输入框并填充
    #         date_input = picker_panel.locator(".el-date-range-picker__editor input").nth(index) if len(日期列表) > 1 \
    #             else date_picker.locator(".el-date-editor input")
    #
    #         date_input.fill(格式化后的日期, timeout=timeout)
    #
    #     # 点击确认按钮关闭日期选择器
    #     picker_panel.get_by_text("确定").click(timeout=timeout or 3000)

    def 表单_日期范围选择器_左右面板联动(self, 表单项名称: str, 日期: str, 表单最上层定位: Locator = None, timeout: float = None):
        """
        填写基于 Element Plus 的 el-date-picker 控件的日期表单项（通过点击选择）。

        :param 表单项名称: 表单项标签名，例如 "开始时间"
        :param 日期: 日期字符串，支持如下格式：
                     - 范围日期时间："2025-04-05 03:02:00,2025-04-10 05:20:35"
        :param 表单最上层定位: 如果在弹窗或嵌套容器中，传入该容器的 Locator
        :param timeout: 超时时间（毫秒）
        """
        if 日期 is None:
            return

        from datetime import datetime

        if 表单最上层定位:
            date_picker = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称))
        else:
            date_picker = self.locators.表单项中包含操作元素的最上级div(表单项名称)

        if 日期 == "":
            # 清空表单项
            # 将鼠标悬停到表单项上
            date_picker.hover()
            清空按钮 = date_picker.locator(".el-range__close-icon")
            # 若出现了清空按钮，则点击清空按钮
            if 清空按钮.count() > 0:
                清空按钮.click(timeout=timeout)
            return
        # 打开日期选择面板
        date_picker.locator("input").first.click(timeout=timeout)

        # 获取当前显示的日期面板
        picker_panel = self.page.locator(".el-picker-panel").locator("visible=true")

        # 解析输入日期
        日期列表 = 日期.split(",")

        # 定位控制按钮
        上一年按钮 = picker_panel.locator("button.el-icon-d-arrow-left").locator("visible=true")
        下一年按钮 = picker_panel.locator("button.el-icon-d-arrow-right").locator("visible=true")
        上一月按钮 = picker_panel.locator("button.el-icon-arrow-left").locator("visible=true")
        下一月按钮 = picker_panel.locator("button.el-icon-arrow-right").locator("visible=true")

        for index, 单日期 in enumerate(日期列表):
            try:
                days_offset = int(单日期)
                格式化后的日期 = 返回当前时间xxxx_xx_xx加N天(days_offset)
            except ValueError:
                格式化后的日期 = 单日期

            dt = datetime.strptime(格式化后的日期, "%Y-%m-%d %H:%M:%S")
            target_year = dt.year
            target_month = dt.month
            target_day = dt.day

            # 左右面板定位器
            date_tables = picker_panel.locator(".el-date-table")

            # 判断是哪个面板需要调整（index == 0 为开始时间，index == 1 为结束时间）
            panel_index = 0 if index == 0 or len(日期列表) == 1 else 1

            while True:
                # 等待年月标签出现（最多等待 timeout 毫秒）
                start_time = time.time()
                while (time.time() - start_time) < (timeout or 5000) / 1000:
                    month_labels = picker_panel.locator("div:not([class])", has_text="年").filter(has_text="月").all()
                    if len(month_labels) > panel_index:
                        break
                    time.sleep(0.2)
                else:
                    raise TimeoutError(f"超时：未找到足够的年份标签，期望至少 {panel_index + 1} 个")

                # 获取当前面板的年月
                current_label = month_labels[panel_index].inner_html()
                年份_str, 月份_str = current_label.split("年")
                current_year = int(年份_str)
                current_month = int(月份_str.replace("月", ""))

                # 如果已经匹配，跳出循环
                if current_year == target_year and current_month == target_month:
                    break

                # 控制面板切换
                if current_year > target_year:
                    上一年按钮.first.click(timeout=timeout)
                elif current_year < target_year:
                    下一年按钮.first.click(timeout=timeout)
                elif current_year == target_year and current_month > target_month:
                    上一月按钮.first.click(timeout=timeout)
                elif current_year == target_year and current_month < target_month:
                    下一月按钮.first.click(timeout=timeout)
            # 在对应面板中选择日期
            date_tables.nth(panel_index).locator(".available span", has_text=str(target_day)).first.click(
                timeout=timeout)

    def _select_time_in_picker(self, time_panel: Locator, time_info: dict, timeout: float = None):
        hour_str = f"{time_info['hour']:02d}"
        minute_str = f"{time_info['minute']:02d}"
        second_str = f"{time_info['second']:02d}"

        # 选择小时
        hour_spinner = time_panel.locator(".el-time-spinner__list").nth(0).locator(".el-time-spinner__item",
                                                                                   has_text=hour_str).first
        hour_spinner.scroll_into_view_if_needed(timeout=timeout)
        # hour_spinner.click(timeout=timeout)

        # 选择分钟
        minute_spinner = time_panel.locator(".el-time-spinner__list").nth(1).locator(".el-time-spinner__item",
                                                                                     has_text=minute_str).first
        minute_spinner.scroll_into_view_if_needed(timeout=timeout)
        # minute_spinner.click(timeout=timeout)

        # 判断是否支持秒
        if time_panel.locator(".el-time-spinner__list").count() >= 3:
            second_spinner = time_panel.locator(".el-time-spinner__list").nth(2).locator(".el-time-spinner__item",
                                                                                         has_text=second_str).first
            second_spinner.scroll_into_view_if_needed(timeout=timeout)
            # second_spinner.click(timeout=timeout)

        # 点击时间选择器中的“确定”
        time_panel.get_by_text("确定").click(timeout=timeout)

    def 表单_日期时间范围选择器_左右面板联动(self, 表单项名称: str, 日期: str, 表单最上层定位: Locator = None, timeout: float = None):
        """
        填写基于 Element Plus 的 el-date-picker 控件的日期表单项（通过点击选择）。

        :param 表单项名称: 表单项标签名，例如 "开始时间"
        :param 日期: 日期字符串，支持如下格式：
                     - 范围日期："2025-04-05,2025-04-10" "2060-07-05 03:02:00,2060-08-29 05:04:00"
        :param 表单最上层定位: 如果在弹窗或嵌套容器中，传入该容器的 Locator
        :param timeout: 超时时间（毫秒）
        """
        if 日期 is None:
            return

        from datetime import datetime

        if 表单最上层定位:
            date_picker = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称))
        else:
            date_picker = self.locators.表单项中包含操作元素的最上级div(表单项名称)

        if 日期 == "":
            # 清空表单项
            # 将鼠标悬停到表单项上
            date_picker.hover()
            清空按钮 = date_picker.locator(".el-range__close-icon")
            # 若出现了清空按钮，则点击清空按钮
            if 清空按钮.count() > 0:
                清空按钮.click(timeout=timeout)
            return
        # 打开日期选择面板
        date_picker.locator("input").first.click(timeout=timeout)

        # 获取当前显示的日期面板
        picker_panel = self.page.locator(".el-picker-panel").locator("visible=true")

        # 解析输入日期
        日期列表 = 日期.split(",")

        # 定位控制按钮
        上一年按钮 = picker_panel.locator("button.el-icon-d-arrow-left").locator("visible=true")
        下一年按钮 = picker_panel.locator("button.el-icon-d-arrow-right").locator("visible=true")
        上一月按钮 = picker_panel.locator("button.el-icon-arrow-left").locator("visible=true")
        下一月按钮 = picker_panel.locator("button.el-icon-arrow-right").locator("visible=true")

        # 保存两个时间的信息
        start_time_info = None
        end_time_info = None

        for index, 单日期 in enumerate(日期列表):
            try:
                days_offset = int(单日期)
                格式化后的日期 = 返回当前时间xxxx_xx_xx加N天(days_offset)
            except ValueError:
                格式化后的日期 = 单日期

            dt = None
            formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]
            for fmt in formats:
                try:
                    dt = datetime.strptime(格式化后的日期, fmt)
                    break
                except ValueError:
                    continue
            if not dt:
                raise ValueError(f"无法识别的日期时间格式：{格式化后的日期}")

            target_year = dt.year
            target_month = dt.month
            target_day = dt.day
            # 判断是否包含时间信息
            has_time_info = dt.hour != 0 or dt.minute != 0 or dt.second != 0

            # 保存时间信息
            time_info = {
                "hour": dt.hour,
                "minute": dt.minute,
                "second": dt.second,
                "has_time_info": has_time_info
            }

            if index == 0:
                start_time_info = time_info
            elif index == 1:
                end_time_info = time_info

            # 左右面板定位器
            date_tables = picker_panel.locator(".el-date-table")

            # 判断是哪个面板需要调整（index == 0 为开始时间，index == 1 为结束时间）
            panel_index = 0 if index == 0 or len(日期列表) == 1 else 1

            while True:
                # 等待年月标签出现（最多等待 timeout 毫秒）
                start_time = time.time()
                while (time.time() - start_time) < (timeout or 5000) / 1000:
                    month_labels = picker_panel.locator("div:not([class])", has_text="年").filter(has_text="月").all()
                    if len(month_labels) > panel_index:
                        break
                    time.sleep(0.2)
                else:
                    raise TimeoutError(f"超时：未找到足够的年份标签，期望至少 {panel_index + 1} 个")

                # 获取当前面板的年月
                current_label = month_labels[panel_index].inner_html()
                年份_str, 月份_str = current_label.split("年")
                current_year = int(年份_str)
                current_month = int(月份_str.replace("月", ""))

                # 如果已经匹配，跳出循环
                if current_year == target_year and current_month == target_month:
                    break

                # 控制面板切换
                if current_year > target_year:
                    上一年按钮.first.click(timeout=timeout)
                elif current_year < target_year:
                    下一年按钮.first.click(timeout=timeout)
                elif current_year == target_year and current_month > target_month:
                    上一月按钮.first.click(timeout=timeout)
                elif current_year == target_year and current_month < target_month:
                    下一月按钮.first.click(timeout=timeout)
            # 在对应面板中选择日期
            date_tables.nth(panel_index).locator(".available span", has_text=str(target_day)).first.click(
                timeout=timeout)

        if start_time_info["has_time_info"] or (end_time_info and end_time_info["has_time_info"]):
            # 点击开始时间输入框，打开时间面板
            start_time_input = picker_panel.get_by_placeholder("开始时间")
            start_time_input.click(timeout=timeout)

            # 显式等待时间面板出现
            time_panel = picker_panel.locator(".el-time-panel").locator("visible=true")
            expect(time_panel).to_be_visible(timeout=timeout)

            # 处理开始时间
            self._select_time_in_picker(time_panel, start_time_info, timeout)

            # 等待time_panel消失
            expect(time_panel).to_be_hidden(timeout=timeout)

            # 如果是范围时间，并且有结束时间信息，则处理结束时间
            if len(日期列表) > 1 and end_time_info and end_time_info["has_time_info"]:
                # 等待“结束时间”输入框可见并点击
                end_time_input = picker_panel.get_by_placeholder("结束时间")
                end_time_input.wait_for(timeout=timeout)
                end_time_input.click(timeout=timeout)
                # 再次确认时间面板仍然可见
                expect(time_panel).to_be_visible(timeout=timeout)
                # 处理结束时间
                self._select_time_in_picker(time_panel, end_time_info, timeout)

        # 最后点击确定按钮
        确定按钮 = picker_panel.locator(".el-picker-panel__footer").get_by_text("确定").locator("visible=true")
        if 确定按钮.is_visible():
            确定按钮.click(timeout=timeout)

    def 表单_radio选择(self, 表单项名称: str, 需要选择的项: str, 表单最上层定位: Locator = None, timeout: float = None):
        if 表单最上层定位:
            表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator("label").locator(
                "visible=true").filter(has_text=需要选择的项).locator("input").check(timeout=timeout)
        else:
            self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("label").locator("visible=true").filter(
                has_text=需要选择的项).locator("input").check(timeout=timeout)

    def 表单_switch开关(self, 表单项名称: str, 开关状态: str, 表单最上层定位: Locator = None, timeout: float = None):
        if "开" in 开关状态 or "是" in 开关状态:
            开关状态bool = True
        else:
            开关状态bool = False
        if 表单最上层定位:
            表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).get_by_role(
                "switch").set_checked(开关状态bool, timeout=timeout)
        else:
            self.locators.表单项中包含操作元素的最上级div(表单项名称).get_by_role("switch").set_checked(开关状态bool,
                                                                                                        timeout=timeout)

    def 表单_日期(self, 表单项名称: str, 日期: str, 表单最上层定位: Locator = None, timeout: float = None):
        if 表单最上层定位:
            日期控件定位 = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称))
        else:
            日期控件定位 = self.locators.表单项中包含操作元素的最上级div(表单项名称)
        日期列表 = 日期.split(",")
        for index, 单日期 in enumerate(日期列表):
            try:
                int(单日期)
                格式化后的日期 = 返回当前时间xxxx_xx_xx加N天(int(单日期))
            except:
                格式化后的日期 = 单日期
            日期控件定位.locator("input").nth(index).click(timeout=timeout)
            日期控件定位.locator("input").nth(index).fill(格式化后的日期, timeout=timeout)
            日期控件定位.locator("input").nth(index).blur(timeout=timeout)

    def 快捷操作_填写表单(self, 表单最上层定位: Locator = None, timeout=None, **kwargs):
        for 表单项, 内容 in kwargs.items():
            if not 内容:
                continue
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-input").count():
                self.表单_文本框填写(表单项名称=表单项, 需要填写的文本=内容, 表单最上层定位=表单最上层定位,
                                     timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-select-selector").count():
                self.表单_下拉框选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=表单最上层定位,
                                     timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-radio-group").count():
                self.表单_radio选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=表单最上层定位,
                                    timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).get_by_role("switch").count():
                self.表单_switch开关(表单项名称=表单项, 开关状态=内容, 表单最上层定位=表单最上层定位, timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-picker").count():
                self.表单_日期(表单项名称=表单项, 日期=内容, 表单最上层定位=表单最上层定位, timeout=timeout)
            else:
                pytest.fail(f"不支持的快捷表单填写:\n{表单项}:{内容}")

    def 快捷操作_填写表单_增加根据数据类确定唯一表单版(self, 表单最上层定位: Locator = None, timeout=None, **kwargs):
        页面上已有的表单项列表 = []
        已经有唯一表单项 = False
        if 表单最上层定位:
            处理后的表单最上层定位 = 表单最上层定位
        else:
            for index, 表单项 in enumerate(kwargs.keys()):
                if index == 0:
                    try:
                        self.locators.表单项中包含操作元素的最上级div(表单项).last.wait_for(timeout=timeout)
                    except:
                        pass

                if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 0:
                    continue
                else:
                    if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 1:
                        已经有唯一表单项 = True
                    页面上已有的表单项列表.append(self.locators.表单项中包含操作元素的最上级div(表单项))
                if 已经有唯一表单项 and len(页面上已有的表单项列表) >= 2:
                    break

            包含可见表单项的loc = self.page.locator("*")
            for 已有表单项_loc in 页面上已有的表单项列表:
                包含可见表单项的loc = 包含可见表单项的loc.filter(has=已有表单项_loc)
            if 已经有唯一表单项:
                处理后的表单最上层定位 = 包含可见表单项的loc.last
            else:
                处理后的表单最上层定位 = min(包含可见表单项的loc.all(), key=lambda loc: len(loc.text_content()))

        for 表单项, 内容 in kwargs.items():
            if not 内容:
                continue
            if self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-input").count():
                self.表单_文本框填写(表单项名称=表单项, 需要填写的文本=内容, 表单最上层定位=处理后的表单最上层定位,
                                     timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-select-selector").count():
                self.表单_下拉框选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位,
                                     timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-radio-group").count():
                self.表单_radio选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位,
                                    timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).get_by_role("switch").count():
                self.表单_switch开关(表单项名称=表单项, 开关状态=内容, 表单最上层定位=处理后的表单最上层定位,
                                     timeout=timeout)
            elif self.locators.表单项中包含操作元素的最上级div(表单项).locator(".ant-picker").count():
                self.表单_日期(表单项名称=表单项, 日期=内容, 表单最上层定位=处理后的表单最上层定位, timeout=timeout)
            else:
                pytest.fail(f"不支持的快捷表单填写:\n{表单项}:{内容}")


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
        page = PageObject(page)
        # page.表单_文本框填写("会议室名称","测试会议室")
        # page.表单_下拉框选择("会议室状态","正常")
        # page.表单_下拉框选择("设备", "电视")
        # page.表单_下拉框选择("当前状态", "正常")
        # page.表单_下拉框选择("审批", "是")
        # page.表单_下拉框选择("审批", "是")
        # page.表单_级联选择器选择("管理部门","集成公司/省DICT研发中心/产品需求团队")
        # page.表单_级联选择器选择("管理人","集成公司/省DICT研发中心/产品需求团队")

        # # 单个日期
        # page.表单_日期_element("发布日期", "1825-04-05")
        #
        # # 单个日期
        # page.表单_日期_element("发布日期", "2725-04-05")

        # 日期范围
        # page.表单_日期范围选择器_左右面板联动("公开时间", "2060-07-05,2060-08-29")
        # page.表单_日期范围选择器_左右面板联动("公开时间", "")

        # page.表单_日期时间范围选择器_左右面板联动("发布日期", "2060-07-05,2060-08-29")
        # page.表单_日期时间范围选择器_左右面板联动("公开时间", "2060-07-05,2060-08-29")
        page.表单_日期时间范围选择器_左右面板联动("发布日期", "2060-07-05 02:30:59,2060-07-14 17:08:26")
        # page.表单_日期时间范围选择器_左右面板联动("发布日期", "2060-07-05 10:20:40,2060-07-14 17:08:26")

        # 单个日期 + 时间
        # page.表单_日期_element("发布日期", "2025-04-05 14:30")
        #
        #
        #
        # # 日期时间范围
        # page.表单_日期_element("发布日期", "2025-04-05 14:30,2025-04-10 18:00")

        # page.wait_for_timeout(10000)
