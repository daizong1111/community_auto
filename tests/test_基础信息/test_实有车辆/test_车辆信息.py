"""
此模块使用 Playwright 框架实现会议室管理模块的 UI 自动化测试，
包含增、删、改、查功能的测试用例。
"""
import random
import time

import allure

# 生成随机身份证号码和手机号码，防止数据重复
from faker import Faker

fake = Faker('zh_CN')

from playwright.sync_api import expect
from base_case import BaseCase
import pytest
import logging

from pages.基础信息.实有车辆.车辆信息 import PageCarInfo

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# fake生成随机车牌号
随机车牌号 = f"苏A{str(random.randint(10000,99999))}"
车牌号_修改后 = f"苏A{str(random.randint(10000,99999))}"


@pytest.fixture(scope="module")
def 车辆信息页面(浏览器已打开的页面):
    # 将页面封装为车辆信息页面
    page = PageCarInfo(浏览器已打开的页面)
    yield page


# 定义一个模块级变量，用于标记是否新增成功
NEW_PERSON_ADDED = False


@pytest.mark.usefixtures("车辆信息页面")
class TestAdd(BaseCase):
    @pytest.mark.parametrize(
        "表单数据",

        [
            {"车牌号码": 随机车牌号, "小区名称": "中电数智街道/中电数智社区/小区99", "车主姓名": fake.name(),
             "手机号码": fake.phone_number(), "身份证号码": fake.ssn(),
             "车辆品牌": "奥迪", "车辆类型": "小型客车", "车身颜色": "白",
             "号牌类型": "挂车号牌", "号牌颜色": "白", "备注": "这辆车很贵",
             },
            # {"车牌号码": 随机车牌号, "小区名称": "中电数智街道/中电数智社区/小区99", "车主姓名": fake.name(),
            #  "手机号码": fake.phone_number(), "身份证号码": fake.ssn(),
            #  "车辆品牌": "奥迪", "车辆类型": "小型客车", "车身颜色": "白",
            #  "号牌类型": "挂车号牌", "号牌颜色": "白", "备注":"小区环境宜人，绿化覆盖率高，四季皆有景。内部设有儿童游乐区、健身角，方便居民休闲活动。物业服务响应及时，保洁到位，安保巡逻频繁，让人住得安心。邻里关系和谐，常有社区活动增进感情。停车管理有序，虽有高峰时段紧张，但总体尚可。周边配套齐全，超市、餐厅、学校、医院均在步行范围内。交通便捷，多条公交线路经过，离地铁站也不远。房屋多为中高层，采光良好。唯一不足是部分楼栋间存在视野遮挡。总体而言，是一个适宜居住、生活便利的成熟社区。"
            #  },

            # 添加更多测试数据集
        ],
        # ids=["新增-成功"
        #
        #      ]
    )
    @allure.step("测试新增人员-成功")
    def test_add_success(self, 车辆信息页面,
                         db_connection, 表单数据: dict
                         ):
        global NEW_PERSON_ADDED
        try:
            车辆信息页面.click_button("新增")
            self.log_step("点击新增按钮")

            车辆信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据)
            self.log_step("填写表单信息")

            车辆信息页面.click_button("确定")
            self.log_step("点击提交按钮")

            expect(车辆信息页面.page.get_by_text("提交成功")).to_be_visible(timeout=5000)
            self.log_step("验证新增成功-页面提示信息")

            车辆信息页面.填写搜索框({"车牌号": 表单数据.get("车牌号码")})
            要寻找的车牌号 = 表单数据.get("车牌号码")[0:3] + "***" + 表单数据.get("车牌号码")[-1:]
            要寻找的手机号 = 表单数据.get("手机号码")[0:3] + "****" + 表单数据.get("手机号码")[-4:]
            要寻找的身份证号 = 表单数据.get("身份证号码")[0:4] + "****"

            loc_新增的行 = 车辆信息页面.get_table_rows().filter(has_text=要寻找的车牌号).filter(has_text=要寻找的手机号).filter(has_text=要寻找的身份证号).first

            # 检查表格中是否有新增的数据
            expect(loc_新增的行).to_be_visible()

            # 标记新增成功
            NEW_PERSON_ADDED = True
        except Exception as e:
            raise e

    # @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "表单数据",

        [
            {"车牌号码": "苏A88888", "小区名称": "中电数智街道/中电数智社区/小区99", "车主姓名": fake.name(),
             "手机号码": fake.phone_number(), "身份证号码": fake.ssn(),
             "车辆品牌": "奥迪", "车辆类型": "小型客车", "车身颜色": "白",
             "号牌类型": "挂车号牌", "号牌颜色": "白", "备注": "这辆车很贵",
             },

        ]
    )
    @allure.step("测试新增车辆-失败-去重校验：同一小区下不能有重复车牌号")
    def test_add_repeat_validation(self, 车辆信息页面,
                                   db_connection, 表单数据: dict
                                   ):
        # 点击新增按钮
        车辆信息页面.click_button("新增")
        self.log_step("点击新增按钮")
        # 填写表单信息
        车辆信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据)
        self.log_step("填写表单信息")
        # 点击提交按钮
        车辆信息页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言该人员已存在字样在页面出现
        车辆信息页面.验证页面顶部出现全局提示("已录入该车牌")
        self.log_step("验证新增失败-去重校验-页面提示信息")
        # 刷新页面
        车辆信息页面.page.reload()

        # 检查表格中是否有新增的数据
        车辆信息页面.填写搜索框({"选择小区":表单数据.get("小区名称"),"车牌号": 表单数据.get("车牌号码")})

        # 检查表格中是否有新增的数据
        expect(车辆信息页面.get_table_rows()).to_have_count(1)
        self.log_step("验证查询列表中无新增的数据")

