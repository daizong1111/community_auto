# 数据库中的数据可能有datetime类型的，需要做处理
from abc import abstractmethod
from datetime import datetime
from playwright.sync_api import expect

"""查询页面基类，封装了查询操作相关的所有功能"""
class BaseQueryPage:
    def __init__(self, page):
        self.page = page

    @abstractmethod
    def get_first_page_button(self):
        # 首页按钮
        pass

    @abstractmethod
    def get_next_button(self):
        # 下一页按钮
        pass

    def click_next_button(self):
        # 若下一页按钮可用，则点击下一页按钮
        if self.get_next_button().is_visible():
            self.get_next_button().click()
            # 等待表格更新，但是这段代码在1.40.0的playwright中似乎不支持
            expect(self.get_table_rows()).to_have_count(count_gt=0)


    @abstractmethod
    def get_table_rows(self):
        # 定位表格中的所有行
        pass

    def extract_table_data(self):
        """从当前页开始，抽取表格中的数据到列表中"""
        # 用于存放所有页面中的表格数据
        data = []
        # 统计所有页的行数
        total_rows_count = 0

        while True:
            # 此处，使用列表推导式进行了优化，避免使用双重for循环
            rows = self.get_table_rows().all()
            # 遍历所有行，将每一行的数据添加到列表中
            data.extend([row.locator("td").all_text_contents()[:-1] for row in rows])
            total_rows_count += len(rows)
            # 若下一页按钮可用，则点击下一页按钮
            if self.get_next_button().is_enabled():
                self.click_next_button()
                # 等待1秒，让表格内容刷新
                self.page.wait_for_timeout(1000)
            else:
                # 退出循环
                break

        return data, total_rows_count

    def get_table_data(self):
        """获取所有页的表格中的数据"""
        # 处理查询结果列表为空的情况
        if self._is_table_empty():
            return [], 0
        # 将当前页置为第一页
        self.get_first_page_button().click()
        # 强制等待一秒，使表格内容更新
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
        with connection.cursor(dictionary=True) as cursor:
            try:
                cursor.execute(query, params)  # 使用参数化查询
                db_data = cursor.fetchall() # 获取查询结果
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





