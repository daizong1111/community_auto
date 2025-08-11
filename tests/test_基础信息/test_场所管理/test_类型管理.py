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

from pages.基础信息.场所管理.类型管理 import PageTypeManage

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取当前时间，精确到时分秒
current_time = datetime.now()
# 将时间转换为字符串格式
time_string = current_time.strftime("%Y-%m-%d,%H:%M:%S")


@pytest.fixture(scope="module")
def 类型管理页面(浏览器已打开的页面):
    # 将页面封装为类型管理页面
    page = PageTypeManage(浏览器已打开的页面)
    page.跳转到某菜单('基础信息','场所管理/类型管理')
    yield page

@pytest.fixture(scope="class")
def 前置操作_自动下发和启用禁用(类型管理页面):
    """
    一次性插入多组数据，在整个测试类结束后统一清理
    """
    # 定义多组参数
    多组参数 = [
        {"类型名称": f"新增-成功{time_string}_1", "场所类别": "商铺"},
        {"类型名称": f"新增-成功{time_string}_2", "场所类别": "商铺", "任务频率": "每月两次", "任务处理时效": "11"},
    ]

    inserted_names = []  # 保存插入的类型名称，用于后续删除

    # 批量插入数据
    test_add = TestAdd()
    for 表单数据_基础 in 多组参数:
        表单数据_检查指引维护 = {"1": "请耐心检查"}
        test_add.test_add_success(类型管理页面, 表单数据_基础, 表单数据_检查指引维护)
        inserted_names.append(表单数据_基础["类型名称"])
    类型管理页面.page.reload()
    yield  # 测试类中的所有用例在此暂停，继续执行

    # 统一删除所有插入的数据
    test_delete = TestDelete()
    for 类型名称 in inserted_names:
        test_delete.test_delete_success(类型管理页面, {"类型名称": 类型名称})

# 定义一个模块级变量，用于标记是否新增成功
NEW_PERSON_ADDED = False


@pytest.mark.usefixtures("后置操作_重置查询条件")
@pytest.mark.usefixtures("类型管理页面")
class TestAdd(BaseCase):
    @pytest.mark.parametrize(
        "表单数据_基础, 表单数据_检查指引维护",

        [
            ({"类型名称": f"新增-成功{time_string}", "场所类别": "商铺", "任务频率": "每月两次", "任务处理时效": "11"}
                 , {"1": "请耐心检查"})

            # 添加更多测试数据集
        ],
        # ids=["新增-成功"
        #
        #      ]
    )
    @allure.step("测试新增人员-成功")
    def test_add_success(self, 类型管理页面,
                         表单数据_基础: dict, 表单数据_检查指引维护: dict
                         ):
        global NEW_PERSON_ADDED
        try:
            类型管理页面.click_button("新增")
            self.log_step("点击新增按钮")

            类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=类型管理页面.获取新增表单最上层定位(),**表单数据_基础)
            类型管理页面.检查指引维护_输入(表单数据_检查指引维护.get("1"))
            # 类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(籍贯="北京市/市辖区/东城区",)

            self.log_step("填写表单信息")

            类型管理页面.click_button("提交")
            类型管理页面.点击提示弹窗中的确定按钮()
            self.log_step("提交表单")

            expect(类型管理页面.page.get_by_text("新增成功")).to_be_visible(timeout=5000)
            self.log_step("验证新增成功-页面提示信息")

            类型管理页面.填写搜索框({"类型名称": 表单数据_基础.get("类型名称")})

            loc_新增的行 = 类型管理页面.get_table_rows().filter(has_text=表单数据_基础.get("类型名称")).filter(
                has_text=表单数据_基础.get("场所类别")).filter(has_text=表单数据_基础.get("任务频率")).filter(
                has_text=表单数据_基础.get("任务处理时效")).first
            # 检查表格中是否有新增的数据
            expect(loc_新增的行).to_be_visible()

            # 标记新增成功
            NEW_PERSON_ADDED = True
        except Exception as e:
            raise e

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "表单数据",

        [
            {"类型名称": "8844", "场所类别": "商铺", "任务频率": "每月两次", "任务处理时效": "11"}
            # 添加更多测试数据集
        ],
    )
    @allure.step("测试新增类型失败-去重校验：场所类别+类型名称不能重复")
    def test_add_repeat_validation(self, 类型管理页面,
                                   表单数据: dict
                                   ):
        # 点击新增按钮
        类型管理页面.click_button("新增")
        self.log_step("点击新增按钮")
        # 填写表单信息
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据)
        self.log_step("填写表单信息")
        # 点击提交按钮
        类型管理页面.click_button("提交")
        类型管理页面.点击提示弹窗中的确定按钮()
        self.log_step("提交表单")
        # 断言该人员已存在字样在页面出现
        类型管理页面.验证页面顶部出现全局提示("类型已存在")
        self.log_step("验证新增失败-去重校验-页面提示信息")
        # 刷新页面
        类型管理页面.page.reload()
        # 填写搜索框
        类型管理页面.填写搜索框({"类型名称": 表单数据.get("类型名称"), "场所类别": 表单数据.get("场所类别")})
        # 检查表格中是否有新增的数据
        expect(类型管理页面.get_table_rows()).to_have_count(1)
        self.log_step("验证查询列表中无新增的数据")


