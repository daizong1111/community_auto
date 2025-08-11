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

from playwright.sync_api import expect, Page
from base_case import BaseCase
import pytest
import logging

from pages.网格管理.网格员管理 import PageGridderManage
from pages.基础信息.实有房屋.楼栋管理 import PageFloor
from pages.系统管理.用户管理 import PageUserManage

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取当前时间，精确到时分秒
current_time = datetime.now()
# 将时间转换为字符串格式
time_string = current_time.strftime("%Y-%m-%d,%H:%M:%S")


@pytest.fixture(scope="module")
def 网格员管理页面(浏览器已打开的页面):
    # 将页面封装为网格员管理页面
    page = PageGridderManage(浏览器已打开的页面)
    page.跳转到某菜单("网格管理", "网格员管理")
    yield page


用户数据_修改前 = {"用户真实姓名:": "石峰", "手机号码:": "18955491775", "关联区域": "中电数智社区"}
用户数据_修改后 = {"用户真实姓名:": "方程程", "手机号码:": "15055419272", "关联区域": "中电数智社区（测试）"}


@pytest.fixture(scope="function")
def 夹具_测试关联性(浏览器已打开的页面):
    page = PageUserManage(浏览器已打开的页面)
    page.跳转到某菜单("系统管理", "用户管理")
    # 编辑用户信息
    # 查找用户信息
    page.快捷操作_填写表单_增加根据数据类确定唯一表单版(手机号=用户数据_修改前.get("手机号码:"))
    page.click_button("搜索")
    page.等待表格加载完成()
    page.点击表格中某行按钮(行号=1, 按钮名="编辑")
    page.快捷操作_填写表单_增加根据数据类确定唯一表单版(**用户数据_修改后)
    page.click_button("确认")
    page.点击提示弹窗中的确定按钮()
    page = PageGridderManage(浏览器已打开的页面)
    page.跳转到某菜单("网格管理", "网格员管理")
    yield page
    # 将数据改回去
    page = PageUserManage(浏览器已打开的页面)
    page.跳转到某菜单("系统管理", "用户管理")
    # 编辑用户信息
    # 查找用户信息
    page.快捷操作_填写表单_增加根据数据类确定唯一表单版(手机号=用户数据_修改后.get("手机号码:"))
    page.click_button("搜索")
    page.等待表格加载完成()
    page.点击表格中某行按钮(行号=1, 按钮名="编辑")
    page.快捷操作_填写表单_增加根据数据类确定唯一表单版(**用户数据_修改前)
    page.click_button("确认")
    page.点击提示弹窗中的确定按钮()
    page = PageGridderManage(浏览器已打开的页面)
    page.跳转到某菜单("网格管理", "网格员管理")


# 定义一个模块级变量，用于标记是否新增成功
NEW_PERSON_ADDED = True


# 测试新增功能最好写个夹具去用户管理里面查一下有没有18055422739这个手机号，若是没有，用这个手机号创建一个二级网格员
@pytest.mark.usefixtures("后置操作_重置查询条件")
@pytest.mark.usefixtures("网格员管理页面")
class TestAdd(BaseCase):
    @pytest.mark.flaky(reruns=3)  # 当测试失败时，最多重试 3 次
    @pytest.mark.parametrize(
        "表单数据_新增,网格员信息",

        [
            ({"手机号": "18955491775", "网格员图片": r"C:\Users\Administrator\Pictures\111.png", "上级领导": "陶正东",
              "选择责任网格": ["测试网格1", "测试网格2"],
              },
             {"居委会": "中电数智街道/中电数智社区", "网格": "测试网格2", "姓名": "石峰", "手机号码": "18955491775"}
             )

            # 添加更多测试数据集
        ],
        # ids=["新增-成功"
        #
        #      ]
    )
    @allure.step("测试新增人员-成功")
    def test_add_success(self, 网格员管理页面,
                         表单数据_新增: dict, 网格员信息: dict
                         ):
        global NEW_PERSON_ADDED
        try:
            网格员管理页面.click_button("新增")
            self.log_step("点击新增按钮")

            网格员管理页面.填写新增或编辑表单(表单数据_新增)

            self.log_step("填写表单信息")

            网格员管理页面.click_button("保存")
            self.log_step("提交表单")

            expect(网格员管理页面.page.get_by_text("保存成功")).to_be_visible(timeout=5000)
            self.log_step("验证新增成功-页面提示信息")

            网格员管理页面.输入查询条件(手机号码=网格员信息.get("手机号码"))
            网格员管理页面.click_button("搜索")
            网格员管理页面.等待表格加载完成()
            self.log_step("查询刚才新增的数据")
            网格员姓名_密文 = 网格员信息.get("姓名")[0] + "*" * (len(网格员信息.get("姓名")) - 1)
            手机号_密文 = 网格员信息.get("手机号码")[0:3] + "****" + 网格员信息.get("手机号码")[-4:]
            loc_新增的行 = 网格员管理页面.get_table_rows().filter(has_text=网格员信息.get("居委会").split("/")[-1]).filter(
                has_text=网格员姓名_密文).filter(has_text=手机号_密文).first
            # 检查表格中是否有新增的数据
            expect(loc_新增的行).to_be_visible()

            # 标记新增成功
            NEW_PERSON_ADDED = True
        except Exception as e:
            raise e

    @allure.step("测试新增网格员-失败-使用未绑定账号的手机号")
    def test_add_fail_phone_number_without_account(self, 网格员管理页面, ):

        网格员管理页面.click_button("新增")
        self.log_step("点击新增按钮")

        网格员管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(手机号=fake.phone_number())
        网格员管理页面.click_button("检测账号")
        self.log_step("填写表单信息")

        expect(网格员管理页面.page.get_by_text("未查询到网格员账号信息")).to_be_visible()
        网格员管理页面.page.reload()


