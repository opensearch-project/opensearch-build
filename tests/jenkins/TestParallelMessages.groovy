/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import org.junit.*
import static org.junit.Assert.*
import java.util.*
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.ProjectSource.projectSource
import com.lesfurets.jenkins.unit.LibClassLoader
import com.lesfurets.jenkins.unit.declarative.*
import com.lesfurets.jenkins.unit.MethodCall
import static org.assertj.core.api.Assertions.assertThat

class TestParallelMessages extends DeclarativePipelineTest {
    def jenkinsScript = "tests/jenkins/jobs/parallelmessages.groovy"

    @Override
    @Before
    void setUp() throws Exception {
        super.setUp()

        helper.registerAllowedMethod('findFiles', [Map.class], null)
        
        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('<notNeeded>')
                .allowOverride(true)
                .implicit(true)
                .targetPath('<notNeeded>')
                .retriever(projectSource())
                .build()
            )
    }

    @Test
    @Ignore // raises MissingMethodException on docker agent declaration, need to upgrade jenkins-pipeline-unit which has new problems
    void testParallelMessages() throws Exception {
        binding.setVariable('scm', {})
        helper.registerAllowedMethod("legacySCM", [Closure.class], null)
        
        helper.registerAllowedMethod("library", [Map.class], { Map args ->
            helper.getLibLoader().loadLibrary(args["identifier"])
            return new LibClassLoader(helper, null)
        })

        assertJobStatusSuccess()
        printCallStack()
    }
}
