from playwright.sync_api import Page, Locator, sync_playwright


class PagePersonalCenter():
    def __init__(self, page: Page):
        self.page = page
        self.按钮_切换身份 = self.page.locator(
            "//uni-image[@class='userSignImg']")
        self.按钮_角色_居民 = self.page.locator("//uni-view[text()='我是社区居民']")
        self.按钮_角色_物业管理员 = self.page.locator("//uni-view[text()='我是物业管理员']")
        self.按钮_角色_物业工作人员 = self.page.locator("//uni-view[text()='我是物业工作人员']")
        self.按钮_角色_三级网格员 = self.page.locator("//uni-view[text()='我是三级网格员']")
        self.按钮_角色_二级网格员 = self.page.locator("//uni-view[text()='我是二级网格员']")
        self.按钮_角色_一级网格员 = self.page.locator("//uni-view[text()='我是一级网格员']")




    def 选择角色(self, 角色: str):
        # 使用字典将角色名称映射到对应的按钮
        role_buttons = {
            "居民": self.按钮_角色_居民,
            "物业管理员": self.按钮_角色_物业管理员,
            "物业工作人员": self.按钮_角色_物业工作人员,
            "三级网格员": self.按钮_角色_三级网格员,
            "二级网格员": self.按钮_角色_二级网格员,
            "一级网格员": self.按钮_角色_一级网格员,
        }
        self.按钮_切换身份.click()
        # 根据传入的角色名称点击对应的按钮
        if 角色 in role_buttons:
            role_buttons[角色].click()
        else:
            raise ValueError(f"不支持的角色名称: {角色}")

if __name__ == '__main__':
    with sync_playwright() as playwright:
        # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        # 通过ip和端口连接到已经打开的chromium浏览器
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9224")
        # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
        page = context.pages[0] if context.pages else context.new_page()
        page.screenshot(path="screenshot.png")
        page.set_default_timeout(3000)  # 设置默认超时时间为 3000 毫秒
        page = PagePersonalCenter(page)
        page.选择角色("居民")





