/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestRpmOpenSearchDistValidation extends BuildPipelineTest {

    @Before
    void setUp() {

        def bundleManifest = "tests/jenkins/data/opensearch-1.3.1-x64-rpm.yml"
        def rpmDistribution = "$workspace/opensearch-1.3.1-linux-x64.rpm"
        this.registerLibTester(new RpmOpenSearchDistValidationLibTester(rpmDistribution, bundleManifest))
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
                "OpenSearch makes it easy to ingest, search, visualize, and analyze your data\n" +
                "For more information, see: https://opensearch.org/"
        helper.addShMock("rpm -qip $workspace/opensearch-1.3.1-linux-x64.rpm") { script ->
            return [stdout: out, exitValue: 0]
        }
        def sigOut = "/tmp/workspace/opensearch-1.3.1-linux-x64.rpm:\n" + "Header V4 RSA/SHA512 Signature, key ID 9310d3fc: OK\n" +
                "Header SHA256 digest: OK\n" + "Header SHA1 digest: OK\n" + "Payload SHA256 digest: OK\n" +
                "V4 RSA/SHA512 Signature, key ID 9310d3fc: OK\n" + "MD5 digest: OK"
        helper.addShMock("rpm -K -v $rpmDistribution") { script ->
            return [stdout: sigOut, exitValue: 0]
        }
        helper.addShMock("ls /etc/opensearch") { script ->
            return [stdout: "esnode-key.pem  jvm.options.d        kirk.pem                  opensearch-reports-scheduler" +
                    "  performance_analyzer_enabled.conf    esnode.pem      jvm.options.rpmsave  log4j2.properties" +
                    "         opensearch.yml                rca_enabled.conf    jvm.options     kirk-key.pem" +
                    "         opensearch-observability  opensearch.yml.rpmsave        root-ca.pem", exitValue: 0]
        }
        def log_message = "OpenSearch Security Demo Installer\n" +
                " ** Warning: Do not use on production or public reachable systems **\n" +
                "Basedir: /usr/share/opensearch\n" +
                "OpenSearch install type: rpm/deb on CentOS Linux release 7.9.2009 (Core)\n" +
                "OpenSearch config dir: /etc/opensearch\n" +
                "OpenSearch config file: /etc/opensearch/opensearch.yml\n" +
                "OpenSearch bin dir: /usr/share/opensearch/bin\n" +
                "OpenSearch plugins dir: /usr/share/opensearch/plugins\n" +
                "OpenSearch lib dir: /usr/share/opensearch/lib\n" +
                "Detected OpenSearch Version: x-content-1.3.0\n" +
                "Detected OpenSearch Security Version: 1.3.0.0\n" +
                "\n" +
                "### Success\n" +
                "### Execute this script now on all your nodes and then start all nodes\n" +
                "### OpenSearch Security will be automatically initialized.\n" +
                "### If you like to change the runtime configuration\n" +
                "### change the files in ../securityconfig and execute:\n" +
                "\"/usr/share/opensearch/plugins/opensearch-security/tools/securityadmin.sh\" -cd \"/usr/share/opensearch/plugins/opensearch-security/securityconfig\" -icl -key \"/etc/opensearch/kirk-key.pem\" -cert \"/etc/opensearch/kirk.pem\" -cacert \"/etc/opensearch/root-ca.pem\" -nhnv\n" +
                "### or run ./securityadmin_demo.sh\n" +
                "### To use the Security Plugin ConfigurationGUI\n" +
                "### To access your secured cluster open https://<hostname>:<HTTP port> and log in with admin/admin.\n" +
                "### (Ignore the SSL certificate warning because we installed self-signed demo certificates)"
        helper.addShMock("cat /var/log/opensearch/install_demo_configuration.log") { script ->
            return [stdout: log_message, exitValue: 0]
        }
        def status_message = "   Loaded: loaded (/usr/lib/systemd/system/opensearch.service; disabled; vendor preset: disabled)\n" +
                "   Active: active (running) since Mon 2022-04-04 21:41:23 UTC; 2h 52min ago\n" +
                "     Docs: https://opensearch.org/\n" +
                " Main PID: 32009 (java)\n" +
                "   CGroup: /system.slice/opensearch.service\n" +
                "           └─32009 /usr/share/opensearch/jdk/bin/java -Xshare:auto -Dopensearch.networkaddress.cache.ttl=60 -Dopensearch.networkaddress.cache.negative.ttl=1...\n" +
                "\n" +
                "Apr 04 21:41:25 dummy_desktop systemd-entrypoint[32009]: WARNING: An illegal reflective access operation has occurred\n" +
                "Apr 04 21:41:25 dummy_desktop systemd-entrypoint[32009]: WARNING: Illegal reflective access by org.opensearch.securi...name\n" +
                "Apr 04 21:41:25 dummy_desktop systemd-entrypoint[32009]: WARNING: Please consider reporting this to the maintainers ...tter\n" +
                "Apr 04 21:41:25 dummy_desktop systemd-entrypoint[32009]: WARNING: Use --illegal-access=warn to enable warnings of fu...ions\n" +
                "Apr 04 21:41:25 dummy_desktop systemd-entrypoint[32009]: WARNING: All illegal access operations will be denied in a ...ease\n" +
                "Apr 04 22:11:35 dummy_desktop systemd-entrypoint[32009]: Exception in thread \"Attach Listener\" Agent failed to start!\n" +
                "Apr 04 22:41:47 dummy_desktop systemd-entrypoint[32009]: Exception in thread \"Attach Listener\" Agent failed to start!\n" +
                "Apr 04 23:11:59 dummy_desktop systemd-entrypoint[32009]: Exception in thread \"Attach Listener\" Agent failed to start!\n" +
                "Apr 04 23:42:10 dummy_desktop systemd-entrypoint[32009]: Exception in thread \"Attach Listener\" Agent failed to start!\n" +
                "Apr 05 00:12:22 dummy_desktop systemd-entrypoint[32009]: Exception in thread \"Attach Listener\" Agent failed to start!\n" +
                "Hint: Some lines were ellipsized, use -l to show in full."
        helper.addShMock("systemctl status opensearch") { script ->
            return [stdout: status_message, exitValue: 0]
        }
        def cluster_info_n_status = [
                "name" : "dummy_desktop",
                "cluster_name" : "opensearch",
                "status":"green",
                "cluster_uuid" : "uClFQNw6T_KCO2fmdP2jTA",
                "version" : [
                        "distribution" : "opensearch",
                        "number" : "1.3.1",
                        "build_type" : "rpm",
                        "build_hash" : "40481be2be0536a34588b1fad10eb6c289713803",
                        "build_date" : "2022-03-28T18:33:36.499005Z",
                        "build_snapshot" : false,
                        "lucene_version" : "8.10.1",
                        "minimum_wire_compatibility_version" : "6.8.0",
                        "minimum_index_compatibility_version" : "6.0.0-beta1"],
                "tagline" : "The OpenSearch Project: https://opensearch.org/"
        ]
        helper.addShMock("curl -s \"https://localhost:9200\" -u admin:admin --insecure") { script ->
            return [stdout: cluster_info_n_status.inspect(), exitValue: 0]
        }
        helper.registerAllowedMethod("readJSON", [Map.class], {c -> cluster_info_n_status})
        def cluster_status = [cluster_name:"opensearch", status:"green", timed_out:false, number_of_nodes:1,
                              number_of_data_nodes:1, discovered_master:true, active_primary_shards:1, active_shards:1,
                              relocating_shards:0, initializing_shards:0, unassigned_shards:0, delayed_unassigned_shards:0,
                              number_of_pending_tasks:0, number_of_in_flight_fetch:0, task_max_waiting_in_queue_millis:0,
                              active_shards_percent_as_number:100.0]
        helper.addShMock("curl -s \"https://localhost:9200/_cluster/health?pretty\" -u admin:admin --insecure") { script ->
            return [stdout: cluster_status.inspect(), exitValue: 0]
        }
        def cluster_plugin = "dummy_desktop opensearch-alerting                  1.3.1.0\n" +
                "dummy_desktop opensearch-job-scheduler             1.3.1.0\n" +
                "dummy_desktop opensearch-ml                        1.3.1.0"
        helper.addShMock("curl -s \"https://localhost:9200/_cat/plugins\" -u admin:admin --insecure") { script ->
            return [stdout: cluster_plugin, exitValue: 0]
        }

        def pa_status_message = "opensearch-performance-analyzer.service - OpenSearch Performance Analyzer\n" +
                "   Loaded: loaded (/usr/lib/systemd/system/opensearch-performance-analyzer.service; disabled; vendor preset: disabled)\n" +
                "   Active: active (running) since Wed 2022-04-27 23:41:32 UTC; 20min ago\n" +
                " Main PID: 518 (java)\n" +
                "   CGroup: /docker/0ac16d0953dba2520b57227f93645847c916e1747c7d0fb47ffaef593075f809/system.slice/opensearch-performance-analyzer.service\n" +
                "           └─518 /usr/share/opensearch/jdk/bin/java -Xshare:auto -Xms4m -Xmx64m -XX:+UseSerialGC -Dlog4j.configurationFile=/usr/share/opensearch/plugins/opensearch-performance-a...\n" +
                "\n" +
                "Apr 28 00:02:00 0ac16d0953db performance-analyzer-agent-cli[518]: 00:02:00.413 [JPhU4pKjSySOd03YU1Fm6g-task-0-] ERROR org.opensearch.performanceanalyzer.rca.store.metric.Aggrega...\n" +
                "Hint: Some lines were ellipsized, use -l to show in full."
        helper.addShMock("systemctl status opensearch-performance-analyzer") { script ->
            return [stdout: pa_status_message, exitValue: 0]
        }

        def pa_metrics = "{\"JPhU4pKjSySOd03YU1Fm6g\": {\"timestamp\": 1651104310000, \"data\": {\"fields\":" +
                "[{\"name\":\"CPU_Utilization\",\"type\":\"DOUBLE\"}],\"records\":[[1.258446418449754E-4]]}}}"
        helper.addShMock("curl -s localhost:9600/_plugins/_performanceanalyzer/metrics?metrics=CPU_Utilization\\&agg=avg") { script ->
            return [stdout: pa_metrics, exitValue: 0]
        }


    }

    @Test
    void testRpmOpenSearchDistValidation() {
        super.testPipeline("tests/jenkins/jobs/RpmOpenSearchDistValidation_Jenkinsfile")
    }
}
