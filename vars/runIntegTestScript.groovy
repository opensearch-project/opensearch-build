void call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    String jobName = args.jobName ?: 'distribution-build-opensearch'
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))

    String buildId = buildManifest.build.id
    echo "Build Id: ${buildId}"

    String artifactRootUrl = buildManifest.getArtifactRootUrl(jobName, buildId)
    echo "Artifact root URL: ${artifactRootUrl}"

    String localPath = args.localPath ?: 'None'
    String paths = generatePaths(buildManifest, artifactRootUrl, localPath)
    echo "Paths: ${paths}"

    String component = args.componentName
    echo "Component: ${component}"

    sh([
        './test.sh',
        'integ-test',
        "${args.testManifest}",
        "--component ${component}",
        "--test-run-id ${env.BUILD_NUMBER}",
        "--paths ${paths}",
    ].join(' '))
}

String generatePaths(buildManifest, artifactRootUrl, localPath) {
    String name = buildManifest.build.name
    String version = buildManifest.build.version
    String platform = buildManifest.build.platform
    String architecture = buildManifest.build.architecture
    String distribution = buildManifest.build.distribution
    
    String latestOpenSearchArtifactRootUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/${version}/latest/${platform}/${architecture}/${distribution}"
    if (localPath.equals('None')) {
        echo "No localPath found, download from url"
        return name == 'OpenSearch' ? 
            "opensearch=${artifactRootUrl}" :
            "opensearch=${latestOpenSearchArtifactRootUrl} opensearch-dashboards=${artifactRootUrl}"
    }
    else {
        echo "User provides localPath, use local artifacts: ${localPath}"
        return name == 'OpenSearch' ?
            "opensearch=${localPath}" :
            "opensearch=${localPath} opensearch-dashboards=${localPath}"
    }
}
