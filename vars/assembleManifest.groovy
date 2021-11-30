void call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    String manifestFilename = args.manifest ?: 'builds/opensearch/manifest.yml'
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: manifestFilename))
    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    sh ([
        args.dryRun ? 'echo ./assemble.sh' : './assemble.sh',
        "\"${manifestFilename}\"",
        "--base-url ${baseUrl}"
    ].join(' '))
}
