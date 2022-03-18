Map call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))
    def testManifest = lib.jenkins.TestManifest.new(readYaml(file: args.testManifest))

    dockerImage = testManifest.ci?.image?.name
    dockerArgs = testManifest.ci?.image?.args
    echo "Using Docker image ${dockerImage} (${dockerArgs})"
    return [
        image: dockerImage,
        args: dockerArgs
    ]
}