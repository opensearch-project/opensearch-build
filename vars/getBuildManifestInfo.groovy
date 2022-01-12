String[] call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))
    String buildManifestUrl = args.buildManifestUrl ?: BUILD_MANIFEST_URL

    String buildManifestPath = 'manifest.yml'
    sh "wget ${buildManifestUrl} -O ${buildManifestPath}"
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: buildManifestPath))
    String buildId = buildManifest.getArtifactBuildId()

    echo "buildManifestPath: ${buildManifestPath}"
    echo "buildId: ${buildId}"

    return [buildManifestPath, buildId]
}