import allure
import pytest
from playwright.sync_api import expect

from base_case import BaseCase
from pages.pages_h5.上报物业 import PageReportProperty
from pages.pages_h5.首页 import PageHome
from pages.网格管理.事件管理 import PageIncidentManage
from tests.test_网格管理.test_事件管理.test_事件管理 import 事件管理页面

"""
    可以按照事件传递的方向来划分流程：（1）从下级到上级  （2）从上级到下级
    事件的5种处理方式：（1）跟进。级别不变
                    （2）转交（同级）。级别不变
                     （3）办结。结束
                       （4）下发。级别向下
                         （5）转交网格员。级别向上
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

            # ({
            #      "上报类型": "建议",
            #      "上报描述": "居民上报，物管转交给同级",
            #      "上报图片路径": ""
            #  },
            #  {
            #      "处理方式": "转交(同级)",
            #      "指定处理人": "石**",
            #      "处理意见": "同意",
            #      "图片": r"C:\Users\Administrator\Pictures\111.png"
            #  }
            # ),
            # 添加更多测试数据集
        ],
    )
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_h5_居民")
    # @allure.step("以居民为起点，物管为终点的事件处理流程")
    def test_process_路径1(self, page_h5_居民, page_pc_物业管理员1, 表单数据_居民: dict, 表单数据_物管: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民.get("上报类型"), 表单数据_居民.get("上报描述"),
                                   表单数据_居民.get("上报图片路径"))
        # 刷新一下页面，让列表更新
        page_pc_物业管理员1.reload()
        事件管理页面_物业管理员 = PageIncidentManage(page_pc_物业管理员1)
        事件管理页面_物业管理员.处理最新事件(表单数据_物管)
        # 处理成功后，出现成功字样，表格第一行的处理按钮消失
        expect(事件管理页面_物业管理员.page.get_by_text("处理成功")).to_be_visible()
        expect(事件管理页面_物业管理员.get_table_rows().first.locator("button", has_text="处理")).not_to_be_visible(
            timeout=3000)
        事件管理页面_物业管理员.点击表格中某行按钮(行号=1, 按钮名="查看")
        处理方式 = "转交" if 表单数据_物管.get("处理方式") == "转交(同级)" else 表单数据_物管.get("处理方式")
        assert 事件管理页面_物业管理员.处理记录节点_最新.text_content().strip() == "物业管理人员" + 处理方式
        # 点击空白位置，关闭抽屉
        page_pc_物业管理员1.mouse.click(x=10, y=10)
        # 事业管理页面_物业管理员.page.wait_for_timeout(10000000)

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
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民.get("上报类型"), 表单数据_居民.get("上报描述"),
                                   表单数据_居民.get("上报图片路径"))
        # 刷新一下页面，让列表更新
        page_pc_物业管理员1.reload()
        事件管理页面_物业管理员 = PageIncidentManage(page_pc_物业管理员1)
        事件管理页面_物业管理员.处理最新事件(表单数据_物管_跟进)
        # 处理成功后，出现成功字样
        expect(事件管理页面_物业管理员.page.get_by_text("处理成功")).to_be_visible()
        事件管理页面_物业管理员.点击表格中某行按钮(行号=1, 按钮名="查看")
        处理方式 = "转交" if 表单数据_物管_跟进.get("处理方式") == "转交(同级)" else 表单数据_物管_跟进.get("处理方式")
        assert 事件管理页面_物业管理员.处理记录节点_最新.text_content().strip() == "物业管理人员" + 处理方式
        # 点击空白位置，关闭抽屉
        page_pc_物业管理员1.mouse.click(x=10, y=10)

        事件管理页面_物业管理员.处理最新事件(表单数据_物管_办结)
        # 处理成功后，出现成功字样，表格第一行的处理按钮消失
        expect(事件管理页面_物业管理员.page.get_by_text("处理成功")).to_be_visible()
        expect(事件管理页面_物业管理员.get_table_rows().first.locator("button", has_text="处理")).not_to_be_visible(
            timeout=3000)
        事件管理页面_物业管理员.点击表格中某行按钮(行号=1, 按钮名="查看")
        处理方式 = "转交" if 表单数据_物管_办结.get("处理方式") == "转交(同级)" else 表单数据_物管_办结.get("处理方式")
        assert 事件管理页面_物业管理员.处理记录节点_最新.text_content().strip() == "物业管理人员" + 处理方式
        # 点击空白位置，关闭抽屉
        page_pc_物业管理员1.mouse.click(x=10, y=10)
        # 事件管理页面_物业管理员.page.wait_for_timeout(10000000)

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
    @pytest.mark.usefixtures("page_pc_物业管理员2")
    @pytest.mark.usefixtures("page_pc_物业管理员1")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报，物管1转交给同级，物管2办结")
    def test_process_路径3(self, page_h5_居民, page_pc_物业管理员1, page_pc_物业管理员2, 表单数据_居民: dict, 表单数据_物管_转交: dict,
                           表单数据_物管_办结: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民.get("上报类型"), 表单数据_居民.get("上报描述"),
                                   表单数据_居民.get("上报图片路径"))
        # 刷新一下页面，让列表更新
        page_pc_物业管理员1.reload()
        事件管理页面_物业管理员1 = PageIncidentManage(page_pc_物业管理员1)
        事件管理页面_物业管理员1.处理最新事件(表单数据_物管_转交)
        # 处理成功后，出现成功字样
        expect(事件管理页面_物业管理员1.page.get_by_text("处理成功")).to_be_visible()
        expect(事件管理页面_物业管理员1.get_table_rows().first.locator("button", has_text="处理")).not_to_be_visible(
            timeout=3000)
        事件管理页面_物业管理员1.点击表格中某行按钮(行号=1, 按钮名="查看")
        处理方式 = "转交" if 表单数据_物管_转交.get("处理方式") == "转交(同级)" else 表单数据_物管_转交.get("处理方式")
        assert 事件管理页面_物业管理员1.处理记录节点_最新.text_content().strip() == "物业管理人员" + 处理方式
        # 点击空白位置，关闭抽屉
        page_pc_物业管理员1.mouse.click(x=10, y=10)

        page_pc_物业管理员2.reload()
        事件管理页面_物业管理员2 = PageIncidentManage(page_pc_物业管理员2)
        事件管理页面_物业管理员2.处理最新事件(表单数据_物管_办结)
        # 处理成功后，出现成功字样，表格第一行的处理按钮消失
        expect(事件管理页面_物业管理员2.page.get_by_text("处理成功")).to_be_visible()
        expect(事件管理页面_物业管理员2.get_table_rows().first.locator("button", has_text="处理")).not_to_be_visible(
            timeout=3000)
        事件管理页面_物业管理员2.点击表格中某行按钮(行号=1, 按钮名="查看")
        处理方式 = "转交" if 表单数据_物管_办结.get("处理方式") == "转交(同级)" else 表单数据_物管_办结.get("处理方式")
        assert 事件管理页面_物业管理员2.处理记录节点_最新.text_content().strip() == "物业管理人员" + 处理方式
        # 点击空白位置，关闭抽屉
        page_pc_物业管理员1.mouse.click(x=10, y=10)
        # 事件管理页面_物业管理员2.page.wait_for_timeout(10000000)


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
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报物业()
        上报物业页面_居民 = PageReportProperty(page_h5_居民)
        上报物业页面_居民.上报事件(表单数据_居民.get("上报类型"), 表单数据_居民.get("上报描述"),
                                   表单数据_居民.get("上报图片路径"))
        # 刷新一下页面，让列表更新
        page_pc_物业管理员1.reload()
        事件管理页面_物业管理员 = PageIncidentManage(page_pc_物业管理员1)
        事件管理页面_物业管理员.处理最新事件(表单数据_物管)
        # 处理成功后，出现成功字样，表格第一行的处理按钮消失
        expect(事件管理页面_物业管理员.page.get_by_text("处理成功")).to_be_visible()
        expect(事件管理页面_物业管理员.get_table_rows().first.locator("button", has_text="处理")).not_to_be_visible(
            timeout=3000)
        事件管理页面_物业管理员.点击表格中某行按钮(行号=1, 按钮名="查看")
        处理方式 = "转交" if 表单数据_物管.get("处理方式") == "转交(同级)" else 表单数据_物管.get("处理方式")
        assert 事件管理页面_物业管理员.处理记录节点_最新.text_content().strip() == "物业管理人员" + 处理方式
        # 点击空白位置，关闭抽屉
        page_pc_物业管理员1.mouse.click(x=10, y=10)

        # 刷新一下页面，让列表更新
        page_pc_物业工作人员.reload()
        事件管理页面_物业工作人员 = PageIncidentManage(page_pc_物业工作人员)
        事件管理页面_物业工作人员.处理最新事件(表单数据_物工)
        expect(事件管理页面_物业工作人员.page.get_by_text("处理成功")).to_be_visible()
        expect(事件管理页面_物业工作人员.get_table_rows().first.locator("button", has_text="处理")).not_to_be_visible(
            timeout=3000)
        事件管理页面_物业工作人员.点击表格中某行按钮(行号=1, 按钮名="查看")
        处理方式 = "转交" if 表单数据_物工.get("处理方式") == "转交(同级)" else 表单数据_物工.get("处理方式")
        assert 事件管理页面_物业工作人员.处理记录节点_最新.text_content().strip() == "物业工作人员" + 处理方式
        # 点击空白位置，关闭抽屉
        page_pc_物业工作人员.mouse.click(x=10, y=10)

        # 事件管理页面_物业工作人员.page.wait_for_timeout(10000000)

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
    @pytest.mark.usefixtures("page_pc_三级网格员")
    @pytest.mark.usefixtures("page_h5_居民")
    @allure.step("居民上报给社区，三级网格员办结")
    def test_process_路径1(self, page_h5_居民, page_pc_三级网格员, 表单数据_居民: dict,
                           表单数据_三级: dict):
        首页 = PageHome(page_h5_居民)
        # 跳转到上报物业，进行一次上报
        首页.跳转到上报社区()
        上报社区页面_居民 = PageReportProperty(page_h5_居民)
        上报社区页面_居民.上报事件(表单数据_居民.get("上报类型"), 表单数据_居民.get("上报描述"),
                                   表单数据_居民.get("上报图片路径"))

        # 刷新一下页面，让列表更新
        page_pc_三级网格员.reload()
        事件管理页面_三级网格员 = PageIncidentManage(page_pc_三级网格员)
        事件管理页面_三级网格员.处理最新事件(表单数据_三级)
        expect(事件管理页面_三级网格员.page.get_by_text("处理成功")).to_be_visible()
        expect(事件管理页面_三级网格员.get_table_rows().first.locator("button", has_text="处理")).not_to_be_visible(
            timeout=3000)
        事件管理页面_三级网格员.点击表格中某行按钮(行号=1, 按钮名="查看")
        处理方式 = "转交" if 表单数据_三级.get("处理方式") == "转交(同级)" else 表单数据_三级.get("处理方式")
        assert 事件管理页面_三级网格员.处理记录节点_最新.text_content().strip() == "三级网格员" + 处理方式
        # 点击空白位置，关闭抽屉
        page_pc_三级网格员.mouse.click(x=10, y=10)

        # 事件管理页面_三级网格员.page.wait_for_timeout(10000000)
