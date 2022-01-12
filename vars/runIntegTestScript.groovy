void call(Map args = [:]) {
    // TODO: put this back to 'distribution-build-opensearch' once 
    String jobName = args.jobName ?: 'Playground/ohltyler-distribution-build-opensearch'
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))
    String artifactRootUrl = buildManifest.getArtifactRootUrl(jobName, args.buildId)
    echo "Artifact root URL: ${artifactRootUrl}"
    
    sh([
        './test.sh',
        'integ-test',
        "${args.testManifest}",
        "--paths opensearch=${artifactRootUrl}",
    ].join(' '))
}