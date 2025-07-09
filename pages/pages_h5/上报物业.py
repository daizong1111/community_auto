from playwright.sync_api import Page, Locator, sync_playwright


class PageReportProperty():
    def __init__(self, page: Page):
        self.page = page
        # self.按钮_新增 = self.page.locator("//span[text()='新增']")
        self.按钮_新增 = self.page.locator('uni-button', has_text='新增')

        self.输入框_上报描述 = self.page.locator("//textarea")
        self.按钮_上报图片 = self.page.locator("//input")
        self.按钮_确认提交 = self.page.locator('uni-button', has_text='确认提交')

    def 选择上报类型(self, 上报类型: str):
        self.page.locator(f"//uni-view[text()='{上报类型}']").click()

    def 上报事件(self, 表单数据:dict):
        self.按钮_新增.click()
        self.选择上报类型(表单数据["上报类型"])
        self.输入框_上报描述.fill(表单数据["上报描述"])
        # self.按钮_上报图片.set_input_files(表单数据["上报图片路径"])
        # 等待文件选择器出现并设置文件
        # self.page.wait_forFileChooser()
        # file_chooser = page.file_chooser()
        # file_chooser.set_files(file_path)
        self.按钮_确认提交.click()
        self.page.go_back()


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
        page = PageReportProperty(page)
        page.上报事件("建议", "太难了", r"C:\Users\Administrator\Pictures\111.png")





