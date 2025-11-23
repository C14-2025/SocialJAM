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
                    npm run test:run -- src/_testes/forms
                    '''
                    }
            }
        }
        stage("Build Backend"){
            steps{
                dir('backend') {
                echo 'Build Backend'
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
    
    }
}
