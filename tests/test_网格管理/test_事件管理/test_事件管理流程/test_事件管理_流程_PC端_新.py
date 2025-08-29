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

# 定义需要创建页面夹具的物业相关角色
PROPERTY_ROLES = ['物业管理员1', '物业管理员2', '物业工作人员']
# 定义需要创建页面夹具的网格员角色
GRID_ROLES = ['三级网格员', '二级网格员', '一级网格员']

# 存放角色到page的映射
role_to_page = {}

@pytest.fixture(scope="module")
def page_pc_by_roles(request, browser):
    """根据角色列表参数创建多个页面的夹具，会自动跳转到相应菜单"""
    roles = request.param if isinstance(request.param, list) else [request.param]
    pages_dict = {}
    contexts = []

    for role in roles:
        context = browser.new_context()
        contexts.append(context)
        page = context.new_page()
        page.set_default_timeout(5000)
        login_page = LoginPagePc(page)
        login_page.goto()
        login_page.登录(USERS_BY_ROLE[role]['username'], USERS_BY_ROLE[role]['password'], '202208')
        login_page.进入系统()

        query_page = BaseQueryPage(page)
        # 根据角色类型跳转到相应的菜单
        if role in PROPERTY_ROLES:
            query_page.跳转到某菜单("物业服务", "事件管理")
        elif role == '三级网格员':
            query_page.跳转到某菜单("网格管理", "三级网格管理/居民上报")
        else:
            # 适用于一级、二级网格员
            query_page.跳转到某菜单("网格管理", "事件管理")

        role_to_page[role] = page
        pages_dict[role] = page

    yield pages_dict

    # 清理资源
    for page in pages_dict.values():
        page.close()
    for context in contexts:
        context.close()

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
    expect(loc_处理的行.locator("button", has_text="处理")).not_to_be_visible(timeout=3000)
    expect(loc_处理的行.locator("button", has_text="办理")).not_to_be_visible(timeout=3000)

    # 若转交给物业，那么当前账号将看不到这条记录
    if 处理方式 != "转交物业":
        if 角色名称 not in("三级网格员", "物业工作人员"):
            # 三级网格员提交后似乎看不到记录了
            # 点击查看按钮
            if "网格员" in 角色名称:
                当前页面.点击表格中某行按钮(行号=1, 按钮名="详情")
            else:
                当前页面.点击表格中某行按钮(行号=1, 按钮名="查看")
            expect(当前页面.page.locator('.el-timeline-item__timestamp', has_text=角色名称 + 处理方式)).to_be_visible(timeout=8000)
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


