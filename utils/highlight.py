def highlight_elements(page, locator_list):
    # 假设 locator_list 是一个包含 locator 对象的列表
    for locator in locator_list:
        count = locator.count()  # 同步获取元素数量
        if count > 0:
            for i in range(count):
                element_handle = locator.nth(i).element_handle()  # 获取第i个元素句柄
                page.evaluate("""
                    (element) => {
                        element.style.border = '2px solid red';
                    }
                """, element_handle)
        else:
            print("元素未找到，无法高亮")
