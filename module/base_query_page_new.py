# 数据库中的数据可能有datetime类型的，需要做处理
import binascii
import json
import re

from datetime import datetime
from urllib.parse import parse_qs

from playwright.sync_api import expect, Locator
from module.BasePageNew import PageObject
from gmssl import sm4


# 将 Hex 字符串转为 bytes
def hex2bytes(hex_str: str) -> bytes:
    return binascii.unhexlify(hex_str.encode())


# SM4 CBC 解密函数
def decrypt_sm4_cbc(encrypted_data_hex: str, key_hex: str, iv_hex: str) -> dict:
    """
    使用 SM4 CBC 模式解密 Hex 编码的密文。

    :param encrypted_data_hex: Hex 编码的加密数据
    :param key_hex: 十六进制字符串表示的密钥（16 字节）
    :param iv_hex: 十六进制字符串表示的 IV（16 字节）
    :return: 解密后的 JSON 数据（dict）
    """
    # 转换为字节
    cipher_bytes = binascii.unhexlify(encrypted_data_hex)
    key_bytes = binascii.unhexlify(key_hex)
    iv_bytes = binascii.unhexlify(iv_hex)

    # 初始化 SM4 解密器
    crypt_sm4 = sm4.CryptSM4()
    crypt_sm4.set_key(key_bytes, sm4.SM4_DECRYPT)

    # 执行 CBC 解密
    decrypted_bytes = crypt_sm4.crypt_cbc(iv_bytes, cipher_bytes)
    # decrypted_bytes = crypt_sm4.cbc_decrypt(iv_bytes, cipher_bytes)

    # 去除 PKCS5Padding 并转换为字符串
    decrypted_text = decrypted_bytes.decode('utf-8')

    # 如果是 JSON 格式数据，进一步解析
    try:
        return json.loads(decrypted_text)
    except json.JSONDecodeError:
        print("解密结果不是 JSON 格式，返回原始文本")
        return {"plaintext": decrypted_text}


