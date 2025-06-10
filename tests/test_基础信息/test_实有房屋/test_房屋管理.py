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

from pages.基础信息.实有房屋.房屋管理 import PageHouse

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.fixture(scope="module")
def 随机门牌号():
    return str(random.randint(1, 9999))


@pytest.fixture(scope="module")
def 修改后的门牌号(随机门牌号):
    return str(int(随机门牌号) + 1)


@pytest.fixture(scope="function")
def 房屋管理页面(浏览器已打开的页面):
    # 将页面封装为房屋管理页面
    page = PageHouse(浏览器已打开的页面)
    yield page


@pytest.mark.usefixtures("房屋管理页面")  # 显式声明夹具
class TestAdd(BaseCase):

    @pytest.mark.parametrize(
        "所属小区,楼栋名称,所属单元,门牌号,房屋状态,楼层数,房屋用途,房屋产权性质,房屋面积,备注,房屋照片",

        [
            # ("天王巷小区", "官塘新村", "1单元", "102", "自住",
            #  "1层", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
            #  ),
            ("天王巷小区", "官塘新村", "1单元", "102", "自住",
             "1层", "住宅", "国有房产", "100",
             "小区环境宜人，绿化覆盖率高，四季皆有景。内部设有儿童游乐区、健身角，方便居民休闲活动。物业服务响应及时，保洁到位，安保巡逻频繁，让人住得安心。邻里关系和谐，常有社区活动增进感情。停车管理有序，虽有高峰时段紧张，但总体尚可。周边配套齐全，超市、餐厅、学校、医院均在步行范围内。交通便捷，多条公交线路经过，离地铁站也不远。房屋多为中高层，采光良好。唯一不足是部分楼栋间存在视野遮挡。总体而言，是一个适宜居住、生活便利的成熟社区。",
             r"C:\Users\Administrator\Pictures\111.png"
             )
            # 添加更多测试数据集
        ],
        # ids=["新增-成功"
        #
        #      ]
    )
    @allure.step("测试新增房屋-成功")
    def test_add_success(self, 房屋管理页面,
                         db_connection, 随机门牌号,
                         所属小区, 楼栋名称, 所属单元, 门牌号, 房屋状态, 楼层数, 房屋用途, 房屋产权性质, 房屋面积, 备注,
                         房屋照片
                         ):
        # 统计数据库中的数据条数
        数据量_新增前 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        房屋管理页面.click_button("新增")
        self.log_step("点击新增按钮")
        # 填写表单信息
        门牌号 = 随机门牌号
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=房屋管理页面.定位器_新增表单(), 所属小区=所属小区, 楼栋名称=楼栋名称, 所属单元=所属单元,
            门牌号=门牌号, 房屋状态=房屋状态, 楼层数=楼层数, 房屋用途=房屋用途, 房屋产权性质=房屋产权性质,
            房屋面积=房屋面积, 备注=备注,
            房屋照片=房屋照片)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        房屋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言操作成功字样在页面出现
        expect(房屋管理页面.page.get_by_text("保存成功")).to_be_visible(timeout=5000)
        self.log_step("验证新增成功-页面提示信息")
        # 等待1秒
        房屋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 断言新增后数据库表中数据量增加了1
        assert 数据量_新增后 == 数据量_新增前 + 1, f"新增失败，数据库中数据量没有增加，新增前的数据量为{数据量_新增前}，新增后的数据量为{数据量_新增后}"
        self.log_step("验证新增成功-数据库校验")

    @pytest.mark.parametrize(
        "所属小区,楼栋名称,所属单元,门牌号,房屋状态,楼层数,房屋用途,房屋产权性质,房屋面积,备注,房屋照片",

        [
            ("", "", "", "102", "自住",
             "", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
             ),
            ("天王巷小区", "", "", "102", "自住",
             "", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
             ),
            ("天王巷小区", "官塘新村", "", "102", "自住",
             "1层", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
             ),
            ("天王巷小区", "官塘新村", "1单元", "", "自住",
             "1层", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
             ),
            ("天王巷小区", "官塘新村", "1单元", "102", "",
             "1层", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
             ),
            ("天王巷小区", "官塘新村", "1单元", "102", "自住",
             "", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
             ),
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
    def test_add__miss_data(self, 房屋管理页面,
                            db_connection,
                            所属小区, 楼栋名称, 所属单元, 门牌号, 房屋状态, 楼层数, 房屋用途, 房屋产权性质, 房屋面积,
                            备注, 房屋照片
                            ):
        # 统计数据库中的数据条数
        数据量_新增前 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        房屋管理页面.click_button("新增")
        self.log_step("点击新增按钮")
        # 填写表单信息
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=房屋管理页面.定位器_新增表单(), 所属小区=所属小区, 楼栋名称=楼栋名称, 所属单元=所属单元,
            门牌号=门牌号, 房屋状态=房屋状态, 楼层数=楼层数, 房屋用途=房屋用途, 房屋产权性质=房屋产权性质,
            房屋面积=房屋面积, 备注=备注,
            房屋照片=房屋照片)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        房屋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言操作成功字样未在页面出现
        expect(房屋管理页面.page.get_by_text("保存成功")).not_to_be_visible(timeout=5000)
        assert 房屋管理页面.page.get_by_text("不能为空").count() > 0
        self.log_step("验证新增失败-必填项缺失-页面提示信息")
        # 等待1秒
        房屋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        assert 数据量_新增后 == 数据量_新增前, f"数据库校验失败，数据库中数据量发生变化，新增前的数据量为{数据量_新增前}，新增后的数据量为{数据量_新增后}"
        self.log_step("验证新增失败-必填项缺失-数据库校验")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "所属小区,楼栋名称,所属单元,门牌号,房屋状态,楼层数,房屋用途,房屋产权性质,房屋面积,备注,房屋照片",

        [
            ("天王巷小区", "1栋", "1单元", "1", "自住",
             "1层", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
             )
            # 添加更多测试数据集
        ],
    )
    @allure.step("测试新增楼栋-失败-去重校验：同一小区名称，同一楼栋名称，同一单元下不能有重复的门牌号")
    def test_add_repeat_validation(self, 房屋管理页面,
                                   db_connection,
                                   所属小区, 楼栋名称, 所属单元, 门牌号, 房屋状态, 楼层数, 房屋用途, 房屋产权性质,
                                   房屋面积, 备注, 房屋照片
                                   ):
        # 统计数据库中的数据条数
        数据量_新增前 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        房屋管理页面.click_button("新增")
        self.log_step("点击新增按钮")
        # 填写表单信息
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=房屋管理页面.定位器_新增表单(), 所属小区=所属小区, 楼栋名称=楼栋名称, 所属单元=所属单元,
            门牌号=门牌号, 房屋状态=房屋状态, 楼层数=楼层数, 房屋用途=房屋用途, 房屋产权性质=房屋产权性质,
            房屋面积=房屋面积, 备注=备注,
            房屋照片=房屋照片)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        房屋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言该小区已存在字样在页面出现
        expect(房屋管理页面.page.get_by_text("该房屋已存在")).to_be_visible(timeout=5000)
        self.log_step("验证新增失败-去重校验-页面提示信息")
        # 等待1秒
        房屋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 房屋管理页面.统计数据库表中的记录数(db_connection)

        assert 数据量_新增后 == 数据量_新增前, f"数据库校验失败，数据库中数据量发生变化，新增前的数据量为{数据量_新增前}，新增后的数据量为{数据量_新增后}"
        self.log_step("验证新增失败-去重校验-数据库校验")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @allure.step("测试新增楼栋-前端格式校验与数据合法性")
    def test_add_frontend_validation(
            self, 房屋管理页面, db_connection,
    ):
        房屋管理页面.click_button("新增")
        self.log_step("点击新增按钮")

        # 输入门牌号
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_新增表单(),
                                                                    门牌号="-123")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待，等待刷新提示信息
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")

        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_新增表单(),
                                                                    门牌号="0")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")

        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_新增表单(),
                                                                    门牌号="12.34")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")

        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_新增表单(),
                                                                    门牌号="A1")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")

        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_新增表单(),
                                                                    门牌号="#4")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")

        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_新增表单(),
                                                                    门牌号="1 2")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")


