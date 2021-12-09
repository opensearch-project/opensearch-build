Map call(Map args = [:]) {
    git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    dockerImage = inputManifest.ci?.image?.name ?: 'opensearchstaging/ci-runner:centos7-x64-arm64-jdkmulti-node10.24.1-cypress6.9.1-20211028'
    dockerArgs = inputManifest.ci?.image?.args
    echo "Using Docker image ${dockerImage} (${dockerArgs})"
    return [
        image: dockerImage,
        args: dockerArgs
    ]
}