pipeline {
    agent any

    environment {
        SSH_CRED = 'jenkins-key'
        SSH_HOST = '192.168.100.93'
        SSH_USER = 'root'
        REMOTE_DIR = '/opt/task-tracker'
        GIT_REPO = 'https://github.com/vprocopan/task-tracker-web.git'
    }

    stages {

        stage('Checkout (local)') {
            steps {
                git branch: 'master',
                    url: 'git@github.com:vprocopan/task-tracker-web.git',
                    credentialsId: SSH_CRED
            }
        }

        stage('Setup Python Env (local)') {
            steps {
                sh """
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    . .venv/bin/activate
                    pytest -v || true
                """
            }
        }

        stage('Deploy to 192.168.100.93 as root') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: SSH_CRED,
                        keyFileVariable: 'SSH_KEY'
                    )
                ]) {

                    sh """
                        echo "=== Deploying as ROOT to $SSH_HOST ==="

                        ssh -i \$SSH_KEY -o StrictHostKeyChecking=no $SSH_USER@$SSH_HOST '
                            set -e

                            echo "[+] Creating directory"
                            mkdir -p $REMOTE_DIR

                            echo "[+] Cloning or pulling repository"
                            if [ -d "$REMOTE_DIR/.git" ]; then
                                cd $REMOTE_DIR && git pull
                            else
                                git clone $GIT_REPO $REMOTE_DIR
                            fi

                            echo "[+] Installing dependencies"
                            cd $REMOTE_DIR
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt

                            echo "[+] Restarting Flask app"
                            pkill -f "flask run" 2>/dev/null || true
                            nohup .venv/bin/python3 -m flask run --host=0.0.0.0 --port=5000 &>/dev/null &
                        '
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
    }
}