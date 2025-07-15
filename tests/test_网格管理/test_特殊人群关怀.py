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

from pages.网格管理.特殊人群关怀 import PageSpecialCare

# from pages.基础信息.实有房屋.楼栋管理 import PageFloor


# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取当前时间，精确到时分秒
current_time = datetime.now()
# 将时间转换为字符串格式
time_string = current_time.strftime("%Y-%m-%d,%H:%M:%S")


@pytest.fixture(scope="module")
def 特殊人群关怀页面(浏览器已打开的页面):
    # 将页面封装为特殊人群关怀页面
    page = PageSpecialCare(浏览器已打开的页面)
    page.跳转到某菜单("网格管理", "特殊人群关怀")
    yield page

@pytest.fixture(scope="class")
def 夹具_测试任务记录页面(特殊人群关怀页面):
    特殊人群关怀页面.输入查询条件(走访项目名称=f"新增-成功{time_string}")
    特殊人群关怀页面.click_button("搜索")
    特殊人群关怀页面.等待表格加载完成()
    特殊人群关怀页面.点击表格中某行按钮(行号=1,按钮名="任务记录")
    特殊人群关怀页面.等待表格加载完成()
    yield 特殊人群关怀页面
    特殊人群关怀页面.click_button("返回")

# 定义一个模块级变量，用于标记是否新增成功
NEW_PERSON_ADDED = False


@pytest.mark.usefixtures("后置操作_重置查询条件")
@pytest.mark.usefixtures("特殊人群关怀页面")
class TestAdd(BaseCase):
    @pytest.mark.parametrize(
        "表单数据",

        [
            {"走访项目": f"新增-成功{time_string}", "位置": "庐阳区/中电数智街道/中电数智社区", "网格": "测试网格5",
             "人员标签": "现役军人", "选择被访人员": "全选/车*__庐阳区中电数智街道中电数智社区小区*栋*",
             "项目时间": "2026-03-20,2026-06-10", "任务频率": "单次",
             "是否发布": "是", "负责人类型": "网格员", "任务负责人":"全选/付**__三级网格员",
             }

            # 添加更多测试数据集
        ],
        # ids=["新增-成功"
        #
        #      ]
    )
    @allure.step("测试新增人员-成功")
    def test_add_success(self, 特殊人群关怀页面,
                         表单数据: dict
                         ):
        global NEW_PERSON_ADDED
        try:
            特殊人群关怀页面.click_button("新增")
            self.log_step("点击新增按钮")

            特殊人群关怀页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
                **表单数据)
            self.log_step("填写表单信息")

            特殊人群关怀页面.click_button("确定")
            self.log_step("提交表单")

            expect(特殊人群关怀页面.page.get_by_text("添加成功")).to_be_visible(timeout=5000)
            self.log_step("验证新增成功-页面提示信息")

            特殊人群关怀页面.输入查询条件(走访项目名称=表单数据.get("走访项目"))
            特殊人群关怀页面.click_button("搜索")
            特殊人群关怀页面.等待表格加载完成()
            self.log_step("查询刚才新增的数据")
            loc_新增的行 = 特殊人群关怀页面.get_table_rows().filter(has_text=表单数据.get("走访项目")).filter(
                has_text=表单数据.get("位置").split("/")[-1]).filter(has_text=表单数据.get("人员标签")).filter(
                has_text=表单数据.get("任务频率")).first
            # 检查表格中是否有新增的数据
            expect(loc_新增的行).to_be_visible()

            # 标记新增成功
            NEW_PERSON_ADDED = True
        except Exception as e:
            raise e

    # @pytest.mark.usefixtures("后置操作_刷新页面")
    # @pytest.mark.parametrize(
    #     "表单数据",
    #
    #     [
    #         {"商铺名称": f"彭超", "所属居委会": "中电数智街道/中电数智社区", "所属网格": "测试网格1213",
    #          "统一信用代码": "91310115MA1K41MXQ5",
    #          "负责人": "石童涛", "联系方式": "13955499272", "商铺类型": "测试", "商铺等级": "小型商铺",
    #          "归属部门": "合肥市市场管理局", "入驻时间": "2015-07-13", "具体位置": "安徽省合肥市蜀山区芙蓉社区1005号",
    #          "执照日期": "2015-06-10,2029-07-28",
    #          "营业时间": "06:20:00,21:30:00",
    #          "门头照": r"C:\Users\Administrator\Pictures\111.png"
    #          }
    #     ],
    # )
    # @allure.step("测试新增商铺失败-去重校验：同一网格内商铺名称不能重复")
    # def test_add_repeat_validation(self, 特殊人群关怀页面,
    #                                表单数据: dict
    #                                ):
    #     特殊人群关怀页面.输入查询条件(商铺名称=表单数据.get("商铺名称"))
    #     特殊人群关怀页面.click_button("搜索")
    #     新增前的数据量 = 特殊人群关怀页面.获取页面统计的总数据量()
    #     # 点击新增按钮
    #     特殊人群关怀页面.click_button("新增")
    #     self.log_step("点击新增按钮")
    #     # 填写表单信息
    #     特殊人群关怀页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据)
    #     self.log_step("填写表单信息")
    #     # 点击提交按钮
    #     特殊人群关怀页面.click_button("提交")
    #     特殊人群关怀页面.点击提示弹窗中的确定按钮()
    #     self.log_step("提交表单")
    #     # 断言该人员已存在字样在页面出现
    #     特殊人群关怀页面.验证页面顶部出现全局提示("名称已存在")
    #     self.log_step("验证新增失败-去重校验-页面提示信息")
    #     # 刷新页面
    #     特殊人群关怀页面.page.reload()
    #     # 填写搜索框
    #     特殊人群关怀页面.输入查询条件(商铺名称=表单数据.get("商铺名称"))
    #     特殊人群关怀页面.click_button("搜索")
    #     新增后的数据量 = 特殊人群关怀页面.获取页面统计的总数据量()
    #     # 检查表格中是否有新增的数据
    #     assert 新增前的数据量 == 新增后的数据量
    #     self.log_step("验证查询列表中无新增的数据")



