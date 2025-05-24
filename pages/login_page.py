from playwright.sync_api import Page, expect

# 与验证码识别相关的库
from PIL import Image
import pytesseract
import io
# from captchasolver import CaptchaSolver
# 定义登录页面的类，包含页面元素和操作方法
class LoginPage:
    def __init__(self, page: Page):
        # 初始化页面对象和页面元素
        self.page = page
        self.username_input = page.get_by_placeholder("账号")  # 账号输入框
        self.password_input = page.get_by_placeholder("密码")  # 密码输入框
        self.captcha_input = page.get_by_placeholder("验证码") # 验证码
        self.login_button = page.get_by_role("button", name="登录")  # 登录按钮

    def goto(self):
        # 导航到登录页面
        self.page.goto("http://134.84.202.69:9081/meeting-web/#/login?redirect=%2F")

    def fill_username(self, username: str):
        # 填写用户名
        self.username_input.fill(username)

    def fill_password(self, password: str):
        # 填写密码
        self.password_input.fill(password)

    # def fill_captcha(self):
    #     # 获取验证码元素
    #     captcha_element = self.page.locator("//img[@class='login-code-img']")  # 根据实际页面调整选择器
    #
    #     # 截图验证码图片
    #     captcha_image_bytes = captcha_element.screenshot()
    #
    #     # 将字节流转换为 PIL 图像对象
    #     image = Image.open(io.BytesIO(captcha_image_bytes))
    #
    #     # 使用 Tesseract OCR 识别图片中的文字
    #     captcha_text = pytesseract.image_to_string(image)
    #
    #     # 清除空格和换行符
    #     captcha_text = captcha_text.strip()
    #
    #     # 如果是类似 "3+5=" 的表达式，提取表达式部分并计算
    #     if captcha_text.endswith("="):
    #         # 去掉等号，并计算表达式
    #         expression = captcha_text[:-1]
    #         try:
    #             result = str(eval(expression))
    #         except Exception as e:
    #             raise ValueError(f"无法计算验证码表达式: {expression}") from e
    #     else:
    #         result = captcha_text
    #
    #     # 填入识别到的验证码
    #     self.captcha_input.fill(result)

    # def fill_captcha(self):
    #     # 获取验证码元素
    #     captcha_element = self.page.locator("//img[@class='login-code-img']")  # 根据实际页面调整选择器
    #
    #     # 截图验证码图片
    #     captcha_image_bytes = captcha_element.screenshot()
    #
    #     # 将字节流保存为临时文件或使用内存文件处理
    #     with open("temp_captcha.png", "wb") as f:
    #         f.write(captcha_image_bytes)
    #
    #     # 使用 CaptchaSolver 进行识别
    #     solver = CaptchaSolver('browser')  # 可选 'phantomjs' 或 'browser'
    #     with open("temp_captcha.png", "rb") as img_file:
    #         captcha_text = solver.solve_captcha(img_file.read(), captcha_type='text')
    #
    #     # 清除空格和换行符
    #     captcha_text = captcha_text.strip()
    #
    #     # 如果是类似 "3+5=" 的表达式，提取表达式部分并计算
    #     if captcha_text.endswith("="):
    #         # 去掉等号，并计算表达式
    #         expression = captcha_text[:-1]
    #         try:
    #             result = str(eval(expression))
    #         except Exception as e:
    #             raise ValueError(f"无法计算验证码表达式: {expression}") from e
    #     else:
    #         result = captcha_text
    #
    #     # 填入识别到的验证码
    #     self.captcha_input.fill(result)

    def fill_captcha(self, captcha: str):
        # 填写验证码
        self.captcha_input.fill(captcha)

    def click_login(self):
        # 点击登录按钮
        self.login_button.click()

    def get_error_message(self):
        # 获取错误信息
        return self.page.locator(".error-message").text_content()


