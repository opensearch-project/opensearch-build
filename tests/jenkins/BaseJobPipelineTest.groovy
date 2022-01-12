/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */

package jenkins.tests

import jenkins.tests.CommonPipelineTest
import org.junit.Before

/**
 * Base class for testing jobs which do not need the implementation
 * details of the Jenkins library exposed.
 */
abstract class BaseJobPipelineTest extends CommonPipelineTest {
    @Override
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('scm', {})
        helper.registerAllowedMethod('legacySCM', [Closure.class], null)
        helper.registerAllowedMethod("library", [Map.class], {})
    }
}
