void call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))
    
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifestFileName))

    String buildId = buildManifest.build.id
    echo "Build Id: ${buildId}"

    def artifactPath = buildManifest.getArtifactRoot(args.jobName, buildId)
    echo "Uploading to s3://${ARTIFACT_BUCKET_NAME}/${artifactPath}"

    withAWS(role: 'opensearch-test', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Upload(file: 'test-results', bucket: "${ARTIFACT_BUCKET_NAME}", path: "${artifactPath}/test-results")
    }

    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", args.jobName, args.buildNumber)
    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "${baseUrl}/test-results/")
}
