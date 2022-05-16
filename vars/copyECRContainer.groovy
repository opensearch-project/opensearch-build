/**@
 * Copies a container from one docker registry to another
 *
 * @param args A map of the following parameters
 * @param args.imageRepository The repository name of the product we perform promoting and tagging. E.g.: opensearch
 * @param args.imageTag The image tag from the staging docker repository.
 * @param args.latestTag The boolean parameter of whether tag this staging container with latest in the promoting ECR.
 * @param args.majorVersionTag The boolean parameter of whether tag this staging container with major version of it in the promoting ECR.
 * @param args.minorVersionTag The boolean parameter of whether tag this staging container with major.minor version of it in the promoting ECR.
 */
void call(Map args = [:]) {
    res = sh(script: "test -f /usr/local/bin/gcrane && echo '1' || echo '0' ", returnStdout: true).trim()
    if (res == '0') {
        install_gcrane()
    }

    sh 'docker logout'

    def imageRepository = args.imageRepository
    def imageVersionTag = args.imageTag
    def latestBoolean = args.latestTag
    def majorVersionBoolean = args.majorVersionTag
    def minorVersionBoolean = args.minorVersionTag
    def majorVersion = imageVersionTag.split("\\.").first()
    def minorVersion = imageVersionTag.split("\\.")[1]

    copy_image(imageRepository, imageVersionTag, imageVersionTag)
    if (latestBoolean.toBoolean()) {
        echo("Tagging with latest for this ECR image.")
        copy_image(imageRepository, imageVersionTag, "latest")
    }
    if (majorVersionBoolean.toBoolean()) {
        echo("Tagging with its major version for this ECR image.")
        copy_image(imageRepository, imageVersionTag, majorVersion)
    }
    if (minorVersionBoolean.toBoolean()) {
        echo("Tagging with its major and minor version for this ECR image.")
        copy_image(imageRepository, imageVersionTag, majorVersion + "." + minorVersion)
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

void copy_image(String imageRepository, String imageTag, String destinationTag) {
    def destinationCredentialIdentifier= "public.ecr.aws/p5f6l6i3"
    withAWS(role: 'Upload_ECR_Image', roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
        sh """
               aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin "$destinationCredentialIdentifier"
               gcrane cp opensearchstaging/$imageRepository:$imageTag public.ecr.aws/p5f6l6i3/$imageRepository:$destinationTag
           """
    }
}
