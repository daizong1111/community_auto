# 第一阶段：构建精简的 JRE 镜像
FROM eclipse-temurin:21-jdk-jammy AS jre-build

# 构建参数，用于触发CI构建（时间戳）
#ARG CI_TRIGGER="20251111-144543"

# 使用 jlink 工具创建自定义运行时镜像，减小镜像体积
RUN jlink \
         --add-modules ALL-MODULE-PATH \
         --strip-debug \
         --no-man-pages \
         --no-header-files \
         --compress=2 \
         --output /javaruntime

# 第二阶段：使用 Jenkins inbound-agent 作为中间层
 https://github.com/jenkinsci/docker-agent/blob/master/debian/Dockerfile
FROM jenkins/inbound-agent:3309.v27b_9314fd1a_4-3 AS inbound-agent

# 第三阶段：基础镜像是 Playwright Python 运行环境
FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

# 设置 Java 环境变量
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH "${JAVA_HOME}/bin:${PATH}"
# 将第一阶段构建的精简 JRE 复制到当前镜像
COPY --from=jre-build /javaruntime $JAVA_HOME

# Jenkins Agent 配置
#ARG VERSION=3309.v27b_9314fd1a_4
#ARG AGENT_WORKDIR=/root/agent

# 安装必要工具并下载 Jenkins agent jar 包
RUN apt-get update \
  && apt-get -y install \
    git-lfs \
    curl \
    fontconfig \
    unzip \
    wget \
  # 下载 Jenkins remoting jar 包
#  && curl --create-dirs -fsSLo /usr/share/jenkins/agent.jar https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/${VERSION}/remoting-${VERSION}.jar \
#  && chmod 755 /usr/share/jenkins \
#  && chmod 644 /usr/share/jenkins/agent.jar \
#  && ln -sf /usr/share/jenkins/agent.jar /usr/share/jenkins/slave.jar \
  && rm -rf /var/lib/apt/lists/*

# 复制并配置 Jenkins agent 启动脚本
#COPY --from=inbound-agent /usr/local/bin/jenkins-agent /usr/local/bin/jenkins-agent
#RUN chmod +x /usr/local/bin/jenkins-agent &&\
#    ln -s /usr/local/bin/jenkins-agent /usr/local/bin/jenkins-slave

# 设置语言环境和工作目录
ENV LANG C.UTF-8
#ENV AGENT_WORKDIR=${AGENT_WORKDIR}
#RUN mkdir /root/.jenkins && mkdir -p ${AGENT_WORKDIR}

# allure2
ARG ALLURE2_VERSION=2.34.0
RUN wget -qO /tmp/allure.zip "https://github.com/allure-framework/allure2/releases/download/${ALLURE2_VERSION}/allure-${ALLURE2_VERSION}.zip"; \
    unzip /tmp/allure.zip -d /opt/; \
    mv /opt/allure-${ALLURE2_VERSION} /opt/allure; \
    ln -s /opt/allure/bin/allure /usr/local/bin/allure; \
    rm -f /tmp/allure.zip

# Python 环境和时区配置
#ARG DEBIAN_FRONTEND=noninteractive
#ARG TIMEZONE="Asia/Shanghai"

# 安装时区支持并设置时区
#RUN apt-get update; \
#    apt-get install -y \
#        tzdata; \
#    apt-get upgrade -y --no-install-recommends; \
#    echo ${TIMEZONE} > /etc/timezone; \
#    rm /etc/localtime; \
#    dpkg-reconfigure -f noninteractive tzdata; \
#    rm -rf /var/lib/apt/lists/*; \

# 复制并安装 Python 依赖
COPY requirements.txt /root
RUN pip3 install --no-cache-dir -r /root/requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple; \
    playwright install-deps; \
    playwright install

# 添加这一行：复制当前项目到 docker 镜像中
# 添加这一行：复制当前项目到用户主目录
COPY . /root/project

CMD ["pytest", "testcases"]

# 复制自定义的 Playwright 用户实现到 Locust 插件目录
#COPY locust_plugins/users/playwright.py /usr/local/lib/python3.10/dist-packages/locust_plugins/users/playwright.py
