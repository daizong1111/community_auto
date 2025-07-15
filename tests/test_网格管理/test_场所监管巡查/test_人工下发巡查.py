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

from pages.网格管理.场所监管巡查.人工下发巡查 import PageManualInspection
from pages.基础信息.场所管理.场所信息.商铺信息 import PageStoreInfo

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

number = str(random.randint(1, 10000000))


@pytest.fixture(scope="module")
def 人工下发巡查页面(浏览器已打开的页面):
    # 将页面封装为人工下发巡查页面
    page = PageManualInspection(浏览器已打开的页面)
    page.跳转到某菜单("网格管理", "场所监管巡查/人工下发巡查")
    yield page

列表_被访商铺 = []
字符串_任务负责人 = None
@pytest.fixture(scope="class")
def 夹具_测试走访明细页面(人工下发巡查页面):
    global 字符串_任务负责人
    人工下发巡查页面.输入查询条件(项目名称="111")
    人工下发巡查页面.click_button("搜索")
    人工下发巡查页面.等待表格加载完成()
    # 从详情页中取出被访商铺列表，保存起来
    字符串_任务负责人 = 人工下发巡查页面.get_table_rows().first.locator("td").nth(8).inner_text().strip()
    人工下发巡查页面.点击表格中某行按钮(行号=1, 按钮名="详情")
    人工下发巡查页面.获取被访商铺列表(列表_被访商铺)
    人工下发巡查页面.关闭抽屉()

    人工下发巡查页面.点击表格中某行按钮(行号=1, 按钮名="走访明细")
    人工下发巡查页面.等待表格加载完成()
    yield 人工下发巡查页面
    人工下发巡查页面.click_button("返回")


# 定义一个模块级变量，用于标记是否新增成功
NEW_PERSON_ADDED = False

@pytest.mark.usefixtures("后置操作_重置查询条件")
@pytest.mark.usefixtures("人工下发巡查页面")
class TestAdd(BaseCase):
    @pytest.mark.parametrize(
        "表单数据",

        [
            {"走访项目": f"新增-成功{number}", "所属社区": r"中电数智街道/中电数智社区", "所属网格": "测试网格1213",
             "商铺类型": "测试", "商铺等级": "小型商铺", "被访商铺": "全选/固话", "任务频率": "单次",
             "项目时间": "2025-08-12,2025-08-22", "任务负责人": "全选/刘**---三级网格员",
             },

            # 添加更多测试数据集
        ],
        # ids=["新增-成功"
        #
        #      ]
    )
    @allure.step("测试新增人员-成功")
    def test_add_success(self, 人工下发巡查页面,
                         表单数据: dict
                         ):
        global NEW_PERSON_ADDED
        try:
            人工下发巡查页面.click_button("新增")
            self.log_step("点击新增按钮")

            人工下发巡查页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据)

            self.log_step("填写表单信息")

            人工下发巡查页面.click_button("确定")
            self.log_step("提交表单")

            expect(人工下发巡查页面.page.get_by_text("添加成功")).to_be_visible(timeout=5000)
            self.log_step("验证新增成功-页面提示信息")

            人工下发巡查页面.输入查询条件(项目名称=表单数据.get("走访项目"))
            人工下发巡查页面.click_button("搜索")
            人工下发巡查页面.等待表格加载完成()
            self.log_step("查询刚才新增的数据")
            loc_新增的行 = 人工下发巡查页面.get_table_rows().filter(has_text=表单数据.get("走访项目")).filter(
                has_text=表单数据.get("所属社区").split("/")[-1], ).filter(has_text=表单数据.get("商铺类型")).first
            # 检查表格中是否有新增的数据
            expect(loc_新增的行).to_be_visible()

            # 标记新增成功
            NEW_PERSON_ADDED = True
        except Exception as e:
            raise e


