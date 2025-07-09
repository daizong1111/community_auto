from playwright.sync_api import Page, Locator, sync_playwright

from pages.pages_h5.个人中心 import PagePersonalCenter


class PageHome():
    def __init__(self, page: Page):
        self.page = page
        self.按钮_个人中心 = self.page.locator(
            "//span[text()='个人中心']")
        self.按钮_首页 = self.page.locator("//span[text()='首页']")
        self.图标_上报物业 = self.page.locator("//span[text()='上报物业']/../preceding-sibling::*")
        self.图标_上报社区 = self.page.locator("//span[text()='上报社区']/../preceding-sibling::*")
        self.按钮_工单 = self.page.locator("//span[text()='工单']")

    def 跳转到个人中心(self):
        self.按钮_个人中心.click()

    def 跳转到首页(self):
        self.按钮_首页.click()

    def 跳转到上报物业(self):
        self.图标_上报物业.click()

    def 跳转到上报社区(self):
        self.图标_上报社区.click()

    def 切换角色(self, 角色: str):
        self.跳转到个人中心()
        # 跳转到个人中心，并选择角色
        page_personal_center = PagePersonalCenter(self.page)
        page_personal_center.选择角色(角色)

    def 点击事件管理选修卡(self):
        self.page.locator(".image").nth(2).click()
    def 处理工单(self, 表单数据: dict, 角色名称:str):
        if "网格员" in 角色名称:
            self.点击事件管理选修卡()
            # 点击位于列表最上方的工单项，跳转到表单页面
            self.page.locator(".o_list .o_l_item").first.click()
        # 跳转到工单页
        else:
            self.按钮_工单.click()
            # 点击位于列表最上方的工单项，跳转到表单页面
            self.page.locator(".list .item:nth-child(1)").click()

        # 右箭头_处理方式 = self.page.locator("//div[text()='请选择处理方式']/../../../following-sibling::*")
        右箭头_处理方式 = self.page.locator("(//span[text()=''])[1]")
        右箭头_处理方式.click()
        loc_目标选项 = self.page.locator(".u-picker__view__column__item", has_text=表单数据["处理方式"])
        # 选项_处理方式.scroll_into_view_if_needed()
        # 滚动前先将鼠标悬浮到黑色加粗的选项上面
        loc_当前选项 = self.page.locator('.u-picker__view__column__item[style*="font-weight: bold"]')
        loc_当前选项.hover()
        while loc_当前选项.inner_text() != loc_目标选项.inner_text():
            self.page.mouse.wheel(delta_x=0, delta_y=100)
            # 滚动后，当前选项可能会变化，重新定位
            loc_当前选项 = self.page.locator('.u-picker__view__column__item[style*="font-weight: bold"]')
        # bound_处理方式 = 选项_处理方式.bounding_box()
        # self.page.mouse.click(x=bound_处理方式['x'] + bound_处理方式['width'] / 2,
        #                       y=bound_处理方式['y'] + bound_处理方式['height'] / 2)
        # 选项_处理方式.click()
        # 选项_处理方式.tap()
        按钮_确定 = self.page.locator("//span[text()='确定']")
        按钮_确定.click()

        if 表单数据.get("指定处理人") != None:
            右箭头_指定处理人 = self.page.locator("(//span[text()=''])[2]")
            右箭头_指定处理人.click()
            loc_目标选项 = self.page.locator(".u-picker__view__column__item", has_text=表单数据["指定处理人"])
            # 选项_处理方式.scroll_into_view_if_needed()
            # 滚动前先将鼠标悬浮到黑色加粗的选项上面
            loc_当前选项 = self.page.locator('.u-picker__view__column__item[style*="font-weight: bold"]')
            loc_当前选项.hover()
            while loc_当前选项.inner_text() != loc_目标选项.inner_text():
                self.page.mouse.wheel(delta_x=0, delta_y=100)
                # 滚动后，当前选项可能会变化，重新定位
                loc_当前选项 = self.page.locator('.u-picker__view__column__item[style*="font-weight: bold"]')
            按钮_确定 = self.page.locator("//span[text()='确定']")
            按钮_确定.click()

        输入框_处理意见 = self.page.locator("//*[text()='请输入处理意见']/following-sibling::textarea")
        输入框_处理意见.fill(表单数据["处理意见"])

        按钮_提交 = self.page.locator("uni-button", has_text="提交")
        按钮_提交.click()



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
