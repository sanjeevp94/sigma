pipeline {
    agent any

    environment {
        SIGMA_CLIENT_ID = credentials('sigma-client-id')
        SIGMA_CLIENT_SECRET = credentials('sigma-client-secret')
        // Map branches to DEPLOY_ENV
        DEPLOY_ENV = "${env.BRANCH_NAME == 'main' ? 'uat' : (env.BRANCH_NAME == 'release' ? 'prod' : 'dev')}"
    }

    stages {
        stage('Checkout & Setup') {
            steps {
                checkout scm
                // Ensure uv is installed
                sh 'curl -LsSf https://astral.sh/uv/install.sh | sh'
                sh 'make setup'
            }
        }

        stage('Code Quality & Security') {
            steps {
                sh 'make lint'
                sh 'make security'
            }
        }

        stage('Deploy Connections & RBAC') {
            // Deploy connections/rbac on main (UAT) and release (PROD)
            when {
                anyOf {
                    branch 'main'
                    branch 'release'
                }
            }
            steps {
                script {
                    // Pull specific db credentials based on environment
                    withCredentials([string(credentialsId: "redshift-svc-${env.DEPLOY_ENV}-pass", variable: "REDSHIFT_${env.DEPLOY_ENV.toUpperCase()}_PASS")]) {
                        sh "uv run python -m src.sync_connections"
                    }
                }
                sh 'uv run python -m src.sync_rbac'
            }
        }

        stage('Deploy Artifacts & Update UAT Tag') {
            when { branch 'main' }
            steps {
                // Pushes new JSON and increments version
                sh 'uv run python -m src.sync_artifacts'
                // Reconciles the UAT tag to point to latest version
                sh 'uv run python -m src.sync_tags'
            }
        }

        stage('Promote PROD Release') {
            when { branch 'release' }
            steps {
                // Skips pushing artifacts; only advances the PROD tag pointer based on tags.yaml state
                sh 'uv run python -m src.sync_tags'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
