import re

import pytest
from joblib.testing import timeout
from playwright.sync_api import sync_playwright, Playwright, Page, expect

from module.BasePageNew import PageObject
from module.base_query_page import BaseQueryPage
import pymysql
import allure
import time

from pages.login_page_h5 import LoginPageH5
from pages.login_page_pc import LoginPagePc
from pages.pages_h5.首页 import PageHome
from pages.pages_h5.个人中心 import PagePersonalCenter

# 导入用户配置信息，以字典形式保存
from user_data import USERS_BY_ROLE

# 存放角色到page的映射
role_to_page = {}

"""存放UI自动化测试过程中用到的测试夹具"""


# 定义Playwright fixture，用于初始化Playwright实例
@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p


# # 测试夹具-获取浏览器当前打开页面
# @pytest.fixture(scope="session")
# def browser(playwright):
#     # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
#     # 通过ip和端口连接到已经打开的chromium浏览器
#     browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
#     yield browser

# 测试夹具-获取浏览器当前打开页面
@pytest.fixture(scope="session")
def browser(playwright):
    # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    # 通过ip和端口连接到已经打开的chromium浏览器
    # browser = playwright.chromium.launch(headless=False,args=['--start-maximized'])  # 启动浏览器
    browser = playwright.chromium.launch(
        headless=False,
        args=["--window-size=1920,1080"]  # 设置窗口大小
    )
    yield browser
    browser.close()  # 关闭浏览器


# 测试夹具-启动新的浏览器
# 测试夹具 - 使用 browser fixture 创建 context 并应用 iPhone 13 设备配置
@pytest.fixture(scope="session")
def page_h5(playwright, browser):
    # 获取 iPhone 13 设备参数
    iphone_13 = playwright.devices['iPhone 13']
    # 使用传入的 browser 实例创建一个新的 context，并应用 iPhone 13 的设备参数
    context = browser.new_context(**iphone_13)
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(10000)  # 设置全局默认超时时间为 10 秒
    yield page
    page.close()  # 关闭页面
    context.close()  # 关闭上下文


@pytest.fixture(scope="session")
def page_pc(browser):
    # 使用传入的 browser 实例创建一个新的 context，并应用 iPhone 13 的设备参数
    # context = browser.new_context(no_viewport=True)
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    yield page
    page.close()  # 关闭页面
    context.close()  # 关闭上下文


# 登录的前置操作
# @pytest.fixture(scope="session")
# def logged_in_page_pc(page_pc: Page):
#     login_page = LoginPagePc(page_pc)
#     login_page.goto()
#     login_page.fill_account("wgy017916")
#     login_page.fill_password("dxnb66@2024_")
#     login_page.fill_captcha("202208")
#     login_page.check()
#     login_page.click_login()
#     page_pc.wait_for_timeout(2000)
#     yield page_pc


# @pytest.fixture(scope="session")
# def logged_in_page_h5(page_h5: Page):
#     login_page = LoginPageH5(page_h5)
#     login_page.goto()
#     login_page.fill_account("wgy017916")
#     login_page.fill_password("dxnb66@2024_")
#     login_page.fill_captcha("202208")
#     login_page.check()
#     login_page.click_login()
#     page_h5.wait_for_timeout(2000)
#     yield page_h5

@pytest.fixture(scope="session")
def page_h5_居民(page_h5: Page):
    login_page = LoginPageH5(page_h5)
    login_page.goto()
    login_page.同意登录()
    login_page.登录(USERS_BY_ROLE['居民']['phone_number'], '22', '202208')
    # page_h5.wait_for_timeout(2000)
    # 登录后跳转到首页
    home_page = PageHome(page_h5)
    home_page.跳转到个人中心()
    # 跳转到个人中心，并选择角色
    page_personal_center = PagePersonalCenter(page_h5)
    page_personal_center.选择角色("居民")
    role_to_page['居民'] = page_h5
    yield page_h5


@pytest.fixture(scope="session")
def page_pc_物业管理员1(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['物业管理员1']['username'], USERS_BY_ROLE['物业管理员1']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("物业服务", "事件管理")
    role_to_page['物业管理员1'] = page
    yield page

@pytest.fixture(scope="session")
def page_pc_物业管理员2(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['物业管理员2']['username'], USERS_BY_ROLE['物业管理员2']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("物业服务", "事件管理")
    role_to_page['物业管理员2'] = page
    yield page

@pytest.fixture(scope="session")
def page_pc_物业工作人员(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['物业工作人员']['username'], USERS_BY_ROLE['物业工作人员']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("物业服务", "事件管理")
    role_to_page['物业工作人员'] = page
    yield page

@pytest.fixture(scope="session")
def page_pc_三级网格员(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['三级网格员']['username'], USERS_BY_ROLE['三级网格员']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("网格管理", "事件管理")
    role_to_page['三级网格员'] = page
    yield page

@pytest.fixture(scope="session")
def page_pc_二级网格员(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['二级网格员']['username'], USERS_BY_ROLE['二级网格员']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("网格管理", "事件管理")
    role_to_page['二级网格员'] = page
    yield page

@pytest.fixture(scope="session")
def page_pc_一级网格员(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['一级网格员']['username'], USERS_BY_ROLE['一级网格员']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("网格管理", "事件管理")
    role_to_page['一级网格员'] = page
    yield page

# 监听页面的请求
# def requests(request):
#     """监听请求"""
#     if request.url == "cccc":
#         return
#     print("============================================")
#     print(f"请求：{request.url}")
#     print(f"请求头：{request.headers}")
#     print("============================================")
def slow_response(route, request):
    # 延迟请求处理，模拟高延迟网络
    print("请求开始处理...")
    time.sleep(1)  # 5000ms 延迟

    # 可选：修改响应体大小，模拟低带宽
    route.continue_()
    # 如果你需要截获并修改响应内容：
    # response = route.fetch()
    # body = response.json()
    # 自定义返回数据，例如裁剪大文件等
    # route.fulfill(response=response, json=body)


@pytest.fixture(scope="module")
def 浏览器已打开的页面(browser):
    # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    # 模拟弱网环境
    # 拦截所有请求，模拟网络延迟
    # context.route(re.compile(r"https?://.*"), slow_response)
    # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
    page = context.pages[0] if context.pages else context.new_page()
    page.set_default_timeout(6000)  # 设置默认超时时间为 4000 毫秒

    # page.on("response", requests)

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
    # expect(查询页面.page.get_by_text("加载中")).not_to_be_visible(timeout=5000)
    expect(查询页面.page.locator(".el-loading-spinner").locator("visible=true")).not_to_be_visible(timeout=5000)
    # 等待网络请求完成
    # 查询页面.page.wait_for_load_state("networkidle")
