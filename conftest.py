import pytest
from playwright.sync_api import sync_playwright, Playwright, Page, expect

from module.base_query_page import BaseQueryPage
import pymysql
import allure
import time

"""存放UI自动化测试过程中用到的测试夹具"""

# 定义Playwright fixture，用于初始化Playwright实例
@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p

# page fixture，用于每条测试用例单独打开浏览器
@pytest.fixture(scope="function")
def page(playwright):
    browser = playwright.chromium.launch(headless=False)  # 启动浏览器
    context = browser.new_context()  # 创建新的浏览器上下文
    page = context.new_page()  # 打开新页面
    yield page
    page.close()  # 关闭页面
    browser.close()  # 关闭浏览器


# 登录的前置操作
# @pytest.fixture(scope="function")
# def logged_in_page(page: Page):
#     login_page = LoginPage(page)
#     login_page.goto()
#     login_page.fill_email("121292679@qq.com")
#     login_page.fill_password("a546245426")
#     login_page.click_login()
#     page.wait_for_timeout(2000)
#     yield page
# 测试夹具-获取浏览器当前打开页面，并返回 MeetingRoomManagePageBase 对象
@pytest.fixture(scope="session")
def browser(playwright):
    # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    # 通过ip和端口连接到已经打开的chromium浏览器
    browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
    yield browser


# 测试夹具-获取浏览器当前打开页面，并返回 MeetingRoomManagePageBase 对象
# @pytest.fixture(scope="function")
# def 浏览器已打开的页面(playwright):
#     # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
#     # 通过ip和端口连接到已经打开的chromium浏览器
#     browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
#     # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
#     context = browser.contexts[0] if browser.contexts else browser.new_context()
#     # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
#     page = context.pages[0] if context.pages else context.new_page()
#     page.set_default_timeout(6000)  # 设置默认超时时间为 4000 毫秒
#     # # 创建小区信息页面对象
#     # page = PageFloor(page)
#     # 返回会议室管理页面对象
#     yield page

@pytest.fixture(scope="module")
def 浏览器已打开的页面(browser):
    # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
    page = context.pages[0] if context.pages else context.new_page()
    page.set_default_timeout(6000)  # 设置默认超时时间为 4000 毫秒
    yield page

# 用例运行失败自动截图
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        try:
            for context in item.funcargs['browser'].contexts:
                for page in context.pages:
                    if page.is_closed():
                        continue
                    # 开始截图并统计耗时
                    try:
                        screenshot_start = time.time()
                        bytes_png = page.screenshot(timeout=10000, full_page=True)
                        screenshot_end = time.time()
                        duration_ms = (screenshot_end - screenshot_start) * 1000
                        print(f"截图成功，耗时: {duration_ms:.2f} ms")

                        # 将截图添加到 Allure 报告
                        allure.attach(
                            bytes_png,
                            name=f"失败截图 - {page.title()}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    except Exception as e:
                        # 截图失败时记录异常，并附加错误信息到报告
                        error_msg = f"❌ 页面 '{page.title()}' 截图失败: {str(e)}"
                        allure.attach(
                            error_msg,
                            name="截图失败原因",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        print(error_msg)
                    #
                    # bytes_png = page.screenshot(timeout=10000, full_page=True)
                    # allure.attach(bytes_png, f"失败截图---{page.title()}")

        except Exception as e:
            # 其他错误处理（如 browser 不存在）
            error_msg = f"🚨 截图失败（全局）: {str(e)}"
            allure.attach(
                error_msg,
                name="截图失败原因（全局）",
                attachment_type=allure.attachment_type.TEXT
            )
            print(error_msg)
            ...

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

@pytest.fixture(scope="module")
def 查询页面(浏览器已打开的页面):
    查询页面 = BaseQueryPage(浏览器已打开的页面)
    yield 查询页面

@pytest.fixture(scope="function")
def 后置操作_刷新页面(浏览器已打开的页面):
    yield 浏览器已打开的页面
    # 刷新
    浏览器已打开的页面.reload()
    # 等待网络请求完成
    expect(浏览器已打开的页面.get_by_text("系统加载中")).not_to_be_visible(timeout=5000)

@pytest.fixture(scope="function")
def 后置操作_重置查询条件(查询页面):
    yield 查询页面
    # 执行完用例之后，点击重置按钮，清空查询条件
    查询页面.click_reset_btn()
    expect(查询页面.page.get_by_text("加载中")).not_to_be_visible(timeout=5000)
    # 等待网络请求完成
    # 查询页面.page.wait_for_load_state("networkidle")





