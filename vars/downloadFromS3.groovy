void call(Map args = [:]) {
    withCredentials([string(credentialsId: 'jenkins-aws-account-public', variable: 'AWS_ACCOUNT_PUBLIC')]) {
            withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
                s3Download(file: args.destPath, bucket: args.bucket, path: args.path, force: args.force)
            }
    }
}
