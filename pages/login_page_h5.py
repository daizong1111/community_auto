from playwright.sync_api import Page, expect


# 定义登录页面的类，包含页面元素和操作方法
class LoginPageH5:
    def __init__(self, page: Page):
        # 初始化页面对象和页面元素
        self.page = page
        self.按钮_立即登录 = self.page.locator('.uni-modal__btn', has_text='立即登录')
        self.勾选框_用户协议= self.page.locator('.uicon-checkbox-mark')
        self.phone_input = self.page.locator("//div[text()='请输入手机号']/following-sibling::input")  # 手机号输入框
        self.img_captcha_input = self.page.locator("//div[text()='请输入图形验证码']/following-sibling::input")
        self.sms_captcha_input = self.page.locator("//div[text()='请输入短信验证码']/following-sibling::input")
        self.login_button = self.page.locator('.u-button', has_text='登录')  # 登录按钮

    def 同意登录(self):
        self.按钮_立即登录.click()
        self.勾选框_用户协议.click()
        self.page.get_by_text('同意',exact=True).locator("visible=true").click()
        self.page.get_by_text('自有登录',exact=True).locator("visible=true").click()
    def goto(self):
        # 导航到登录页面
        self.page.goto("http:/114.96.83.242:8087/h5/")

    def 登录(self, phone: str, img_captcha: str, sms_captcha: str):
        self.phone_input.fill(phone)
        self.img_captcha_input.fill(img_captcha)
        self.sms_captcha_input.fill(sms_captcha)
        self.login_button.click()

