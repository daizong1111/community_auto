"""
此模块使用 Playwright 框架实现会议室管理模块的 UI 自动化测试，
包含增、删、改、查功能的测试用例。
"""
import random
import time

import allure

from playwright.sync_api import expect
from base_case import BaseCase
import pytest
import logging

from pages.基础信息.实有人口.特殊人群 import PageSpecialPeople
from pages.基础信息.实有人口.人口信息 import PagePeopleInfo

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

随机号码 = str(random.randint(1, 9999))
随机号码_修改后 = str(int(随机号码) + 1)


@pytest.fixture(scope="module")
def 特殊人群页面(浏览器已打开的页面):
    # 将页面封装为特殊人群页面
    page = PageSpecialPeople(浏览器已打开的页面)
    yield page

@pytest.mark.usefixtures("特殊人群页面")  # 显式声明夹具
class TestEdit(BaseCase):
    @pytest.mark.parametrize(
        "待修改的姓名, 表单数据",
        [
            (
                    "谢路",  # 待修改的姓名
                    {  # 表单数据
                        "人口标签": ["异常人群", "孤寡老人"],
                    }
            ),
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试修改小区")
    def test_edit_success(self, 特殊人群页面,
                          db_connection, 待修改的姓名, 表单数据: dict):
        # 输入查询条件
        特殊人群页面.填写搜索框({"姓名": 待修改的姓名})
        # 点击编辑按钮
        特殊人群页面.点击编辑按钮(None)
        self.log_step("点击编辑按钮")
        # 填写表单信息
        特殊人群页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            **表单数据)
        self.log_step("填写表单信息")
        # 点击提交按钮
        特殊人群页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 点击提示弹窗中的确定按钮
        特殊人群页面.点击提示弹窗中的确定按钮()
        # 断言操作成功字样在页面出现
        expect(特殊人群页面.page.get_by_text("修改成功")).to_be_visible(timeout=5000)
        self.log_step("验证修改成功-页面提示信息")
        特殊人群页面.填写搜索框({"姓名": 表单数据.get("姓名")})
        # 等待1秒
        特殊人群页面.page.wait_for_timeout(1000)
        # 检查表格中数据是否成功修改
        特殊人群页面.点击编辑按钮(None)
        特殊人群页面.检查人口标签是否修改成功(表单数据.get("人口标签"))
        特殊人群页面.page.reload()
        特殊人群页面.跳转到某菜单("实有人口/人口信息")
        人口信息页面 = PagePeopleInfo(特殊人群页面.page)
        人口信息页面.填写搜索框({"姓名": 待修改的姓名})
        # 断言该人员的信息已修改
        expect(人口信息页面.get_table_rows().get_by_text(",".join(表单数据["人口标签"]))).to_be_visible()
        人口信息页面.跳转到某菜单("实有人口/特殊人群")


def contains_any(list_a, list_b):
    """
    判断 list_a 是否包含 list_b 中的任意一个元素。

    :param list_a: 被检查的列表
    :param list_b: 包含目标元素的列表
    :return: True/False
    """
    return any(item in list_a for item in list_b)


class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "表单数据",
        [
            {"选择小区": "中电数智街道/中电数智社区/小区99"},
            {"人员标签": ["现役军人", "高危人群", "孤寡老人"]},
            {"姓名": "谢路"},
            {"手机号码": "15655426823"},
            {"选择小区": "中电数智街道/中电数智社区/小区99", "人员标签": ["现役军人", "高危人群", "孤寡老人"],
             "姓名": "黄嘉鹏", "手机号码": "15655426823"},

        ]
    )
    def test_query(self, 特殊人群页面, 表单数据: dict):
        # 展开搜索条件
        特殊人群页面.点击展开筛选()
        # 输入查询条件
        特殊人群页面.填写搜索框(表单数据)

        # 定义字段与验证逻辑的映射
        def verify_小区名称():
            列表_小区名称 = 特殊人群页面.get_column_values_by_name("小区名称")
            小区名称_预期值 = 表单数据["选择小区"].split("/")[-1]

            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(小区名称_预期值 in 小区名称 for 小区名称 in
                       列表_小区名称), f"查询条件-小区名称:{小区名称_预期值}, 表格中的小区名称为:{列表_小区名称}"

        def verify_人员标签():
            列表_人口标签 = 特殊人群页面.get_column_values_by_name("人口标签")
            人员标签_预期值 = 表单数据["人员标签"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(contains_any(人员标签_预期值, 人口标签.split(",")) for 人口标签 in
                       列表_人口标签), f"查询条件-人口标签:{人员标签_预期值}, 表格中的人口标签为:{列表_人口标签}"

        def verify_姓名():
            列表_姓名 = 特殊人群页面.get_column_values_by_name("姓名")
            姓名_预期值 = 表单数据["姓名"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(姓名_预期值[0] == 姓名[0] for 姓名 in
                       列表_姓名), f"查询条件-姓名:{姓名_预期值}, 表格中的姓名为:{列表_姓名}"

        def verify_手机号码():
            列表_手机号码 = 特殊人群页面.get_column_values_by_name("联系电话")
            手机号码_预期值 = 表单数据["手机号码"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(手机号码_预期值[0:3] == 手机号码[0:3] and 手机号码_预期值[-4:] == 手机号码[-4:] for 手机号码 in
                       列表_手机号码), f"查询条件-手机号码:{手机号码_预期值}, 表格中的人员类型为:{列表_手机号码}"

        # 字典映射字段到验证函数
        验证规则 = {
            "选择小区": verify_小区名称,
            "姓名": verify_姓名,
            "人员标签": verify_人员标签,
            "手机号码": verify_手机号码,
        }

        # 执行匹配的验证规则
        for field in 表单数据:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")


class TestReset(BaseCase):
    def test_reset(self, 特殊人群页面):
        # 输入查询条件
        特殊人群页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(选择小区="中电数智街道/中电数智社区/小区99",
                                                                    人员标签=["现役军人", "高危人群", "孤寡老人"],
                                                                    姓名="谢路", 手机号码="15655426823")
        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        特殊人群页面.click_button("重置")

        特殊人群页面.校验表单中数据成功修改(选择小区="", 人员标签="", 手机号码="")