@pytest.mark.usefixtures("类型管理页面")  # 显式声明夹具
class TestEdit(BaseCase):
    def setup_class(self):
        if not NEW_PERSON_ADDED:
            pytest.skip("新增用例执行失败，跳过修改相关测试")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "表单数据_搜索框, 表单数据",
        [
            (
                    {
                        "类型名称": f"新增-成功{time_string}",
                        # "类型名称": "新增-成功2025-06-25,09:32:15"
                    },
                    {"类型名称": f"修改-成功{time_string}", "场所类别": "单位", "任务频率": "每月一次",
                     "任务处理时效": "24",
                     },
            ),
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试修改小区")
    def test_edit_success(self, 类型管理页面,
                          表单数据_搜索框: dict, 表单数据: dict):
        # 输入查询条件
        类型管理页面.填写搜索框(表单数据_搜索框)
        # 点击编辑按钮
        类型管理页面.点击表格中某行按钮(行号=1, 按钮名="编辑")
        self.log_step("点击编辑按钮")
        # 类型管理页面.page.wait_for_timeout(1000)
        # 填写表单信息
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            **表单数据)
        self.log_step("填写表单信息")
        # 点击提交按钮
        类型管理页面.click_button("提交")
        self.log_step("点击提交按钮")
        # 点击提示弹窗中的确定按钮
        类型管理页面.点击提示弹窗中的确定按钮()
        # 断言操作成功字样在页面出现
        expect(类型管理页面.page.get_by_text("编辑成功")).to_be_visible(timeout=5000)
        self.log_step("验证修改成功-页面提示信息")
        类型管理页面.填写搜索框({"类型名称": f"修改-成功{time_string}"})
        # 检查表格中数据是否成功修改
        类型管理页面.点击表格中某行按钮(行号=1, 按钮名="编辑")
        类型管理页面.校验表单中数据成功修改(类型名称=表单数据.get("类型名称"),
                                            场所类别=表单数据.get("场所类别"),
                                            任务频率=表单数据.get("任务频率"),
                                            任务处理时效=表单数据.get("任务处理时效"),
                                            )

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "表单数据_搜索框, 表单数据",

        [
            (
                    {
                        "类型名称": f"修改-成功{time_string}",
                        # "类型名称": "新增-成功2025-06-2509:26:37"
                    },
                    {"类型名称": f"8844", "场所类别": "商铺", "任务频率": "每月一次",
                     "任务处理时效": "24",
                     },
            ),
        ],
    )
    @allure.step("测试新增类型失败-去重校验：场所类别+类型名称不能重复")
    def test_edit_repeat_validation(self, 类型管理页面, 表单数据_搜索框: dict,
                                    表单数据: dict
                                    ):
        # 输入查询条件
        类型管理页面.填写搜索框(表单数据_搜索框)
        # 点击编辑按钮
        类型管理页面.点击表格中某行按钮(行号=1, 按钮名="编辑")
        self.log_step("点击编辑按钮")
        # 类型管理页面.page.wait_for_timeout(1000)
        # 填写表单信息
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            **表单数据)
        self.log_step("填写表单信息")
        # 点击提交按钮
        类型管理页面.click_button("提交")
        类型管理页面.点击提示弹窗中的确定按钮()
        self.log_step("提交表单")
        # 断言该人员已存在字样在页面出现
        类型管理页面.验证页面顶部出现全局提示("类型已存在")
        self.log_step("验证编辑失败-去重校验-页面提示信息")
        # 刷新页面
        类型管理页面.page.reload()
        # 填写搜索框
        类型管理页面.填写搜索框({"类型名称": 表单数据.get("类型名称"), "场所类别": 表单数据.get("场所类别")})
        # 检查表格中是否有新增的数据
        expect(类型管理页面.get_table_rows()).to_have_count(1)
        self.log_step("验证查询列表中无新增的数据")


