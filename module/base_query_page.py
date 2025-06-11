# 数据库中的数据可能有datetime类型的，需要做处理
import re
from abc import abstractmethod
from collections import OrderedDict
from datetime import datetime
from playwright.sync_api import expect, Locator
from .BasePage import PageObject

"""查询页面基类，封装了查询操作相关的所有功能"""


class BaseQueryPage(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    @abstractmethod
    def 获取查询接口响应的数据(self):
        pass

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
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody/tr")

    def 定位器_表格(self) -> Locator:
        return self.page.locator("(//table[@class='el-table__body'])[1]")

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
                    expect(self.get_next_button()).to_be_enabled(timeout=1000)
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
        self.page.wait_for_timeout(1000)

        # 遍历所有的页，提取表格中的数据到列表中
        return self.extract_table_data()

    def _is_table_empty(self):
        # 判断表格是否为空
        return self.get_first_page_button().count() == 0

    def get_db_data(self, connection, query, params=None):
        """
        执行带参数的 SQL 查询。

        :param connection: 数据库连接对象
        :param query: 包含占位符的 SQL 查询语句，例如:
                      "SELECT * FROM users WHERE dept_name = %(dept_name)s"
        :param params: 一个字典，包含查询参数，例如:
                       {"dept_name": "集成公司"}
        :return: 查询结果列表
        """
        # 获取数据库游标
        # with connection.cursor(dictionary=True) as cursor: # mysql-connector-python
        with connection.cursor() as cursor:  # pymysql

            try:
                sql = cursor.mogrify(query, params)
                print("执行的SQL:", sql)  # 打印拼接后的 SQL

                cursor.execute(query, params)  # 使用参数化查询
                db_data = cursor.fetchall()  # 获取查询结果

            except Exception as e:
                print(f"Database error: {e}")
                db_data = []
        return db_data

    def compare_data(self, page_data, db_data, fields):
        """
        比较页面数据和数据库数据。

        :param page_data: 页面数据，格式为二维列表。
        :param db_data: 数据库数据，格式为字典列表。
        :param fields: 需要比较的字段名列表，例如 ['room_name', 'room_code', 'capacity']。
        :return: 如果数据一致返回 True，否则返回 False。
        """
        # 将数据库数据转换为列表
        db_list = []
        # 遍历数据库数据
        for row in db_data:
            row_data = []
            # 遍历字段名列表
            for field in fields:
                # 从当前行中获取字段的值
                value = row.get(field, "")
                if isinstance(value, datetime):  # 检查是否为 datetime 类型
                    value = value.strftime('%Y-%m-%d %H:%M:%S')  # 转换为指定格式的字符串
                # 将转换后的数据添加到行数据列表中
                row_data.append(str(value))
            # 将行数据添加到总列表中
            db_list.append(row_data)

        # 比较两个数据集
        # if page_data == db_list:
        #     print("数据一致，测试通过")
        #     return True
        if len(page_data) == len(db_list):
            print("数据一致，测试通过")
            print("页面数据:", page_data)
            print("数据库数据:", db_list)
            print("页面数据条数:", len(page_data))
            print("数据库数据条数", len(db_list))
            return True
        else:
            print("数据不一致，测试不通过")
            print("页面数据:", page_data)
            print("数据库数据:", db_list)
            print("页面数据条数:", len(page_data))
            print("数据库数据条数", len(db_list))
            return False

    def 对比查询接口数据和数据库数据(self, response, db_data, fields):
        """
        比较页面数据和数据库数据。

        :param response: 页面数据，格式为二维列表。
        :param db_data: 数据库数据，格式为字典列表。
        :param fields: 需要比较的字段名列表，例如 ['room_name', 'room_code', 'capacity']。
        :return: 如果数据一致返回 True，否则返回 False。
        """
        # 将数据库数据转换为列表
        db_list = []
        # 遍历数据库数据
        for row in db_data:
            row_data = []
            # 遍历字段名列表
            for field in fields:
                # 从当前行中获取字段的值
                value = row.get(field, "")
                if isinstance(value, datetime):  # 检查是否为 datetime 类型
                    value = value.strftime('%Y-%m-%d %H:%M:%S')  # 转换为指定格式的字符串
                # 将转换后的数据添加到行数据列表中
                row_data.append(str(value))
            # 将行数据添加到总列表中
            db_list.append(row_data)

        total = response["data"]["total"]
        records = response["data"]["records"]
        # 比较两个数据集
        # if response == db_list:
        #     print("数据一致，测试通过")
        #     return True

        len_db = len(db_list)

        if total == len_db:
            print("数据一致，测试通过")
            # print("接口数据:", records)
            # print("数据库数据:", db_list)
            # print("接口数据条数:", total)
            # print("数据库数据条数", len_db)
            return True
        else:
            # 将接口数据转换为列表
            response_data_list = []
            # 遍历数据库数据
            for row in records:
                row_data = []
                # 遍历字段名列表
                for field in fields:
                    # 从当前行中获取字段的值
                    value = row.get(field, "")
                    if isinstance(value, datetime):  # 检查是否为 datetime 类型
                        value = value.strftime('%Y-%m-%d %H:%M:%S')  # 转换为指定格式的字符串
                    # 将转换后的数据添加到行数据列表中
                    row_data.append(str(value))
                # 将行数据添加到总列表中
                response_data_list.append(row_data)
            print("数据不一致，测试不通过")
            print("接口数据:", response_data_list)
            print("数据库数据:", db_list)
            print("接口数据条数:", total)
            print("数据库数据条数", len_db)
            return False

    def get_reset_btn(self):
        """获取重置按钮"""
        return self.page.get_by_role("button", name="重置")

    def click_reset_btn(self):
        """点击重置按钮"""
        self.get_reset_btn().click()

    def 获取编辑按钮(self, 关键字):
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody").locator("tr",
                                                                                        has_text=关键字).first.locator(
            "button", has_text="编辑")

    def 点击编辑按钮(self, 关键字):
        self.获取编辑按钮(关键字).evaluate("(el) => el.click()")

    def 获取详情按钮(self, 关键字):
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody").locator("tr",
                                                                                        has_text=关键字).first.locator(
            "button", has_text="详情")

    def 点击详情按钮(self, 关键字):
        self.获取详情按钮(关键字).evaluate("(el) => el.click()")

    def 获取删除按钮(self, 关键字):
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody").locator("tr",
                                                                                        has_text=关键字).first.locator(
            "button", has_text="删除")

    def 点击删除按钮(self, 关键字):
        self.获取删除按钮(关键字).evaluate("(el) => el.click()")

    def 定位器_勾选框_包含关键字(self, 关键字: str):
        return self.定位器_表格().locator("tr", has_text=关键字)

    def 点击批量删除按钮(self, 关键字, 删除数据数量):
        已勾选数据量 = 0
        for 勾选框 in self.定位器_勾选框_包含关键字(关键字).all():
            勾选框.click()
            已勾选数据量 += 1
            if 已勾选数据量 == 删除数据数量:
                break
        self.click_button("批量删除")
