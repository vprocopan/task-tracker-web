pipeline {
    agent any

    environment {
        PYTHON = 'python3'
        VENV_DIR = '.venv'
    }

    stages {

        stage('Checkout') {
            steps {
                git credentialsId: 'jenkins-key',
                    branch: 'master',
                    url: 'git@github.com:vprocopan/task-tracker-web.git'
            }
        }

        stage('Setup Python Environment (local)') {
            steps {
                sh """
                    ${PYTHON} -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    . ${VENV_DIR}/bin/activate
                    pytest --cov=. --cov-report=xml -v || true
                """
            }
        }

        stage('Deploy to Remote Server') {
            steps {
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'jenkins-key',
                    keyFileVariable: 'SSH_KEY',
                    usernameVariable: 'SSH_USER'
                )]) {
                    sh """
                        echo "Deploying to remote server..."

                        rsync -avz -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" ./ $SSH_USER@192.168.100.93:/opt/task-tracker/

                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SSH_USER@192.168.100.93 "
                            pkill -f flask || true
                            cd /opt/task-tracker
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install -r requirements.txt
                            FLASK_APP=app.py nohup flask run --host=0.0.0.0 --port=5000 &
                        "
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
            echo "Workspace cleaned."
        }
        success {
            echo "Pipeline succeeded!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}