@pytest.mark.usefixtures("房屋管理页面")  # 显式声明夹具
class TestEdit(BaseCase):
    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "所属小区,楼栋名称,所属单元,门牌号,房屋状态,楼层数,房屋用途,房屋产权性质,房屋面积,备注,房屋照片",

        [
            ("金城大厦", "88栋", "1单元", "1", "空置",
             "2层", "商业", "私有房产", "200", "这套房子很小，采光很差", r"C:\Users\Administrator\Pictures\guanyu.jpeg"
             )
            # 添加更多测试数据集
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试修改小区")
    def test_edit_success(self, 房屋管理页面,
                          db_connection, 随机门牌号, 修改后的门牌号,
                          所属小区, 楼栋名称, 所属单元, 门牌号, 房屋状态, 楼层数, 房屋用途,
                          房屋产权性质, 房屋面积, 备注, 房屋照片):
        # 输入查询条件
        # 随机门牌号 = "1736"
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(门牌号=随机门牌号)
        self.log_step("输入查询条件")
        # 点击查询按钮
        房屋管理页面.click_button("搜索")
        # 点击编辑按钮
        房屋管理页面.点击编辑按钮(随机门牌号)
        self.log_step("点击编辑按钮")
        # 填写表单信息
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=房屋管理页面.定位器_编辑表单(), 所属小区=所属小区, 楼栋名称=楼栋名称, 所属单元=所属单元,
            门牌号=修改后的门牌号, 房屋状态=房屋状态, 楼层数=楼层数, 房屋用途=房屋用途, 房屋产权性质=房屋产权性质,
            房屋面积=房屋面积, 备注=备注,
            房屋照片=房屋照片)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        房屋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 点击提示弹窗中的确定按钮
        房屋管理页面.点击提示弹窗中的确定按钮()
        # 断言操作成功字样在页面出现
        expect(房屋管理页面.page.get_by_text("保存成功!")).to_be_visible(timeout=5000)
        self.log_step("验证修改成功-页面提示信息")
        # 等待1秒
        房屋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 执行sql查询，断言一定能查到修改后的数据
        count = 房屋管理页面.统计数据库表中的记录数_修改后(db_connection, 修改后的门牌号)
        assert count > 0
        self.log_step("验证修改成功-数据库")
        # 输入查询条件
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(门牌号=修改后的门牌号)
        self.log_step("输入查询条件")
        # 点击查询按钮
        房屋管理页面.click_button("搜索")
        房屋管理页面.点击编辑按钮(修改后的门牌号)
        房屋管理页面.校验表单中数据成功修改(房屋管理页面.定位器_编辑表单(), 所属小区=所属小区, 楼栋名称=楼栋名称,
                                            所属单元=所属单元,
                                            门牌号=修改后的门牌号, 房屋状态=房屋状态, 楼层数=楼层数, 房屋用途=房屋用途,
                                            房屋产权性质=房屋产权性质,
                                            房屋面积=房屋面积, 备注=备注)

    @pytest.mark.parametrize(
        "所属小区,楼栋名称,所属单元,门牌号,房屋状态,楼层数,房屋用途,房屋产权性质,房屋面积,备注,房屋照片",

        [

            ("天王巷小区", "官塘新村", "1单元", "", "自住",
             "1层", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
             ),

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
    @allure.step("测试编辑房屋-失败-必填项缺失")
    def test_edit__miss_data(self, 房屋管理页面,
                             db_connection, 修改后的门牌号,
                             所属小区, 楼栋名称, 所属单元, 门牌号, 房屋状态, 楼层数, 房屋用途, 房屋产权性质, 房屋面积,
                             备注, 房屋照片
                             ):
        # 输入查询条件
        # 修改后的门牌号 = "103"
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(门牌号=修改后的门牌号)
        self.log_step("输入查询条件")
        # 点击查询按钮
        房屋管理页面.click_button("搜索")
        # 点击编辑按钮
        房屋管理页面.点击编辑按钮(修改后的门牌号)
        self.log_step("点击编辑按钮")
        # 修改后的门牌号 = str(int(随机门牌号) + 1)
        修改后的门牌号 = 门牌号
        # 填写表单信息
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=房屋管理页面.定位器_编辑表单(), 所属小区=所属小区, 楼栋名称=楼栋名称, 所属单元=所属单元,
            门牌号=修改后的门牌号, 房屋状态=房屋状态, 楼层数=楼层数, 房屋用途=房屋用途, 房屋产权性质=房屋产权性质,
            房屋面积=房屋面积, 备注=备注,
            房屋照片=房屋照片)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        房屋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言操作成功字样在页面出现
        expect(房屋管理页面.page.get_by_text("保存成功!")).not_to_be_visible(timeout=5000)
        assert 房屋管理页面.page.get_by_text("不能为空").count() > 0
        self.log_step("验证修改失败-页面提示信息")
        # 等待1秒
        房屋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 执行sql查询，断言一定能查到修改后的数据
        count = 房屋管理页面.统计数据库表中的记录数_修改后(db_connection, 修改后的门牌号)
        assert count == 0
        self.log_step("验证修改失败-数据库")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @pytest.mark.parametrize(
        "所属小区,楼栋名称,所属单元,门牌号,房屋状态,楼层数,房屋用途,房屋产权性质,房屋面积,备注,房屋照片",

        [
            ("天王巷小区", "1栋", "1单元", "1", "自住",
             "1层", "住宅", "国有房产", "100", "这套房子很大，采光很好", r"C:\Users\Administrator\Pictures\111.png"
             )
            # 添加更多测试数据集
        ],
    )
    @allure.step("测试编辑房屋-失败-去重校验：同一小区名称，同一楼栋名称，同一单元下不能有重复的门牌号")
    def test_edit_repeat_validation(self, 房屋管理页面,
                                    db_connection, 修改后的门牌号,
                                    所属小区, 楼栋名称, 所属单元, 门牌号, 房屋状态, 楼层数, 房屋用途, 房屋产权性质,
                                    房屋面积, 备注, 房屋照片
                                    ):
        # 输入查询条件
        # 修改后的门牌号 = "103"
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(门牌号=修改后的门牌号)
        self.log_step("输入查询条件")
        # 点击查询按钮
        房屋管理页面.click_button("搜索")
        # 点击编辑按钮
        房屋管理页面.点击编辑按钮(修改后的门牌号)
        self.log_step("点击编辑按钮")
        # 修改后的门牌号 = str(int(修改后的门牌号) + 1)
        修改后的门牌号 = 门牌号
        # 填写表单信息
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(
            表单最上层定位=房屋管理页面.定位器_编辑表单(), 所属小区=所属小区, 楼栋名称=楼栋名称, 所属单元=所属单元,
            门牌号=修改后的门牌号, 房屋状态=房屋状态, 楼层数=楼层数, 房屋用途=房屋用途, 房屋产权性质=房屋产权性质,
            房屋面积=房屋面积, 备注=备注,
            房屋照片=房屋照片)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        房屋管理页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 点击提示弹窗中的确定按钮
        房屋管理页面.点击提示弹窗中的确定按钮()
        # 断言操作失败字样在页面出现
        expect(房屋管理页面.page.get_by_text("该房屋已存在")).to_be_visible(timeout=5000)
        self.log_step("验证修改失败-页面提示信息")
        # 等待1秒
        房屋管理页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 执行sql查询，断言查询到的数据量不变
        count = 房屋管理页面.统计数据库表中的记录数_修改后(db_connection, 修改后的门牌号)
        assert count > 0
        self.log_step("验证修改失败-数据库")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @allure.step("测试编辑房屋-前端格式校验与数据合法性")
    def test_edit_frontend_validation(
            self, 房屋管理页面, db_connection, 修改后的门牌号
    ):
        # 修改后的门牌号 = "103"
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(门牌号=修改后的门牌号)
        self.log_step("输入查询条件")
        # 点击查询按钮
        房屋管理页面.click_button("搜索")
        # 点击编辑按钮
        房屋管理页面.点击编辑按钮(修改后的门牌号)
        self.log_step("点击编辑按钮")

        # 输入门牌号
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_编辑表单(),
                                                                    门牌号="-123")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待，等待刷新提示信息
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")

        # 房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_编辑表单(),
        #                                                             门牌号="0")
        # self.log_step("填写门牌号")
        # 房屋管理页面.page.wait_for_timeout(500)  # 简单等待
        # expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        # self.log_step("断言页面提示信息-门牌号")

        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_编辑表单(),
                                                                    门牌号="12.34")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")

        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_编辑表单(),
                                                                    门牌号="A1")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")

        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(表单最上层定位=房屋管理页面.定位器_编辑表单(),
                                                                    门牌号="#4")
        self.log_step("填写门牌号")
        房屋管理页面.page.wait_for_timeout(500)  # 简单等待
        expect(房屋管理页面.page.get_by_text("请输入0-4位正整数")).to_have_count(1)
        self.log_step("断言页面提示信息-门牌号")