表单数据_修改后 = {"网格员图片": r"C:\Users\Administrator\Pictures\111.png", "上级领导": "金雨菲",
                   "选择责任网格": ["788", "测试网格5"],
                   }
网格员信息 = {"居委会": "中电数智街道/中电数智社区", "网格": "测试网格2", "姓名": "石峰", "手机号码": "18955491775"}


@pytest.mark.usefixtures("网格员管理页面")  # 显式声明夹具
class TestEdit(BaseCase):
    def setup_class(self):
        if not NEW_PERSON_ADDED:
            pytest.skip("新增用例执行失败，跳过修改相关测试")

    @pytest.mark.flaky(reruns=3)  # 当测试失败时，最多重试 3 次
    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "表单数据,网格员信息",

        [
            (表单数据_修改后,
             网格员信息
             )

            # 添加更多测试数据集
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试修改小区")
    def test_edit_success(self, 网格员管理页面,
                          网格员信息: dict, 表单数据: dict):
        # 输入查询条件
        网格员管理页面.输入查询条件(**网格员信息)
        网格员管理页面.click_button("搜索")
        网格员管理页面.等待表格加载完成()
        # 点击编辑按钮
        网格员管理页面.点击表格中某行按钮(行号=1, 按钮名="编辑")
        self.log_step("点击编辑按钮")
        # 填写表单信息
        网格员管理页面.填写新增或编辑表单(表单数据)
        self.log_step("填写表单信息")
        # 点击提交按钮
        网格员管理页面.click_button("保存")
        self.log_step("提交表单")
        # 点击提示弹窗中的确定按钮
        网格员管理页面.点击提示弹窗中的确定按钮()
        # 断言操作成功字样在页面出现
        expect(网格员管理页面.page.get_by_text("保存成功")).to_be_visible(timeout=5000)
        self.log_step("验证修改成功-页面提示信息")
        # 查找修改后的数据
        网格员管理页面.输入查询条件(
            **{"居委会": 网格员信息.get("居委会"), "网格": 表单数据_修改后.get("选择责任网格")[0],
               "姓名": 网格员信息.get("姓名"), "手机号码": 网格员信息.get("手机号码")})
        网格员管理页面.click_button("搜索")
        网格员管理页面.等待表格加载完成()
        # 检查表格中数据是否成功修改
        网格员管理页面.点击表格中某行按钮(行号=1, 按钮名="编辑")
        网格员管理页面.click_button("保存到下一步")
        网格员管理页面.校验表单中数据成功修改(上级领导=表单数据_修改后.get("上级领导"))
        网格员管理页面.校验选择责任网格成功修改(表单数据_修改后.get("选择责任网格"))

    # @pytest.mark.usefixtures("后置操作_刷新页面")
    # @pytest.mark.parametrize(
    #     "表单数据_搜索框, 表单数据",
    #
    #     [
    #         (
    #                 {
    #                     "商铺名称": f"修改-成功{time_string}",
    #                     # "商铺名称": "新增-成功2025-06-26,11:46:24"
    #                 },
    #                 {"商铺名称": f"彭超", "所属居委会": "中电数智街道/中电数智社区",
    #                  "所属网格": "测试网格1213",
    #                  "统一信用代码": "91440101MA5JL12345",
    #                  "负责人": "力洋", "联系方式": "18855429112", "商铺类型": "测试类型1", "商铺等级": "大型商铺",
    #                  "归属部门": "淮南市人力资源局", "入驻时间": "2025-02-13",
    #                  "具体位置": "安徽省淮南市田家庵区福海元社区103号",
    #                  "执照日期": "2000-02-10,2017-07-28",
    #                  "营业时间": "09:20:00,15:30:00",
    #                  "门头照": r"C:\Users\Administrator\Pictures\111.png"
    #                  },
    #         ),
    #     ],
    # )
    # @allure.step("测试编辑失败-去重校验：同一网格下商铺名称不能重复")
    # def test_edit_repeat_validation(self, 网格员管理页面, 表单数据_搜索框: dict,
    #                                 表单数据: dict
    #                                 ):
    #     # 输入查询条件
    #     网格员管理页面.输入查询条件(**表单数据_搜索框)
    #     网格员管理页面.click_button("搜索")
    #     网格员管理页面.等待表格加载完成()
    #     # 点击编辑按钮
    #     网格员管理页面.点击表格中某行按钮(行号=1, 按钮名="编辑")
    #     self.log_step("点击编辑按钮")
    #     # 填写表单信息
    #     网格员管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
    #         **表单数据)
    #     self.log_step("填写表单信息")
    #     # 点击提交按钮
    #     网格员管理页面.click_button("提交")
    #     网格员管理页面.点击提示弹窗中的确定按钮()
    #     self.log_step("提交表单")
    #     # 断言该人员已存在字样在页面出现
    #     网格员管理页面.验证页面顶部出现全局提示("名称已存在")
    #     self.log_step("验证编辑失败-去重校验-页面提示信息")
    #     # 刷新页面
    #     网格员管理页面.page.reload()
    #     # 填写搜索框
    #     网格员管理页面.输入查询条件(**表单数据_搜索框)
    #     网格员管理页面.click_button("搜索")
    #     网格员管理页面.等待表格加载完成()
    #     # 检查原来的数据是否没了
    #     expect(网格员管理页面.get_table_rows()).to_have_count(1)
    #     self.log_step("验证查询列表中仍然有旧的数据")


# @pytest.mark.usefixtures("网格员管理页面")  # 显式声明夹具
# class TestDetail(BaseCase):
#     @pytest.mark.usefixtures("后置操作_刷新页面")
#     @pytest.mark.parametrize(
#         "行号",
#         [
#             (1),
#         ],
#         # ids=["修改-成功"]
#     )
#     @allure.step("测试商铺详情")
#     def test_detail(self, 网格员管理页面, 行号):
#         list_某行 = 网格员管理页面.获取表格中指定行的所有字段值(行号)
#         网格员管理页面.点击表格中某行按钮(行号=行号, 按钮名="详情")
#         网格员管理页面.校验表单中数据成功修改(
#             **{"商铺名称": list_某行[2], "所属居委会": list_某行[4], "商铺类型": list_某行[3],
#                "所属网格": list_某行[5], "具体位置": list_某行[6], "负责人": list_某行[7],
#                "联系方式": list_某行[8], "入驻时间": list_某行[9]})


class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "表单数据",
        [
            {"居委会": "中电数智街道/中电数智社区"},
            {"姓名": "石岱宗"},
            {"手机号码": "18133601926"},
            {"居委会": "中电数智街道/中电数智社区", "姓名": "陶正东", "手机号码": "16656007969"},
        ]
    )
    def test_query(self, 网格员管理页面, 表单数据: dict):
        # 输入查询条件
        网格员管理页面.输入查询条件(**表单数据)
        网格员管理页面.click_button("搜索")
        网格员管理页面.等待表格加载完成()

        # 定义字段与验证逻辑的映射
        def verify_居委会():
            列表_居委会 = 网格员管理页面.get_column_values_by_name("所属社区")
            居委会_预期值 = 表单数据["居委会"].split("/")[-1]

            # 断言 列表_居委会 中的每一项都包含 居委会_预期值
            assert all(居委会_预期值 == 居委会 for 居委会 in
                       列表_居委会), f"查询条件-居委会:{居委会_预期值}, 表格中的居委会为:{列表_居委会}"

        def verify_姓名():
            列表_姓名 = 网格员管理页面.get_column_values_by_name("姓名")
            姓名_预期值 = 表单数据["姓名"][0] + "*" * (len(表单数据["姓名"]) - 1)
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                姓名_预期值 == 姓名 for 姓名 in
                列表_姓名), f"查询条件-姓名:{姓名_预期值}, 表格中的姓名为:{列表_姓名}"

        def verify_手机号码():
            列表_手机号 = 网格员管理页面.get_column_values_by_name("手机号")
            手机号_预期值 = 表单数据["手机号码"][0:3] + "****" + 表单数据["手机号码"][-4:]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                手机号_预期值 == 手机号 for 手机号 in
                列表_手机号), f"查询条件-手机号:{手机号_预期值}, 表格中的手机号为:{列表_手机号}"

        # 字典映射字段到验证函数
        验证规则 = {
            "居委会": verify_居委会,
            "姓名": verify_姓名,
            "手机号码": verify_手机号码,
        }

        # 执行匹配的验证规则
        for field in 表单数据:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")


