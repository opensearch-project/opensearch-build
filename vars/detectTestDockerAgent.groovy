Map call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))
    String manifest = args.testManifest ?: "manifests/${TEST_MANIFEST}"
    def testManifest = lib.jenkins.TestManifest.new(readYaml(file: manifest))
    dockerImage = testManifest.ci?.image?.name ?: 'opensearchstaging/ci-runner:ci-runner-centos7-v1'
    dockerArgs = testManifest.ci?.image?.args
    echo "Using Docker image ${dockerImage} (${dockerArgs})"
    return [
        image: dockerImage,
        args: dockerArgs
    ]
}