def build_query_sql(选择小区=None, 选择楼栋=None, 楼栋名称=None, 选择单元=None, 门牌号=None):
    """
    根据给定参数动态生成小区查询 SQL。
    """
    sql = """SELECT a.*, v.xqmc,b.ldh, b.ldmc, u.name as dymc FROM ybds_house a LEFT JOIN ybds_building b ON a.ldbm=b.ldbm LEFT JOIN ybds_unit u on a.dybm = u.dybm left join base_village as v on a.xqbm = v.xqbm where v.xqbm IN ( '340103225001001' , '340103225001002' , '340103225001111' , '340103225001223' , '2010005425' , '340103225002002' , '340103225003001' , '340103225001012' , '340103225002213' , '340103225003198' , '340103225003188' )"""

    # 存放动态条件列表和参数字典
    conditions = []
    params = {}

    if 选择小区 is not None:
        # 根据/来分割选择小区，获取最后一级小区名称
        选择小区 = 选择小区.split('/')[-1]

        # 添加选择小区条件
        conditions.append(f"and BINARY v.xqmc = %(选择小区)s")
        # 添加参数
        params["选择小区"] = f"{选择小区}"

    if 选择楼栋 is not None:
        conditions.append("and b.ldh = %(选择楼栋)s")
        params["选择楼栋"] = f"{选择楼栋}"

    if 楼栋名称 is not None:
        conditions.append("and b.ldmc like CONCAT('%%', %(楼栋名称)s,'%%' )")
        params["楼栋名称"] = f"{楼栋名称}"

    if 选择单元 is not None:
        conditions.append("and u.name like CONCAT('%%', %(选择单元)s,'%%' )")
        params["选择单元"] = f"{选择单元}"

    if 门牌号 is not None:
        conditions.append("and a.mph = %(门牌号)s")
        params["门牌号"] = f"{门牌号}"

    # 拼接sql
    sql += " " + " ".join(conditions)
    sql += ' ORDER BY b.ldh+0, a.dyh+0, a.mph+0'
    return sql, params


