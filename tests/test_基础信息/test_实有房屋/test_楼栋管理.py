"""
此模块使用 Playwright 框架实现会议室管理模块的 UI 自动化测试，
包含增、删、改、查功能的测试用例。
"""
import random
import allure

from base_case import BaseCase

from playwright.sync_api import expect, sync_playwright
import pytest
import logging

from pages.基础信息.实有房屋.楼栋管理 import PageFloor

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="module")
def 随机楼栋号():
    return str(random.randint(1, 99))

@pytest.fixture(scope="function")
def 楼栋管理页面(浏览器已打开的页面):
    # 将页面封装为楼栋管理页面
    page = PageFloor(浏览器已打开的页面)
    yield page


@pytest.mark.usefixtures("楼栋管理页面")  # 显式声明夹具
class TestAdd(BaseCase):

    @pytest.mark.parametrize(
        "小区名称,楼栋号,单元数,楼层数,楼栋名称,经度,纬度",

        [
            ("金城大厦", "11", "9", "4", "新增-成功",
             "117.271140", "31.826378",
             )
            # 添加更多测试数据集
        ],
        # ids=["新增-成功"
        #
        #      ]
    )
    @allure.step("测试新增楼栋-成功")
    def test_add_success(self, 楼栋管理页面,
                         db_connection,
                         小区名称, 楼栋号, 单元数, 楼层数, 楼栋名称, 经度, 纬度
                         ):
        楼栋号 = str(random.randint(1, 99))
        # 统计数据库中的数据条数
        数据量_新增前 = 楼栋管理页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        楼栋管理页面.click_button("新增")
        self.log_step("点击新增按钮")
        # 填写表单信息
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=楼栋管理页面.page.locator('//div[@aria-label="楼栋信息"]'), 小区名称=小区名称, 楼栋号=楼栋号,
            单元数=单元数, 楼层数=楼层数, 楼栋名称=楼栋名称, 经度=经度, 纬度=纬度)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        楼栋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言操作成功字样在页面出现
        expect(楼栋管理页面.page.get_by_text("保存成功")).to_be_visible(timeout=5000)
        self.log_step("验证新增成功-页面提示信息")
        # 等待1秒
        楼栋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 楼栋管理页面.统计数据库表中的记录数(db_connection)
        # 断言新增后数据库表中数据量增加了1
        assert 数据量_新增后 == 数据量_新增前 + 1
        self.log_step("验证新增成功-数据库校验")

    @pytest.mark.parametrize(
        "小区名称,楼栋号,单元数,楼层数,楼栋名称,经度,纬度",

        [
            ("", "11", "9", "4", "A区1号",
             "117.271140", "31.826378",
             ),
            ("金城大厦", "", "9", "4", "A区1号",
             "117.271140", "31.826378",
             ),
            ("金城大厦", "11", "", "4", "A区1号",
             "117.271140", "31.826378",
             ),
            ("金城大厦", "11", "9", "", "A区1号",
             "117.271140", "31.826378",
             )
            # 添加更多测试数据集
        ],
        # ids=[
        #      "新增-失败-必填项为空-会议室名称",
        #      "新增-失败-必填项为空-容纳人数",
        #      "新增-失败-必填项为空-会议室位置",
        #      "新增-失败-必填项为空-会议室状态",
        #      '新增-失败-必填项为空-会议室设备',
        #      '新增-失败-必填项为空-管理部门',
        #      '新增-失败-必填项为空-管理人',
        #      '新增-失败-必填项为空-审批人',
        #      '新增-失败-必填项为空-可预约的时间范围',
        #      '新增-失败-必填项为空-单次可预约最长时间',
        #      ]
    )
    @pytest.mark.usefixtures("后置操作_刷新页面")
    @allure.step("测试新增楼栋-失败-必填项缺失")
    def test_add__miss_data(self, 楼栋管理页面,
                            db_connection,
                            小区名称, 楼栋号, 单元数, 楼层数, 楼栋名称, 经度, 纬度
                            ):
        # 统计数据库中的数据条数
        数据量_新增前 = 楼栋管理页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        楼栋管理页面.点击新增按钮()
        self.log_step("点击新增按钮")
        # 填写表单信息
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=楼栋管理页面.page.locator('//div[@aria-label="楼栋信息"]'), 小区名称=小区名称, 楼栋号=楼栋号,
            单元数=单元数, 楼层数=楼层数, 楼栋名称=楼栋名称, 经度=经度, 纬度=纬度)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        楼栋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言操作成功字样未在页面出现
        expect(楼栋管理页面.page.get_by_text("保存成功")).not_to_be_visible(timeout=5000)
        assert 楼栋管理页面.page.get_by_text("不能为空").count() > 0
        self.log_step("验证新增失败-必填项缺失-页面提示信息")
        # 等待1秒
        楼栋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 楼栋管理页面.统计数据库表中的记录数(db_connection)

        assert 数据量_新增后 == 数据量_新增前
        self.log_step("验证新增失败-必填项缺失-数据库校验")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "小区名称,楼栋号,单元数,楼层数,楼栋名称,经度,纬度",

        [
            ("金城大厦", "1", "9", "4", "A区1号",
             "117.271140", "31.826378",
             ),
            # 添加更多测试数据集
        ],
    )
    @allure.step("测试新增楼栋-失败-去重校验")
    def test_add_repeat_validation(self, 楼栋管理页面,
                                   db_connection,
                                   小区名称, 楼栋号, 单元数, 楼层数, 楼栋名称, 经度, 纬度
                                   ):
        # 统计数据库中的数据条数
        数据量_新增前 = 楼栋管理页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        楼栋管理页面.点击新增按钮()
        self.log_step("点击新增按钮")
        # 填写表单信息
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=楼栋管理页面.page.locator('//div[@aria-label="楼栋信息"]'), 小区名称=小区名称, 楼栋号=楼栋号,
            单元数=单元数, 楼层数=楼层数, 楼栋名称=楼栋名称, 经度=经度, 纬度=纬度)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        楼栋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言该小区已存在字样在页面出现
        expect(楼栋管理页面.page.get_by_text("该楼栋已存在")).to_be_visible(timeout=5000)
        self.log_step("验证新增失败-去重校验-页面提示信息")
        # 等待1秒
        楼栋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 楼栋管理页面.统计数据库表中的记录数(db_connection)

        assert 数据量_新增后 == 数据量_新增前
        self.log_step("验证新增失败-去重校验-数据库校验")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @allure.step("测试新增楼栋-前端格式校验与数据合法性")
    def test_add_frontend_validation(
            self, 楼栋管理页面, db_connection,
    ):
        楼栋管理页面.click_button("新增")
        self.log_step("点击新增按钮")

        # 输入楼栋号
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼栋号="0")
        self.log_step("填写楼栋号")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-楼栋号")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼栋号="-1")
        self.log_step("填写楼栋号")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-楼栋号")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼栋号="0.5")
        self.log_step("填写楼栋号")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-楼栋号")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼栋号="1/2")
        self.log_step("填写楼栋号")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-楼栋号")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼栋号="100")
        self.log_step("填写楼栋号")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-楼栋号")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼栋号="abc")
        self.log_step("填写楼栋号")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-楼栋号")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼栋号="@")
        self.log_step("填写楼栋号")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-楼栋号")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼栋号="001")
        self.log_step("填写楼栋号")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-楼栋号")

        # 输入单元数
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    单元数="0")
        self.log_step("填写单元数")
        expect(楼栋管理页面.page.get_by_text("请输入10以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-单元数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    单元数="-1")
        self.log_step("填写单元数")
        expect(楼栋管理页面.page.get_by_text("请输入10以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-单元数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    单元数="10.1")
        self.log_step("填写单元数")
        expect(楼栋管理页面.page.get_by_text("请输入10以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-单元数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    单元数="a")
        self.log_step("填写单元数")
        expect(楼栋管理页面.page.get_by_text("请输入10以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-单元数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    单元数="@")
        self.log_step("填写单元数")
        expect(楼栋管理页面.page.get_by_text("请输入10以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-单元数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    单元数="1,0")
        self.log_step("填写单元数")
        expect(楼栋管理页面.page.get_by_text("请输入10以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-单元数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    单元数="1/2")
        self.log_step("填写单元数")
        expect(楼栋管理页面.page.get_by_text("请输入10以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-单元数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    单元数="十")
        self.log_step("填写单元数")
        expect(楼栋管理页面.page.get_by_text("请输入10以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-单元数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    单元数="10.1e1")
        self.log_step("填写单元数")
        expect(楼栋管理页面.page.get_by_text("请输入10以内的正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-单元数")

        # 输入楼层数
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼层数="0")
        self.log_step("填写楼层数")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(2)
        self.log_step("断言页面提示信息-楼层数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼层数="-1")
        self.log_step("填写楼层数")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(2)
        self.log_step("断言页面提示信息-楼层数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼层数="0.5")
        self.log_step("填写楼层数")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(2)
        self.log_step("断言页面提示信息-楼层数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼层数="1/2")
        self.log_step("填写楼层数")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(2)
        self.log_step("断言页面提示信息-楼层数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼层数="100")
        self.log_step("填写楼层数")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(2)
        self.log_step("断言页面提示信息-楼层数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼层数="abc")
        self.log_step("填写楼层数")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(2)
        self.log_step("断言页面提示信息-楼层数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼层数="@")
        self.log_step("填写楼层数")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(2)
        self.log_step("断言页面提示信息-楼层数")

        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=楼栋管理页面.定位器_新增表单(),
                                                                    楼层数="001")
        self.log_step("填写楼层数")
        expect(楼栋管理页面.page.get_by_text("请输入1-99以内的正整数")).to_have_count(2)
        self.log_step("断言页面提示信息-楼层数")


@pytest.mark.usefixtures("楼栋管理页面")  # 显式声明夹具
class TestEdit(BaseCase):
    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "楼栋名称_待修改记录, 单元数, 楼层数, 楼栋名称, 经度, 纬度",

        [
            ("新增-成功", "9", "4", "修改-成功",
             "117.271140", "31.826378")
            # 添加更多测试数据集
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试修改小区")
    def test_edit_success(self, 楼栋管理页面,
                            db_connection,
                            楼栋名称_待修改记录, 单元数, 楼层数, 楼栋名称, 经度, 纬度):
        # 输入查询条件
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(选择小区=None, 楼栋号=None, 楼栋名称=楼栋名称_待修改记录)
        self.log_step("输入查询条件")
        # 点击查询按钮
        楼栋管理页面.click_button("搜索")
        # 点击编辑按钮
        楼栋管理页面.点击编辑按钮(楼栋名称_待修改记录)
        self.log_step("点击编辑按钮")
        楼栋管理页面.验证编辑表单的可交互性()
        # 填写表单信息
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=楼栋管理页面.page.locator('//div[@aria-label="楼栋信息"]'), 单元数=单元数, 楼层数=楼层数, 楼栋名称=楼栋名称, 经度=经度, 纬度=纬度)

        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        楼栋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 点击提示弹窗中的确定按钮
        楼栋管理页面.点击提示弹窗中的确定按钮()
        # 断言操作成功字样在页面出现
        expect(楼栋管理页面.page.get_by_text("保存成功!")).to_be_visible(timeout=5000)
        self.log_step("验证修改成功-页面提示信息")
        # 等待1秒
        楼栋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 执行sql查询，断言一定能查到修改后的数据
        db_data = 楼栋管理页面.get_db_data(db_connection,"SELECT count(*) as count FROM ybds_building where ldmc = %(楼栋名称)s",
                                                                   {"楼栋名称": 楼栋名称})
        count = db_data[0]["count"]
        assert count > 0
        self.log_step("验证修改成功-数据库")
        # 输入查询条件
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(选择小区=None, 楼栋号=None,
                                                                    楼栋名称=楼栋名称)
        self.log_step("输入查询条件")
        # 点击查询按钮
        楼栋管理页面.click_button("搜索")
        楼栋管理页面.点击编辑按钮(楼栋名称)
        楼栋管理页面.校验表单中数据成功修改(楼栋管理页面.获取楼栋信息表单(), 单元数=单元数, 楼层数=楼层数, 楼栋名称=楼栋名称, 经度=经度, 纬度=纬度)

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "单元数, 楼层数, 楼栋名称, 经度, 纬度",

        [
            ("1", None, None,
             "117.271140", "31.826378")
            # 添加更多测试数据集
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试修改小区-失败-该楼栋+单元+楼层下有房屋,不允许改小单元号")
    def test_edit_fail_decrease_unit(self, 楼栋管理页面,
                            db_connection,
                             单元数, 楼层数, 楼栋名称, 经度, 纬度):
        # 输入查询条件，找到其下已存在房屋的楼栋
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(选择小区="中电数智街道/中电数智社区/金城大厦", 楼栋号="1", 楼栋名称="修改-失败-不允许改小")
        self.log_step("输入查询条件")
        # 点击查询按钮
        楼栋管理页面.click_button("搜索")
        # 点击编辑按钮
        楼栋管理页面.点击编辑按钮("修改-失败-不允许改小")
        self.log_step("点击编辑按钮")
        # 填写表单信息
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=楼栋管理页面.page.locator('//div[@aria-label="楼栋信息"]'), 单元数=单元数, 楼层数=楼层数, 楼栋名称=楼栋名称, 经度=经度, 纬度=纬度)

        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        楼栋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 点击提示弹窗中的确定按钮
        楼栋管理页面.点击提示弹窗中的确定按钮()
        # 断言操作成功字样在页面出现
        expect(楼栋管理页面.page.get_by_text("楼栋单元数不允许比现有单元数小")).to_be_visible(timeout=5000)
        self.log_step("验证修改失败-页面提示信息")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "单元数, 楼层数, 楼栋名称, 经度, 纬度",

        [
            (None, "1", None,
             "117.271140", "31.826378")
            # 添加更多测试数据集
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试修改小区-失败-该楼栋+单元+楼层下有房屋,不允许改小楼层数")
    def test_edit_fail_decrease_floor(self, 楼栋管理页面,
                                     db_connection,
                                     单元数, 楼层数, 楼栋名称, 经度, 纬度):
        # 输入查询条件，找到其下已存在房屋的楼栋
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            选择小区="中电数智街道/中电数智社区/金城大厦", 楼栋号="1", 楼栋名称="修改-失败-不允许改小")
        self.log_step("输入查询条件")
        # 点击查询按钮
        楼栋管理页面.click_button("搜索")
        # 点击编辑按钮
        楼栋管理页面.点击编辑按钮("修改-失败-不允许改小")
        self.log_step("点击编辑按钮")
        # 填写表单信息
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=楼栋管理页面.page.locator('//div[@aria-label="楼栋信息"]'), 单元数=单元数, 楼层数=楼层数,
            楼栋名称=楼栋名称, 经度=经度, 纬度=纬度)

        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        楼栋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 点击提示弹窗中的确定按钮
        楼栋管理页面.点击提示弹窗中的确定按钮()
        # 断言操作成功字样在页面出现
        expect(楼栋管理页面.page.get_by_text("楼栋楼层数不允许比现有楼层数小")).to_be_visible(timeout=2000)
        self.log_step("验证修改失败-页面提示信息")

def build_query_sql(选择小区=None, 楼栋号=None, 楼栋名称=None):
    """
    根据给定参数动态生成小区查询 SQL。
    """
    sql = """select b.xqmc, y.* from base_village as b inner join ybds_building as y on b.xqbm = y.xqbm where 1=1 AND y.xqbm IN ( '340103225001001' , '340103225001002' , '340103225001111' , '340103225001223' , '2010005425' , '340103225002002' , '340103225003001' , '340103225001012' , '340103225002213' , '340103225003198' , '340103225003188' )"""

    # 存放动态条件列表和参数字典
    conditions = []
    params = {}

    if 选择小区 is not None:
        # 根据/来分割选择小区，获取最后一级小区名称
        选择小区 = 选择小区.split('/')[-1]

        # 添加选择小区条件
        conditions.append(f"and BINARY b.xqmc = %(选择小区)s")
        # 添加参数
        params["选择小区"] = f"{选择小区}"

    if 楼栋号 is not None:
        conditions.append("and y.ldh like CONCAT('%%', %(楼栋号)s,'%%' )")
        params["楼栋号"] = f"{楼栋号}"

    if 楼栋名称 is not None:
        conditions.append("and y.ldmc like CONCAT('%%', %(楼栋名称)s,'%%' )")
        params["楼栋名称"] = f"{楼栋名称}"

    # 拼接sql
    sql += " " + " ".join(conditions)
    sql += ' ORDER BY y.ldh+0'
    return sql, params


class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "选择小区, 楼栋号, 楼栋名称",
        [
            (None, None, None),
            ("中电数智街道/中电数智社区/金城大厦", None, None),
            (None, "1", None),
            (None, None, "1栋"),
            ("中电数智街道/中电数智社区/金城大厦", "1", None),
            ("中电数智街道/中电数智社区/金城大厦", None, "1栋"),
            (None, "1", "1栋"),
            ("中电数智街道/中电数智社区/金城大厦", "1", "1栋"),
        ]
    )
    def test_query(self, 楼栋管理页面, db_connection, 选择小区, 楼栋号, 楼栋名称):
        # 输入查询条件
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(选择小区=选择小区, 楼栋号=楼栋号,
                                                                    楼栋名称=楼栋名称)
        self.log_step("输入查询条件")

        # 点击查询按钮
        楼栋管理页面.click_button("搜索")
        self.log_step("点击查询按钮")
        # 等待查询结果加载
        楼栋管理页面.page.wait_for_timeout(1000)  # 等待
        self.log_step("等待查询结果加载")
        pages_data, pages_data_count = 楼栋管理页面.get_table_data()
        # print(pages_data)
        self.log_step("获取所有页面的表格数据")

        # 构建 SQL 查询
        sql, params = build_query_sql(选择小区=选择小区, 楼栋号=楼栋号, 楼栋名称=楼栋名称)

        # 根据sql语句和参数，从数据库中提取数据
        db_data = 楼栋管理页面.get_db_data(db_connection, query=sql, params=params)
        self.log_step("从数据库中提取数据")

        # 比较两个数据集
        assert 楼栋管理页面.compare_data(pages_data, db_data,
                                         ['xqmc', 'ldh', 'ldmc', 'lcs', 'dys' ]), "页面数据与数据库数据不一致"
        self.log_step("比较两个数据集")


class TestReset(BaseCase):
    def test_reset(self, 楼栋管理页面, db_connection):
        # 输入查询条件
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(选择小区="中电数智街道/中电数智社区/金城大厦", 楼栋号="1",
                                                                    楼栋名称="1栋")
        self.log_step("输入查询条件")
        # 点击查询按钮
        楼栋管理页面.click_button("搜索")
        self.log_step("点击查询按钮")
        # 等待查询结果加载
        楼栋管理页面.page.wait_for_timeout(1000)  # 等待
        self.log_step("等待查询结果加载")
        # 点击重置按钮
        楼栋管理页面.click_reset_btn()
        # 等待查询结果加载
        楼栋管理页面.page.wait_for_timeout(1000)  # 等待

        楼栋管理页面.验证搜索框内容被重置()

        pages_data, pages_data_count = 楼栋管理页面.get_table_data()
        # print(pages_data)
        self.log_step("获取所有页面的表格数据")

        # 构建 SQL 查询
        sql, params = build_query_sql(选择小区=None, 楼栋号=None,楼栋名称=None)


        # 根据sql语句和参数，从数据库中提取数据
        db_data = 楼栋管理页面.get_db_data(db_connection, query=sql, params=params)
        self.log_step("从数据库中提取数据")

        # 比较两个数据集
        assert 楼栋管理页面.compare_data(pages_data, db_data,
                                         ['xqmc', 'ldh', 'ldmc', 'lcs', 'dys']), "页面数据与数据库数据不一致"
        self.log_step("比较两个数据集")

sql_查询楼栋表记录数 = "SELECT count(*) as count FROM ybds_building"

@pytest.mark.usefixtures("后置操作_重置查询条件")
class TestDelete(BaseCase):
    @pytest.mark.parametrize("楼栋名称_待删除", [
        "修改-成功"
    ])
    def test_delete_success(self, 楼栋管理页面, db_connection, 楼栋名称_待删除):
        # 从数据库中统计状态为删除的数据条数
        数据库中数据量_删除前 = 楼栋管理页面.get_db_data(
            db_connection,
            query=sql_查询楼栋表记录数,
        )
        数据库中数据量_删除前 = 数据库中数据量_删除前[0]["count"]
        # 查找待删除的记录
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(楼栋名称=楼栋名称_待删除)

        楼栋管理页面.click_button("搜索")
        _, 表格中数据量_删除前 = 楼栋管理页面.get_table_data()
        self.log_step("统计删除操作前表格行数")
        楼栋管理页面.点击删除按钮(楼栋名称_待删除)
        楼栋管理页面.click_button("确定")
        self.log_step("点击删除按钮,弹窗后点击确定按钮")
        expect(楼栋管理页面.page.get_by_text("删除成功")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现删除成功字样")
        # 等待1秒
        楼栋管理页面.page.wait_for_timeout(1000)
        _, 表格中数据量_删除后 = 楼栋管理页面.get_table_data()
        self.log_step("统计删除成功操作后表格行数")
        # 断言：表格中的行数减1
        assert 表格中数据量_删除后 == 表格中数据量_删除前 - 1, "表格中的行数未减少"
        # 验证数据库中的数据是否已删除（或标记为已删除）
        db_connection.ping(reconnect=True)  # 确保数据库连接有效
        db_connection.commit()
        数据库中数据量_删除后 = 楼栋管理页面.get_db_data(
            db_connection,
            query=sql_查询楼栋表记录数,
        )
        数据库中数据量_删除后 = 数据库中数据量_删除后[0]["count"]
        # 断言：数据库中状态为已删除的数据多了1条
        assert 数据库中数据量_删除后 == 数据库中数据量_删除前 - 1, "数据库中的数据未删除"
        self.log_step("验证数据库中的数据是否已删除")

    @pytest.mark.parametrize("楼栋名称_待删除", [
        "1栋"
    ])
    def test_delete_cancel(self, 楼栋管理页面, db_connection, 楼栋名称_待删除):
        # 从数据库中统计状态为删除的数据条数
        数据库中数据量_删除前 = 楼栋管理页面.get_db_data(
            db_connection,
            query=sql_查询楼栋表记录数,
        )
        数据库中数据量_删除前 = 数据库中数据量_删除前[0]["count"]
        # 查找待删除的记录
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(楼栋名称=楼栋名称_待删除)

        楼栋管理页面.click_button("搜索")
        _, 表格中数据量_删除前 = 楼栋管理页面.get_table_data()
        self.log_step("统计删除操作前表格行数")
        楼栋管理页面.点击删除按钮(楼栋名称_待删除)
        楼栋管理页面.click_button("取消")
        self.log_step("点击删除按钮,弹窗后点击取消按钮")
        expect(楼栋管理页面.page.get_by_text("删除成功")).not_to_be_visible(timeout=5000)
        self.log_step("验证页面未出现删除成功字样")
        # 等待1秒
        楼栋管理页面.page.wait_for_timeout(1000)
        _, 表格中数据量_删除后 = 楼栋管理页面.get_table_data()
        self.log_step("统计删除取消操作后表格行数")
        # 断言：表格中的行数减1
        assert 表格中数据量_删除后 == 表格中数据量_删除前, "表格中的行数减少了"
        # 验证数据库中的数据是否已删除（或标记为已删除）
        db_connection.ping(reconnect=True)  # 确保数据库连接有效
        db_connection.commit()
        数据库中数据量_删除后 = 楼栋管理页面.get_db_data(
            db_connection,
            query=sql_查询楼栋表记录数,
        )
        数据库中数据量_删除后 = 数据库中数据量_删除后[0]["count"]
        # 断言：数据库中状态为已删除的数据不变
        assert 数据库中数据量_删除后 == 数据库中数据量_删除前, "数据库中的数据被删除了"
        self.log_step("验证数据库中的数据是否已删除")

    @pytest.mark.parametrize("楼栋名称_待删除", [
        "修改-失败"
    ])
    def test_delete_fail(self, 楼栋管理页面, db_connection, 楼栋名称_待删除):
        # 从数据库中统计状态为删除的数据条数
        数据库中数据量_删除前 = 楼栋管理页面.get_db_data(
            db_connection,
            query=sql_查询楼栋表记录数,
        )
        数据库中数据量_删除前 = 数据库中数据量_删除前[0]["count"]
        # 查找待删除的记录
        楼栋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(楼栋名称=楼栋名称_待删除)

        楼栋管理页面.click_button("搜索")
        _, 表格中数据量_删除前 = 楼栋管理页面.get_table_data()
        self.log_step("统计删除操作前表格行数")
        楼栋管理页面.点击删除按钮(楼栋名称_待删除)
        楼栋管理页面.click_button("确定")
        self.log_step("点击删除按钮,弹窗后点击确定按钮")
        expect(楼栋管理页面.page.get_by_text("所选楼栋里还存在房屋数据，不允许删除")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现不允许删除字样")
        # 等待1秒
        楼栋管理页面.page.wait_for_timeout(1000)
        _, 表格中数据量_删除后 = 楼栋管理页面.get_table_data()
        self.log_step("统计删除操作后表格行数")
        # 断言：表格中的行数不变
        assert 表格中数据量_删除后 == 表格中数据量_删除前, "表格中的行数减少了"
        # 验证数据库中的数据是否已删除（或标记为已删除）
        db_connection.ping(reconnect=True)  # 确保数据库连接有效
        db_connection.commit()
        数据库中数据量_删除后 = 楼栋管理页面.get_db_data(
            db_connection,
            query=sql_查询楼栋表记录数,
        )
        数据库中数据量_删除后 = 数据库中数据量_删除后[0]["count"]
        # 断言：数据库中数据量不变
        assert 数据库中数据量_删除后 == 数据库中数据量_删除前, "数据库中的数据删除了"
        self.log_step("验证数据库中的数据是否已删除")
