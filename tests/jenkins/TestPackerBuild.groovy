/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.MatcherAssert.assertThat
import static org.hamcrest.CoreMatchers.hasItem
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library


class TestPackerBuild extends BuildPipelineTest {

    // Variables
    String packerBuildGitRespository = 'https://github.com/opensearch-project/opensearch-ci'
    String packerBuildGitRespositoryReference = 'main'
    String packerTemplateName = 'jenkins-agent-al2-arm64.json'

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('2.2.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()

        binding.setVariable('PACKER_TEMPLATE_NAME', packerTemplateName)
        def sample_json = [
            "variables" : [
                "name-base" : "Jenkins-Agent-AL2-X64" ,
                "os-version" : "AL2" ,
                "build-region" : "us-east-1" ,
                "build-vpc" : "vpc-<>" ,
                "build-subnet" : "subnet-<>" ,
                "build-secgrp" : "sg-<>" ,
                "build-time" : "{{isotime \"2006-01-02T03-04-05Z\"}}" ,
                "aws_ami_region" : "us-east-1"
            ]
        ]
        helper.registerAllowedMethod("readJSON", [Map.class], {c -> sample_json})
        def sample_json_output = [
                "variables" : [
                        "name-base" : "Jenkins-Agent-AL2-X64" ,
                        "os-version" : "AL2" ,
                        "build-region" : "us-east-1" ,
                        "build-vpc" : "vpc-123" ,
                        "build-subnet" : "subnet-123" ,
                        "build-secgrp" : "sg-123" ,
                        "build-time" : "{{isotime \"2006-01-02T03-04-05Z\"}}" ,
                        "aws_ami_region" : "us-east-1"
                ]
        ]
        helper.registerAllowedMethod("writeJSON", [Map.class], {c -> sample_json_output})
        helper.registerAllowedMethod("checkout", [Map], {})
        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.addShMock("cd packer && packer build -color=false substitute_jenkins-agent-al2-arm64.json") { script ->
            return [stdout: "", exitValue: 0]
        }
    }

    @Test
    void PackerBuildRegression() {
        super.testPipeline('jenkins/packer/packer-build.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/packer/packer-build.jenkinsfile')

        def gitCheckoutCommands = getCommands('checkout', 'GitSCM').findAll {
            shCommand -> shCommand.contains('git')
        }
        assertThat(gitCheckoutCommands, hasItem("{\$class=GitSCM, branches=[{name=main}], userRemoteConfigs=[{url=https://github.com/opensearch-project/opensearch-ci}]}".toString()))

        def aws = getCommands('withAWS', 'packer')
        assertThat(aws, hasItem('{role=opensearch-packer, roleAccount=AWS_ACCOUNT_PUBLIC, duration=3600, roleSessionName=jenkins-session, useNode=true}, groovy.lang.Closure'))

        def packerCommands = getCommands('sh', 'packer')
        assertThat(packerCommands, hasItem('cd packer && packer build -color=false substitute_jenkins-agent-al2-arm64.json'))

    }

    def getCommands(method, text) {
        def shCommands = helper.callStack.findAll { call ->
            call.methodName == method
        }.collect { call ->
            callArgsToString(call)
        }.findAll { command ->
            command.contains(text)
        }
        return shCommands
    }

}
