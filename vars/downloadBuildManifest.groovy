def call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))

    sh "curl -sSL ${args.url} --output ${args.path}"
    def buildManifestObj = lib.jenkins.BuildManifest.new(readYaml(file: args.path))
    return buildManifestObj
}