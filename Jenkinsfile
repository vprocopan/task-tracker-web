pipeline {
    agent any

    environment {
        GIT_CRED = 'jenkins-key'     // GitHub SSH key
        SSH_CRED = 'jenkins-key'     // Same key for deployment
        PYTHON = 'python3'
        VENV_DIR = '.venv'

        REMOTE_USER = 'root'         // <---- changed to root
        REMOTE_HOST = '192.168.100.93'
        REMOTE_DIR = '/opt/task-tracker'
    }

    stages {

        stage('Checkout') {
            steps {
                git credentialsId: GIT_CRED,
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
                sshagent([SSH_CRED]) {

                    sh """
                        echo "Creating remote directory..."
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_DIR}"

                        echo "Copying project files..."
                        rsync -avz --delete \
                            --exclude '__pycache__' \
                            --exclude '.venv' \
                            ./ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/

                        echo "Setting up remote venv..."
                        ssh ${REMOTE_USER}@${REMOTE_HOST} "
                            cd ${REMOTE_DIR} &&
                            ${PYTHON} -m venv venv &&
                            . venv/bin/activate &&
                            pip install --upgrade pip &&
                            pip install -r requirements.txt
                        "

                        echo "Restarting Flask app on remote..."
                        ssh ${REMOTE_USER}@${REMOTE_HOST} "
                            pkill -f 'flask' || true
                            cd ${REMOTE_DIR}
                            . venv/bin/activate
                            nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
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
            echo "Deployment successful!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}