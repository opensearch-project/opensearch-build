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

    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))

    assembleUpload(
        args + [
            manifest: "builds/${inputManifest.build.getFilename()}/manifest.yml",
        ]
    )
}
