<h1>OpenSearch and OpenSearch Dashboards 2.11.0 Release Notes</h1>
<h2>FEATURES</h2>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Support sparse semantic retrieval by introducing <code>sparse_encoding</code> ingest processor and query builder (<a href="https://github.com/opensearch-project/neural-search/pull/333">#333</a>)</li>
<li>Enabled support for applying default modelId in neural search query (<a href="https://github.com/opensearch-project/neural-search/pull/337">#337</a></li>
<li>Added Multimodal semantic search feature (<a href="https://github.com/opensearch-project/neural-search/pull/359">#359</a>)</li>
</ul>

<h2>ENHANCEMENTS</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Add logging for execution and indexes of monitors and workflows. (<a href="https://github.com/opensearch-project/alerting/pull/1223">#1223</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Provide unique id for each rollup job and add debug logs. (<a href="https://github.com/opensearch-project/index-management/pull/968">#968</a>)</li>
</ul>

<h3>Opensearch KNN</h3>

<ul>
<li>Added support for ignore_unmapped in KNN queries. <a href="https://github.com/opensearch-project/k-NN/pull/1071">#1071</a></li>
<li>Add graph creation stats to the KNNStats API. <a href="https://github.com/opensearch-project/k-NN/pull/1141">#1141</a></li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Add neural search default processor for non OpenAI/Cohere scenario (<a href="https://github.com/opensearch-project/ml-commons/pull/1274">#1274</a>)</li>
<li>Add tokenizer and sparse encoding (<a href="https://github.com/opensearch-project/ml-commons/pull/1301">#1301</a>)</li>
<li>allow input null for text docs input (<a href="https://github.com/opensearch-project/ml-commons/pull/1402">#1402</a>)</li>
<li>Add support for context_size and include 'interaction_id' in SearchRequest (<a href="https://github.com/opensearch-project/ml-commons/pull/1385">#1385</a>)</li>
<li>adding model level metric in node level (<a href="https://github.com/opensearch-project/ml-commons/pull/1330">#1330</a>)</li>
<li>add status code to model tensor (<a href="https://github.com/opensearch-project/ml-commons/pull/1443">#1443</a>)</li>
<li>add bedrockURL to trusted connector regex list (<a href="https://github.com/opensearch-project/ml-commons/pull/1461">#1461</a>)</li>
<li>Performance enhacement for predict action by caching model info (<a href="https://github.com/opensearch-project/ml-commons/pull/1472">#1472</a>)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Add <code>max_token_score</code> parameter to improve the execution efficiency for <code>neural_sparse</code> query clause (<a href="https://github.com/opensearch-project/neural-search/pull/348">#348</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Authorization in Rest Layer (<a href="https://github.com/opensearch-project/security/pull/2753">#2753</a>)</li>
<li>Improve serialization speeds (<a href="https://github.com/opensearch-project/security/pull/2802">#2802</a>)</li>
<li>Integration tests framework (<a href="https://github.com/opensearch-project/security/pull/3388">#3388</a>)</li>
<li>Allow for automatic merging of dependabot changes after checks pass (<a href="https://github.com/opensearch-project/security/pull/3409">#3409</a>)</li>
<li>Support security config updates on the REST API using permission(<a href="https://github.com/opensearch-project/security/pull/3264">#3264</a>)</li>
<li>Expanding Authentication with SecurityRequest Abstraction (<a href="https://github.com/opensearch-project/security/pull/3430">#3430</a>)</li>
<li>Add early rejection from RestHandler for unauthorized requests (<a href="https://github.com/opensearch-project/security/pull/3418">#3418</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Adds support for alerts and triggers on group by based sigma rules. (<a href="https://github.com/opensearch-project/security-analytics/pull/545">#545</a>)</li>
<li>Auto expand replicas. (<a href="https://github.com/opensearch-project/security-analytics/pull/547">#547</a>)</li>
<li>Auto expand replicas for logtype index. (<a href="https://github.com/opensearch-project/security-analytics/pull/568">#568</a>)</li>
<li>Adding WAF Log type. (<a href="https://github.com/opensearch-project/security-analytics/pull/617">#617</a>)</li>
<li>Add category to custom log types. (<a href="https://github.com/opensearch-project/security-analytics/pull/634">#634</a>)</li>
</ul>

<h3>SQL</h3>

<ul>
<li>Enable PPL lang and add datasource to async query API in https://github.com/opensearch-project/sql/pull/2195</li>
<li>Refactor Flint Auth in https://github.com/opensearch-project/sql/pull/2201</li>
<li>Add conf for spark structured streaming job in https://github.com/opensearch-project/sql/pull/2203</li>
<li>Submit long running job only when auto_refresh = false in https://github.com/opensearch-project/sql/pull/2209</li>
<li>Bug Fix, handle DESC TABLE response in https://github.com/opensearch-project/sql/pull/2213</li>
<li>Drop Index Implementation in https://github.com/opensearch-project/sql/pull/2217</li>
<li>Enable PPL Queries in https://github.com/opensearch-project/sql/pull/2223</li>
<li>Read extra Spark submit parameters from cluster settings in https://github.com/opensearch-project/sql/pull/2236</li>
<li>Spark Execution Engine Config Refactor in https://github.com/opensearch-project/sql/pull/2266</li>
<li>Provide auth.type and auth.role_arn paramters in GET Datasource API response. in https://github.com/opensearch-project/sql/pull/2283</li>
<li>Add support for <code>date_nanos</code> and tests. (#337) in https://github.com/opensearch-project/sql/pull/2020</li>
<li>Applied formatting improvements to Antlr files based on spotless changes (#2017) by @MitchellGale in https://github.com/opensearch-project/sql/pull/2023</li>
<li>Revert &quot;Guarantee datasource read api is strong consistent read (#1815)&quot; in https://github.com/opensearch-project/sql/pull/2031</li>
<li>Add _primary preference only for segment replication enabled indices in https://github.com/opensearch-project/sql/pull/2045</li>
<li>Changed allowlist config to denylist ip config for datasource uri hosts in https://github.com/opensearch-project/sql/pull/2058</li>
</ul>

<h2>BUG FIXES</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Fix workflow execution for first run. (<a href="https://github.com/opensearch-project/alerting/pull/1227">#1227</a>)</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Fix flaky test, testIndexingMultiPolygon (<a href="https://github.com/opensearch-project/geospatial/pull/483">#483</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Fix auto managed index always have -2 seqNo bug. (<a href="https://github.com/opensearch-project/index-management/pull/924">#924</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>fix parameter name in preprocess function (<a href="https://github.com/opensearch-project/ml-commons/pull/1362">#1362</a>)</li>
<li>fix spelling in Readme.md (<a href="https://github.com/opensearch-project/ml-commons/pull/1363">#1363</a>)</li>
<li>Fix error message in TransportDeplpoyModelAction class (<a href="https://github.com/opensearch-project/ml-commons/pull/1368">#1368</a>)</li>
<li>fix null exception in text docs data set (<a href="https://github.com/opensearch-project/ml-commons/pull/1403">#1403</a>)</li>
<li>fix text docs input unescaped error; enable deploy remote model (<a href="https://github.com/opensearch-project/ml-commons/pull/1407">#1407</a>)</li>
<li>restore thread context before running action listener (<a href="https://github.com/opensearch-project/ml-commons/pull/1418">#1418</a>)</li>
<li>fix more places where thread context not restored (<a href="https://github.com/opensearch-project/ml-commons/pull/1421">#1421</a>)</li>
<li>Fix BWC test suite (<a href="https://github.com/opensearch-project/ml-commons/pull/1426">#1426</a>)</li>
<li>support bwc for process function (<a href="https://github.com/opensearch-project/ml-commons/pull/1427">#1427</a>)</li>
<li>fix model group auto-deletion when last version is deleted (<a href="https://github.com/opensearch-project/ml-commons/pull/1444">#1444</a>)</li>
<li>fixing metrics correlation algorithm (<a href="https://github.com/opensearch-project/ml-commons/pull/1448">#1448</a>)</li>
<li>throw exception if remote model doesn't return 2xx status code; fix predict runner (<a href="https://github.com/opensearch-project/ml-commons/pull/1477">#1477</a>)</li>
<li>fix no worker node exception for remote embedding model (<a href="https://github.com/opensearch-project/ml-commons/pull/1482">#1482</a>)</li>
<li>fix for delete model group API throwing incorrect error when model index not created (<a href="https://github.com/opensearch-project/ml-commons/pull/1485">#1485</a>)</li>
<li>fix no worker node error on multi-node cluster (<a href="https://github.com/opensearch-project/ml-commons/pull/1487">#1487</a>)</li>
<li>Fix prompt passing for Bedrock by passing a single string prompt for Bedrock models. (<a href="https://github.com/opensearch-project/ml-commons/pull/1490">#1490</a>)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Fixed exception in Hybrid Query for one shard and multiple node (<a href="https://github.com/opensearch-project/neural-search/pull/396">#396</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Update Jooq version and address bind variable failure in AdmissionControl Emitter <a href="https://github.com/opensearch-project/performance-analyzer/pull/493">#493</a></li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Refactors reRequestAuthentication to call notifyIpAuthFailureListener before sending the response to the channel (<a href="https://github.com/opensearch-project/security/pull/3411">#3411</a>)</li>
<li>For read-only tenants filter with allow list (<a href="https://github.com/opensearch-project/security/commit/c3e53e20a69dc8eb401653594a130c2a4fd4b6bd">c3e53e2</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Fixes verifying workflow test when security is enabled. (<a href="https://github.com/opensearch-project/security-analytics/pull/563">#563</a>)</li>
<li>Fix flaky integration tests. (<a href="https://github.com/opensearch-project/security-analytics/pull/581">#581</a>)</li>
<li>Sigma Aggregation rule fixes. (<a href="https://github.com/opensearch-project/security-analytics/pull/622">#622</a>)</li>
</ul>

<h3>SQL</h3>

<ul>
<li>fix broken link for connectors doc in https://github.com/opensearch-project/sql/pull/2199</li>
<li>Fix response codes returned by JSON formatting them in https://github.com/opensearch-project/sql/pull/2200</li>
<li>Bug fix, datasource API should be case sensitive in https://github.com/opensearch-project/sql/pull/2202</li>
<li>Minor fix in dropping covering index in https://github.com/opensearch-project/sql/pull/2240</li>
<li>Fix Unit tests for FlintIndexReader in https://github.com/opensearch-project/sql/pull/2242</li>
<li>Bug Fix , delete OpenSearch index when DROP INDEX in https://github.com/opensearch-project/sql/pull/2252</li>
<li>Correctly Set query status in https://github.com/opensearch-project/sql/pull/2232</li>
<li>Exclude generated files from spotless  in https://github.com/opensearch-project/sql/pull/2024</li>
<li>Fix mockito core conflict. in https://github.com/opensearch-project/sql/pull/2131</li>
<li>Fix <code>ASCII</code> function and groom UT for text functions. (#301) in https://github.com/opensearch-project/sql/pull/2029</li>
<li>Fixed response codes For Requests With security exception. in https://github.com/opensearch-project/sql/pull/2036</li>
</ul>

<h2>INFRASTRUCTURE</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Ignore flaky security test suites. (<a href="https://github.com/opensearch-project/alerting/pull/1188">#1188</a>)</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Add dependabot.yml (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1026">#1026</a>)</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Add integration test against security enabled cluster (<a href="https://github.com/opensearch-project/geospatial/pull/513">#513</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Upload docker test cluster log. (<a href="https://github.com/opensearch-project/index-management/pull/964">#964</a>)</li>
<li>Reduce test running time. (<a href="https://github.com/opensearch-project/index-management/pull/965">#965</a>)</li>
<li>Parallel test run. (<a href="https://github.com/opensearch-project/index-management/pull/966">#966</a>)</li>
<li>Security test filtered. (<a href="https://github.com/opensearch-project/index-management/pull/969">#969</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Update PULL_REQUEST_TEMPLATE.md <a href="https://github.com/opensearch-project/performance-analyzer/pull/560">#560)</a></li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Ignore tests that may be flaky. (<a href="https://github.com/opensearch-project/security-analytics/pull/596">#596</a>)</li>
</ul>

<h3>SQL</h3>

<ul>
<li>bump aws-encryption-sdk-java to 1.71 in https://github.com/opensearch-project/sql/pull/2057</li>
<li>Run IT tests with security plugin (#335) #1986 by @MitchellGale in https://github.com/opensearch-project/sql/pull/2022</li>
</ul>

<h2>DOCUMENTATION</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Added 2.11 release notes (<a href="https://github.com/opensearch-project/alerting/pull/1251">#1251</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Added 2.11 release notes. (<a href="https://github.com/opensearch-project/index-management/pull/1004">#1004</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Add 2.11.0 release notes (<a href="https://github.com/opensearch-project/notifications/issues/774">#774</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Added 2.11.0 release notes. (<a href="https://github.com/opensearch-project/security-analytics/pull/660">#660</a>)</li>
</ul>

<h3>SQL</h3>

<ul>
<li>Datasource description in https://github.com/opensearch-project/sql/pull/2138</li>
<li>Add documentation for S3GlueConnector. in https://github.com/opensearch-project/sql/pull/2234</li>
</ul>

<h2>MAINTENANCE</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Increment version to 2.11.0-SNAPSHOT. (<a href="https://github.com/opensearch-project/alerting/pull/1116">#1116</a>)</li>
</ul>

<h3>Opensearch Asynchronous Search</h3>

<ul>
<li>Increment version to 2.11.0 (<a href="https://github.com/opensearch-project/asynchronous-search/pull/446">#446</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Increment version to 2.11.0-SNAPSHOT. (<a href="https://github.com/opensearch-project/index-management/pull/922">#922</a>)</li>
</ul>

<h3>Opensearch Job Scheduler</h3>

<ul>
<li>bump actions/upload-release-asset from 1.0.1 to 1.0.2 (<a href="https://github.com/opensearch-project/job-scheduler/pull/504">#504</a>)(<a href="https://github.com/opensearch-project/job-scheduler/pull/506">#506</a>)</li>
<li>bump aws-actions/configure-aws-credentials from 1 to 4 (<a href="https://github.com/opensearch-project/job-scheduler/pull/501">#501</a>)(<a href="https://github.com/opensearch-project/job-scheduler/pull/507">#507</a>)</li>
<li>bump com.netflix.nebula.ospackage from 11.4.0 to 11.5.0  (<a href="https://github.com/opensearch-project/job-scheduler/pull/500">#500</a>)(<a href="https://github.com/opensearch-project/job-scheduler/pull/508">#508</a>)</li>
<li>manual backport of #503 (<a href="https://github.com/opensearch-project/job-scheduler/pull/509">#509</a>)</li>
<li>bump actions/create-release from 1.0.0 to 1.1.4 (<a href="https://github.com/opensearch-project/job-scheduler/pull/514">#514</a>)(<a href="https://github.com/opensearch-project/job-scheduler/pull/521">#521</a>)</li>
<li>bump codecov/codecov-action from 1 to 3 (<a href="https://github.com/opensearch-project/job-scheduler/pull/513">#513</a>)(<a href="https://github.com/opensearch-project/job-scheduler/pull/520">#520</a>)</li>
<li>bump actions/upload-artifact from 1 to 3 (<a href="https://github.com/opensearch-project/job-scheduler/pull/512">#512</a>) (<a href="https://github.com/opensearch-project/job-scheduler/pull/519">#519</a>)</li>
<li>bump tibdex/github-app-token from 1.5.0 to 2.1.0 (<a href="https://github.com/opensearch-project/job-scheduler/pull/511">#511</a>)(<a href="https://github.com/opensearch-project/job-scheduler/pull/518">#518</a>)</li>
<li>bump com.diffplug.spotless from 6.21.0 to 6.22.0 (<a href="https://github.com/opensearch-project/job-scheduler/pull/510">#510</a>)(<a href="https://github.com/opensearch-project/job-scheduler/pull/517">#517</a>)</li>
<li>bump VachaShah/backport from 1.1.4 to 2.2.0 (<a href="https://github.com/opensearch-project/job-scheduler/pull/515">#515</a>)(<a href="https://github.com/opensearch-project/job-scheduler/pull/516">#516</a>)</li>
</ul>

<h3>Opensearch KNN</h3>

<ul>
<li>Update bytebuddy to 1.14.7 <a href="https://github.com/opensearch-project/k-NN/pull/1135">#1135</a></li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Ignoring Redeploy test on MacOS due to known failures (<a href="https://github.com/opensearch-project/ml-commons/pull/1414">#1414</a>)</li>
<li>throw exception when model group not found during update request (<a href="https://github.com/opensearch-project/ml-commons/pull/1447">#1447</a>)</li>
<li>Add a setting to control the update connector API (<a href="https://github.com/opensearch-project/ml-commons/pull/1274">#1274</a>)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Consumed latest changes from core, use QueryPhaseSearcherWrapper as parent class for Hybrid QPS (<a href="https://github.com/opensearch-project/neural-search/pull/356">#356</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Bump bwc version to 2.11(<a href="https://github.com/opensearch-project/notifications/pull/763">#763</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Depreceate NodeStatsFixedShardsMetricsCollector in favor of NodeStatsAllShardsMetricsCollector <a href="https://github.com/opensearch-project/performance-analyzer/pull/551">#551</a></li>
<li>Add tracer to getTransports <a href="https://github.com/opensearch-project/performance-analyzer/pull/556">#556</a></li>
</ul>

<h3>Opensearch Reporting</h3>

<ul>
<li>Update demo certs used in integ tests (<a href="https://github.com/opensearch-project/reporting/pull/755">#755</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Change log message from warning to trace on WWW-Authenticate challenge (<a href="https://github.com/opensearch-project/security/pull/3446">#3446</a>)</li>
<li>Disable codecov from failing CI if there is an upload issue (<a href="https://github.com/opensearch-project/security/pull/3379">#3379</a>)</li>
<li>[Refactor] Change HTTP routes for Audit and Config PUT methods   (<a href="https://github.com/opensearch-project/security/pull/3407">#3407</a>)</li>
<li>Add tracer to Transport (<a href="https://github.com/opensearch-project/security/pull/3463">#3463</a>)</li>
<li>Adds opensearch trigger bot to discerning merger list to allow automatic merges (<a href="https://github.com/opensearch-project/security/pull/3481">#3481</a>)</li>
<li>Bump org.apache.camel:camel-xmlsecurity from 3.21.0 to 3.21.1 (<a href="https://github.com/opensearch-project/security/pull/3436">#3436</a>)</li>
<li>Bump com.github.wnameless.json:json-base from 2.4.2 to 2.4.3 (<a href="https://github.com/opensearch-project/security/pull/3437">#3437</a>)</li>
<li>Bump org.xerial.snappy:snappy-java from 1.1.10.4 to 1.1.10.5 (<a href="https://github.com/opensearch-project/security/pull/3438">#3438</a>)</li>
<li>Bump org.ow2.asm:asm from 9.5 to 9.6 (<a href="https://github.com/opensearch-project/security/pull/3439">#3439</a>)</li>
<li>Bump org.xerial.snappy:snappy-java from 1.1.10.3 to 1.1.10.4 (<a href="https://github.com/opensearch-project/security/pull/3396">#3396</a>)</li>
<li>Bump com.google.errorprone:error_prone_annotations from 2.21.1 to 2.22.0 (<a href="https://github.com/opensearch-project/security/pull/3400">#3400</a>)</li>
<li>Bump org.passay:passay from 1.6.3 to 1.6.4 (<a href="https://github.com/opensearch-project/security/pull/3397">#3397</a>)</li>
<li>Bump org.gradle.test-retry from 1.5.4 to 1.5.5 (<a href="https://github.com/opensearch-project/security/pull/3399">#3399</a>)</li>
<li>Bump org.springframework:spring-core from 5.3.29 to 5.3.30 (<a href="https://github.com/opensearch-project/security/pull/3398">#3398</a>)</li>
<li>Bump tibdex/github-app-token from 2.0.0 to 2.1.0 (<a href="https://github.com/opensearch-project/security/pull/3395">#3395</a>)</li>
<li>Bump org.apache.ws.xmlschema:xmlschema-core from 2.3.0 to 2.3.1 (<a href="https://github.com/opensearch-project/security/pull/3374">#3374</a>)</li>
<li>Bump apache_cxf_version from 4.0.2 to 4.0.3 (<a href="https://github.com/opensearch-project/security/pull/3376">#3376</a>)</li>
<li>Bump org.springframework:spring-beans from 5.3.29 to 5.3.30 (<a href="https://github.com/opensearch-project/security/pull/3375">#3375</a>)</li>
<li>Bump com.github.wnameless.json:json-flattener from 0.16.5 to 0.16.6 (<a href="https://github.com/opensearch-project/security/pull/3371">#3371</a>)</li>
<li>Bump aws-actions/configure-aws-credentials from 3 to 4 (<a href="https://github.com/opensearch-project/security/pull/3373">#3373</a>)</li>
<li>Bump org.checkerframework:checker-qual from 3.36.0 to 3.38.0 (<a href="https://github.com/opensearch-project/security/pull/3378">#3378</a>)</li>
<li>Bump com.nulab-inc:zxcvbn from 1.8.0 to 1.8.2 (<a href="https://github.com/opensearch-project/security/pull/3357">#3357</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Bump version to 2.11. (<a href="https://github.com/opensearch-project/security-analytics/pull/631">#631</a>)</li>
</ul>

<h2>REFACTORING</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Optimize doc-level monitor workflow for index patterns. (<a href="https://github.com/opensearch-project/alerting/pull/1122">#1122</a>)</li>
<li>Add workflow null or empty check only when empty workflow id passed. ([#1139(https://github.com/opensearch-project/alerting/pull/1139))</li>
<li>Add primary first calls for different monitor types. (<a href="https://github.com/opensearch-project/alerting/pull/1205">#1205</a>)</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>[2.x] Fix TransportService constructor due to changes in core plus guava bump (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1069">#1069</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>register new versions to a model group based on the name provided (<a href="https://github.com/opensearch-project/ml-commons/pull/1452">#1452</a>)</li>
<li>if model version fails to register, update model group accordingly (<a href="https://github.com/opensearch-project/ml-commons/pull/1463">#1463</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Address search request timeouts as transient error. (<a href="https://github.com/opensearch-project/security-analytics/pull/561">#561</a>)</li>
<li>Change ruleId if it exists. (<a href="https://github.com/opensearch-project/security-analytics/pull/628">#628</a>)</li>
</ul>

<h3>SQL</h3>

<ul>
<li>Merging Async Query APIs feature branch into main. in https://github.com/opensearch-project/sql/pull/2163</li>
<li>Removed Domain Validation in https://github.com/opensearch-project/sql/pull/2136</li>
<li>Check for existence of security plugin in https://github.com/opensearch-project/sql/pull/2069</li>
<li>Always use snapshot version for security plugin download in https://github.com/opensearch-project/sql/pull/2061</li>
<li>Add customized result index in data source etc in https://github.com/opensearch-project/sql/pull/2220</li>
</ul>

<h2>EXPERIMENTAL</h2>

<h3>Opensearch ML Common</h3>

<ul>
<li>Update Connector API (<a href="https://github.com/opensearch-project/ml-commons/pull/1227">#1227</a>)</li>
</ul>

<h2>NON-COMPLIANT</h2>
<h2>SECURITY</h2>
<h3>SQL</h3>
<ul>
<li>bump okhttp to 4.10.0 (#2043) by @joshuali925 in https://github.com/opensearch-project/sql/pull/2044</li>
<li>bump okio to 3.4.0 by @joshuali925 in https://github.com/opensearch-project/sql/pull/2047</li>
</ul>
<hr />
<p><strong>Full Changelog</strong>: https://github.com/opensearch-project/sql/compare/2.3.0.0...v.2.11.0.0</p>
