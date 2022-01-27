void call(Map args = [:]){

    withAWS(role: "${ARTIFACT_DOWNLOAD_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Download(file: args.destPath, bucket: args.bucket, path: args.path, force: args.force)
    }

}
