import random
import time
from datetime import datetime

import pytest
from playwright.sync_api import expect

from module.BasePage import 使用new_context登录并返回实例化的page
from testcases import *

import random
def generate_unique_coordinates():
     # 生成随机的区域坐标集，供新增小区时使用
     base_longitude = random.uniform(110, 120)
     base_latitude = random.uniform(30, 40)
     coordinates = []
     for i in range(4):
         lon = base_longitude + random.uniform(-0.01, 0.01)
         lat = base_latitude + random.uniform(-0.01, 0.01)
         coordinates.append(f"{{{lon:.6f},{lat:.6f}}}")
     return ",".join(coordinates)

@用例名称("测试小区信息的新增、修改、删除功能")
@用例描述("""
1.新建一个小区
2.修改一个小区
3.删除一个小区
创建人：石岱宗          
""")
@用例级别(严重)
def test_小区信息_新增修改删除(new_context):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到小区信息页面"):
        my_page_测试员.小区信息.navigate()
    with 测试步骤("新增一个小区"):
        my_page_测试员.小区信息.click_button("新增")
        timestamp = datetime.now().strftime("%H:%M:%S")
        小区名称 = f"自动化创建_{timestamp}"
        唯一的坐标集 = generate_unique_coordinates()
        my_page_测试员.小区信息.填写表单项_小区名称(小区名称)
        小区信息_新增 = {"行政区域":"安徽省/合肥市/庐阳区", "所属居委会":"中电数智社区", "公安机构":"河北省公安局", "小区类型":"商业", "物业名称":"中电数智物业", "小区序号":f"{random.randint(1,999)}",
                       "管理类别":"物管小区", "小区地址":"安徽省合肥市包河区1005号", "地图坐标集":唯一的坐标集, "经度":"118", "纬度":"32"}
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**小区信息_新增)
        my_page_测试员.小区信息.click_button("确定")
        expect(my_page_测试员.小区信息.page.get_by_text("保存成功")).to_be_visible()

        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区名称=小区名称)
        my_page_测试员.小区信息.click_button("搜索")
        expect(my_page_测试员.小区信息.table.table_body.locator("tr").filter(has_text=小区名称).get_by_text("商业")).to_be_visible()
        expect(my_page_测试员.小区信息.table.table_body.locator("tr").filter(has_text=小区名称).get_by_text("物管小区")).to_be_visible()
    with 测试步骤("修改一个小区"):
        my_page_测试员.小区信息.table.点击表格中某行按钮(loc_行or行号or关键字=1, 按钮名="编辑")
        timestamp = datetime.now().strftime("%H:%M:%S")
        小区名称_修改后 = f"自动化创建_{timestamp}"
        唯一的坐标集 = generate_unique_coordinates()
        my_page_测试员.小区信息.填写表单项_小区名称(小区名称_修改后)
        小区信息_修改 = {"行政区域": "安徽省/合肥市/庐阳区", "公安机构": "邯郸市公安局",
                         "小区类型": "自营", "物业名称": "大同物业",
                         "管理类别": "社区代管", "小区地址": "安徽省淮北市相山区1006号",
                         "地图坐标集": 唯一的坐标集,
                         "经度": "120", "纬度": "34"}
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**小区信息_修改)
        my_page_测试员.小区信息.click_button("确定")
        my_page_测试员.小区信息.点击提示弹窗中的确定按钮()
        expect(my_page_测试员.小区信息.page.get_by_text("保存成功")).to_be_visible()
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区名称=小区名称_修改后)
        my_page_测试员.小区信息.click_button("搜索")
        expect(my_page_测试员.小区信息.table.table_body.locator("tr").filter(has_text=小区名称_修改后).get_by_text(
            "自营")).to_be_visible()
        expect(my_page_测试员.小区信息.table.table_body.locator("tr").filter(has_text=小区名称_修改后).get_by_text(
            "社区代管")).to_be_visible()
    with 测试步骤("删除一个小区"):
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区名称="自动化创建_")
        my_page_测试员.小区信息.click_button("搜索")
        my_page_测试员.小区信息.table.等待表格加载完成()
        start = time.time()
        while True:
            if time.time() - start > 30:
                break
            try:
                my_page_测试员.小区信息.table.点击表格中某行按钮(loc_行or行号or关键字=0, 按钮名="删除")
                my_page_测试员.小区信息.click_button("确定")
                expect(my_page_测试员.小区信息.page.get_by_text("删除成功")).to_be_visible()
            except:
                break

