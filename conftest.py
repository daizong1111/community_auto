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
from module.base_query_page_new import BaseQueryPage

# 导入用户配置信息，以字典形式保存
from user_data import USERS_BY_ROLE

# 处理页面水合现象需要使用的包
import hashlib
import shutil
import os
import sys
import time
from pathlib import Path
from utils.GetPath import get_path
from filelock import FileLock
from playwright._impl._locator import Locator as LocatorImpl
from playwright._impl._sync_base import mapping
from playwright.sync_api._generated import Locator as _Locator
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Optional,
    cast,
)
import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Error,
    Page,
    Playwright,
    expect,
    BrowserType,
)
from pytest_playwright.pytest_playwright import CreateContextCallback, _build_artifact_test_folder
from slugify import slugify
import tempfile
import allure
import re
from utils.globalMap import GlobalMap
import json
from allure import step
api_Count = []
time_out = 0

# 存放角色到page的映射
role_to_page = {}

"""存放UI自动化测试过程中用到的测试夹具"""
# 定义Playwright fixture，用于初始化Playwright实例
@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p


# 设置浏览器分辨率
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 600,
            "height": 800
        },
        "record_video_dir": {
            "width": 1440,
            "height": 900
        },
    }

# 测试夹具-获取已经打开的浏览器
@pytest.fixture(scope="session")
def browser_opened(playwright):
    # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    # 通过ip和端口连接到已经打开的chromium浏览器
    browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
    yield browser


# 测试夹具-打开新的浏览器
@pytest.fixture(scope="session")
def browser(playwright):
    # 通过ip和端口连接到已经打开的chromium浏览器
    # browser = playwright.chromium.launch(headless=False,args=['--start-maximized'])  # 启动浏览器
    browser = playwright.chromium.launch(
        # slow_mo=1000, # 全局设置速度
        headless=False,
        # args=["--window-size=1920,1080"]  # 设置窗口大小
    )
    yield browser
    browser.close()  # 关闭浏览器


# 测试夹具-启动新的浏览器
# 测试夹具 - 使用 browser fixture 创建 context 并应用 iPhone 13 设备配置
@pytest.fixture(scope="package")
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


@pytest.fixture(scope="package")
def page_pc(browser):
    # 使用传入的 browser 实例创建一个新的 context，并应用 iPhone 13 的设备参数
    # context = browser.new_context(no_viewport=True)
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    yield page
    page.close()  # 关闭页面
    context.close()  # 关闭上下文


