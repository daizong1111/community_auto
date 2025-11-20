import os
import time

import pytest
from filelock import FileLock
from playwright.sync_api import Locator, Page, expect, sync_playwright, BrowserContext

from module.table import Table
from module.locators import Locators
from utils.my_date import *
from datetime import datetime


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


def paste_text(locator: Locator, text: str):
    """
    使用剪贴板 + 快捷键方式模拟粘贴
    :param locator: 输入框定位器
    :param text: 要粘贴的内容
    """
    page = locator.page
    # 将文本写入剪贴板
    page.evaluate(f"navigator.clipboard.writeText('{text}')")
    # 聚焦输入框
    locator.focus()
    # 执行粘贴快捷键
    if page.platform == "mac":
        locator.press("Meta+V")
    else:
        locator.press("Control+V")


class PageObject:
    def __init__(self, page: Page):
        self.page = page
        self.url = ""
        self.locators = Locators(self.page)
        # self.对话框 = self.page.locator("div[role='dialog']").locator("visible=true")
        self.对话框 = self.page.locator(".el-dialog").locator("visible=true")
        self.提示弹窗 = self.page.locator(".el-message-box").locator("visible=true")

    def 验证表单项中出现错误提示(self):
        assert self.page.locator(".el-form-item__error").count() > 0

    def 验证页面顶部出现全局提示(self, 提示语: str):
        expect(self.page.locator(".el-message__content", has_text=提示语)).to_be_visible()

    def navigate(self):
        self.page.goto(self.url)

    @property
    def table(self):
        return Table(self.page)

    def click_button(self, button_name, timeout=30_000, 按钮的父元素: Locator = None, nth=-1):
        if 按钮的父元素 is not None:
            button_loc = 按钮的父元素.locator("button")
        else:
            button_loc = self.page.locator("button")
        for 单字符 in button_name:
            button_loc = button_loc.filter(has_text=单字符)
        button_loc = button_loc.locator("visible=true")
        button_loc.nth(nth).click(timeout=timeout)

    def search(self, 搜索内容: str, placeholder=None):
        if placeholder:
            self.page.locator(
                f"//span[@class='ant-input-affix-wrapper']//input[contains(@placeholder,'{placeholder}')]").fill(
                搜索内容)
        else:
            self.page.locator(".ant-input-affix-wrapper input").fill(搜索内容)
        self.page.wait_for_load_state("networkidle")

    def hover_retry(self, hover对象: Locator, 下一步点击对象: Locator, 第一步动作="hover", 第二步动作="click", timeout=30_000):
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout / 1000:
                pytest.fail(f"hover重试{hover对象.__str__()}在{timeout / 1000}秒内未成功")
            try:
                self.page.mouse.move(x=1, y=1)
                self.page.wait_for_timeout(1_000)
                if 第一步动作 == "hover":
                    hover对象.last.hover()
                else:
                    hover对象.last.click()
                self.page.wait_for_timeout(3_000)
                if 第二步动作 == "click":
                    下一步点击对象.last.click(timeout=3000)
                else:
                    下一步点击对象.last.wait_for(state="visible", timeout=3000)
                break
            except:
                continue

    # 该函数在会议室管理系统中测试通过
    def 表单_文本框填写(self, 表单项名称: str = None, 定位器: Locator = None, 需要填写的文本: str = None,
                        表单最上层定位: Locator = None,
                        timeout: float = 8000):
        if 需要填写的文本 is None:
            return

        if 定位器:
            loc_输入框 = 定位器.locator("input,textarea").locator("visible=true").last

        elif 表单最上层定位:
            loc_输入框 = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                "input,textarea").locator("visible=true").last
        else:
            loc_输入框 = self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("input,textarea").locator(
                "visible=true").last
        # loc_输入框.fill(需要填写的文本, timeout=timeout)
        # 点击输入框
        loc_输入框.click()
        # 清空内容
        loc_输入框.clear()
        # 聚焦输入框
        loc_输入框.focus()
        # 逐字符输入内容
        loc_输入框.press_sequentially(需要填写的文本, delay=0, timeout=timeout)
        # 让元素失去焦点，必须加，否则某些输入框输入内容后会自动清空
        loc_输入框.blur()

    def 表单_下拉框选择(self, 表单项名称: str = None, 定位器: Locator = None, 需要选择的项: str = None,
                        表单最上层定位: Locator = None,
                        timeout: float = None):
        if 需要选择的项 is None:
            return

            # 根据是否传入了定位器，决定如何获取表单项
        if 定位器:
            表单项 = 定位器
        elif 表单最上层定位:
            表单项 = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator("input").locator(
                "visible=true")
        else:
            表单项 = self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("input").locator("visible=true")

        下拉箭头_下拉框 = 表单项.locator("i.el-select__caret").locator("visible=true")
        if 需要选择的项 == "":
            # 将鼠标悬停到下拉箭头_下拉框上面
            box = 下拉箭头_下拉框.first.bounding_box()
            self.page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)

            关闭按钮 = 表单项.locator(".el-icon-circle-close").locator("visible=true")
            if 关闭按钮.count() > 0:
                关闭按钮.click()
            return
        表单项.click(timeout=timeout)
        if 表单项.locator('//input[@type="search"]').count():
            表单项.locator('//input[@type="search"]').fill(需要选择的项, timeout=timeout)

        选择面板 = self.page.locator(".el-select-dropdown").locator("visible=true")
        选择面板.get_by_text(需要选择的项, exact=True).first.click(timeout=timeout)

        if 定位器:
            定位器.click()
        else:
            表单项的标签 = 表单最上层定位.locator("label", has_text=表单项名称).locator("visible=true")
            表单项的标签.click(force=True)

    def 表单_级联选择器选择(self, 表单项名称: str = None, 定位器: Locator = None, 路径: str = None,
                            表单最上层定位: Locator = None, timeout: float = None):
        """
        在 Element Plus 的级联选择器中选择指定路径的项。

        :param 表单项名称: 表单项标签名，如 "所属区域"
        :param 路径: 级联路径，如 "北京/朝阳区" 或 "一级分类/二级分类/三级分类"
        :param 表单最上层定位: 如果在弹窗或嵌套容器中，传入该容器的 Locator
        :param timeout: 操作超时时间
        """
        if 路径 is None:
            return

        分段路径 = 路径.split("/")

        if 定位器:
            表单元素 = 定位器
        elif 表单最上层定位:
            # 定位到当前表单项并点击打开级联选择器
            表单项的标签 = 表单最上层定位.locator("label", has_text=表单项名称).locator("visible=true")
            表单元素 = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                "visible=true")
        else:
            表单项的标签 = self.page.locator("label").locator("visible=true", has_text=表单项名称)
            表单元素 = self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("visible=true")

        if 路径 == "":
            表单元素.hover()
            关闭按钮 = 表单元素.locator(".el-icon-circle-close")
            if 关闭按钮.count() > 0:
                关闭按钮.click()
            return
        # 打开级联选择器
        表单元素.locator("input.el-input__inner").click(timeout=timeout)

        # 获取当前显示的级联面板
        dropdown = self.page.locator(".el-cascader__dropdown").locator("visible=true")

        length = len(分段路径)
        # 遍历分段路径中的每个节点，为每个节点找到对应的菜单项并点击
        for index, 节点 in enumerate(分段路径):
            # 定位到当前层级的菜单列表
            menu_list = dropdown.locator(f".el-cascader-menu:nth-child({index + 1}) .el-cascader-menu__list")
            # 在当前菜单列表中找到含有指定节点文本的第一个菜单项
            item_locator = menu_list.locator("li", has_text=节点).first
            # item_locator = menu_list.get_by_text(节点, exact=True).first
            # item_locator = menu_list.locator(".el-cascader-node", has_text=节点).first
            # 先尝试找 checkbox/radio
            checkbox = item_locator.locator("label").first
            if checkbox.count() > 0 and index == length - 1:
                checkbox.click(timeout=timeout)
                # checkbox.check(timeout=timeout)
            else:
                # 点击找到的菜单项，带有超时设置
                item_locator.click(timeout=timeout)
        if 定位器:
            定位器.click()
        else:
            表单项的标签.click(force=True)
        # 点击当前表单项外的其他稳定元素，如页面顶部、标题栏等，关闭选择面板，
        # self.page.locator("header").click()
        # 若选择了与之前相同的选项，面板不会关闭，需点击表单项，让它关闭
        # if dropdown.is_visible():
        #     表单元素.click()

    def 表单_树形控件(self, 表单项名称: str = None, 树容器: Locator = None, 路径: str = None,
                      表单最上层定位: Locator = None, timeout: float = 3000):
        """
        在 Element Plus 的 el-tree 控件中选择指定路径的节点，支持多选。

        :param 树容器: 定位到 el-tree 的 Locator
        :param 路径: 节点路径，如 "全选/车*__庐阳区中电数智街道中电数智社区小区*栋*"，多个路径用逗号分隔
        :param timeout: 操作超时时间
        """
        self.page.wait_for_timeout(2000)
        if 路径 is None:
            return

        if 树容器:
            pass
        elif 表单最上层定位:
            树容器 = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                ".el-tree")
        else:
            树容器 = self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("visible=true").locator(
                ".el-tree")

        # 处理多个路径的情况，支持多选
        所有路径 = [p.strip() for p in 路径.split(',') if p.strip()]

        for 单个路径 in 所有路径:
            分段路径 = 单个路径.split('/')
            current_level_nodes = 树容器.locator(">.el-tree-node").all()

            for index, 节点文本 in enumerate(分段路径):
                matched_node = None
                cnt = 0
                while True:
                    # 遍历当前层级的所有节点
                    for node in current_level_nodes:
                        node_content = node.locator(".el-tree-node__content")
                        node_label = node_content.locator("span.over").first.inner_text(timeout=timeout)
                        if node_label.strip() == 节点文本.strip():
                            matched_node = node
                            break
                    if matched_node is not None:
                        break
                    elif cnt < 10:
                        self.page.wait_for_timeout(1000)
                        cnt += 1
                    else:
                        raise Exception(f"未找到匹配的节点：{节点文本}")

                # 展开节点（如果还有下一层）
                if index < len(分段路径) - 1:
                    expand_icon = matched_node.locator(">.el-tree-node__content>.el-tree-node__expand-icon").locator(
                        "visible=true")
                    if "expanded" not in expand_icon.get_attribute("class"):
                        expand_icon.click(timeout=timeout)

                # 对于路径中的最后一个节点，点击复选框选中该节点
                if index == len(分段路径) - 1:
                    # 点击复选框选中该节点
                    checkbox = matched_node.locator(".el-checkbox__inner")
                    if checkbox.count() > 0:
                        checkbox.click(timeout=timeout)

                # 更新下一级节点列表
                current_level_nodes = matched_node.locator(">.el-tree-node__children>.el-tree-node").all()

    def 表单_日期时间选择器(self, 表单项名称: str = None, 定位器: Locator = None, 日期: str = None,
                            表单最上层定位: Locator = None, timeout: float = None):
        """
        填写基于 Element Plus 的 el-date-picker 控件的日期表单项（通过点击选择）。

        :param 表单项名称: 表单项标签名，例如 "开始时间"
        :param 日期: 日期字符串，支持如下格式：
                     - 单个日期："2025-04-05" 或 "2025-04-05 14:30"（未来打算支持这种，目前还不行）
        :param 表单最上层定位: 如果在弹窗或嵌套容器中，传入该容器的 Locator
        :param timeout: 超时时间（毫秒）
        """

        from datetime import datetime
        if 日期 is None:
            return
        if 定位器:
            date_picker = 定位器
        elif 表单最上层定位:
            date_picker = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称))
        else:
            date_picker = self.locators.表单项中包含操作元素的最上级div(表单项名称)

        if 日期 == "":
            date_picker.hover()
            关闭按钮 = date_picker.locator(".el-icon-circle-close")
            if 关闭按钮.count() > 0:
                关闭按钮.click()
                return

        # 点击打开日期选择面板
        date_picker.locator("input").first.click(timeout=timeout)

        # 获取当前显示的日期面板
        picker_panel = self.page.locator(".el-picker-panel").locator("visible=true")

        单日期 = 日期
        try:
            days_offset = int(单日期)
            格式化后的日期 = 返回当前时间xxxx_xx_xx加N天(days_offset)
        except ValueError:
            格式化后的日期 = 单日期

        # 将日期拆分为年、月、日
        dt = datetime.strptime(格式化后的日期, "%Y-%m-%d")
        year = dt.year
        month = dt.month
        day = dt.day

        # 点击年份标题进入年份选择器（如果未展开）
        picker_panel.locator(".el-date-picker__header-label", has_text="年").click(timeout=timeout)

        上一页按钮 = picker_panel.locator(".el-date-picker__prev-btn").locator("visible=true")
        下一页按钮 = picker_panel.locator(".el-date-picker__next-btn").locator("visible=true")
        当前年份区间 = picker_panel.locator(".el-date-picker__header-label", has_text="年").inner_html()
        # 当前年份区间为1990年-2020年这种格式，把两个年份拆分出来，要把年这个字去除掉
        拆开后的年份区间 = [i.replace("年", "") for i in 当前年份区间.split("-")]
        区间的开始年份 = int(拆开后的年份区间[0])
        区间的结束年份 = int(拆开后的年份区间[1])

        while year < 区间的开始年份:
            上一页按钮.click()
            当前年份区间 = picker_panel.locator(".el-date-picker__header-label", has_text="年").inner_html()
            # 当前年份区间为1990年-2020年这种格式，把两个年份拆分出来，要把年这个字去除掉
            拆开后的年份区间 = [i.replace("年", "") for i in 当前年份区间.split("-")]
            区间的开始年份 = int(拆开后的年份区间[0])
            区间的结束年份 = int(拆开后的年份区间[1])
        while year > 区间的结束年份:
            下一页按钮.click()
            当前年份区间 = picker_panel.locator(".el-date-picker__header-label", has_text="年").inner_html()
            # 当前年份区间为1990年-2020年这种格式，把两个年份拆分出来，要把年这个字去除掉
            拆开后的年份区间 = [i.replace("年", "") for i in 当前年份区间.split("-")]
            区间的开始年份 = int(拆开后的年份区间[0])
            区间的结束年份 = int(拆开后的年份区间[1])

        # 选择年份
        picker_panel.locator(".el-year-table td a", has_text=str(year)).click(timeout=timeout)

        # 选择月份
        # picker_panel.locator(".el-month-table td div a", has_text=f"{数字月份转中文(month)}月").click(timeout=timeout)
        picker_panel.locator(".el-month-table td div a").get_by_text(f"{数字月份转中文(month)}月", exact=True).click(
            timeout=timeout)

        # 选择具体日期
        picker_panel.locator(".el-date-table .available span", has_text=str(day)).first.click(timeout=timeout)

        expect(picker_panel).not_to_be_visible(timeout=timeout)

    def _select_time_in_picker(self, time_panel: Locator, time_info: dict, timeout: float = None,
                               need_click: bool = True):
        # time_panel必须是一个时间面板或者时间范围面板的半边，need_click代表是否需要点击该面板中的确定按钮
        hour_str = f"{time_info['hour']:02d}"
        minute_str = f"{time_info['minute']:02d}"
        second_str = f"{time_info['second']:02d}"

        # 选择小时
        hour_spinner = time_panel.locator(".el-time-spinner__list").nth(0).locator(".el-time-spinner__item",
                                                                                   has_text=hour_str).first
        hour_next_str = str(f"{int(hour_str) + 1:02d}")
        hour_spinner_next = time_panel.locator(".el-time-spinner__list").nth(0).locator(".el-time-spinner__item",
                                                                                        has_text=hour_next_str).first
        # 必须滚动下一个小时可见，否则点击可能失败
        hour_spinner_next.scroll_into_view_if_needed(timeout=timeout)
        hour_spinner.click(timeout=timeout)

        # 选择分钟
        minute_spinner = time_panel.locator(".el-time-spinner__list").nth(1).locator(".el-time-spinner__item",
                                                                                     has_text=minute_str).first
        minute_next_str = str(f"{int(minute_str) + 1:02d}")
        minute_spinner_next = time_panel.locator(".el-time-spinner__list").nth(1).locator(".el-time-spinner__item",
                                                                                          has_text=minute_next_str).first
        minute_spinner_next.scroll_into_view_if_needed(timeout=timeout)
        minute_spinner.click(timeout=timeout)

        # 判断是否支持秒
        if time_panel.locator(".el-time-spinner__list").count() >= 3:
            second_next_str = str(f"{int(second_str) + 1:02d}")
            second_spinner = time_panel.locator(".el-time-spinner__list").nth(2).locator(".el-time-spinner__item",
                                                                                         has_text=second_str).first
            second_spinner_next = time_panel.locator(".el-time-spinner__list").nth(2).locator(".el-time-spinner__item",
                                                                                              has_text=second_next_str).first
            second_spinner_next.scroll_into_view_if_needed(timeout=timeout)
            second_spinner.click(timeout=timeout)

        if need_click is True:
            time_panel.get_by_text("确定").click(force=True, timeout=timeout)

    def 表单_日期时间范围选择器_左右面板联动(self, 定位器: Locator = None, 表单项名称: str = None, 日期: str = None,
                                             表单最上层定位: Locator = None,
                                             timeout: float = None):
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
        if 定位器:
            date_picker = 定位器
        elif 表单最上层定位:
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

    def 表单_时间选择器(self, 定位器: Locator = None, 表单项名称: str = None, 时间: str = None,
                        表单最上层定位: Locator = None,
                        timeout: float = None):
        """
        填写基于 Element Plus 的 el-date-picker 控件的时间范围表单项（通过点击选择）。

        :param 表单项名称: 表单项标签名，例如 "开始时间"
        :param 时间: 时间字符串，支持如下格式：
                     - 范围时间： "03:02:00,05:04:00"
        :param 表单最上层定位: 如果在弹窗或嵌套容器中，传入该容器的 Locator
        :param timeout: 超时时间（毫秒）
        """
        if 时间 is None:
            return
        # 定位表单项
        if 定位器:
            表单元素 = 定位器
        elif 表单最上层定位:
            # 定位到当前表单项并点击打开选择面板
            表单元素 = 表单最上层定位.locator(self.locators.表单项中包含操作元素的最上级div(表单项名称)).locator(
                "visible=true")
        else:
            表单元素 = self.locators.表单项中包含操作元素的最上级div(表单项名称).locator("visible=true")
        # 点击叉号按钮，清空表单项
        if 时间 == "":
            表单元素.hover()
            关闭按钮 = 表单元素.locator(".el-icon-circle-close")
            if 关闭按钮.count() > 0:
                关闭按钮.click()
            return
        # 需要填写内容的处理逻辑
        列表_时间 = 时间.split(",")
        # 保存两个时间的信息
        start_time_info = None
        end_time_info = None

        for index, 单时间 in enumerate(列表_时间):
            dt = None
            formats = ["%H:%M:%S", "%H:%M", "%H"]
            for fmt in formats:
                try:
                    dt = datetime.strptime(单时间, fmt)
                    break
                except ValueError:
                    continue
            if not dt:
                raise ValueError(f"无法识别的时间格式：{单时间}")

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

        # 叫出面板
        表单元素.click()

        # 显式等待时间面板出现
        time_panel = self.page.locator(".el-time-range-picker,.el-time-picker").locator("visible=true")
        expect(time_panel).to_be_visible(timeout=timeout)

        # 注意：这里要先处理结束时间，再处理开始时间，避免该表单项已经选择了时间，且它的结束时间早于我们想要选择的开始时间
        # 如果是范围时间，并且有结束时间信息，则处理结束时间
        if len(列表_时间) > 1 and end_time_info and end_time_info["has_time_info"]:
            # 再次确认时间面板仍然可见
            expect(time_panel).to_be_visible(timeout=timeout)
            # 处理结束时间
            self._select_time_in_picker(time_panel.locator(".el-time-panel__content").nth(1), end_time_info, timeout,
                                        need_click=False)

        # 处理开始时间,此时需要点击面板中的确定按钮来提交表单
        self._select_time_in_picker(time_panel.locator(".el-time-panel__content").nth(0), start_time_info, timeout,
                                    need_click=False)

        # 等待time_panel消失
        time_panel.get_by_text("确定").click(timeout=timeout)
        expect(time_panel).to_be_hidden(timeout=timeout)

    def 表单_文件上传(self, 定位器: Locator = None, 表单项名称: str = None, 文件路径: str = None,
                      表单最上层定位: Locator = None, timeout: float = None):
        """
        在指定表单项中上传文件。

        :param 表单项名称: 表单项标签名，如 "附件"
        :param 文件路径: 要上传的文件的本地路径（绝对路径）
        :param 表单最上层定位: 如果在弹窗或嵌套容器中，传入该容器的 Locator
        :param timeout: 操作超时时间（毫秒）
        """
        if 文件路径 is None:
            return

        if 定位器:
            表单项中包含操作元素的最上级div = 定位器
        elif 表单最上层定位:
            # 注意：这个input元素不是一个可见元素，不要对其进行可见性过滤
            表单项中包含操作元素的最上级div = 表单最上层定位.locator(
                self.locators.表单项中包含操作元素的最上级div(表单项名称))
            file_input = 表单项中包含操作元素的最上级div.locator("input[type='file']").first
        else:
            表单项中包含操作元素的最上级div = self.locators.表单项中包含操作元素的最上级div(表单项名称)
            file_input = 表单项中包含操作元素的最上级div.locator("input[type='file']").first

        # 清空该表单项
        if 文件路径 == "":
            # 遍历已上传文件列表，点击所有的删除按钮
            已上传文件列表 = 表单项中包含操作元素的最上级div.locator("ul li")
            if 已上传文件列表.count() > 0:
                for 已上传文件列表项 in 已上传文件列表.all():
                    已上传文件列表项.hover()
                    关闭按钮 = 已上传文件列表项.locator(".el-icon-delete")
                    if 关闭按钮.count() > 0:
                        关闭按钮.click(timeout=timeout)
            return

        # 尝试上传文件
        try:
            print(f"开始上传文件：{文件路径}")
            file_input.set_input_files(文件路径, timeout=timeout)
            print("文件上传成功")
        except Exception as e:
            pytest.fail(f"上传失败：{str(e)}")

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

    def 快捷操作_填写表单(self, 表单最上层定位: Locator = None, timeout=None, **kwargs):
        for 表单项, 内容 in kwargs.items():
            # if not 内容:
            #     continue
            if 内容 is None:
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

    def 快捷操作_填写表单_传入定位器(self, timeout=None, kwargs: dict = {}):
        for 定位器, 内容 in kwargs.items():
            # if not 内容:
            #     continue
            if 内容 is None:
                continue
            if 定位器.locator(">.el-input, .el-textarea").count() and 定位器.locator(".el-icon-date").count() == 0:
                # if 表单项中包含操作元素的最上级div.locator(">.el-input, .el-textarea:not(.el-select):not(.el-cascader):not(.el-date-editor--date):not(.el-date-editor--datetime):not(.el-date-editor--datetimerange):not(.el-upload)").count():
                self.表单_文本框填写(定位器=定位器, 需要填写的文本=内容, timeout=8000)

            elif 定位器.locator(".el-select").count():
                self.表单_下拉框选择(定位器=定位器, 需要选择的项=内容, timeout=timeout)

            elif 定位器.locator(".el-cascader").count():
                self.表单_级联选择器选择(定位器=定位器, 路径=内容, timeout=timeout)

            # elif 表单项中包含操作元素的最上级div.locator(".ant-radio-group").count():
            #     self.表单_radio选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位,
            #                         timeout=timeout)
            elif 定位器.locator(".el-date-editor--date, .el-date-editor--datetime").count():
                self.表单_日期时间选择器(定位器=定位器, 日期=内容, timeout=timeout)

            # elif 表单项中包含操作元素的最上级div.get_by_role("switch").count():
            #     self.表单_switch开关(表单项名称=表单项, 开关状态=内容, 表单最上层定位=处理后的表单最上层定位,
            #                          timeout=timeout)
            elif 定位器.locator(".el-date-editor--datetimerange, .el-date-editor--daterange").count():
                self.表单_日期时间范围选择器_左右面板联动(定位器=定位器, 日期=内容, timeout=timeout)


            elif 定位器.locator(".el-upload").count():
                self.表单_文件上传(定位器=定位器, 文件路径=内容, timeout=timeout)

            else:
                pytest.fail(f"不支持的快捷表单填写:\n{定位器}:{内容}")

    def 快捷操作_填写表单_增加根据数据类确定唯一表单版(self, 表单最上层定位: Locator = None, timeout=None, **kwargs):
        # 该函数要添加等待，等待所有的表单加载完成
        self.page.wait_for_timeout(1000)

        # 先用try去写等待转圈出现，然后再等待转圈消失，等待转圈消失后，再等待0.5秒（也可以尝试不等0.5秒）
        # 等待查询接口已经返回数据
        # 等待加载中状态消失
        expect(self.page.locator(".el-loading-spinner").locator("visible=true")).not_to_be_visible(timeout=10000)

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

            missing_items = None
            处理后的表单最上层定位 = None
            # 遍历出所有的el-form
            # TODO: 对于传入的定位器，要做特殊处理
            for form in form_list.all():
                # 提取当前 form 中可见的文本内容
                form_text = form.text_content().strip()

                # 判断是否包含所有 kwargs 中的表单项名称
                # missing_items = [item for item in kwargs.keys() if item not in form_text]
                missing_items = [item for item in kwargs.keys() if item not in form_text and not item.startswith("loc:")]

                if not missing_items:
                    处理后的表单最上层定位 = form
                    flag = True
                    # highlight_elements(self.page, [处理后的表单最上层定位])
                    break

            if not flag:
                print(form_list.last.text_content())
                raise Exception(f"未找到包含所有指定表单项的表单，缺失字段: {', '.join(missing_items)}")

            # for index, 表单项 in enumerate(kwargs.keys()):
            #     if index == 0:
            #         # 这里尝试去找第一个表单项，一般情况下第一个表单项的文本是固定的，但不排除特殊情况，所以这里写了try，若找不到，就等一段时间
            #         try:
            #             self.locators.表单项中包含操作元素的最上级div(表单项).last.wait_for(timeout=timeout)
            #         except:
            #             pass
            #
            #     if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 0:
            #         print(f"表单项:{表单项}的最上级div未找到")
            #         # 查看是否找到，没找到，则跳过，找下一个
            #         continue
            #     else:
            #         if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 1:
            #             已经有唯一表单项 = True
            #         页面上已有的表单项列表.append(self.locators.表单项中包含操作元素的最上级div(表单项))
            #     if 已经有唯一表单项 and len(页面上已有的表单项列表) >= 2:
            #         # 这里只要找到一个唯一的表单项，并且页面上已经有2个表单项，通过这两个表单项的共同祖先便可以唯一确定表单最上层定位了，所以，可以退出循环
            #         break
            #
            # 包含可见表单项的loc = self.page.locator("*")
            # # =====================================================================
            # for 已有表单项_loc in 页面上已有的表单项列表:
            #     包含可见表单项的loc = 包含可见表单项的loc.filter(has=已有表单项_loc)
            #
            # if 已经有唯一表单项:
            #     处理后的表单最上层定位 = 包含可见表单项的loc.last
            # else:
            #     # 从多个候选的表单容器中，选择一个“最紧凑”的定位器（即文本内容最少的那个）作为最终操作的目标表单容器。
            #     处理后的表单最上层定位 = min(包含可见表单项的loc.all(), key=lambda loc: len(loc.text_content()))
            #     for loc in 包含可见表单项的loc.all():
            #         loc.highlight()
            #         print(loc.text_content())

        for 表单项, 内容 in kwargs.items():
            flag_定位器 = False
            # 该函数要能处理2种类型的输入：表单项名称和定位器
            if 表单项.startswith("loc:"):
                表单项中包含操作元素的最上级div = self.page.locator(表单项[4:]).locator("visible=true")
                flag_定位器 = True

            else:
                表单项中包含操作元素的最上级div = self.locators.表单项中包含操作元素的最上级div(表单项,处理后的表单最上层定位)


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
                if flag_定位器:
                    self.表单_文本框填写(定位器=表单项中包含操作元素的最上级div, 需要填写的文本=内容, 表单最上层定位=处理后的表单最上层定位,
                                         timeout=8000)
                else:
                    self.表单_文本框填写(表单项名称=表单项, 需要填写的文本=内容, 表单最上层定位=处理后的表单最上层定位,
                                         timeout=8000)
            elif 表单项中包含操作元素的最上级div.locator(".el-select").count():
                if flag_定位器:
                    self.表单_下拉框选择(定位器=表单项中包含操作元素的最上级div, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位,
                                         timeout=timeout)
                else:
                    self.表单_下拉框选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位,
                                         timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-cascader").count():
                if flag_定位器:
                    self.表单_级联选择器选择(定位器=表单项中包含操作元素的最上级div, 路径=内容, 表单最上层定位=处理后的表单最上层定位,
                                             timeout=timeout)
                else:
                    self.表单_级联选择器选择(表单项名称=表单项, 路径=内容, 表单最上层定位=处理后的表单最上层定位,
                                             timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-tree").count():
                if flag_定位器:
                    self.表单_树形控件(树容器=表单项中包含操作元素的最上级div, 路径=内容, 表单最上层定位=处理后的表单最上层定位, timeout=timeout)
                else:
                    self.表单_树形控件(表单项名称=表单项, 路径=内容, 表单最上层定位=处理后的表单最上层定位, timeout=timeout)
            # elif 表单项中包含操作元素的最上级div.locator(".ant-radio-group").count():
            #     self.表单_radio选择(表单项名称=表单项, 需要选择的项=内容, 表单最上层定位=处理后的表单最上层定位,
            #                         timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-date-editor--date, .el-date-editor--datetime").count():
                if flag_定位器 == True:
                    self.表单_日期时间选择器(定位器=表单项中包含操作元素的最上级div, 日期=内容, 表单最上层定位=处理后的表单最上层定位,
                                             timeout=timeout)
                else:
                    self.表单_日期时间选择器(表单项名称=表单项, 日期=内容, 表单最上层定位=处理后的表单最上层定位,
                                         timeout=timeout)
            # elif 表单项中包含操作元素的最上级div.get_by_role("switch").count():
            #     self.表单_switch开关(表单项名称=表单项, 开关状态=内容, 表单最上层定位=处理后的表单最上层定位,
            #                          timeout=timeout)
            elif 表单项中包含操作元素的最上级div.locator(".el-date-editor--timerange, .el-date-editor--time").count():
                if flag_定位器 == True:
                    self.表单_时间选择器(定位器=表单项中包含操作元素的最上级div, 时间=内容, 表单最上层定位=处理后的表单最上层定位,
                                     timeout=timeout)
                else:
                    self.表单_时间选择器(表单项名称=表单项, 时间=内容, 表单最上层定位=处理后的表单最上层定位,
                                     timeout=timeout)

            elif 表单项中包含操作元素的最上级div.locator(
                    ".el-date-editor--daterange,.el-date-editor--datetimerange").count():
                if flag_定位器 == True:
                    self.表单_日期时间范围选择器_左右面板联动(定位器=表单项中包含操作元素的最上级div, 日期=内容,
                                                              表单最上层定位=处理后的表单最上层定位,
                                                              timeout=timeout)
                else:
                    self.表单_日期时间范围选择器_左右面板联动(表单项名称=表单项, 日期=内容,
                                                              表单最上层定位=处理后的表单最上层定位,
                                                              timeout=timeout)

            elif 表单项中包含操作元素的最上级div.locator(".el-upload").count():
                if flag_定位器:
                    self.表单_文件上传(定位器=表单项中包含操作元素的最上级div, 文件路径=内容, 表单最上层定位=处理后的表单最上层定位,
                                   timeout=timeout)
                else:
                    self.表单_文件上传(表单项名称=表单项, 文件路径=内容, 表单最上层定位=处理后的表单最上层定位,
                                   timeout=timeout)
            else:
                pytest.fail(f"不支持的快捷表单填写:\n{表单项}:{内容}")

    def 校验表单中数据成功修改(self, 表单最上层定位: Locator = None, timeout=None, **kwargs):
        # 强制等待，避免内容未更新
        # self.page.wait_for_timeout(3000)
        # 等待加载中状态消失
        # expect(self.page.locator(".el-loading-spinner").locator("visible=true")).not_to_be_visible(timeout=10000)
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
                # 获取所有的表单项
                # 遍历所有的表单项
                for item in kwargs.keys():
                    # 获取表单项的文本
                    if form.filter(has_text=item).count():
                        continue
                    else:
                        break
                else:
                    flag = True
                    处理后的表单最上层定位 = form
                    # highlight_elements(self.page, [处理后的表单最上层定位])
                    break

            if not flag:
                raise Exception("未找到包含所有指定表单项的表单")

            # for index, 表单项 in enumerate(kwargs.keys()):
            #     if index == 0:
            #         # 这里尝试去找第一个表单项，一般情况下第一个表单项的文本是固定的，但不排除特殊情况，所以这里写了try，若找不到，就等一段时间
            #         try:
            #             self.locators.表单项中包含操作元素的最上级div(表单项).last.wait_for(timeout=timeout)
            #         except:
            #             pass
            #
            #     if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 0:
            #         # 查看是否找到，没找到，则跳过，找下一个
            #         continue
            #     else:
            #         if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 1:
            #             已经有唯一表单项 = True
            #         页面上已有的表单项列表.append(self.locators.表单项中包含操作元素的最上级div(表单项))
            #     if 已经有唯一表单项 and len(页面上已有的表单项列表) >= 2:
            #         # 这里只要找到一个唯一的表单项，并且页面上已经有2个表单项，通过这两个表单项的共同祖先便可以唯一确定表单最上层定位了，所以，可以退出循环
            #         break
            #
            # 包含可见表单项的loc = self.page.locator("*")
            # for 已有表单项_loc in 页面上已有的表单项列表:
            #     包含可见表单项的loc = 包含可见表单项的loc.filter(has=已有表单项_loc)
            # if 已经有唯一表单项:
            #     处理后的表单最上层定位 = 包含可见表单项的loc.last
            # else:
            #     # 从多个候选的表单容器中，选择一个“最紧凑”的定位器（即文本内容最少的那个）作为最终操作的目标表单容器。
            #     处理后的表单最上层定位 = min(包含可见表单项的loc.all(), key=lambda loc: len(loc.text_content()))
            #     # for loc in 包含可见表单项的loc.all():
            #     #     loc.highlight()
            #     #     print(loc.text_content())

        for 表单项, 内容 in kwargs.items():
            if 内容 is None:
                continue
            表单项中包含操作元素的最上级div = self.locators.表单项中包含操作元素的最上级div(表单项, 处理后的表单最上层定位)

            assert 表单项中包含操作元素的最上级div.count() > 0, f"表单项: {表单项} 的最上级div未找到"
            loc_表单项 = 表单项中包含操作元素的最上级div.locator('input,textarea')
            # 内容_表单项 = 表单项中包含操作元素的最上级div.locator('input,textarea').input_value()

            # 统一格式：去除两边空格，并将 " / " 替换为 "/"，再与预期值对比
            # 内容_表单项_标准化 = 内容_表单项.replace(" / ", "/").strip()
            预期内容_标准化 = str(内容).strip().replace(" / ", "/")
            # assert 内容_表单项_标准化 in 预期内容_标准化, \
            #     f"表单项{表单项}填写内容不一致，实际内容：{内容_表单项}，预期内容：{内容}"
            expect(loc_表单项).to_have_value(预期内容_标准化)

    def 校验表单中数据成功修改_传入定位器(self, kwargs: dict, timeout=None):
        # 强制等待，避免内容未更新
        self.page.wait_for_timeout(3000)
        for 定位器, 内容 in kwargs.items():
            # if not 内容:
            #     continue
            if 内容 is None:
                continue
            表单项中包含操作元素的最上级div = 定位器
            assert 表单项中包含操作元素的最上级div.count() > 0, f"{定位器} 未找到"
            内容_表单项 = 表单项中包含操作元素的最上级div.locator('input,textarea').input_value()

            # 统一格式：去除两边空格，并将 " / " 替换为 "/"，再与预期值对比
            内容_表单项_标准化 = 内容_表单项.replace(" / ", "/").strip()
            预期内容_标准化 = str(内容).strip().replace(" / ", "/")
            # print(内容_表单项)
            assert 内容_表单项_标准化 in 预期内容_标准化, \
                f"定位器{定位器}填写内容不一致，实际内容：{内容_表单项}，预期内容：{内容}"

    def 关闭抽屉(self):
        self.page.mouse.click(x=10,y=10)
        self.click_button("确定")

    # 这段代码不要直接调用，让子类重写
    def 校验表单中项目时间成功修改(self, 开始日期: str, 结束日期: str):
        项目开始时间_表单项内容 = self.locators.表单项中包含操作元素的最上级div("项目时间").locator(
            "xpath=//input[@placeholder='开始日期']").input_value()
        项目结束时间_表单项内容 = self.locators.表单项中包含操作元素的最上级div("项目时间").locator(
            "xpath=//input[@placeholder='结束日期']").input_value()
        # print(项目开始时间_表单项内容, 项目结束时间_表单项内容)
        assert 项目开始时间_表单项内容 == 开始日期 and 项目结束时间_表单项内容 == 结束日期, f"项目时间修改失败,项目开始时间_表单项内容:{项目开始时间_表单项内容},项目结束时间_表单项内容:{项目结束时间_表单项内容}"

    def 点击提示弹窗中的确定按钮(self):
        self.提示弹窗.locator("button", has_text="确定").click()

    def 跳转到某菜单(self, 顶部菜单名称: str = None, 左侧菜单路径: str = None):
        """"左侧菜单路径如 小区信息/房屋管理 """
        if 顶部菜单名称 is not None:
            顶部菜单按钮 = self.page.locator('.meunBtn').get_by_text(顶部菜单名称, exact=True)
            顶部菜单按钮.click()
        for idx, 菜单名称 in enumerate(左侧菜单路径.split("/")):
            菜单名称 = self.page.get_by_role("menuitem").get_by_text(菜单名称)
            if idx == 0:
                menuitem = 菜单名称.locator("xpath=./ancestor::*[@role='menuitem']")
                # 若menuitem的class属性中不包含is-opened，则点击菜单名称
                if "is-opened" not in menuitem.get_attribute("class"):
                    菜单名称.click()
            else:
                菜单名称.click()

        # 等待页面加载完成
        # self.page.wait_for_load_state('load')
        self.page.wait_for_timeout(1000)

    def 获取详情页中的数据(self, loc_表单项最上层: Locator = None) -> dict:
        """只能提取有label的input中的数据"""
        res = {}
        if loc_表单项最上层 is not None:
            # 等待页面加载完成
            expect(loc_表单项最上层).to_be_visible()
            # 遍历所有的input元素
            for loc_input in loc_表单项最上层.locator("input").all():
                # 判断它是否有label，若没有label，则跳过
                loc_label = loc_input.locator(
                    "xpath=//ancestor::div[@class='el-form-item__content']//preceding-sibling::label[position()=1]")
                if loc_label.count() == 0:
                    continue
                key = loc_input.locator(
                    "xpath=//ancestor::div[@class='el-form-item__content']//preceding-sibling::label[position()=1]").inner_text()
                # 有bug，可能存在多个input元素对应同一个label的情况，这样的话，会导致value被覆盖。
                # 日期范围中有两个input元素，它们对应同一个label，会导致值被覆盖
                value = loc_input.input_value()
                res[key] = value

        else:
            for loc_input in self.page.locator("input").all():
                key = loc_input.locator(
                    "xpath=//ancestor::div[@class='el-form-item__content']//preceding-sibling::label[position()=1]").inner_text()
                value = loc_input.input_value()
                res[key] = value

        return res

def 使用new_context登录并返回实例化的page(new_context, 用户别名):
    from module.PageInstance import PageIns
    from utils.globalMap import GlobalMap
    from data_module.auth_Data import MyData
    from utils.GetPath import get_path
    global_map = GlobalMap()
    被测环境 = global_map.get("env")
    用户名 = MyData().userinfo(被测环境,用户别名)["username"]
    密码 = MyData().userinfo(被测环境,用户别名)["password"]

    with FileLock(get_path(f".temp/{被测环境}-{用户别名}.lock")):
        if os.path.exists(get_path(f".temp/{被测环境}-{用户别名}.json")):
            context: BrowserContext = new_context(storage_state=get_path(f".temp/{被测环境}-{用户别名}.json"))
            page = context.new_page()
            my_page = PageIns(page)
            my_page.page.goto("/homeIndex")
            # 等待输入框_用户名出现或基础信息出现
            expect(my_page.登录页.输入框_用户名.or_(my_page.登录页.基础信息)).to_be_visible()
            if my_page.登录页.输入框_用户名.count() or my_page.登录页.提示语_该令牌已过期.count():
                my_page.登录页.登录(用户名,密码,'202208')
                my_page.page.context.storage_state(path=get_path(f".temp/{被测环境}-{用户别名}.json"))
        else:
            context: BrowserContext = new_context()
            page = context.new_page()
            my_page = PageIns(page)
            my_page.登录页.登录(用户名,密码,'202208')
            my_page.page.context.storage_state(path=get_path(f".temp/{被测环境}-{用户别名}.json"))
    return my_page

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


