void call(Map args = [:]) {
    lib = library(identifier: "jenkins@current", retriever: legacySCM(scm))
    def manifestFilename = args.manifest ?: 'builds/manifest.yml'
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: manifestFilename))
    def baseUrl = buildManifest.getArtifactRootUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    sh ([
        args.script ?: './assemble.sh',
        "\"${manifestFilename}\"",
        "--base-url ${baseUrl}"
    ].join(' '))
}