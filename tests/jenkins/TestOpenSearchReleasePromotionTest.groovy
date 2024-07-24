/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.MatcherAssert.assertThat

class TestOpenSearchReleasePromotionTest extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('5.11.1')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()

        helper.registerAllowedMethod('withAWS', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('cfInvalidate', [Map])
        addParam('RELEASE_VERSION', '1.0.0')
        addParam('OPENSEARCH_RC_BUILD_NUMBER', '2050')
        addParam('OPENSEARCH_DASHBOARDS_RC_BUILD_NUMBER', '3050')
        binding.setVariable('AGENT_LINUX_X64', 'Jenkins-Agent-AL2023-X64-C54xlarge-Docker-Host')
    }

    @Test
    void shouldExecuteWithoutErrors() {
        super.testPipeline('jenkins/release-workflows/release-promotion.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/release-promotion.jenkinsfile')

        def callStack = helper.getCallStack()
        // Parameters Check
        assertCallStack().contains('stage(Parameters Check, groovy.lang.Closure)')

        // OpenSearch Debian Apt promotion
        assertCallStack().contains('stage(OpenSearch Debian Apt promotion, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_REPO_TYPE, value=apt})')

        // OpenSearch Yum promotion
        assertCallStack().contains('stage(OpenSearch Yum promotion, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_REPO_TYPE, value=yum})')

        // OpenSearch Dashboards Debian Apt promotion
        assertCallStack().contains('stage(OpenSearch Dashboards Debian Apt promotion, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch-dashboards})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_REPO_TYPE, value=apt})')

        // OpenSearch Dashboards Yum promotion
        assertCallStack().contains('stage(OpenSearch Dashboards Yum promotion, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch-dashboards})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_REPO_TYPE, value=yum})')

        // OpenSearch Windows promotion
        assertCallStack().contains('stage(OpenSearch Windows promotion, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=windows})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=zip})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=x64})')

        // OpenSearch Dashboards Windows promotion
        assertCallStack().contains('stage(OpenSearch Dashboards Windows promotion, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch-dashboards})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=windows})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=zip})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=x64})')

        // OpenSearch Linux deb arm64
        assertCallStack().contains('stage(OpenSearch Linux deb arm64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=deb})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=arm64})')

        // OpenSearch Linux deb x64
        assertCallStack().contains('stage(OpenSearch Linux deb x64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=deb})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=x64})')

        // OpenSearch Dashboards Linux deb arm64
        assertCallStack().contains('stage(OpenSearch Dashboards Linux deb arm64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch-dashboards})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=deb})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=arm64})')

        // OpenSearch Dashboards Linux deb x64
        assertCallStack().contains('stage(OpenSearch Dashboards Linux deb x64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch-dashboards})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=deb})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=x64})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_BUILD_NUMBER, value=3050})')

        // OpenSearch Linux rpm arm64
        assertCallStack().contains('stage(OpenSearch Linux rpm arm64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=rpm})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=arm64})')

        // OpenSearch Linux rpm x64
        assertCallStack().contains('stage(OpenSearch Linux rpm x64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=rpm})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=x64})')

        // OpenSearch Dashboards Linux rpm arm64
        assertCallStack().contains('stage(OpenSearch Dashboards Linux rpm arm64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch-dashboards})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=rpm})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=arm64})')

        // OpenSearch Dashboards Linux rpm x64
        assertCallStack().contains('stage(OpenSearch Dashboards Linux rpm x64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch-dashboards})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=rpm})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=x64})')

        // OpenSearch Linux tar arm64
        assertCallStack().contains('stage(OpenSearch Linux tar arm64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=tar})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=arm64})')

        // OpenSearch Dashboards Linux tar arm64
        assertCallStack().contains('stage(OpenSearch Dashboards Linux tar arm64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch-dashboards})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=tar})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=arm64})')

        // OpenSearch Dashboards Linux tar x64
        assertCallStack().contains('stage(OpenSearch Dashboards Linux tar x64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch-dashboards})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=tar})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=x64})')

        // OpenSearch Linux tar x64
        assertCallStack().contains('stage(Publish OpenSearch Linux tar x64, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_JOB_NAME, value=distribution-build-opensearch})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_PLATFORM, value=linux})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_NAME, value=tar})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION_ARCHITECTURE, value=x64})')

        // Docker promotion
        assertCallStack().contains('stage(Promote Docker, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=SOURCE_IMAGES, value=opensearch:1.0.0.2050, opensearch-dashboards:1.0.0.3050})')
        assertCallStack().contains('release-promotion.string({name=RELEASE_VERSION, value=1.0.0})')
        assertCallStack().contains('release-promotion.booleanParam({name=DOCKER_HUB_PROMOTE, value=true})')
        assertCallStack().contains('release-promotion.booleanParam({name=ECR_PROMOTE, value=true})')
        assertCallStack().contains('release-promotion.booleanParam({name=TAG_LATEST, value=true})')
        assertCallStack().contains('release-promotion.booleanParam({name=TAG_MAJOR_VERSION, value=true})')
        assertCallStack().contains('release-promotion.build({job=docker-promotion, wait=true, parameters=[null, null, null, null, null, null]})')

        // Validation Workflow
        assertCallStack().contains('stage(Validate the artifacts, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.string({name=VERSION, value=1.0.0})')
        assertCallStack().contains('release-promotion.string({name=DISTRIBUTION, value=tar rpm yum deb zip docker})')
        assertCallStack().contains('release-promotion.string({name=ARCHITECTURE, value=x64 arm64})')
        assertCallStack().contains('release-promotion.string({name=PLATFORM, value=linux windows})')
        assertCallStack().contains('release-promotion.string({name=PROJECTS, value=Both})')
        assertCallStack().contains('release-promotion.string({name=DOCKER_SOURCE, value=Both})')
        assertCallStack().contains('release-promotion.string({name=ARTIFACT_TYPE, value=production})')
        assertCallStack().contains('release-promotion.string({name=OPTIONAL_ARGS, value=validate-digest-only})')
        assertCallStack().contains('release-promotion.build({job=distribution-validation, wait=true, parameters=[null, null, null, null, null, null, null, null]})')

        // Maven Promotion Workflow
        assertCallStack().contains('stage(Publish to Maven, groovy.lang.Closure)')
        assertCallStack().contains('release-promotion.echo(Triggering publish to maven workflow)')
        assertCallStack().contains('release-promotion.string({name=BUILD_ID, value=2050})')
        assertCallStack().contains('release-promotion.string({name=VERSION, value=1.0.0})')
        assertCallStack().contains('release-promotion.build({job=publish-to-maven, wait=false, parameters=[null, null]})')
    }

    @Test
    void verifyCfnCommands() {
        runScript('jenkins/release-workflows/release-promotion.jenkinsfile')
        def callStack = helper.getCallStack()
         assertCallStack().contains(
            'release-promotion.cfInvalidate({distribution=CLOUDFRONT_DISTRIBUTION_ID, paths=[/releases/bundle/opensearch/1.x/*, /releases/bundle/opensearch-dashboards/1.x/*], waitForCompletion=true})'
        )
    }
}