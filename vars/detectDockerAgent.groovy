Map call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    dockerImage = inputManifest.ci?.image?.name ?: 'opensearchstaging/ci-runner:ci-runner-centos7-v1'
    dockerArgs = inputManifest.ci?.image?.args
    // Using default javaVersion as openjdk-17
    String javaVersion = 'openjdk-17'
    java.util.regex.Matcher jdkMatch = (dockerArgs =~ /openjdk-\d+/) 
    if (jdkMatch.find()) {
        def jdkMatchLine = jdkMatch[0]
        javaVersion = jdkMatchLine
    }
    echo "Using Docker image ${dockerImage} (${dockerArgs})"
    echo "Using java version ${javaVersion}"
    return [
        image: dockerImage,
        args: dockerArgs,
        javaVersion: javaVersion
    ]
}
