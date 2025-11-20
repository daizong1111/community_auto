from playwright.sync_api import expect

from module.BasePage import 使用new_context登录并返回实例化的page
from testcases import *
from utils.GetPath import get_path


@用例名称("测试楼栋管理的批量导入楼栋功能")
@用例描述("""
1.下载模板
2.向模板文件中插入数据
3.上传文件
4.验证文件中数据插入了表格中
""")
def test_楼栋管理_批量导入楼栋(new_context):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到楼栋管理页面"):
        my_page_测试员.楼栋管理.navigate()
    with 测试步骤("下载模板"):
        page = my_page_测试员.楼栋管理.page
        with page.expect_download() as file:
            # 鼠标悬停在下三角箭头上
            page.locator(".el-dropdown__caret-button").hover()
            # 点击下载模板按钮
            page.get_by_text("下载模版").click()
        file.value.save_as(get_path(f".temp/楼栋信息模版.xls"))
    with 测试步骤("向模板文件中插入数据"):
        # 使用xlwt或openpyxl库向Excel模板中写入测试数据
        import xlrd
        from xlutils.copy import copy
        # 读取下载的模板文件
        template_path = get_path(f".temp/楼栋信息模版.xls")
        workbook = xlrd.open_workbook(template_path)
        workbook_copy = copy(workbook)
        worksheet = workbook_copy.get_sheet(0)
        # 写入测试数据（根据实际模板结构调整列索引）
        test_data = [["30", "5", "30", "118", "200", "自动化测试_01"],
                     ["31", "6", "40", "120", "202", "自动化测试_02"]]
        for row_idx, row_data in enumerate(test_data, start=1):
            for col_idx, cell_data in enumerate(row_data):
                worksheet.write(row_idx, col_idx, cell_data)

        # 保存修改后的文件
        modified_template_path = get_path(f".temp/楼栋信息模版_填充数据.xls")
        workbook_copy.save(modified_template_path)
    with 测试步骤("上传文件"):
        with page.expect_file_chooser() as chooser:
            # 触发导入事件的动作
            page.locator(".el-dropdown__caret-button").hover()
            # my_page_测试员.楼栋管理.hover_retry(page.locator(".el-dropdown__caret-button"),page.get_by_text("批量导入",exact=True))
            page.get_by_text("批量导入",exact=True).click()
            my_page_测试员.楼栋管理.快捷操作_填写表单_增加根据数据类确定唯一表单版(所属小区="测试商圈")
            my_page_测试员.楼栋管理.对话框.locator(".el-button--primary", has_text="确定").click()
        chooser.value.set_files(get_path(f".temp/楼栋信息模版_填充数据.xls"))
        # 等待上传完成提示
        expect(page.get_by_text("导入成功")).to_be_visible(timeout=3000)
    with 测试步骤("验证文件中数据插入了表格"):
        my_page_测试员.楼栋管理.快捷操作_填写表单_增加根据数据类确定唯一表单版(楼栋名称="自动化测试")
        my_page_测试员.楼栋管理.click_button("搜索")
        # 验证导入的数据是否显示在表格中
        for row_data in test_data:
            building_name = row_data[-1]
            expect(my_page_测试员.楼栋管理.table.table_body.locator("tr").filter(has_text=building_name)).to_be_visible()
            # 删除测试数据
            my_page_测试员.楼栋管理.table.点击表格中某行按钮(loc_行or行号or关键字=0, 按钮名="删除")
            my_page_测试员.楼栋管理.click_button("确定")
            expect(my_page_测试员.楼栋管理.page.get_by_text("删除成功")).to_be_visible()






