def call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def inputManifestObj = lib.jenkins.InputManifest.new(readYaml(file: args.inputManifest))

    String stashName = "build-archive-${args.platform}-${args.architecture}-${args.distribution}-${JOB_NAME}-${BUILD_NUMBER}"
    echo "Unstashing ${stashName} before starting the assemble process"
    unstash "${stashName}"

    echo "Assembling ${args.inputManifest}"

    String buildManifest = "${args.distribution}/builds/${inputManifestObj.build.getFilename()}/manifest.yml"
    def buildManifestObj = lib.jenkins.BuildManifest.new(readYaml(file: buildManifest))

    assembleUpload(
        args + [
            buildManifest: buildManifest,
        ]
    )

    return buildManifestObj
}
