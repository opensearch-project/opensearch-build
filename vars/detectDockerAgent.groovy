Map call(Map args = [:]) {
    git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    dockerImage = inputManifest.ci.image.name
    dockerArgs = inputManifest.ci.image.args
    echo "Using Docker image ${dockerImage} (${dockerArgs})"
    return [
        image: dockerImage,
        args: dockerArgs
    ]
}