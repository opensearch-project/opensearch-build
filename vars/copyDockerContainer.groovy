/**@
 * Copies a container from one docker registry to another
 *
 * @param args A map of the following parameters
 * @param args.imageRepository The repository name of the product we perform promoting and tagging. E.g.: opensearch
 * @param args.imageTag The image tag from the staging docker repository.
 * @param args.latestTag The boolean parameter of whether tag this staging container with latest in the promoting docker.
 * @param args.majorVersionTag The boolean parameter of whether tag this staging container with major version of it in the promoting docker.
 * @param args.minorVersionTag The boolean parameter of whether tag this staging container with major.minor version of it in the promoting docker.
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
        echo("Tagging with latest for this docker image.")
        copy_image(imageRepository, imageVersionTag, "latest")
    }
    if (majorVersionBoolean.toBoolean()) {
        echo("Tagging with its major version for this docker image.")
        copy_image(imageRepository, imageVersionTag, majorVersion)
    }
    if (minorVersionBoolean.toBoolean()) {
        echo("Tagging with its major and minor version for this docker image.")
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
    withCredentials([usernamePassword(credentialsId: 'jenkins-staging-docker-prod-token', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
        sh """
            docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
            gcrane cp opensearchstaging/$imageRepository:$imageTag opensearchproject/$imageRepository:$destinationTag
        """
    }
}
