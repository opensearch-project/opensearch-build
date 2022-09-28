/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: args.inputManifest))
    def build_qualifier = inputManifest.build.qualifier
    def build_number = args.buildNumber ?: "${BUILD_NUMBER}"

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
        echo 'Trigger docker-build'
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
                            "-n ${build_number}"
                        ].join(' ')
                    ].join(' && ')),
            ]
        }

        echo 'Trigger docker create tag with build number'
        if (args.buildOption == "build_docker_with_build_number_tag") {
            dockerCopy: {
                build job: 'docker-copy',
                parameters: [
                    string(name: 'SOURCE_IMAGE_REGISTRY', value: 'opensearchstaging'),
                    string(name: 'SOURCE_IMAGE', value: "${filename}:${inputManifest.build.version}${build_qualifier}"),
                    string(name: 'DESTINATION_IMAGE_REGISTRY', value: 'opensearchstaging'),
                    string(name: 'DESTINATION_IMAGE', value: "${filename}:${inputManifest.build.version}${build_qualifier}.${build_number}")
                ]
            }
        }

        echo "Trigger docker-scan for ${filename} version ${inputManifest.build.version}"
        dockerScan: {
            build job: 'docker-scan',
            parameters: [
                string(name: 'IMAGE_FULL_NAME', value: "opensearchstaging/${filename}:${inputManifest.build.version}")
            ]
        }

    }
}