class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "选择小区, 选择楼栋, 楼栋名称, 选择单元, 门牌号",
        [
            (None, None, None, None, None),
            ("中电数智街道/中电数智社区/天王巷小区", None, None, None, None),
            (None, None, "官塘新村", None, None),
            (None, None, None, None, "101"),
            ("中电数智街道/中电数智社区/天王巷小区", "1", None, None, None),
            ("中电数智街道/中电数智社区/天王巷小区", None, "官塘新村", None, None),
            ("中电数智街道/中电数智社区/天王巷小区", None, None, None, "101"),
            (None, None, "官塘新村", None, "101"),
            ("中电数智街道/中电数智社区/天王巷小区", "1", "官塘新村", None, None),
            ("中电数智街道/中电数智社区/天王巷小区", "1", None, "1单元", None),
            ("中电数智街道/中电数智社区/天王巷小区", "1", None, None, "101"),
            ("中电数智街道/中电数智社区/天王巷小区", "1", "官塘新村", "1单元", "101"),
        ]
    )
    def test_query(self, 房屋管理页面, db_connection, 选择小区, 选择楼栋, 楼栋名称, 选择单元, 门牌号):
        # 输入查询条件
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(选择小区=选择小区, 选择楼栋=选择楼栋,
                                                                    楼栋名称=楼栋名称, 选择单元=选择单元, 门牌号=门牌号)
        self.log_step("输入查询条件")

        # 获取查询接口响应的数据
        查询接口返回的数据 = 房屋管理页面.获取查询接口响应的数据("搜索")
        self.log_step("获取查询接口响应的数据")

        # 构建 SQL 查询
        sql, params = build_query_sql(选择小区=选择小区, 选择楼栋=选择楼栋, 楼栋名称=楼栋名称, 选择单元=选择单元,
                                      门牌号=门牌号)

        # 根据sql语句和参数，从数据库中提取数据
        db_data = 房屋管理页面.get_db_data(db_connection, query=sql, params=params)
        self.log_step("从数据库中提取数据")

        # 对比数据
        assert 房屋管理页面.对比查询接口数据和数据库数据(查询接口返回的数据, db_data,['xqmc', 'ldh', 'ldmc', 'dymc', 'mph', 'fwmj'])
        self.log_step("比较两个数据集")