@pytest.mark.usefixtures("人工下发巡查页面")  # 显式声明夹具
class TestDetail(BaseCase):
    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "行号",
        [
            (2),
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试商铺详情")
    def test_detail(self, 人工下发巡查页面, 行号):
        list_某行 = 人工下发巡查页面.获取表格中指定行的所有字段值(行号)
        人工下发巡查页面.点击表格中某行按钮(行号=行号, 按钮名="详情")
        人工下发巡查页面.校验表单中数据成功修改(
            **{"走访项目": list_某行[1], "所属社区": list_某行[2],
               "商铺类型": list_某行[3], "商铺等级": list_某行[4], "任务频率": list_某行[7],
               })
        人工下发巡查页面.校验表单中项目时间成功修改(list_某行[5], list_某行[6])
        assert 人工下发巡查页面.获取任务负责人字符串().strip() == list_某行[8].strip()


class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "表单数据",
        [
            {"居委会": "中电数智街道/中电数智社区"},
            {"项目名称": "测试"},
            {"居委会": "中电数智街道/中电数智社区", "商铺类型": "测试"},
            {"商铺等级": "小型商铺"},
            {"日期": "2025-01-01,2025-02-01"},
            {"居委会": "中电数智街道/中电数智社区", "网格": "测试网格1213", "项目名称": "测试", "商铺类型": "测试",
             "商铺等级": "小型商铺", "日期": "2025-01-01,2025-02-01"},
        ]
    )
    def test_query(self, 人工下发巡查页面, 表单数据: dict):
        # 输入查询条件
        人工下发巡查页面.输入查询条件(**表单数据)
        人工下发巡查页面.click_button("搜索")
        人工下发巡查页面.等待表格加载完成()

        # 定义字段与验证逻辑的映射
        def verify_居委会():
            列表_居委会 = 人工下发巡查页面.get_column_values_by_name("社区")
            居委会_预期值 = 表单数据["居委会"].split("/")[-1]

            # 断言 列表_居委会 中的每一项都包含 居委会_预期值
            assert all(居委会_预期值 == 居委会 for 居委会 in
                       列表_居委会), f"查询条件-居委会:{居委会_预期值}, 表格中的居委会为:{列表_居委会}"

        def verify_项目名称():
            列表_项目名称 = 人工下发巡查页面.get_column_values_by_name("走访项目")
            项目名称_预期值 = 表单数据["项目名称"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                项目名称_预期值 in 项目名称 for 项目名称 in
                列表_项目名称), f"查询条件-项目名称:{项目名称_预期值}, 表格中的项目名称为:{列表_项目名称}"

        def verify_商铺类型():
            列表_商铺类型 = 人工下发巡查页面.get_column_values_by_name("商铺类型")
            商铺类型_预期值 = 表单数据["商铺类型"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                商铺类型_预期值 == 商铺类型 for 商铺类型 in
                列表_商铺类型), f"查询条件-商铺类型:{商铺类型_预期值}, 表格中的商铺类型为:{列表_商铺类型}"

        def verify_商铺等级():
            列表_商铺等级 = 人工下发巡查页面.get_column_values_by_name("商铺等级")
            商铺等级_预期值 = 表单数据["商铺等级"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                商铺等级_预期值 == 商铺等级 for 商铺等级 in
                列表_商铺等级), f"查询条件-商铺等级:{商铺等级_预期值}, 表格中的商铺等级为:{列表_商铺等级}"

        def verify_日期():
            # 解析预期的日期范围
            起始日期_str, 结束日期_str = 表单数据["日期"].split(',')
            起始日期 = datetime.strptime(起始日期_str.strip(), "%Y-%m-%d")
            结束日期 = datetime.strptime(结束日期_str.strip(), "%Y-%m-%d")

            # 获取表格中所有任务时间列的值并转换为 datetime 对象
            列表_时间 = 人工下发巡查页面.get_column_values_by_name("项目创建时间")
            时间列表_datetime = [datetime.strptime(时间.strip(), "%Y-%m-%d %H:%M:%S") for 时间 in 列表_时间]

            # 断言每个日期都在范围内
            assert all(起始日期 <= 时间 <= 结束日期 for 时间 in 时间列表_datetime), \
                f"查询条件-日期范围: {表单数据['日期']}, 表格中的时间为: {列表_时间}"

        # 字典映射字段到验证函数
        验证规则 = {
            "居委会": verify_居委会,
            "项目名称": verify_项目名称,
            "商铺类型": verify_商铺类型,
            "商铺等级": verify_商铺等级,
            "日期": verify_日期,
        }

        # 执行匹配的验证规则
        for field in 表单数据:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")


