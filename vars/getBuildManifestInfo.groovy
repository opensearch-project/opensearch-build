Map call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))
    String buildManifestUrl = args.buildManifestUrl ?: BUILD_MANIFEST_URL

    String BUILD_MANIFEST = 'manifest.yml'
    sh "wget ${buildManifestUrl} -O ${BUILD_MANIFEST}"
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: BUILD_MANIFEST))
    String BUILD_ID = buildManifest.getArtifactBuildId()

    echo "BUILD_MANIFEST: ${BUILD_MANIFEST}"
    echo "BUILD_ID: ${BUILD_ID}"

    return [BUILD_MANIFEST, BUILD_ID]
}