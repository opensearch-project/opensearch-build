void call(Map args = [:]) {
    String jobName = args.jobName ?: 'distribution-build-opensearch'
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.bundleManifest))
    String artifactRootUrl = buildManifest.getArtifactRootUrl(jobName, args.buildId)

    install_npm()
    install_dependencies()
    install_opensearch_infra_dependencies()
    withAWS(role: 'opensearch-test', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Download(file: "config.yml", bucket: "${ARTIFACT_BUCKET_NAME}", path: "${PERF_TEST_CONFIG_LOCATION}/config.yml", force: true)
    }

    sh([
        './test.sh',
        'perf-test',
        args.security ? "--stack test-single-security-${args.buildId}" :
        "--stack test-single-${args.buildId}",
        "--bundle-manifest ${args.bundleManifest}",
        "--config config.yml",
        args.security ? "--security" : ""
    ].join(' '))
}

void install_opensearch_infra_dependencies() {
    sh'''
        pipenv install "dataclasses_json~=0.5" "aws_requests_auth~=0.4" "json2html~=1.3.0"
        pipenv install "aws-cdk.core~=1.143.0" "aws_cdk.aws_ec2~=1.143.0" "aws_cdk.aws_iam~=1.143.0"
        pipenv install "boto3~=1.18" "setuptools~=57.4" "retry~=0.9"
    '''
}

void install_npm(){
    sh'''
        sudo yum install -y gcc-c++ make
        curl -sL https://rpm.nodesource.com/setup_16.x | sudo -E bash -
        sudo yum install -y nodejs --enablerepo=nodesource
        node -v
      '''
}

void install_dependencies() {
    sh '''
        sudo npm install -g aws-cdk
        sudo npm install -g cdk-assume-role-credential-plugin
    '''
}