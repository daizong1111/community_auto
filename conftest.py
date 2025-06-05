import pytest
from playwright.sync_api import Playwright, sync_playwright, Page
from pages.login_page import LoginPage
from pages.home_page import HomePage
import logging
import mysql.connector
import pymysql
from pages.meeting_room_manage.meeting_room_manage_page import MeetingRoomManagePageBase
from tests.test_meeting_manage.test_meeting_room_manage import TestAddMeetingRoom

"""存放UI自动化测试过程中用到的测试夹具"""

# 测试夹具-获取浏览器当前打开页面，并返回 MeetingRoomManagePageBase 对象
@pytest.fixture(scope="function")
def 浏览器已打开的页面():
    with sync_playwright() as playwright:
        # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        # 通过ip和端口连接到已经打开的chromium浏览器
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(6000)  # 设置默认超时时间为 4000 毫秒
        # # 创建小区信息页面对象
        # page = PageFloor(page)
        # 返回会议室管理页面对象
        yield page

# 定义Playwright fixture，用于初始化Playwright实例
@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p

# page fixture，用于每条测试用例单独打开浏览器
@pytest.fixture(scope="session")
def page(playwright):
    logging.info("Starting browser...") # 打印日志
    browser = playwright.chromium.launch(headless=False)  # 启动浏览器，有头模式，也就是能看到页面的那种
    logging.info("Browser started.") # 打印日志
    context = browser.new_context()  # 创建新的浏览器上下文
    page = context.new_page() # 打开新页面
    page.set_default_timeout(7000) # 设置超时时间为7秒
    yield page #  返回页面对象
    page.close()  # 关闭页面
    browser.close()  # 关闭浏览器

# 登录的前置操作
@pytest.fixture(scope="session")
def logged_in_page(page: Page):
    login_page = LoginPage(page) # 创建登录页面对象
    login_page.goto() # 跳转到登录页面
    login_page.fill_username("admin") # 填写用户名
    login_page.fill_password("Djmysqltest@2023") # 填写密码
    # login_page.fill_password("Lzs@1991070214")
    login_page.fill_captcha() # 填写验证码
    login_page.click_login() # 点击登录按钮
    yield login_page # 返回登录页面对象

# @pytest.fixture(scope="session")
# def home_page(logged_in_page):
#     home_page = HomePage(logged_in_page.page)
#     yield home_page

# 前置操作-创建会议室管理页面对象
@pytest.fixture(scope="module")
def meeting_manage_page(logged_in_page):
    meeting_manage_page = MeetingRoomManagePageBase(logged_in_page.page) # 创建会议室管理页面对象
    yield meeting_manage_page # 返回会议室管理页面对象

# @pytest.fixture(scope="function")
# def meeting_room_manage_page(meeting_manage_page):
#     # meeting_manage_page.locator("//span[text()='会议室管理']").click()
#     # 点击会议室管理菜单项
#     meeting_manage_page.locator("//ul[@role='menubar']/div[3]").click()
#     yield MeetingRoomManagePageBase(meeting_manage_page)
#     # # 清理逻辑：确保返回到会议室管理首页
#     # try:
#     #     meeting_manage_page.locator("//ul[@role=’menubar‘]/div[3]").click()
#     # except Exception as e:
#     #     logging.error(f"清理逻辑执行失败: {e}")

# 返回数据库连接，给所有的测试用例公用，所有的测试用例都执行完之后，自动关闭数据库连接
@pytest.fixture(scope="session")
def db_connection():
   # 创建数据库连接
   # db_config = {
   #     "host": "114.96.83.242",
   #     "port": "8306",
   #     "user": "root",
   #     "password": "Dxjc@2020",
   #     "database": "chinaictc_sc_common_pre"
   # }
   # connection = mysql.connector.connect(**db_config)
   connection = pymysql.connect(
       host="114.96.83.242",
       user="root",
       port=8306,
       password="Dxjc@2020",
       database="chinaictc_sc_common_pre",
       cursorclass=pymysql.cursors.DictCursor  # 如果你需要字典格式结果
   )
   yield connection  # 返回连接对象
   # 测试结束后关闭连接
   connection.close()

# # 前置操作-用于测试编辑和删除功能，保证表格中一定有数据
# @pytest.fixture(scope="function")
# def 小区信息页面(meeting_room_manage_page, db_connection):
#     # 等待3秒，防止表格尚未加载出来，导致计算出的表格行数为0
#     meeting_room_manage_page.page.wait_for_timeout(3000)
#     # 统计表格行数
#     rows_count = meeting_room_manage_page.get_table_rows().count()
#     if rows_count == 0:
#         # 新增一条数据
#         test_add_meeting_room = TestAddMeetingRoom()
#         test_add_meeting_room.test_add_meeting_room_success(meeting_room_manage_page, db_connection, "新增-成功", "HYS10-506", "10", "天王巷", "正常", ["投影仪"],
#              ["集成公司", "省DICT研发中心", "项目管理办公室"], "刘富豪/17356523872", "会议室很大，能容纳很多人", True,
#              "刘富豪/17356523872", True,
#              ["星期一", "星期二", "星期三"], "08:30", "10:30", "24",
#              ["集成公司", "省DICT研发中心", "项目管理办公室", "刘富豪"], True)
#     yield meeting_room_manage_page


@pytest.fixture(scope="function")
def 后置操作_刷新页面(浏览器已打开的页面):
    yield 浏览器已打开的页面
    # 刷新
    浏览器已打开的页面.reload()

@pytest.fixture(scope="function")
def 后置操作_重置查询条件(小区信息页面):
    yield 小区信息页面
    # 执行完用例之后，点击重置按钮，清空查询条件
    小区信息页面.click_reset_btn()