class TestReset(BaseCase):
    def test_reset(self, 网格员管理页面):
        # 输入查询条件
        网格员管理页面.输入查询条件(
            **{"居委会": "中电数智街道/中电数智社区", "网格": "测试网格2", "姓名": "陶正东", "手机号码": "16656007969"})

        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        网格员管理页面.click_button("重置")

        网格员管理页面.校验查询条件成功修改(**{"居委会": "", "网格": "", "姓名": "", "手机号码": ""})
        # 对比页面查询到的总条数和无查询条件时查数据库的总条数
        # 数据条数_页面 = 网格员管理页面.获取页面统计的总数据量()


class TestRelevance(BaseCase):
    @allure.step("测试用户管理与网格员管理的关联性")
    def test_relevance(self, 夹具_测试关联性):
        网格员管理页面 = 夹具_测试关联性
        # 输入查询条件
        网格员管理页面.输入查询条件(手机号码=用户数据_修改后.get("手机号码:"))
        网格员管理页面.click_button("搜索")
        网格员管理页面.等待表格加载完成()
        # 点击编辑按钮
        网格员管理页面.点击表格中某行按钮(行号=1, 按钮名="编辑")
        self.log_step("点击编辑按钮")
        # 校验表单中数据
        手机号_密文 = 用户数据_修改后.get("手机号码:")[0:3] + "****" + 用户数据_修改后.get("手机号码:")[-4:]
        姓名_密文 = 用户数据_修改后.get("用户真实姓名:")[0] + "*" * (len(用户数据_修改后.get("用户真实姓名:")) - 1)
        网格员管理页面.校验表单中数据成功修改(手机号=手机号_密文, 网格员姓名=姓名_密文)
        网格员管理页面.click_button("保存到下一步")
        网格员管理页面.校验表单中数据成功修改(所属居委会=用户数据_修改后.get("关联区域"))
        # 断言：修改了关联区域后，责任网格必定没有被选中
        assert 网格员管理页面.page.locator(".el-checkbox-group .el-checkbox.is-checked").count() == 0
        # 关闭所有弹窗
        网格员管理页面.page.reload()


