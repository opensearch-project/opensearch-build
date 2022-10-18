/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import com.lesfurets.jenkins.unit.*
import org.yaml.snakeyaml.Yaml

/**
 * Base test class for testing Jenkins library code. This base test
 * sets up the project directory as the library and will execute
 * library code.
 */
abstract class BuildPipelineTest extends CommonPipelineTest {

    private List testers = [];

    public String workspace = '/tmp/workspace'

    public void registerLibTester(LibFunctionTester tester) {
        testers.add(tester)
    }

    @Override
    @Before
    void setUp() {
        super.setUp()

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('1.0.4')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        helper.registerAllowedMethod("readYaml", [Map.class], { args ->
            return new Yaml().load((args.file as File).text)
        })

        binding.setVariable('scm', {})

        helper.registerAllowedMethod("legacySCM", [Closure.class], null)
        
        helper.registerAllowedMethod("modernSCM", [Map.class], null)

        helper.registerAllowedMethod("library", [Map.class], { Map args ->
            helper.getLibLoader().loadLibrary(args["identifier"])
            return new LibClassLoader(helper, null)
        })

        helper.registerAllowedMethod("cleanWs", [Map])

        binding.setVariable('WORKSPACE', workspace)

        testers.each(tester -> tester.configure(helper, binding))
    }

    @After
    public void after() {
        testers.each(tester -> tester.verifyParams(helper))
    }

}
