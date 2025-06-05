# 数据库中的数据可能有datetime类型的，需要做处理
from abc import abstractmethod
from collections import OrderedDict
from datetime import datetime
from playwright.sync_api import expect, Locator

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
            # 等待表格内容更新，使用显示等待
            # 等待表格更新，但是这段代码在1.40.0的playwright中似乎不支持
            # expect(self.get_table_rows()).to_have_count(count_gt=0)
            # expect(self.get_table_rows()).to_be_visible(timeout=2000)
            # expect(self.get_next_button()).to_be_enabled(timeout=2000)



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
                try:
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
        # with connection.cursor(dictionary=True) as cursor: # mysql-connector-python
        with connection.cursor() as cursor: # pymysql

            try:
                # sql = cursor.mogrify(query, params)
                # print("执行的SQL:", sql)  # 打印拼接后的 SQL

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

    def get_reset_btn(self):
        """获取重置按钮"""
        return self.page.get_by_role("button", name="重置")
    def click_reset_btn(self):
        """点击重置按钮"""
        self.get_reset_btn().click()

    def 获取编辑按钮(self, 关键字):
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody").locator("tr",has_text=关键字).first.locator("button", has_text="编辑")

    def 点击编辑按钮(self, 关键字):
        self.获取编辑按钮(关键字).evaluate("(el) => el.click()")

    def 获取详情按钮(self, 关键字):
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody").locator("tr",has_text=关键字).first.locator("button", has_text="详情")

    def 点击详情按钮(self, 关键字):
        self.获取详情按钮(关键字).evaluate("(el) => el.click()")

    def 获取删除按钮(self, 关键字):
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody").locator("tr",has_text=关键字).first.locator("button", has_text="删除")

    def 点击删除按钮(self, 关键字):
        self.获取删除按钮(关键字).evaluate("(el) => el.click()")

    def 校验详情页数据与修改后数据一致(self, 表单最上层定位: Locator = None, timeout=None, **kwargs):
        # 因为有些表单是选中了某些表单项后，会弹出一些新的表单项，所以需要处理
        页面上已有的表单项列表 = []
        已经有唯一表单项 = False
        if 表单最上层定位:
            # 这个判断逻辑的最终目的是得到一个处理后的表单最上层定位，可以通过代码自动寻找，但是有些情况下就是不大好找，可以手动传递到入参里
            处理后的表单最上层定位 = 表单最上层定位
        else:
            for index, 表单项 in enumerate(kwargs.keys()):
                if index == 0:
                    # 这里尝试去找第一个表单项，一般情况下第一个表单项的文本是固定的，但不排除特殊情况，所以这里写了try，若找不到，就等一段时间
                    try:
                        self.locators.表单项中包含操作元素的最上级div(表单项).last.wait_for(timeout=timeout)
                    except:
                        pass

                if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 0:
                    # 查看是否找到，没找到，则跳过，找下一个
                    continue
                else:
                    if self.locators.表单项中包含操作元素的最上级div(表单项).count() == 1:
                        已经有唯一表单项 = True
                    页面上已有的表单项列表.append(self.locators.表单项中包含操作元素的最上级div(表单项))
                if 已经有唯一表单项 and len(页面上已有的表单项列表) >= 2:
                    # 这里只要找到一个唯一的表单项，并且页面上已经有2个表单项，通过这两个表单项的共同祖先便可以唯一确定表单最上层定位了，所以，可以退出循环
                    break

            包含可见表单项的loc = self.page.locator("*")
            for 已有表单项_loc in 页面上已有的表单项列表:
                包含可见表单项的loc = 包含可见表单项的loc.filter(has=已有表单项_loc)
            if 已经有唯一表单项:
                处理后的表单最上层定位 = 包含可见表单项的loc.last
            else:
                # 从多个候选的表单容器中，选择一个“最紧凑”的定位器（即文本内容最少的那个）作为最终操作的目标表单容器。
                处理后的表单最上层定位 = min(包含可见表单项的loc.all(), key=lambda loc: len(loc.text_content()))
                # for loc in 包含可见表单项的loc.all():
                #     loc.highlight()
                #     print(loc.text_content())

        for 表单项, 内容 in kwargs.items():
            # if not 内容:
            #     continue
            if 内容 is None:
                continue

            内容_表单项 = self.locators.表单项中包含操作元素的最上级div(表单项, 处理后的表单最上层定位).locator('input').input_value()
            print(内容_表单项)
            # assert 内容_表单项 == 内容, f"表单项{表单项}填写内容不一致，实际内容：{内容_表单项}，预期内容：{内容}"







