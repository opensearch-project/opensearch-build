/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*
import java.util.*
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.ProjectSource.projectSource
import com.lesfurets.jenkins.unit.*
import com.lesfurets.jenkins.unit.declarative.*
import static org.junit.Assert.*
import org.yaml.snakeyaml.Yaml

abstract class BuildPipelineTest extends DeclarativePipelineTest {
    @Override
    @Before
    void setUp() {
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

        binding.setVariable('scm', {})
        
        helper.registerAllowedMethod("legacySCM", [Closure.class], null)
        
        helper.registerAllowedMethod("library", [Map.class], { Map args ->
            helper.getLibLoader().loadLibrary(args["identifier"])
            return new LibClassLoader(helper, null)
        })
    }

    void testPipeline(String jenkinsScript) {
        runScript(jenkinsScript)
        RegressionTestHelper.testNonRegression(helper, jenkinsScript)
        assertJobStatusSuccess()
        printCallStack()
    }
}