@pytest.mark.usefixtures("特殊人群关怀页面")  # 显式声明夹具
class TestDetail(BaseCase):
    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "行号",
        [
            (1),
            (2),
            (3),
            (4),
            (5),

        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试详情")
    def test_detail(self, 特殊人群关怀页面, 行号):
        特殊人群关怀页面.等待表格加载完成()
        list_某行 = 特殊人群关怀页面.获取表格中指定行的所有字段值(行号)
        特殊人群关怀页面.点击表格中某行按钮(行号=行号, 按钮名="详情")
        特殊人群关怀页面.校验表单中数据成功修改(
            **{"走访项目": list_某行[1], "人员标签": list_某行[4],
               "任务频率": list_某行[7], "是否发布": "是" if list_某行[9] == "已发布" else "否"})
        特殊人群关怀页面.校验表单中位置成功修改(list_某行[3])
        特殊人群关怀页面.校验表单中项目时间成功修改(list_某行[5], list_某行[6])
        特殊人群关怀页面.校验表单中无待选人员表单项()

@pytest.mark.usefixtures("特殊人群关怀页面")
class TestTaskRecord(BaseCase):
    @pytest.mark.usefixtures("后置操作_点击返回按钮")
    @pytest.mark.parametrize(
        "行号",
        [
            (1),
            (2),
            (3),
            (4),
            (5),

        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试任务记录")
    def test_task_record(self, 特殊人群关怀页面, 行号):
        特殊人群关怀页面.等待表格加载完成()
        # 特殊人群关怀页面.点击表格中某行按钮(行号=行号, 按钮名="详情")
        # # 特殊人群关怀页面.等待表格加载完成()
        # expect(特殊人群关怀页面.page.locator(".el-drawer")).to_be_visible()
        # 被访人员列表 = 特殊人群关怀页面.获取被访人员列表()
        # 任务负责人列表 = 特殊人群关怀页面.获取任务负责人列表()
        特殊人群关怀页面.点击表格中某行按钮(行号=行号, 按钮名="任务记录")
        特殊人群关怀页面.等待表格加载完成()
        # 特殊人群关怀页面.核对被访人员列表(被访人员列表)
        # 特殊人群关怀页面.核对任务负责人列表(任务负责人列表)
        任务总数_实际值 = 特殊人群关怀页面.get_table_rows().count()
        完成任务数_实际值 = 特殊人群关怀页面.get_table_rows().filter(has_text="已处理").count()
        任务总数_统计值 = 特殊人群关怀页面.page.locator("xpath=//div[text()='任务总数']/following-sibling::*").inner_text()
        完成任务数_统计值 = 特殊人群关怀页面.page.locator("xpath=//div[text()='完成任务']/following-sibling::*").inner_text()
        assert 任务总数_统计值 == str(任务总数_实际值) ,f"任务总数的统计值为{任务总数_统计值},实际值为{任务总数_实际值}"
        assert 完成任务数_统计值 == str(完成任务数_实际值) ,f"完成任务数的统计值为{完成任务数_统计值},实际值为{完成任务数_实际值}"

@pytest.mark.usefixtures("夹具_测试任务记录页面")
class TestTaskRecordBasic(BaseCase):
    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "表单数据",
        [
            {"姓名": "石岱宗"},
            {"处理状态": "待处理"},
            {"日期": "2025-07-01,2025-08-20"},
            {"姓名": "石岱宗", "处理状态": "待处理", "日期": "2025-07-01,2025-08-20"},
        ]
    )
    @allure.step("测试任务记录页面的查询功能")
    def test_task_record_query(self, 夹具_测试任务记录页面, 表单数据: dict):
        ## 输入查询条件
        夹具_测试任务记录页面.输入查询条件(**表单数据)
        夹具_测试任务记录页面.click_button("搜索")
        夹具_测试任务记录页面.等待表格加载完成()

        # 定义字段与验证逻辑的映射
        def verify_姓名():
            列表_姓名 = 夹具_测试任务记录页面.get_column_values_by_name("姓名")
            姓名_预期值 = 表单数据["姓名"][0] + (len(表单数据["姓名"])-1) * "*"

            # 断言 列表_姓名 中的每一项都包含 姓名_预期值
            assert all(姓名_预期值 == 姓名 for 姓名 in
                       列表_姓名), f"查询条件-姓名:{姓名_预期值}, 表格中的姓名为:{列表_姓名}"

        def verify_处理状态():
            列表_处理状态 = 夹具_测试任务记录页面.get_column_values_by_name("处理状态")
            处理状态_预期值 = 表单数据["处理状态"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                处理状态_预期值 == 处理状态 for 处理状态 in
                列表_处理状态), f"查询条件-处理状态:{处理状态_预期值}, 表格中的处理状态为:{列表_处理状态}"

        def verify_日期():
            # 解析预期的日期范围
            起始日期_str, 结束日期_str = 表单数据["日期"].split(',')
            起始日期 = datetime.strptime(起始日期_str.strip(), "%Y-%m-%d")
            结束日期 = datetime.strptime(结束日期_str.strip(), "%Y-%m-%d")

            # 获取表格中所有任务时间列的值并转换为 datetime 对象
            列表_时间 = 夹具_测试任务记录页面.get_column_values_by_name("任务时间")
            时间列表_datetime = [datetime.strptime(时间.strip(), "%Y-%m-%d") for 时间 in 列表_时间]

            # 断言每个日期都在范围内
            assert all(起始日期 <= 时间 <= 结束日期 for 时间 in 时间列表_datetime), \
                f"查询条件-日期范围: {表单数据['日期']}, 表格中的某些时间为: {列表_时间}"

        # 字典映射字段到验证函数
        验证规则 = {
            "姓名": verify_姓名,
            "处理状态": verify_处理状态,
            "日期": verify_日期,
        }

        # 执行匹配的验证规则
        for field in 表单数据:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")

    def test_reset(self, 夹具_测试任务记录页面):
        # 输入查询条件
        夹具_测试任务记录页面.输入查询条件(
            **{"姓名": "石岱宗", "处理状态": "待处理", "日期": "2025-07-01,2025-08-20"})

        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        夹具_测试任务记录页面.click_button("重置")

        夹具_测试任务记录页面.校验查询条件成功修改(**{"姓名": "", "处理状态": "", "日期": ""})

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "行号",
        [
            (1),
            (2),
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试详情")
    def test_detail(self, 夹具_测试任务记录页面, 行号):
        夹具_测试任务记录页面.等待表格加载完成()
        list_某行 = 夹具_测试任务记录页面.获取表格中指定行的所有字段值(行号)
        夹具_测试任务记录页面.点击表格中某行按钮(行号=行号, 按钮名="查看")
        夹具_测试任务记录页面.校验表单中数据成功修改(
            **{"走访项目": list_某行[1], "姓名": list_某行[2],
               "联系方式": list_某行[3], "住址": list_某行[4], "任务时间": list_某行[5], "任务状态": list_某行[7]})

    def test_delete_success(self, 夹具_测试任务记录页面):
        夹具_测试任务记录页面.等待表格加载完成()
        self.log_step("输入查询条件")
        删除前的数据量 = 夹具_测试任务记录页面.获取页面统计的总数据量()
        # 点击删除按钮
        夹具_测试任务记录页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        夹具_测试任务记录页面.点击提示弹窗中的确定按钮()
        self.log_step("点击删除按钮，再点击确定按钮")
        expect(夹具_测试任务记录页面.page.get_by_text("删除成功")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现删除成功字样")
        # 输入查询条件
        夹具_测试任务记录页面.click_button("搜索")
        夹具_测试任务记录页面.等待表格加载完成()
        删除后的数据量 = 夹具_测试任务记录页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量 - 1
    def test_delete_cancel(self, 夹具_测试任务记录页面):
        # 输入查询条件
        夹具_测试任务记录页面.等待表格加载完成()
        self.log_step("输入查询条件")
        删除前的数据量 = 夹具_测试任务记录页面.获取页面统计的总数据量()
        # 点击删除按钮
        夹具_测试任务记录页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        夹具_测试任务记录页面.click_button("取消")
        self.log_step("点击删除按钮,弹窗后点击取消按钮")
        expect(夹具_测试任务记录页面.page.get_by_text("删除成功")).not_to_be_visible(timeout=5000)
        self.log_step("验证页面未出现删除成功字样")
        夹具_测试任务记录页面.click_button("搜索")
        # 等待1秒
        夹具_测试任务记录页面.等待表格加载完成()
        删除后的数据量 = 夹具_测试任务记录页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量



class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "表单数据",
        [
            {"项目名称": "11111"},
            {"任务来源": "网格自访"},
            {"人员标签": "现役军人"},
            {"日期": "2025-04-01,2025-06-20"},
            {"项目名称": "22222", "任务来源": "上级下发", "人员标签": "特扶家庭", "日期": "2025-05-01,2025-06-01"},
        ]
    )
    def test_query(self, 特殊人群关怀页面, 表单数据: dict):
        # 输入查询条件
        特殊人群关怀页面.输入查询条件(**表单数据)
        特殊人群关怀页面.click_button("搜索")
        特殊人群关怀页面.等待表格加载完成()

        # 定义字段与验证逻辑的映射
        def verify_项目名称():
            列表_项目名称 = 特殊人群关怀页面.get_column_values_by_name("走访项目")
            项目名称_预期值 = 表单数据["项目名称"]

            # 断言 列表_项目名称 中的每一项都包含 项目名称_预期值
            assert all(项目名称_预期值 == 项目名称 for 项目名称 in
                       列表_项目名称), f"查询条件-项目名称:{项目名称_预期值}, 表格中的项目名称为:{列表_项目名称}"

        def verify_任务来源():
            列表_任务来源 = 特殊人群关怀页面.get_column_values_by_name("任务来源")
            任务来源_预期值 = 表单数据["任务来源"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                任务来源_预期值 == 任务来源 for 任务来源 in
                列表_任务来源), f"查询条件-任务来源:{任务来源_预期值}, 表格中的任务来源为:{列表_任务来源}"

        def verify_人员标签():
            列表_人员标签 = 特殊人群关怀页面.get_column_values_by_name("人员标签")
            人员标签_预期值 = 表单数据["人员标签"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                人员标签_预期值 == 人员标签 for 人员标签 in
                列表_人员标签), f"查询条件-人员标签:{人员标签_预期值}, 表格中的人员标签为:{列表_人员标签}"

        def verify_日期():
            # 解析预期的全局日期范围
            起始日期_str, 结束日期_str = 表单数据["日期"].split(',')
            起始日期 = datetime.strptime(起始日期_str.strip(), "%Y-%m-%d")
            结束日期 = datetime.strptime(结束日期_str.strip(), "%Y-%m-%d")

            # 获取表格中所有开始时间和结束时间列，并转换为 datetime 对象
            列表_开始时间 = 特殊人群关怀页面.get_column_values_by_name("项目开始时间")
            列表_结束时间 = 特殊人群关怀页面.get_column_values_by_name("项目结束时间")

            # 转换为 datetime 对象
            开始时间_datetime = [datetime.strptime(t.strip(), "%Y-%m-%d") for t in 列表_开始时间]
            结束时间_datetime = [datetime.strptime(t.strip(), "%Y-%m-%d") for t in 列表_结束时间]

            # 断言每条记录的时间段都在查询范围内
            assert all(
                起始日期 <= s <= e <= 结束日期
                for s, e in zip(开始时间_datetime, 结束时间_datetime)
            ), (
                f"查询条件-日期范围: {表单数据['日期']}, "
                f"表格中某些时间段超出范围，时间段列表为：{list(zip(开始时间_datetime, 结束时间_datetime))} "
            )

        # 字典映射字段到验证函数
        验证规则 = {
            "项目名称": verify_项目名称,
            "任务来源": verify_任务来源,
            "人员标签": verify_人员标签,
            "日期": verify_日期,
        }

        # 执行匹配的验证规则
        for field in 表单数据:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")


class TestReset(BaseCase):
    def test_reset(self, 特殊人群关怀页面):
        # 输入查询条件
        特殊人群关怀页面.输入查询条件(
            **{"项目名称": "22222", "任务来源": "上级下发", "人员标签": "特扶家庭", "日期": "2025-05-01,2025-06-01"})

        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        特殊人群关怀页面.click_button("重置")

        特殊人群关怀页面.校验查询条件成功修改(**{"项目名称": "", "任务来源": "", "人员标签": "", "日期": ""})
        # 对比页面查询到的总条数和无查询条件时查数据库的总条数
        # 数据条数_页面 = 特殊人群关怀页面.获取页面统计的总数据量()


@pytest.mark.usefixtures("后置操作_重置查询条件")
class TestDelete(BaseCase):
    # def setup_class(self):
    #     if not NEW_PERSON_ADDED:
    #         pytest.skip("新增用例执行失败，跳过删除相关测试")

    @pytest.mark.parametrize(
        "表单数据_查询",
        [
            {
                # "项目名称": f"新增-成功{time_string}",
                "项目名称": "新增-成功2025-07-14,15:43:31",

            },
            # f"修改-成功{车牌号_修改后}"
        ]
    )
    def test_delete_success(self, 特殊人群关怀页面, 表单数据_查询):
        # 查找待删除的记录
        # 输入查询条件
        特殊人群关怀页面.输入查询条件(**表单数据_查询)
        特殊人群关怀页面.click_button("搜索")
        特殊人群关怀页面.等待表格加载完成()
        self.log_step("输入查询条件")
        删除前的数据量 = 特殊人群关怀页面.获取页面统计的总数据量()
        # 点击删除按钮
        特殊人群关怀页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        特殊人群关怀页面.点击提示弹窗中的确定按钮()
        self.log_step("点击删除按钮，再点击确定按钮")
        expect(特殊人群关怀页面.page.get_by_text("删除成功")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现删除成功字样")
        # 输入查询条件
        特殊人群关怀页面.click_button("搜索")
        特殊人群关怀页面.等待表格加载完成()
        删除后的数据量 = 特殊人群关怀页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量 - 1

    @pytest.mark.parametrize("表单数据_查询", [
        {
            "项目名称": "测试同步",
        },
    ])
    def test_delete_cancel(self, 特殊人群关怀页面, 表单数据_查询):
        # 输入查询条件
        特殊人群关怀页面.输入查询条件(**表单数据_查询)
        特殊人群关怀页面.click_button("搜索")
        特殊人群关怀页面.等待表格加载完成()
        self.log_step("输入查询条件")
        删除前的数据量 = 特殊人群关怀页面.获取页面统计的总数据量()
        # 点击删除按钮
        特殊人群关怀页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        特殊人群关怀页面.click_button("取消")
        self.log_step("点击删除按钮,弹窗后点击取消按钮")
        expect(特殊人群关怀页面.page.get_by_text("删除成功")).not_to_be_visible(timeout=5000)
        self.log_step("验证页面未出现删除成功字样")
        特殊人群关怀页面.click_button("搜索")
        # 等待1秒
        特殊人群关怀页面.等待表格加载完成()
        删除后的数据量 = 特殊人群关怀页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量



