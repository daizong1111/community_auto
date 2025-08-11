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

def highlight_position(page, x, y, color="red", size=20):
    """
    在指定的屏幕坐标位置添加一个高亮标记（如圆形）
    :param page: Playwright 的 page 对象
    :param x: X 坐标
    :param y: Y 坐标
    :param color: 高亮颜色
    :param size: 圆的直径
    """
    script = f"""
        () => {{
            const overlay = document.createElement('div');
            overlay.style.position = 'absolute';
            overlay.style.left = '{x - size // 2}px';
            overlay.style.top = '{y - size // 2}px';
            overlay.style.width = '{size}px';
            overlay.style.height = '{size}px';
            overlay.style.borderRadius = '50%';
            overlay.style.backgroundColor = '{color}';
            overlay.style.zIndex = '9999';
            overlay.style.pointerEvents = 'none';  // 不影响页面交互
            document.body.appendChild(overlay);

            // 3秒后自动移除
            setTimeout(() => {{ document.body.removeChild(overlay); }}, 3000);
        }}
    """
    page.evaluate(script)
