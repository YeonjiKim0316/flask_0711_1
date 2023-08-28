node { 
    git poll: true, url:'https://github.com/YeonjiKim0316/flask_0711_1' 
    withCredentials([[$class: 'UsernamePasswordMultiBinding', 
        credentialsId: 'docker-hub', 
        usernameVariable: 'DOCKER_USER_ID', 
        passwordVariable: 'DOCKER_USER_PASSWORD']]) 
        { 
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

      stage('Build') {
         steps {
            sh(script: 'sudo docker build -t flask_app2 .')
         }
      }

      stage('Tag') {
              sh(script: '''sudo docker tag ${DOCKER_USER_ID}/flask_app2 \
  
              ${DOCKER_USER_ID}/flask:${BUILD_NUMBER}''') 
            }

      stage('Push') {
            withCredentials([[$class: 'UsernamePasswordMultiBinding',
                     credentialsId: 'sudo docker-hub',
                     usernameVariable: 'DOCKER_USER_ID', 
                     passwordVariable: 'DOCKER_USER_PASSWORD']]) 
           
            sh(script: 'sudo docker login -u ${DOCKER_USER_ID} -p ${DOCKER_USER_PASSWORD}') 

            sh(script: 'sudo docker push ${DOCKER_USER_ID}/flask_app2:${BUILD_NUMBER}') 

            sh(script: 'sudo docker push ${DOCKER_USER_ID}/flask_app2:latest')
      }
      
      stage('Deploy') {
            sshagent(credentials: ['yeonji-jenkins-ec2-key']) {
                sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@3.34.183.240
                    scp -r /var/lib/jenkins/workspace/flask-app-from-sudo dockerhub ubuntu@3.34.183.240:/home/ubuntu
                    ssh ubuntu@3.34.183.240 'sudo sudo docker run --env-file .env -e TZ=Asia/Seoul -p 80:80 -d -t  ${DOCKER_USER_ID}/flask_app2:latest') 
                '''
        }
    }

    stage('Cleaning up') { 
              sh "sudo docker rmi ${DOCKER_USER_ID}/flask_app2:latest" // sudo docker image 제거
      } 
    }
  }

