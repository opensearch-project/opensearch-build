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
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import com.lesfurets.jenkins.unit.MethodCall
import static org.junit.Assert.*
import static org.assertj.core.api.Assertions.assertThat
import java.util.*

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

        assertArrayEquals(Arrays.asList(
            "{includes=messages/*, name=messages-stage1}",
            "{includes=messages/*, name=messages-stage2}"
        ).toArray(), helper.callStack.stream()
            .filter { c -> c.methodName == "stash" }
            .map(MethodCall.&callArgsToString)
            .collect()
            .toArray()
        )

        assertArrayEquals(Arrays.asList(
            "{file=messages/stage1.msg, text=message 1}",
            "{file=messages/stage2.msg, text=message 2}"
        ).toArray(), helper.callStack.stream()
            .filter { c -> c.methodName == "writeFile" }
            .map(MethodCall.&callArgsToString)
            .collect()
            .toArray()
        )

        assertArrayEquals(Arrays.asList(
            "{name=messages-stage1}",
            "{name=messages-stage2}"
        ).toArray(), helper.callStack.stream()
            .filter { c -> c.methodName == "unstash" }
            .map(MethodCall.&callArgsToString)
            .collect()
            .toArray()
        )

        assertThat(helper.callStack.stream()
            .filter { c -> c.methodName == "deleteDir" }
            .collect()
        ).hasSize(1)

        assertJobStatusSuccess()
        printCallStack()
    }
}
