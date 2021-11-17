lib = library(identifier: "jenkins@current", retriever: legacySCM(scm))

pipeline {
    agent none
    stages {
        stage('build') {
            parallel {
                stage('build-on-host') {
                    steps {
                        node('Jenkins-Agent-al2-x64-c54xlarge-Docker-Host') {
                            script {
                                def messages = lib.jenkins.Messages.new(this);
                                messages.add("${STAGE_NAME}", "built ${STAGE_NAME}")
                            }
                        }
                    }
                }
                stage('build-snapshots') {
                    agent {
                        docker {
                            label 'Jenkins-Agent-al2-x64-c54xlarge-Docker-Host'
                            image 'ubuntu:latest'
                            alwaysPull
                        }
                    }
                    steps {
                        script {
                            build()
                        }
                    }
                }
                stage('build-x86') {
                    agent {
                        docker {
                            label 'Jenkins-Agent-al2-x64-c54xlarge-Docker-Host'
                            image 'amazonlinux'
                            alwaysPull
                        }
                    }
                    steps {
                        script {
                            build()
                        }
                    }
                }
                stage('build-arm64') {
                    agent {
                        docker {
                            label 'Jenkins-Agent-al2-arm64-c6g4xlarge-Docker-Host'
                            image 'ubuntu:jammy'
                            alwaysPull
                        }
                    }
                    steps {
                        script {
                            build()
                        }
                    }
                }
            }
            post() {
                success {
                    node('Jenkins-Agent-al2-x64-c54xlarge-Docker-Host') {
                        script {
                            def messages = lib.jenkins.Messages.new(this)
                            def stashed = messages.get(['build-on-host', 'build-snapshots', 'build-x86', 'build-arm64'])
                            echo stashed
                        }
                    }
                }
            }
        }
    }
}

def build() {
    def messages = lib.jenkins.Messages.new(this);
    messages.add("${STAGE_NAME}", "built ${STAGE_NAME}")
}