from playwright.sync_api import Page, expect

from module.BasePage import PageObject


# 定义登录页面的类，包含页面元素和操作方法
class 登录页(PageObject):
    def __init__(self, page: Page):
        # 初始化页面对象和页面元素
        super().__init__(page)
        self.输入框_用户名 = page.get_by_placeholder("请输入账号")  # 邮箱输入框
        self.输入框_密码 = page.get_by_placeholder("请输入密码")  # 密码输入框
        self.按钮_获取手机验证码 = page.locator("button", has_text="获取手机验证码")
        self.按钮_获取手机验证码_禁用后 = page.locator(".el-button.el-button--primary.is-disabled")
        self.手机验证码 = page.get_by_placeholder("请输入手机验证码")
        self.用户协议单选框 = page.locator(".el-checkbox")
        self.输入框_图形验证码 = page.locator("//input[@placeholder='请输入验证码']")
        self.按钮_登录 = page.get_by_role('button', name='登 录 ')  # 登录按钮
        self.基础信息 = page.get_by_text("基础信息")
        self.提示语_该令牌已过期 = page.get_by_text("该令牌已过期")

    def 发送手机验证码(self, 图形验证码: str = "202208"):
        # 点击手机验证码发送按钮
        self.按钮_获取手机验证码.click()
        # 输入图形验证码
        self.输入框_图形验证码.fill(图形验证码)
        # 点击确定按钮
        self.click_button("确定")

    def 登录(self, account: str, password: str, sms_captcha: str):
        """
        成功登录
        :param account: 用户名
        :param password: 密码
        :param sms_captcha: 手机验证码
        :return:
        """
        self.page.goto("/login")
        # 输入用户名和密码
        self.输入框_用户名.fill(account)
        self.输入框_密码.fill(password)
        # 发送手机验证码
        self.发送手机验证码()
        # 等待验证码可以输入
        expect(self.page.locator("//input[@placeholder='请输入验证码']")).not_to_be_visible(timeout=5000)
        # 输入手机验证码
        self.手机验证码.fill(sms_captcha)
        # 勾选用户协议
        self.用户协议单选框.click()
        # 点击登录按钮
        self.按钮_登录.click()
        expect(self.page.get_by_text("基础信息")).to_be_visible()

    def 登录_错误的用户名(self, account: str, password: str, sms_captcha: str):
        self.page.goto("/login")
        # 输入用户名和密码
        self.输入框_用户名.fill(account)
        self.输入框_密码.fill(password)
        # 发送手机验证码
        self.按钮_获取手机验证码.click()
        # 等待验证码可以输入
        expect(self.page.get_by_text("账号或密码输入错误")).to_be_visible()

    def 登录_输入错误的图形验证码(self, account: str, password: str, sms_captcha: str):
        self.page.goto("/login")
        # 输入用户名和密码
        self.输入框_用户名.fill(account)
        self.输入框_密码.fill(password)
        # 发送手机验证码
        self.发送手机验证码(sms_captcha)
        expect(self.page.get_by_text("输入的图形验证码不正确，请重试")).to_be_visible()


    def 登录_输入错误的短信验证码(self, account: str, password: str, sms_captcha: str):
        self.page.goto("/login")
        # 输入用户名和密码
        self.输入框_用户名.fill(account)
        self.输入框_密码.fill(password)
        # 发送手机验证码
        self.发送手机验证码()
        # 等待验证码可以输入
        expect(self.按钮_获取手机验证码).not_to_be_visible(timeout=5000)
        expect(self.page.get_by_text("验证码不能为空")).to_be_visible(timeout=5000)
        # 输入手机验证码
        self.手机验证码.fill(sms_captcha)
        expect(self.手机验证码).to_have_value(sms_captcha)
        # 勾选用户协议
        self.用户协议单选框.click()
        # 点击登录按钮
        self.按钮_登录.click()
        # 断言
        expect(self.page.get_by_text("输入的短信验证码不正确")).to_be_visible(timeout=3000)

    def 登录_发送短信验证码按钮60s倒计时内刷新页面(self, account: str, password: str, sms_captcha: str):
        """
                成功登录
                :param account: 用户名
                :param password: 密码
                :param sms_captcha: 手机验证码
                :return:
                """
        self.page.goto("/login")
        # 输入用户名和密码
        self.输入框_用户名.fill(account)
        self.输入框_密码.fill(password)
        # 发送手机验证码
        self.发送手机验证码()
        # 等待验证码可以输入
        expect(self.按钮_获取手机验证码_禁用后).to_be_visible()
        expect(self.按钮_获取手机验证码_禁用后).not_to_be_enabled()
        # 刷新页面
        self.page.reload()
        # 按钮变为可以点击
        expect(self.按钮_获取手机验证码).to_be_enabled(timeout=5000)





