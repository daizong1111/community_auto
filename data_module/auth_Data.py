class MyData:
    def __init__(self, local=True, excel=None, yaml=None, feishu=None):
        self.local = local
        self.excel = excel
        self.yaml = yaml
        self.feishu = feishu

    def userinfo(self, 被测环境, 角色名称):
        user = ""
        if self.excel:
            pass
            # todo 把excel转换成字典的方法
        elif self.yaml:
            pass
            # todo 把yaml转换成字典的方法
        elif self.feishu:
            pass
            # todo 把feishu转换成字典的方法
        else:
            user = {
                    # 测试环境
                    "test":
                    {
                     "错误用户名":
                         {"username": "ahs", "password": "Chinaictc@2022"},
                     "省级管理员-安徽省":
                         {"username": "ahsAdmin", "password": "Chinaictc@2022"},
                     "市级管理员-合肥市":
                         {"username": "shiji7969", "password": "dxnb66@2024_"},
                     "区县级管理员-庐阳区":
                         {"username": "quji7969", "password": "dxnb66@2024_"},
                     "街道管理员-中电数智街道":
                         {"username": "jdsdz6823", "password": "dxnb66@2024_"},
                     "社区管理员-中电数智社区":
                         {"username": "sqjyf3802", "password": "dxnb66@2024_"},
                     "物业管理人员-天王巷":
                         {"username":"wyjyf7916", "password": "dxnb66@2024_"},
                     "物业工作人员-小区99":
                         {"username": "WYgzrysdz6823", "password": "dxnb66@2024_"},
                     "一级网格员":
                         {"username": "yiji3066", "password": "dxnb66@2024_"},
                     "二级网格员":
                        {"username": "erji0509", "password": "dxnb66@2024_"},
                     "三级网格员":
                        {"username": "sanji7969", "password": "dxnb66@2024_"},
                     },
                   }

        return user[被测环境][角色名称]