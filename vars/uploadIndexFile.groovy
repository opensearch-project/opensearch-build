void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    def inputManifestObj = lib.jenkins.InputManifest.new(readYaml(file: args.inputManifest))
    String buildManifest = "${args.distribution}/builds/${inputManifestObj.build.getFilename()}/manifest.yml"
    def buildManifestObj = lib.jenkins.BuildManifest.new(readYaml(file: buildManifest))

    def indexFilePath = buildManifestObj.getIndexFileRoot("${JOB_NAME}")
    def latestBuildData = ['latest': "${BUILD_NUMBER}"]
    writeJSON file: 'index.json', json: latestBuildData

    echo "Uploading index.json to s3://${ARTIFACT_PRODUCTION_BUCKET_NAME}/${indexFilePath}"

    uploadToS3(
            sourcePath: 'index.json',
            bucket: "${ARTIFACT_BUCKET_NAME}",
            path: "${indexFilePath}/index.json"
    )
}