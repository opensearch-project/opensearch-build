void call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    echo "Assembling ${args.manifest}"

    copyArtifacts(
        filter: "*.zip",
        fingerprintArtifacts: true,
        projectName: "${JOB_NAME}",
        selector: specific("${BUILD_NUMBER}")
    )

    unzip(zipFile: "builds.zip")
    unzip(zipFile: "manifest.zip")

    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: args.manifest))

    assembleUpload(
        args + [
            manifest: "builds/${inputManifest.build.getFilename()}/manifest.yml",
        ]
    )
}
