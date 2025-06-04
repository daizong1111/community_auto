"""
此模块使用 Playwright 框架实现会议室管理模块的 UI 自动化测试，
包含增、删、改、查功能的测试用例。
"""
import random
import allure

from base_case import BaseCase
from pages.meeting_room_manage.meeting_room_manage_page import MeetingRoomManagePageBase

from playwright.sync_api import expect, sync_playwright
import pytest
import logging

from pages.基础信息.实有房屋.小区信息 import PageCommunity

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 测试夹具-获取浏览器当前打开页面，并返回 MeetingRoomManagePageBase 对象
@pytest.fixture(scope="function")
def 小区信息页面():
    with sync_playwright() as playwright:
        # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        # 通过ip和端口连接到已经打开的chromium浏览器
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(6000)  # 设置默认超时时间为 4000 毫秒
        # 创建小区信息页面对象
        page = PageCommunity(page)
        # 返回会议室管理页面对象
        yield page


@pytest.mark.usefixtures("小区信息页面")  # 显式声明夹具
class TestAdd(BaseCase):

    @pytest.mark.parametrize(
        "小区名称,行政区域,所属居委会,公安机构,小区类型,物业名称,物业管理员,物业管理员手机号码,物业管理员身份证号,建设厂家,建设厂家负责人,警员姓名,警员编号,警员联系方式,建设厂家联系电话,小区序号,管理类别,小区地址,小区照片,视联网小区ID, 占地面积, 建筑面积, 标准地址,备注,地图坐标集, 经度, 纬度",

        [
            #     ("新增-成功", "安徽省/合肥市/庐阳区", "中电数智社区（演示）", "河北省公安局", "商业", "中电数智物业", "蔡文",
            #      "13865546155", "340421199711170022", "河北省京东直营家电采购厂",
            #      "刘富豪", "石童涛", "1281130022", "15855211922", "13955392033", "383", "物管小区", "北京市义安区街道1005号", r"C:\Users\Administrator\Pictures\111.png", "3397","20030","18900", "北京市义安区街道1005号", "本小区属于高档富人小区，闲人免进", "{116.794571,33.971816},{116.794585,33.972089},{116.794600,33.972037},{116.794781,33.971885},{116.794783,33.971750},{116.794783,33.971750}", "116.794677","33.971920"),
            #
            ("新增-成功-备注输入200字", "安徽省/合肥市/庐阳区", "中电数智社区（演示）", "河北省公安局", "商业",
             "中电数智物业", "蔡文",
             "13865546155", "340421199711170022", "河北省京东直营家电采购厂",
             "刘富豪", "石童涛", "1281130022", "15855211922", "13955392033", "383", "物管小区",
             "北京市义安区街道1005号", r"C:\Users\Administrator\Pictures\111.png", "3397", "20030", "18900",
             "北京市义安区街道1005号",
             "小区环境宜人，绿化覆盖率高，四季皆有景。内部设有儿童游乐区、健身角，方便居民休闲活动。物业服务响应及时，保洁到位，安保巡逻频繁，让人住得安心。邻里关系和谐，常有社区活动增进感情。停车管理有序，虽有高峰时段紧张，但总体尚可。周边配套齐全，超市、餐厅、学校、医院均在步行范围内。交通便捷，多条公交线路经过，离地铁站也不远。房屋多为中高层，采光良好。唯一不足是部分楼栋间存在视野遮挡。总体而言，是一个适宜居住、生活便利的成熟社区。",
             "{116.794571,33.971816},{116.794585,33.972089},{116.794600,33.972037},{116.794781,33.971885},{116.794783,33.971750},{116.794783,33.971750}",
             "116.794677", "33.971920")
            # 添加更多测试数据集
        ],
        # ids=["新增-成功"
        #
        #      ]
    )
    @allure.step("测试新增小区信息-成功")
    def test_add_success(self, 小区信息页面,
                         db_connection,
                         小区名称: object,
                         行政区域: object, 所属居委会: object,
                         公安机构: object, 小区类型: object,
                         物业名称: object,
                         物业管理员, 物业管理员手机号码: object, 物业管理员身份证号: object,
                         建设厂家: object,
                         建设厂家负责人: object,
                         警员姓名: object,
                         警员编号: object, 警员联系方式, 建设厂家联系电话, 小区序号, 管理类别, 小区地址, 小区照片,
                         视联网小区ID, 占地面积, 建筑面积, 标准地址, 备注, 地图坐标集, 经度, 纬度
                         ):
        # 统计数据库中的数据条数
        数据量_新增前 = 小区信息页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        小区信息页面.点击新增按钮()
        self.log_step("点击新增按钮")
        # 填写表单信息
        小区信息页面.表单_文本框填写("小区名称", 小区名称,
                                     小区信息页面.page.locator('//div[@aria-label="新增小区信息"]'))
        小区信息页面.click_below_and_right_of_element(小区信息页面.page.locator('//div[@aria-label="新增小区信息"]'))
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(行政区域=行政区域, 所属居委会=所属居委会,
                                                                    公安机构=公安机构, 小区类型=小区类型,
                                                                    物业名称=物业名称, 物业管理员=物业管理员,
                                                                    手机号码=物业管理员手机号码,
                                                                    身份证号=物业管理员身份证号,
                                                                    建设厂家=建设厂家, 建设厂家负责人=建设厂家负责人,
                                                                    警员姓名=警员姓名, 警员编号=警员编号,
                                                                    警员联系方式=警员联系方式,
                                                                    小区序号=小区序号, 管理类别=管理类别,
                                                                    小区地址=小区地址, 小区照片=小区照片,
                                                                    视联网小区ID=视联网小区ID,
                                                                    占地面积=占地面积, 建筑面积=建筑面积,
                                                                    标准地址=标准地址, 备注=备注, 地图坐标集=地图坐标集,
                                                                    经度=经度, 纬度=纬度)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        小区信息页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言操作成功字样在页面出现
        小区信息页面.page.get_by_text("保存成功!").wait_for(timeout=5000)
        assert 小区信息页面.page.get_by_text("操作成功").is_visible()
        self.log_step("验证新增成功-页面提示信息")
        # 等待1秒
        小区信息页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 小区信息页面.统计数据库表中的记录数(db_connection)
        # 断言新增后数据库表中数据量增加了1
        assert 数据量_新增后 == 数据量_新增前 + 1
        self.log_step("验证新增成功-数据库校验")

    @pytest.mark.parametrize(
        "小区名称,行政区域,所属居委会,公安机构,小区类型,物业名称,物业管理员姓名,物业管理员手机号码,物业管理员身份证号,建设厂家,建设厂家负责人,警员姓名,警员编号,警员联系方式,建设厂家联系电话,小区序号,管理类别,小区地址,小区照片,视联网小区ID, 占地面积, 建筑面积, 标准地址,备注,地图坐标集, 经度, 纬度",

        [
            ("", "安徽省/合肥市/庐阳区", "中电数智社区（演示）", "河北省公安局", "商业", "中电数智物业", "蔡文",
             "13865546155", "340421199711170022", "河北省京东直营家电采购厂",
             "刘富豪", "石童涛", "1281130022", "15855211922", "13955392033", "383", "物管小区",
             "北京市义安区街道1005号", r"C:\Users\Administrator\Pictures\111.png", "3397", "20030", "18900",
             "北京市义安区街道1005号", "本小区属于高档富人小区，闲人免进",
             "{116.794571,33.971816},{116.794585,33.972089},{116.794600,33.972037},{116.794781,33.971885},{116.794783,33.971750},{116.794783,33.971750}",
             "116.794677", "33.971920")
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
    @allure.step("测试新增小区-失败-必填项缺失")
    def test_add__miss_data(self, 小区信息页面,
                            db_connection,
                            小区名称: object,
                            行政区域: object, 所属居委会: object,
                            公安机构: object, 小区类型: object,
                            物业名称: object,
                            物业管理员姓名: object, 物业管理员手机号码: object, 物业管理员身份证号: object,
                            建设厂家: object,
                            建设厂家负责人: object,
                            警员姓名: object,
                            警员编号: object, 警员联系方式, 建设厂家联系电话, 小区序号, 管理类别, 小区地址, 小区照片,
                            视联网小区ID, 占地面积, 建筑面积, 标准地址, 备注, 地图坐标集, 经度, 纬度):
        # 统计数据库中的数据条数
        数据量_新增前 = 小区信息页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        小区信息页面.点击新增按钮()
        self.log_step("点击新增按钮")
        # 填写表单信息
        小区信息页面.表单_文本框填写("小区名称", 小区名称,
                                     小区信息页面.page.locator('//div[@aria-label="新增小区信息"]'))
        # 小区信息页面.click_below_and_right_of_element(小区信息页面.page.locator('//div[@aria-label="新增小区信息"]'))
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(行政区域=行政区域, 所属居委会=所属居委会,
                                                                    公安机构=公安机构, 小区类型=小区类型,
                                                                    物业名称=物业名称, 物业管理员姓名=物业管理员姓名,
                                                                    物业管理员手机号码=物业管理员手机号码,
                                                                    物业管理员身份证号=物业管理员身份证号,
                                                                    建设厂家=建设厂家, 建设厂家负责人=建设厂家负责人,
                                                                    警员姓名=警员姓名, 警员编号=警员编号,
                                                                    警员联系方式=警员联系方式,
                                                                    建设厂家联系电话=建设厂家联系电话,
                                                                    小区序号=小区序号, 管理类别=管理类别,
                                                                    小区地址=小区地址, 小区照片=小区照片,
                                                                    视联网小区ID=视联网小区ID,
                                                                    占地面积=占地面积, 建筑面积=建筑面积,
                                                                    标准地址=标准地址, 备注=备注, 地图坐标集=地图坐标集,
                                                                    经度=经度, 纬度=纬度)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区照片="")
        self.log_step("填写表单信息")
        # 点击提交按钮
        小区信息页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言操作成功字样在页面出现
        assert not 小区信息页面.page.get_by_text("保存成功!").is_visible()
        assert 小区信息页面.page.get_by_text("请填写").count() > 0
        self.log_step("验证新增失败-必填项缺失-页面提示信息")
        # 等待1秒
        小区信息页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 小区信息页面.统计数据库表中的记录数(db_connection)

        assert 数据量_新增后 == 数据量_新增前
        self.log_step("验证新增失败-必填项缺失-数据库校验")

    @pytest.mark.parametrize(
        "小区名称,行政区域,所属居委会,公安机构,小区类型,物业名称,物业管理员姓名,物业管理员手机号码,物业管理员身份证号,建设厂家,建设厂家负责人,警员姓名,警员编号,警员联系方式,建设厂家联系电话,小区序号,管理类别,小区地址,小区照片,视联网小区ID, 占地面积, 建筑面积, 标准地址,备注,地图坐标集, 经度, 纬度",

        [
            ("新增-失败-去重校验", "安徽省/合肥市/庐阳区", "中电数智社区（演示）", "河北省公安局", "商业", "中电数智物业",
             "蔡文",
             "13865546155", "340421199711170022", "河北省京东直营家电采购厂",
             "刘富豪", "石童涛", "1281130022", "15855211922", "13955392033", "002", "物管小区",
             "北京市义安区街道1005号", r"C:\Users\Administrator\Pictures\111.png", "3397", "20030", "18900",
             "北京市义安区街道1005号", "本小区属于高档富人小区，闲人免进",
             "{116.794571,33.971816},{116.794585,33.972089},{116.794600,33.972037},{116.794781,33.971885},{116.794783,33.971750},{116.794783,33.971750}",
             "116.794677", "33.971920")
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
    @allure.step("测试新增小区-失败-去重校验")
    def test_add_repeat_validation(self, 小区信息页面,
                                   db_connection,
                                   小区名称: object,
                                   行政区域: object, 所属居委会: object,
                                   公安机构: object, 小区类型: object,
                                   物业名称: object,
                                   物业管理员姓名: object, 物业管理员手机号码: object, 物业管理员身份证号: object,
                                   建设厂家: object,
                                   建设厂家负责人: object,
                                   警员姓名: object,
                                   警员编号: object, 警员联系方式, 建设厂家联系电话, 小区序号, 管理类别, 小区地址,
                                   小区照片,
                                   视联网小区ID, 占地面积, 建筑面积, 标准地址, 备注, 地图坐标集, 经度, 纬度):
        # 统计数据库中的数据条数
        数据量_新增前 = 小区信息页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        小区信息页面.点击新增按钮()
        self.log_step("点击新增按钮")
        # 填写表单信息
        小区信息页面.表单_文本框填写("小区名称", 小区名称,
                                     小区信息页面.page.locator('//div[@aria-label="新增小区信息"]'))
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(行政区域=行政区域, 所属居委会=所属居委会,
                                                                    公安机构=公安机构, 小区类型=小区类型,
                                                                    物业名称=物业名称, 物业管理员姓名=物业管理员姓名,
                                                                    物业管理员手机号码=物业管理员手机号码,
                                                                    物业管理员身份证号=物业管理员身份证号,
                                                                    建设厂家=建设厂家, 建设厂家负责人=建设厂家负责人,
                                                                    警员姓名=警员姓名, 警员编号=警员编号,
                                                                    警员联系方式=警员联系方式,
                                                                    建设厂家联系电话=建设厂家联系电话,
                                                                    小区序号=小区序号, 管理类别=管理类别,
                                                                    小区地址=小区地址, 小区照片=小区照片,
                                                                    视联网小区ID=视联网小区ID,
                                                                    占地面积=占地面积, 建筑面积=建筑面积,
                                                                    标准地址=标准地址, 备注=备注, 地图坐标集=地图坐标集,
                                                                    经度=经度, 纬度=纬度)
        self.log_step("填写表单信息")
        # 点击提交按钮
        小区信息页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言该小区已存在字样在页面出现
        assert 小区信息页面.page.get_by_text("该小区已存在!").is_visible()
        self.log_step("验证新增失败-去重校验-页面提示信息")
        # 等待1秒
        小区信息页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 小区信息页面.统计数据库表中的记录数(db_connection)

        assert 数据量_新增后 == 数据量_新增前
        self.log_step("验证新增失败-去重校验-数据库校验")

    @allure.step("测试新增-前端格式校验与数据合法性")
    def test_add_frontend_validation(
            self, 小区信息页面, db_connection,
    ):
        小区信息页面.click_button("新增")
        self.log_step("点击新增按钮")

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="138001")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="1380013890a")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="1380013890@")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="138 001 3890")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="138-001-3890")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 手机号不以1开头
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="23800138900")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 第二位不是3/5/6/7/8/9
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="11000138900")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 手机号全为同一个数字
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="11111111111")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 刚好11位但不符合规则的最小数字
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="10000000000")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 刚好11位但不符合规则的最大数字
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员手机号码="99999999999")
        self.log_step("填写手机号码")
        assert 小区信息页面.page.get_by_text("请输入正确的联系格式").is_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 长度不足
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员身份证号="199001011234")
        self.log_step("填写物业管理员身份证号")
        assert 小区信息页面.page.get_by_text("请填写正确的身份证号").is_visible()
        self.log_step("断言页面提示信息-物业管理员身份证号")

        # 长度过长
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员身份证号="310101199001011234567")
        self.log_step("填写物业管理员身份证号")
        assert 小区信息页面.page.get_by_text("请填写正确的身份证号").is_visible()
        self.log_step("断言页面提示信息-物业管理员身份证号")

        # 非数字字符
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员身份证号="31010119900101123@")
        self.log_step("填写物业管理员身份证号")
        assert 小区信息页面.page.get_by_text("请填写正确的身份证号").is_visible()
        self.log_step("断言页面提示信息-物业管理员身份证号")

        # 地址码无效
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员身份证号="000000199001011234")
        self.log_step("填写物业管理员身份证号")
        assert 小区信息页面.page.get_by_text("请填写正确的身份证号").is_visible()
        self.log_step("断言页面提示信息-物业管理员身份证号")

        # 出生日期无效-2月30日，不存在
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员身份证号="310101199002301234")
        self.log_step("填写物业管理员身份证号")
        assert 小区信息页面.page.get_by_text("请填写正确的身份证号").is_visible()
        self.log_step("断言页面提示信息-物业管理员身份证号")

        # 性别位错误-第17位非数字
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(物业管理员身份证号="31010119900101123A")
        self.log_step("填写物业管理员身份证号")
        assert 小区信息页面.page.get_by_text("请填写正确的身份证号").is_visible()
        self.log_step("断言页面提示信息-物业管理员身份证号")

        # 小区序号为0
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区序号="0")
        self.log_step("填写小区序号")
        assert 小区信息页面.page.get_by_text("请输入1-3位正整数").is_visible()
        self.log_step("断言页面提示信息-小区序号")

        # 负数
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区序号="-5")
        self.log_step("填写小区序号")
        assert 小区信息页面.page.get_by_text("请输入1-3位正整数").is_visible()
        self.log_step("断言页面提示信息-小区序号")

        # 字母
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区序号="a")
        self.log_step("填写小区序号")
        assert 小区信息页面.page.get_by_text("请输入1-3位正整数").is_visible()
        self.log_step("断言页面提示信息-小区序号")

        # 小数
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区序号="1.2")
        self.log_step("填写小区序号")
        assert 小区信息页面.page.get_by_text("请输入1-3位正整数").is_visible()
        self.log_step("断言页面提示信息-小区序号")

        # 长度过长
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区序号="12345")
        self.log_step("填写小区序号")
        assert 小区信息页面.page.get_by_text("请输入1-3位正整数").is_visible()
        self.log_step("断言页面提示信息-小区序号")

    @pytest.mark.parametrize(
        "小区名称,行政区域,所属居委会,公安机构,小区类型,物业名称,物业管理员姓名,物业管理员手机号码,物业管理员身份证号,建设厂家,建设厂家负责人,警员姓名,警员编号,警员联系方式,建设厂家联系电话,小区序号,管理类别,小区地址,小区照片,视联网小区ID, 占地面积, 建筑面积, 标准地址,备注,地图坐标集, 经度, 纬度",

        [
            ("新增-失败-重复的小区区域", "安徽省/合肥市/庐阳区", "中电数智社区（演示）", "河北省公安局", "商业",
             "中电数智物业", "蔡文",
             "13865546155", "340421199711170022", "河北省京东直营家电采购厂",
             "刘富豪", "石童涛", "1281130022", "15855211922", "13955392033", "383", "物管小区",
             "北京市义安区街道1005号", r"C:\Users\Administrator\Pictures\111.png", "3397", "20030", "18900",
             "北京市义安区街道1005号", "本小区属于高档富人小区，闲人免进",
             "{117.256358,31.832431},{117.285922,31.833339},{117.256714,31.819417}",
             "117.271140", "31.826378")
            # 添加更多测试数据集
        ],
        # ids=[
        #      "新增-失败-必填项为空-会议室名称",
        #      ]
    )
    @allure.step("测试新增小区-失败-重复的小区区域")
    def test_add_repeat_area(self, 小区信息页面,
                             db_connection,
                             小区名称: object,
                             行政区域: object, 所属居委会: object,
                             公安机构: object, 小区类型: object,
                             物业名称: object,
                             物业管理员姓名: object, 物业管理员手机号码: object, 物业管理员身份证号: object,
                             建设厂家: object,
                             建设厂家负责人: object,
                             警员姓名: object,
                             警员编号: object, 警员联系方式, 建设厂家联系电话, 小区序号, 管理类别, 小区地址, 小区照片,
                             视联网小区ID, 占地面积, 建筑面积, 标准地址, 备注, 地图坐标集, 经度, 纬度):
        # 统计数据库中的数据条数
        数据量_新增前 = 小区信息页面.统计数据库表中的记录数(db_connection)
        # 点击新增按钮
        小区信息页面.点击新增按钮()
        self.log_step("点击新增按钮")
        # 填写表单信息
        小区信息页面.表单_文本框填写("小区名称", 小区名称,
                                     小区信息页面.page.locator('//div[@aria-label="新增小区信息"]'))
        # 小区信息页面.click_below_and_right_of_element(小区信息页面.page.locator('//div[@aria-label="新增小区信息"]'))
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(行政区域=行政区域, 所属居委会=所属居委会,
                                                                    公安机构=公安机构, 小区类型=小区类型,
                                                                    物业名称=物业名称, 物业管理员姓名=物业管理员姓名,
                                                                    物业管理员手机号码=物业管理员手机号码,
                                                                    物业管理员身份证号=物业管理员身份证号,
                                                                    建设厂家=建设厂家, 建设厂家负责人=建设厂家负责人,
                                                                    警员姓名=警员姓名, 警员编号=警员编号,
                                                                    警员联系方式=警员联系方式,
                                                                    建设厂家联系电话=建设厂家联系电话,
                                                                    小区序号=小区序号, 管理类别=管理类别,
                                                                    小区地址=小区地址, 小区照片=小区照片,
                                                                    视联网小区ID=视联网小区ID,
                                                                    占地面积=占地面积, 建筑面积=建筑面积,
                                                                    标准地址=标准地址, 备注=备注, 地图坐标集=地图坐标集,
                                                                    经度=经度, 纬度=纬度)
        self.log_step("填写表单信息")
        # 点击提交按钮
        小区信息页面.click_button("确定")
        self.log_step("点击提交按钮")
        # 断言操作成功字样在页面出现
        assert 小区信息页面.page.get_by_text("小区区域重叠").is_visible()
        self.log_step("验证新增失败-重复的小区区域")
        # 等待1秒
        小区信息页面.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是新增之前的
        # 统计数据库中的数据条数
        数据量_新增后 = 小区信息页面.统计数据库表中的记录数(db_connection)

        assert 数据量_新增后 == 数据量_新增前
        self.log_step("验证新增失败-重复的小区区域")

    @pytest.mark.parametrize(
        "区域, 物业名称, 办公地址, 联系人, 联系人电话",

        [
            #     ("新增-成功", "安徽省/合肥市/庐阳区", "中电数智社区（演示）", "河北省公安局", "商业", "中电数智物业", "蔡文",
            #      "13865546155", "340421199711170022", "河北省京东直营家电采购厂",
            #      "刘富豪", "石童涛", "1281130022", "15855211922", "13955392033", "383", "物管小区", "北京市义安区街道1005号", r"C:\Users\Administrator\Pictures\111.png", "3397","20030","18900", "北京市义安区街道1005号", "本小区属于高档富人小区，闲人免进", "{116.794571,33.971816},{116.794585,33.972089},{116.794600,33.972037},{116.794781,33.971885},{116.794783,33.971750},{116.794783,33.971750}", "116.794677","33.971920"),
            #
            ("中电数智街道/中电数智社区（测试）", "万科物业", "安徽省合肥市蜀山区大蜀山地铁口旁财富大楼14层1403号",
             "石童涛", "13955499272")
            # 添加更多测试数据集
        ],
        # ids=["新增-成功"
        #
        #      ]
    )
    @allure.step("测试新增物业信息-成功")
    def test_add_property_success(self, 小区信息页面, 区域, 物业名称, 办公地址, 联系人, 联系人电话
                                  ):
        # 生成一串随机数字
        随机数字 = random.randint(1000, 9999)
        物业名称 = 物业名称 + str(随机数字)
        # 点击新增按钮
        小区信息页面.点击新增按钮()
        self.log_step("点击新增按钮")

        小区信息页面.点击物业新增按钮()
        self.log_step("点击物业新增按钮")
        # 填写表单信息
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(区域=区域, 物业名称=物业名称, 办公地址=办公地址,
                                                                    联系人=联系人, 联系人电话=联系人电话)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        小区信息页面.click_button("确定", 按钮的父元素=小区信息页面.page.locator('//div[@aria-label="新增物业信息"]'))
        self.log_step("点击提交按钮")
        # 断言操作成功字样在页面出现
        小区信息页面.page.get_by_text("添加成功").wait_for(timeout=5000)
        assert 小区信息页面.page.get_by_text("添加成功").is_visible()
        self.log_step("验证新增物业成功-页面提示信息")

        小区信息页面.验证新增的物业存在于下拉选项中(物业名称)
        self.log_step("验证新增物业成功-下拉选项中存在新增的物业")

    @pytest.mark.parametrize(
        "区域, 物业名称, 办公地址, 联系人, 联系人电话",
        [
            ("", "万科物业", "安徽省合肥市蜀山区大蜀山地铁口旁财富大楼14层1403号",
             "石童涛", "13955499272"),
            ("中电数智街道/中电数智社区（测试）", "", "安徽省合肥市蜀山区大蜀山地铁口旁财富大楼14层1403号",
             "石童涛", "13955499272"),
            ("中电数智街道/中电数智社区（测试）", "万科物业", "",
             "石童涛", "13955499272"),
            ("中电数智街道/中电数智社区（测试）", "万科物业", "安徽省合肥市蜀山区大蜀山地铁口旁财富大楼14层1403号",
             "", "13955499272"),
            ("中电数智街道/中电数智社区（测试）", "万科物业", "安徽省合肥市蜀山区大蜀山地铁口旁财富大楼14层1403号",
             "石童涛", "")

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
    @allure.step("测试新增物业-失败-必填项缺失")
    def test_add_property_miss_data(self, 小区信息页面, 区域, 物业名称, 办公地址, 联系人, 联系人电话):
        # 点击新增按钮
        小区信息页面.点击新增按钮()
        self.log_step("点击新增按钮")

        小区信息页面.点击物业新增按钮()
        self.log_step("点击物业新增按钮")
        # 填写表单信息
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(区域=区域, 物业名称=物业名称, 办公地址=办公地址,
                                                                    联系人=联系人, 联系人电话=联系人电话)
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(备注=备注)
        self.log_step("填写表单信息")
        # 点击提交按钮
        小区信息页面.click_button("确定", 按钮的父元素=小区信息页面.page.locator('//div[@aria-label="新增物业信息"]'))
        self.log_step("点击提交按钮")
        # 断言操作成功字样在页面出现
        assert not 小区信息页面.page.get_by_text("添加成功").is_visible()
        小区信息页面.验证新增物业信息_失败_必填项缺失()
        self.log_step("验证新增物业失败-必填项缺失-页面提示信息")

    @pytest.mark.usefixtures("后置操作_刷新页面")
    @allure.step("测试新增物业-前端格式校验与数据合法性")
    def test_add_property_frontend_validation(
            self, 小区信息页面
    ):
        # 点击新增按钮
        小区信息页面.点击新增按钮()
        self.log_step("点击新增按钮")

        小区信息页面.点击物业新增按钮()
        self.log_step("点击物业新增按钮")

        对话框_新增物业信息 = 小区信息页面.获取新增物业信息对话框()

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="138001")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="1380013890a")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="1380013890@")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="138 001 3890")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="138-001-3890")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 手机号不以1开头
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="23800138900")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 第二位不是3/5/6/7/8/9
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="11000138900")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 手机号全为同一个数字
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="11111111111")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 刚好11位但不符合规则的最小数字
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="10000000000")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 刚好11位但不符合规则的最大数字
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="99999999999")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 输入国际电话号码
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="+861012345678")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 输入不存在的区号
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="999-1234567")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 输入区号，但缺少号码
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="010-")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 输入号码，但缺少区号
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="1234567")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 使用不支持的格式分隔符
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="010/12345678")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 使用不支持的格式分隔符
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="010.1234")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 输入非数字区号
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="0AB-1234567")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")

        # 输入非数字号码
        小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(联系人电话="010-ABCDEF7")
        self.log_step("填写手机号码")
        expect(小区信息页面.page.get_by_text("请输入正确的联系格式")).to_be_visible()
        self.log_step("断言页面提示信息-手机号码")


