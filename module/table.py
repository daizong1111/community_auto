import random
import re
from typing import Union

from playwright.sync_api import Locator, Page, sync_playwright, expect
from module import *


class Table:
    def __init__(self, page: Page, 表格序号: int = 0):
        """
        默认找页面上的第一个可见的表格
        """
        self.page = page
        self.page.wait_for_load_state("networkidle")
        # self.table_div = self.page.locator(".ant-table-wrapper").filter(has_text=唯一文字).nth(表格序号)
        self.table_div = self.page.locator(".el-table").locator("visible=true").nth(表格序号)
        # 有些场景下，表格可能有多个tbody，这里只取第一个
        self.table_body = self.table_div.locator("tbody").first
        self.table_header_tr = self.table_div.locator("thead").first.locator("tr")

    def get_header_index(self, 表头文字: str) -> int:
        return self.table_header_tr.locator("th").all_text_contents().index(表头文字)

    def get_row_locator(self, 行元素定位: Locator) -> Locator:
        return self.table_body.locator("tr").filter(has=行元素定位)

    def get_cell(self, 表头文字or列序号: Union[str, int], 行元素定位or行序号or行文字: Union[Locator, int, str]) -> Locator:
        if isinstance(表头文字or列序号, str):
            列序号 = self.get_header_index(表头文字or列序号)
        else:
            列序号 = 表头文字or列序号

        if isinstance(行元素定位or行序号or行文字, Locator):
            行定位 = self.get_row_locator(行元素定位or行序号or行文字)
        elif isinstance(行元素定位or行序号or行文字, str):
            # 行定位 = self.table_div.locator("tr").filter(has_text=行元素定位or行序号or行文字)
            行定位 = self.table_body.locator("tr").filter(has_text=行元素定位or行序号or行文字)
        else:
            # 行定位 = self.table_div.locator("tbody").locator('//tr[not(@aria-hidden="true")]').nth(行元素定位or行序号or行文字)
            行定位 = self.table_body.locator('//tr[not(@aria-hidden="true")]').nth(行元素定位or行序号or行文字)

        return 行定位.locator("td").nth(列序号)

    def get_row_dict(self, 行元素定位or行序号: Union[Locator, int] = "random") -> dict:
        if isinstance(行元素定位or行序号, int):
            tr = self.table_body.locator("tr").locator("visible=true").nth(行元素定位or行序号)
        elif isinstance(行元素定位or行序号, Locator):
            tr = self.table_body.locator("tr").filter(has=行元素定位or行序号)
        else:
            all_tr = self.table_body.locator("tr").locator("visible=ture").all()
            tr = random.choice(all_tr)

        td_text_list = tr.locator("td").all_text_contents()
        header_text_list = self.table_header_tr.locator("th").all_text_contents()
        row_dict = dict(zip(header_text_list, td_text_list))
        return row_dict

    def get_col_list(self, 表头文字: str) -> list:
        index = self.get_header_index(表头文字)
        all_tr = self.table_body.locator("tr").locator("visible=true").all()
        col_list = []
        for tr in all_tr:
            col_list.append(tr.locator("td").nth(index).text_content())
        return col_list

    def get_first_page_button(self):
        # 首页按钮
        return self.page.locator("//ul[@class='el-pager']/li[text()='1']")

    def get_some_page_button(self, page_number):
        # 某个页码按钮
        return self.page.locator(".el-pager li").get_by_text(str(page_number), exact=True)

    def get_next_button(self):
        # 下一页按钮
        return self.page.locator('.btn-next')

    def click_next_button(self):
        # 若下一页按钮可用，则点击下一页按钮
        if self.get_next_button().is_visible():
            self.get_next_button().click()

    def get_table_rows(self):
        # 定位表格中的所有行
        return self.page.locator("(//table[@class='el-table__body'])").locator("visible=true").first.locator("xpath=//tbody/tr")

        # return self.page.locator("//table[@class='el-table__body']//tbody").locator("visible=true").first.locator("tr")

    # def 获取表格中指定行的所有字段值(self, index) -> list:
    #     """ index 为行号，从1开始 """
    #     return self.get_table_rows().nth(index-1).locator("td").all_text_contents()[:-1]

    def get_column_values_by_name(self, column_name: str) -> list:
        # 把表格里面所有数据提取出来
        table_body = self.page.locator("(//table[@class='el-table__body'])").locator("visible=true").first

        # 根据查的字段去找一下是表格里面的第几列
        # ;locator('//table//tr')/all_inner_texts()  ===>  [‘aaaa,aaa,322,22’，‘111,222,33,444,55’]
        # 根据idx遍历每一行，从每一行中拿到想要的列的数据
        # self.等待表格加载完成()

        # 等待表格加载完成并不能真正等到它加载完成，要更换
        self.page.wait_for_timeout(1000)
        """
        获取表格中当前页指定列名的所有字段值。
        :param column_name: 表格列名（完全匹配）
        :return: 指定列的所有字段值列表
        """
        # 定位表格主体
        table_body = self.page.locator("(//table[@class='el-table__body'])").locator("visible=true").first

        # 获取表头行的所有列名单元格
        header_cells = self.page.locator(".el-table__header").locator("visible=true").first.locator("th").all()

        # 查找目标列的索引
        column_index = -1
        for idx, cell in enumerate(header_cells):
            # print(cell.inner_text())
            if cell.inner_text().strip() == column_name:
                column_index = idx
                break

        assert column_index != -1, f"未找到列名为 '{column_name}' 的列"

        # 获取所有数据行
        rows = table_body.locator("tbody > tr").all()

        # 提取每行对应列的数据
        column_values = []

        for row in rows:
            cell_value = row.locator(f"td:nth-child({column_index + 1})").inner_text().strip()
            column_values.append(cell_value)
        # 去重
        # column_values = list(set(column_values))

        return column_values

    def 等待表格加载完成(self):
        self.page.wait_for_timeout(1000)
        expect(self.page.locator(".el-loading-spinner").locator("visible=true")).not_to_be_visible(timeout=10000)

    def 获取页面统计的总数据量(self):
        self.等待表格加载完成()
        # self.page.locator(".el-pagination__total").wait_for()
        text = self.page.locator(".el-pagination__total").locator("visible=true").inner_text().strip()
        match = re.search(r'\d+', text)
        if match:
            number = match.group()
            # print(number)  # 输出例如 "50"
        return int(number)

    def extract_table_data(self):
        """从当前页开始，抽取表格中的数据到列表中"""
        # 用于存放所有页面中的表格数据
        data = []
        # 统计所有页的行数
        total_rows_count = 0
        # 统计当前页码
        page = 1
        while True:
            # 此处，使用列表推导式进行了优化，避免使用双重for循环
            rows = self.get_table_rows().all()
            # 遍历所有行，将每一行的数据添加到列表中
            data.extend([row.locator("td").all_text_contents()[:-1] for row in rows])
            total_rows_count += len(rows)
            # 若下一页按钮可用，则点击下一页按钮
            if self.get_next_button().is_enabled():
                # 点击下一页按钮
                self.click_next_button()
                page += 1
                # 等待选择的页码按钮有个被选中的样式，该方式不行
                # expect(self.get_some_page_button(page)).to_have_class(re.compile(r'\bactive\b'),timeout=2000)
                try:
                    # 等待下一页按钮可用，可用代表表格中元素已经加载完成
                    self.等待表格加载完成()
                    # expect(self.get_next_button()).to_be_enabled(timeout=1000)
                except Exception as e:
                    continue
            else:
                # 退出循环
                break

        # while True:
        #     # 此处，使用列表推导式进行了优化，避免使用双重for循环
        #     rows = self.get_table_rows().all()
        #     # 遍历所有行，将每一行的数据添加到列表中
        #     data.extend([row.locator("td").all_text_contents()[:-1] for row in rows])
        #     total_rows_count += len(rows)
        #     # 若下一页按钮可用，则点击下一页按钮
        #     self.click_next_button()
        #     try:
        #         expect(self.get_next_button()).to_be_enabled(timeout=2000)
        #     except:
        #         break

        return data, total_rows_count

    def get_table_data(self):
        """获取所有页的表格中的数据"""
        # 处理查询结果列表为空的情况
        if self._is_table_empty():
            return [], 0
        # 将当前页置为第一页
        self.get_first_page_button().click()
        # # 强制等待一秒，使表格内容更新，待后续优化为显示等待
        # 等待表格内容刷新完毕
        # 等待页面加载完毕
        self.等待表格加载完成()
        # self.page.wait_for_timeout(1000)
        # 遍历所有的页，提取表格中的数据到列表中
        return self.extract_table_data()

    def _is_table_empty(self):
        # 判断表格是否为空
        return self.get_first_page_button().count() == 0

    def 获取表格中某行按钮(self, 关键字=None, 行号=None, 按钮名:str=None):
        if 行号:
            return self.get_table_rows().nth(行号-1).locator("button",has_text=按钮名)
        elif 关键字:
            return self.get_table_rows().filter(has_text=关键字).first.locator("button", has_text=按钮名)

        else:
            raise Exception("请输入关键字或行号")

    def 点击表格中某行按钮(self, loc_行:Locator=None,关键字=None, 行号=None, 按钮名:str=None):
        if loc_行 is not None:
            loc_行.locator("button", has_text=按钮名).evaluate("(el) => el.click()")
        else:
            self.获取表格中某行按钮(关键字=关键字,行号=行号, 按钮名=按钮名).evaluate("(el) => el.click()")

    def loc_表格中每列内容完全等于筛选条件的行(self, 匹配条件:dict):
        # res = self.get_table_rows()
        #
        # for key, value in 匹配条件.items():
        #     idx = self.根据列名获取索引(key)
        #     res = res.filter(has=self.get_table_rows().get_by_text(value,exact=True))
        #     if res is None:
        #         raise Exception(f"没有找到匹配的行，请检查筛选条件是否正确")
        # return res

        # 获取表格所有行
        rows = self.get_table_rows()

        for column_name, expected_value in 匹配条件.items():
            # 获取当前列的索引
            idx = self.根据列名获取索引(column_name)

            # 筛选出该列值精确等于 expected_value 的行
            # rows = rows.filter(
            #     has=rows.locator(f"td:nth-child({idx + 1})").get_by_text(expected_value, exact=True)
            # )

            rows = rows.filter(has=self.page.get_by_text(expected_value,exact=True))
            # 如果中间某一步没有匹配结果，提前结束
            if not rows.count():
                raise Exception(f"未找到满足条件的行：{column_name} = {expected_value}")
        return rows

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
        table = Table(page)
        table.get_header_index("社区")
        table.get_row_locator(page.get_by_text("丁燃测试商品")).highlight()
        table.get_cell("社区", page.get_by_text("测试网格1213")).highlight()
        table.get_cell("社区", 3).highlight()
        dict = table.get_row_dict(page.get_by_text("修改-成功2025-06-30,16:18:10"))
        list = table.get_col_list("名称")
        page.wait_for_timeout(10000)