@pytest.mark.usefixtures("page_h5_居民")
@allure.step("居民上报事件处理流程综合测试")
@pytest.mark.parametrize("page_pc_by_roles, test_scenario", [
    # 居民到物管的测试场景
    (
        ["物业管理员1"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报，物管办结",
            "resident_action": "上报物业",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报，物管办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [{
                    "角色": "物业管理员1",
                    "表单数据": {
                        "处理方式": "办结",
                        "处理意见": "同意",
                        "图片": r"C:\Users\Administrator\Pictures\111.png"
                    }
                }]
            }
        }
    ),
    (
        ["物业管理员1"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报，物管先跟进再办结",
            "resident_action": "上报物业",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报，物管跟进",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "跟进",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    ),
    (
        ["物业管理员1", "物业管理员2"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报，物管1转交给同级，物管2办结",
            "resident_action": "上报物业",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报，物管跟进",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "转交(同级)",
                            "指定处理人": "章**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "物业管理员2",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    ),
    (
        ["物业管理员1", "物业工作人员", "三级网格员"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报给物业，物管下发给物工，物工转交给三级，三级下发给物管，物管办结",
            "resident_action": "上报物业",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报给物业，物管下发给物工，物工转交给三级，三级下发给物管，物管办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "下发",
                            "指定处理人": "石**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "物业工作人员",
                        "表单数据": {
                            "处理方式": "转交网格员",
                            "指定处理人": "陶**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "三级网格员",
                        "表单数据": {
                            "处理方式": "转交物业",
                            "处理描述": "同意",
                            "照片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    ),
    (
        ["三级网格员", "物业管理员1"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报给社区，三级下发给物管，物管办结",
            "resident_action": "上报社区",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报给社区，三级下发给物管，物管办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "三级网格员",
                        "表单数据": {
                            "处理方式": "转交物业",
                            "处理描述": "同意",
                            "照片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    ),
    # 居民到物工的测试场景
    (
        ["物业管理员1", "物业工作人员"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报，物管下发，物工办结",
            "resident_action": "上报物业",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报，物管下发，物工办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "下发",
                            "指定处理人": "石**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "物业工作人员",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    ),
    # 居民到三级的测试场景
    (
        ["三级网格员"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报给社区，三级管理员办结",
            "resident_action": "上报社区",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报给社区，三级管理员办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [{
                    "角色": "三级网格员",
                    "表单数据": {
                        "处理方式": "办结",
                        "处理描述": "同意",
                        "照片": r"C:\Users\Administrator\Pictures\111.png"
                    }
                }]
            }
        }
    ),
    (
        ["物业管理员1", "物业工作人员", "三级网格员"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报给物管，物管下发给物工，物工转交给三级，三级网格员办结",
            "resident_action": "上报物业",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报给物管，物管下发给物工，物工转交给三级，三级网格员办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "下发",
                            "指定处理人": "石**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "物业工作人员",
                        "表单数据": {
                            "处理方式": "转交网格员",
                            "指定处理人": "陶**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "三级网格员",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理描述": "同意",
                            "照片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    ),
    # 居民到二级的测试场景
    (
        ["三级网格员", "二级网格员"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报给社区，三级向二级申请协助，二级办结",
            "resident_action": "上报社区",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报给社区，三级网格员转交给二级，二级办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "三级网格员",
                        "表单数据": {
                            "处理方式": "申请协助(上级)",
                            "指定处理人": "陶**",
                            "处理描述": "同意",
                        }
                    },
                    {
                        "角色": "二级网格员",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    ),
    (
        ["物业管理员1", "物业工作人员", "三级网格员", "二级网格员"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级网格员办结",
            "resident_action": "上报物业",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级网格员办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "下发",
                            "指定处理人": "石**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "物业工作人员",
                        "表单数据": {
                            "处理方式": "转交网格员",
                            "指定处理人": "陶**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "三级网格员",
                        "表单数据": {
                            "处理方式": "申请协助(上级)",
                            "指定处理人": "陶**",
                            "处理描述": "同意",
                        }
                    },
                    {
                        "角色": "二级网格员",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    ),
    # 居民到一级的测试场景
    (
        ["三级网格员", "二级网格员", "一级网格员"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报给社区，三级向二级申请协助，二级向一级申请协助，一级办结",
            "resident_action": "上报社区",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报给社区，三级网格员转交给二级，二级办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "三级网格员",
                        "表单数据": {
                            "处理方式": "申请协助(上级)",
                            "指定处理人": "陶**",
                            "处理描述": "同意",
                        }
                    },
                    {
                        "角色": "二级网格员",
                        "表单数据": {
                            "处理方式": "申请协助(上级)",
                            "指定处理人": "石**",
                            "处理意见": "同意"
                        }
                    },
                    {
                        "角色": "一级网格员",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    ),
    (
        ["物业管理员1", "物业工作人员", "三级网格员", "二级网格员", "一级网格员"],  # 传给page_pc_by_roles的参数
        {
            "name": "居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级网格员办结",
            "resident_action": "上报物业",
            "data": {
                "表单数据_居民": {
                    "上报类型": "建议",
                    "上报描述": "居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级网格员办结",
                    "上报图片路径": ""
                },
                "表单数据_处理": [
                    {
                        "角色": "物业管理员1",
                        "表单数据": {
                            "处理方式": "下发",
                            "指定处理人": "石**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "物业工作人员",
                        "表单数据": {
                            "处理方式": "转交网格员",
                            "指定处理人": "陶**",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    },
                    {
                        "角色": "三级网格员",
                        "表单数据": {
                            "处理方式": "申请协助(上级)",
                            "指定处理人": "陶**",
                            "处理描述": "同意",
                        }
                    },
                    {
                        "角色": "二级网格员",
                        "表单数据": {
                            "处理方式": "申请协助(上级)",
                            "指定处理人": "石**",
                            "处理意见": "同意"
                        }
                    },
                    {
                        "角色": "一级网格员",
                        "表单数据": {
                            "处理方式": "办结",
                            "处理意见": "同意",
                            "图片": r"C:\Users\Administrator\Pictures\111.png"
                        }
                    }
                ]
            }
        }
    )
], indirect=["page_pc_by_roles"])  # 指定page_pc_by_roles是间接参数
def test_process_combined(page_h5_居民, test_scenario, page_pc_by_roles):
    """
    综合测试事件处理流程
    """
    # try:
        # 使用page_pc_by_roles fixture根据角色列表创建页面
    pages_dict = page_pc_by_roles

    # 居民上报事件
    page_h5_居民.bring_to_front()
    首页 = PageHome(page_h5_居民)
    首页.切换角色("居民")

    # 根据场景决定上报类型
    if test_scenario["resident_action"] == "上报物业":
        首页.跳转到上报物业()
    else:
        首页.跳转到上报社区()

    上报物业页面_居民 = PageReportProperty(page_h5_居民)
    上报物业页面_居民.上报事件(test_scenario["data"]["表单数据_居民"])

    # 处理事件流程
    for 处理步骤 in test_scenario["data"]["表单数据_处理"]:
        role = 处理步骤["角色"]
        表单数据 = 处理步骤["表单数据"]

        # 获取对应角色的页面
        role_page = pages_dict[role]
        role_page.bring_to_front()

        # 确定角色名称用于处理事件函数
        role_name = ""
        if "物业管理员" in role:
            role_name = "物业管理人员"
        elif "物业工作人员" in role:
            role_name = "物业工作人员"
        elif "三级网格员" == role:
            role_name = "三级网格员"
        elif "二级网格员" == role:
            role_name = "二级网格员"
        elif "一级网格员" == role:
            role_name = "一级网格员"

        处理事件(role_page, 表单数据, role_name)

    # except Exception as e:
    #     print(f"发生异常：{e}")
    #     time.sleep(100000)



