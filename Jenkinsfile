pipeline {

    agent any

    stages {

        stage("POR FAVOR FUNCIONA"){
            steps{
                echo 'PFV'
            }
        }

        stage('Instalando as dependencias do front'){
            steps{
                dir('front') {
                    sh '''
                    node -v
                    npm -v
                    rm -rf node_modules package-lock.json
                    npm install --legacy-peer-deps --no-audit
                    '''
                    }
            }
        }
        stage('Testando'){
            steps{
                dir('front') {
                    sh '''
                    npm run test:run
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'front/test-results/**/*', allowEmptyResults: true, fingerprint: true
                }
            }
        }
        stage('Build Frontend'){
            steps{
                dir('front') {
                    sh '''
                    npm run build
                    '''
                }
            }
            post {
                success {
                    archiveArtifacts artifacts: 'front/dist/**/*', fingerprint: true
                }
            }
        }
        stage("Build Backend"){
            steps{
                dir('backend') {
                echo ' Começando Build Backend'
                sh """
                    python3 --version
                    pip3 --version
                    echo 'Criando UV Venv'
                    python3 -m venv venv
                    . venv/bin/activate
                    pip3 install uv
                    uv sync
                    echo 'Uv Instalado'
                """
                }
            }
        }
        stage("Test Backend") {
            steps { 
                dir("backend") {
                    echo "Testing Backend"
                    sh """
                        . venv/bin/activate
                        uv run pytest tests/. 
                    """
                }
            }
        }
        stage("Gerando Docker Image"){
            steps{
                dir("backend"){
                    sh """
                        docker --version
                        docker build -t socialjam-backend:latest .
                    """
                }
            }
        }
        
        stage('Send Notification') {
            steps {
                echo 'Enviando notificação de conclusão...'
                
                sh '''
                    cd Scripts
                    python3 send_email.py
                '''
            }
        }
    
    }
}
