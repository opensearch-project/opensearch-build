void call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))

    def manifestFilename = args.manifest ?: "manifest.yml"
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: manifestFilename))

    def artifactPath = buildManifest.getArtifactRoot(args.jobName, args.buildNumber)
    echo "Uploading to s3://${ARTIFACT_BUCKET_NAME}/${artifactPath}"

    withAWS(role: 'opensearch-test', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        if (!args.dryRun) {
            s3Upload(file: 'test-results', bucket: "${ARTIFACT_BUCKET_NAME}", path: "${artifactPath}/test-results")
        } else {
            echo "s3Upload(file: 'test-results', bucket: ${ARTIFACT_BUCKET_NAME}, path: ${artifactPath}/test-results)"
        }
    }

    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", args.jobName, args.buildNumber)
    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "${baseUrl}/test-results/")
}
