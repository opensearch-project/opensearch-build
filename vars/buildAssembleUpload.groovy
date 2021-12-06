void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def sha = getManifestSHA(args)

    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: sha.lock))

    buildManifest(
        args + [
            manifest: sha.lock
        ]
    )

    assembleUpload(
        args + [
            manifest: "builds/${inputManifest.build.getFilename()}/manifest.yml",
            sha: sha
        ]
    )
}