@pytest.mark.usefixtures("后置操作_重置查询条件")
class TestDelete(BaseCase):
    def setup_class(self):
        if not NEW_PERSON_ADDED:
            pytest.skip("新增用例执行失败，跳过删除相关测试")

    @pytest.mark.parametrize(
        "表单数据_查询",
        [
            {
                "手机号码": 网格员信息.get("手机号码")
            },
            # f"修改-成功{车牌号_修改后}"
        ]
    )
    def test_delete_success(self, 网格员管理页面, 表单数据_查询):
        # 查找待删除的记录
        # 输入查询条件
        网格员管理页面.输入查询条件(**表单数据_查询)
        网格员管理页面.click_button("搜索")
        网格员管理页面.等待表格加载完成()
        self.log_step("输入查询条件")
        删除前的数据量 = 网格员管理页面.获取页面统计的总数据量()
        # 点击删除按钮
        网格员管理页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        网格员管理页面.点击提示弹窗中的确定按钮()
        self.log_step("点击删除按钮，再点击确定按钮")
        expect(网格员管理页面.page.get_by_text("删除成功")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现删除成功字样")
        # 输入查询条件
        网格员管理页面.click_button("搜索")
        网格员管理页面.等待表格加载完成()
        删除后的数据量 = 网格员管理页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量 - 1

    @pytest.mark.parametrize("表单数据_查询", [
        {
            "手机号码": "16656007969",
        },
    ])
    def test_delete_cancel(self, 网格员管理页面, 表单数据_查询):
        # 输入查询条件
        网格员管理页面.输入查询条件(**表单数据_查询)
        网格员管理页面.click_button("搜索")
        网格员管理页面.等待表格加载完成()
        self.log_step("输入查询条件")
        删除前的数据量 = 网格员管理页面.获取页面统计的总数据量()
        # 点击删除按钮
        网格员管理页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        网格员管理页面.click_button("取消")
        self.log_step("点击删除按钮,弹窗后点击取消按钮")
        expect(网格员管理页面.page.get_by_text("删除成功")).not_to_be_visible(timeout=5000)
        self.log_step("验证页面未出现删除成功字样")
        网格员管理页面.click_button("搜索")
        # 等待1秒
        网格员管理页面.等待表格加载完成()
        删除后的数据量 = 网格员管理页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量
