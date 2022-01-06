void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.manifest))

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

    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", [
            "${baseUrl}/builds/${buildManifest.build.getFilename()}/manifest.yml",
            "${baseUrl}/dist/${buildManifest.build.getFilename()}/manifest.yml"
        ].join('\n')
    )
}
