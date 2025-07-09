import re

import allure
import pytest
from playwright.sync_api import expect, Page

from base_case import BaseCase
from pages.pages_h5.上报物业 import PageReportProperty
from pages.pages_h5.首页 import PageHome
from pages.网格管理.事件管理 import PageIncidentManage


def 处理事件(角色页面: Page, 表单数据: dict, 角色名称: str):
    角色页面 = PageHome(角色页面)
    角色页面.切换角色(角色名称)
    角色页面.处理工单(表单数据, 角色名称)
    if "网格员" in 角色名称:
        角色页面.page.go_back()
    角色页面.跳转到首页()


"""
    可以按照事件传递的方向来划分流程：（1）从下级到上级  （2）从上级到下级
    事件的5种处理方式：（1）跟进。级别不变
                    （2）转交（同级）。级别不变
                     （3）办结。结束
                       （4）下发。级别向下
                         （5）转交网格员。级别向上
    工作人员级别：一级 > 二级 > 三级 > 物管 > 物工 > 居民
"""


class TestProcess居民到物管(BaseCase):
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
    @allure.step("居民上报物业，物管办结")
    def test_process_路径1(self, page_h5_居民, 表单数据_居民: dict, 表单数据_物管: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        # 处理事件
        角色列表 = [
            {"页面": page_h5_居民, "表单数据": 表单数据_物管, "角色名称": "物业管理员"},
        ]
        for 角色 in 角色列表:
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
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报，物管先跟进再办结")
    def test_process_路径2(self, page_h5_居民, 表单数据_居民: dict, 表单数据_物管_跟进: dict,
                           表单数据_物管_办结: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        # 处理事件
        角色列表 = [
            {"页面": page_h5_居民, "表单数据": 表单数据_物管_跟进, "角色名称": "物业管理员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_物管_办结, "角色名称": "物业管理员"},

        ]
        for 角色 in 角色列表:
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
                 "指定处理人": "金**",
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
    @pytest.mark.usefixtures("page_h5_物业管理员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报，物管1转交给同级，物管2办结")
    def test_process_路径3(self, page_h5_居民, page_h5_物业管理员, 表单数据_居民: dict,
                           表单数据_物管_转交: dict,
                           表单数据_物管_办结: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        # 处理事件
        角色列表 = [
            {"页面": page_h5_居民, "表单数据": 表单数据_物管_转交, "角色名称": "物业管理员"},
            {"页面": page_h5_物业管理员, "表单数据": 表单数据_物管_办结, "角色名称": "物业管理员"},
        ]
        for 角色 in 角色列表:
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])
        # 事件管理页面_物业管理员2.page.wait_for_timeout(10000000)

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
    @pytest.mark.usefixtures("page_h5_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给物业，物管下发给物工，物工转交给三级，三级下发给物管，物管办结")
    def test_process_路径4(self, page_h5_居民, page_h5_三级网格员,
                           表单数据_居民: dict, 表单数据_物管_下发: dict, 表单数据_物工: dict, 表单数据_三级: dict,
                           表单数据_物管_办结: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_h5_居民, "表单数据": 表单数据_物管_下发, "角色名称": "物业管理员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_物管_办结, "角色名称": "物业管理员"},
        ]
        for 角色 in 角色列表:
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])

    # TODO: 系统有bug，三级管理员没有转交物业选项，未调通
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
    @pytest.mark.usefixtures("page_h5_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给社区，三级下发给物管，物管办结")
    def test_process_路径5(self, page_h5_居民, page_h5_三级网格员,
                           表单数据_居民: dict, 表单数据_三级: dict, 表单数据_物管: dict):

        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_物管, "角色名称": "物业管理员"},
        ]
        for 角色 in 角色列表:
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])

    # TODO: 系统有bug，三级管理员没有转交物业选项，未调通
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
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "石**",
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
                 "处理方式": "下发",
                 "指定处理人": "陶**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "转交物业",
                 "指定处理人": "石**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "办结",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
            ),
        ],
    )
    @pytest.mark.usefixtures("page_h5_二级网格员")
    @pytest.mark.usefixtures("page_h5_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step(
        "居民上报给社区，三级申请二级的协助，二级申请一级的协助，一级下发给二级，二级下发给三级，三级转派给物管，物管办结")
    def test_process_路径6(self, page_h5_居民, page_h5_三级网格员, page_h5_二级网格员,
                           表单数据_居民: dict, 表单数据_三级_上传: dict, 表单数据_二级_上传: dict, 表单数据_一级: dict,
                           表单数据_二级_下发: dict, 表单数据_三级_下发: dict,
                           表单数据_物管: dict):

        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级_上传, "角色名称": "三级网格员"},
            {"页面": page_h5_二级网格员, "表单数据": 表单数据_二级_上传, "角色名称": "二级网格员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_一级, "角色名称": "一级网格员"},
            {"页面": page_h5_二级网格员, "表单数据": 表单数据_二级_下发, "角色名称": "二级网格员"},
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级_下发, "角色名称": "三级网格员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_物管, "角色名称": "物业管理员"},
        ]

        for 角色 in 角色列表:
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
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报，物管下发，物工办结")
    def test_process_路径1(self, page_h5_居民, 表单数据_居民: dict,
                           表单数据_物管: dict, 表单数据_物工: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_h5_居民, "表单数据": 表单数据_物管, "角色名称": "物业管理员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
        ]

        for 角色 in 角色列表:
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
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_h5_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给社区，三级网格员办结")
    def test_process_路径1(self, page_h5_居民, page_h5_三级网格员, 表单数据_居民: dict,
                           表单数据_三级: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
        ]

        for 角色 in 角色列表:
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])

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
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             }
            ),
        ],
    )
    @pytest.mark.usefixtures("page_h5_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给物业，物管下发给物工，物工转交给三级，三级网格员办结")
    def test_process_路径2(self, page_h5_居民, page_h5_三级网格员,
                           表单数据_居民: dict, 表单数据_物管: dict, 表单数据_物工: dict, 表单数据_三级: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_h5_居民, "表单数据": 表单数据_物管, "角色名称": "物业管理员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
        ]

        for 角色 in 角色列表:
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
    @pytest.mark.usefixtures("page_h5_二级网格员")
    @pytest.mark.usefixtures("page_h5_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给社区，三级向二级申请协助，二级办结")
    def test_process_路径1(self, page_h5_居民, page_h5_三级网格员, page_h5_二级网格员, 表单数据_居民: dict,
                           表单数据_三级: dict, 表单数据_二级: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_h5_二级网格员, "表单数据": 表单数据_二级, "角色名称": "二级网格员"},
        ]

        for 角色 in 角色列表:
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])

    # TODO: 转交网格员后，三级收不到，二级能收到，等待开发那边修改
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
    @pytest.mark.usefixtures("page_h5_二级网格员")
    @pytest.mark.usefixtures("page_h5_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级网格员办结")
    def test_process_路径2(self, page_h5_居民, page_h5_三级网格员,
                           page_h5_二级网格员,
                           表单数据_居民: dict, 表单数据_物管: dict, 表单数据_物工: dict, 表单数据_三级: dict,
                           表单数据_二级: dict):
        # 上报事件
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        # 处理事件
        角色列表 = [
            {"页面": page_h5_居民, "表单数据": 表单数据_物管, "角色名称": "物业管理员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_h5_二级网格员, "表单数据": 表单数据_二级, "角色名称": "二级网格员"},
        ]
        for 角色 in 角色列表:
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])


