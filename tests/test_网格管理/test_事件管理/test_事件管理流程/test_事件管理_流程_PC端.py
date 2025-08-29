import re
import time

import allure
import pytest
from playwright.sync_api import expect, Page, sync_playwright

from base_case import BaseCase
from module.base_query_page_new import BaseQueryPage
from pages.login_page_pc import LoginPagePc
from pages.pages_h5.上报物业 import PageReportProperty
from pages.pages_h5.首页 import PageHome
from pages.网格管理.三级网格管理.居民上报.居民上报 import PageResidentsReport
from pages.网格管理.事件管理 import PageIncidentManage
from user_data import USERS_BY_ROLE

@pytest.fixture(scope="function")
def close_all_drawers(request):
    """
    在测试用例执行后关闭所有角色页面的抽屉
    """
    yield
    # 获取所有已打开的页面对象
    opened_pages = []

    for name, value in request.node.funcargs.items():
        if isinstance(value, Page):
            opened_pages.append(value)

    # 刷新所有已打开的页面
    for page in opened_pages:
        try:
            page.reload()
        except Exception as e:
            print(f"刷新页面失败: {e}")


def 处理事件(角色页面: Page, 表单数据: dict, 角色名称: str):
    # 将 申请协助(上级) 和 转交(上级) 类似文本中的括号内部的内容去掉
    处理方式 = re.sub(r'\(.*?\)', '', 表单数据.get("处理方式"))
    角色页面.reload()
    if 角色名称 == '三级网格员':
        # 刷新页面
        当前页面 = PageResidentsReport(角色页面)
    else:
        当前页面 = PageIncidentManage(角色页面)

    # 在处理事件之前获取当前第一行的文本或其他唯一标识
    first_row_before = 当前页面.get_table_rows().first.text_content()
    # 处理事件
    当前页面.处理最新事件(表单数据)
    # 验证处理成功，不同角色的提示语不一致，这里只做模糊检查
    expect(当前页面.page.get_by_text("成功")).to_be_visible()

    # 断言处理事件后，之前的首行的处理按钮不再可见
    loc_处理的行 = 当前页面.get_table_rows().filter(has_text=first_row_before)
    expect(loc_处理的行.locator("button",has_text="处理")).not_to_be_visible(timeout=3000)
    expect(loc_处理的行.locator("button",has_text="办理")).not_to_be_visible(timeout=3000)

    # 若转交给物业，那么当前账号将看不到这条记录
    if 处理方式 != "转交物业":
        if 角色名称 != "三级网格员":
            # 三级网格员提交后似乎看不到记录了
            # 点击查看按钮
            if "网格员" in 角色名称:
                当前页面.点击表格中某行按钮(行号=1, 按钮名="详情")
            else:
                当前页面.点击表格中某行按钮(行号=1, 按钮名="查看")
            expect(当前页面.page.locator('.el-timeline-item__timestamp',has_text=角色名称 + 处理方式)).to_be_visible()
            # # 断言处理记录
            # assert 当前页面.处理记录节点_最新.text_content().strip() == 角色名称 + 处理方式, f"页面上的实际值{当前页面.处理记录节点_最新.text_content().strip()}，预期值为{角色名称 + 处理方式}"
            # 关闭抽屉
            角色页面.mouse.click(x=10, y=10)




"""
    可以按照事件传递的方向来划分流程：（1）从下级到上级  （2）从上级到下级
    事件的5种处理方式：（1）跟进。级别不变
                    （2）转交（同级）。级别不变
                     （3）办结。结束
                       （4）下发。级别向下
                         （5）转交网格员。级别向上
    工作人员级别：一级 > 二级 > 三级 > 物管 > 物工 > 居民
"""

pytestmark = pytest.mark.usefixtures("close_all_drawers")

