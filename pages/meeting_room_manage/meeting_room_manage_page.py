from base_case import BaseCase
from pages.meeting_room_manage.meeting_room_info_page import MeetingRoomInfoPage
from pages.base_query_page import BaseQueryPage

"""会议室管理页面类"""
class MeetingRoomManagePageBase(BaseQueryPage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    # 从数据库中查询会议室表中的数据条数
    def excute_query_count(self, connection):
        sql = """select count(*) as count from meeting_room where del_flag = 0;"""
        db_data = self.get_db_data(connection, sql)
        return db_data[0]["count"]

    def get_add_button(self):
        # 新建按钮
        return self.page.get_by_role("button", name="新建")

    def click_add_button(self):
        # 点击新建按钮
        self.get_add_button().click()
        # 返回会议室信息页面
        return MeetingRoomInfoPage(self.page)

    def get_room_input(self):
        # 输入框-会议室
        return self.page.locator("//input[@placeholder='会议室编号/名称']")

    def input_room(self, room):
        # 向输入框输入会议室编号/名称
        if room is None:
            return
        self.get_room_input().fill(room)

    def get_capacity_input(self):
        # 输入框-容纳人数
        return self.page.locator("//input[@placeholder='最少容纳人数']")

    def input_capacity(self, capacity):
        # 向输入框输入容纳人数
        if capacity is None:
            return
        self.get_capacity_input().fill(capacity)

    def get_device_input(self):
        # 输入框-设备
        return self.page.locator("(//input[@placeholder='请选择'])[1]")

    def get_device_span(self, device):
        # 设备选项
        return self.page.locator(f"//span[text()='{device}']")

    def get_device_close_button(self):
        # 设备输入框点击后出现的叉号按钮
        return self.page.locator("(//input[@placeholder='请选择'])[1]/following-sibling::span/span/i[@class='el-select__caret el-input__icon el-icon-circle-close']")
    def choose_device(self, device):
        # 选择设备
        if device is None:
            return
        if device == "":
            # 清空选择框内容
            self.get_device_input().click()
            if self.get_device_close_button().is_visible():
                # 点击叉号按钮
                self.get_device_close_button().click()
            # 清空选择框
            # self.get_device_input().evaluate("element => element.value = ''")
            return
        # 点击输入框
        self.get_device_input().click()
        # 点击设备选项
        self.get_device_span(device).click()

    def get_status_input(self):
        # 输入框-状态
        return self.page.locator("(//input[@placeholder='请选择'])[2]")

    def get_status_span(self, status):
        # 状态选项
        # return self.page.get_by_role("menuitem", name=f"{status}")
        return self.page.locator(f"//li[contains(@class, 'el-select-dropdown__item')]/span[text()='{status}']")

    def get_status_close_button(self):
        # 点击状态输入框出现的叉号按钮
        return self.page.locator("(//input[@placeholder='请选择'])[2]/following-sibling::span/span/i[@class='el-select__caret el-input__icon el-icon-circle-close']")
    def choose_status(self, status):
        # 选择状态
        if status is None:
            return
        if status == "":
            # 此处似乎不能直接清空，直接清空后下次选状态会选不上。采用了替代方案
            # 点击输入框
            self.get_status_input().click()
            # 若状态选择框中已经有内容，那么叉号图标必然可见，点击它，清空内容
            if self.get_status_close_button().is_visible():
                self.get_status_close_button().click()
            # self.get_status_input().evaluate("element => element.value=''")
            return
        # 点击选择框
        self.get_status_input().click()
        self.get_status_span(status).wait_for(state='visible')
        # 选中选项
        self.get_status_span(status).click()
        # 鼠标点击空白处，关闭选择框
        self.page.mouse.click(x=10, y=10)

    def get_location_input(self):
        # 输入框-位置
        return self.page.locator("//input[@placeholder='会议室所在位置']")

    def input_location(self, location):
        if location is None:
            return
        # 输入内容
        self.get_location_input().fill(location)

    def get_approval_input(self):
        # 输入框-审批人
        return self.page.locator("(//input[@placeholder='请选择'])[3]")

    def get_approval_span(self, approval):
        # 审批人选项
        return self.page.locator(f"//span[text()='{approval}']")

    def choose_approval(self, approval):
        if approval is None:
            return
        if approval == "":
            # 清空选择框内容
            self.get_approval_input().evaluate("element => element.value = ''")
            return
        # 点击输入框
        self.get_approval_input().click()
        # 选择审批人
        self.get_approval_span(approval).click()

    def get_department_input(self):
        # 输入框-部门
        return self.page.locator("(//input[@placeholder='请选择'])[4]")

    def get_department_label(self, department):
        # 部门选项前面的勾选按钮
        return self.page.locator(f"//span[text()='{department}']/preceding-sibling::label")

    def get_department_close_button(self):
        # 部门输入框点击后出现的叉号按钮
        return self.page.locator("(//input[@placeholder='请选择'])[4]/following-sibling::span/span/i[@class='el-input__icon el-icon-circle-close']")
    def choose_department(self, departments):
        if departments is None:
            return
        if departments == "":
            # 点击输入框
            self.get_department_input().click()
            if self.get_department_close_button().is_visible():
                # 点击叉号按钮
                self.get_department_close_button().click()
            self.page.mouse.click(x=10, y=10)
            # self.get_department_input().evaluate("element => element.value = ''")
            return
        # 点击输入框
        self.get_department_input().click()
        # 点击选项
        for department in departments:
            self.get_department_label(department).click()
        self.page.mouse.click(x=10, y=10)

    def get_manager_input(self):
        # 输入框-管理员
        return self.page.locator("//input[@placeholder='请输入姓名']")

    def input_manager(self, manager):
        # 输入管理员
        if manager is None:
            return
        self.get_manager_input().fill(manager)

    def get_edit_button(self):
        # return self.page.get_by_role("button", name="编辑")
        # return self.page.locator("(//span[text()='编辑 '])[1]/..")
        # 页面中的第一个编辑按钮
        return self.page.locator("//span[text()='编辑 ']").first

    def click_edit_button(self):
        # if self.get_edit_button().is_visible():
        #     print("-------------------------------------------------------")
        #     self.get_edit_button().click()
        # self.get_edit_button().click()
        # 这个元素直接点击无效，必须使用evaluate函数执行js代码来点击
        self.get_edit_button().evaluate("(element) => element.click()")
        return MeetingRoomInfoPage(self.page)

    def get_query_button(self):
        # 查询按钮
        return self.page.locator("//span[text()=' 查询']")

    def click_query_button(self):
        # 点击查询按钮
        self.get_query_button().click()

    def get_next_button(self):
        # 下一页按钮
        return self.page.locator("//button[@class='btn-next']")

    def click_next_button(self):
        # 点击下一页按钮
        self.get_next_button().click()

    def get_delete_button(self):
        # 页面中的第一个删除按钮
        return self.page.locator("//span[text()='删除 ']").first

    def click_delete_button(self):
        # 点击删除按钮
        self.get_delete_button().evaluate("(element) => element.click()")
        # 点击确定按钮
        self.page.get_by_role("button", name="确定").click()

    def click_delete_button_cancel(self):
        # 点击删除按钮
        self.get_delete_button().evaluate("(element) => element.click()")
        # 点击取消按钮
        self.page.get_by_role("button", name="取消").click()

    def verify_delete_success_message(self):
        # 等待“删除成功”消息出现
        self.page.get_by_role("alert").get_by_text("删除成功").wait_for()
        # 断言删除成功消息可见
        assert self.page.get_by_role("alert").get_by_text("删除成功").is_visible()

    def verify_delete_cancel_message(self, count_pre, count_after):
        # 等待“删除成功”消息消失
        delete_success_message = self.page.get_by_role("alert").get_by_text("删除成功")
        delete_success_message.wait_for(state='hidden', timeout=7000)
        # 断言删除成功消息不可见,且删除前的数量和删除后的数量相同
        assert not self.page.get_by_role("alert").get_by_text("删除成功").is_visible() and count_pre == count_after

    def get_table_rows(self):
        # 表格中的所有行
        return self.page.locator("(//table[@class='el-table__body'])[1]/tbody/tr")

    def get_first_page_button(self):
        # 首页按钮
        return self.page.locator('//li[text()=1]')

    def get_table_rows(self):
        # 表格中的所有行
        return self.page.locator('(//table[@class="el-table__body"])[1]/tbody/tr')

    def get_reset_btn(self):
        # 重置按钮
        return self.page.locator("//span[text()=' 重置']")

    def click_reset_btn(self):
        # 点击重置按钮
        self.get_reset_btn().click()