class TestReset(BaseCase):
    def test_reset(self, 人工下发巡查页面):
        # 输入查询条件
        人工下发巡查页面.输入查询条件(
            **{"居委会": "中电数智街道/中电数智社区", "网格": "测试网格1213", "项目名称": "测试", "商铺类型": "测试",
             "商铺等级": "小型商铺", "日期": "2025-01-01,2025-02-01"})

        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        人工下发巡查页面.click_button("重置")

        人工下发巡查页面.校验查询条件成功修改(**{"居委会": "", "网格": "", "项目名称": "", "商铺类型": "",
             "商铺等级": ""})
        人工下发巡查页面.校验查询条件_日期("","")
        # 对比页面查询到的总条数和无查询条件时查数据库的总条数
        # 数据条数_页面 = 人工下发巡查页面.获取页面统计的总数据量()


@pytest.mark.usefixtures("后置操作_重置查询条件")
class TestDelete(BaseCase):
    def setup_class(self):
        if not NEW_PERSON_ADDED:
            pytest.skip("新增用例执行失败，跳过删除相关测试")

    @pytest.mark.parametrize(
        "表单数据_查询",
        [
            {
                "项目名称": f"新增-成功{number}",
                # "项目名称": "新增-成功1345947"
            },
            # f"修改-成功{车牌号_修改后}"
        ]
    )
    def test_delete_success(self, 人工下发巡查页面, 表单数据_查询):
        # 查找待删除的记录
        # 输入查询条件
        人工下发巡查页面.输入查询条件(**表单数据_查询)
        人工下发巡查页面.click_button("搜索")
        人工下发巡查页面.等待表格加载完成()
        self.log_step("输入查询条件")
        删除前的数据量 = 人工下发巡查页面.获取页面统计的总数据量()
        # 点击删除按钮
        人工下发巡查页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        人工下发巡查页面.点击提示弹窗中的确定按钮()
        self.log_step("点击删除按钮，再点击确定按钮")
        expect(人工下发巡查页面.page.get_by_text("删除成功")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现删除成功字样")
        # 输入查询条件
        人工下发巡查页面.click_button("搜索")
        人工下发巡查页面.等待表格加载完成()
        删除后的数据量 = 人工下发巡查页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量 - 1

    @pytest.mark.parametrize("表单数据_查询", [
        {
            "项目名称": "测试1"
        },
    ])
    def test_delete_cancel(self, 人工下发巡查页面, 表单数据_查询):
        # 输入查询条件
        人工下发巡查页面.输入查询条件(**表单数据_查询)
        人工下发巡查页面.click_button("搜索")
        人工下发巡查页面.等待表格加载完成()
        self.log_step("输入查询条件")
        删除前的数据量 = 人工下发巡查页面.获取页面统计的总数据量()
        # 点击删除按钮
        人工下发巡查页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        人工下发巡查页面.click_button("取消")
        self.log_step("点击删除按钮,弹窗后点击取消按钮")
        expect(人工下发巡查页面.page.get_by_text("删除成功")).not_to_be_visible(timeout=5000)
        self.log_step("验证页面未出现删除成功字样")
        人工下发巡查页面.click_button("搜索")
        # 等待1秒
        人工下发巡查页面.等待表格加载完成()
        删除后的数据量 = 人工下发巡查页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量


@pytest.mark.usefixtures("夹具_测试走访明细页面")
class TestVisitDetailsBasic(BaseCase):
    @allure.step("测试走访明细页面列表中的商铺名称和任务负责人等数据是否正确")
    def test_data_check(self, 夹具_测试走访明细页面):
        夹具_测试走访明细页面.等待表格加载完成()
        列表_商铺名称 = 夹具_测试走访明细页面.get_column_values_by_name("商铺名称")
        列表_任务负责人 = 夹具_测试走访明细页面.get_column_values_by_name("任务负责人")
        页面统计的数据量 = str(夹具_测试走访明细页面.获取页面统计的总数据量())
        表格中已办结的行数 = str(夹具_测试走访明细页面.get_table_rows().filter(has_text="已办结").count())
        任务总数_统计值 = 夹具_测试走访明细页面.获取任务总数()
        已办结任务数_统计值 = 夹具_测试走访明细页面.获取已完成任务数()
        assert 页面统计的数据量 == 任务总数_统计值, f"页面统计的数据量与页面的实际行数不一致，页面统计的数据量为{任务总数_统计值}，表格中的行数为{页面统计的数据量}"
        assert 表格中已办结的行数 == 已办结任务数_统计值, f"已办结任务数_统计值与表格中已办结的行数不一致，已办结任务数_统计值为{已办结任务数_统计值}，表格中已办结的行数为{表格中已办结的行数}"
        assert all(任务负责人.strip() == 字符串_任务负责人 for 任务负责人 in 列表_任务负责人), f"走访明细中的任务负责人与走访商铺详情中的不一致，走访明细中的任务负责人为:{列表_任务负责人}，走访商铺详情中的任务负责人为:{字符串_任务负责人}"
        assert all(商铺名称 in 列表_被访商铺 for 商铺名称 in 列表_商铺名称), f"走访明细中的某些商铺在走访商铺详情中不存在，走访明细中的商铺为:{列表_商铺名称}，走访商铺详情中的商铺为:{列表_被访商铺}"


    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "表单数据",
        [
            {"商铺名称": "兰州拉面"},
            {"任务状态": "待处理"},
            {"日期": "2025-06-10,2025-07-20"},
            {"商铺名称": "兰州拉面", "任务状态": "待处理", "日期": "2025-06-10,2025-07-20"},
        ]
    )
    @allure.step("测试走访明细页面的查询功能")
    def test_query(self, 夹具_测试走访明细页面, 表单数据: dict):
        ## 输入查询条件
        夹具_测试走访明细页面.输入查询条件(**表单数据)
        夹具_测试走访明细页面.click_button("搜索")
        夹具_测试走访明细页面.等待表格加载完成()

        # 定义字段与验证逻辑的映射
        def verify_商铺名称():
            列表_商铺名称 = 夹具_测试走访明细页面.get_column_values_by_name("商铺名称")
            商铺名称_预期值 = 表单数据["商铺名称"]

            # 断言 列表_商铺名称 中的每一项都包含 商铺名称_预期值
            assert all(商铺名称_预期值 == 商铺名称 for 商铺名称 in
                       列表_商铺名称), f"查询条件-商铺名称:{商铺名称_预期值}, 表格中的商铺名称为:{列表_商铺名称}"

        def verify_任务状态():
            列表_任务状态 = 夹具_测试走访明细页面.get_column_values_by_name("处理状态")
            任务状态_预期值 = 表单数据["任务状态"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                任务状态_预期值 == 任务状态 for 任务状态 in
                列表_任务状态), f"查询条件-任务状态:{任务状态_预期值}, 表格中的任务状态为:{列表_任务状态}"

        def verify_日期():
            # 解析预期的日期范围
            起始日期_str, 结束日期_str = 表单数据["日期"].split(',')
            起始日期 = datetime.strptime(起始日期_str.strip(), "%Y-%m-%d")
            结束日期 = datetime.strptime(结束日期_str.strip(), "%Y-%m-%d")

            # 获取表格中所有任务时间列的值并转换为 datetime 对象
            列表_时间 = 夹具_测试走访明细页面.get_column_values_by_name("任务时间")
            时间列表_datetime = [datetime.strptime(时间.strip(), "%Y-%m-%d") for 时间 in 列表_时间]

            # 断言每个日期都在范围内
            assert all(起始日期 <= 时间 <= 结束日期 for 时间 in 时间列表_datetime), \
                f"查询条件-日期范围: {表单数据['日期']}, 表格中的时间为: {列表_时间}"

        # 字典映射字段到验证函数
        验证规则 = {
            "商铺名称": verify_商铺名称,
            "任务状态": verify_任务状态,
            "日期": verify_日期,
        }

        # 执行匹配的验证规则
        for field in 表单数据:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")

    def test_reset(self, 夹具_测试走访明细页面):
        # 输入查询条件
        夹具_测试走访明细页面.输入查询条件(
            **{"商铺名称": "兰州拉面", "任务状态": "待处理", "日期": "2025-06-10,2025-07-20"})

        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        夹具_测试走访明细页面.click_button("重置")
        # 校验
        夹具_测试走访明细页面.校验查询条件成功修改(**{"商铺名称": "", "任务状态": ""})
        夹具_测试走访明细页面.校验查询条件_日期("", "")

    @pytest.mark.usefixtures("后置操作_关闭抽屉")
    @pytest.mark.parametrize(
        "行号",
        [
            (1),
            (2),
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试详情")
    def test_detail(self, 夹具_测试走访明细页面, 行号):
        # 跳转到场所
        夹具_测试走访明细页面.等待表格加载完成()
        list_某行 = 夹具_测试走访明细页面.获取表格中指定行的所有字段值(行号)
        夹具_测试走访明细页面.点击表格中某行按钮(行号=行号, 按钮名="详情")
        数据字典_走访明细详情页 = 夹具_测试走访明细页面.获取详情页中的数据(loc_表单项最上层=夹具_测试走访明细页面.page.locator(".el-drawer"))
        夹具_测试走访明细页面.关闭抽屉()
        夹具_测试走访明细页面.跳转到某菜单("基础信息","场所管理/场所信息")
        场所信息页面 = PageStoreInfo(夹具_测试走访明细页面.page)
        场所信息页面.输入查询条件(商铺名称=list_某行[2])
        场所信息页面.click_button("搜索")
        场所信息页面.等待表格加载完成()
        列表_名称 = 场所信息页面.get_column_values_by_name("名称")
        列表_待查找的下标 = [i for i, x in enumerate(列表_名称) if x == list_某行[2]]
        assert len(列表_待查找的下标) == 1,"表格中存在名称重复的元素，系统无法决定对哪个元素进行操作"
        场所信息页面.点击表格中某行按钮(行号=列表_待查找的下标[0]+1, 按钮名="详情")
        数据字典_场所信息详情页 = 场所信息页面.获取详情页中的数据(loc_表单项最上层=场所信息页面.page.locator(".el-drawer"))
        夹具_测试走访明细页面.校验表单中数据成功修改(
            **{"商铺名称": list_某行[2], "任务生成时间": list_某行[3],
               "任务状态": list_某行[5]})


    """由于我的账号没有删除的权限，无法进行测试"""
    # def test_delete_success(self, 夹具_测试走访明细页面):
    #     夹具_测试走访明细页面.等待表格加载完成()
    #     self.log_step("输入查询条件")
    #     删除前的数据量 = 夹具_测试走访明细页面.获取页面统计的总数据量()
    #     # 点击删除按钮
    #     夹具_测试走访明细页面.点击表格中某行按钮(行号=1, 按钮名="删除")
    #     夹具_测试走访明细页面.点击提示弹窗中的确定按钮()
    #     self.log_step("点击删除按钮，再点击确定按钮")
    #     expect(夹具_测试走访明细页面.page.get_by_text("删除成功")).to_be_visible(timeout=5000)
    #     self.log_step("验证页面出现删除成功字样")
    #     # 输入查询条件
    #     夹具_测试走访明细页面.click_button("搜索")
    #     夹具_测试走访明细页面.等待表格加载完成()
    #     删除后的数据量 = 夹具_测试走访明细页面.获取页面统计的总数据量()
    #     assert 删除后的数据量 == 删除前的数据量 - 1

    # def test_delete_cancel(self, 夹具_测试走访明细页面):
    #     # 输入查询条件
    #     夹具_测试走访明细页面.等待表格加载完成()
    #     self.log_step("输入查询条件")
    #     删除前的数据量 = 夹具_测试走访明细页面.获取页面统计的总数据量()
    #     # 点击删除按钮
    #     夹具_测试走访明细页面.点击表格中某行按钮(行号=1, 按钮名="删除")
    #     夹具_测试走访明细页面.click_button("取消")
    #     self.log_step("点击删除按钮,弹窗后点击取消按钮")
    #     expect(夹具_测试走访明细页面.page.get_by_text("删除成功")).not_to_be_visible(timeout=5000)
    #     self.log_step("验证页面未出现删除成功字样")
    #     夹具_测试走访明细页面.click_button("搜索")
    #     # 等待1秒
    #     夹具_测试走访明细页面.等待表格加载完成()
    #     删除后的数据量 = 夹具_测试走访明细页面.获取页面统计的总数据量()
    #     assert 删除后的数据量 == 删除前的数据量
