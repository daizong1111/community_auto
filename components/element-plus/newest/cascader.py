from playwright.sync_api import Page, Locator


class Cascader:
    def __init__(self, page: Page, label_text: str):
        """
        初始化一个通用的 el-cascader 组件操作类
        :param page: Playwright 页面对象
        :param label_text: 级联选择器上方标签文本，用于定位组件
        """
        self.page = page
        self.label_text = label_text
        self.container: Locator = self._locate_cascader_container()

    def _locate_cascader_container(self) -> Locator:
        """通过 label 文本找到对应的 el-cascader 容器"""
        return self.page.locator(
            f"//div[p[normalize-space()='{self.label_text}']]/following-sibling::div[1]"
        )

    def _get_panel(self) -> Locator:
        """获取级联面板区域"""
        return self.container.locator(".el-cascader-panel")

    def _get_node_by_label(self, label: str) -> Locator:
        """根据 label 获取节点"""
        return self._get_panel().locator(".el-cascader-node__label").filter(has_text=label)

    def _click_expand_arrow(self, level: int = 0):
        """点击指定层级的下拉箭头"""
        self.container.locator(".el-cascader-node__postfix").nth(level).click()

    def select(
        self,
        *values: str,
        expand_by_click: bool = True,
        check_strictly: bool = False,
        multiple: bool = False
    ):
        """
        选择级联选项（兼容不同 props 配置）

        :param values: 要选择的每一级值
        :param expand_by_click: 是否通过点击展开下一级（False 表示 hover）
        :param check_strictly: 是否启用 checkStrictly 模式（允许选择任意层级）
        :param multiple: 是否启用多选模式
        """
        for i, value in enumerate(values):
            if expand_by_click and i < len(values) - 1:
                # 展开当前层级
                self._click_expand_arrow(i)

            node = self._get_node_by_label(value)
            if check_strictly:
                # 在 checkStrictly 模式下，需要点击前面的 radio 或 checkbox
                if multiple:
                    # 多选时点击 checkbox
                    node.locator("..").locator(".el-checkbox").click()
                else:
                    # 单选时点击 radio
                    node.locator("..").locator(".el-radio").click()
            else:
                # 正常级联选择，点击 label 即可
                node.click()

def test_normal_cascader(page: Page):
    cascader = Cascader(page, "Child options expand when clicked (default)")
    cascader.select("Guide", "Disciplines", "Consistency")

def test_check_strictly_cascader(page: Page):
    cascader = Cascader(page, "Select any level of options (Single selection)")
    cascader.select("Guide", "Disciplines", "Consistency", check_strictly=True)

def test_multiple_check_strictly_cascader(page: Page):
    cascader = Cascader(page, "Select any level of options (Multiple selection)")
    cascader.select("Guide", "Navigation", check_strictly=True, multiple=True)


