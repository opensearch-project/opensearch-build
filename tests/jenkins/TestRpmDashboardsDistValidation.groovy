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

class TestRpmDashboardsDistValidation extends BuildPipelineTest {

    @Before
    void setUp() {

        def bundleManifest = "tests/jenkins/data/opensearch-dashboards-1.3.0-x64-rpm.yml"
        def rpmDistribution = "$workspace/opensearch-dashboards-1.3.0-linux-x64.rpm"
        this.registerLibTester(new RpmDashboardsDistValidationLibTester(rpmDistribution, bundleManifest))
        super.setUp()
        def out = "Name        : opensearch-dashboards\n" +
                "Version     : 1.3.0\n" +
                "Release     : 1\n" +
                "Architecture: x86_64\n" +
                "Install Date: (not installed)\n" +
                "Group       : Application/Internet\n" +
                "Size        : 698202962\n" +
                "License     : Apache-2.0\n" +
                "Signature   : (none)\n" +
                "Source RPM  : opensearch-dashboards-1.3.0-1.src.rpm\n" +
                "Build Date  : Wed 30 Mar 2022 01:09:33 AM UTC\n" +
                "Build Host  : dummy_desktop\n" +
                "Relocations : (not relocatable)\n" +
                "URL         : https://opensearch.org/\n" +
                "Summary     : Open source visualization dashboards for OpenSearch\n" +
                "Description :\n" +
                "OpenSearch Dashboards is the visualization tool for data in OpenSearch\n" +
                "For more information, see: https://opensearch.org/"
        helper.addShMock("rpm -qip $workspace/opensearch-dashboards-1.3.0-linux-x64.rpm") { script ->
            return [stdout: out, exitValue: 0]
        }
        def status_message = "opensearch-dashboards.service - \"OpenSearch Dashboards\"\n" +
                "   Loaded: loaded (/usr/lib/systemd/system/opensearch-dashboards.service; disabled; vendor preset: disabled)\n" +
                "   Active: active (running) since Mon 2022-04-04 21:38:58 UTC; 3 days ago\n" +
                " Main PID: 30297 (node)\n" +
                "   CGroup: /system.slice/opensearch-dashboards.service\n" +
                "           └─30297 /usr/share/opensearch-dashboards/bin/../node/bin/node /usr/share/opensearch-dashboards/bin/../src/cli/dist\n" +
                "\n" +
                "Apr 04 21:41:10 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"log\",\"@timestamp\":\"2022-04-04T21:41:10Z\",\"tags\"...00\"}\n" +
                "Apr 04 21:41:12 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"log\",\"@timestamp\":\"2022-04-04T21:41:12Z\",\"tags\"...00\"}\n" +
                "Apr 04 21:41:15 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"log\",\"@timestamp\":\"2022-04-04T21:41:15Z\",\"tags\"...00\"}\n" +
                "Apr 04 21:41:17 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"log\",\"@timestamp\":\"2022-04-04T21:41:17Z\",\"tags\"...00\"}\n" +
                "Apr 04 21:41:20 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"log\",\"@timestamp\":\"2022-04-04T21:41:20Z\",\"tags\"...00\"}\n" +
                "Apr 04 21:41:22 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"log\",\"@timestamp\":\"2022-04-04T21:41:22Z\",\"tags\"...00\"}\n" +
                "Apr 04 21:41:28 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"response\",\"@timestamp\":\"2022-04-04T21:41:28Z\",\"tags...\n" +
                "Apr 05 00:35:41 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"response\",\"@timestamp\":\"2022-04-05T00:35:41Z\",\"tags...\n" +
                "Apr 05 18:45:25 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"response\",\"@timestamp\":\"2022-04-05T18:45:25Z\",\"tags...\n" +
                "Apr 05 18:45:32 dummy_desktop opensearch-dashboards[30297]: {\"type\":\"response\",\"@timestamp\":\"2022-04-05T18:45:32Z\",\"tags...\n" +
                "Hint: Some lines were ellipsized, use -l to show in full."
        helper.addShMock("systemctl status opensearch-dashboards") { script ->
            return [stdout: status_message, exitValue: 0]
        }
        def cluster_status = [
                "name": "dummy_desktop",
                "uuid": "c4677c7a-d76f-45eb-a124-7e30d2b10e4b",
                "version": [
                        "number": "1.3.0",
                        "build_hash": "00e06934211e9819f99aabbf139885682f33e95e",
                        "build_number": 1,
                        "build_snapshot": false
                ],
                "status": [
                        "overall": [
                                "since": "2022-04-07T21:54:39.960Z",
                                "state": "green",
                                "title": "Green",
                                "nickname": "Looking good",
                                "icon": "success",
                                "uiColor": "secondary"
                        ]
                ]
        ]
        helper.addShMock("curl -s \"http://localhost:5601/api/status\" -u admin:admin") { script ->
            return [stdout: cluster_status.inspect(), exitValue: 0]
        }
        helper.registerAllowedMethod("readJSON", [Map.class], {c -> cluster_status})
        def cluster_plugin = "anomalyDetectionDashboards@1.3.0.0\n" +
                "ganttChartDashboards@1.3.0.0\n" +
                "reportsDashboards@1.3.0.0\n" +
                "securityDashboards@1.3.0.0"
        helper.addShMock("/usr/share/opensearch-dashboards/bin/opensearch-dashboards-plugin list --allow-root") { script ->
            return [stdout: cluster_plugin, exitValue: 0]
        }
    }

    @Test
    void testRpmDashboardsDistValidation() {
        super.testPipeline("tests/jenkins/jobs/RpmDashboardsDistValidation_Jenkinsfile")
    }
}