class TestProcess居民到物管(BaseCase):
    # @pytest.mark.parametrize("page_pc_specific_role", ["物业管理员1"], indirect=True)
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_物管",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报，物管办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_h5_居民")
    # @allure.step("以居民为起点，物管为终点的事件处理流程")
    def test_process_路径1(self, page_h5_居民, page_pc_物业管理员1, 表单数据_居民: dict, 表单数据_物管: dict):
        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管, "角色名称": "物业管理人员"},
        ]
        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])

    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_物管_跟进, 表单数据_物管_办结",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报，物管跟进",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "跟进",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报，物管先跟进再办结")
    def test_process_路径2(self, page_h5_居民, page_pc_物业管理员1, 表单数据_居民: dict, 表单数据_物管_跟进: dict,
                           表单数据_物管_办结: dict):
        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管_跟进, "角色名称": "物业管理人员"},
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管_办结, "角色名称": "物业管理人员"},
        ]
        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])

    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_物管_转交, 表单数据_物管_办结",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报，物管跟进",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "转交(同级)",
                 "指定处理人": "章**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_物业管理员2")
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报，物管1转交给同级，物管2办结")
    def test_process_路径3(self, page_h5_居民, page_pc_物业管理员1, page_pc_物业管理员2, 表单数据_居民: dict,
                           表单数据_物管_转交: dict,
                           表单数据_物管_办结: dict):
        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        角色列表 = [

            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管_转交, "角色名称": "物业管理人员"},
            {"页面": page_pc_物业管理员2, "表单数据": 表单数据_物管_办结, "角色名称": "物业管理人员"},

        ]

        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])


    # TODO: 未调试
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_物管_下发, 表单数据_物工, 表单数据_三级, 表单数据_物管_办结",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给物业，物管下发给物工，物工转交给三级，三级下发给物管，物管办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "下发",
                 "指定处理人": "石**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "转交网格员",
                 "指定处理人": "陶**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "转交物业",
                 "处理描述": "同意",
                 "照片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_pc_物业工作人员")
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给物业，物管下发给物工，物工转交给三级，三级下发给物管，物管办结")
    def test_process_路径4(self, page_h5_居民, page_pc_物业管理员1, page_pc_物业工作人员, page_pc_三级网格员,
                           表单数据_居民: dict, 表单数据_物管_下发: dict, 表单数据_物工: dict, 表单数据_三级: dict,
                           表单数据_物管_办结: dict):
        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管_下发, "角色名称": "物业管理人员"},
            {"页面": page_pc_物业工作人员, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
            {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管_办结, "角色名称": "物业管理人员"},
        ]
        for 角色 in 角色列表:
            # 激活当前页面，让它显示在前台
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])

    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_三级, 表单数据_物管",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给社区，三级下发给物管，物管办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "转交物业",
                 # "指定处理人": "金**",
                 "处理描述": "同意",
                 "照片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给社区，三级下发给物管，物管办结")
    def test_process_路径5(self, page_h5_居民, page_pc_三级网格员, page_pc_物业管理员1,
                           表单数据_居民: dict, 表单数据_三级: dict, 表单数据_物管: dict):

        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管, "角色名称": "物业管理人员"},
        ]
        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])

    # TODO:未调通 三级转交给物管后，物管收不到待处理的事件
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_三级_上传, 表单数据_二级_上传, 表单数据_一级,表单数据_二级_下发, 表单数据_三级_下发,表单数据_物管",
        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给社区，三级申请二级的协助，二级申请一级的协助，一级下发给二级，二级下发给三级，三级转派给物管，物管办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "陶**",
                 "处理描述": "同意",
                 # "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "石**",
                 "处理描述": "同意"
             },
             {
                 "处理方式": "下发",
                 "指定处理人": "陶**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "下发",
                 "指定处理人": "陶**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "转交物业",
                 "处理描述": "同意",
                 "照片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_pc_一级网格员")
    @pytest.mark.usefixtures("page_pc_二级网格员")
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step(
        "居民上报给社区，三级申请二级的协助，二级申请一级的协助，一级下发给二级，二级下发给三级，三级转派给物管，物管办结")
    def test_process_路径6(self, page_h5_居民, page_pc_三级网格员, page_pc_二级网格员, page_pc_一级网格员,
                           page_pc_物业管理员1,
                           表单数据_居民: dict, 表单数据_三级_上传: dict, 表单数据_二级_上传: dict, 表单数据_一级: dict,
                           表单数据_二级_下发: dict, 表单数据_三级_下发: dict,
                           表单数据_物管: dict):


        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级_上传, "角色名称": "三级网格员"},
            {"页面": page_pc_二级网格员, "表单数据": 表单数据_二级_上传, "角色名称": "二级网格员"},
            {"页面": page_pc_一级网格员, "表单数据": 表单数据_一级, "角色名称": "一级网格员"},
            {"页面": page_pc_二级网格员, "表单数据": 表单数据_二级_下发, "角色名称": "二级网格员"},
            {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级_下发, "角色名称": "三级网格员"},
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管, "角色名称": "物业管理人员"},

        ]

        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])



