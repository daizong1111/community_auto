from playwright.sync_api import Locator, Page, sync_playwright

from module import *


class Locators:
    def __init__(self, page: Page):
        self.page = page

    def button_按钮(self, text, nth=-1) -> Locator:
        button = self.page.locator("button")
        for word in text:
            button = button.filter(has_text=word)
        return button.locator('visible=true').nth(nth)

    def below_元素下方紧邻的元素(self, 要找的元素类型="*") -> Locator:
        return self.page.locator(f"xpath=/following::{要找的元素类型}[position()=1]")

    # def 表单项中包含操作元素的最上级div(self, 字段名: str) -> Locator:
    #     最终上级元素locator = self.page.locator("label").locator("visible=true").filter(has=self.page.get_by_text(字段名)).locator(self.below_元素下方紧邻的元素())
    #     return 最终上级元素locator

    def 表单项中包含操作元素的最上级div(self, 字段名: str, 处理后的表单最上层定位:Locator=None) -> Locator:
        if 处理后的表单最上层定位 is not None:
            最终上级元素locator = 处理后的表单最上层定位.locator("label").locator("visible=true").filter(has=self.page.get_by_text(字段名,exact=True)).locator(self.below_元素下方紧邻的元素())
        else:
            最终上级元素locator = self.page.locator("label").locator("visible=true").filter(has=self.page.get_by_text(字段名,exact=True)).locator(self.below_元素下方紧邻的元素())
        return 最终上级元素locator

if __name__ == '__main__':
    with sync_playwright() as playwright:
        # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        # 通过ip和端口连接到已经打开的chromium浏览器
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(10000)  # 设置默认超时时间为 3000 毫秒
        locators = Locators(page)
        locators.表单项中包含操作元素的最上级div("会议室名称").highlight()
        page.wait_for_timeout(10000)


