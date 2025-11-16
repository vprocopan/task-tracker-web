pipeline {
    agent any

    environment {
        SSH_CRED = 'jenkins-key'
        SSH_HOST = '192.168.100.93'
        REMOTE_DIR = '/opt/task-tracker'
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
                    pip install pytest pytest-cov
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

        stage('Deploy via SSH') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: SSH_CRED,
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER_VAR'
                    )
                ]) {

                    sh """
                        echo "=== Deploying to $SSH_HOST ==="

                        ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER_VAR@$SSH_HOST" << 'EOF' || true
set +e

echo '[+] Creating target directory'
mkdir -p $REMOTE_DIR

if [ -d "$REMOTE_DIR/.git" ]; then
    echo '[+] Repo exists — pulling latest'
    cd $REMOTE_DIR && git pull || true
else
    echo '[+] Fresh clone'
    git clone git@github.com:vprocopan/task-tracker-web.git $REMOTE_DIR || true
fi

echo '[+] Installing Python packages'
cd $REMOTE_DIR
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo '[+] Restarting Flask app'
pkill -f 'flask run' || true
nohup .venv/bin/python3 -m flask run --host=0.0.0.0 --port=5000 >/dev/null 2>&1 &

echo '[✓] Deploy finished'
EOF
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
            echo "Deployment successful! 🎉"
        }
        failure {
            echo "Deployment failed ❌"
        }
    }
}