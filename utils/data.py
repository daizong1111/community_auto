def 对比两个字典中的数据(字典1: dict, 字典2: dict, 映射关系: dict):
    for key, value in 映射关系.items():
        assert 字典1[key] == 字典2[value], f"两个字典的值不相同，当前比较的项目的名称为{key}，第一个字典的值为{字典1[key]}，第二个字典的值为{字典2[value]}，第一个字典为：{字典1}，第二个字典为：{字典2}"
    return True
