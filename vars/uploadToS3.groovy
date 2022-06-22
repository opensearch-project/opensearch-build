void call(Map args = [:]){

    withCredentials([string(credentialsId: 'AWS_ACCOUNT_PUBLIC', variable: 'aws_account_public')]) {
        withAWS(role: 'opensearch-bundle', roleAccount: "${aws_account_public}", duration: 900, roleSessionName: 'jenkins-session') {
            s3Upload(file: args.sourcePath, bucket: args.bucket, path: args.path)
        }
    }
}
