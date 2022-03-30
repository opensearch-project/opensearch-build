void call(Map args = [:]) {
    def latestBuildData = ['latest': "${BUILD_NUMBER}"]
    writeJSON file: 'index.json', json: latestBuildData

    echo "Uploading index.json to s3://${ARTIFACT_PRODUCTION_BUCKET_NAME}/${args.indexFilePath}"

    uploadToS3(
            sourcePath: 'index.json',
            bucket: "${ARTIFACT_BUCKET_NAME}",
            path: "${args.indexFilePath}/index.json"
    )
}