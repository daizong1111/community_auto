#!/bin/bash
# 切换到 hcbm-auto-Playwright 项目目录
#cd hcbm-auto-Playwright
#rm -rf allure-results
rm -rf pw-allure .test-results

sleep ${delay}m

# 获取当前星期几（1=周一，7=周日
weekday=$(date +%u)
# 获取当前小时（24小时制）
hour=$(date +%H)

# 判断是否只执行冒烟测试的条件：
# 条件1：今天是周四（weekday等于4）且当前时间在19:00-23:59之间
# 条件2：smoke环境变量等于"only_Thursday" 或 "yes"
if [ "$weekday" -eq 4 ] && [ "$hour" -ge 19 ] && [ "$hour" -le 23 ] && [ "$smoke" = "only_Thursday" ] || [ "$smoke" = "yes" ]; then
	# 输出提示信息：仅运行冒烟测试
	echo ”仅运行冒烟测试“
	# 调用change_round.py脚本，设置测试轮次为normal模式
	python utils/change_round.py ${feishu_receive_id} $base_url normal
	# 执行冒烟测试用例
    # 参数说明：
    # -vqs: 详细输出、静默模式、简短测试进度显示
    # --alluredir=allure-results: 指定Allure测试报告结果存储目录
    # --tracing=on: 启用追踪记录
    # --video=retain-on-failure: 失败时保留视频录制
    # --screenshot=only-on-failure: 仅在失败时截图
    # --base-url=$base_url: 指定被测系统的基础URL
    # --persistent=on: 启用持久化上下文
    # --maxschedchunk=1: 最大调度块大小
    # --verbose: 详细输出
    # --reruns ${rurun_count}: 失败重试次数
    # -n ${concurrent}: 并发执行的worker数量
    # -p no:warnings: 禁用警告插件
    # --feishu ${feishu_receive_id}: 飞书通知接收人ID
    # --jobUrl ${JOB_URL}: Jenkins任务URL
    # --send_feishu_report=on: 启用飞书报告发送
    # --ui_timeout 40_000: UI操作超时时间（40秒）
    # -k 冒烟: 只执行标记为"冒烟"的测试用例
    # --report_mark 冒烟: 报告标记为"冒烟"
    # --tempdir /home/jenkins/cache: 指定临时目录
    # testcases: 测试用例目录
    pytest -vqs --alluredir=allure-results --tracing=on --video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url --persistent=on  --maxschedchunk=1 --verbose --reruns ${rurun_count} -n ${concurrent} -p no:warnings --feishu ${feishu_receive_id} --jobUrl ${JOB_URL} --send_feishu_report=on --ui_timeout 40_000 -k 冒烟 --report_mark 冒烟 --tempdir /home/jenkins/cache testcases
else
   # 输出提示信息：运行全量测试
	echo ”运行全量测试“
	 # 设置测试轮次为normal模式
    python utils/change_round.py ${feishu_receive_id} $base_url normal
     # 关闭错误退出模式，即使测试失败也继续执行后续命令
    set +e
     # 第一轮：执行冒烟测试用例
    pytest -vqs --alluredir=allure-results --tracing=on --video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url --persistent=on  --maxschedchunk=1 --verbose --reruns ${rurun_count} -n ${concurrent} -p no:warnings --feishu ${feishu_receive_id} --jobUrl ${JOB_URL} --send_feishu_report=on --ui_timeout 40_000 -k 冒烟 --report_mark 冒烟 --tempdir /home/jenkins/cache testcases
    # 第二轮：执行除round和冒烟以外的基本功能测试
    pytest -vqs --alluredir=allure-results --tracing=on --video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url --persistent=on  --maxschedchunk=1 --verbose --reruns ${rurun_count} -n ${concurrent} -p no:warnings --feishu ${feishu_receive_id} --jobUrl ${JOB_URL} --send_feishu_report=on --ui_timeout 40_000 -k "not round and not 冒烟" --report_mark 基本功能 --tempdir /home/jenkins/cache testcases
     # 恢复错误退出模式
    set -e
    # 设置测试轮次为变更v3模式
    python utils/change_round.py ${feishu_receive_id} $base_url 变更v3
    # 关闭错误退出模式
    set +e
    # 第三轮：执行变更v3相关的测试用例
    pytest -vqs --alluredir=allure-results --tracing=on --video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url --persistent=on  --maxschedchunk=1 --verbose --reruns ${rurun_count} -n ${concurrent} -p no:warnings --feishu ${feishu_receive_id} --jobUrl ${JOB_URL} --send_feishu_report=on --ui_timeout 40_000 -k round_变更_v3 --report_mark 变更v3 --tempdir /home/jenkins/cache testcases
    # 恢复错误退出模式
    set -e
    # 设置测试轮次为拟制v3模式
    python utils/change_round.py ${feishu_receive_id} $base_url 拟制v3
    # 关闭错误退出模式
    set +e
    # 第四轮：执行拟制3.0相关的测试用例
    pytest -vqs --alluredir=allure-results --tracing=on --video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url --persistent=on  --maxschedchunk=1 --verbose --reruns ${rurun_count} -n ${concurrent} -p no:warnings --feishu ${feishu_receive_id} --jobUrl ${JOB_URL} --send_feishu_report=on --ui_timeout 40_000 -k 拟制3_0 --report_mark 拟制3.0 --tempdir /home/jenkins/cache --test-suffix 拟制v3 testcases
    # 第五轮：执行系统登录测试用例（汇总测试）
    pytest -vqs --alluredir=allure-results --tracing=on --video=retain-on-failure --screenshot=only-on-failure --base-url=$base_url --persistent=on  --maxschedchunk=1 --verbose --reruns ${rurun_count} -n ${concurrent} -p no:warnings --feishu ${feishu_receive_id} --jobUrl ${JOB_URL} --send_feishu_report=on --ui_timeout 40_000 --report_mark 汇总 --tempdir /home/jenkins/cache testcases/系统登录/test_login.py
    # 恢复错误退出模式
    set -e
    # 最后恢复测试轮次为normal模式
    python utils/change_round.py ${feishu_receive_id} $base_url normal
fi