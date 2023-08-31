node { 
    withCredentials([[$class: 'UsernamePasswordMultiBinding', 
        credentialsId: 'docker-hub', 
        usernameVariable: 'DOCKER_USER_ID', 
        passwordVariable: 'DOCKER_USER_PASSWORD']]) 
    { 
     stage('Pull') {
           git branch: 'main', url: 'https://github.com/YeonjiKim0316/flask_0711_1/'
        }
        

      stage('Build') {
            sh(script: 'sudo docker build -t flask_app2 .')
        }

      stage('Tag') {
              sh(script: '''sudo docker tag flask_app2 ${DOCKER_USER_ID}/flask_app2:${BUILD_NUMBER}''') 
            }

      stage('Push') {
           
            sh(script: 'sudo docker login -u ${DOCKER_USER_ID} -p ${DOCKER_USER_PASSWORD}') 

            sh(script: 'sudo docker push ${DOCKER_USER_ID}/flask_app2:${BUILD_NUMBER}') 
        }
      
      stage('Deploy') {
            sshagent(credentials: ['yeonji-jenkins-ec2-key']) {
                sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@13.125.156.5
                    ssh ubuntu@13.125.156.5 "sudo docker stop -f $(docker ps -qa)""
                    ssh ubuntu@13.125.156.5 "sudo docker rm -f $(docker ps -qa)"
                    ssh ubuntu@13.125.156.5 "sudo docker run --name docker_flask --env-file .env -e TZ=Asia/Seoul -p 80:80 -d -t \$DOCKER_USER_ID/flask_app2:\$BUILD_NUMBER"
                '''
        }
    }

    stage('Cleaning up') { 
              sh "sudo docker rmi ${DOCKER_USER_ID}/flask_app2:${BUILD_NUMBER}" // sudo docker image 제거
      } 
    }
  }
