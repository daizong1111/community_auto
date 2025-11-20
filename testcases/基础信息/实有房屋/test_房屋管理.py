from playwright.sync_api import expect

from module.BasePage import 使用new_context登录并返回实例化的page
from testcases import *
from utils.GetPath import get_path


@用例名称("测试房屋管理的批量导入、批量删除功能")
@用例描述("""
1.下载模板
2.向模板文件中插入数据
3.上传文件
4.搜索，验证文件中数据插入了表格中，勾选表格中所有的数据，点击批量删除按钮
5.验证表格中数据量为0
""")
def test_房屋管理_批量删除房屋(new_context):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到房屋管理页面"):
        my_page_测试员.房屋管理.navigate()
    with 测试步骤("下载模板"):
        page = my_page_测试员.房屋管理.page
        with page.expect_download() as file:
            # 鼠标悬停在下三角箭头上
            page.locator(".el-dropdown__caret-button").hover()
            # 点击下载模板按钮
            page.get_by_text("下载模版").click()
        file.value.save_as(get_path(f".temp/房屋信息模版.xls"))
    with 测试步骤("向模板文件中插入数据"):
        # 使用xlwt或openpyxl库向Excel模板中写入测试数据
        import xlrd
        from xlutils.copy import copy
        # 读取下载的模板文件
        template_path = get_path(f".temp/房屋信息模版.xls")
        workbook = xlrd.open_workbook(template_path)
        workbook_copy = copy(workbook)
        worksheet = workbook_copy.get_sheet(0)
        # 写入测试数据（根据实际模板结构调整列索引）
        test_data = [["6", "1", "13", "132", "出租", "综合", "100", "国有房产"],
                     ["6", "1", "13", "131", "自住", "住宅", "90", "其它"]]
        for row_idx, row_data in enumerate(test_data, start=1):
            for col_idx, cell_data in enumerate(row_data):
                worksheet.write(row_idx, col_idx, cell_data)

        # 保存修改后的文件
        modified_template_path = get_path(f".temp/房屋信息模版_填充数据.xls")
        workbook_copy.save(modified_template_path)
    with 测试步骤("上传文件"):
        with page.expect_file_chooser() as chooser:
            # 触发导入事件的动作
            page.locator(".el-dropdown__caret-button").hover()
            # my_page_测试员.房屋管理.hover_retry(page.locator(".el-dropdown__caret-button"),page.get_by_text("批量导入",exact=True))
            page.get_by_text("批量导入", exact=True).click()
            my_page_测试员.房屋管理.快捷操作_填写表单_增加根据数据类确定唯一表单版(所属小区="测试商圈")
            my_page_测试员.房屋管理.对话框.locator(".el-button--primary", has_text="确定").click()
        chooser.value.set_files(get_path(f".temp/房屋信息模版_填充数据.xls"))
        # 等待上传完成提示
        expect(page.get_by_text("导入成功")).to_be_visible(timeout=3000)
    with 测试步骤("搜索，验证数据成功导入，勾选表格中所有的数据，点击批量删除按钮"):
        my_page_测试员.房屋管理.快捷操作_填写表单_增加根据数据类确定唯一表单版(门牌号="13")
        my_page_测试员.房屋管理.click_button("搜索")
        # 验证导入的数据是否显示在表格中
        for row_data in test_data:
            house_num = row_data[3]
            expect(my_page_测试员.房屋管理.table.table_body.locator("tr").filter(has_text=house_num)).to_be_visible()
        for row_label in my_page_测试员.房屋管理.table.labels_loc.all():
            row_label.click()
        # 删除测试数据
        my_page_测试员.房屋管理.click_button("批量删除")
        my_page_测试员.房屋管理.click_button("确定")
        expect(my_page_测试员.房屋管理.page.get_by_text("删除成功")).to_be_visible()
    with 测试步骤("验证表格中暂无数据"):
        expect(my_page_测试员.房屋管理.page.get_by_text("暂无数据")).to_be_visible()

@用例名称("验证一房一档的页面数据")
@用例描述("""
1.获取该房屋的详细数据
2.跳转到一房一档页面，核对每个居民的详细信息
""")
def test_一房一档_验证页面数据(new_context):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到房屋管理页面"):
        my_page_测试员.房屋管理.navigate()
    行号 = 1
    with 测试步骤("获取该房屋的详细数据"):
        row_dict = my_page_测试员.房屋管理.table.get_row_dict(行号)
        小区名称_预期值 = row_dict["小区名称"]
        门牌号_预期值 = row_dict["门牌号"]
        楼栋名称_预期值 = row_dict["楼栋名称"]
        单元名称_预期值 = row_dict["单元名称"]
    with 测试步骤("打开一房一档页面，核对每个居民的详细信息"):
        my_page_测试员.房屋管理.table.点击表格中某行按钮(loc_行or行号or关键字=行号, 按钮名="一房一档")
        my_page_测试员.一房一档.table.等待表格加载完成()
        for i in range(5):
            try:
                my_page_测试员.一房一档.table.点击表格中某行按钮(loc_行or行号or关键字=i, 按钮名="编辑")
            except:
                # 若是表格中没有行号为i的数据，则跳出循环
                break
            my_page_测试员.一房一档.校验表单中数据成功修改(所属小区=小区名称_预期值, 房屋=门牌号_预期值,楼栋=楼栋名称_预期值, 单元=单元名称_预期值)
            my_page_测试员.一房一档.关闭抽屉()