class TestProcess居民到物工(BaseCase):
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_物管, 表单数据_物工",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报，物管下发，物工办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "下发",
                 "指定处理人": "石**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_物业工作人员")
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报，物管下发，物工办结")
    def test_process_路径1(self, page_h5_居民, page_pc_物业管理员1, page_pc_物业工作人员, 表单数据_居民: dict,
                           表单数据_物管: dict, 表单数据_物工: dict):
        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管, "角色名称": "物业管理人员"},
            {"页面": page_pc_物业工作人员, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
        ]
        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])


class TestProcess居民到三级(BaseCase):
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_三级",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给社区，三级管理员办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "办结",
                 "处理描述": "同意",
                 "照片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给社区，三级网格员办结")
    def test_process_路径1(self, page_h5_居民, page_pc_三级网格员, 表单数据_居民: dict,
                           表单数据_三级: dict):
        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
        ]
        try:
            for 角色 in 角色列表:
                角色["页面"].bring_to_front()
                处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])
        except Exception:
            time.sleep(1000)


    # TODO: 转交网格员后，三级收不到，二级能收到，等待开发那边修改
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_物管, 表单数据_物工, 表单数据_三级",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给物管，物管下发给物工，物工转交给三级，三级网格员办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "下发",
                 "指定处理人": "石**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "转交网格员",
                 "指定处理人": "陶**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "办结",
                 "处理描述": "同意",
                 "照片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_pc_物业工作人员")
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给物业，物管下发给物工，物工转交给三级，三级网格员办结")
    def test_process_路径2(self, page_h5_居民, page_pc_物业管理员1, page_pc_物业工作人员, page_pc_三级网格员,
                           表单数据_居民: dict, 表单数据_物管: dict, 表单数据_物工: dict, 表单数据_三级: dict):

        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管, "角色名称": "物业管理人员"},
            {"页面": page_pc_物业工作人员, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
            {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},

        ]

        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])


class TestProcess居民到二级(BaseCase):
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_三级, 表单数据_二级",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给社区，三级网格员转交给二级，二级办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "陶**",
                 "处理描述": "同意",

             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_二级网格员")
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给社区，三级向二级申请协助，二级办结")
    def test_process_路径1(self, page_h5_居民, page_pc_三级网格员, page_pc_二级网格员, 表单数据_居民: dict,
                           表单数据_三级: dict, 表单数据_二级: dict):
        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_pc_二级网格员, "表单数据": 表单数据_二级, "角色名称": "二级网格员"},
        ]

        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_物管, 表单数据_物工, 表单数据_三级, 表单数据_二级",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级网格员办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "下发",
                 "指定处理人": "石**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "转交网格员",
                 "指定处理人": "陶**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "陶**",
                 "处理描述": "同意",
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_二级网格员")
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_pc_物业工作人员")
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级网格员办结")
    def test_process_路径2(self, page_h5_居民, page_pc_物业管理员1, page_pc_物业工作人员, page_pc_三级网格员,
                           page_pc_二级网格员,
                           表单数据_居民: dict, 表单数据_物管: dict, 表单数据_物工: dict, 表单数据_三级: dict,
                           表单数据_二级: dict):
        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        # 处理事件
        角色列表 = [
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管, "角色名称": "物业管理人员"},
            {"页面": page_pc_物业工作人员, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
            {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_pc_二级网格员, "表单数据": 表单数据_二级, "角色名称": "二级网格员"},
        ]
        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])


