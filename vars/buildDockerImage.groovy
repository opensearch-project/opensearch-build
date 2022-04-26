void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: args.inputManifest))
    def build_qualifier = inputManifest.build.qualifier

    if (build_qualifier != null && build_qualifier != 'null') {
        build_qualifier = "-" + build_qualifier
    }
    else {
        build_qualifier = ''
    }
    String filename = inputManifest.build.getFilename()

    if (args.artifactUrlX64 == null || args.artifactUrlArm64 ==  null) {
        echo 'Skipping docker build, one of x64 or arm64 artifacts was not built.'
    } else {
        dockerBuild: {
            build job: 'docker-build',
            parameters: [
                string(name: 'DOCKER_BUILD_GIT_REPOSITORY', value: 'https://github.com/opensearch-project/opensearch-build'),
                string(name: 'DOCKER_BUILD_GIT_REPOSITORY_REFERENCE', value: 'main'),
                string(name: 'DOCKER_BUILD_SCRIPT_WITH_COMMANDS', value: [
                        'id',
                        'pwd',
                        'cd docker/release',
                        "curl -sSL ${args.artifactUrlX64} -o ${filename}-x64.tgz",
                        "curl -sSL ${args.artifactUrlArm64} -o ${filename}-arm64.tgz",
                        [
                            'bash',
                            'build-image-multi-arch.sh',
                            "-v ${inputManifest.build.version}${build_qualifier}",
                            "-f ./dockerfiles/${filename}.al2.dockerfile",
                            "-p ${filename}",
                            "-a 'x64,arm64'",
                            "-r opensearchstaging/${filename}",
                            "-t '${filename}-x64.tgz,${filename}-arm64.tgz'",
                            "-n ${BUILD_NUMBER}"
                        ].join(' ')
                    ].join(' && ')),
                booleanParam(name: 'IS_STAGING', value: true)
            ]
        }
    }
}
