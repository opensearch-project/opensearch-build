void call(Map args = [:]){

    res = sh(script: "test -f /usr/local/bin/gcrane && echo '1' || echo '0' ", returnStdout: true).trim()
    if(res == '0') {
        install_gcrane()
    }

    sh "docker logout"

    if(args.destinationType == 'docker'){
        withCredentials([usernamePassword(credentialsId: args.destinationCredentialIdentifier, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            sh """
                docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                gcrane cp ${args.sourceImagePath} ${args.destinationImagePath}
            """
        }
    } else if(args.destinationType == 'ecr'){
        withAWS(role: 'Upload_ECR_Image', roleAccount: "${args.accountName}", duration: 900, roleSessionName: 'jenkins-session') {
            sh """
                aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${args.destinationCredentialIdentifier}
                gcrane cp ${args.sourceImagePath} ${args.destinationImagePath}
            """
        }
    }
}

void install_gcrane(){
    sh'''
        curl -L https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz \\
            -o go-containerregistry.tar.gz
        tar -zxvf go-containerregistry.tar.gz
        chmod +x gcrane
        mv gcrane /usr/local/bin/
      '''
}