class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "表单数据",
        [
            {"类型名称": "测试类型"},
            {"场所类别": "商铺"},
            {"类型状态": "启用"},
            {"开关状态": "开"},
            {"类型名称": "测试类型", "场所类别": "商铺", "类型状态": "启用", "开关状态": "开"},

        ]
    )
    def test_query(self, 类型管理页面, 表单数据: dict):
        # 输入查询条件
        类型管理页面.填写搜索框(表单数据)

        # 定义字段与验证逻辑的映射
        def verify_类型名称():
            列表_类型名称 = 类型管理页面.get_column_values_by_name("类型名称")
            类型名称_预期值 = 表单数据["类型名称"]

            # 断言 列表_类型名称 中的每一项都包含 类型名称_预期值
            assert all(类型名称_预期值 in 类型名称 for 类型名称 in
                       列表_类型名称), f"查询条件-类型名称:{类型名称_预期值}, 表格中的类型名称为:{列表_类型名称}"

        def verify_场所类别():
            列表_场所类别 = 类型管理页面.get_column_values_by_name("所属场所类别")
            场所类别_预期值 = 表单数据["场所类别"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                场所类别_预期值 == 场所类别 for 场所类别 in
                列表_场所类别), f"查询条件-场所类别:{场所类别_预期值}, 表格中的场所类别为:{列表_场所类别}"

        def verify_类型状态():
            列表_类型状态 = 类型管理页面.获取类型状态列()
            类型状态_预期值 = 表单数据["类型状态"]
            if 类型状态_预期值 == "启用":
                类型状态_预期值 = "禁用"
            elif 类型状态_预期值 == "禁用":
                类型状态_预期值 = "启用"
            else:
                raise Exception(f"类型状态输入错误:{类型状态_预期值}")
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                类型状态_预期值 == 类型状态 for 类型状态 in
                列表_类型状态), f"查询条件-类型状态:{类型状态_预期值}, 表格中的类型状态为:{列表_类型状态}"

        def verify_开关状态():
            列表_开关状态列的class属性 = 类型管理页面.获取开关状态列的class属性()
            开关状态_预期值 = 表单数据["开关状态"]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            if 开关状态_预期值 == "开":
                assert all(
                    "is-checked" in class属性 for class属性 in
                    列表_开关状态列的class属性), f"查询条件-开关状态:{开关状态_预期值}, 表格中的开关状态属性为:{列表_开关状态列的class属性}"
            else:
                assert all(
                    "is-checked" not in class属性 for class属性 in
                    列表_开关状态列的class属性), f"查询条件-开关状态:{开关状态_预期值}, 表格中的开关状态属性为:{列表_开关状态列的class属性}"

        # 字典映射字段到验证函数
        验证规则 = {
            "类型名称": verify_类型名称,
            "场所类别": verify_场所类别,
            "类型状态": verify_类型状态,
            "开关状态": verify_开关状态,

        }

        # 执行匹配的验证规则
        for field in 表单数据:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")


class TestReset(BaseCase):
    def test_reset(self, 类型管理页面):
        # 输入查询条件
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            **{"类型名称": "测试类型", "场所类别": "商铺", "类型状态": "启用", "开关状态": "开"})

        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        类型管理页面.click_button("重置")

        类型管理页面.校验表单中数据成功修改(**{"类型名称": "", "场所类别": "", "类型状态": "", "开关状态": ""})


