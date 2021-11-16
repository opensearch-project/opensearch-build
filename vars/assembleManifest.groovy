void call(Map args = [:]) {
    lib = library(identifier: "jenkins@current", retriever: legacySCM(scm)).jenkins
    def manifestFilename = args.manifest ?: 'builds/manifest.yml'
    def buildManifest = lib.BuildManifest.new(readYaml(file: manifestFilename))
    def baseUrl = buildManifest.getArtifactRootUrl(env.PUBLIC_ARTIFACT_URL, env.JOB_NAME, env.BUILD_NUMBER)
    sh ([
        args.script ?: './assemble.sh',
        "\"${manifestFilename}\"",
        "--base-url ${baseUrl}"
    ].join(' '))
}