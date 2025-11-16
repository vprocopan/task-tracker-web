pipeline {
	agent any

	environment {
		// Jenkins credential ID for GitHub SSH key
		GIT_CRED = 'github_ssh'
		PYTHON = 'python3'
		VENV_DIR = '.venv'
	}

	stages {

		stage('Checkout') {
			steps {
				sshagent([jenkins-key]) {
					checkout([
						$class: 'GitSCM',
						branches: [[name: '*/main']],
						userRemoteConfigs: [[
							url: 'git@github.com:vprocopan/task-tracker-web.git',
							credentialsId: jenkins-key
						]]
					])
				}
			}
		}

		stage('Setup Python Environment') {
			steps {
				sh """
					${PYTHON} -m venv ${VENV_DIR}
					. ${VENV_DIR}/bin/activate
					pip install --upgrade pip
					pip install -r requirements.txt
					pip install pytest pytest-cov flake8
				"""
			}
		}

		stage('Code Quality') {
			steps {
				sh """
					. ${VENV_DIR}/bin/activate
					flake8 . --max-line-length=120 --exclude=${VENV_DIR}
				"""
			}
		}

		stage('Run Tests') {
			steps {
				sh """
					. ${VENV_DIR}/bin/activate
					pytest --cov=. --cov-report=xml -v
				"""
			}
		}

		stage('Build and Deploy') {
			steps {
				sh """
					. ${VENV_DIR}/bin/activate
					echo "Starting Flask Task Tracker..."
					export FLASK_APP=app.py
					export FLASK_ENV=production
					python -m flask run --host=0.0.0.0 &
				"""
			}
		}
	}

	post {
		always {
			cleanWs()
			echo "Cleaning workspace..."
		}
		success {
			echo 'Pipeline succeeded!'
		}
		failure {
			echo 'Pipeline failed!'
		}
	}
}