"""查询页面基类，封装了查询操作相关的所有功能"""
class BaseQueryPage(PageObject):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.sm4_key = "160adbe13e74171f617436344d4b0980"
        self.sm4_iv = "00100000100000000001000000000010"

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
        return self.page.locator("(//table[@class='el-table__body'])").locator("visible=true").locator("xpath=//tbody/tr")

    def 获取表格中指定行的所有字段值(self, index) -> list:
        """ index 为行号，从1开始 """
        return self.get_table_rows().nth(index-1).locator("td").all_text_contents()[:-1]

    def get_column_values_by_name(self, column_name: str) -> list:
        # self.等待表格加载完成()
        # 等待表格加载完成并不能真正等到它加载完成，要更换
        self.page.wait_for_timeout(1000)
        """
        获取表格中当前页指定列名的所有字段值。

        :param column_name: 表格列名（完全匹配）
        :return: 指定列的所有字段值列表
        """
        # 定位表格主体
        table_body = self.page.locator("(//table[@class='el-table__body'])").locator("visible=true")

        # 获取表头行的所有列名单元格
        header_cells = self.page.locator(".el-table__header th").all()

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
        expect(self.page.locator(".el-loading-spinner").locator("visible=true")).not_to_be_visible(timeout=5000)

    def 获取页面统计的总数据量(self):
        self.等待表格加载完成()
        # self.page.locator(".el-pagination__total").wait_for()
        text = self.page.locator(".el-pagination__total").locator("visible=true").inner_text().strip()
        match = re.search(r'\d+', text)
        if match:
            number = match.group()
            # print(number)  # 输出例如 "50"
        return int(number)

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

    def 点击展开筛选(self):
        展开筛选按钮 = self.page.get_by_text("展开筛选").locator("visible=true")
        if 展开筛选按钮.is_visible():
            展开筛选按钮.click()

    def 点击收起筛选(self):
        收起筛选按钮 = self.page.get_by_text("收起筛选").locator("visible=true")
        if 收起筛选按钮.is_visible():
            收起筛选按钮.click()

    def 填写搜索框(self, kwargs:dict):
        self.快捷操作_填写表单_增加根据数据类确定唯一表单版(**kwargs)
        self.click_button("搜索")
        # 等待表格加载出来
        self.等待表格加载完成()

    def 获取表格中某行按钮(self, 关键字=None, 行号=None, 按钮名:str=None):
        if 行号:
            return self.page.locator("(//table[@class='el-table__body'])[1]/tbody//tr").nth(行号-1).locator("button",
                                                                                                           has_text=按钮名)
        elif 关键字:
            return self.page.locator("(//table[@class='el-table__body'])[1]/tbody").locator("tr",
                                                                                            has_text=关键字).first.locator(
                "button", has_text=按钮名)
        else:
            raise Exception("请输入关键字或行号")

    def 点击表格中某行按钮(self, 关键字=None, 行号=None, 按钮名:str=None):
        self.获取表格中某行按钮(关键字=关键字,行号=行号, 按钮名=按钮名).evaluate("(el) => el.click()")

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

    def 获取表格中的按钮(self, 关键字, 按钮名称:str):
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody").locator("tr",
                                                                                        has_text=关键字).first.locator(
            "button", has_text=按钮名称)

    def 点击批量删除按钮(self, 关键字, 删除数据数量):
        已勾选数据量 = 0
        for 勾选框 in self.定位器_勾选框_包含关键字(关键字).all():
            勾选框.click()
            已勾选数据量 += 1
            if 已勾选数据量 == 删除数据数量:
                break
        self.click_button("批量删除")

    def 获取查询接口响应的数据(self, 按钮名称: str, 接口路径: str):
        """
                点击查询按钮后，等待并获取查询接口的响应数据。
                接口路径如 r"/ybdsPerson/queryPersonList" 即接口完整路径的一部分
                :return: 接口返回的 JSON 数据。
                """
        # 1. 监听将要发出的请求（假设查询接口路径包含 '/page'）
        # 先监听响应，再触发请求
        with self.page.expect_request(re.compile(接口路径)) as request_info, \
                self.page.expect_response(re.compile(接口路径)) as response_info:
            self.click_button(按钮名称)  # 触发请求

        # 3. 获取请求对象
        request = request_info.value
        # print("捕获到的请求URL:", request.url)  # 打印实际发出的 URL

        response = response_info.value  # 获取响应对象
        json_data = response.json()  # 解析 JSON 响应内容

        # 判断是否需要解密
        if json_data.get("flag") == "encrypt":
            encrypted_data = json_data.get("data")
            # 这里调用你的解密函数，例如 decrypt(data)
            try:
                decrypted_data = self.decrypt(encrypted_data)
                json_data["data"] = decrypted_data  # 替换为解密后的数据
            except Exception as e:
                raise ValueError(f"解密失败: {e}")

        return json_data

    def 触发请求(self, 触发方式:str):
        if 触发方式 == "查询":
            self.click_button("查询")
        elif 触发方式 == "刷新":
            self.page.reload()

    def 获取请求的payload数据(self, 触发方式: str, 接口路径: str):
        with self.page.expect_request(re.compile(接口路径)) as request_info:
            self.触发请求(触发方式)

        request = request_info.value

        try:
            # 判断是否是 GET 请求
            if request.method.upper() == 'GET':
                print("这是一个 GET 请求")

                # 从 URL 中提取查询参数
                url = request.url
                if '?' in url:
                    query_string = url.split('?', 1)[1]  # 提取 ? 后面的部分
                    params = parse_qs(query_string)  # 解析为字典格式

                    # 将 list 类型的值转为单个字符串（如 a=1&a=2 → a=2）
                    params = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
                    return params
                else:
                    print("GET 请求没有查询参数")
                    return {}

            # 非 GET 请求：尝试获取 post_data
            post_data = request.post_data

            if post_data is None:
                print("请求没有 payload 数据")
                return {}

            # 解析 payload
            if isinstance(post_data, str):
                try:
                    payload = json.loads(post_data)
                except json.JSONDecodeError:
                    payload = parse_qs(post_data)
            elif isinstance(post_data, dict):
                payload = post_data
            else:
                payload = post_data  # 如 FormData 等类型

            # 判断是否加密（仅当 payload 是 dict 类型时才处理）
            if isinstance(payload, dict) and payload.get("flag") == "encrypt":
                encrypted_data_hex = payload.get("data")
                decrypted_data = self.decrypt(encrypted_data_hex)
                payload["data"] = decrypted_data

            return payload

        except Exception as e:
            print(f"解析请求 payload 失败: {e}")
            return {}

    def decrypt(self, encrypted_data_hex: str) -> dict:
        return decrypt_sm4_cbc(encrypted_data_hex, self.sm4_key, self.sm4_iv)

if __name__ == '__main__':
    # 示例参数（请替换为真实值）
    encrypted_data_hex = "你的加密Hex字符串"  # 替换为实际密文
    key_hex = "160adbe13e74171f617436344d4b0980"
    iv_hex = "00100000100000000001000000000010"

    try:
        result = decrypt_sm4_cbc(encrypted_data_hex, key_hex, iv_hex)
        print("解密成功:", result)
    except Exception as e:
        print("解密失败:", str(e))

