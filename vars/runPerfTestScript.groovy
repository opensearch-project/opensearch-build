void call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.bundleManifest))

    install_dependencies()
    install_opensearch_infra_dependencies()
    config_name = isNullOrEmpty(args.config) ? "config.yml" : args.config
    withAWS(role: 'opensearch-test', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Download(file: "config.yml", bucket: "${ARTIFACT_BUCKET_NAME}", path: "${PERF_TEST_CONFIG_LOCATION}/${config_name}", force: true)
    }

    String stackNameSuffix = isNullOrEmpty(args.stackNameSuffix) ? 'perf-test' : args.stackNameSuffix

    withCredentials([usernamePassword(credentialsId: "${GITHUB_BOT_TOKEN_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
        sh([
            './test.sh',
            'perf-test',
            args.insecure ? "--stack test-single-${args.buildId}-${args.architecture}-${stackNameSuffix}" :
            "--stack test-single-security-${args.buildId}-${args.architecture}-${stackNameSuffix}",
            "--bundle-manifest ${args.bundleManifest}",
            "--config config.yml",
            args.insecure ? "--without-security" : "",
            isNullOrEmpty(args.workload) ? "" : "--workload ${args.workload}",
            isNullOrEmpty(args.testIterations) ? "" : "--test-iters ${args.testIterations}",
            isNullOrEmpty(args.warmupIterations) ? "" : "--warmup-iters ${args.warmupIterations}",
            isNullOrEmpty(args.component) ? "" : "--component ${args.component}"
        ].join(' '))
    }
}

boolean isNullOrEmpty(String str) { return (str == null || str.allWhitespace) }

void install_opensearch_infra_dependencies() {
    sh'''
        pipenv install "dataclasses_json~=0.5" "aws_requests_auth~=0.4" "json2html~=1.3.0"
        pipenv install "aws-cdk.core~=1.143.0" "aws_cdk.aws_ec2~=1.143.0" "aws_cdk.aws_iam~=1.143.0"
        pipenv install "boto3~=1.18" "setuptools~=57.4" "retry~=0.9"
    '''
}

void install_dependencies() {
    sh '''
        npm install -g fs-extra
        npm install -g chalk@4.1.2
        npm install -g @aws-cdk/cloudformation-diff
        npm install -g aws-cdk
        npm install -g cdk-assume-role-credential-plugin@1.4.0
    '''
}