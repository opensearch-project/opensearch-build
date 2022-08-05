/**@
 * Copies a container from one docker registry to another
 *
 * @param args A map of the following parameters
 * @param args.sourceImage The Source Image name and tag <IMAGE_NAME>:<IMAGE_TAG> Eg: opensearch:1.3.2
 * @param args.sourceRegistry The source docker registry, currently supports 'DockerHub' or 'ECR'
 * @param args.destinationImage The Destination Image name and tag <IMAGE_NAME>:<IMAGE_TAG> Eg: opensearch:1.3.2
 * @param args.destinationRegistry The destination docker registry, currently supports 'DockerHub' or 'ECR'
 */
void call(Map args = [:]) {


    if (args.destinationRegistry == 'opensearchstaging' || args.destinationRegistry == 'opensearchproject') {
        def dockerJenkinsCredential = args.destinationRegistry == 'opensearchproject' ? "jenkins-production-dockerhub-credential" : "jenkins-staging-dockerhub-credential"
        withCredentials([usernamePassword(credentialsId: dockerJenkinsCredential, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            def dockerLogin = sh(returnStdout: true, script: "echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin").trim()
            sh """
                gcrane cp ${args.sourceRegistry}/${args.sourceImage} ${args.destinationRegistry}/${args.destinationImage}
                docker logout
            """
        }
    }
    if (args.destinationRegistry == 'public.ecr.aws/opensearchproject') {
        withCredentials([
            string(credentialsId: 'jenkins-artifact-promotion-role', variable: 'ARTIFACT_PROMOTION_ROLE_NAME'),
            string(credentialsId: 'jenkins-aws-production-account', variable: 'AWS_ACCOUNT_ARTIFACT')]) 
            {
                withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
                    def ecrLogin = sh(returnStdout: true, script: "aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${args.destinationRegistry}").trim()
                    sh """
                        gcrane cp ${args.sourceRegistry}/${args.sourceImage} ${args.destinationRegistry}/${args.destinationImage}
                        docker logout ${args.destinationRegistry}
                    """
                }
            }
    }
    if(args.destinationRegistry == 'public.ecr.aws/opensearchstaging') {
            def ecrLogin = sh(returnStdout: true, script: "aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${args.destinationRegistry}").trim()
            sh """
                 gcrane cp ${args.sourceRegistry}/${args.sourceImage} ${args.destinationRegistry}/${args.destinationImage}
                 docker logout ${args.destinationRegistry}
            """
    }
}