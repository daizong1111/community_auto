# 测试夹具-获取已经打开的浏览器
# import pytest
# from playwright.sync_api import Browser, expect
# from pages.工单报表 import 工单报表
# from utils.GetPath import get_path

# @pytest.fixture(scope="session")
# def browser_opened(playwright):
#     # browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
#     # 通过ip和端口连接到已经打开的chromium浏览器
#     browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
#     yield browser

# @pytest.fixture(scope="module")
# def 浏览器已打开的页面(browser_opened):
#     # 若浏览器已打开，则直接使用已打开的浏览器，否则创建一个新的浏览器实例
#     context = browser_opened.contexts[0] if browser_opened.contexts else browser_opened.new_context(accept_downloads=True)
#     # 模拟弱网环境
#     # 拦截所有请求，模拟网络延迟
#     # context.route(re.compile(r"https?://.*"), slow_response)
#     # 若该浏览器中有页面，则直接使用已打开的页面，否则创建一个新的页面
#     page = context.pages[0] if context.pages else context.new_page()
#     page.set_default_timeout(6000)  # 设置默认超时时间为 4000 毫秒
#     # page.on("response", requests)
#     yield page

# def test_导出(浏览器已打开的页面):
#     """
#     导出功能测试用例
#     1. 点击导出按钮
#     2. 打开导出的文件
#     3. 将导出的文件与页面中的表格内容对比
#     4. 断言：二者内容完全相同
#     """
#     import os
#     import pandas as pd
#     from io import StringIO
#
#     page = 浏览器已打开的页面
#     page.goto("http://223.244.28.251:8087/gdbb")
#     page_工单报表 = 工单报表(page)
#
#     # 等待页面加载完成
#     expect(page_工单报表.page.get_by_text("暂无数据")).not_to_be_visible()
#
#     # 获取页面表格数据
#     table_data = []
#     # 假设表格有表头，从第二行开始读取数据
#     rows = page.query_selector_all(".el-table__body-wrapper tbody tr")
#     for row in rows:
#         cells = row.query_selector_all("td")
#         row_data = [cell.inner_text().strip() for cell in cells]
#         table_data.append(row_data)
#
#     with page.expect_download() as file:
#         # 点击导出按钮
#         page_工单报表.click_button("导出明细")  # 假设有这样的方法
#     file.value.save_as(get_path(f".temp/工单明细.xls"))
#
#     # 查找最近下载的文件（假设下载到默认下载目录）
#     download_path = get_path(f".temp")
#     files = os.listdir(download_path)
#     # 找到最新的CSV文件（假设导出的是CSV格式）
#     # 找到最新的.xls文件（导出的是Excel格式）
#     export_files = [f for f in files if f.endswith('.xls')]
#     export_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_path, x)), reverse=True)
#
#     if export_files:
#         latest_file = os.path.join(download_path, export_files[0])
#
#         import os
#
#         # 确保文件存在且是正确的格式
#         if os.path.exists(latest_file) and latest_file.endswith('.xls'):
#             try:
#                 # 读取导出的Excel文件内容
#                 exported_df = pd.read_excel(latest_file, engine='xlrd')
#             except Exception as e:
#                 print(f"读取Excel文件时出错: {e}")
#                 # 可以尝试其他引擎或方法
#                 exported_df = pd.read_excel(latest_file, engine='openpyxl')
#         else:
#             raise FileNotFoundError(f"找不到有效的.xls文件: {latest_file}")
#         # 将页面表格数据转换为DataFrame
#         # 这里需要根据实际表格结构调整列名
#         columns = ["维保人姓名", "联系电话", "关联区域", "工单总数", "已处理工单数", "工单处理率", "超48h办结数", "超时办结率"]  # 需要替换为实际的列名
#         table_df = pd.DataFrame(table_data, columns=columns[:len(table_data[0]) if table_data else 0])
#
#         # 比较两个DataFrame是否完全相同（忽略空格和换行）
#         # 预处理数据：去除空格和换行符
#         exported_df_clean = exported_df.applymap(
#             lambda x: str(x).strip().replace('\n', '').replace('\r', '') if pd.notna(x) else x)
#         table_df_clean = table_df.applymap(
#             lambda x: str(x).strip().replace('\n', '').replace('\r', '') if pd.notna(x) else x)
#
#         assert exported_df_clean.equals(table_df_clean), "导出的文件内容与页面表格内容不一致"
#
#         print("导出功能测试通过：导出文件内容与页面表格内容完全一致")
#     else:
#         raise FileNotFoundError("未找到导出的文件")


