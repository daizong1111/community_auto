
from playwright.sync_api import Page, Locator, sync_playwright



class PageHome():
    def __init__(self, page: Page):
        self.page = page
        self.按钮_个人中心 = self.page.locator(
            "//span[text()='个人中心']")
        self.按钮_首页 = self.page.locator("//span[text()='首页']")
        self.图标_上报物业 = self.page.locator("//span[text()='上报物业']/../preceding-sibling::*")
        self.图标_上报社区 = self.page.locator("//span[text()='上报社区']/../preceding-sibling::*")

    def 跳转到个人中心(self):
        self.按钮_个人中心.click()

    def 跳转到上报物业(self):
        self.图标_上报物业.click()

    def 跳转到上报社区(self):
        self.图标_上报社区.click()




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
        page = PageHome(page)