@pytest.mark.usefixtures("车辆信息页面")  # 显式声明夹具
class TestEdit(BaseCase):
    def setup_class(self):
        if not NEW_PERSON_ADDED:
            pytest.skip("新增用例执行失败，跳过修改相关测试")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "待修改的车牌号, 表单数据",
        [
            (
                    随机车牌号,
                    { "车主姓名": fake.name(),
                     "手机号码": fake.phone_number(), "身份证号码": fake.ssn(),
                     "车辆品牌": "安凯客车", "车辆类型": "中型货车", "车身颜色": "蓝",
                     "号牌类型": "小型汽车号牌", "号牌颜色": "绿", "备注": "这辆车很便宜",
                     }
            ),
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试修改小区")
    def test_edit_success(self, 车辆信息页面, 待修改的车牌号, 表单数据: dict):

        # 输入查询条件
        车辆信息页面.填写搜索框({"车牌号": 待修改的车牌号})
        # 点击编辑按钮
        车辆信息页面.点击编辑按钮(None)
        self.log_step("点击编辑按钮")
        # 填写表单信息
        车辆信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            **表单数据)
        self.log_step("填写表单信息")
        # 点击提交按钮
        车辆信息页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 点击提示弹窗中的确定按钮
        车辆信息页面.点击提示弹窗中的确定按钮()
        # 断言操作成功字样在页面出现
        expect(车辆信息页面.page.get_by_text("提交成功")).to_be_visible(timeout=5000)
        self.log_step("验证修改成功-页面提示信息")
        车辆信息页面.填写搜索框({"车牌号": 待修改的车牌号})
        # 等待1秒
        车辆信息页面.page.wait_for_timeout(1000)
        # 检查表格中数据是否成功修改
        车辆信息页面.点击编辑按钮(None)
        车辆信息页面.校验表单中数据成功修改(必填表单项="车主姓名",车辆品牌=表单数据.get("车辆品牌"),车辆类型=表单数据.get("车辆类型"),车身颜色=表单数据.get("车身颜色"),
                                            号牌类型=表单数据.get("号牌类型"),号牌颜色=表单数据.get("号牌颜色"),备注=表单数据.get("备注")
                                            )

class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "表单数据",
        [
            {"选择小区": "中电数智街道/中电数智社区/小区99"},
            {"车牌号": "苏A88888"},
            {"车主姓名": "石岱宗"},
            {"手机号": "15655426823"},
            {"证件号码": "340421199711170020"},
            {"选择小区": "中电数智街道/中电数智社区/小区99", "车牌号": "苏C82312", "车主姓名": "石岱宗", "手机号": "13865546155", "证件号码": "340421199711170020"},

        ]
    )
    def test_query(self, 车辆信息页面, 表单数据: dict):
        # 输入查询条件
        车辆信息页面.填写搜索框(表单数据)

        # 定义字段与验证逻辑的映射
        def verify_小区名称():
            列表_小区名称 = 车辆信息页面.get_column_values_by_name("所属小区")
            小区名称_预期值 = 表单数据["选择小区"].split("/")[-1]

            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(小区名称_预期值 == 小区名称 for 小区名称 in
                       列表_小区名称), f"查询条件-小区名称:{小区名称_预期值}, 表格中的小区名称为:{列表_小区名称}"

        def verify_车牌号():
            列表_车牌号 = 车辆信息页面.get_column_values_by_name("车牌号")
            车牌号_预期值 = 表单数据["车牌号"][0:3] + "***" + 表单数据["车牌号"][-1]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(
                车牌号_预期值 == 车牌号 for 车牌号 in 列表_车牌号), f"查询条件-车牌号:{车牌号_预期值}, 表格中的车牌号为:{列表_车牌号}"

        def verify_车主姓名():
            列表_车主姓名 = 车辆信息页面.get_column_values_by_name("车主姓名")
            车主姓名_预期值_姓氏 = 表单数据["车主姓名"][0]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(车主姓名_预期值_姓氏 == 车主姓名[0] for 车主姓名 in 列表_车主姓名), f"查询条件-车主姓名的姓氏:{车主姓名_预期值_姓氏}, 表格中的车主姓名为:{列表_车主姓名}"


        def verify_手机号():
            列表_手机号 = 车辆信息页面.get_column_values_by_name("联系电话")
            手机号_预期值 = 表单数据["手机号"][0:3] + "****" + 表单数据["手机号"][-4:]
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(手机号_预期值 == 手机号 for 手机号 in
                       列表_手机号), f"查询条件-手机号:{手机号_预期值}, 表格中的手机号为:{列表_手机号}"

        def verify_证件号码():
            列表_证件号码 = 车辆信息页面.get_column_values_by_name("身份证号码")
            证件号码_预期值_开头 = 表单数据["证件号码"][0:4] + "****"
            # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
            assert all(证件号码_预期值_开头 in 证件号码 for 证件号码 in
                       列表_证件号码), f"查询条件-证件号码的开头:{证件号码_预期值_开头}, 表格中的证件号码为:{列表_证件号码}"

        # 字典映射字段到验证函数
        验证规则 = {
            "选择小区": verify_小区名称,
            "车主姓名": verify_车主姓名,
            "车牌号": verify_车牌号,
            "手机号": verify_手机号,
            "证件号码": verify_证件号码
        }

        # 执行匹配的验证规则
        for field in 表单数据:
            if field in 验证规则:
                验证规则[field]()
        self.log_step("检验表格中数据是否满足查询条件")


