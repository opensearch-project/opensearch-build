def call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def inputManifestObj = lib.jenkins.InputManifest.new(readYaml(file: args.inputManifest))

    echo "Assembling ${args.inputManifest}"

    copyArtifacts(
        filter: "${args.distribution}/*.zip",
        fingerprintArtifacts: true,
        projectName: "${JOB_NAME}",
        selector: specific("${BUILD_NUMBER}")
    )

    unzip(zipFile: "${args.distribution}/archived-builds.zip")

    String buildManifest = "${args.distribution}/builds/${inputManifestObj.build.getFilename()}/manifest.yml"
    def buildManifestObj = lib.jenkins.BuildManifest.new(readYaml(file: buildManifest))

    assembleUpload(
        args + [
            buildManifest: buildManifest,
        ]
    )

    return buildManifestObj
}
