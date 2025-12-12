from playwright.sync_api import expect

from module.BasePage import 使用new_context登录并返回实例化的page
from testcases import *
from utils.GetPath import get_path

@用例名称("测试类型管理的列表数据权限功能")
@用例描述("""
1.登录街道管理员账号，并跳转到类型管理页面
2.查看表格中所属组织这一列，断言其全部等于“中电数智街道”
3.登录一级网格员账号，并跳转到类型管理页面
4.查看表格中所属组织这一列，断言其全部等于“中电数智街道”
""")
def test_验证列表数据权限(new_context):
    列表_需要登录的用户别名 = [
        "街道管理员-中电数智街道",
        "一级网格员",

    ]
    for 用户名 in 列表_需要登录的用户别名:
        my_page_用户 = 使用new_context登录并返回实例化的page(new_context, 用户名)
        with 测试步骤("跳转到类型管理页面"):
            my_page_用户.类型管理.navigate()
            my_page_用户.类型管理.table.get_col_list("所属组织")
            col_所属组织 = my_page_用户.类型管理.table.get_col_list("所属组织")
            assert all(值 == "中电数智街道" for 值 in
                       col_所属组织), f"期望所有值都是'中电数智街道'，但实际列表为: {col_所属组织}"

@用例名称("测试类型管理的菜单权限功能")
@用例描述("""
1.登录各种角色账号，并跳转到类型管理页面
2.查看二级菜单下是否有类型管理菜单
""")
def test_验证菜单权限(new_context):
    列表_需要登录的用户别名 = [
        "省级管理员-安徽省",
        "街道管理员-中电数智街道",
        "社区管理员-中电数智社区",
        "物业管理人员-天王巷",
        "物业工作人员-小区99",
        "一级网格员",
        "二级网格员",
        "三级网格员",
    ]

    for 用户名 in 列表_需要登录的用户别名:
        my_page_用户 = 使用new_context登录并返回实例化的page(new_context, 用户名)
        with 测试步骤("跳转到类型管理页面"):
            my_page_用户.类型管理.navigate()
        with 测试步骤("查看表格中所属组织这一列，断言其全部等于“中电数智街道”"):
            if "街道管理员" in 用户名 or "一级网格员" in 用户名:
                expect(my_page_用户.类型管理.page.locator("li[class='el-menu-item is-active']", has_text="类型管理")).to_be_visible()
            else:
                expect(my_page_用户.类型管理.page.get_by_text("当前用户无权限").or_(my_page_用户.类型管理.page.get_by_text("暂无访问权限"))).to_be_visible()