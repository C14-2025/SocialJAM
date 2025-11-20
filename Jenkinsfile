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
                    npm install --legacy-peer-deps --no-audit --prefer-offline
                    '''
                    }
            }
        }
    
    }
    
}