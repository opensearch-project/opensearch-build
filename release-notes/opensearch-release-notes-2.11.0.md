OpenSearch and OpenSearch Dashboards 2.11.0 Release Notes

## Release Highlights

OpenSearch 2.11.0 introduces an array of features for semantic search applications, new options for durable data storage, and new functionality for security analytics, observability, and more. Experimental features include new tools for tracing OpenSearch requests and enhancements for conversational search pipelines.

### New Features

* Multimodal semantic search lets you combine images with text, adding valuable context to support better relevancy for search results.
* Sparse retrieval is now available for text-based vector search. OpenSearch now offers both sparse and dense retrieval methods so you can choose the approach that suits your application requirements.
* The search comparison tool is now generally available, allowing you to compare the results of two different search ranking techniques side by side so you can identify opportunities to fine-tune your results.
* Snapshots are now interoperable with remote-backed storage, offering another approach to data durability with the potential to reduce storage resource requirements.
* Updates to the Security Analytics interface are designed to make it easier to use the security toolkit, introducing a new workflow to simplify creation of threat detectors and alerts as well as the ability to organize log types by category.
* OpenSearch can now facilitate authorization at the REST layer, empowering plugin developers to establish secure access controls over endpoints in addition to transport layer authorization.
* This release removes dependencies on AngularJS, helping modernize and improve the security posture of OpenSearch Dashboards. A recent announcement of this update with additional details can be found [here](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/4993)

### Experimental Features

OpenSearch 2.11.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.

* The ability to track OpenSearch requests with traces is new for 2.11, allowing developers to follow OpenSearch requests and tasks as they traverse components and services across the distributed architecture, monitor the path of requests through the system, measure request latencies, and more.
* Updates to the conversational search tools introduced as experimental in 2.10 offer several parameters that can be used to customize retrieval augmented generation pipelines, providing core logic that allows you to adapt the way OpenSearch interacts with large language learning models as part of generative AI applications.

