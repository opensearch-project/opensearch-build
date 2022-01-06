void call(Map args = [:]) {
    String jobName = args.jobName ?: 'distribution-build-opensearch'
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))
    String artifactRootUrl = buildManifest.getArtifactRootUrl("${jobName}", "${env.BUILD_ID}")
    echo "Artifact root URL: ${artifactRootUrl}"
    
    sh([
        './test.sh',
        'integ-test',
        "${args.testManifest}",
        "--paths opensearch=${artifactRootUrl}",
        "--test-run-id ${env.BUILD_NUMBER}"
    ].join(' '))
}