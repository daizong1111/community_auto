# from datetime import datetime
#
# from playwright.sync_api import expect, BrowserContext, Route, Page
#
# from module.BasePage import 使用new_context登录并返回实例化的page
#
#
# def test_登录_输入正确用户名(new_context):
#     context: BrowserContext = new_context()
#     page = context.new_page()
#     page.goto("https://www.baidu.com/")
#     loc = page.locator("#kw").first
#     loc.fill("我是大宝宝")
#     expect(loc).to_have_value("我是大宝宝")
#
#
# from playwright.sync_api import sync_playwright, expect
#
#
# def test_run(new_context):
#     # browser = playwright.chromium.launch()
#     context: BrowserContext = new_context()
#     page = context.new_page()
#     page.set_content("""
#         <select id="fruits" multiple>
#             <option value="apple">Apple</option>
#             <option value="banana" selected>Banana</option>
#             <option value="cherry" selected>Cherry</option>
#             <option value="date">Date</option>
#         </select>
#     """)
#
#     # 断言多选下拉框选中的值
#     fruits_select = page.locator("#fruits")
#     # 默认选中了 Banana 和 Cherry
#     expect(fruits_select).to_have_values(["banana", "cherry"])
#
#     # 模拟用户选择更多选项
#     fruits_select.select_option(["apple", "date"])
#
#     # 再次断言，现在应该四个都被选中
#     expect(fruits_select).to_have_values(["apple", "banana", "cherry", "date"])
#
#     context.close()
#
#     import datetime
#     from playwright.sync_api import expect, sync_playwright
#
#
# # def test_countdown(new_context):
# #     context: BrowserContext = new_context()
# #     page = context.new_page()
# #     page.set_content("""
# #         <button id="btn">Send Code</button>
# #         <span id="timer"></span>
# #         <script>
# #             const btn = document.getElementById('btn');
# #             const timer = document.getElementById('timer');
# #             let countdown = 60;
# #             btn.onclick = () => {
# #                 btn.disabled = true;
# #                 const interval = setInterval(() => {
# #                     timer.textContent = countdown;
# #                     countdown--;
# #                     if (countdown < 0) {
# #                         clearInterval(interval);
# #                         btn.disabled = false;
# #                         timer.textContent = '';
# #                     }
# #                 }, 1000);
# #             };
# #         </script>
# #     """)
# #     # 1. 安装一个虚拟时钟并立即启动
# #     page.clock.install(datetime.datetime(2024, 1, 1))
# #     page.clock.fast_forward("00:01:00")  # 快进60秒
# #
# #     # 2. 点击按钮
# #     page.locator("#btn").click()
# #
# #     # 3. 验证倒计时结束，按钮重新可用
# #     # 因为时间已经被快进，所以倒计时会瞬间完成
# #     expect(page.locator("#btn")).to_be_enabled()
# #     expect(page.locator("#timer")).to_have_text("")
#
# from playwright.sync_api import sync_playwright, expect
#
#
# def test_dialog_handling():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#
#         # 监听 dialog 事件
#         page.on("dialog", lambda dialog:
#         print(f"Dialog type: {dialog.type}, message: {dialog.message}") or
#         dialog.accept("Hello World")  # 接受对话框并输入文本（如果是prompt）
#                 )
#
#         # 设置页面内容，包含触发对话框的按钮
#         page.set_content("""
#             <button id="alertBtn" onclick="alert('This is an alert!')">Show Alert</button>
#             <button id="confirmBtn" onclick="confirm('Do you agree?')">Show Confirm</button>
#             <button id="promptBtn" onclick="prompt('Enter your name:')">Show Prompt</button>
#             <div id="result"></div>
#             <script>
#                 document.getElementById('confirmBtn').onclick = function() {
#                     const result = confirm('Do you agree?');
#                     document.getElementById('result').textContent = result ? 'Agreed' : 'Declined';
#                 };
#                 document.getElementById('promptBtn').onclick = function() {
#                     const name = prompt('Enter your name:');
#                     if (name) document.getElementById('result').textContent = 'Hello ' + name;
#                 };
#             </script>
#         """)
#
#         # 测试 alert 对话框
#         page.locator("#alertBtn").click()
#
#         # 测试 confirm 对话框
#         page.locator("#confirmBtn").click()
#         expect(page.locator("#result")).to_have_text("Agreed")
#
#         # 测试 prompt 对话框
#         page.locator("#promptBtn").click()
#         expect(page.locator("#result")).to_have_text("Hello Hello World")
#
#         browser.close()
#
#
# # 更精细的对话框控制示例
# def test_advanced_dialog_control():
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#
#         # 自定义对话框处理逻辑
#         def handle_dialog(dialog):
#             print(f"Handling {dialog.type} dialog with message: {dialog.message}")
#             if dialog.type == "alert":
#                 dialog.accept()
#             elif dialog.type == "confirm":
#                 dialog.dismiss()  # 拒绝确认对话框
#             elif dialog.type == "prompt":
#                 dialog.accept("Custom Input")  # 提供自定义输入
#
#         page.on("dialog", handle_dialog)
#
#         page.set_content("""
#             <button onclick="alert('Alert Message')">Alert</button>
#             <button id="confirmBtn" onclick="document.getElementById('result').textContent = confirm('Are you sure?') ? 'Yes' : 'No'">Confirm</button>
#             <button onclick="prompt('Enter something')">Prompt</button>
#             <div id="result"></div>
#         """)
#
#         # 触发各种对话框
#         page.click("button:has-text('Alert')")
#         page.click("#confirmBtn")
#         expect(page.locator("#result")).to_have_text("No")  # 因为我们拒绝了confirm
#
#         page.click("button:has-text('Prompt')")
#
#         browser.close()
#
#
# def test_filter_has(new_context):
#     # browser = playwright.chromium.launch()
#     context: BrowserContext = new_context()
#     page = context.new_page()
#
#     page.set_content(  # 示例HTML
#         """
#         <ul>
#           <button>Add to cart</button>
#           <li>
#             <h3>Product 1</h3>
#             <button>Add to cart</button>
#           </li>
#           <li>
#             <h3>Product 2</h3>
#             <button>Add to cart</button>
#           </li>
#         </ul>
#         """)
#
#     loc = page.locator("li").filter(has=page.locator("button", has_text="Add to cart"))
#     loc.highlight()
#
#
# def test_断言列表中的所有文本(new_context):
#     context: BrowserContext = new_context()
#     page = context.new_page()
#     page.set_content("""
#         <ul>
#           <li>apple</li>
#           <li>banana</li>
#           <li>orange</li>
#         </ul>
#     """)
#     # page.get_by_role("listitem").highlight()
#     page.get_by_role("listitem").count()
#     expect(page.get_by_role("listitem")).to_have_text(["apple", "banana", "orange"])
#
# def test_evaluating_javascript(new_context):
#     my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
#     my_page_测试员.小区信息.navigate()
#     page = my_page_测试员.小区信息.page
#     button1 = page.locator("button", has_text="搜索")
#     button2 = page.locator("button", has_text="新增")
#     button1.highlight()
#     button2.highlight()
#
#
# def test_multiple_handles():
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#
#         page.set_content("""
#             <button id="btn1">Button One</button>
#             <button id="btn2">Button Two</button>
#         """)
#
#         # 方式1：通过选择器创建句柄
#         button1 = page.evaluate_handle('#btn1')
#         button2 = page.evaluate_handle('#btn2')
#
#         # 方式2：将多个句柄作为对象传递
#         result = page.evaluate(
#             """handles => handles.btn1.textContent + ' and ' + handles.btn2.textContent""",
#             {'btn1': button1, 'btn2': button2}
#         )
#         print(result)  # 输出: "Button One and Button Two"
#
#         # 方式3：获取元素属性
#         attributes = page.evaluate(
#             """elements => ({
#                 btn1_id: elements.btn1.id,
#                 btn2_id: elements.btn2.id,
#                 combined_text: elements.btn1.textContent + elements.btn2.textContent
#             })""",
#             {'btn1': button1, 'btn2': button2}
#         )
#         print(attributes)
#
#         browser.close()
#
# def test_链式过滤器(new_context):
#     context = new_context()
#     page = context.new_page()
#
#     page.set_content("""
#         <ul>
#               <li>
#                 <div>John</div>
#                 <div><button>Say hello</button></div>
#               </li>
#               <li>
#                 <div>Mary</div>
#                 <div><button>Say hello</button></div>
#               </li>
#               <li>
#                 <div>John</div>
#                 <div><button>Say goodbye</button></div>
#               </li>
#               <li>
#                 <div>Mary</div>
#                 <div><button>Say goodbye</button></div>
#               </li>
#         </ul>
#     """)
#
#     row_locator = page.get_by_role("listitem")
#     page.get_by_role("button", name="Say hello").highlight()
#     row_locator.filter(has_text="Mary").filter(has=page.get_by_role("button", name="Say hello")).screenshot(path="screenshot.png")
#     # row_locator.filter(has_text="Mary").highlight()
#     # page.locator("li",has_text="Mary").highlight()
#     page.wait_for_timeout(10000)
#
# def test_mock_the_fruit_api(page: Page):
#     def handle(route: Route):
#         json = [{"name": "Strawberry", "id": 21}]
#         # fulfill the route with the mock data
#         route.fulfill(json=json)
#
#     # Intercept the route to the fruit API
#     # page.route("*/**/api/v1/fruits", handle)
#
#     # Go to the page
#     page.goto("https://www.baidu.com/")
#
#     page.wait_for_url("https://www.baidu.com/", timeout=3000)
#
#     # Assert that the Strawberry fruit is visible
#     # expect(page.get_by_text("Strawberry")).to_be_visible()
#     # token = "sdasdasd"
#     # with page.expect_response(lambda response: token in response.url) as response_info:
#     #     page.get_by_text("Update").click()
#     # response = response_info.value
#
#
# def test_capture_api_response_with_token(new_context):
#     """测试捕获包含特定token的API响应"""
#     context: BrowserContext = new_context()
#     page = context.new_page()
#
#     # 设置页面内容，包含一个触发API请求的按钮
#     page.set_content("""
#         <button id="updateBtn">Update</button>
#         <div id="result"></div>
#         <script>
#             document.getElementById('updateBtn').onclick = function() {
#                 // 模拟发送包含用户token的API请求
#                 const token = "abc123xyz";
#                 fetch(`/api/user-data?token=${token}`)
#                     .then(response => response.json())
#                     .then(data => {
#                         document.getElementById('result').textContent = JSON.stringify(data);
#                     });
#             };
#         </script>
#     """)
#
#     # 定义要查找的token
#     token = "abc123xyz"
#
#     # Mock掉fetch请求，使其返回模拟数据
#     page.route("**/api/user-data*", lambda route: route.fulfill(
#         status=200,
#         content_type="application/json",
#         body='{"message": "success"}'
#     ))
#
#     # 使用expect_response捕获包含特定token的响应
#     with page.expect_response(lambda response: token in response.url) as response_info:
#         page.click("#updateBtn")
#
#     # 获取捕获到的响应对象
#     response = response_info.value
#
#     # 验证捕获到的响应
#     assert token in response.url
#     print(f"捕获到的响应URL: {response.url}")
#     print(f"响应状态码: {response.status}")
#
#
# from playwright.sync_api import sync_playwright, expect
#
#
# def pan(locator, deltaX=0, deltaY=0, steps=5):
#     """
#     在指定元素上模拟平移手势。
#     这个函数本身是通用的，不需要修改。
#     """
#     bounds = locator.bounding_box()
#     # 确保元素可见且有边界
#     if not bounds:
#         raise ValueError("Locator has no bounding box. Is it visible?")
#
#     centerX = bounds['x'] + bounds['width'] / 2
#     centerY = bounds['y'] + bounds['height'] / 2
#
#     # 1. 触摸开始
#     touches = [{
#         'identifier': 0,
#         'clientX': centerX,
#         'clientY': centerY,
#     }]
#     locator.dispatch_event('touchstart', {
#         'touches': touches,
#         'changedTouches': touches,
#         'targetTouches': touches
#     })
#
#     # 2. 触摸移动
#     for i in range(1, steps + 1):
#         # 计算每一步移动的位置
#         currentX = centerX + deltaX * i / steps
#         currentY = centerY + deltaY * i / steps
#         touches = [{
#             'identifier': 0,
#             'clientX': currentX,
#             'clientY': currentY,
#         }]
#         locator.dispatch_event('touchmove', {
#             'touches': touches,
#             'changedTouches': touches,
#             'targetTouches': touches
#         })
#
#     # 3. 触摸结束
#     locator.dispatch_event('touchend')
#
#
# # def test_pan_gesture_on_amap(page):
# #     """
# #     在高德地图上测试平移手势。
# #     """
# #     # 使用高德地图的URL，定位到北京故宫
# #     page.goto('https://m.amap.com/search/mapview/poi=B000A7BD6C', wait_until='domcontentloaded')
# #
# #     # 等待地图容器加载完成
# #     # 高德地图的地图容器通常有一个id为 'amap-container' 的div
# #     map_container = page.locator('.amap-container')
# #     expect(map_container).to_be_visible()
# #
# #     print("开始平移地图...")
# #
# #     # 在地图容器上执行5次平移操作，每次向右下角移动
# #     for i in range(5):
# #         print(f"执行第 {i + 1} 次平移...")
# #         # deltaX为正数向右，deltaY为正数向下
# #         pan(map_container, deltaX=150, deltaY=100)
# #         # 每次平移后稍作等待，让地图有时间响应和渲染
# #         page.wait_for_timeout(500)
# #
# #     print("平移完成，准备截图...")
# #     page.screenshot(path="screenshot_amap.png")
# #     print("截图已保存为 screenshot_amap.png")
# #
# #
# # # --- 主执行逻辑 ---
# # with sync_playwright() as p:
# #     # 启动 Chromium 浏览器
# #     browser = p.chromium.launch(headless=False)  # 设置为非无头模式，方便观察
# #     # 使用移动设备上下文 (Pixel 7)
# #     context = browser.new_context(**p.devices['Pixel 7'])
# #     page = context.new_page()
# #
# #     # 运行测试
# #     test_pan_gesture_on_amap(page)
# #
# #     # 关闭浏览器
# #     browser.close()
#
#
def outer_function(x):
    # 外部函数的变量
    outer_var = x

    def inner_function(y):
        # 内部函数引用外部函数的变量
        return outer_var + y

    # 返回内部函数（不是调用）
    return inner_function


# 创建闭包
closure = outer_function(10)
# 调用闭包
result = closure(5)  # 结果为 15
print(result)
