import random
import time
from datetime import datetime

import pytest
from playwright.sync_api import expect

from module.BasePage import 使用new_context登录并返回实例化的page
from testcases import *



# TODO:跑之前要检查数据是否存在，若存在，则删除
def test_一人一档(new_context):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到人口信息页面"):
        my_page_测试员.人口信息.navigate()
    with 测试步骤("新增一个人口"):
        my_page_测试员.人口信息.click_button("新增")
        timestamp = datetime.now().strftime("%H:%M:%S")
        姓名 = f"自动化创建_{timestamp}"
        人口信息_新增 = {"姓名": 姓名,"性别": "男", "人口类型": "常住人口", "手机号码": "15655426823",
                         "民族": "汉族", "籍贯": "北京市/市辖区/东城区", "出生日期": "2025-11-4", "身份证号码":"340421199711170018",
                         "所属小区": "小区99", "与房主关系": "租客", "楼栋": "1栋",
                         "单元": "1单元", "房屋": "101"}
        my_page_测试员.人口信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**人口信息_新增)
        my_page_测试员.人口信息.click_button("确定")
        expect(my_page_测试员.人口信息.page.get_by_text("保存成功")).to_be_visible()

    with 测试步骤("新增一个车辆"):
        my_page_测试员.车辆信息.navigate()
        my_page_测试员.车辆信息.click_button("新增")
        车辆信息_新增 = {"车牌号码": "皖A12345", "小区名称": "中电数智街道/中电数智社区/小区99", "车主姓名": 姓名, "手机号码": "15655426823",
                         "身份证号码":"340421199711170018", "车辆品牌": "奥迪", "车辆类型": "大型客车",
                         "车身颜色": "灰", "号牌类型": "大型汽车号牌", "号牌颜色": "黄"}
        my_page_测试员.车辆信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(**车辆信息_新增)
        my_page_测试员.车辆信息.click_button("确定")

    with 测试步骤("核对一人一档信息"):
        my_page_测试员.人口信息.navigate()
        my_page_测试员.人口信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(姓名= 姓名)
        my_page_测试员.人口信息.click_button("搜索")
        my_page_测试员.人口信息.table.点击表格中某行按钮(loc_行or行号or关键字=0, 按钮名="一人一档")
        my_page_测试员.一人一档.校验个人信息(性别=人口信息_新增["性别"],电话=人口信息_新增["手机号码"])
        my_page_测试员.一人一档.校验关联房屋(与房主关系=人口信息_新增["与房主关系"])
        my_page_测试员.一人一档.校验关联车辆(车牌号=车辆信息_新增["车牌号码"])
    with 测试步骤("删除车辆"):
        my_page_测试员.车辆信息.navigate()
        my_page_测试员.车辆信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(手机号="15655426823")
        my_page_测试员.车辆信息.click_button("搜索")
        my_page_测试员.车辆信息.table.等待表格加载完成()
        start = time.time()
        while True:
            if time.time() - start > 30:
                break
            try:
                my_page_测试员.车辆信息.table.点击表格中某行按钮(loc_行or行号or关键字=0, 按钮名="删除")
                my_page_测试员.车辆信息.click_button("确定")
                expect(my_page_测试员.车辆信息.page.get_by_text("删除成功")).to_be_visible()
            except:
                break
    with 测试步骤("删除人口"):
        my_page_测试员.人口信息.navigate()
        my_page_测试员.人口信息.快捷操作_填写表单_增加根据数据类确定唯一表单版(姓名=姓名)
        my_page_测试员.人口信息.click_button("搜索")
        my_page_测试员.人口信息.table.等待表格加载完成()
        start = time.time()
        while True:
            if time.time() - start > 30:
                break
            try:
                my_page_测试员.人口信息.table.点击表格中某行按钮(loc_行or行号or关键字=0, 按钮名="删除")
                my_page_测试员.人口信息.click_button("确定")
                expect(my_page_测试员.人口信息.page.get_by_text("删除成功")).to_be_visible()
            except:
                break