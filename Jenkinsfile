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
                sh '''
                node -v
                npm -v
                cd front
                npm install
                '''
            }
        }
    
    }
    
}