## Release Details
[OpenSearch and OpenSearch Dashboards 2.11.0](https://opensearch.org/versions/opensearch-2-11-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.11/release-notes/opensearch.release-notes-2.11.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.11/release-notes/opensearch-dashboards.release-notes-2.11.0.md).

## FEATURES


### OpenSearch Alerting Dashboards
* Support any channel types from Notification. ([#743](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/743))


### OpenSearch Dashboards Notifications
* Improve wording for TLS-related options ([#115](https://github.com/opensearch-project/dashboards-notifications/pull/115))


### OpenSearch Dashboards Observability
* Add nightly cron schedule to E2E workflow in ([#1005](https://github.com/opensearch-project/dashboards-observability/pull/1005))
* Create Data sources plugin with Manage Datasources Flow in ([#1035](https://github.com/opensearch-project/dashboards-observability/pull/1035))
* Configure S3 datasource flow  in ([#1049](https://github.com/opensearch-project/dashboards-observability/pull/1049))
* Create prometheus datasource flow  in ([#1054](https://github.com/opensearch-project/dashboards-observability/pull/1054))
* Adding redirection to query workbench in ([#1063](https://github.com/opensearch-project/dashboards-observability/pull/1063))
* Setup S3 connection with integrations in ([#1057](https://github.com/opensearch-project/dashboards-observability/pull/1057))
* Support SQL direct query in Observability in ([#988](https://github.com/opensearch-project/dashboards-observability/pull/988))
* Support SQL direct updated - query in Observability (#988) in ([#1072](https://github.com/opensearch-project/dashboards-observability/pull/1072))
* Metrics Explorer - single-line graph only, no legends in ([#1068](https://github.com/opensearch-project/dashboards-observability/pull/1068))
* Metrics Explorer - updated - single-line graph only, no legends in ([#1073](https://github.com/opensearch-project/dashboards-observability/pull/1073))


### OpenSearch Dashboards Query Workbench
* Add table acceleration flyout ([#128](https://github.com/opensearch-project/dashboards-query-workbench/pull/128)) ([#135](https://github.com/opensearch-project/dashboards-query-workbench/pull/135)) ([#137](https://github.com/opensearch-project/dashboards-query-workbench/pull/137)) ([#140](https://github.com/opensearch-project/dashboards-query-workbench/pull/140))
* Update validations for acceleration ([#133](https://github.com/opensearch-project/dashboards-query-workbench/pull/133))
* Add materialized view visual builder and query builder ([#129](https://github.com/opensearch-project/dashboards-query-workbench/pull/129))
* Add async query support ([#131](https://github.com/opensearch-project/dashboards-query-workbench/pull/131)) ([#136](https://github.com/opensearch-project/dashboards-query-workbench/pull/136))
* Add skipping index queries ([#134](https://github.com/opensearch-project/dashboards-query-workbench/pull/134))
* Add acceleration for opensearch-spark ([#139](https://github.com/opensearch-project/dashboards-query-workbench/pull/139))


### OpenSearch Dashboards Reporting
* Enable Reporting for new OSD Discover module ([#184](https://github.com/opensearch-project/dashboards-reporting/pull/184)) ([#190](https://github.com/opensearch-project/dashboards-reporting/pull/190)) ([#212](https://github.com/opensearch-project/dashboards-reporting/pull/212))


### OpenSearch Neural Search
* Support sparse semantic retrieval by introducing `sparse_encoding` ingest processor and query builder ([#333](https://github.com/opensearch-project/neural-search/pull/333))
* Enabled support for applying default modelId in neural search query ([#337](https://github.com/opensearch-project/neural-search/pull/337)
* Added Multimodal semantic search feature ([#359](https://github.com/opensearch-project/neural-search/pull/359))


## ENHANCEMENTS


### OpenSearch Alerting
* Add logging for execution and indexes of monitors and workflows. ([#1223](https://github.com/opensearch-project/alerting/pull/1223))


### OpenSearch Dashboards Search Relevance
* Adding error messages in Search Comparison Tool ([#267](https://github.com/opensearch-project/dashboards-search-relevance/pull/267)) ([#305](https://github.com/opensearch-project/dashboards-search-relevance/pull/305))
* Remove Experimental Tag ([#302](https://github.com/opensearch-project/dashboards-search-relevance/pull/302)) ([#313](https://github.com/opensearch-project/dashboards-search-relevance/pull/313))


### OpenSearch Index Management
* Provide unique id for each rollup job and add debug logs. ([#968](https://github.com/opensearch-project/index-management/pull/968))


### OpenSearch k-NN
* Added support for ignore_unmapped in KNN queries. [#1071](https://github.com/opensearch-project/k-NN/pull/1071)
* Add graph creation stats to the KNNStats API. [#1141](https://github.com/opensearch-project/k-NN/pull/1141)


### OpenSearch ML Commons
* Add neural search default processor for non OpenAI/Cohere scenario ([#1274](https://github.com/opensearch-project/ml-commons/pull/1274))
* Add tokenizer and sparse encoding ([#1301](https://github.com/opensearch-project/ml-commons/pull/1301))
* Allow input null for text docs input ([#1402](https://github.com/opensearch-project/ml-commons/pull/1402))
* Add support for context_size and include 'interaction_id' in SearchRequest ([#1385](https://github.com/opensearch-project/ml-commons/pull/1385))
* Adding model level metric in node level ([#1330](https://github.com/opensearch-project/ml-commons/pull/1330))
* Add status code to model tensor ([#1443](https://github.com/opensearch-project/ml-commons/pull/1443))
* Add bedrockURL to trusted connector regex list ([#1461](https://github.com/opensearch-project/ml-commons/pull/1461))
* Performance enhacement for predict action by caching model info ([#1472](https://github.com/opensearch-project/ml-commons/pull/1472))


### OpenSearch Neural Search
* Add `max_token_score` parameter to improve the execution efficiency for `neural_sparse` query clause ([#348](https://github.com/opensearch-project/neural-search/pull/348))


### OpenSearch Security Analytics Dashboards
* Ux improvements for correlations page. ([#732](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/732))
* Simplify detector creation UX. ([#738](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/738))
* Added categories for log types. ([#741](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/741))
* Enhance log type filters correlations. ([#745](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/745))


### OpenSearch Security Analytics
* Adds support for alerts and triggers on group by based sigma rules. ([#545](https://github.com/opensearch-project/security-analytics/pull/545))
* Auto expand replicas. ([#547](https://github.com/opensearch-project/security-analytics/pull/547))
* Auto expand replicas for logtype index. ([#568](https://github.com/opensearch-project/security-analytics/pull/568))
* Adding WAF Log type. ([#617](https://github.com/opensearch-project/security-analytics/pull/617))
* Add category to custom log types. ([#634](https://github.com/opensearch-project/security-analytics/pull/634))


### OpenSearch Security
* Authorization in Rest Layer ([#2753](https://github.com/opensearch-project/security/pull/2753))
* Improve serialization speeds ([#2802](https://github.com/opensearch-project/security/pull/2802))
* Integration tests framework ([#3388](https://github.com/opensearch-project/security/pull/3388))
* Allow for automatic merging of dependabot changes after checks pass ([#3409](https://github.com/opensearch-project/security/pull/3409))
* Support security config updates on the REST API using permission([#3264](https://github.com/opensearch-project/security/pull/3264))
* Expanding Authentication with SecurityRequest Abstraction ([#3430](https://github.com/opensearch-project/security/pull/3430))
* Add early rejection from RestHandler for unauthorized requests ([#3418](https://github.com/opensearch-project/security/pull/3418))


### SQL
*  Enable PPL lang and add datasource to async query API in https://github.com/opensearch-project/sql/pull/2195
*  Refactor Flint Auth in https://github.com/opensearch-project/sql/pull/2201
*  Add conf for spark structured streaming job in https://github.com/opensearch-project/sql/pull/2203
*  Submit long running job only when auto_refresh = false in https://github.com/opensearch-project/sql/pull/2209
*  Bug Fix, handle DESC TABLE response in https://github.com/opensearch-project/sql/pull/2213
*  Drop Index Implementation in https://github.com/opensearch-project/sql/pull/2217
*  Enable PPL Queries in https://github.com/opensearch-project/sql/pull/2223
*  Read extra Spark submit parameters from cluster settings in https://github.com/opensearch-project/sql/pull/2236
*  Spark Execution Engine Config Refactor in https://github.com/opensearch-project/sql/pull/2266
*  Provide auth.type and auth.role_arn paramters in GET Datasource API response. in https://github.com/opensearch-project/sql/pull/2283
*  Add support for `date_nanos` and tests. (#337) in https://github.com/opensearch-project/sql/pull/2020
*  Applied formatting improvements to Antlr files based on spotless changes (#2017) by @MitchellGale in https://github.com/opensearch-project/sql/pull/2023
*  Revert "Guarantee datasource read api is strong consistent read (#1815)" in https://github.com/opensearch-project/sql/pull/2031
*  Add _primary preference only for segment replication enabled indices in https://github.com/opensearch-project/sql/pull/2045
*  Changed allowlist config to denylist ip config for datasource uri hosts in https://github.com/opensearch-project/sql/pull/2058


## BUG FIXES


### OpenSearch Alerting
* Fix workflow execution for first run. ([#1227](https://github.com/opensearch-project/alerting/pull/1227))


### OpenSearch Anomaly Detection Dashboards
* Prevent empty task IDs passed to server side ([#616](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/616))


### OpenSearch Dashboards Observability
* Update E2E Test Config in ([#1025](https://github.com/opensearch-project/dashboards-observability/pull/1025))
* Adjust explorer chart color and spacing in ([#1051](https://github.com/opensearch-project/dashboards-observability/pull/1051))
* Modified explorer data grid to follow discover look and feel in ([#1041](https://github.com/opensearch-project/dashboards-observability/pull/1041))
* Fix missing import 'moment' on query_utils. in ([#1067](https://github.com/opensearch-project/dashboards-observability/pull/1067))
* Data sources copy updates  in ([#1092](https://github.com/opensearch-project/dashboards-observability/pull/1092))
* Explorer minor UI updates  in ([#1100](https://github.com/opensearch-project/dashboards-observability/pull/1100))
* Reverting notebooks changes, add docs/validation to datasources, explorer minor in ([#1103](https://github.com/opensearch-project/dashboards-observability/pull/1103))
* Add callout and modify content for S3 datasource  in ([#1113](https://github.com/opensearch-project/dashboards-observability/pull/1113))
* Fix dropdown display behavior  in ([#1116](https://github.com/opensearch-project/dashboards-observability/pull/1116))
* Include minor UI fixes for Log Explorer  in ([#1119](https://github.com/opensearch-project/dashboards-observability/pull/1119))


### OpenSearch Dashboards Query Workbench
* Fix SQL UI buttons ([#149](https://github.com/opensearch-project/dashboards-query-workbench/pull/149))


### OpenSearch Dashboards Reporting
* Fix date-format in csv export ([#148](https://github.com/opensearch-project/dashboards-reporting/pull/148)) ([#211](https://github.com/opensearch-project/dashboards-reporting/pull/211))


### OpenSearch Dashboards Search Relevance
* Update border color of Search Relevance to be compliant with Dark Mode ([#315](https://github.com/opensearch-project/dashboards-search-relevance/pull/315)) ([#328](https://github.com/opensearch-project/dashboards-search-relevance/pull/328))
* Make ace editor theme consistent for Search Relevance plugin ([#300](https://github.com/opensearch-project/dashboards-search-relevance/pull/300)) ([#327](https://github.com/opensearch-project/dashboards-search-relevance/pull/327))


### OpenSearch Geospatial
* Fix flaky test, testIndexingMultiPolygon ([#483](https://github.com/opensearch-project/geospatial/pull/483))


### OpenSearch Index Management
* Fix auto managed index always have -2 seqNo bug. ([#924](https://github.com/opensearch-project/index-management/pull/924))


### OpenSearch ML Commons
* Fix parameter name in preprocess function ([#1362](https://github.com/opensearch-project/ml-commons/pull/1362))
* Fix spelling in Readme.md ([#1363](https://github.com/opensearch-project/ml-commons/pull/1363))
* Fix error message in TransportDeplpoyModelAction class ([#1368](https://github.com/opensearch-project/ml-commons/pull/1368))
* Fix null exception in text docs data set ([#1403](https://github.com/opensearch-project/ml-commons/pull/1403))
* Fix text docs input unescaped error; enable deploy remote model ([#1407](https://github.com/opensearch-project/ml-commons/pull/1407))
* Restore thread context before running action listener ([#1418](https://github.com/opensearch-project/ml-commons/pull/1418))
* Fix more places where thread context not restored ([#1421](https://github.com/opensearch-project/ml-commons/pull/1421))
* Fix BWC test suite ([#1426](https://github.com/opensearch-project/ml-commons/pull/1426))
* Support bwc for process function ([#1427](https://github.com/opensearch-project/ml-commons/pull/1427))
* Fix model group auto-deletion when last version is deleted ([#1444](https://github.com/opensearch-project/ml-commons/pull/1444))
* Fixing metrics correlation algorithm ([#1448](https://github.com/opensearch-project/ml-commons/pull/1448))
* Throw exception if remote model doesn't return 2xx status code; fix predict runner ([#1477](https://github.com/opensearch-project/ml-commons/pull/1477))
* Fix no worker node exception for remote embedding model ([#1482](https://github.com/opensearch-project/ml-commons/pull/1482))
* Fix for delete model group API throwing incorrect error when model index not created ([#1485](https://github.com/opensearch-project/ml-commons/pull/1485))
* Fix no worker node error on multi-node cluster ([#1487](https://github.com/opensearch-project/ml-commons/pull/1487))
* Fix prompt passing for Bedrock by passing a single string prompt for Bedrock models. ([#1490](https://github.com/opensearch-project/ml-commons/pull/1490))


### OpenSearch Neural Search
* Fixed exception in Hybrid Query for one shard and multiple node ([#396](https://github.com/opensearch-project/neural-search/pull/396))


### OpenSearch Performance Analyzer
* Update Jooq version and address bind variable failure in AdmissionControl Emitter [#493](https://github.com/opensearch-project/performance-analyzer/pull/493)


### OpenSearch Security Analytics
* Fixes verifying workflow test when security is enabled. ([#563](https://github.com/opensearch-project/security-analytics/pull/563))
* Fix flaky integration tests. ([#581](https://github.com/opensearch-project/security-analytics/pull/581))
* Sigma Aggregation rule fixes. ([#622](https://github.com/opensearch-project/security-analytics/pull/622))


### OpenSearch Security
* Refactors reRequestAuthentication to call notifyIpAuthFailureListener before sending the response to the channel ([#3411](https://github.com/opensearch-project/security/pull/3411))
* For read-only tenants filter with allow list ([c3e53e2](https://github.com/opensearch-project/security/commit/c3e53e20a69dc8eb401653594a130c2a4fd4b6bd))


### OpenSearch Security Dashboards
* Fix OIDC refresh token flow when using the cookie splitter ([#1580](https://github.com/opensearch-project/security-dashboards-plugin/pull/1580))


### SQL
*  Fix broken link for connectors doc in https://github.com/opensearch-project/sql/pull/2199
*  Fix response codes returned by JSON formatting them in https://github.com/opensearch-project/sql/pull/2200
*  Bug fix, datasource API should be case sensitive in https://github.com/opensearch-project/sql/pull/2202
*  Minor fix in dropping covering index in https://github.com/opensearch-project/sql/pull/2240
*  Fix Unit tests for FlintIndexReader in https://github.com/opensearch-project/sql/pull/2242
*  Bug Fix , delete OpenSearch index when DROP INDEX in https://github.com/opensearch-project/sql/pull/2252
*  Correctly Set query status in https://github.com/opensearch-project/sql/pull/2232
*  Exclude generated files from spotless  in https://github.com/opensearch-project/sql/pull/2024
*  Fix mockito core conflict. in https://github.com/opensearch-project/sql/pull/2131
*  Fix `ASCII` function and groom UT for text functions. (#301) in https://github.com/opensearch-project/sql/pull/2029
*  Fixed response codes For Requests With security exception. in https://github.com/opensearch-project/sql/pull/2036


## INFRASTRUCTURE


### OpenSearch Alerting
* Ignore flaky security test suites. ([#1188](https://github.com/opensearch-project/alerting/pull/1188))


###  OpenSearch Anomaly Detection
* Add dependabot.yml ([#1026](https://github.com/opensearch-project/anomaly-detection/pull/1026))


### OpenSearch Dashboards Query Workbench
* Update sidebar design ([#138](https://github.com/opensearch-project/dashboards-query-workbench/pull/138))


### OpenSearch Dashboards Search Relevance
* Update CI to see error logs ([#316](https://github.com/opensearch-project/dashboards-search-relevance/pull/316)) ([#325](https://github.com/opensearch-project/dashboards-search-relevance/pull/325))


### OpenSearch Geospatial
* Add integration test against security enabled cluster ([#513](https://github.com/opensearch-project/geospatial/pull/513))


### OpenSearch Index Management
* Upload docker test cluster log. ([#964](https://github.com/opensearch-project/index-management/pull/964))
* Reduce test running time. ([#965](https://github.com/opensearch-project/index-management/pull/965))
* Parallel test run. ([#966](https://github.com/opensearch-project/index-management/pull/966))
* Security test filtered. ([#969](https://github.com/opensearch-project/index-management/pull/969))


### OpenSearch Performance Analyzer
* Update PULL_REQUEST_TEMPLATE.md [#560)](https://github.com/opensearch-project/performance-analyzer/pull/560)


### OpenSearch Security Analytics
* Ignore tests that may be flaky. ([#596](https://github.com/opensearch-project/security-analytics/pull/596))


### SQL
*  Bump aws-encryption-sdk-java to 1.71 in https://github.com/opensearch-project/sql/pull/2057
*  Run IT tests with security plugin (#335) #1986 by @MitchellGale in https://github.com/opensearch-project/sql/pull/2022


## DOCUMENTATION


### OpenSearch Alerting
* Added 2.11 release notes ([#1251](https://github.com/opensearch-project/alerting/pull/1251))


### OpenSearch Alerting Dashboards
* Add 2.11.0 release notes ([#764](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/764))


### OpenSearch Dashboards Notifications
* 2.11 release notes. ([#123](https://github.com/opensearch-project/dashboards-notifications/issues/123))


### OpenSearch Dashboards Observability
* Use approved svg from UX in ([#1066](https://github.com/opensearch-project/dashboards-observability/pull/1066))
* Add docker-compose.yml testing and readme for integration to 2.9 in ([#923](https://github.com/opensearch-project/dashboards-observability/pull/923))


### OpenSearch Index Management
* Added 2.11 release notes. ([#1004](https://github.com/opensearch-project/index-management/pull/1004))


### OpenSearch Notifications
* Add 2.11.0 release notes ([#774](https://github.com/opensearch-project/notifications/issues/774))


### OpenSearch Security Analytics Dashboards
* Added 2.11.0 release notes. ([#756](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/756))


### OpenSearch Security Analytics
* Added 2.11.0 release notes. ([#660](https://github.com/opensearch-project/security-analytics/pull/660))


### SQL
*  Datasource description in https://github.com/opensearch-project/sql/pull/2138
*  Add documentation for S3GlueConnector. in https://github.com/opensearch-project/sql/pull/2234


## MAINTENANCE


### OpenSearch Alerting
* Increment version to 2.11.0-SNAPSHOT. ([#1116](https://github.com/opensearch-project/alerting/pull/1116))


### OpenSearch Alerting Dashboards
* Incremented version to 2.11 ([#716](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/716))


### OpenSearch Asynchronous Search
* Increment version to 2.11.0 ([#446](https://github.com/opensearch-project/asynchronous-search/pull/446))


### OpenSearch Dashboards Maps
* Increment version to 2.11.0.0 ([#476](https://github.com/opensearch-project/dashboards-maps/pull/476))


### OpenSearch Dashboards Query Workbench
* Upgrade cypress dependency ([#120](https://github.com/opensearch-project/dashboards-query-workbench/pull/120))
* Upgrade packages and tsconfig ([#130](https://github.com/opensearch-project/dashboards-query-workbench/pull/130))
* Update CI workflow ([#146](https://github.com/opensearch-project/dashboards-query-workbench/pull/146))


### OpenSearch Dashboards Reporting
* Upgrade debug and other deps ([#208](https://github.com/opensearch-project/dashboards-reporting/pull/208))


### OpenSearch Dashboards Visualizations
* Increment Version to 2.11.0 ([#253](https://github.com/opensearch-project/dashboards-visualizations/pull/253))


### OpenSearch Index Management
* Increment version to 2.11.0-SNAPSHOT. ([#922](https://github.com/opensearch-project/index-management/pull/922))


### OpenSearch Job Scheduler
* Bump actions/upload-release-asset from 1.0.1 to 1.0.2 ([#504](https://github.com/opensearch-project/job-scheduler/pull/504))([#506](https://github.com/opensearch-project/job-scheduler/pull/506))
* Bump aws-actions/configure-aws-credentials from 1 to 4 ([#501](https://github.com/opensearch-project/job-scheduler/pull/501))([#507](https://github.com/opensearch-project/job-scheduler/pull/507))
* Bump com.netflix.nebula.ospackage from 11.4.0 to 11.5.0  ([#500](https://github.com/opensearch-project/job-scheduler/pull/500))([#508](https://github.com/opensearch-project/job-scheduler/pull/508))
* Manual backport of #503 ([#509](https://github.com/opensearch-project/job-scheduler/pull/509))
* Bump actions/create-release from 1.0.0 to 1.1.4 ([#514](https://github.com/opensearch-project/job-scheduler/pull/514))([#521](https://github.com/opensearch-project/job-scheduler/pull/521))
* Bump codecov/codecov-action from 1 to 3 ([#513](https://github.com/opensearch-project/job-scheduler/pull/513))([#520](https://github.com/opensearch-project/job-scheduler/pull/520))
* Bump actions/upload-artifact from 1 to 3 ([#512](https://github.com/opensearch-project/job-scheduler/pull/512)) ([#519](https://github.com/opensearch-project/job-scheduler/pull/519))
* Bump tibdex/github-app-token from 1.5.0 to 2.1.0 ([#511](https://github.com/opensearch-project/job-scheduler/pull/511))([#518](https://github.com/opensearch-project/job-scheduler/pull/518))
* Bump com.diffplug.spotless from 6.21.0 to 6.22.0 ([#510](https://github.com/opensearch-project/job-scheduler/pull/510))([#517](https://github.com/opensearch-project/job-scheduler/pull/517))
* Bump VachaShah/backport from 1.1.4 to 2.2.0 ([#515](https://github.com/opensearch-project/job-scheduler/pull/515))([#516](https://github.com/opensearch-project/job-scheduler/pull/516))


### OpenSearch k-NN
* Update bytebuddy to 1.14.7 [#1135](https://github.com/opensearch-project/k-NN/pull/1135)


### OpenSearch ML Commons
* Ignoring Redeploy test on MacOS due to known failures ([#1414](https://github.com/opensearch-project/ml-commons/pull/1414))
* Throw exception when model group not found during update request ([#1447](https://github.com/opensearch-project/ml-commons/pull/1447))
* Add a setting to control the update connector API ([#1274](https://github.com/opensearch-project/ml-commons/pull/1274))


### OpenSearch ML Commons Dashboards
* Increment version to 2.11.0.0 ([#265](https://github.com/opensearch-project/ml-commons-dashboards/pull/265))

### OpenSearch Neural Search
* Consumed latest changes from core, use QueryPhaseSearcherWrapper as parent class for Hybrid QPS ([#356](https://github.com/opensearch-project/neural-search/pull/356))


### OpenSearch Notifications
* Bump bwc version to 2.11([#763](https://github.com/opensearch-project/notifications/pull/763))


### OpenSearch Performance Analyzer
* Depreceate NodeStatsFixedShardsMetricsCollector in favor of NodeStatsAllShardsMetricsCollector [#551](https://github.com/opensearch-project/performance-analyzer/pull/551)
* Add tracer to getTransports [#556](https://github.com/opensearch-project/performance-analyzer/pull/556)


### OpenSearch Reporting
* Update demo certs used in integ tests ([#755](https://github.com/opensearch-project/reporting/pull/755))


### OpenSearch Security Analytics Dashboards
* Increment version to 2.11.0.0. ([#720](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/720))


### OpenSearch Security Analytics
* Bump version to 2.11. ([#631](https://github.com/opensearch-project/security-analytics/pull/631))


### OpenSearch Security
* Change log message from warning to trace on WWW-Authenticate challenge ([#3446](https://github.com/opensearch-project/security/pull/3446))
* Disable codecov from failing CI if there is an upload issue ([#3379](https://github.com/opensearch-project/security/pull/3379))
* [Refactor] Change HTTP routes for Audit and Config PUT methods   ([#3407](https://github.com/opensearch-project/security/pull/3407))
* Add tracer to Transport ([#3463](https://github.com/opensearch-project/security/pull/3463))
* Adds opensearch trigger bot to discerning merger list to allow automatic merges ([#3481](https://github.com/opensearch-project/security/pull/3481))
* Bump org.apache.camel:camel-xmlsecurity from 3.21.0 to 3.21.1 ([#3436](https://github.com/opensearch-project/security/pull/3436))
* Bump com.github.wnameless.json:json-base from 2.4.2 to 2.4.3 ([#3437](https://github.com/opensearch-project/security/pull/3437))
* Bump org.xerial.snappy:snappy-java from 1.1.10.4 to 1.1.10.5 ([#3438](https://github.com/opensearch-project/security/pull/3438))
* Bump org.ow2.asm:asm from 9.5 to 9.6 ([#3439](https://github.com/opensearch-project/security/pull/3439))
* Bump org.xerial.snappy:snappy-java from 1.1.10.3 to 1.1.10.4 ([#3396](https://github.com/opensearch-project/security/pull/3396))
* Bump com.google.errorprone:error_prone_annotations from 2.21.1 to 2.22.0 ([#3400](https://github.com/opensearch-project/security/pull/3400))
* Bump org.passay:passay from 1.6.3 to 1.6.4 ([#3397](https://github.com/opensearch-project/security/pull/3397))
* Bump org.gradle.test-retry from 1.5.4 to 1.5.5 ([#3399](https://github.com/opensearch-project/security/pull/3399))
* Bump org.springframework:spring-core from 5.3.29 to 5.3.30 ([#3398](https://github.com/opensearch-project/security/pull/3398))
* Bump tibdex/github-app-token from 2.0.0 to 2.1.0 ([#3395](https://github.com/opensearch-project/security/pull/3395))
* Bump org.apache.ws.xmlschema:xmlschema-core from 2.3.0 to 2.3.1 ([#3374](https://github.com/opensearch-project/security/pull/3374))
* Bump apache_cxf_version from 4.0.2 to 4.0.3 ([#3376](https://github.com/opensearch-project/security/pull/3376))
* Bump org.springframework:spring-beans from 5.3.29 to 5.3.30 ([#3375](https://github.com/opensearch-project/security/pull/3375))
* Bump com.github.wnameless.json:json-flattener from 0.16.5 to 0.16.6 ([#3371](https://github.com/opensearch-project/security/pull/3371))
* Bump aws-actions/configure-aws-credentials from 3 to 4 ([#3373](https://github.com/opensearch-project/security/pull/3373))
* Bump org.checkerframework:checker-qual from 3.36.0 to 3.38.0 ([#3378](https://github.com/opensearch-project/security/pull/3378))
* Bump com.nulab-inc:zxcvbn from 1.8.0 to 1.8.2 ([#3357](https://github.com/opensearch-project/security/pull/3357))

## REFACTORING


### OpenSearch Alerting
* Optimize doc-level monitor workflow for index patterns. ([#1122](https://github.com/opensearch-project/alerting/pull/1122))
* Add workflow null or empty check only when empty workflow id passed. ([#1139(https://github.com/opensearch-project/alerting/pull/1139))
* Add primary first calls for different monitor types. ([#1205](https://github.com/opensearch-project/alerting/pull/1205))


### OpenSearch Anomaly Detection
* [2.x] Fix TransportService constructor due to changes in core plus guava bump ([#1069](https://github.com/opensearch-project/anomaly-detection/pull/1069))


### OpenSearch ML Commons
* Register new versions to a model group based on the name provided ([#1452](https://github.com/opensearch-project/ml-commons/pull/1452))
* If model version fails to register, update model group accordingly ([#1463](https://github.com/opensearch-project/ml-commons/pull/1463))


### OpenSearch Security Analytics
* Address search request timeouts as transient error. ([#561](https://github.com/opensearch-project/security-analytics/pull/561))
* Change ruleId if it exists. ([#628](https://github.com/opensearch-project/security-analytics/pull/628))


### SQL
*  Merging Async Query APIs feature branch into main. in https://github.com/opensearch-project/sql/pull/2163
*  Removed Domain Validation in https://github.com/opensearch-project/sql/pull/2136
*  Check for existence of security plugin in https://github.com/opensearch-project/sql/pull/2069
*  Always use snapshot version for security plugin download in https://github.com/opensearch-project/sql/pull/2061
*  Add customized result index in data source etc in https://github.com/opensearch-project/sql/pull/2220
