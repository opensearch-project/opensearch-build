void call(Map args = [:]){

    if(args.destinationType == 'docker'){
        withCredentials([usernamePassword(credentialsId: args.destinationCredentialIdentifier, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            sh """
                set -ex
                echo Login to $CREDENTIAL_ID
                docker logout && docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                gcrane cp ${args.sourceImagePath} ${args.destinationImagePath}
            """
        }
    } else if(args.destinationType == 'ecr'){
        withAWS(role: 'Upload_ECR_Image', roleAccount: "${args.accountName}", duration: 900, roleSessionName: 'jenkins-session') {
            sh """
                docker logout
                aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${args.destinationCredentialIdentifier}
                gcrane cp ${args.sourceImagePath} ${args.destinationImagePath}
            """
        }
    }

}
