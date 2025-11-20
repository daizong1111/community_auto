import random
import time
from datetime import datetime

import pytest
from playwright.sync_api import expect

from module.BasePage import 使用new_context登录并返回实例化的page
from testcases import *

def test_验证特殊人群列表数据(new_context):
    my_page_测试员 = 使用new_context登录并返回实例化的page(new_context, "街道管理员-中电数智街道")
    with 测试步骤("跳转到人口信息页面"):
        my_page_测试员.人口信息.navigate()

    with 测试步骤("跳转到特殊人群页面"):
        my_page_测试员.特殊人群.navigate()