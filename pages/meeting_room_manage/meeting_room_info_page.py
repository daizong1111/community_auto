from playwright.sync_api import expect

"""新增或修改会议室时填写的表单页面类"""
class MeetingRoomInfoPage:
    def __init__(self, page):
        self.page = page

    # 某些选择框右侧的叉号按钮，用来清空内容
    def get_close_btn(self):
        return self.page.locator("//i[contains(@class, 'el-input__icon') and contains(@class, 'el-icon-circle-close') and not(contains(@class,'el-input__validateIcon'))]")

    # 点击新建按钮
    def click_add_meeting_room_button(self):
        self.page.get_by_role("button", name="新建").click()

    # 获取会议室名称输入框的内容
    def get_room_name(self):
        return self.page.get_by_placeholder('不超过10个字').input_value()

    # 填写输入框-会议室名称
    def fill_room_name(self, room_name):
        if room_name is None:
            return
        self.page.get_by_placeholder('不超过10个字').fill(room_name)

    # 通过键盘输入的方式填写输入框-会议室名称
    def fill_room_name_by_press(self, room_name):
        if room_name is None:
            return
        locator = self.page.get_by_placeholder('不超过10个字')
        # 点击输入框
        locator.click()
        # 清空内容
        locator.clear()
        # 逐字符输入内容
        locator.press_sequentially(str(room_name), delay=10)

    # 获取会议室编号输入框的内容
    def get_room_code(self):
        return self.page.get_by_placeholder("请输入,如HYS10-506").input_value()

    # 填写输入框-会议室编号
    def fill_room_code(self, room_code):
        if room_code is None:
            return

        self.page.get_by_placeholder("请输入,如HYS10-506").fill(room_code)

    # 通过键盘输入的方式填写输入框-会议室编号
    def fill_room_code_by_press(self, room_code):
        if room_code is None:
            return

        locator = self.page.get_by_placeholder("请输入,如HYS10-506")
        locator.click()
        locator.clear()
        locator.press_sequentially(str(room_code), delay=10)

    # 填写输入框-容纳人数
    def fill_capacity(self, capacity):
        if capacity is None:
            return

        self.page.get_by_role("spinbutton").first.fill(capacity)

    # 通过键盘输入的方式填写输入框-容纳人数
    def fill_capacity_by_press(self, capacity):
        if capacity is None:
            return

        locator = self.page.get_by_role("spinbutton").first
        locator.click()
        locator.clear()
        locator.press_sequentially(str(capacity), delay=10)

    # 输入框-容纳人数
    def get_capacity(self):
        return self.page.get_by_role("spinbutton").first.input_value()

    # 填写位置输入框
    def fill_location(self, location):
        if location is None:
            return

        self.page.get_by_placeholder("不超过30个字").first.fill(location)

    # 通过键盘输入的方式填写输入框-位置
    def fill_location_by_press(self, location):
        if location is None:
            return

        locator = self.page.get_by_placeholder("不超过30个字").first
        locator.click()
        locator.clear()
        locator.press_sequentially(str(location), delay=10)

    # 输入框-位置
    def get_location(self):
        return self.page.get_by_placeholder("不超过30个字").first.input_value()

    # 选择会议室状态
    def select_room_status(self, status):
        if status is None:
            return
        if status == "":
            # 清空该选择框的内容
            if self.page.get_by_placeholder("请选择").first.input_value() != "":
                # 点击选择框
                self.page.get_by_placeholder("请选择").first.click()
                # 点击叉号
                self.get_close_btn().click()
            # self.page.get_by_placeholder("请选择").first.evaluate("element => element.value = ''")
            return
        # 点击选择框
        self.page.get_by_placeholder("请选择").first.click()
        # 根据文本定位列表中的选项
        room_status_li = self.page.locator("li").filter(has_text=status)
        # 等待选项可见
        room_status_li.wait_for(state="visible")
        # 点击选项
        room_status_li.click()

    # 选择设备
    def select_devices(self, devices):
        if devices is None:
            return  # 如果devices为空，直接返回
        if devices == "":
            # 遍历所有被选中选项，点击它们，取消勾选
            choose_devices_item = self.page.locator("(//div[@class='el-form-item__content'])[6]/div/span[contains(@class,'equipment_checked')]").all()
            # 列表的长度会发生变化，每次点击列表头部的元素
            for i in range(len(choose_devices_item)):
                choose_devices_item[0].evaluate("(element) => element.click()")
            return
        if not isinstance(devices, (list, tuple, set)):
            # 若devices不是可迭代对象，则抛出异常
            raise TypeError("devices必须是一个可迭代对象（如列表、元组或集合）")
        for device in devices:
            # 遍历列表中的元素，若该元素已被选中，则跳过，否则，点击它
            # 若该元素未被选中，则点击它
            device_span = self.page.locator(f"(//div[@class='el-form-item__content'])[6]/div/span[contains(text(),'{device}')]")
            class_attribute = device_span.get_attribute("class")
            # 若该元素的class中包含equipment_unchecked，则点击它
            if class_attribute is not None and "equipment_unchecked" in class_attribute:
                device_span.click()
            # self.page.get_by_text(device).click()

    # 选择部门
    def select_departments(self, departments):
        if departments is None:
            return  # 如果为空，直接返回
        if departments == "":
            # 清空该选择框的内容
            # self.page.get_by_placeholder("请选择").nth(1).evaluate("element => element.value = ''")
            if self.page.get_by_placeholder("请选择").nth(1).input_value() != "":
                self.page.get_by_placeholder("请选择").nth(1).click()
                self.get_close_btn().click()
            return
        # 点击选择框
        self.page.get_by_placeholder("请选择").nth(1).click()
        if not isinstance(departments, (list, tuple, set)):
            raise TypeError("departments必须是一个可迭代对象（如列表、元组或集合）")
        # 遍历列表中的元素
        for department in departments:
            # 根据文本定位列表中的选项
            org_item = self.page.get_by_role("menuitem", name=department).get_by_role("radio")
            # 点击选项
            org_item.click()
        self.page.mouse.click(x=10, y=10)  # 点击空白处

    """选择完管理部门后，再选择管理员时，默认只能选择该部门下的人员"""
    def select_manager(self, manager):
        if manager is None:
            return
        if manager == "":
            # 清空该选择框的内容
            self.page.get_by_placeholder("请选择").nth(2).evaluate("element => element.value = ''")
            return
        # 点击选择框
        self.page.get_by_placeholder("请选择").nth(2).click()
        # 根据文本定位列表中的选项
        manager_item = self.page.get_by_role("menuitem", name=manager)
        # 点击选项
        manager_item.click()
        self.page.mouse.click(x=10, y=10)  # 点击空白处

    def fill_description(self, description):
        # 填写描述输入框
        if description is None:
            return
        self.page.get_by_role("textbox", name="请输入", exact=True).fill(description)

    # 通过键盘输入的方式填写输入框-描述
    def fill_description_by_press(self, description):
        if description is None:
            return

        locator = self.page.get_by_role("textbox", name="请输入", exact=True)
        locator.click()
        locator.clear()
        locator.press_sequentially(str(description), delay=10)

    # 获取输入框-描述的内容
    def get_description(self):
        return self.page.get_by_role("textbox", name="请输入", exact=True).input_value()


    # 选择完管理部门后，再选择审批人时，默认只能选择该部门下的人员
    def toggle_approval(self, need_approval_switch, approval_person):
        # 审批开关
        approval_switch = self.page.locator("(//div[@role='switch'])[1]")
        # 调试信息：打印 aria-checked 和 approval_person 的值
        # 开关的开启关闭状态的切换，通过aria-checked属性判断
        aria_checked = approval_switch.get_attribute("aria-checked")
        print(f"aria-checked: {aria_checked}, approval_person: {approval_person}")
        if need_approval_switch is True:
            # 若需要审批，则打开开关
            # 若开关为关闭状态，则点击开关
            if aria_checked is None:
                approval_switch.click()
        if need_approval_switch is False:
            # 若不需要审批，则关闭开关
            # 若开关为打开状态，则点击开关
            if aria_checked == "true":
                approval_switch.click()
        # 若开关为打开状态，则上面这个元素必定拥有aria-checked属性，若该元素没有该属性，get_attribute会返回None
        if approval_switch.get_attribute("aria-checked") == "true" and approval_person is not None:
            if approval_person == "":
                # 清空该选择框的内容
                self.page.get_by_placeholder("请选择").nth(3).evaluate("element => element.value = ''")
                return
            # 点击选择框
            self.page.get_by_placeholder("请选择").nth(3).click()
            # 等待菜单出现
            # self.page.locator('//div[@class="form_area"]').get_by_role("menuitem", name=approval_person).wait_for(state="visible")
            if isinstance(approval_person, str):
                # 若approval_person是字符串，则从列表项中找出匹配该字符串的选项，并点击它
                self.page.get_by_role("menuitem", name=approval_person).last.click()
                # approval_item = self.page.locator(f"//span[text()='{approval_person}']").nth(1)
                # 这处定位表达式要改。如果上面的那个张超未选中的话，这里的下标就和之前正常时候不一样了
                # approval_item = self.page.nth(1)
                # approval_item.click()
                # approval_items = self.page.get_by_role("menuitem", name=approval_person).all()
                # for approval_item in approval_items:
                #     # 若元素可见，才点击。一定要加is_enabled，否则可能会报错，加enabled可以过滤掉屏幕中不可见的
                #     if approval_item.is_visible() and approval_item.is_enabled():
                #         approval_item.wait_for(state="visible")
                #         # 可能会定位到被隐藏的元素，强制点击
                #         approval_item.click(force=True)
            # # 点击空白处
            self.page.mouse.click(x=10, y=10)

    def toggle_time_limit(self, need_time_switch, days, start_time, end_time, max_duration):
        # 时间限制开关
        time_limit_switch = self.page.locator("(//div[@role='switch'])[2]")
        # 开关的开启关闭状态的切换，通过aria-checked属性判断
        time_switch_status = time_limit_switch.get_attribute("aria-checked")
        if need_time_switch is True:
            # 若需要时间限制，则打开开关
            # 若开关为关闭状态，点击开关
            if time_switch_status is None:
                time_limit_switch.click()
        if need_time_switch is False:
            # 若不需要时间限制，则关闭开关
            # 若开关为打开状态，点击开关
            if time_switch_status == "true":
                time_limit_switch.click()
        # 若时间限制开关为打开状态
        if time_limit_switch.get_attribute("aria-checked") == "true":
            if days is not None:
                # 选择框-可预约的时间范围
                element = self.page.locator('(//div[@class="el-select el-select--medium"])[2]')
                # 删除所有已选中选项
                # 所有的已选中选项右侧的删除按钮
                i_days = self.page.locator('//div[@class="el-select__tags"]/span/span/i')
                len_i = i_days.count()
                for i in range(len_i):
                    # 循环若干次，每次只删除最前面的选项
                    i_days.first.click()
                # # 先清空所有的选项
                # sub_element = self.page.locator('//div[@class="el-select__tags"]/span')
                # # 删除sub_element子元素中的所有span元素
                # sub_element.evaluate(
                #     "element => Array.from(element.querySelectorAll('span')).forEach(span => span.remove())")
                # days_li = self.page.locator('(//ul[@class="el-scrollbar__view el-select-dropdown__list"])[2]/li').all()
                # for li in days_li:
                #     # 删除li的class属性中的selected字段
                #     li.evaluate("element => element.classList.remove('selected')")
                if days != "":
                    # 若days不为空，则添加选项
                    # 点击选择框
                    element.click()
                    # 将所有的日期选中
                    for day in days:
                        self.page.locator(
                            '(//ul[@class="el-scrollbar__view el-select-dropdown__list"])[2]').get_by_text(day).click()
                    self.page.mouse.click(x=10, y=10)  # 点击空白处

            if start_time is not None:
                if start_time == "":
                    # 清空该选择框的内容
                    self.page.get_by_placeholder("开始时间").evaluate("element => element.value = ''")
                else:
                    # 点击该选择框
                    self.page.get_by_placeholder("开始时间").click()
                    # 从参数中分隔出小时和分钟
                    start_hour, start_minute = start_time.split(":")
                    # 该小时选项
                    start_hour_locator = self.page.locator(
                        "(//ul[@class='el-scrollbar__view el-time-spinner__list'])[1]/li").filter(has_text=start_hour)
                    # 滚动到该小时选项
                    start_hour_locator.scroll_into_view_if_needed()
                    # 点击该小时选项
                    start_hour_locator.click()
                    # 该分钟选项
                    start_minute_locator = self.page.locator(
                        "(//ul[@class='el-scrollbar__view el-time-spinner__list'])[2]/li").filter(has_text=start_minute)
                    # 滚动到该分钟选项
                    start_minute_locator.scroll_into_view_if_needed()
                    # 点击
                    start_minute_locator.click()
            if end_time is not None:
                if end_time == "":
                    # 清空该选择框的内容
                    self.page.get_by_placeholder("结束时间").evaluate("element => element.value = ''")
                else:
                    # 点击该选项
                    self.page.get_by_placeholder("结束时间").click()
                    # 分割出小时和分钟
                    end_hour, end_minute = end_time.split(":")
                    # 该小时选项
                    end_hour_locator = self.page.locator(
                        "(//ul[@class='el-scrollbar__view el-time-spinner__list'])[4]/li").filter(has_text=end_hour)
                    # 滚动到该小时选项
                    end_hour_locator.scroll_into_view_if_needed()
                    # 点击
                    end_hour_locator.click()
                    # 分钟选项
                    end_minute_locator = self.page.locator(
                        "(//ul[@class='el-scrollbar__view el-time-spinner__list'])[5]/li").filter(has_text=end_minute)
                    # 滚动到该分钟选项
                    end_minute_locator.scroll_into_view_if_needed()
                    # 点击
                    end_minute_locator.click()
            # 输入单次可预约最长时间
            if max_duration is not None:
                self.page.locator("(//input[@placeholder='请输入'])[3]").fill(max_duration)

    # 通过键盘输入单次可预约最长时间
    def fill_max_duration_by_press(self, max_duration):
        duration_locator = self.page.locator("(//input[@placeholder='请输入'])[3]")
        duration_locator.click()
        duration_locator.clear()
        duration_locator.press_sequentially(str(max_duration), delay=10)

    # 获取单次可预约最长时间输入框中的内容
    def get_max_duration(self):
        return self.page.locator("(//input[@placeholder='请输入'])[3]").input_value()

    # 选择可使用者
    def select_users(self, users):
        if users is None:
            return
        if users == "":
            # 清空该选择框的内容
            self.page.locator(".text_area").evaluate("element => element.innerHTML = ''")
            return
        # 点击该选择框
        self.page.locator(".text_area").click()
        # 获取users列表的长度
        n = len(users)
        # 遍历列表
        for user in users:
            # 若走到最后一个元素，则需要点击该元素前的单选框
            if user == users[n-1]:
                self.page.get_by_label("请选择部门和人员").get_by_text(user).locator("../preceding-sibling::label").click()
            else:
                # 点击该列表项
                self.page.get_by_label("请选择部门和人员").get_by_text(user).click()
        # 点击确定按钮
        self.page.get_by_role("button", name="确 定").click()

    # 填写基本信息
    def fill_basic_info(self, room_name, room_code, capacity, location, status, devices, departments, manager, description):
        self.fill_room_name(room_name)
        self.fill_room_code(room_code)
        self.fill_capacity(capacity)
        self.fill_location(location)
        self.select_room_status(status)
        self.select_devices(devices)
        self.select_departments(departments)
        self.select_manager(manager)
        self.fill_description(description)

    # 填写高级设置信息
    def fill_high_level_info(self, need_approval, approval_person, need_time_limit, days, start_time, end_time, max_duration, users):
        self.toggle_approval(need_approval, approval_person)
        self.toggle_time_limit(need_time_limit, days, start_time, end_time, max_duration)
        self.select_users(users)

    # 点击提交按钮
    def click_submit_button(self):
        self.page.get_by_role("button", name="提交").click()

    # 判断添加成功
    def verify_add_success_message(self, count_pre, count_after): \
        # 断言操作成功字样在页面出现
        self.page.get_by_text("操作成功").wait_for(timeout=5000)
        assert self.page.get_by_text("操作成功").is_visible() and count_after == count_pre + 1

    # 判断修改成功
    def verify_edit_success_message(self, count): \
        # 断言操作成功字样在页面出现
        self.page.get_by_text("操作成功").wait_for(timeout=5000)
        assert self.page.get_by_text("操作成功").is_visible() and count > 0

    # 判断添加失败-必填项不能为空
    def verify_error_add_miss_message(self, count_pre, count_after):
        # 断言*必填项不能为空在页面出现
        self.page.get_by_text("*必填项不能为空").wait_for(timeout=5000)
        assert self.page.get_by_text("*必填项不能为空").is_visible() and count_pre == count_after

    # 判断修改失败-必填项不能为空
    def verify_error_edit_miss_message(self):
        # 断言*必填项不能为空在页面出现
        self.page.get_by_text("*必填项不能为空").wait_for(timeout=5000)
        assert self.page.get_by_text("*必填项不能为空").is_visible()
