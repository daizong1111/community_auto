import re

from playwright.sync_api import Page, Locator, sync_playwright

from module.base_query_page_new import BaseQueryPage

import re

import allure
import pytest
from playwright.sync_api import expect, Page, sync_playwright

from base_case import BaseCase
from pages.pages_h5.上报物业 import PageReportProperty
from pages.pages_h5.首页 import PageHome
from pages.网格管理.事件管理 import PageIncidentManage

@pytest.fixture(scope="function")
def close_all_drawers(request):
    """
    在测试用例执行后关闭所有角色页面的抽屉
    """
    yield
    # 获取所有已打开的页面对象
    opened_pages = []

    for name, value in request.node.funcargs.items():
        if isinstance(value, Page):
            opened_pages.append(value)

    # 刷新所有已打开的页面
    for page in opened_pages:
        try:
            page.reload()
        except Exception as e:
            print(f"刷新页面失败: {e}")


def 处理事件(角色页面: Page, 表单数据: dict, 角色名称: str):
    # 将 申请协助(上级) 和 转交(上级) 类似文本中的括号内部的内容去掉
    处理方式 = re.sub(r'\(.*?\)', '', 表单数据.get("处理方式"))
    角色页面.reload()
    if 角色名称 == '三级网格员':
        # 刷新页面
        当前页面 = PageResidentsReport(角色页面)
    else:
        当前页面 = PageIncidentManage(角色页面)

    # 在处理事件之前获取当前第一行的文本或其他唯一标识
    first_row_before = 当前页面.get_table_rows().first.text_content()
    # 处理事件
    当前页面.处理最新事件(表单数据)
    # 验证处理成功，不同角色的提示语不一致，这里只做模糊检查
    expect(当前页面.page.get_by_text("成功")).to_be_visible()

    # 断言处理事件后，之前的首行内容不再可见
    expect(当前页面.get_table_rows().filter(has_text=first_row_before)).not_to_be_visible(timeout=3000)


    # 若转交给物业，那么当前账号将看不到这条记录
    if 处理方式 != "转交物业":
        # 点击查看按钮
        if "网格员" in 角色名称:
            当前页面.点击表格中某行按钮(行号=1, 按钮名="详情")
        else:
            当前页面.点击表格中某行按钮(行号=1, 按钮名="查看")

        if 角色名称 == "三级网格员":
            # 三级网格员需要切换选项卡
            当前页面.page.locator("//div[@class='el-dialog']//div[text()='处理流程']").click()

        expect(当前页面.page.locator('.el-timeline-item__timestamp',has_text=角色名称 + 处理方式)).to_be_visible()
        # # 断言处理记录
        # assert 当前页面.处理记录节点_最新.text_content().strip() == 角色名称 + 处理方式, f"页面上的实际值{当前页面.处理记录节点_最新.text_content().strip()}，预期值为{角色名称 + 处理方式}"
    if 角色名称 == '三级网格员':
        当前页面.page.locator('.el-dialog__close').locator("visible=true").click()
    else:
        # 关闭抽屉
        角色页面.mouse.click(x=10, y=10)

class PageResidentsReport(BaseQueryPage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.表单_处理 = self.page.locator('.el-dialog').locator("visible=true")
        self.处理记录节点_最新 = self.page.locator(".el-timeline-item__timestamp").first
        self.详情页的关闭按钮 = self.page.locator('.el-dialog__close').locator("visible=true")


    def 处理最新事件(self, 表单数据_工单处理:dict):
        self.点击表格中某行按钮(行号=1,按钮名="办理")
        处理方式 = 表单数据_工单处理.get("处理方式")
        loc_选项卡_处理方式 = self.表单_处理.locator(f"xpath=//div[contains(text(),'{处理方式}')]")
        loc_选项卡_处理方式.click()
        # 去掉字典中的第一项
        first_key = next(iter(表单数据_工单处理))
        表单数据_工单处理.pop(first_key)
        self.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_工单处理,表单最上层定位=self.表单_处理)
        提交按钮上的文本 = re.sub(r'\(.*?\)', '', 处理方式)
        self.click_button(提交按钮上的文本)









if __name__ == '__main__':
    with sync_playwright() as playwright:
        # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        # 通过ip和端口连接到已经打开的chromium浏览器
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(3000)  # 设置默认超时时间为 3000 毫秒
        # page = PageResidentsReport(page)
        # page.处理最新事件({"处理方式":"下发","指定处理人":"石**","处理意见":"同意","图片":r"C:\Users\Administrator\Pictures\111.png"})
        # page.处理最新事件({"处理方式":"办结","处理描述":"很好很薄","照片":r"C:\Users\Administrator\Pictures\111.png"})
        处理事件(page, {"处理方式": "办结", "处理描述": "很好很薄", "照片": r"C:\Users\Administrator\Pictures\111.png"},
                 "三级网格员")





