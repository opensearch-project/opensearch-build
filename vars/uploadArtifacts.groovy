void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.manifest))
    def fileLocation = buildManifest.components.get("OpenSearch").artifacts.get("dist").first()
    def productName = buildManifest.build.getFilename()
    def fileName = buildManifest.build.getPackageName()

    def artifactPath = buildManifest.getArtifactRoot("${JOB_NAME}", "${BUILD_NUMBER}")
    echo "Uploading to s3://${ARTIFACT_BUCKET_NAME}/${artifactPath}"

    uploadToS3(
            sourcePath: 'builds',
            bucket: "${ARTIFACT_BUCKET_NAME}",
            path: "${artifactPath}/builds"
    )

    uploadToS3(
            sourcePath: 'dist',
            bucket: "${ARTIFACT_BUCKET_NAME}",
            path: "${artifactPath}/dist"
    )

    echo "Uploading to s3://${ARTIFACT_PRODUCTION_BUCKET_NAME}/${artifactPath}"

    withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Upload(file: "builds/${productName}/${fileLocation}", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "builds/test-release-candidates/core/${productName}/${buildManifest.build.version}/")
        s3Upload(file: "dist/${productName}/${fileName}", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "builds/test-release-candidates/bundle/${productName}/${buildManifest.build.version}/")
    }

    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", [
            "${baseUrl}/builds/${productName}/manifest.yml",
            "${baseUrl}/dist/${productName}/manifest.yml"
        ].join('\n')
    )
}