@pytest.fixture(scope="package")
def page_h5_居民(playwright, browser):
    # 获取 iPhone 13 设备参数
    iphone_13 = playwright.devices['iPhone 13']
    # 使用传入的 browser 实例创建一个新的 context，并应用 iPhone 13 的设备参数
    context = browser.new_context(**iphone_13)
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(10000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPageH5(page)
    login_page.goto()
    login_page.同意登录()
    login_page.登录(USERS_BY_ROLE['居民']['phone_number'], '22', '202208')
    role_to_page['居民'] = page
    yield page
    page.close()  # 关闭页面
    context.close()  # 关闭上下文


@pytest.fixture(scope="package")
def page_h5_一级网格员(playwright, browser):
    # 获取 iPhone 13 设备参数
    iphone_13 = playwright.devices['iPhone 13']
    # 使用传入的 browser 实例创建一个新的 context，并应用 iPhone 13 的设备参数
    context = browser.new_context(**iphone_13)
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(10000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPageH5(page)
    login_page.goto()
    login_page.同意登录()
    login_page.登录(USERS_BY_ROLE['一级网格员_H5']['phone_number'], '22', '202208')
    role_to_page['一级网格员_H5'] = page
    yield page
    page.close()  # 关闭页面
    context.close()  # 关闭上下文


@pytest.fixture(scope="package")
def page_h5_物业管理员(playwright, browser):
    # 获取 iPhone 13 设备参数
    iphone_13 = playwright.devices['iPhone 13']
    # 使用传入的 browser 实例创建一个新的 context，并应用 iPhone 13 的设备参数
    context = browser.new_context(**iphone_13)
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(10000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPageH5(page)
    login_page.goto()
    login_page.同意登录()
    login_page.登录(USERS_BY_ROLE['物业管理员_H5']['phone_number'], '22', '202208')
    role_to_page['物业管理员_H5'] = page
    yield page
    page.close()  # 关闭页面
    context.close()  # 关闭上下文


@pytest.fixture(scope="package")
def page_h5_三级网格员(playwright, browser):
    # 获取 iPhone 13 设备参数
    iphone_13 = playwright.devices['iPhone 13']
    # 使用传入的 browser 实例创建一个新的 context，并应用 iPhone 13 的设备参数
    context = browser.new_context(**iphone_13)
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(10000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPageH5(page)
    login_page.goto()
    login_page.同意登录()
    login_page.登录(USERS_BY_ROLE['三级网格员_H5']['phone_number'], '22', '202208')
    role_to_page['三级网格员_H5'] = page
    yield page
    page.close()  # 关闭页面
    context.close()  # 关闭上下文


@pytest.fixture(scope="package")
def page_h5_二级网格员(playwright, browser):
    # 获取 iPhone 13 设备参数
    iphone_13 = playwright.devices['iPhone 13']
    # 使用传入的 browser 实例创建一个新的 context，并应用 iPhone 13 的设备参数
    context = browser.new_context(**iphone_13)
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(10000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPageH5(page)
    login_page.goto()
    login_page.同意登录()
    login_page.登录(USERS_BY_ROLE['二级网格员_H5']['phone_number'], '22', '202208')
    role_to_page['二级网格员_H5'] = page
    yield page
    page.close()  # 关闭页面
    context.close()  # 关闭上下文


@pytest.fixture(scope="module")
def page_pc_物业管理员1(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(5000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['物业管理员1']['username'], USERS_BY_ROLE['物业管理员1']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("物业服务", "事件管理")
    role_to_page['物业管理员1'] = page
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="module")
def page_pc_物业管理员2(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(5000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['物业管理员2']['username'], USERS_BY_ROLE['物业管理员2']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("物业服务", "事件管理")
    role_to_page['物业管理员2'] = page
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="module")
def page_pc_物业工作人员(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(5000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['物业工作人员']['username'], USERS_BY_ROLE['物业工作人员']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("物业服务", "事件管理")
    role_to_page['物业工作人员'] = page
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="module")
def page_pc_三级网格员(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(5000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['三级网格员']['username'], USERS_BY_ROLE['三级网格员']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    # query_page.跳转到某菜单("网格管理", "事件管理")
    query_page.跳转到某菜单("网格管理", "三级网格管理/居民上报")

    role_to_page['三级网格员'] = page
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="module")
def page_pc_二级网格员(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(5000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['二级网格员']['username'], USERS_BY_ROLE['二级网格员']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("网格管理", "事件管理")
    role_to_page['二级网格员'] = page
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="module")
def page_pc_一级网格员(browser):
    context = browser.new_context()
    page = context.new_page()  # 打开新页面
    page.set_default_timeout(5000)  # 设置全局默认超时时间为 10 秒
    login_page = LoginPagePc(page)
    login_page.goto()
    login_page.登录(USERS_BY_ROLE['一级网格员']['username'], USERS_BY_ROLE['一级网格员']['password'], '202208')
    login_page.进入系统()
    # 登录后跳转到事业管理页面
    query_page = BaseQueryPage(page)
    query_page.跳转到某菜单("网格管理", "事件管理")
    role_to_page['一级网格员'] = page
    yield page
    page.close()
    context.close()


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
def 浏览器已打开的页面(browser_opened):
    # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
    context = browser_opened.contexts[0] if browser_opened.contexts else browser_opened.new_context()
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
def 后置操作_点击返回按钮(浏览器已打开的页面):
    yield 浏览器已打开的页面
    浏览器已打开的页面.locator("button").filter(has_text="返回").click()


@pytest.fixture(scope="function")
def 后置操作_重置查询条件(查询页面):
    yield 查询页面
    # 执行完用例之后，点击重置按钮，清空查询条件
    查询页面.click_reset_btn()
    # expect(查询页面.page.get_by_text("加载中")).not_to_be_visible(timeout=5000)
    expect(查询页面.page.locator(".el-loading-spinner").locator("visible=true")).not_to_be_visible(timeout=5000)
    # 等待网络请求完成
    # 查询页面.page.wait_for_load_state("networkidle")


@pytest.fixture(scope="function")
def 后置操作_关闭抽屉(浏览器已打开的页面):
    yield 浏览器已打开的页面
    当前页面 = BaseQueryPage(浏览器已打开的页面)
    当前页面.关闭抽屉()

class ArtifactsRecorder:
    def __init__(
            self,
            pytestconfig: Any,
            request: pytest.FixtureRequest,
            playwright: Playwright,
            pw_artifacts_folder: tempfile.TemporaryDirectory,
    ) -> None:
        self._request = request
        self._pytestconfig = pytestconfig
        self._playwright = playwright
        self._pw_artifacts_folder = pw_artifacts_folder

        self._all_pages: List[Page] = []
        self._screenshots: List[str] = []
        self._traces: List[str] = []
        self._rerun_strategy = pytestconfig.getoption("--rerun_strategy").split(",")
        self._reruns = pytestconfig.getoption("--reruns")
        #  这里逻辑了上面的一致,不赘述了
        if self._rerun_strategy and self._reruns:
            if self._reruns + 1 >= len(self._rerun_strategy):
                self._init_rerun_strategy = [""] * (1 + self._reruns - len(self._rerun_strategy)) + self._rerun_strategy
            else:
                self._init_rerun_strategy = self._rerun_strategy[:self._reruns + 1]

            rerun_round = request.node.execution_count - 1
            self._round_rerun_strategy = self._init_rerun_strategy[rerun_round]

            #  以下为判断log策略内容和参数的方法,注意,如果没有则设置为off
            if "screenshot" in self._round_rerun_strategy:
                self._screenshot_option = self._round_rerun_strategy.split("=")[-1]
            else:
                self._screenshot_option = "off"
            if "video" in self._round_rerun_strategy:
                self._video_option = self._round_rerun_strategy.split("=")[-1]
            else:
                self._video_option = "off"
            if "tracing" in self._round_rerun_strategy:
                self._tracing_option = self._round_rerun_strategy.split("=")[-1]
            else:
                self._tracing_option = "off"
            self._capture_trace = self._tracing_option in ["on", "retain-on-failure"]
        else:
            #  没有重试log策略和重试次数,自然取原始的log策略
            self._screenshot_option = self._pytestconfig.getoption("--screenshot")
            self._video_option = self._pytestconfig.getoption("--video")
            self._tracing_option = pytestconfig.getoption("--tracing")
            self._capture_trace = self._tracing_option in ["on", "retain-on-failure"]

    def did_finish_test(self, failed: bool) -> None:
        #  获取当前轮次并初始化一个字符串,给保存文件做前缀
        round_prefix = f"round{self._request.node.execution_count}-"
        #  这里可以学习一下组合的布尔逻辑
        capture_screenshot = self._screenshot_option == "on" or (
                failed and self._screenshot_option == "only-on-failure"
        )
        if capture_screenshot:
            for index, screenshot in enumerate(self._screenshots):
                human_readable_status = "failed" if failed else "finished"
                screenshot_path = _build_artifact_test_folder(
                    self._pytestconfig,
                    self._request,
                    #  原始为 f"test-{human_readable_status}-{index + 1}.png",
                    f"{round_prefix}{index + 1}-{human_readable_status}-{screenshot.split(os.sep)[-1]}.png",
                )
                #  这里这种写法注意下,如果自己需要放log,用这个方式创建很好
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                shutil.move(screenshot, screenshot_path)
                # allure附加图片文件的方法
                allure.attach.file(screenshot_path, f"{round_prefix}{index + 1}-{human_readable_status}-{screenshot.split(os.sep)[-1]}.png")
        else:
            for screenshot in self._screenshots:
                os.remove(screenshot)

        if self._tracing_option == "on" or (
                failed and self._tracing_option == "retain-on-failure"
        ):
            for index, trace in enumerate(self._traces):
                trace_file_name = (
                    f"{round_prefix}trace.zip" if len(self._traces) == 1 else f"{round_prefix}trace-{index + 1}.zip"
                )
                trace_path = _build_artifact_test_folder(
                    self._pytestconfig, self._request, trace_file_name
                )
                os.makedirs(os.path.dirname(trace_path), exist_ok=True)
                shutil.move(trace, trace_path)
                # allure附加zip文件的方法
                allure.attach.file(trace_path, "trace.playwright.dev", extension="zip")
        else:
            for trace in self._traces:
                os.remove(trace)

        preserve_video = self._video_option == "on" or (
                failed and self._video_option == "retain-on-failure"
        )
        if preserve_video:
            for index, page in enumerate(self._all_pages):
                video = page.video
                if not video:
                    continue
                try:
                    video_file_name = (
                        f"{round_prefix}video.webm"
                        if len(self._all_pages) == 1
                        else f"{round_prefix}video-{index + 1}.webm"
                    )
                    video.save_as(
                        path=_build_artifact_test_folder(
                            self._pytestconfig, self._request, video_file_name
                        )
                    )
                    # allure附加webm录像的方法
                    allure.attach.file(_build_artifact_test_folder(
                        self._pytestconfig, self._request, video_file_name
                    ), "过程录像", allure.attachment_type.WEBM)
                except Error:
                    # Silent catch empty video
                    pass
        else:
            for page in self._all_pages:
                # Can be changed to "if page.video" without try/except once https://github.com/microsoft/playwright-python/pull/2410 is released and widely adopted.
                if self._video_option in ["on", "retain-on-failure"]:
                    try:
                        page.video.delete()
                    except Error:
                        pass

    def on_did_create_browser_context(self, context: BrowserContext) -> None:
        #  上下文里监听,有新的page就添加到列表中
        base_url = GlobalMap().get("baseurl")
        context.on("page", lambda page: self._all_pages.append(page))
        global api_Count

        def on_page(page: Page):
            def on_clear(my_page: Page):
                try:
                    api_Count.clear()
                    my_page.wait_for_timeout(500)
                except:
                    pass

            # pages.append(page)
            page.on("close", on_clear)
            page.on("load", on_clear)

        def on_add_request(req):
            if any(fix in req.url for fix in [base_url]):
                api_Count.append(req.url)

        def on_remove_request(req):
            try:
                api_Count.remove(req.url)
            except:
                pass

        context.on("page", on_page)
        context.on("request", on_add_request)
        context.on("requestfinished", on_remove_request)
        context.on("requestfailed", on_remove_request)
        #  判断是否需要trace,如果需要,就开始录制
        if self._request and self._capture_trace:
            context.tracing.start(
                title=slugify(self._request.node.name),
                screenshots=True,
                snapshots=True,
                sources=True,
            )

    def on_will_close_browser_context(self, context: BrowserContext) -> None:
        #  判断是否需要trace,如果需要,就结束录制
        if self._capture_trace:
            trace_path = Path(self._pw_artifacts_folder.name) / create_guid()
            context.tracing.stop(path=trace_path)
            self._traces.append(str(trace_path))
        else:
            context.tracing.stop()

        #  如果需要截图,就在关闭page前,获取截图
        if self._screenshot_option in ["on", "only-on-failure"]:
            for page in context.pages:
                #  这里用try是因为有可能page已经关闭了
                try:
                    screenshot_path = (
                        # Path(self._pw_artifacts_folder.name) / create_guid()
                            Path(self._pw_artifacts_folder.name) / "".join([page.title(), str(time.time_ns())])
                    )
                    page.screenshot(
                        timeout=5000,
                        path=screenshot_path,
                        full_page=self._pytestconfig.getoption(
                            "--full-page-screenshot"
                        ),
                    )
                    self._screenshots.append(str(screenshot_path))
                except Error:
                    pass


def create_guid() -> str:
    return hashlib.sha256(os.urandom(16)).hexdigest()


class Locator(_Locator):
    __last_step = None

    @property
    def selector(self):
        _repr = self.__repr__()
        if "selector" in _repr:
            __selector = []
            for _ in _repr.split("selector=")[1][1:-2].split(" >> "):
                if r"\\u" not in _:
                    __selector.append(_)
                    continue
                __selector.append(
                    _.encode("utf8")
                    .decode("unicode_escape")
                    .encode("utf8")
                    .decode("unicode_escape")
                )
            return " >> ".join(__selector)

    def __getattribute__(self, attr):
        global api_Count
        global time_out
        try:
            orig_attr = super().__getattribute__(attr)
            if callable(orig_attr):

                def wrapped(*args, **kwargs):
                    step_title = None
                    if attr == "_sync" and self.__last_step:
                        step_title = self.__last_step
                    else:
                        self.__last_step = attr
                    start_time = time.time()
                    while True:
                        self.page.wait_for_load_state()
                        if time.time() - start_time < int(time_out / 1333):
                            try:
                                if attr in ["click", "fill", "hover", "check", "blur", "focus"]:
                                    self.page.wait_for_timeout(100)
                                    api_length = len(api_Count)
                                    if api_Count:
                                        self.page.wait_for_timeout(200)
                                        self.page.evaluate('''() => {
                                               const spanToRemove = document.getElementById('ainotestgogogo');
                                               if (spanToRemove) {
                                                   spanToRemove.remove();
                                               }
                                           }''')
                                        self.page.evaluate(f'''() => {{
                                                const span = document.createElement('span');
                                                span.textContent = '{attr}:{api_length}';
                                                span.style.position = 'absolute';
                                                span.style.top = '0';
                                                span.style.left = '50%';
                                                span.style.transform = 'translateX(-50%)';
                                                span.style.backgroundColor = 'yellow'; // 设置背景色以便更容易看到
                                                span.style.zIndex = '9999';
                                                span.id = 'ainotestgogogo';
                                                document.body.appendChild(span);
                                            }}''')
                                    else:
                                        # 在这里可以添加自己需要等待或者处理的动作,比如等待转圈,关闭弹窗等等(当然,弹窗最好单独做个监听)
                                        self.page.locator("//*[contains(@class, 'el-loading-spinner')]").locator("visible=true").last.wait_for(state="hidden", timeout=30_000)
                                        if self.page.locator('//div[@class="antHcbm_routesDashboardCardsHcbmCards_down"][text()="关闭"]').locator("visible=true").or_(self.page.locator(".driver-close-btn").filter(has_text="关闭").locator("visible-true")).count():
                                            self.page.locator('//div[@class="antHcbm_routesDashboardCardsHcbmCards_down"][text()="关闭"]').locator("visible=true").or_(self.page.locator(".driver-close-btn").filter(has_text="关闭").locator("visible-true")).last.evaluate("node => node.click()")
                                        self.page.evaluate('''() => {
                                                const spanToRemove = document.getElementById('ainotestgogogo');
                                                if (spanToRemove) {
                                                    spanToRemove.remove();
                                                }
                                            }''')
                                        self.page.evaluate(f'''() => {{
                                                const span = document.createElement('span');
                                                span.textContent = '{attr}:{api_length}';
                                                span.style.position = 'absolute';
                                                span.style.top = '0';
                                                span.style.left = '50%';
                                                span.style.transform = 'translateX(-50%)';
                                                span.style.backgroundColor = 'green'; // 设置背景色以便更容易看到
                                                span.style.zIndex = '9999';
                                                span.id = 'ainotestgogogo';
                                                document.body.appendChild(span);
                                            }}''')
                                        break
                                else:
                                    break
                            except:
                                self.page.evaluate('''() => {
                                        const spanToRemove = document.getElementById('ainotestgogogo');
                                        if (spanToRemove) {
                                            spanToRemove.remove();
                                        }
                                    }''')
                                self.page.evaluate(f'''() => {{
                                        const span = document.createElement('span');
                                        span.textContent = '操作等待中.....';
                                        span.style.position = 'absolute';
                                        span.style.top = '0';
                                        span.style.left = '50%';
                                        span.style.transform = 'translateX(-50%)';
                                        span.style.backgroundColor = 'red'; // 设置背景色以便更容易看到
                                        span.style.zIndex = '9999';
                                        span.id = 'ainotestgogogo';
                                        document.body.appendChild(span);
                                    }}''')
                                break
                        else:
                            self.page.evaluate('''() => {
                                    const spanToRemove = document.getElementById('ainotestgogogo');
                                    if (spanToRemove) {
                                        spanToRemove.remove();
                                    }
                                }''')
                            escaped_api_count = json.dumps(api_Count)
                            self.page.evaluate(f'''() => {{
                                    const span = document.createElement('span');
                                    span.textContent = `当前列表内容为: {escaped_api_count}`;
                                    span.style.position = 'absolute';
                                    span.style.top = '0';
                                    span.style.left = '50%';
                                    span.style.transform = 'translateX(-50%)';
                                    span.style.backgroundColor = 'red'; // 设置背景色以便更容易看到
                                    span.style.zIndex = '9999';
                                    span.id = 'ainotestgogogo';
                                    document.body.appendChild(span);
                                }}''')
                            if sys.platform != "linux":
                                print("接口卡超时了,暂时放行,需要查看超时接口或调整接口监听范围:")
                                print(escaped_api_count)
                                pass
                            api_Count.clear()
                            break

                    if step_title:
                        with step(f"{step_title}: {self.selector}"):
                            return orig_attr(*args, **kwargs)
                    return orig_attr(*args, **kwargs)

                return wrapped
            return orig_attr
        except AttributeError:
            ...


mapping.register(LocatorImpl, Locator)


# @pytest.hookimpl(trylast=True)
# def pytest_sessionfinish(session):
#     allure_report_auto_open_config = session.config.getoption("--allure_report_auto_open")
#     if session.config.getoption("--allure_report_auto_open") != "off":
#         if sys.platform != "linux":
#             import subprocess
#             allure_report_dir = allure_report_auto_open_config
#             # 尝试关闭可能已经在运行的 Allure 服务
#             try:
#                 if sys.platform == 'darwin':  # macOS
#                     subprocess.call("pkill -f 'allure'", shell=True)
#                 elif sys.platform == 'win32':  # Windows
#                     command = "taskkill /F /IM allure.exe /T"
#                     subprocess.call(command, shell=True)
#             except Exception as e:
#                 print(e)
#             allure_command = f'allure serve {allure_report_dir}'
#             subprocess.Popen(allure_command, shell=True)

