from playwright.sync_api import Page

from pages.场所管理.类型管理 import 类型管理
from pages.基础信息.实有房屋.一房一档 import 一房一档
from pages.基础信息.实有房屋.小区信息 import 小区信息
from pages.基础信息.实有人口.人口信息 import 人口信息
from pages.基础信息.实有人口.特殊人群 import 特殊人群
from pages.基础信息.实有房屋.房屋管理 import 房屋管理
from pages.基础信息.实有房屋.楼栋管理 import 楼栋管理
from pages.基础信息.实有车辆.车辆信息 import 车辆信息
from pages.基础信息.实有人口.一人一档 import 一人一档
from pages.场所管理.场所信息 import 场所信息
from pages.登录页 import 登录页


class PageIns:
    def __init__(self, page: Page):
        self.page = page
        self.小区信息 = 小区信息(self.page)
        self.人口信息 = 人口信息(self.page)
        self.特殊人群 = 特殊人群(self.page)
        self.楼栋管理 = 楼栋管理(self.page)
        self.类型管理 = 类型管理(self.page)
        self.房屋管理 = 房屋管理(self.page)
        self.一房一档 = 一房一档(self.page)
        self.车辆信息 = 车辆信息(self.page)
        self.一人一档 = 一人一档(self.page)
        self.场所信息 = 场所信息(self.page)
        self.登录页 = 登录页(self.page)
