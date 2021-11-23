void call(Map args = [:]) {
    git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))

    String filename = inputManifest.build.getFilename()
    String x64TarGz = inputManifest.getPublicDistUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}", 'linux', 'x64')
    String arm64TarGz = inputManifest.getPublicDistUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}", 'linux', 'arm64')

    def parameters = [
        string(name: 'DOCKER_BUILD_GIT_REPOSITORY', value: 'https://github.com/opensearch-project/opensearch-build'),
        string(name: 'DOCKER_BUILD_GIT_REPOSITORY_REFERENCE', value: 'main'),
        string(name: 'DOCKER_BUILD_SCRIPT_WITH_COMMANDS', value: [
                'id',
                'pwd',
                'cd docker/release',
                "curl -sSL ${x64TarGz} -o ${filename}-x64.tgz",
                "curl -sSL ${arm64TarGz} -o ${filename}-arm64.tgz",
                [
                    'bash',
                    'build-image-multi-arch.sh',
                    "-v ${inputManifest.build.version}",
                    "-f ./dockerfiles/${filename}.al2.dockerfile",
                    "-p ${filename}",
                    "-a 'x64,arm64'",
                    "-r ${filename}staging/${filename}",
                    "-t '${filename}-x64.tgz,${filename}-arm64.tgz'",
                    "-n ${BUILD_NUMBER}"
                ].join(' ')
            ].join(' && ')),
        booleanParam(name: 'IS_STAGING', value: true)
    ]

    if (! args.dryRun) {
        dockerBuild: {
            build job: 'docker-build',
            parameters: parameters
        }
    } else {
        echo "dockerBuild: { build job: 'docker-build', parameters: ${parameters} }"
    }
}