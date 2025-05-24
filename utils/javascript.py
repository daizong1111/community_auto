# 某些元素使用playwright的方法直接操作是无效的，必须执行js脚本才可以，对这些常用的js操作进行封装
def clear_locator(locator):
    locator.evaluate("element => element.value = ''")

def click_locator(locator):
    locator.evaluate("element => element.click()")
