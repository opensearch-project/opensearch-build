void call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))

    def manifestFilename = args.dryRun ? 'tests/data/opensearch-build-1.1.0.yml' : 'builds/opensearch/manifest.yml'
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: manifestFilename))

    def artifactPath = buildManifest.getArtifactRoot("${JOB_NAME}", "${BUILD_NUMBER}")
    echo "Uploading to s3://${ARTIFACT_BUCKET_NAME}/${artifactPath}"

    withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        if (!args.dryRun) {
            s3Upload(file: 'builds', bucket: "${ARTIFACT_BUCKET_NAME}", path: "${artifactPath}/builds")
            s3Upload(file: 'dist', bucket: "${ARTIFACT_BUCKET_NAME}", path: "${artifactPath}/dist")
        } else {
            echo "s3Upload(file: 'builds', bucket: ${ARTIFACT_BUCKET_NAME}, path: ${artifactPath}/builds)"
            echo "s3Upload(file: 'dist', bucket: ${ARTIFACT_BUCKET_NAME}, path: ${artifactPath}/dist)"
        }
    }

    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", [
            "${baseUrl}/builds/opensearch/manifest.yml",
            "${baseUrl}/dist/opensearch/manifest.yml"
        ].join('\n')
    )
}
