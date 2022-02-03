void call(Map args = [:]){

    withAWS(role: "${ARTIFACT_UPLOAD_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Upload(file: args.sourcePath, bucket: args.bucket, path: args.path)
    }

}
