pipeline {
    agent any

    environment {
        IMAGE = "vprocopan/task-tracker"
        CONTAINER_NAME = "task-tracker-web"
        SSH_HOST = "192.168.100.93"
        SSH_USER = "root"
    }

    stages {

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

                            echo "[+] Pulling latest image from Docker Hub"
                            docker pull ${IMAGE}:latest

                            echo "[+] Stopping old container"
                            docker stop ${CONTAINER_NAME} || true

                            echo "[+] Removing old container"
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