def test_新增小区_去重校验(new_context):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到小区信息页面"):
        my_page_测试员.小区信息.navigate()
    with 测试步骤("新增一个小区"):
        my_page_测试员.小区信息.click_button("新增")
        timestamp = datetime.now().strftime("%H:%M:%S")
        小区名称 = f"自动化创建_{timestamp}"
        小区序号 = f"{random.randint(1, 999)}"
        my_page_测试员.小区信息.填写表单项_小区名称(小区名称)
        唯一的坐标集 = generate_unique_coordinates()
        小区信息_新增 = {"行政区域": "安徽省/合肥市/庐阳区", "所属居委会": "中电数智社区", "公安机构": "河北省公安局",
                         "小区类型": "商业", "物业名称": "中电数智物业", "小区序号": 小区序号,
                         "管理类别": "物管小区", "小区地址": "安徽省合肥市包河区1005号",
                         "地图坐标集": 唯一的坐标集,
                         "经度": "118", "纬度": "32"}
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**小区信息_新增)
        my_page_测试员.小区信息.click_button("确定")
        expect(my_page_测试员.小区信息.page.get_by_text("保存成功")).to_be_visible()

        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区名称=小区名称)
        my_page_测试员.小区信息.click_button("搜索")
        expect(my_page_测试员.小区信息.table.table_body.locator("tr").filter(has_text=小区名称).get_by_text(
            "商业")).to_be_visible()
        expect(my_page_测试员.小区信息.table.table_body.locator("tr").filter(has_text=小区名称).get_by_text(
            "物管小区")).to_be_visible()
    with 测试步骤("再新增一个小区，使用相同的小区序号"):
        my_page_测试员.小区信息.click_button("新增")
        timestamp = datetime.now().strftime("%H:%M:%S")
        小区名称 = f"自动化创建_{timestamp}"
        my_page_测试员.小区信息.填写表单项_小区名称(小区名称)
        唯一的坐标集 = generate_unique_coordinates()
        小区信息_新增 = {"行政区域": "安徽省/合肥市/庐阳区", "所属居委会": "中电数智社区", "公安机构": "河北省公安局",
                         "小区类型": "商业", "物业名称": "中电数智物业", "小区序号": 小区序号,
                         "管理类别": "物管小区", "小区地址": "安徽省合肥市包河区1005号",
                         "地图坐标集": 唯一的坐标集,
                         "经度": "118", "纬度": "32"}
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**小区信息_新增)
        my_page_测试员.小区信息.click_button("确定")
        expect(my_page_测试员.小区信息.page.get_by_text("保存失败,该小区已存在!")).to_be_visible()
    with 测试步骤("删除测试数据"):
        my_page_测试员.小区信息.关闭抽屉()
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区名称="自动化创建_")
        my_page_测试员.小区信息.click_button("搜索")
        my_page_测试员.小区信息.table.等待表格加载完成()
        start = time.time()
        while True:
            if time.time() - start > 30:
                break
            try:
                my_page_测试员.小区信息.table.点击表格中某行按钮(loc_行or行号or关键字=0, 按钮名="删除")
                my_page_测试员.小区信息.click_button("确定")
                expect(my_page_测试员.小区信息.page.get_by_text("删除成功")).to_be_visible()
            except:
                break

def test_新增小区_校验重叠小区区域(new_context):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到小区信息页面"):
        my_page_测试员.小区信息.navigate()
    with 测试步骤("新增一个小区"):
        my_page_测试员.小区信息.click_button("新增")
        timestamp = datetime.now().strftime("%H:%M:%S")
        小区名称 = f"自动化创建_{timestamp}"
        小区序号 = f"{random.randint(1, 999)}"
        my_page_测试员.小区信息.填写表单项_小区名称(小区名称)
        唯一的坐标集 = generate_unique_coordinates()
        小区信息_新增 = {"行政区域": "安徽省/合肥市/庐阳区", "所属居委会": "中电数智社区", "公安机构": "河北省公安局",
                         "小区类型": "商业", "物业名称": "中电数智物业", "小区序号": 小区序号,
                         "管理类别": "物管小区", "小区地址": "安徽省合肥市包河区1005号",
                         "地图坐标集": 唯一的坐标集,
                         "经度": "118", "纬度": "32"}
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**小区信息_新增)
        my_page_测试员.小区信息.click_button("确定")
        expect(my_page_测试员.小区信息.page.get_by_text("保存成功")).to_be_visible()

        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区名称=小区名称)
        my_page_测试员.小区信息.click_button("搜索")
        expect(my_page_测试员.小区信息.table.table_body.locator("tr").filter(has_text=小区名称).get_by_text(
            "商业")).to_be_visible()
        expect(my_page_测试员.小区信息.table.table_body.locator("tr").filter(has_text=小区名称).get_by_text(
            "物管小区")).to_be_visible()
    with 测试步骤("再新增一个小区，使用相同的坐标集"):
        my_page_测试员.小区信息.click_button("新增")
        timestamp = datetime.now().strftime("%H:%M:%S")
        小区名称 = f"自动化创建_{timestamp}"
        小区序号 = f"{random.randint(1, 999)}"
        my_page_测试员.小区信息.填写表单项_小区名称(小区名称)
        小区信息_新增 = {"行政区域": "安徽省/合肥市/庐阳区", "所属居委会": "中电数智社区", "公安机构": "河北省公安局",
                         "小区类型": "商业", "物业名称": "中电数智物业", "小区序号": 小区序号,
                         "管理类别": "物管小区", "小区地址": "安徽省合肥市包河区1005号",
                         "地图坐标集": 唯一的坐标集,
                         "经度": "118", "纬度": "32"}
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**小区信息_新增)
        my_page_测试员.小区信息.click_button("确定")
        expect(my_page_测试员.小区信息.page.get_by_text("小区地图范围区域重合")).to_be_visible()
    with 测试步骤("删除测试数据"):
        my_page_测试员.小区信息.关闭抽屉()
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(小区名称="自动化创建_")
        my_page_测试员.小区信息.click_button("搜索")
        my_page_测试员.小区信息.table.等待表格加载完成()
        start = time.time()
        while True:
            if time.time() - start > 30:
                break
            try:
                my_page_测试员.小区信息.table.点击表格中某行按钮(loc_行or行号or关键字=0, 按钮名="删除")
                my_page_测试员.小区信息.click_button("确定")
                expect(my_page_测试员.小区信息.page.get_by_text("删除成功")).to_be_visible()
            except:
                break