@pytest.mark.usefixtures("后置操作_重置查询条件")
class TestDelete(BaseCase):
    def setup_class(self):
        if not NEW_PERSON_ADDED:
            pytest.skip("新增用例执行失败，跳过删除相关测试")

    @pytest.mark.parametrize(
        "表单数据_查询",
        [
            {
                "类型名称": f"修改-成功{time_string}",
                # "类型名称": "新增-成功2025-06-2509:26:37"
            },

            # f"修改-成功{车牌号_修改后}"
        ]
    )
    def test_delete_success(self, 类型管理页面, 表单数据_查询):
        # 查找待删除的记录
        # 输入查询条件
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_查询)
        类型管理页面.click_button("搜索")
        类型管理页面.等待表格加载完成()
        self.log_step("输入查询条件")
        删除前的数据量 = 类型管理页面.获取页面统计的总数据量()
        # 点击删除按钮
        类型管理页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        类型管理页面.click_button("确定")
        self.log_step("点击删除按钮,弹窗后点击确定按钮")
        expect(类型管理页面.page.get_by_text("删除成功")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现删除成功字样")
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_查询)
        类型管理页面.click_button("搜索")
        类型管理页面.等待表格加载完成()
        删除后的数据量 = 类型管理页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量 - 1

    @pytest.mark.parametrize("表单数据_查询", [
        {
            # "类型名称": f"修改-成功{time_string}",
            "类型名称": "餐饮用气场所"
        },
        # f"修改-成功{车牌号_修改后}"
    ])
    def test_delete_cancel(self, 类型管理页面, 表单数据_查询):
        # 输入查询条件
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_查询)
        类型管理页面.click_button("搜索")
        self.log_step("输入查询条件")
        类型管理页面.等待表格加载完成()
        删除前的数据量 = 类型管理页面.获取页面统计的总数据量()
        # 点击删除按钮
        类型管理页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        类型管理页面.click_button("取消")
        self.log_step("点击删除按钮,弹窗后点击取消按钮")
        expect(类型管理页面.page.get_by_text("已取消删除")).not_to_be_visible(timeout=5000)
        expect(类型管理页面.page.get_by_text("删除成功")).not_to_be_visible(timeout=5000)
        self.log_step("验证页面未出现删除成功字样")
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_查询)
        类型管理页面.click_button("搜索")
        self.log_step("输入查询条件")
        # 等待1秒
        类型管理页面.等待表格加载完成()
        删除后的数据量 = 类型管理页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量

    @pytest.mark.parametrize("表单数据_查询", [
        {
            # "类型名称": f"修改-成功{time_string}",
            "类型名称": "该类型下有商铺"
        },
    ])
    def test_delete_fail(self, 类型管理页面, 表单数据_查询):
        # 输入查询条件
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_查询)
        类型管理页面.click_button("搜索")
        self.log_step("输入查询条件")
        类型管理页面.等待表格加载完成()
        删除前的数据量 = 类型管理页面.获取页面统计的总数据量()
        # 点击删除按钮
        类型管理页面.点击表格中某行按钮(行号=1, 按钮名="删除")
        类型管理页面.click_button("确定")
        self.log_step("点击删除按钮,弹窗后点击确定按钮")
        expect(类型管理页面.page.get_by_text("请先移除关联的数据")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现删除失败字样")
        类型管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_查询)
        类型管理页面.click_button("搜索")
        self.log_step("输入查询条件")
        # 等待1秒
        类型管理页面.等待表格加载完成()
        删除后的数据量 = 类型管理页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量

