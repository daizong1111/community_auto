from playwright.sync_api import Page, expect

from module.BasePageNew import PageObject


# 定义登录页面的类，包含页面元素和操作方法
class LoginPagePc(PageObject):
    def __init__(self, page: Page):
        # 初始化页面对象和页面元素
        super().__init__(page)
        self.account_input = page.get_by_placeholder("请输入账号")  # 邮箱输入框
        self.password_input = page.get_by_placeholder("请输入密码")  # 密码输入框
        self.captcha_input = page.get_by_placeholder("请输入手机验证码")
        self.check_box = page.locator(".el-checkbox")
        self.login_button = page.get_by_role('button', name='登 录 ')  # 登录按钮

    def goto(self):
        # 导航到登录页面
        self.page.goto("http://114.96.83.242:8087/login")

    def 发送手机验证码(self):
        # 点击手机验证码发送按钮
        self.page.locator("button", has_text="获取手机验证码").click()
        # 输入图形验证码
        self.page.locator("//input[@placeholder='请输入验证码']").fill("202208")
        # 点击确定按钮
        self.click_button("确定")

    def 登录(self, account: str, password: str, sms_captcha: str):
        # 输入用户名和密码
        self.account_input.fill(account)
        self.password_input.fill(password)
        # 发送手机验证码
        self.发送手机验证码()
        # 等待验证码可以输入
        expect(self.page.locator("//input[@placeholder='请输入验证码']")).not_to_be_visible(timeout=5000)
        # 输入手机验证码
        self.captcha_input.fill(sms_captcha)
        # 勾选用户协议
        self.check_box.click()
        # 点击登录按钮
        self.login_button.click()

    def 进入系统(self):
        self.page.locator("//div[text()='基础信息']").click()

    def get_error_message(self):
        # 获取错误信息
        return self.page.locator(".error-message").text_content()