@pytest.mark.usefixtures("小区信息页面")  # 显式声明夹具
class TestEditMeetingRoom(BaseCase):
    @pytest.mark.parametrize(
        "room_name, room_code, capacity, location, status, devices, departments, manager, description, need_approval, approval_person, need_time_limit, days, start_time, end_time, max_duration, users, is_positive",

        [
            ("修改-成功", "HYS10-506", "10", "天王巷", "正常", ["投影仪"],
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
             "刘富豪/17356523872", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], True),
            # 添加更多测试数据集
        ],
        # ids=["修改-成功"]
    )
    @allure.step("测试修改会议室")
    def test_edit_meeting_room_success(self, meeting_room_manage_edit_and_del_pre, db_connection, room_name, room_code,
                                       capacity, location, status,
                                       devices,
                                       departments, manager, description, need_approval, approval_person,
                                       need_time_limit, days,
                                       start_time,
                                       end_time, max_duration, users, is_positive):
        # 对于正向用例，生成一段随机数字，6位的，插入到会议室名称和编号的尾部
        random_code = str(random.randint(10000, 99999))
        room_name = room_name + random_code
        room_code = room_code + random_code
        meeting_room_info_page = meeting_room_manage_edit_and_del_pre.click_edit_button()
        self.log_step("点击编辑按钮")
        meeting_room_info_page.fill_basic_info(room_name, room_code, capacity, location, status, devices, departments,
                                               manager, description)
        self.log_step("填写基本信息")
        meeting_room_info_page.fill_high_level_info(need_approval, approval_person, need_time_limit, days, start_time,
                                                    end_time, max_duration, users)
        self.log_step("填写高级信息")
        meeting_room_info_page.click_submit_button()
        self.log_step("点击提交按钮")
        # 等待1秒
        meeting_room_manage_edit_and_del_pre.page.wait_for_timeout(1000)
        # 重新连接数据库，并提交事务
        db_connection.ping(reconnect=True)
        db_connection.commit()  # 提交事务确保可见，必须加上这段代码，否则读取到的数据数仍然是修改之前的
        # 执行sql查询，断言一定能查到修改后的数据
        db_data = meeting_room_manage_edit_and_del_pre.get_db_data(db_connection,
                                                                   "SELECT count(*) as count FROM meeting_room WHERE name = %(room_name)s and number = %(room_code)s and del_flag = 0",
                                                                   {"room_name": room_name, "room_code": room_code})
        count = db_data[0]["count"]
        meeting_room_info_page.verify_edit_success_message(count)
        self.log_step("验证修改成功")

    @pytest.mark.parametrize(
        "room_name, room_code, capacity, location, status, devices, departments, manager, description, need_approval, approval_person, need_time_limit, days, start_time, end_time, max_duration, users, is_positive",

        [
            ("", "HYS10-506", "10", "天王巷", "正常", ["投影仪"],
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
             "刘富豪/17356523872", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            ("编辑-失败-必填项为空-容纳人数", "HYS10-506", "", "天王巷", "正常", ["投影仪"],
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
             "刘富豪/17356523872", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            ("编辑-失败-必填项为空-会议室位置", "HYS10-506", "10", "", "正常", ["投影仪"],
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
             "刘富豪/17356523872", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            ("编辑-失败-必填项为空-会议室状态", "HYS10-506", "10", "天王巷", "", ["投影仪"],
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
             "刘富豪/17356523872", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            ("编辑-失败-必填项为空-会议室设备", "HYS10-506", "10", "天王巷", "正常", "",
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
             "刘富豪/17356523872", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            ("编辑-失败-必填项为空-管理部门和管理人和审批人", "HYS10-506", "10", "天王巷", "正常", ["投影仪"],
             "", "", "会议室很大，能容纳很多人", True, "", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            ("编辑-失败-必填项为空-管理人", "HYS10-506", "10", "天王巷", "正常", ["投影仪"],
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "", "会议室很大，能容纳很多人", True,
             "刘富豪/17356523872", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            ("编辑-失败-必填项为空-审批人", "HYS10-506", "10", "天王巷", "正常", ["投影仪"],
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
             "", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            ("编辑-失败-必填项为空-可预约的时间范围", "HYS10-506", "10", "天王巷", "正常", ["投影仪"],
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
             "刘富豪/17356523872", True,
             "", "08:30", "10:30", "24",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            ("编辑-失败-必填项为空-单次可预约最长时间", "HYS10-506", "10", "天王巷", "正常", ["投影仪"],
             ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
             "刘富豪/17356523872", True,
             ["星期一", "星期二", "星期三"], "08:30", "10:30", "",
             ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], False),
            # 添加更多测试数据集
        ],
        # ids=[
        #      "修改-失败-必填项为空-会议室名称",
        #      "修改-失败-必填项为空-容纳人数",
        #      "修改-失败-必填项为空-会议室位置",
        #      "修改-失败-必填项为空-会议室状态",
        #      '修改-失败-必填项为空-会议室设备',
        #      '修改-失败-必填项为空-管理部门',
        #      '修改-失败-必填项为空-管理人',
        #      '修改-失败-必填项为空-审批人',
        #      '修改-失败-必填项为空-可预约的时间范围',
        #      '修改-失败-必填项为空-单次可预约最长时间',
        #      ]
    )
    @allure.step("测试修改会议室-必填项缺失")
    def test_edit_meeting_room_miss_data(self, meeting_room_manage_edit_and_del_pre, db_connection, room_name,
                                         room_code,
                                         capacity, location, status,
                                         devices,
                                         departments, manager, description, need_approval, approval_person,
                                         need_time_limit, days,
                                         start_time,
                                         end_time, max_duration, users, is_positive):
        meeting_room_info_page = meeting_room_manage_edit_and_del_pre.click_edit_button()
        self.log_step("点击编辑按钮")
        meeting_room_info_page.fill_basic_info(room_name, room_code, capacity, location, status, devices, departments,
                                               manager, description)
        self.log_step("填写基本信息")
        meeting_room_info_page.fill_high_level_info(need_approval, approval_person, need_time_limit, days, start_time,
                                                    end_time, max_duration, users)
        self.log_step("填写高级信息")
        meeting_room_info_page.click_submit_button()
        self.log_step("点击提交按钮")
        meeting_room_info_page.verify_error_edit_miss_message()
        self.log_step("验证修改失败-必填项缺失")

    @allure.step("测试修改会议室-前端格式校验与数据合法性")
    def test_edit_meeting_room_frontend_validation(
            self, meeting_room_manage_edit_and_del_pre, db_connection,
    ):
        meeting_room_info_page = meeting_room_manage_edit_and_del_pre.click_edit_button()
        self.log_step("点击编辑按钮")

        meeting_room_info_page.fill_room_name_by_press("新增会议室名称过长示例" * 2)
        self.log_step("填写会议室名称")
        meeting_room_name = meeting_room_info_page.get_room_name()
        assert len(meeting_room_name) <= 10
        self.log_step("校验会议室名称长度小于等于10")

        meeting_room_info_page.fill_room_code_by_press("HYS10-506" * 4)
        self.log_step("填写会议室编号")
        meeting_room_code = meeting_room_info_page.get_room_code()
        assert len(meeting_room_code) <= 30
        self.log_step("校验会议室编号长度小于等于30")

        meeting_room_info_page.fill_capacity_by_press("1001")
        self.log_step("填写会议室容量")
        assert meeting_room_info_page.get_capacity() == "1000"
        self.log_step("校验会议室容量小于等于1000")

        meeting_room_info_page.fill_capacity_by_press("3.4")
        self.log_step("填写会议室容量")
        assert meeting_room_info_page.get_capacity() == "34"
        self.log_step("校验会议室容量无法输入小数")

        meeting_room_info_page.fill_capacity_by_press("3/4")
        self.log_step("填写会议室容量")
        assert meeting_room_info_page.get_capacity() == "34"
        self.log_step("校验会议室容量无法输入分数")

        meeting_room_info_page.fill_capacity_by_press("-1")
        self.log_step("填写会议室容量")
        assert meeting_room_info_page.get_capacity() == "1"
        self.log_step("校验会议室容量无法输入负数")

        meeting_room_info_page.fill_capacity_by_press("abc")
        self.log_step("填写会议室容量")
        assert meeting_room_info_page.get_capacity() == ""
        self.log_step("校验会议室容量无法输入字母")

        meeting_room_info_page.fill_capacity_by_press("￥￥￥￥￥")
        self.log_step("填写会议室容量")
        assert meeting_room_info_page.get_capacity() == ""
        self.log_step("校验会议室容量无法输入特殊字符")

        meeting_room_info_page.fill_capacity_by_press("中文")
        self.log_step("填写会议室容量")
        assert meeting_room_info_page.get_capacity() == ""
        self.log_step("校验会议室容量无法输入中文")

        meeting_room_info_page.fill_location_by_press("天王巷" * 15)
        self.log_step("填写会议室位置")
        assert len(meeting_room_info_page.get_location()) <= 40
        self.log_step("校验会议室位置长度小于等于40")

        meeting_room_info_page.toggle_time_limit(True, None, None, None, "25")
        self.log_step("填写可预约最长时间")
        assert meeting_room_info_page.get_max_duration() == "24"
        self.log_step("校验可预约最长时间小于等于24")

        meeting_room_info_page.fill_max_duration_by_press("3/4")
        self.log_step("填写可预约最长时间")
        assert meeting_room_info_page.get_max_duration() == "24"
        self.log_step("校验可预约最长时间无法输入分数")

        meeting_room_info_page.fill_max_duration_by_press("-1")
        self.log_step("填写可预约最长时间")
        assert meeting_room_info_page.get_max_duration() == "1"
        self.log_step("校验可预约最长时间无法输入负数")

        meeting_room_info_page.fill_max_duration_by_press("abc")
        self.log_step("填写可预约最长时间")
        assert meeting_room_info_page.get_max_duration() == ""
        self.log_step("校验可预约最长时间无法输入字母")

        meeting_room_info_page.fill_max_duration_by_press("$$$$")
        self.log_step("填写可预约最长时间")
        assert meeting_room_info_page.get_max_duration() == ""
        self.log_step("校验可预约最长时间无法输入特殊字符")

        meeting_room_info_page.fill_max_duration_by_press("中文")
        self.log_step("填写可预约最长时间")
        assert meeting_room_info_page.get_max_duration() == ""
        self.log_step("校验可预约最长时间无法输入中文")


# def get_department_ids(db_connection, department_names):
#     """
#     根据部门名称列表获取对应的部门 ID 列表。
#     """
#     # 判断部门名称列表是否为空或非列表类型
#     if not department_names or not isinstance(department_names, list):
#         return []
#
#     # 构造参数化 SQL 查询
#     placeholders = "%s"
#     sql = f"""
#         SELECT dept_id
#         FROM sys_dept
#         WHERE dept_name IN ({placeholders}) AND status = '0' AND del_flag = '0'
#     """
#
#     # 使用参数化查询防止 SQL 注入，执行查询
#     results = db_connection.execute_query(sql, params=department_names[-1])
#     # 查询结果是一个列表，每个元素是一个字典，包含一个字段，需要将内容转换为列表
#     dept_ids = [row["dept_id"] for row in results]
#     return dept_ids

字典_小区类型 = {
    "商业": "1",
    "自营": "2",
    "单位小区": "3",
    "回迁": "4",
    "三无": "5",
    "城中村": "6",
    "自然村": "7",
    "园区":"8",
    "商圈": "9"
}

字典_管理类别 = {
    "物管小区":"WGXQ",
    "社区代管":"SQDG",
    "自管小区":"ZGXQ"
}


def build_query_sql(小区类型=None, 管理类别=None, 小区名称=None):
    """
    根据给定参数动态生成小区查询 SQL。
    """
    sql = """
            SELECT a.*,b.xm as wyxm,b.sjhm as wysjhm FROM base_village a 
            LEFT JOIN ( SELECT * FROM base_village_staff WHERE id in ( SELECT max(id) FROM base_village_staff WHERE ryjsdm = "0101" OR ryjsdm = "01" GROUP BY xqbm)) b 
            ON a.xqbm = b.xqbm where a.sqdm like '%%340103225%%' and a.type = %(小区类型)s
        """

    # 存放动态条件列表和参数字典
    conditions = []
    params = {}

    if 小区类型 is not None and 小区类型 != "全部":
        小区类型 =  字典_小区类型[小区类型]
        # 添加小区类型条件
        conditions.append(f"and a.type = %(小区类型)s")
        # 添加参数
        params["小区类型"] = f"{小区类型}"

    if 管理类别 is not None and 管理类别 != "全部":
        管理类别 = 字典_管理类别[管理类别]
        conditions.append("and a.gllb = %(管理类别)s ")
        params["管理类别"] = f"{管理类别}"

    if 小区名称 is not None:
        conditions.append("AND a.xqmc LIKE CONCAT('%', %(小区名称)s,'%' )")
        params["小区名称"] = f"{小区名称}"


    # 拼接sql
    sql += " " + " ".join(conditions)
    sql += ' ORDER BY IFNULL(b.ryjsdm, 0) desc'


    return sql, params


class TestQuery(BaseCase):

    @pytest.mark.usefixtures("后置操作_重置查询条件")
    @pytest.mark.parametrize(
        "小区类型, 管理类别, 小区名称",
        [
            # (None, None, None),
            # ("商业", None, None),
            # (None, "物管小区", None),
            # (None, None, "天王巷小区"),
            # (None, None, "金城"),
            # ("商业", "物管小区", None),
            ("商业", None, "安徽数字生活"),
            # (None , "物管小区", "安徽数字工作"),
            # ("自营" , "物管小区", "安徽数字"),
        ]
    )
    def test_query(self, 小区信息页面, db_connection, 小区类型, 管理类别, 小区名称):
        # # 输入查询条件
        # 小区信息页面.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区类型=小区类型, 管理类别=管理类别,
        #                                                             小区名称=小区名称)
        # self.log_step("输入查询条件")
        #
        # # 点击查询按钮
        # 小区信息页面.click_button("搜索")
        # self.log_step("点击查询按钮")
        # # 等待查询结果加载
        # 小区信息页面.page.wait_for_timeout(2000)  # 等待 2 秒
        # self.log_step("等待查询结果加载")
        # pages_data, pages_data_count = 小区信息页面.get_table_data()
        # # print(pages_data)
        # self.log_step("获取所有页面的表格数据")

        # 构建 SQL 查询
        sql, params = build_query_sql(小区类型=小区类型, 管理类别=管理类别, 小区名称=小区名称, )

        # 根据sql语句和参数，从数据库中提取数据
        db_data = 小区信息页面.get_db_data(db_connection, query=sql, params=params)
        self.log_step("从数据库中提取数据")

        # 比较两个数据集
        # assert 小区信息页面.compare_data(pages_data, db_data,
        #                                  ['xqmc']), "页面数据与数据库数据不一致"
        self.log_step("比较两个数据集")


class TestDeleteMeetingRoom(BaseCase):
    def test_delete_meeting_room(self, meeting_room_manage_edit_and_del_pre, db_connection):
        # 从数据库中统计状态为删除的数据条数
        db_data_pre = meeting_room_manage_edit_and_del_pre.get_db_data(
            db_connection,
            query="SELECT count(*) as count FROM meeting_room WHERE del_flag = '1'",
        )
        db_count_pre = db_data_pre[0]["count"]
        _, count_pre = meeting_room_manage_edit_and_del_pre.get_table_data()
        self.log_step("统计删除操作前表格行数")
        meeting_room_manage_edit_and_del_pre.click_delete_button()
        self.log_step("点击删除按钮,弹窗后点击确定按钮")
        meeting_room_manage_edit_and_del_pre.verify_delete_success_message()
        self.log_step("验证页面出现删除成功字样")
        # 等待1秒
        meeting_room_manage_edit_and_del_pre.page.wait_for_timeout(1000)
        _, count_after = meeting_room_manage_edit_and_del_pre.get_table_data()
        self.log_step("统计删除成功操作后表格行数")
        # 断言：表格中的行数减1
        assert count_after == count_pre - 1, "表格中的行数未减少"
        # 验证数据库中的数据是否已删除（或标记为已删除）
        db_connection.ping(reconnect=True)  # 确保数据库连接有效
        db_connection.commit()
        db_data_after = meeting_room_manage_edit_and_del_pre.get_db_data(
            db_connection,
            query="SELECT count(*) as count FROM meeting_room WHERE del_flag = '1'",
        )
        db_count_after = db_data_after[0]["count"]
        # 断言：数据库中状态为已删除的数据多了1条
        assert db_count_after == db_count_pre + 1, "数据库中的数据未删除"
        self.log_step("验证数据库中的数据是否已删除")

    def test_delete_meeting_room_cancel(self, meeting_room_manage_edit_and_del_pre, db_connection):
        # 从数据库中统计状态为删除的数据条数
        db_data_pre = meeting_room_manage_edit_and_del_pre.get_db_data(
            db_connection,
            query="SELECT count(*) as count FROM meeting_room WHERE del_flag = '1'",
        )
        db_count_pre = db_data_pre[0]["count"]
        # 点击删除按钮之前，表格中的行数
        _, count_pre = meeting_room_manage_edit_and_del_pre.get_table_data()
        self.log_step("统计删除操作前表格行数")
        meeting_room_manage_edit_and_del_pre.click_delete_button_cancel()
        self.log_step("点击删除按钮，弹窗后点击取消按钮")
        # 点击删除按钮之后，表格中的行数
        _, count_after = meeting_room_manage_edit_and_del_pre.get_table_data()
        self.log_step("统计删除取消操作后表格行数")
        meeting_room_manage_edit_and_del_pre.verify_delete_cancel_message(count_pre, count_after)
        self.log_step("验证删除取消")
        # 等待1秒
        meeting_room_manage_edit_and_del_pre.page.wait_for_timeout(1000)
        # 验证数据库中的数据是否已删除（或标记为已删除）
        db_connection.ping(reconnect=True)  # 确保数据库连接有效
        db_connection.commit()
        # 统计数据库中状态为已删除的数据条数
        db_data_after = meeting_room_manage_edit_and_del_pre.get_db_data(
            db_connection,
            query="SELECT count(*) as count FROM meeting_room WHERE del_flag = '1'",
        )
        db_count_after = db_data_after[0]["count"]
        # 断言：数据库中状态为已删除的数据条数未改变
        assert db_count_after == db_count_pre, "数据库中的数据被误删除"