@pytest.mark.usefixtures("前置操作_自动下发和启用禁用")
class TestButton(BaseCase):
    def test_启动自动下发(self, 类型管理页面):
        loc_目标行 = 类型管理页面.获取任务频率和任务处理时效不为空的行()
        # 将该行状态设置为启用
        if 类型管理页面.获取类型状态按钮(loc_目标行).locator("span").inner_html() == "启用":
            类型管理页面.点击类型状态按钮(loc_目标行)
        self.log_step("将该行的类型状态设置为启用")
        # 断言:该开关是可以交互的
        expect(类型管理页面.获取自动下发任务开关(loc_目标行)).to_be_enabled()
        # 若开关已打开,则点击一次,将其关闭
        if "is-checked" in 类型管理页面.获取自动下发任务开关(loc_目标行).get_attribute("class"):
            类型管理页面.点击自动下发任务开关(loc_目标行)
            类型管理页面.page.wait_for_timeout(500)
            expect(类型管理页面.page.get_by_text("修改成功")).not_to_be_visible()
        self.log_step("若自动下发任务开关已经打开,则将其关闭")
        类型管理页面.点击自动下发任务开关(loc_目标行)
        # 断言:出现修改成功字样
        expect(类型管理页面.page.get_by_text("修改成功")).to_be_visible()
        expect(类型管理页面.获取自动下发任务开关(loc_目标行)).to_have_class("el-switch is-checked")
        self.log_step("断言:出现修改成功字样且开关处于开启状态")
        # 还要去检查 网格管理-场所监管巡查-系统下发巡查 页面中 对应类型的商铺是否会按时下发任务,这个逻辑比较复杂,后续完善
        expect(类型管理页面.page.get_by_text("修改成功")).not_to_be_visible()


    def test_关闭自动下发(self, 类型管理页面):
        loc_目标行 = 类型管理页面.获取任务频率和任务处理时效不为空的行()
        # 将该行状态设置为启用
        if 类型管理页面.获取类型状态按钮(loc_目标行).locator("span").inner_html() == "启用":
            类型管理页面.点击类型状态按钮(loc_目标行)
        self.log_step("将该行的类型状态设置为启用")
        # 断言:该开关是可以交互的
        expect(类型管理页面.获取自动下发任务开关(loc_目标行)).to_be_enabled()
        # 若开关已关闭,则点击一次,将其打开
        if "is-checked" not in 类型管理页面.获取自动下发任务开关(loc_目标行).get_attribute("class"):
            类型管理页面.点击自动下发任务开关(loc_目标行)
            类型管理页面.page.wait_for_timeout(500)
            expect(类型管理页面.page.get_by_text("修改成功")).not_to_be_visible()
        self.log_step("若自动下发任务开关已经关闭,则将其打开")
        类型管理页面.点击自动下发任务开关(loc_目标行)
        # 断言:出现修改成功字样
        expect(类型管理页面.page.get_by_text("修改成功")).to_be_visible()
        expect(类型管理页面.获取自动下发任务开关(loc_目标行)).not_to_have_class("el-switch is-checked")
        self.log_step("断言:出现修改成功字样且开关处于关闭状态")
        expect(类型管理页面.page.get_by_text("修改成功")).not_to_be_visible()

        # 还要去检查 网格管理-场所监管巡查-系统下发巡查 页面中 对应类型的商铺不会再按时下发任务,这个逻辑比较复杂,后续完善

    def test_启动自动下发校验(self, 类型管理页面):
        loc_目标行 = 类型管理页面.获取任务频率和任务处理时效为空的行()
        # 将该行状态设置为启用
        if 类型管理页面.获取类型状态按钮(loc_目标行).locator("span").inner_html() == "启用":
            类型管理页面.点击类型状态按钮(loc_目标行)
        self.log_step("将该行的类型状态设置为启用")
        # 断言:该开关是可以交互的
        expect(类型管理页面.获取自动下发任务开关(loc_目标行)).to_be_enabled()
        self.log_step("断言:该开关是可以交互的")
        assert "is-checked" not in 类型管理页面.获取自动下发任务开关(loc_目标行).get_attribute("class")
        self.log_step("断言:该开关一定处于关闭状态")
        类型管理页面.点击自动下发任务开关(loc_目标行)
        # 断言:出现修改失败字样
        expect(类型管理页面.page.get_by_text("请先配置该类型的任务频率和任务处理时效")).to_be_visible()

    def test_禁用类型(self, 类型管理页面):
        loc_目标行 = 类型管理页面.获取任务频率和任务处理时效不为空的行()
        # 将该行状态设置为启用
        if 类型管理页面.获取类型状态按钮(loc_目标行).locator("span").inner_html() == "启用":
            类型管理页面.点击类型状态按钮(loc_目标行)
            类型管理页面.page.wait_for_timeout(500)
            expect(类型管理页面.page.get_by_text("修改成功")).not_to_be_visible()
        self.log_step("将该行的类型状态设置为启用")
        # 点击禁用按钮
        类型管理页面.点击类型状态按钮(loc_目标行)
        self.log_step("点击禁用按钮")
        # 断言:该开关是可以交互的
        expect(类型管理页面.page.get_by_text("修改成功")).to_be_visible()
        expect(类型管理页面.获取自动下发任务开关(loc_目标行)).not_to_be_enabled()
        expect(类型管理页面.获取自动下发任务开关(loc_目标行)).to_have_class("el-switch is-disabled")
        self.log_step("断言:出现了修改成功字样且该开关是变为不可交互状态且开关状态为关闭")
        expect(类型管理页面.page.get_by_text("修改成功")).not_to_be_visible()


    def test_启用类型(self, 类型管理页面):
        loc_目标行 = 类型管理页面.获取任务频率和任务处理时效不为空的行()
        # 将该行状态设置为禁用
        if 类型管理页面.获取类型状态按钮(loc_目标行).locator("span").inner_html() == "禁用":
            类型管理页面.点击类型状态按钮(loc_目标行)
            类型管理页面.page.wait_for_timeout(500)
            expect(类型管理页面.page.get_by_text("修改成功")).not_to_be_visible()
        self.log_step("将该行的类型状态设置为禁用")
        # 点击启用按钮
        类型管理页面.点击类型状态按钮(loc_目标行)
        self.log_step("点击启用按钮")
        # 断言:该开关是可以交互的
        expect(类型管理页面.page.get_by_text("修改成功")).to_be_visible()
        expect(类型管理页面.获取自动下发任务开关(loc_目标行)).to_be_enabled()
        expect(类型管理页面.获取自动下发任务开关(loc_目标行)).to_have_class("el-switch")
        self.log_step("断言:出现了修改成功字样且该开关是变为不可交互状态且开关状态为关闭")
        expect(类型管理页面.page.get_by_text("修改成功")).not_to_be_visible()


