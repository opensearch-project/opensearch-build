/**@
 * Copies a container from one docker registry to another
 *
 * @param args A map of the following parameters
 * @param args.sourceImagePath The url to the image to be copied from, supports any public docker registry
 * @param args.destinationImagePath Follows the format NAME[:TAG|@DIGEST], e.g. opensearchproject/opensearch:1.2.4
 * @param args.destinationType The docker registry, currently supports 'docker' or 'ecr'
 * @param args.destinationCredentialIdentifier The credential identifier registered in the jenkins system associated with the NAME
 * @param args.ecrProd (true/false) to choose between production and staging environments
 */
void call(Map args = [:]) {

    if (args.destinationType == 'docker') {
        withCredentials([usernamePassword(credentialsId: args.destinationCredentialIdentifier, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            sh """
                docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                gcrane cp ${args.sourceImagePath} ${args.destinationImagePath}
                docker logout
            """
        }
    }
    if (args.destinationType == 'ecr') {
        if(args.ecrProd) {
            withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
            sh """
                aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${args.destinationCredentialIdentifier}
                gcrane cp ${args.sourceImagePath} ${args.destinationImagePath}
            """
            }
        }
        if(!args.ecrProd) {
            sh """
                aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${args.destinationCredentialIdentifier}
                gcrane cp ${args.sourceImagePath} ${args.destinationImagePath}
            """
        }
    }
    sh "docker logout ${args.destinationCredentialIdentifier}"
}
