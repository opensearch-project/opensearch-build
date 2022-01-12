void call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"

    echo "Assembling ${manifest}"

    copyArtifacts(
        filter: "*.zip",
        fingerprintArtifacts: true,
        projectName: "${JOB_NAME}",
        selector: specific("${BUILD_NUMBER}")
    )

    unzip(zipFile: "archived-builds.zip")

    def inputManifestObj = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    String buildManifest = "builds/${inputManifestObj.build.getFilename()}/manifest.yml"

    assembleUpload(
        args + [
            buildManifest: buildManifest,
        ]
    )
}
