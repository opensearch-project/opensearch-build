// similar jenkins/opensearch/Jenkinsfile but echo instead of sh for testing

lib = library(identifier: "jenkins@current", retriever: legacySCM(scm)).jenkins

pipeline {
    agent none
    stages {
        stage('parameters') {
            steps {
                script {
                    properties([
                            parameters([
                                    string(
                                            defaultValue: '2.0.0/opensearch-2.0.0.yml',
                                            name: 'INPUT_MANIFEST',
                                            trim: true
                                    )
                            ])
                    ])
                }
            }
        }
        stage('detect Docker image + args to use for the build') {
            agent {
                docker {
                    label 'Jenkins-Agent-al2-x64-c54xlarge-Docker-Host'
                    image 'opensearchstaging/ci-runner:centos7-x64-arm64-jdkmulti-node10.24.1-cypress6.9.1-20211028'
                    alwaysPull true
                }
            }
            steps {
                script { 
                    git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'
                    manifest = readYaml(file: "manifests/$INPUT_MANIFEST") 
                    
                    dockerImage = "${manifest.ci?.image?.name}" 
                    // If the 'image' key is not present, it is populated with "null" string 
                    if (dockerImage == null || dockerImage == "null") {
                        error("The Docker image for the build is required but was not provided in the manifest")
                    }

                    dockerArgs = "${manifest.ci?.image?.args}" 
                    // If the 'args' key is not present, it is populated with "null" string 
                    if (dockerArgs == null || dockerArgs == "null") {
                        dockerArgs = '-e JAVA_HOME=/usr/lib/jvm/adoptopenjdk-14-hotspot'
                    }

                    echo "Using Docker image: " + dockerImage
                    echo "Using Docker container args: " + dockerArgs
                }
            }
        }
        stage('build') {
            parallel {
                stage('build-snapshots') {
                    environment {
                        SNAPSHOT_REPO_URL = "https://aws.oss.sonatype.org/content/repositories/snapshots/"
                    }
                    agent {
                        docker {
                            label 'Jenkins-Agent-al2-x64-c54xlarge-Docker-Host'
                            image dockerImage
                            // Unlike freestyle docker, pipeline docker does not login to the container and run commands
                            // It use executes which does not source the docker container internal ENV VAR
                            args dockerArgs
                            alwaysPull true
                        }
                    }
                    steps {
                        script {
                            git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'
                            sh "echo ./build.sh manifests/$INPUT_MANIFEST --snapshot"
                            withCredentials([usernamePassword(credentialsId: 'Sonatype', usernameVariable: 'SONATYPE_USERNAME', passwordVariable: 'SONATYPE_PASSWORD')]) {
                                echo "$WORKSPACE/publish/publish-snapshot.sh $WORKSPACE/builds/maven"
                            }
                        }
                    }
                    post() {
                        always {
                            cleanWs disableDeferredWipeout: true, deleteDirs: true
                        }
                    }
                }
                stage('build-x64') {
                    agent {
                        docker {
                            label 'Jenkins-Agent-al2-x64-c54xlarge-Docker-Host'
                            image dockerImage
                            // Unlike freestyle docker, pipeline docker does not login to the container and run commands
                            // It use executes which does not source the docker container internal ENV VAR
                            args dockerArgs
                            alwaysPull true
                        }
                    }
                    steps {
                        script {
                            build()
                        }
                    }
                    post() {
                        always {
                            cleanWs disableDeferredWipeout: true, deleteDirs: true
                        }
                    }
                }
                stage('build-arm64') {
                    agent {
                        docker {
                            label 'Jenkins-Agent-al2-arm64-c6g4xlarge-Docker-Host'
                            image dockerImage
                            // Unlike freestyle docker, pipeline docker does not login to the container and run commands
                            // It use executes which does not source the docker container internal ENV VAR
                            args dockerArgs
                            alwaysPull true
                        }
                    }
                    steps {
                        script {
                            build()
                        }
                    }
                    post() {
                        always {
                            cleanWs disableDeferredWipeout: true, deleteDirs: true
                        }
                    }
                }
            }
            post() {
                success {
                    node('Jenkins-Agent-al2-x64-c54xlarge-Docker-Host') {
                        script {
                            def VERSION = sh(script: 'echo ${INPUT_MANIFEST} | grep -Po "[0-9.]+?(?=.yml)"', returnStdout: true).trim()
                            sh "echo VERSION:$VERSION BUILD_NUMBER:$BUILD_NUMBER"
                            def URL_x64 = "${PUBLIC_ARTIFACT_URL}/${env.JOB_NAME}/${VERSION}/${env.BUILD_NUMBER}/linux/x64/dist/opensearch-${VERSION}-linux-x64.tar.gz"
                            def URL_arm64 = "${PUBLIC_ARTIFACT_URL}/${env.JOB_NAME}/${VERSION}/${env.BUILD_NUMBER}/linux/arm64/dist/opensearch-${VERSION}-linux-arm64.tar.gz"
                            def s = "id && pwd && cd docker/release && curl -sSL $URL_x64 -o opensearch-x64.tgz && curl -sSL $URL_arm64 -o opensearch-arm64.tgz && bash build-image-multi-arch.sh -v ${VERSION} -f ./dockerfiles/opensearch.al2.dockerfile -p opensearch -a 'x64,arm64' -r opensearchstaging/opensearch -t 'opensearch-x64.tgz,opensearch-arm64.tgz' -n ${env.BUILD_NUMBER}"
                            echo "dockerBuild:${s}"
                            def stashed = lib.Messages.new(this).get(['build-x64', 'build-arm64'])
                            publishNotification(":white_check_mark:", "Successful Build", "\n${stashed}")
                        }
                    }
                }
                failure {
                    node('Jenkins-Agent-al2-x64-c54xlarge-Docker-Host') {
                        publishNotification(":warning:", "Failed Build", "")
                    }
                }
            }
        }
    }
}

void build() {
    git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'

    sh "echo ./build.sh manifests/$INPUT_MANIFEST"
    
    manifest = readYaml(file: 'tests/data/opensearch-build-1.1.0.yml')
    
    def artifactPath = "${env.JOB_NAME}/${manifest.build.version}/${env.BUILD_NUMBER}/${manifest.build.platform}/${manifest.build.architecture}";
    def BASE_URL = "${PUBLIC_ARTIFACT_URL}/${artifactPath}";

    echo "sh ./assemble.sh builds/manifest.yml --base-url ${BASE_URL}"

    withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        echo "s3Upload(file: 'builds', bucket: '${ARTIFACT_BUCKET_NAME}', path: '${artifactPath}/builds')"
        echo "s3Upload(file: 'dist', bucket: '${ARTIFACT_BUCKET_NAME}', path: '${artifactPath}/dist')"
    }

    lib.Messages.new(this).add("${STAGE_NAME}", "${BASE_URL}/builds/manifest.yml\n${BASE_URL}/dist/manifest.yml")
}

/** Publishes a notification to a slack instance*/
void publishNotification(icon, msg, extra) {
    withCredentials([string(credentialsId: 'BUILD_NOTICE_WEBHOOK', variable: 'TOKEN')]) {
        def cmd = """curl -XPOST --header "Content-Type: application/json" --data '{"result_text": "$icon ${env.JOB_NAME} [${env.BUILD_NUMBER}] $msg ${env.BUILD_URL}\nManifest: ${INPUT_MANIFEST} $extra"}' """
        echo cmd
    }
}