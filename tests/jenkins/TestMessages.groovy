/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.ProjectSource.projectSource
import org.junit.Before
import org.junit.Test
import com.lesfurets.jenkins.unit.declarative.DeclarativePipelineTest

class TestMessages extends DeclarativePipelineTest {

    String sharedLibs = ''

    @Override
    @Before
    void setUp() throws Exception {
        scriptRoots += 'tests/jenkins/jobs'   

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
    void testMessages() throws Exception {
        def script = runScript("messages.groovy")
        assertJobStatusSuccess()
        printCallStack()
    }
}
