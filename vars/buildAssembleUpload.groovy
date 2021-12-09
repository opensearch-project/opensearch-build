void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"

    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))

    buildManifest(args)

    assembleUpload(
        args + [
            manifest: "builds/${inputManifest.build.getFilename()}/manifest.yml",
        ]
    )
}
