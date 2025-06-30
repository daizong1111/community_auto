"""
此模块使用 Playwright 框架实现会议室管理模块的 UI 自动化测试，
包含增、删、改、查功能的测试用例。
"""
import random
from datetime import datetime

import allure

# 生成随机身份证号码和手机号码，防止数据重复
from faker import Faker

fake = Faker('zh_CN')

from playwright.sync_api import expect
from base_case import BaseCase
import pytest
import logging

from pages.基础信息.场所管理.删除申请审批 import PageDeleteApproval

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取当前时间，精确到时分秒
current_time = datetime.now()
# 将时间转换为字符串格式
time_string = current_time.strftime("%Y-%m-%d,%H:%M:%S")


@pytest.fixture(scope="module")
def 删除申请审批页面(浏览器已打开的页面):
    # 将页面封装为删除申请审批页面
    page = PageDeleteApproval(浏览器已打开的页面)
    yield page


# 定义一个模块级变量，用于标记是否新增成功
NEW_PERSON_ADDED = False


class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "表单数据_标签,表单数据_定位器",
        [
            ({"选择居委会": "中电数智街道/中电数智社区"}, {"所属网格": "测试网格1213"}),
            ({"请筛选申请时间段": "2025-03-02 03:20:51,2025-07-14 08:32:21"}, {}),
            ({"审批状态": "审批通过"}, {}),
            ({"选择居委会": "中电数智街道/中电数智社区", "请筛选申请时间段": "2025-03-02 03:20:51,2025-07-14 08:32:21",
              "审批状态": "审批通过"}, {"所属网格": "测试网格1213"}),

        ]
    )
    def test_query(self, 删除申请审批页面, 表单数据_标签: dict, 表单数据_定位器: dict):
        # 输入查询条件
        删除申请审批页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_标签)
        删除申请审批页面.填写表单项_传入定位器(**表单数据_定位器)
        删除申请审批页面.click_button("搜索")

        # 定义字段与验证逻辑的映射
        def verify_所属网格():
            列表_所属网格 = 删除申请审批页面.get_column_values_by_name("所属网格")
            所属网格_预期值 = 表单数据_定位器["所属网格"]

            # 断言 列表_所属网格 中的每一项都包含 所属网格_预期值
            assert all(所属网格_预期值 == 所属网格 for 所属网格 in
                       列表_所属网格), f"查询条件-所属网格:{所属网格_预期值}, 表格中的所属网格为:{列表_所属网格}"

        def verify_申请时间段():
            # 获取输入的申请时间段，并拆分为开始和结束时间
            申请时间段_预期值 = 表单数据_标签["请筛选申请时间段"]
            列表_开始和结束时间_预期值 = 申请时间段_预期值.split(",")
            申请时间_开始_预期 = 列表_开始和结束时间_预期值[0]
            申请时间_结束_预期 = 列表_开始和结束时间_预期值[1]
            # 定义日期格式，假设时间为 "YYYY-MM-DD HH:MM:SS" 格式
            date_format = "%Y-%m-%d %H:%M:%S"
            dt_开始 = datetime.strptime(申请时间_开始_预期, date_format)
            dt_结束 = datetime.strptime(申请时间_结束_预期, date_format)

            列表_申请时间 = 删除申请审批页面.get_column_values_by_name("申请时间")

            # 验证每一条申请时间是否在预期的时间段内
            for 申请时间 in 列表_申请时间:
                # 将字符串转换为 datetime 对象进行比较
                dt_申请时间 = datetime.strptime(申请时间, date_format)
                # 断言：申请时间必须在 [开始时间, 结束时间] 范围内
                assert dt_开始 <= dt_申请时间 <= dt_结束, \
                    f"实际申请时间 {申请时间} 不在查询时间段 [{申请时间_开始_预期}, {申请时间_结束_预期}] 内"

        def verify_审批状态():
            列表_审批状态 = 删除申请审批页面.get_column_values_by_name("审批状态")
            审批状态_预期值 = 表单数据_标签["审批状态"].replace("批", "核")
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                审批状态_预期值 == 审批状态 for 审批状态 in
                列表_审批状态), f"查询条件-审批状态:{审批状态_预期值}, 表格中的审批状态为:{列表_审批状态}"

        # 字典映射字段到验证函数
        验证规则 = {
            "所属网格": verify_所属网格,
            "请筛选申请时间段": verify_申请时间段,
            "审批状态": verify_审批状态,

        }

        # 执行匹配的验证规则
        for field in 表单数据_标签:
            if field in 验证规则:
                验证规则[field]()
        for field in 表单数据_定位器:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")


class TestReset(BaseCase):
    def test_reset(self, 删除申请审批页面):
        # 输入查询条件
        删除申请审批页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            **{"选择居委会": "中电数智街道/中电数智社区", "请筛选申请时间段": "2025-03-02 03:20:51,2025-07-14 08:32:21",
               "审批状态": "审批通过"})
        删除申请审批页面.填写表单项_传入定位器(**{"所属网格": "测试网格1213"})
        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        删除申请审批页面.click_button("重置")

        删除申请审批页面.校验表单中数据成功修改(**{"选择居委会": "", "审批状态": ""})
        删除申请审批页面.校验表单中数据成功修改_申请时间段(开始时间_预期值="", 结束时间_预期值="")
        删除申请审批页面.校验表单中数据成功修改_传入定位器(kwargs={删除申请审批页面.输入框_网格: ""})


@pytest.mark.usefixtures("删除申请审批页面")  # 显式声明夹具
class TestDetail(BaseCase):
    @pytest.mark.parametrize(
        "行号",
        [
            (1),(2),(3),(4),(5),(6),(7),(8),
            (9),
            (10)
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试删除申请审批详情")
    def test_detail(self, 删除申请审批页面, 行号):
        list_某行 = 删除申请审批页面.获取表格中指定行的所有字段值(行号)
        self.log_step("获取表格中某行的数据")
        删除申请审批页面.点击表格中某行按钮(行号=行号, 按钮名="查看")
        self.log_step("点击表格中某行的查看按钮")
        删除申请审批页面.校验详情页中内容({"所属网格": list_某行[1], "场所名称": list_某行[2],
               "场所类型": list_某行[3], "具体位置": list_某行[4], "申请人": list_某行[5],
               "申请时间": list_某行[6], "申请事由": list_某行[7], "审批状态": list_某行[8],
               })
        self.log_step("校验详情页中内容")
        删除申请审批页面.click_button("关闭")
        self.log_step("关闭详情页")

@pytest.mark.usefixtures("删除申请审批页面")
class TestApprove(BaseCase):
    @allure.step("测试删除申请审批通过")
    def test_pass(self, 删除申请审批页面):
        删除申请审批页面.点击表格中第i个审批按钮(1)
        删除申请审批页面.提交审批表单(True)
        expect(删除申请审批页面.page.get_by_text("提交成功")).to_be_visible()


    @pytest.mark.parametrize("不通过原因", [
        "测试删除申请审批不通过",
        # "无理由不通过",
        # "半年亏损一个亿",

    ])
    @allure.step("测试删除申请审批不通过")
    def test_not_pass(self, 删除申请审批页面, 不通过原因: str):
        删除申请审批页面.点击表格中第i个审批按钮(1)
        删除申请审批页面.提交审批表单(False, 不通过原因)
        expect(删除申请审批页面.page.get_by_text("提交成功")).to_be_visible()
