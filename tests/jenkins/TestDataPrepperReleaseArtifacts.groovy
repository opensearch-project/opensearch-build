/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.CoreMatchers.hasItems
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestDataPrepperReleaseArtifacts extends BuildPipelineTest {

    private String version

    @Before
    void setUp() {

        version = '0.22.1'

        String sourceImageRepository = 'http://public.ecr.aws/data-prepper-container-repository'

        this.registerLibTester(new SignArtifactsLibTester( '.sig', 'linux', "${workspace}/archive", null, null))

        this.registerLibTester(new CopyContainerLibTester("${sourceImageRepository}/data-prepper:${version}-997908",
                "opensearchproject/data-prepper:${version}",
                'docker',
                'jenkins-staging-docker-prod-token'))

        super.setUp()

        binding.setVariable('VERSION', version)
        binding.setVariable('DATA_PREPPER_BUILD_NUMBER', '997908')

        binding.setVariable('DATA_PREPPER_ARTIFACT_STAGING_SITE', 'http://staging-artifacts.cloudfront.net')
        binding.setVariable('DATA_PREPPER_STAGING_CONTAINER_REPOSITORY', sourceImageRepository)

        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'production-s3-bucket-name')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'production-role-name')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', 'aws-account-artifact')

        helper.registerAllowedMethod('withAWS', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod('s3Upload', [Map], {})
    }

    @Test
    void 'release-data-prepper-all-artifacts builds consistently with same inputs'() {
        testPipeline('jenkins/data-prepper/release-data-prepper-all-artifacts.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/data-prepper/release-data-prepper-all-artifacts.jenkinsfile')
    }

    @Test
    void 'downloads archives from the correct URLs'() {
        runScript('jenkins/data-prepper/release-data-prepper-all-artifacts.jenkinsfile')

        def archiveCommands = getCurlCommands().findAll {
            shCommand -> shCommand.contains('tar')
        }

        assertThat(archiveCommands.size(), equalTo(2))
        assertThat(archiveCommands, hasItem(
                "curl -sSL http://staging-artifacts.cloudfront.net/${version}/997908/archive/opensearch-data-prepper-${version}-linux-x64.tar.gz -o opensearch-data-prepper-${version}-linux-x64.tar.gz".toString()
        ))
        assertThat(archiveCommands, hasItem(
                "curl -sSL http://staging-artifacts.cloudfront.net/${version}/997908/archive/opensearch-data-prepper-jdk-${version}-linux-x64.tar.gz -o opensearch-data-prepper-jdk-${version}-linux-x64.tar.gz".toString()
        ))
    }

    @Test
    void 'downloads Maven artifacts from the correct URLs'() {
        runScript('jenkins/data-prepper/release-data-prepper-all-artifacts.jenkinsfile')

        def mavenCommands = getCurlCommands().findAll {
            shCommand -> shCommand.contains('maven/org/opensearch/dataprepper')
        }

        assertThat(mavenCommands, hasItems(
                "curl -sSL http://staging-artifacts.cloudfront.net/${version}/997908/maven/org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}-javadoc.jar -o org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}-javadoc.jar".toString(),
                "curl -sSL http://staging-artifacts.cloudfront.net/${version}/997908/maven/org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}.jar.md5 -o org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}.jar.md5".toString(),
                "curl -sSL http://staging-artifacts.cloudfront.net/${version}/997908/maven/org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}.pom.sha1 -o org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}.pom.sha1".toString(),
                "curl -sSL http://staging-artifacts.cloudfront.net/${version}/997908/maven/org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}-sources.jar.sha256 -o org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}-sources.jar.sha256".toString(),
                "curl -sSL http://staging-artifacts.cloudfront.net/${version}/997908/maven/org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}.module.sha512 -o org/opensearch/dataprepper/data-prepper-api/${version}/data-prepper-api-${version}.module.sha512".toString()
        ))
    }

    @Test
    void 's3Upload uploads to the correct path'() {
        runScript('jenkins/data-prepper/release-data-prepper-all-artifacts.jenkinsfile')

        def actualS3Upload = helper.callStack.findAll { call ->
            call.methodName == 's3Upload'
        }.first()

        assertThat(actualS3Upload, notNullValue())
        assertThat(actualS3Upload.args[0].get('path'), equalTo("data-prepper/${version}/"))
    }

    def getCurlCommands() {
        def shCurlCommands = helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.collect { call ->
            callArgsToString(call)
        }.findAll { curlCommand ->
            curlCommand.contains('curl')
        }

        return shCurlCommands
    }
}
