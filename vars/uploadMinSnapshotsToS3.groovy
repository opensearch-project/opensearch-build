void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    version = inputManifest.build.version
    architecture = inputManifest.build.architecture
    platform = inputManifest.build.platform
    minArtifactName = opensearch-min-${version}-SNAPSHOT-${platform}-${architecture}-latest.tar.gz


    withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Upload(file: "$WORKSPACE/builds/opensearch/dist/", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "builds/test-release-candidates/snapshots/core/opensearch/${version}-SNAPSHOT/${minArtifactName}")
        }
}