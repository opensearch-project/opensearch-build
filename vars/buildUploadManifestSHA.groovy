void call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    def sha = getManifestSHA(args)

    withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Upload(bucket: "${ARTIFACT_BUCKET_NAME}", file: sha.lock, path: sha.path)
    }
}