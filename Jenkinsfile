pipeline {
    agent any
    // agent {
    //     docker {
    //         image 'docker:24'
    //         args '-v /var/run/docker.sock:/var/run/docker.sock -u root'
    //     }
    // }
    //agent { label 'docker-node' }
    
    
    environment {
        gitUsername = 'daizong1111'
        repositoryName = 'community_auto'
        imageName = 'community'
        imageTag = '1.0.0'
        containerName = 'community_ui_auto_test'
    }
    stages {
        stage('前置工作') {
            steps {
                sh '''
                // apk add --no-cache docker  # Alpine Linux
                # 或
                apt-get update && apt-get install -y docker.io  # Debian/Ubuntu
                # 或
                // yum install -y docker      # CentOS/RHEL（较旧）
                '''
                sh 'docker images'
                
                script {
                    echo '工作目录'
                    if (isUnix()) {
                        sh 'pwd'
                    } else {
                        bat 'cd'
                    }

                    echo '清理历史文件'
                    if (isUnix()) {
                        sh "rm -rf ${env.WORKSPACE}/${env.repositoryName}"
                    } else {
                        bat "if exist \"${env.WORKSPACE}\\${env.repositoryName}\" rd /s /q \"${env.WORKSPACE}\\${env.repositoryName}\""
                    }

                    echo '拉取项目'
                    if (isUnix()) {
                        sh "git clone https://github.com/${env.gitUsername}/${env.repositoryName}.git"
                    } else {
                        bat "git clone https://github.com/${env.gitUsername}/${env.repositoryName}.git"
                    }

                    echo '查看当前 Docker 状态'
                    sh 'docker images'
                    sh 'docker ps -a'

                    echo '开始构建 Docker 镜像（带详细日志）'
                    // 关键：添加 --progress=plain 确保逐行输出日志，便于 Jenkins 显示
                    if (isUnix()) {
                        sh "cd ${env.repositoryName} && docker build --progress=plain -t ${env.imageName}:${env.imageTag} ."
                    } else {
                        bat "cd ${env.repositoryName} && docker build --progress=plain -t ${env.imageName}:${env.imageTag} ."
                    }

                    echo '镜像构建完成'
                    sh 'docker images | grep ${imageName}'
                }
            }
        }

        stage('执行测试') {
            steps {
                script {
                    if (isUnix()) {
                        echo '运行容器并执行测试'
                        // 同样，容器运行日志也会自动输出到控制台
                        sh "docker run -i --rm --name=${env.containerName} ${env.imageName}:${env.imageTag}"
                    } else {
                        echo '运行容器并执行测试'
                        bat "docker run -i --rm --name=${env.containerName} ${env.imageName}:${env.imageTag}"
                    }
                    
                }
            }
        }

        stage('后置工作') {
            steps {
                script {
                    echo '保存测试报告'
                    if (isUnix()) {
                        sh "mkdir -p ${env.WORKSPACE}/${env.repositoryName}/reports"
                        sh "docker cp ${env.containerName}:/code/reports/. ${env.WORKSPACE}/${env.repositoryName}/reports/ || echo 'No reports to copy'"
                    } else {
                        bat "if not exist \"${env.WORKSPACE}\\${env.repositoryName}\\reports\" mkdir \"${env.WORKSPACE}\\${env.repositoryName}\\reports\""
                        bat "docker cp ${env.containerName}:/code/reports \"${env.WORKSPACE}\\${env.repositoryName}\\reports\" || echo 'No reports to copy'"
                    }

                    // 注意：如果容器在测试阶段已加 --rm，则此处可能不存在
                    echo '清理容器（如果存在）'
                    sh "docker rm -f ${env.containerName} || true"

                    echo '清理镜像'
                    sh "docker rmi ${env.imageName}:${env.imageTag} || true"
                }
            }
        }
    }

    post {
        always {
            script {
                echo '=== 最终状态 ==='
                sh 'docker images'
                sh 'docker ps -a'
            }
        }
        success {
            echo '✅ 流水线执行成功！'
        }
        failure {
            echo '❌ 流水线执行失败！请检查上述日志。'
        }
    }
}
