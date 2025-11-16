pipeline {
    agent any

    environment {
        SSH_CRED = 'jenkins-key'
        SSH_HOST = '192.168.100.93'
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

        stage('Setup Python Environment (local)') {
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

        stage('Deploy') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: SSH_CRED,
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {

                    sh """
                        echo "=== SSH into server and deploy ==="

                        ssh -i \$SSH_KEY -o StrictHostKeyChecking=no \$SSH_USER@$SSH_HOST '

                            set -e

                            echo "[+] Ensure directory"
                            mkdir -p $REMOTE_DIR

                            echo "[+] Clone or pull"
                            if [ -d "$REMOTE_DIR/.git" ]; then
                                cd $REMOTE_DIR && git pull
                            else
                                git clone $GIT_REPO $REMOTE_DIR
                            fi

                            echo "[+] Install dependencies"
                            cd $REMOTE_DIR
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt

                            echo "[+] Restart Flask"
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
        }
    }
}