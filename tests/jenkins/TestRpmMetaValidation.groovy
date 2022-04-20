/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestRpmMetaValidation extends BuildPipelineTest {

    @Before
    void setUp() {

        def rpmDistribution = "$workspace/opensearch-1.3.1-linux-x64.rpm"
        def refMap = [Name:"opensearch", Version: "1.3.1", Architecture: "x64", Group: "Application/Internet",
                License: "Apache-2.0", Relocations: "(not relocatable)", URL: "https://opensearch.org/",
                Summary: "An open source distributed and RESTful search engine",
                Description: "OpenSearch makes it easy to ingest, search, visualize, and analyze your data.\n" +
                        "For more information, see: https://opensearch.org/"
        ]
        this.registerLibTester(new RpmMetaValidationLibTester(rpmDistribution, refMap))
        super.setUp()
        def out = "Name        : opensearch\n" +
                "Version     : 1.3.1\n" +
                "Release     : 1\n" +
                "Architecture: x86_64\n" +
                "Install Date: (not installed)\n" +
                "Group       : Application/Internet\n" +
                "Size        : 646503829\n" +
                "License     : Apache-2.0\n" +
                "Signature   : (none)\n" +
                "Source RPM  : opensearch-1.3.1-1.src.rpm\n" +
                "Build Date  : Wed Mar 23 22:10:17 2022\n" +
                "Build Host  : f8a4d27a00d9\n" +
                "Relocations : (not relocatable)\n" +
                "URL         : https://opensearch.org/\n" +
                "Summary     : An open source distributed and RESTful search engine\n" +
                "Description :\n" +
                "OpenSearch makes it easy to ingest, search, visualize, and analyze your data.\n" +
                "For more information, see: https://opensearch.org/"
        helper.addShMock("rpm -qip $workspace/opensearch-1.3.1-linux-x64.rpm") { script ->
            return [stdout: out, exitValue: 0]
        }
    }

    @Test
    void testRpmMetaValidation() {
        super.testPipeline("tests/jenkins/jobs/RpmMetaValidation_Jenkinsfile")
    }
}
