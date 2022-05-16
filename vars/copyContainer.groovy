/**@
 * Copies a container from one docker registry to another
 *
 * @param args A map of the following parameters
 * @param args.sourceImagePath The url to the image to be copied from, supports any public docker registry
 * @param args.destinationImagePath Follows the format NAME[:TAG|@DIGEST], e.g. opensearchproject/opensearch:1.2.4
 * @param args.destinationType The docker registry, currently supports 'docker' or 'ecr'
 * @param args.destinationCredentialIdentifier The credential identifier registered in the jenkins system associated with the NAME
 * @param args.accountName Only used for the 'ecr' registry, the AWS role to assume
 */
void call(Map args = [:]) {
    res = sh(script: "test -f /usr/local/bin/gcrane && echo '1' || echo '0' ", returnStdout: true).trim()
    if (res == '0') {
        install_gcrane()
    }

    sh 'docker logout'

    if (args.destinationType == 'docker') {
        withCredentials([usernamePassword(credentialsId: args.destinationCredentialIdentifier, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            sh """
                docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                gcrane cp ${args.sourceImagePath} ${args.destinationImagePath}
            """
        }
    } else if (args.destinationType == 'ecr') {
        withAWS(role: 'Upload_ECR_Image', roleAccount: "${args.accountName}", duration: 900, roleSessionName: 'jenkins-session') {
            sh """
                aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${args.destinationCredentialIdentifier}
                gcrane cp ${args.sourceImagePath} ${args.destinationImagePath}
            """
        }
    }
}

void install_gcrane() {
    sh'''
        curl -L https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz \\
            -o go-containerregistry.tar.gz
        tar -zxvf go-containerregistry.tar.gz
        chmod +x gcrane
        mv gcrane /usr/local/bin/
      '''
}
