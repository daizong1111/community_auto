"""
此模块使用 Playwright 框架实现会议室管理模块的 UI 自动化测试，
包含增、删、改、查功能的测试用例。
"""
import random
from datetime import datetime

import allure

# 生成随机身份证号码和手机号码，防止数据重复
from faker import Faker

from pages.pages_h5.上报物业 import PageReportProperty
from pages.pages_h5.个人中心 import PagePersonalCenter
from pages.pages_h5.首页 import PageHome

fake = Faker('zh_CN')

from playwright.sync_api import expect
from base_case import BaseCase
import pytest
import logging

from pages.网格管理.事件管理 import PageIncidentManage

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取当前时间，精确到时分秒
current_time = datetime.now()
# 将时间转换为字符串格式
time_string = current_time.strftime("%Y-%m-%d,%H:%M:%S")


# @pytest.fixture(scope="module")
# def 事件管理页面(logged_in_page):
#     # 将页面封装为事件管理页面
#     page = PageIncidentManage(logged_in_page)
#     page.跳转到某菜单('网格管理', "事件管理")
#     yield page

@pytest.fixture(scope="module")
def 事件管理页面(浏览器已打开的页面):
    # 将页面封装为事件管理页面
    page = PageIncidentManage(浏览器已打开的页面)
    page.跳转到某菜单('网格管理', "事件管理")
    yield page


@pytest.fixture(scope="function")
def 后置操作_重置查询条件(事件管理页面) -> None:
    logs = []
    try:
        # logs.append("日志数据0000000000000")

        yield
        事件管理页面.click_button("重置", 按钮的父元素=事件管理页面.page.locator(".query-form").first)
        # logs.append("日志数据22222222222222222")
        事件管理页面.click_button("重置", 按钮的父元素=事件管理页面.page.locator(".query-form").nth(1))
        # logs.append("日志数据33333333333333333")
    finally:
        allure.attach("\n".join(logs), name="夹具日志")


@allure.step("关闭详情页")
@pytest.fixture(scope="function")
def 后置操作_关闭详情页(事件管理页面):
    yield
    事件管理页面.page.mouse.click(x=10, y=10)
    allure.attach("点击屏幕上的 (10, 10) 坐标来关闭详情页", name="操作描述")


# 定义一个模块级变量，用于标记是否新增成功
NEW_PERSON_ADDED = False