class TestReset(BaseCase):
    def test_reset(self, 房屋管理页面, db_connection):
        # 输入查询条件
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(选择小区="中电数智街道/中电数智社区/天王巷小区",
                                                                    选择楼栋="1",
                                                                    楼栋名称="官塘新村", 选择单元="1单元", 门牌号="101")
        self.log_step("输入查询条件")

        # 点击重置按钮，获取查询接口响应的数据
        查询接口返回的数据 = 房屋管理页面.获取查询接口响应的数据("重置")
        self.log_step("获取查询接口响应的数据")

        # 构建 SQL 查询
        sql, params = build_query_sql(选择小区=None, 选择楼栋=None, 楼栋名称=None, 选择单元=None, 门牌号=None)

        # 根据sql语句和参数，从数据库中提取数据
        db_data = 房屋管理页面.get_db_data(db_connection, query=sql, params=params)
        self.log_step("从数据库中提取数据")

        # 对比数据
        assert 房屋管理页面.对比查询接口数据和数据库数据(查询接口返回的数据, db_data,
                                                         ['xqmc', 'ldh', 'ldmc', 'dymc', 'mph', 'fwmj'])
        self.log_step("比较两个数据集")

        房屋管理页面.校验表单中数据成功修改(选择小区="", 选择楼栋="", 楼栋名称="", 选择单元="", 门牌号="")


