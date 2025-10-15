pipeline {
  agent any

  environment {
    REPO = 'https://github.com/Ar-Aros/flask-deploy-demo'   // your repo
    REMOTE = 'ubuntu@13.126.212.118'                            // docker server
    CRED_ID = 'docker-server-ssh'                               // credential id in Jenkins
    APP_DIR = 'flask-deploy-demo'                              // remote clone dir name
    IMAGE = 'flask-deploy-demo'
    CONTAINER = 'flask-deploy-demo'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout([$class: 'GitSCM',
    branches: [[name: '*/main']],
    userRemoteConfigs: [[url: env.REPO]],
    extensions: [[$class: 'WipeWorkspace']]
])

      }
    }

    stage('Deploy to remote Docker host') {
      steps {
        sshagent (credentials: [env.CRED_ID]) {
          sh """
            ssh -o StrictHostKeyChecking=no ${env.REMOTE} bash -l -c '
              set -e
              cd /home/ubuntu
              if [ -d "${env.APP_DIR}" ]; then rm -rf "${env.APP_DIR}"; fi
              git clone ${env.REPO} ${env.APP_DIR}
              cd ${env.APP_DIR}
              # stop & remove existing container
              if docker ps -a --format "{{.Names}}" | grep -Eq "^${env.CONTAINER}\$"; then
                docker stop ${env.CONTAINER} || true
                docker rm ${env.CONTAINER} || true
              fi
              # build and run (maps host port 5000 -> container 5000)
              docker build -t ${env.IMAGE} .
              docker run -d -p 5000:5000 --name ${env.CONTAINER} ${env.IMAGE}
            '
          """
        }
      }
    }
  }

  post {
    failure { echo "Deployment failed" }
    success { echo "Deployment succeeded" }
  }
}
