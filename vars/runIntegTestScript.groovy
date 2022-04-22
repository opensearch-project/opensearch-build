void call(Map args = [:]) {
    String jobName = args.jobName ?: 'distribution-build-opensearch'
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))
    String artifactRootUrl = buildManifest.getArtifactRootUrl(jobName, args.buildId)
    echo "Artifact root URL: ${artifactRootUrl}"

    String paths = generatePaths(buildManifest, artifactRootUrl)
    echo "Paths: ${paths}"

    sh([
        './test.sh',
        'integ-test',
        "${args.testManifest}",
        '--test-run-id 1',
        "--paths ${paths}",
    ].join(' '))
}

String generatePaths(buildManifest, artifactRootUrl) {
    String name = buildManifest.build.name
    String version = buildManifest.build.version
    String platform = buildManifest.build.platform
    String architecture = buildManifest.build.architecture
    
    // only support tar for now. will use parameter for distribution in https://github.com/opensearch-project/opensearch-build/issues/1857
    String latestOpenSearchArtifactRootUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/${version}/latest/${platform}/${architecture}/tar"
    return name == 'OpenSearch' ? 
        "opensearch=${artifactRootUrl}" :
        "opensearch=${latestOpenSearchArtifactRootUrl} opensearch-dashboards=${artifactRootUrl}"
}