void call(Map args = [:]) {
    def latestBuildData = ['latest': "${BUILD_NUMBER}"]
    writeJSON file: 'index.json', json: latestBuildData

    withCredentials([string(credentialsId: 'jenkins-artifact-bucket-name', variable: 'ARTIFACT_BUCKET_NAME')]) {
        echo "Uploading index.json to s3://${ARTIFACT_BUCKET_NAME}/${args.indexFilePath}"

        uploadToS3(
            sourcePath: 'index.json',
            bucket: "${ARTIFACT_BUCKET_NAME}",
            path: "${args.indexFilePath}/index.json"
        )
    }
}
