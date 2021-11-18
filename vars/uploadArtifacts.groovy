void call(Map args = [:]) {
    lib = library(identifier: "jenkins@20211118", retriever: legacySCM(scm))

    def manifestFilename = args.manifest ?: 'builds/manifest.yml'
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: manifestFilename))

    def artifactPath = buildManifest.getArtifactRoot("${JOB_NAME}", "${BUILD_NUMBER}")
    echo "Uploading to s3://${ARTIFACT_BUCKET_NAME}/${artifactPath}"

    withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        if (args.upload) {
            s3Upload(file: 'builds', bucket: "${ARTIFACT_BUCKET_NAME}", path: "${artifactPath}/builds")
            s3Upload(file: 'dist', bucket: "${ARTIFACT_BUCKET_NAME}", path: "${artifactPath}/dist")
        } else {
            echo "s3Upload(file: 'builds', bucket: ${ARTIFACT_BUCKET_NAME}, path: ${artifactPath}/builds)"
            echo "s3Upload(file: 'dist', bucket: ${ARTIFACT_BUCKET_NAME}, path: ${artifactPath}/dist)"
        }
    }

    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", [
            "${baseUrl}/builds/manifest.yml",
            "${baseUrl}/dist/manifest.yml"
        ].join("\n")
    )
}