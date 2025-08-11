import os
import datetime

import pytest

# 定义运行测试的函数
def run_tests():
    # print(os.environ['PATH'])
    # 获取系统当前时间
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # 将时间拼接到文件名中
    results_dir = f"allure-results_{timestamp}"
    # 如果目录不存在，则创建目录
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    # 构建 pytest 参数
    pytest_args = ['-v',
                   '-s',
                   f"--alluredir={results_dir}",
                   # '--alluredir=allure-results',
                   # 执行指定的用例文件(不写则执行所有的用例)

                   # 'tests/test_基础信息/test_场所管理/test_场所信息/test_单位信息.py::TestAdd::test_add_success',
                   # 'tests/test_基础信息/test_场所管理/test_场所信息/test_单位信息.py::TestEdit::test_edit_success',
                   # 'tests/test_基础信息/test_实有车辆/test_车辆黑名单.py::TestAdd::test_add_success',
                   # r'tests/test_网格管理/test_事件管理/test_事件管理_流程_PC端.py::TestProcess居民到物管::test_process_路径6',
                   # 'tests/test_网格管理/test_网格区域管理/test_网格区域划分.py::TestAdd::test_add_success',
                   # 'tests/test_网格管理/test_网格区域管理/test_网格区域划分.py::TestEdit::test_edit_success',
                   # 'tests/test_网格管理/test_网格区域管理/test_网格区域划分.py::TestDelete::test_delete_success',

                   # 'tests/test_基础信息/test_场所管理',
                   # 'tests/test_网格管理/test_事件管理/test_事件管理流程/test_事件管理_流程_H5端.py',
                   'tests/test_网格管理/test_事件管理/test_事件管理流程/test_事件管理_流程_PC端.py',

                   # 'tests/test_网格管理',

                   ]
    # 运行 pytest
    pytest.main(pytest_args)
    # 生成HTML报告
    os.system(f"allure serve {results_dir}")


# 主程序入口
if __name__ == "__main__":
    run_tests()  # 运行测试
