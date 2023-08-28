pipeline {
  agent any
   
  stages { 
     stage('Pull') {
         steps {
            git branch: 'main', url: 'https://github.com/YeonjiKim0316/flask_0711_1'
        }
        post {
            failure {
              echo 'Repository clone failure !'
            }
            success {
              echo 'Repository clone success !'
            }
        }
    }
           
      stage('Unit Test') {

      }

      stage('Build') {

            sh(script: 'docker build -t flask_app2 .')

      }

      stage('Tag') {
         withCredentials([[$class: 'UsernamePasswordMultiBinding',
                   credentialsId: 'docker-hub',
                   usernameVariable: 'DOCKER_USER_ID', 
                   passwordVariable: 'DOCKER_USER_PASSWORD']]) 

            sh(script: '''docker tag ${DOCKER_USER_ID}/flask_app2 \

            ${DOCKER_USER_ID}/flask:${BUILD_NUMBER}''') 
            }

      stage('Push') {

            sh(script: 'docker login -u ${DOCKER_USER_ID} -p ${DOCKER_USER_PASSWORD}') 

            sh(script: 'docker push ${DOCKER_USER_ID}/flask_app2:${BUILD_NUMBER}') 

            sh(script: 'docker push ${DOCKER_USER_ID}/flask_app2:latest')

      }
      
      stage('Deploy') {
            steps {
            sshagent(credentials: ['yeonji-jenkins-ec2-key']) {
                sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@3.34.183.240
                    scp -r /var/lib/jenkins/workspace/flask-app-from-dockerhub ubuntu@3.34.183.240:/home/ubuntu
                    ssh ubuntu@3.34.183.240 'sudo docker run --env-file .env -e TZ=Asia/Seoul -p 80:80 -d -t  ${DOCKER_USER_ID}/flask_app2:latest') 
                '''
            }
        }
    }

    stage('Cleaning up') { 
          steps { 
              sh "docker rmi ${DOCKER_USER_ID}/flask_app2:latest" // docker image 제거
          }
      } 
    }
  }

