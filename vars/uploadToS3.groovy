void call(Map args = [:]){

    withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Upload(file: args.sourcePath, bucket: args.bucket, path: args.path)
    }

}