class TestProcess居民到一级(BaseCase):
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_三级, 表单数据_二级, 表单数据_一级",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给社区，三级向二级申请协助，二级向一级申请协助，一级办结",
                 "上报图片路径": ""
             },
             {
                 "处理方式": "申请协助(上级)",
                 "指定处理人": "陶**",
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "申请协助(上级)",
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
    @pytest.mark.usefixtures("page_h5_二级网格员")
    @pytest.mark.usefixtures("page_h5_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给社区，三级向二级申请协助，二级向一级申请协助，一级办结")
    def test_process_路径1(self, page_h5_居民, page_h5_三级网格员, page_h5_二级网格员,
                           表单数据_居民: dict,
                           表单数据_三级: dict, 表单数据_二级: dict, 表单数据_一级: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民)

        角色列表 = [
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_h5_二级网格员, "表单数据": 表单数据_二级, "角色名称": "二级网格员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_一级, "角色名称": "一级网格员"},

        ]

        for 角色 in 角色列表:
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])

    # TODO: 转交网格员后，三级收不到，二级能收到，等待开发那边修改
    @pytest.mark.parametrize(
        "表单数据_居民, 表单数据_物管, 表单数据_物工, 表单数据_三级, 表单数据_二级, 表单数据_一级",

        [
            ({
                 "上报类型": "建议",
                 "上报描述": "居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级转交给一级，一级网格员办结",
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
                 "处理意见": "同意",
                 "图片": r"C:\Users\Administrator\Pictures\111.png"
             },
             {
                 "处理方式": "申请协助(上级)",
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
    @pytest.mark.usefixtures("page_h5_二级网格员")
    @pytest.mark.usefixtures("page_h5_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给物业，物管下发给物工，物工转交给三级，三级转交给二级，二级转交给一级，一级网格员办结")
    def test_process_路径2(self, page_h5_居民, page_h5_三级网格员,
                           page_h5_二级网格员,
                           表单数据_居民: dict, 表单数据_物管: dict, 表单数据_物工: dict, 表单数据_三级: dict,
                           表单数据_二级: dict, 表单数据_一级: dict):
        # 上报事件
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民)

        # 处理事件
        角色列表 = [
            {"页面": page_h5_居民, "表单数据": 表单数据_物管, "角色名称": "物业管理员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_物工, "角色名称": "物业工作人员"},
            {"页面": page_h5_三级网格员, "表单数据": 表单数据_三级, "角色名称": "三级网格员"},
            {"页面": page_h5_二级网格员, "表单数据": 表单数据_二级, "角色名称": "二级网格员"},
            {"页面": page_h5_居民, "表单数据": 表单数据_一级, "角色名称": "一级网格员"},
        ]
        for 角色 in 角色列表:
            处理事件(角色["页面"], 角色["表单数据"], 角色["角色名称"])
