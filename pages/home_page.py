from playwright.sync_api import Page, expect

# 首页页面
class HomePage:
    def __init__(self, page: Page):
        self.page = page


    def get_meeting_manage_icon(self):
        # 新会议管理图标
        return self.page.locator("(//div[normalize-space()='新会议管理'])[1]")
        # return self.page.locator(r"//div[@class='application-content']/div[8]")

    def click_meeting_manage_icon(self):
        # 点击新会议管理图标
        self.get_meeting_manage_icon().click()


    def get_meeting_manage_page(self):
        # 跳转到会议管理页面
        with self.page.expect_popup() as page1_info:
            self.click_meeting_manage_icon()
        page1 = page1_info.value
        return page1
