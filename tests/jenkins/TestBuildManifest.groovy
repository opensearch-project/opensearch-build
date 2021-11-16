/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import org.junit.*
import java.util.*
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.ProjectSource.projectSource
import com.lesfurets.jenkins.unit.*
import com.lesfurets.jenkins.unit.declarative.*
import static org.junit.Assert.*
import org.yaml.snakeyaml.Yaml

class TestBuildManifest extends DeclarativePipelineTest {
    def jenkinsScript = "tests/jenkins/jobs/BuildManifest_Jenkinsfile"

    @Override
    @Before
    void setUp() throws Exception {
        super.setUp()

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('<notNeeded>')
                .allowOverride(true)
                .implicit(true)
                .targetPath('<notNeeded>')
                .retriever(projectSource())
                .build()
            )

        helper.registerAllowedMethod("readYaml", [Map.class], { args ->
            return new Yaml().load((args.file as File).text)
        })
    }

    @Test
    void testBuildManifest() throws Exception {
        runScript(jenkinsScript)
        RegressionTestHelper.testNonRegression(helper, jenkinsScript)
        assertJobStatusSuccess()
        printCallStack()
    }
}
