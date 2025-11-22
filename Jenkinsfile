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
    stages {
        stage('前置工作') {
            steps {
                echo '工作目录'
                bat 'pwd' // 在Git Bash环境下可用，否则用 'echo %cd%'

                echo '清理历史文件'
                // 使用rd /s /q命令递归删除目录，相当于Linux的rm -rf
                bat 'if exist "%WORKSPACE%\\%repositoryName%" rd /s /q "%WORKSPACE%\\%repositoryName%"'

                echo '拉取项目'
                // 注意：Windows下git clone命令需要你的SSH密钥已配置好
                bat 'git clone git@github.com:%gitUsername%/%repositoryName%.git'

                echo '查看镜像'
                bat 'docker images'

                echo '查看容器'
                bat 'docker ps -a'

                echo '构建镜像'
                // 使用bat的&&连接符，确保在正确的目录下执行构建
                bat 'cd %repositoryName% && docker build -t %imageName%:%imageTag% .'
            }
        }
        stage('执行测试') {
            steps {
                echo '运行容器'
                // Windows下变量引用方式为%var%
                bat 'docker run -i --name=%containerName% %imageName%:%imageTag%'
            }
        }
        stage('后置工作') {
            steps {
                echo '保存报告'
                // Windows路径使用反斜杠，且变量用%%包裹
                bat 'docker cp %containerName%:/code/reports "%WORKSPACE%\\%repositoryName%\\reports"'

                echo '删除容器'
                bat 'docker rm %containerName%'

                echo '删除镜像'
                // 为了防止镜像名中包含特殊字符，整个路径用双引号括起来
                bat 'docker rmi "%imageName%:%imageTag%"'
            }
        }
    }
    post {
        success {
            echo '执行成功'
            echo '查看镜像'
            bat 'docker images'
            echo '查看容器'
            bat 'docker ps -a'
        }
        failure {
            echo '执行失败'
            echo '查看镜像'
            bat 'docker images'
            echo '查看容器'
            bat 'docker ps -a'
        }
    }
}
