void call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))
    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    sh([
        './assemble.sh',
        "\"${args.buildManifest}\"",
        "--base-url ${baseUrl}"
    ].join(' '))
}
