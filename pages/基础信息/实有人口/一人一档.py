from playwright.sync_api import Page, expect

from module.BasePage import PageObject
class 一人一档(PageObject):
    def __init__(self, page: Page):
        super().__init__(page)
        self.loc_年龄 = self.page.locator(".detailInfo > .el-row >.el-col").nth(0)
        self.loc_性别 = self.page.locator(".detailInfo > .el-row >.el-col").nth(1)
        self.loc_地址 = self.page.locator(".detailInfo > .el-row >.el-col").nth(2)
        self.loc_电话 = self.page.locator(".detailInfo > .el-row >.el-col").nth(3)
        self.loc_人口标签 = self.page.locator(".detailInfo > .el-row >.el-col").nth(4)

        self.loc_小区类型 = self.page.locator("(//div[@class='cardBox']//span)[4]/span[1]")
        self.loc_与房主关系 = self.page.locator("(//div[@class='cardBox']//span)[6]/span")

        self.loc_车牌号 = self.page.locator(".itemBox span")

    def 校验个人信息(self, 性别=None, 年龄=None, 地址=None, 电话=None, 人口标签=None, 小区类型=None, 与房主关系=None, 车牌号=None):
        expect(self.loc_性别).to_have_text("性别:"+性别)
        电话_密文 = 电话[0:3]+"****"+电话[-4:]
        expect(self.loc_电话).to_have_text("电话: "+电话_密文)

    def 校验关联房屋(self, 小区类型=None, 与房主关系=None):
        # expect(self.loc_小区类型).to_have_text(小区类型)
        expect(self.loc_与房主关系).to_have_text(与房主关系)

    def 校验关联车辆(self, 车牌号):
        车牌号_密文 = 车牌号[0:3]+"***"+车牌号[6:]
        expect(self.loc_车牌号).to_have_text("车辆1 "+车牌号_密文)