class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "搜索框数据_图表, 搜索框数据_表格",
        [
            # ({"loc:(//form[contains(@class,'query-form')]//input[@placeholder='请选择社区']//ancestor::div[@class='el-form-item__content'])[2]": "中电数智社区"},
            #  {}),
            # ({"loc://form[contains(@class,'query-form')]//input[@placeholder='请选择小区']//ancestor::div[@class='el-form-item__content']": "测试商圈"},
            #  {}),
            # ({"loc://form[contains(@class,'query-form')]//input[@placeholder='发起日期']//ancestor::div[@class='el-form-item__content']": "2024-07-01,2025-07-01"},
            #  {}),
            # ({},
            #  {"loc://form[contains(@class,'query-form')]//input[@placeholder='请选择事件类型']//ancestor::div[@class='el-form-item__content']": "建议"}),
            # ({},
            #  {"loc://form[contains(@class,'query-form')]//input[@placeholder='请选择处理状态']//ancestor::div[@class='el-form-item__content']": "待处理"}),
            # ({},
            #  {"loc://form[contains(@class,'query-form')]//input[@placeholder='请输入上报人']//ancestor::div[@class='el-form-item__content']": "杨"}),
            # ({},
            #  {"loc://form[contains(@class,'query-form')]//input[@placeholder='请输入当前处理人']//ancestor::div[@class='el-form-item__content']": "金雨菲"}),
            ({PageIncidentManage.输入框_社区: "中电数智社区", PageIncidentManage.输入框_小区: "测试商圈", PageIncidentManage.输入框_日期: "2024-07-01,2025-07-01"},
             {PageIncidentManage.输入框_事件类型: "建议", PageIncidentManage.输入框_处理状态: "待处理", PageIncidentManage.输入框_上报人: "杨", PageIncidentManage.输入框_处理人: "金雨菲"})

        ]
    )
    def test_query(self, 事件管理页面, 搜索框数据_图表: dict, 搜索框数据_表格: dict):
        # 输入查询条件
        # 事件管理页面.填写表单项_传入定位器(**搜索框数据_图表)
        事件管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**搜索框数据_图表)
        事件管理页面.click_button("搜索", 按钮的父元素=事件管理页面.page.locator(".query-form").first)
        事件管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**搜索框数据_表格)
        事件管理页面.click_button("搜索", 按钮的父元素=事件管理页面.page.locator(".query-form").nth(1))

        # 定义字段与验证逻辑的映射
        def verify_社区():
            列表_社区 = 事件管理页面.get_column_values_by_name("社区")
            社区_预期值 = 搜索框数据_图表["社区"]

            # 断言 列表_社区 中的每一项都包含 社区_预期值
            assert all(社区_预期值 == 社区 for 社区 in
                       列表_社区), f"查询条件-社区:{社区_预期值}, 表格中的社区为:{列表_社区}"

        def verify_小区():
            列表_小区 = 事件管理页面.get_column_values_by_name("小区")
            小区_预期值 = 搜索框数据_图表["小区"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                小区_预期值 == 小区 for 小区 in
                列表_小区), f"查询条件-小区:{小区_预期值}, 表格中的小区为:{列表_小区}"

        def verify_日期():
            # 获取输入的申请时间段，并拆分为开始和结束日期
            申请时间段_预期值 = 搜索框数据_图表["日期"]
            列表_开始和结束时间_预期值 = 申请时间段_预期值.split(",")
            申请日期_开始_预期 = 列表_开始和结束时间_预期值[0]
            申请日期_结束_预期 = 列表_开始和结束时间_预期值[1]

            # 设置默认时间范围：开始时间为当天 00:00:00，结束时间为当天 23:59:59
            date_format_date = "%Y-%m-%d"
            dt_开始 = datetime.strptime(申请日期_开始_预期, date_format_date)
            dt_结束 = datetime.strptime(申请日期_结束_预期, date_format_date).replace(hour=23, minute=59, second=59)

            列表_申请时间 = 事件管理页面.get_column_values_by_name("报事时间")

            # 验证每一条申请时间是否在预期的时间段内
            for 申请时间 in 列表_申请时间:
                # 将字符串转换为 datetime 对象进行比较
                dt_申请时间 = datetime.strptime(申请时间, "%Y-%m-%d %H:%M:%S")
                # 断言：申请时间必须在 [开始时间, 结束时间] 范围内
                assert dt_开始 <= dt_申请时间 <= dt_结束, \
                    f"实际申请时间 {申请时间} 不在查询时间段 [{dt_开始}, {dt_结束}] 内"

        def verify_事件类型():
            事件类型_预期值 = 搜索框数据_表格["事件类型"]
            列表_事件类型 = 事件管理页面.get_column_values_by_name("分类")

            # 断言 列表_事件类型 中的每一项都包含 事件类型_预期值
            assert all(事件类型_预期值 in 事件类型 for 事件类型 in
                       列表_事件类型), f"查询条件-事件类型:{事件类型_预期值}, 表格中的事件类型为:{列表_事件类型}"

        def verify_处理状态():
            处理状态_预期值 = 搜索框数据_表格["处理状态"]
            列表_处理状态 = 事件管理页面.get_column_values_by_name("状态")

            # 断言 列表_处理状态 中的每一项都包含 处理状态_预期值
            assert all(处理状态_预期值 == 处理状态 for 处理状态 in
                       列表_处理状态), f"查询条件-处理状态:{处理状态_预期值}, 表格中的处理状态为:{列表_处理状态}"

        def verify_上报人():
            上报人_预期值 = 搜索框数据_表格["上报人"]
            上报人_预期值 = 上报人_预期值[0] + "*" * (len(上报人_预期值) - 1)
            列表_上报人 = 事件管理页面.get_column_values_by_name("报事人")

            # 断言 列表_上报人 中的每一项都包含 上报人_预期值
            assert all(上报人_预期值 in 上报人 for 上报人 in
                       列表_上报人), f"查询条件-上报人:{上报人_预期值}, 表格中的上报人为:{列表_上报人}"

        def verify_处理人():
            处理人_预期值 = 搜索框数据_表格["处理人"]
            列表_处理人 = 事件管理页面.get_column_values_by_name("当前处理人")

            # 断言 列表_处理人 中的每一项都包含 处理人_预期值
            assert all(处理人_预期值 in 处理人 for 处理人 in
                       列表_处理人), f"查询条件-处理人:{处理人_预期值}, 表格中的处理人为:{列表_处理人}"

        # 字典映射字段到验证函数
        验证规则 = {
            "社区": verify_社区,
            "小区": verify_小区,
            "日期": verify_日期,
            "事件类型": verify_事件类型,
            "处理状态": verify_处理状态,
            "上报人": verify_上报人,
            "处理人": verify_处理人,

        }

        # 执行匹配的验证规则
        for field in 搜索框数据_图表:
            if field in 验证规则:
                验证规则[field]()
        for field in 搜索框数据_表格:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")


class TestReset(BaseCase):
    def test_reset(self, 事件管理页面):
        # 输入查询条件
        事件管理页面.填写表单项_传入定位器(
            **{"社区": "中电数智社区", "小区": "测试商圈", "日期": "2024-07-01,2025-07-01"})
        事件管理页面.填写表单项_传入定位器(
            **{"事件类型": "建议", "处理状态": "待处理", "上报人": "杨", "处理人": "金雨菲"})

        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        事件管理页面.click_button("重置", 按钮的父元素=事件管理页面.page.locator(".query-form").first)
        事件管理页面.click_button("重置", 按钮的父元素=事件管理页面.page.locator(".query-form").nth(1))

        事件管理页面.校验定位器中数据成功修改(
            **{"社区": "", "小区": "", "事件类型": "", "处理状态": "", "上报人": "", "处理人": ""})
        事件管理页面.校验表单中数据成功修改_申请时间段(**{"开始时间_预期值": "", "结束时间_预期值": ""})


@pytest.mark.usefixtures("事件管理页面")
@pytest.mark.usefixtures("后置操作_关闭详情页")  # 显式声明夹具
class TestDetail(BaseCase):
    @pytest.mark.parametrize(
        "行号",
        [
            # (1),(2),(3),(4),(5),(6),(7),(8),
            (9),
            (10)
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试事件管理页面详情")
    def test_detail(self, 事件管理页面, 行号):
        list_某行 = 事件管理页面.获取表格中指定行的所有字段值(行号)
        self.log_step("获取表格中某行的数据")
        事件管理页面.点击表格中某行按钮(行号=行号, 按钮名="详情")
        self.log_step("点击表格中某行的详情按钮")
        事件管理页面.校验表单中数据成功修改(**{"分类": list_某行[5], "社区": list_某行[3],
                                               "小区": list_某行[4], "发起时间": list_某行[8],
                                               "状态": list_某行[9], "当前处理级别": list_某行[10]
                                               })



