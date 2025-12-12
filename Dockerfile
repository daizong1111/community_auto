# 基础镜像
FROM ccr.ccs.tencentyun.com/onecontract-cloud/jnlp-agent-python:0.3.0-playwright


# 复制并安装 Python 依赖
#COPY requirements.txt /root
#RUN pip3 install --no-cache-dir -r /root/requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple;

# 添加这一行：复制当前项目到 docker 镜像中
COPY . /root/project

# 切换到项目根目录
WORKDIR /root/project

CMD ["pytest", "testcases"]
