from playwright.sync_api import expect, BrowserContext

def test_登录_输入正确用户名(new_context):
    from module.PageInstance import PageIns
    from utils.globalMap import GlobalMap
    from data_module.auth_Data import MyData
    global_map = GlobalMap()
    被测环境 = global_map.get("env")
    用户别名 = "省级"
    用户名 = MyData().userinfo(被测环境, 用户别名)["username"]
    密码 = MyData().userinfo(被测环境, 用户别名)["password"]
    context: BrowserContext = new_context()
    page = context.new_page()
    my_page = PageIns(page)
    my_page.登录页.登录(用户名, 密码, '202208')

def test_登录_输入错误用户名(new_context):
    from module.PageInstance import PageIns
    from utils.globalMap import GlobalMap
    from data_module.auth_Data import MyData
    global_map = GlobalMap()
    被测环境 = global_map.get("env")
    用户别名 = "错误用户名"
    用户名 = MyData().userinfo(被测环境, 用户别名)["username"]
    密码 = MyData().userinfo(被测环境, 用户别名)["password"]
    context: BrowserContext = new_context()
    page = context.new_page()
    my_page = PageIns(page)
    my_page.登录页.登录_错误的用户名(用户名, 密码, '202208')

def test_登录_输入错误的图形验证码(new_context):
    from module.PageInstance import PageIns
    from utils.globalMap import GlobalMap
    from data_module.auth_Data import MyData
    global_map = GlobalMap()
    被测环境 = global_map.get("env")
    用户别名 = "省级"
    用户名 = MyData().userinfo(被测环境, 用户别名)["username"]
    密码 = MyData().userinfo(被测环境, 用户别名)["password"]
    context: BrowserContext = new_context()
    page = context.new_page()
    my_page = PageIns(page)
    my_page.登录页.登录_输入错误的图形验证码(用户名, 密码, '20220')

def test_登录_输入错误的短信验证码(new_context):
    from module.PageInstance import PageIns
    from utils.globalMap import GlobalMap
    from data_module.auth_Data import MyData
    global_map = GlobalMap()
    被测环境 = global_map.get("env")
    用户别名 = "省级"
    用户名 = MyData().userinfo(被测环境, 用户别名)["username"]
    密码 = MyData().userinfo(被测环境, 用户别名)["password"]
    context: BrowserContext = new_context()
    page = context.new_page()
    my_page = PageIns(page)
    my_page.登录页.登录_输入错误的短信验证码(用户名, 密码, '20')

def test_登录_发送短信验证码按钮60s倒计时内刷新页面(new_context):
    from module.PageInstance import PageIns
    from utils.globalMap import GlobalMap
    from data_module.auth_Data import MyData
    global_map = GlobalMap()
    被测环境 = global_map.get("env")
    用户别名 = "省级"
    用户名 = MyData().userinfo(被测环境, 用户别名)["username"]
    密码 = MyData().userinfo(被测环境, 用户别名)["password"]
    context: BrowserContext = new_context()
    page = context.new_page()
    my_page = PageIns(page)
    my_page.登录页.登录_发送短信验证码按钮60s倒计时内刷新页面(用户名, 密码, '202208')
