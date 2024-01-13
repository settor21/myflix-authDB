pipeline {
    agent any

    environment {
        PROD_USERNAME = 'amedikusettor'
        PROD_SERVER = '34.121.116.117'
        PROD_DIR = '/home/amedikusettor/myflix/auth-db'
        DOCKER_IMAGE_NAME = 'auth-db-deployment'
        DOCKER_CONTAINER_NAME = 'auth-db'
        DOCKER_CONTAINER_PORT = '6000'
        DOCKER_HOST_PORT = '6000'
    }

    stages {
        stage('Load Code to Workspace') {
            steps {
                checkout scm             
            }
        }

        stage('Deploy Repo to Prod. Server') {
            steps {
                script {
                    sh 'echo Packaging files ...'
                    sh 'tar -czf authdb_files.tar.gz *'
                    sh "scp -o StrictHostKeyChecking=no authdb_files.tar.gz ${PROD_USERNAME}@${PROD_SERVER}:${PROD_DIR}"
                    sh 'echo Files transferred to server. Unpacking ...'
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'pwd && cd myflix/auth-db && tar -xzf authdb_files.tar.gz && ls -l'"
                    sh 'echo Repo unloaded on Prod. Server. Preparing to dockerize application ..'
                }
            }
        }

        stage('Dockerize DB Application') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/auth-db && docker build -t ${DOCKER_IMAGE_NAME} .'"
                    sh "echo Docker image for authDB rebuilt. Preparing to redeploy container to web..."
                }
            }
        }

        stage('Redeploy Container') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/auth-db && docker stop ${DOCKER_CONTAINER_NAME} || true'"
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/auth-db && docker rm ${DOCKER_CONTAINER_NAME} || true'"
                    sh "echo Container stopped and removed. Preparing to redeploy new version"

                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/auth-db && docker run -d -p ${DOCKER_HOST_PORT}:${DOCKER_CONTAINER_PORT} --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_NAME}'"
                    sh "echo authDB Microservice Deployed!"
                }
            }
        }
    }
}
