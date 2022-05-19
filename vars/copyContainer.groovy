/**@
 * Copies a container from one docker registry to another
 *
 * @param args A map of the following parameters
 * @param args.sourceImage The url to the image to be copied from, supports any public docker registry
 * @param args.destinationImage Follows the format NAME[:TAG|@DIGEST], e.g. opensearchproject/opensearch:1.2.4
 * @param args.destinationRegistry The docker registry, currently supports 'docker' or 'ecr'
 * @param args.prod (true/false) to choose between production and staging environments
 */
void call(Map args = [:]) {


    if (args.destinationRegistry == 'opensearchstaging' || args.destinationRegistry == 'opensearchproject') {
        def dockerJenkinsCredential = args.destinationRegistry == 'opensearchproject' ? "jenkins-staging-docker-prod-token" : "jenkins-staging-docker-staging-credential"
        withCredentials([usernamePassword(credentialsId: dockerJenkinsCredential, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            def dockerLogin = sh(returnStdout: true, script: "echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin").trim()
            sh """
                gcrane cp ${args.sourceImage} ${args.destinationImage}
                docker logout
            """
        }
    }
    if (args.destinationRegistry == 'public.ecr.aws/opensearchproject') {
        withCredentials([
            string(credentialsId: 'jenkins-artifact-promotion-role', variable: 'ARTIFACT_PROMOTION_ROLE_NAME'),
            string(credentialsId: 'jenkins-artifact-promotion-account', variable: 'AWS_ACCOUNT_ARTIFACT')]) 
            {
                withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
                    def ecrLogin = sh(returnStdout: true, script: "aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${args.destinationRegistry}").trim()
                    sh """
                        gcrane cp ${args.sourceImage} ${args.destinationImage}
                        docker logout ${args.destinationRegistry}
                    """
                }
            }
    }
    if(args.destinationRegistry == 'public.ecr.aws/opensearchstaging') {
            def ecrLogin = sh(returnStdout: true, script: "aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${args.destinationRegistry}").trim()
            sh """
                 gcrane cp ${args.sourceImage} ${args.destinationImage}
                 docker logout ${args.destinationRegistry}
            """
    }
}