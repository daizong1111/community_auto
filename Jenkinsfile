pipeline {
    agent any
    environment {
        /* Git用户名称 */
        gitUsername = 'daizong1111'
        /* 自动化仓库名称 */
        repositoryName = 'community_auto'
        /* 自定义镜像名称 */
        imageName = 'community'
        /* 自定义镜像版本 */
        imageTag = '1.0.0'
        /* 自定义容器名称 */
        containerName = 'community_ui_auto_test'
    }
    options {
        // 可选：设置超时防止卡死
        timeout(time: 30, unit: 'MINUTES')
    }
    stages {
        stage('前置工作') {
            steps {
                echo '工作目录'
                bat 'cd'

                echo '清理历史文件'
                bat 'if exist "%WORKSPACE%\\%repositoryName%" rd /s /q "%WORKSPACE%\\%repositoryName%"'

                echo '拉取项目'
                bat 'git clone https://github.com/%gitUsername%/%repositoryName%.git'

                echo '查看现有镜像'
                bat 'docker images'

                echo '查看现有容器'
                bat 'docker ps -a'

                echo '构建 Docker 镜像（详细日志）'
                // 添加 --progress=plain 以获得清晰、非 ANSI 的构建日志（推荐 Docker >=20.10）
                // 如果你的 Docker 版本较低，可去掉 --progress=plain
                bat 'cd "%WORKSPACE%\\%repositoryName%" && docker build --progress=plain -t %imageName%:%imageTag% .'
            }
        }
        stage('执行测试') {
            steps {
                echo '运行测试容器（确保容器会自动退出）'
                // 假设你的容器启动后执行测试并退出（非交互式长时间运行）
                // 如果容器不退出，Jenkins 会卡住！
                bat 'docker run --rm --name=%containerName% %imageName%:%imageTag%'
                // 使用 --rm 可自动删除容器，简化后续清理（推荐！）
            }
        }
        stage('后置工作') {
            steps {
                script {
                    // 检查容器是否还存在（如果用了 --rm，这步可能不需要）
                    def containerExists = sh(
                        script: 'docker ps -a --filter "name=^/%containerName%\$" --format "{{.Names}}" | findstr /R "^%containerName%\$"',
                        returnStdout: true
                    ).trim()
                    if (containerExists) {
                        echo '保存测试报告'
                        bat 'docker cp %containerName%:/code/reports "%WORKSPACE%\\%repositoryName%\\reports"'
                    } else {
                        echo '容器已自动清理（可能使用了 --rm），跳过报告复制'
                    }
                }

                echo '强制清理容器（如果存在）'
                bat 'docker rm -f %containerName% 2>nul || exit /b 0'

                echo '删除镜像'
                bat 'docker rmi -f "%imageName%:%imageTag%" 2>nul || exit /b 0'
            }
        }
    }
    post {
        always {
            echo 'Pipeline 结束：显示当前 Docker 状态'
            bat 'docker images'
            bat 'docker ps -a'
        }
        success {
            echo '✅ 执行成功！'
        }
        failure {
            echo '❌ 执行失败！'
        }
    }
}