@pytest.mark.usefixtures("后置操作_重置查询条件")
class TestDelete(BaseCase):
    def test_delete_success(self, 房屋管理页面, db_connection, 修改后的门牌号):
        # 修改后的门牌号 = "103"
        # 从数据库中统计状态为删除的数据条数
        数据库中数据量_删除前 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 查找待删除的记录
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(门牌号=修改后的门牌号)

        房屋管理页面.click_button("搜索")
        _, 表格中数据量_删除前 = 房屋管理页面.get_table_data()
        self.log_step("统计删除操作前表格行数")
        房屋管理页面.点击删除按钮(修改后的门牌号)
        房屋管理页面.click_button("确定")
        self.log_step("点击删除按钮,弹窗后点击确定按钮")
        expect(房屋管理页面.page.get_by_text("删除成功")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现删除成功字样")
        # 等待1秒
        房屋管理页面.page.wait_for_timeout(1000)
        _, 表格中数据量_删除后 = 房屋管理页面.get_table_data()
        self.log_step("统计删除成功操作后表格行数")
        # 断言：表格中的行数减1
        assert 表格中数据量_删除后 == 表格中数据量_删除前 - 1, "表格中的行数未减少"
        # 验证数据库中的数据是否已删除（或标记为已删除）
        db_connection.ping(reconnect=True)  # 确保数据库连接有效
        db_connection.commit()
        数据库中数据量_删除后 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 断言：数据库中状态为已删除的数据多了1条
        assert 数据库中数据量_删除后 == 数据库中数据量_删除前 - 1, "数据库中的数据未删除"
        self.log_step("验证数据库中的数据是否已删除")

    @pytest.mark.parametrize("门牌号_待删除", [
        "1"
    ])
    def test_delete_cancel(self, 房屋管理页面, db_connection, 门牌号_待删除):
        # 从数据库中统计状态为删除的数据条数
        数据库中数据量_删除前 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 查找待删除的记录
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(门牌号=门牌号_待删除)

        房屋管理页面.click_button("搜索")
        _, 表格中数据量_删除前 = 房屋管理页面.get_table_data()
        self.log_step("统计删除操作前表格行数")
        房屋管理页面.点击删除按钮(门牌号_待删除)
        房屋管理页面.click_button("取消")
        self.log_step("点击删除按钮,弹窗后点击取消按钮")
        expect(房屋管理页面.page.get_by_text("删除成功")).not_to_be_visible(timeout=5000)
        self.log_step("验证页面未出现删除成功字样")
        # 等待1秒
        房屋管理页面.page.wait_for_timeout(1000)
        _, 表格中数据量_删除后 = 房屋管理页面.get_table_data()
        self.log_step("统计删除取消操作后表格行数")
        # 断言：表格中的行数减1
        assert 表格中数据量_删除后 == 表格中数据量_删除前, "表格中的行数减少了"
        # 验证数据库中的数据是否已删除（或标记为已删除）
        db_connection.ping(reconnect=True)  # 确保数据库连接有效
        db_connection.commit()
        数据库中数据量_删除后 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 断言：数据库中状态为已删除的数据不变
        assert 数据库中数据量_删除后 == 数据库中数据量_删除前, "数据库中的数据被删除了"
        self.log_step("验证数据库中的数据是否已删除")

    @pytest.mark.parametrize("选择小区_待删除, 选择楼栋_待删除, 选择单元_待删除, 门牌号_待删除",
                             [
                                 ("中电数智街道/中电数智社区/金城大厦", "1", "1单元", "1")
                             ])
    def test_delete_fail(self, 房屋管理页面, db_connection, 选择小区_待删除, 选择楼栋_待删除, 选择单元_待删除,
                         门牌号_待删除):
        # 从数据库中统计状态为删除的数据条数
        数据库中数据量_删除前 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 查找待删除的记录
        房屋管理页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(选择小区=选择小区_待删除, 选择楼栋=选择楼栋_待删除,
                                                                    选择单元=选择单元_待删除, 门牌号=门牌号_待删除)
        房屋管理页面.click_button("搜索")
        _, 表格中数据量_删除前 = 房屋管理页面.get_table_data()
        self.log_step("统计删除操作前表格行数")
        房屋管理页面.点击删除按钮(门牌号_待删除)
        房屋管理页面.click_button("确定")
        self.log_step("点击删除按钮,弹窗后点击确定按钮")
        expect(房屋管理页面.page.get_by_text("不允许删除")).to_be_visible(timeout=5000)
        self.log_step("验证页面出现不允许删除字样")
        # 等待1秒
        房屋管理页面.page.wait_for_timeout(1000)
        _, 表格中数据量_删除后 = 房屋管理页面.get_table_data()
        self.log_step("统计删除操作后表格行数")
        # 断言：表格中的行数不变
        assert 表格中数据量_删除后 == 表格中数据量_删除前, "表格中的行数减少了"
        # 验证数据库中的数据是否已删除（或标记为已删除）
        db_connection.ping(reconnect=True)  # 确保数据库连接有效
        db_connection.commit()
        数据库中数据量_删除后 = 房屋管理页面.统计数据库表中的记录数(db_connection)
        # 断言：数据库中数据量不变
        assert 数据库中数据量_删除后 == 数据库中数据量_删除前, "数据库中的数据删除了"
        self.log_step("验证数据库中的数据是否已删除")