class TestProcess居民到一级(BaseCase):
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_三级, 表单数据_二级, 表单数据_一级",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给社区，三级网格员转交给二级，二级办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "陶**",
                 "处理描述": "同意",
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "石**",
                 "处理意见": "同意"
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_一级网格员")
    @pytest.mark.usefixtures("page_pc_二级网格员")
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给社区，三级向二级申请协助，二级向一级申请协助，一级办结")
    def test_process_路径1(self, page_h5_居民, page_pc_三级网格员, page_pc_二级网格员, page_pc_一级网格员,
                           表单数据_居民: dict,
                           表单数据_三级: dict, 表单数据_二级: dict, 表单数据_一级: dict):
        try:
            page_h5_居民.bring_to_front()
            首页 = PageHome(page_h5_居民)
            首页.切换角色("居民")
            # 跳转到上报物业，进行一次上报
            首页.跳转到上报社区()
            上报社区页面_居民 = PageReportProperty(page_h5_居民)
            上报社区页面_居民.上报事件(表单数据_居民)

            角色列表 = [
                {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
                {"页面": page_pc_二级网格员, "表单数据": 表单数据_二级, "角色名称": "二级网格员"},
                {"页面": page_pc_一级网格员, "表单数据": 表单数据_一级, "角色名称": "一级网格员"},

            ]

            for 角色 in 角色列表:
                角色["页面"].bring_to_front()
                处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])
        except:
            time.sleep(1000)
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_物管, 表单数据_物工, 表单数据_三级, 表单数据_二级, 表单数据_一级",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级网格员办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "下发",
                 "指定处理人": "石**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "转交网格员",
                 "指定处理人": "陶**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "陶**",
                 "处理描述": "同意",
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "石**",
                 "处理意见": "同意"
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_pc_一级网格员")
    @pytest.mark.usefixtures("page_pc_二级网格员")
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_pc_物业工作人员")
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级网格员办结")
    def test_process_路径2(self, page_h5_居民, page_pc_物业管理员1, page_pc_物业工作人员, page_pc_三级网格员,
                           page_pc_二级网格员, page_pc_一级网格员,
                           表单数据_居民: dict, 表单数据_物管: dict, 表单数据_物工: dict, 表单数据_三级: dict,
                           表单数据_二级: dict, 表单数据_一级: dict):

        page_h5_居民.bring_to_front()
        首页 = PageHome(page_h5_居民)
        首页.切换角色("居民")
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        # 处理事件
        角色列表 = [
            {"页面": page_pc_物业管理员1, "表单数据": 表单数据_物管, "角色名称": "物业管理人员"},
            {"页面": page_pc_物业工作人员, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
            {"页面": page_pc_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_pc_二级网格员, "表单数据": 表单数据_二级, "角色名称": "二级网格员"},
            {"页面": page_pc_一级网格员, "表单数据": 表单数据_一级, "角色名称": "一级网格员"},
        ]
        for 角色 in 角色列表:
            角色["页面"].bring_to_front()
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])


if __name__ == '__main__':
    with sync_playwright() as playwright:
        # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        # 通过ip和端口连接到已经打开的chromium浏览器
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(3000)  # 设置默认超时时间为 3000 毫秒
        处理事件(page,{"处理方式": "办结", "处理描述": "很好很薄", "照片": r"C:\Users\Administrator\Pictures\111.png"},"三级网格员")