@用例名称("测试搜索小区")
@用例描述("""
1.跳转到小区信息页面
2.输入单个或多个搜索条件
3.检验表格中数据是否满足查询条件
创建人：石岱宗          
""")
@用例级别(普通)
@pytest.mark.parametrize(
        "表单数据_搜索框",
        [
            {"小区类型":"商业"},
            {"管理类别":"物管小区"},
            {"小区名称":"备注输入200字"},
            {"小区类型":"商业", "管理类别":"物管小区", "小区名称":"备注输入200字"},
        ]
    )
def test_搜索小区(new_context,表单数据_搜索框):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到小区信息页面"):
        my_page_测试员.小区信息.navigate()
    with 测试步骤("输入单个或多个搜索条件"):
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_搜索框)
        my_page_测试员.小区信息.click_button("搜索")
        my_page_测试员.小区信息.table.等待表格加载完成()
    # 定义字段与验证逻辑的映射
    def verify_小区类型():
        列表_小区类型 = my_page_测试员.小区信息.table.get_col_list("小区类型")
        小区类型_预期值 = 表单数据_搜索框["小区类型"]

        # 断言 列表_社区 中的每一项都包含 社区_预期值
        assert all(小区类型_预期值 == 小区类型 for 小区类型 in
                   列表_小区类型), f"查询条件-小区类型:{小区类型_预期值}, 表格中的小区类型为:{列表_小区类型}"

    def verify_管理类别():
        列表_管理类别 = my_page_测试员.小区信息.table.get_col_list("管理类别")
        管理类别_预期值 = 表单数据_搜索框["管理类别"]
        # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
        assert all(
            管理类别_预期值 == 管理类别 for 管理类别 in
            列表_管理类别), f"查询条件-管理类别:{管理类别_预期值}, 表格中的管理类别为:{列表_管理类别}"

    def verify_小区名称():
        # 获取输入的申请时间段，并拆分为开始和结束日期
        列表_小区名称 = my_page_测试员.小区信息.table.get_col_list("小区名称")
        小区名称_预期值 = 表单数据_搜索框["小区名称"]
        # 断言 列表_小区名称 中的每一项都包含 小区名称_预期值
        assert all(
            小区名称_预期值 in 小区名称 for 小区名称 in
            列表_小区名称), f"查询条件-小区名称:{小区名称_预期值}, 表格中的小区名称为:{列表_小区名称}"

    # 字典映射字段到验证函数
    验证规则 = {
        "小区类型": verify_小区类型,
        "管理类别": verify_管理类别,
        "小区名称": verify_小区名称,
    }
    with 测试步骤("检验表格中数据是否满足查询条件"):
        # 执行匹配的验证规则
        for field in 表单数据_搜索框:
            if field in 验证规则:
                验证规则[field]()

@用例名称("测试重置小区")
@用例描述("""
1.跳转到小区信息页面
2.输入单个或多个搜索条件
3.对比重置操作前后的数据量
创建人：石岱宗          
""")
@用例级别(普通)
def test_重置小区(new_context):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到小区信息页面"):
        my_page_测试员.小区信息.navigate()
    with 测试步骤("输入单个或多个搜索条件"):
        表单数据_搜索框 = {"小区类型":"商业", "管理类别":"物管小区", "小区名称":"备注输入200字"}
        my_page_测试员.小区信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**表单数据_搜索框)
        my_page_测试员.小区信息.click_button("搜索")
        my_page_测试员.小区信息.table.等待表格加载完成()
    with 测试步骤("对比重置操作前后的数据量"):
        表格数据量_重置前 = my_page_测试员.小区信息.table.获取页面统计的总数据量()
        my_page_测试员.小区信息.click_button("重置")
        my_page_测试员.小区信息.table.等待表格加载完成()
        表格数据量_重置后 = my_page_测试员.小区信息.table.获取页面统计的总数据量()
        assert 表格数据量_重置后 > 表格数据量_重置前, f"表格数据量_重置前:{表格数据量_重置前}, 表格数据量_重置后:{表格数据量_重置后}"


