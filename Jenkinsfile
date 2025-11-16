pipeline {
    agent any

    environment {
        IMAGE = "ghcr.io/vprocopan/task-tracker-web"
        CONTAINER_NAME = "task-tracker-web"
        SSH_HOST = "192.168.100.93"
        SSH_USER = "root"
    }

    stages {

        /* -----------------------------------------
           CHECKOUT CODE
        ----------------------------------------- */
        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'git@github.com:vprocopan/task-tracker-web.git',
                    credentialsId: 'jenkins-key'
            }
        }

        /* -----------------------------------------
           BUILD DOCKER IMAGE
        ----------------------------------------- */
        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${IMAGE}:latest .
                """
            }
        }

        /* -----------------------------------------
           LOGIN TO GHCR
        ----------------------------------------- */
        stage('Login to GHCR') {
            steps {
                withCredentials([string(credentialsId: 'ghtkn', variable: 'CR_PAT')]) {
                    sh """
                        echo \$CR_PAT | docker login ghcr.io -u vprocopan --password-stdin
                    """
                }
            }
        }

        /* -----------------------------------------
           PUSH DOCKER IMAGE
        ----------------------------------------- */
        stage('Push Docker Image') {
            steps {
                sh """
                    docker push ${IMAGE}:latest
                """
            }
        }

        /* -----------------------------------------
           DEPLOY TO REMOTE SERVER (SSH)
        ----------------------------------------- */
        stage('Deploy to Remote Server') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'jenkins-key',
                                                  keyFileVariable: 'SSH_KEY',
                                                  usernameVariable: 'SSH_USER_VAR')]) {

                    sh """
                        ssh -o StrictHostKeyChecking=no -i \$SSH_KEY ${SSH_USER}@${SSH_HOST} '
                            set -e

                            echo "[+] Logging into GHCR"
                            echo "${CR_PAT}" | docker login ghcr.io -u vprocopan --password-stdin

                            echo "[+] Pulling latest image"
                            docker pull ${IMAGE}:latest

                            echo "[+] Stopping old container"
                            docker stop ${CONTAINER_NAME} || true
                            docker rm ${CONTAINER_NAME} || true

                            echo "[+] Starting new container"
                            docker run -d \
                                --name ${CONTAINER_NAME} \
                                -p 5000:5000 \
                                ${IMAGE}:latest

                            echo "[+] Deployment successful on ${SSH_HOST}"
                        '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "🚀 Deployment completed successfully!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}