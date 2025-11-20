pipeline {

    agent any

    stages {

        stage("POR FAVOR FUNCIONA"){
            steps{
                echo 'PFV'
            }
        }

        stage('Checando se instalou o npm')
            steps{
                sh '''
                node -v
                npm -v
                '''
            }
    
    }
    
}