class TestReset(BaseCase):
    def test_reset(self, 车辆信息页面):
        # 输入查询条件
        车辆信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(**{"选择小区": "中电数智街道/中电数智社区/小区99", "车牌号": "苏C82312", "车主姓名": "石岱宗", "手机号": "13865546155", "证件号码": "340421199711170020"})
        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        车辆信息页面.click_button("重置")

        车辆信息页面.校验表单中数据成功修改(**{"选择小区": "", "车牌号": "", "车主姓名": "", "手机号": "", "证件号码": ""})


@pytest.mark.usefixtures("后置操作_重置查询条件")
class TestDelete(BaseCase):
    def setup_class(self):
        if not NEW_PERSON_ADDED:
            pytest.skip("新增用例执行失败，跳过删除相关测试")

    @pytest.mark.parametrize(
        "待删除的车牌号",
        [
            # "苏A35786"
            f"{随机车牌号}"
        ]
    )
    def test_delete_success(self, 车辆信息页面, 待删除的车牌号):
        # 查找待删除的记录
        # 输入查询条件
        车辆信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(车牌号=待删除的车牌号)
        车辆信息页面.click_button("搜索")
        self.log_step("输入查询条件")
        删除前的数据量 = 车辆信息页面.获取页面统计的总数据量()
        # 点击删除按钮
        车辆信息页面.点击删除按钮(None)
        车辆信息页面.click_button("确定")
        self.log_step("点击删除按钮,弹窗后点击确定按钮")
        expect(车辆信息页面.page.get_by_text("删除成功")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现删除成功字样")
        # 等待1秒
        车辆信息页面.page.wait_for_timeout(1000)
        车辆信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(车牌号=待删除的车牌号)
        车辆信息页面.click_button("搜索")
        self.log_step("输入查询条件")
        # 等待1秒
        车辆信息页面.page.wait_for_timeout(1000)
        删除后的数据量 = 车辆信息页面.获取页面统计的总数据量()
        # 断言
        assert 删除后的数据量 == 删除前的数据量 - 1
        # expect(车辆信息页面.get_table_rows()).to_have_count(0)

    @pytest.mark.parametrize("待删除的车牌号", [
        "苏C82312"
    ])
    def test_delete_cancel(self, 车辆信息页面, 待删除的车牌号):
        # 输入查询条件
        车辆信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(车牌号=待删除的车牌号)
        车辆信息页面.click_button("搜索")
        self.log_step("输入查询条件")
        删除前的数据量 = 车辆信息页面.获取页面统计的总数据量()
        # 点击删除按钮
        车辆信息页面.点击删除按钮(None)
        车辆信息页面.click_button("取消")
        self.log_step("点击删除按钮,弹窗后点击取消按钮")
        expect(车辆信息页面.page.get_by_text("删除成功")).not_to_be_visible(timeout=5000)
        self.log_step("验证页面未出现删除成功字样")
        # 等待1秒
        车辆信息页面.page.wait_for_timeout(1000)
        车辆信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(车牌号=待删除的车牌号)
        车辆信息页面.click_button("搜索")
        self.log_step("输入查询条件")
        # 等待1秒
        车辆信息页面.page.wait_for_timeout(1000)
        删除后的数据量 = 车辆信息页面.获取页面统计的总数据量()
        assert 删除后的数据量 == 删除前的数据量
