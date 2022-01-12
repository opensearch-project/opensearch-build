void call(Map args = [:]) {
    git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'
    
    IntegTests: {
        // TODO: will need to override integ-test in Jenkins with the new workflow in jenkins/opensearch/integ-test.jenkinsfile
        build job: 'Playground/ohltyler-integ-test',
        parameters: [
            string(name: 'TEST_MANIFEST', value: args.testManifest),
            string(name: 'BUILD_MANIFEST_URL', value: args.buildManifestUrl),
            string(name: 'AGENT_LABEL', value: args.agentLabel)
        ]
    }
    
}