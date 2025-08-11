# 测试夹具-获取浏览器当前打开页面，并返回 MeetingRoomManagePageBase 对象
from playwright.sync_api import sync_playwright


def meeting_room_manage_page():
    with sync_playwright() as playwright:
        # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        # 通过ip和端口连接到已经打开的chromium浏览器
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(3000)  # 设置默认超时时间为 3000 毫秒


        # page.get_by_text("会议室名称").highlight()
        # # page.get_by_role("textbox", name='* 会议室名称：').highlight()
        # # # 修改 get_by_role 的 name 参数以正确匹配包含特殊字符的标签
        # loc = page.get_by_role("textbox", name="会议室名称：")
        # loc.highlight()
        # page.get_by_role("textbox", name= "/.*会议室名称： /" ).highlight()
        # page.get_by_placeholder("不超过10个字").highlight()
        page.wait_for_timeout(6000)

if  __name__ == "__main__":
    meeting_room_manage_page()
