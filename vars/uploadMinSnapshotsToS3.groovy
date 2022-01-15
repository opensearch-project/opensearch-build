void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    echo("Retreving build manifest from: $WORKSPACE/builds/${inputManifest.build.getFilename()}/manifest.yml")
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: "$WORKSPACE/builds/${inputManifest.build.getFilename()}/manifest.yml"))
    version = buildManifest.build.version
    architecture = buildManifest.build.architecture
    platform = buildManifest.build.platform
    minArtifactSourceName = "opensearch-min-${version}-${platform}-${architecture}.tar.gz"
    minArtifactName = "opensearch-min-${version}-${platform}-${architecture}-latest.tar.gz"
    withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Upload(file: "$WORKSPACE/builds/opensearch/dist/${minArtifactSourceName}", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "snapshots/core/opensearch/${version}/${minArtifactName}")
    }
}
