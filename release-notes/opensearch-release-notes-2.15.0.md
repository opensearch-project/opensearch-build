# OpenSearch and OpenSearch Dashboards 2.15.0 Release Notes

## Release Highlights

OpenSearch 2.15 introduces new and expanded functionality to help you scale up performance and efficiency; advance stability, availability, and resiliency; and enhance your search applications, along with new machine learning (ML) capabilities and ease-of-use improvements.


### NEW AND UPDATED FEATURES

* Hybrid search, which combines neural search with lexical search to provide higher-quality results than when using either technique alone, can now apply parallel processing to subsearches at various stages of the process, resulting in significant reductions in query latency.
* New parallel and batch ingestion allow you to accelerate ingestion data processing for applications like neural search and reduce API calls to remote services.
* The new wildcard field type gives you the option to build an index using wildcard fields rather than tokens, offering more efficient search for fields that don’t have a natural token structure or when the number of distinct tokens is extremely large.
* New derived fields let you create new fields dynamically by executing scripts on existing fields, so you can manipulate document fields in real time and reduce storage requirements by avoiding direct indexing.
* A new performance optimization, dynamic pruning, offers improved performance for single-cardinality aggregations, with significant improvements in latency, particularly for fields with low cardinality.
* This release introduces support for Single Instruction, Multiple Data (SIMD) instruction sets for exact search queries. No additional configuration steps are required, and users can expect a significant reduction in query latencies compared to non-SIMD implementations.
* OpenSearch 2.15 introduces the ability to disable document values for the k-nn field when using the Lucene engine for vector search, offering reduced shard size for more efficient use of storage without impacting k-NN search functionality.
* You can now reduce downtime for migrations and rolling upgrades by using remote-backed storage for these operations. 
* This release adds the ability to identify the user, application, class of users, or workloads that generate a particular query, offering administrators new tools for measuring and controlling resource consumption.
* A new reindex workflow offers an easy way to enable vector and hybrid search on existing lexical indexes without spending time and resources reindexing source indexes.
* You can now configure remote ML models to serve as guardrails to detect toxic input and output from OpenSearch models. Previous versions only supported regex-based guardrails.
* The ML inference processor adds support for local models, which are models hosted on the search cluster's infrastructure. Previously, the processor only supported remote models, which connect to model provider APIs.
* An update to the ML Commons plugin allows you to use connectors to invoke any REST API function, enhancing the agent and tool functionality that was introduced in OpenSearch 2.13 with additional automation capabilities for ML workloads.
* Support for multiple data sources is extended to four external Dashboards plugins — Metrics Analytics, Security Analytics, Dashboards Assistant, and Alerting — as well as one core plugin, Timeline.


### EXPERIMENTAL FEATURES

* A new experimental feature allows users to enable cluster state publication through remote-backed storage. When enabled, this allows the follower nodes to fetch the state from the remote store directly, reducing memory and communication overhead on the cluster manager node.


## Release Details
[OpenSearch and OpenSearch Dashboards 2.15.0](https://opensearch.org/versions/opensearch-2-15-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.15/release-notes/opensearch.release-notes-2.15.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.15/release-notes/opensearch-dashboards.release-notes-2.15.0.md).



## FEATURES


### Opensearch Alerting Dashboards Plugin


* Initial PR to enable MDS support for Monitors and Alerts Triggers within the Alerting Plugin. ([#949](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/949))
* Support MDS in feature anywhere. ([#964](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/964))


### Opensearch Anomaly Detection Dashboards


* Support MDS in feature anywhere ([#767](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/767))
* Update create detector page and detector detail page to add custom result index lifecycle management settings ([#770](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/770))


### OpenSearch Dashboards Assistant


* Add data source service. ([#191](https://github.com/opensearch-project/dashboards-assistant/pull/191))
* Update router and controller to support MDS. ([#190](https://github.com/opensearch-project/dashboards-assistant/pull/190))
* Hide notebook feature when MDS enabled and remove security dashboard plugin dependency. ([#201](https://github.com/opensearch-project/dashboards-assistant/pull/201))
* Refactor default data source retriever. ([#197](https://github.com/opensearch-project/dashboards-assistant/pull/197))
* Reset chat and reload history after data source change. ([#194](https://github.com/opensearch-project/dashboards-assistant/pull/194))
* Add patch style for fixed position components.([#203](https://github.com/opensearch-project/dashboards-assistant/pull/203))


### Opensearch Common Utils


* CorrelationAlert model added ([#631](https://github.com/opensearch-project/common-utils/pull/631), [#679](https://github.com/opensearch-project/common-utils/pull/679))


### Opensearch Custom Codecs


* Add hardware-accelerated codecs for DEFLATE and LZ4


### Opensearch ML Commons


* Add connector tool ([#2516](https://github.com/opensearch-project/ml-commons/pull/2516))
* Guardrails model support ([#2491](https://github.com/opensearch-project/ml-commons/pull/2491))


### Opensearch Neural Search


* Speed up NeuralSparseQuery by two-phase using a custom search pipeline ([#646](https://github.com/opensearch-project/neural-search/issues/646))
* Support batchExecute in TextEmbeddingProcessor and SparseEncodingProcessor ([#743](https://github.com/opensearch-project/neural-search/issues/743))


### OpenSearch Observability Dashboards


* Implement upload flyout for integrations ([#1897](https://github.com/opensearch-project/dashboards-observability/pull/1897))
* Metrics analytics support for MDS ([#1895](https://github.com/opensearch-project/dashboards-observability/pull/1895))
* Add `applicable_data_sources` field to workflows definition ([#1888](https://github.com/opensearch-project/dashboards-observability/pull/1888))
* Trace Analytics v2 update - adding in conext views, updating filter, … ([#1885](https://github.com/opensearch-project/dashboards-observability/pull/1885))
* Add 'check for version' link in the integration details page ([#1879](https://github.com/opensearch-project/dashboards-observability/pull/1879))
* Integration enhancements ([#1870](https://github.com/opensearch-project/dashboards-observability/pull/1870))
* Bug fix for data-sources page ([#1830](https://github.com/opensearch-project/dashboards-observability/pull/1830))
* Move Cypress related dependencies to devDependencies and remove one unused dependency ([#1829](https://github.com/opensearch-project/dashboards-observability/pull/1829))
* Improve query assist user experiences ([#1817](https://github.com/opensearch-project/dashboards-observability/pull/1817))
* Add JSON5 parsing capabilities for integration configs ([#1815](https://github.com/opensearch-project/dashboards-observability/pull/1815))
* Refactor all the integrations with Amazon branding instead of AWS ([#1787](https://github.com/opensearch-project/dashboards-observability/pull/1787))
* Add otel services support integration ([#1769](https://github.com/opensearch-project/dashboards-observability/pull/1769))
* MDS Support for trace analytics ([#1752](https://github.com/opensearch-project/dashboards-observability/pull/1752))
* Add skipping indices for all integrations that have sample queries ([#1747](https://github.com/opensearch-project/dashboards-observability/pull/1747))
* Add saved queries to vpc flow ([#1744](https://github.com/opensearch-project/dashboards-observability/pull/1744))
* Added fix for jobs and cache Support for workbench ,MDS support ([#1739](https://github.com/opensearch-project/dashboards-observability/pull/1739))
* Cloud trails saved queries integration ([#1737](https://github.com/opensearch-project/dashboards-observability/pull/1737))


### Opensearch Performance Analyzer


* Framework changes to merge PA with RTF ([#662](https://github.com/opensearch-project/performance-analyzer/pull/662))


### Opensearch Security Analytics


* Alerts in correlations [Experminental] ([#1040](https://github.com/opensearch-project/security-analytics/pull/1040))
* Alerts in Correlations Part 2 ([#1062](https://github.com/opensearch-project/security-analytics/pull/1062))


### Opensearch Security Analytics Dashboards


* [MDS][Part 1] Data source component added to all pages. ([#1003](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1003))
* Show all related docs for a finding. ([#1006](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1006))
* Enhanced UI for rendering multiple documents in finding details flyout. ([#1014](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1014))
* [MDS][Part 2] Added server-side glue code to use data source id when getting opensearch client for making API calls to cluster. ([#1008](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1008))
* [MDS][Part 3] Wired all UI components to the data source menu. ([#1029](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1029))


### Opensearch k-NN


* Use the Lucene Distance Calculation Function in Script Scoring for doing exact search [#1699](https://github.com/opensearch-project/k-NN/pull/1699)


### OpenSearch SQL


* Support Percentile in PPL ([#2710](https://github.com/opensearch-project/sql/pull/2710))


## ENHANCEMENTS


### Opensearch Alerting


* Add `start_time` and `end_time` to GetAlertsRequest. ([#1551](https://github.com/opensearch-project/alerting/pull/1551))
* Add Alerting Comments experimental feature ([#1561](https://github.com/opensearch-project/alerting/pull/1561))


### Opensearch Anomaly Detection


* Refinement of Forecasting and AD Precision/Recall Improvements ([#1210](https://github.com/opensearch-project/anomaly-detection/pull/1210))
* Make jvm heap usage a dynamic setting ([#1212](https://github.com/opensearch-project/anomaly-detection/pull/1212))
* Add custom result index lifecycle management condition fields to config ([#1215](https://github.com/opensearch-project/anomaly-detection/pull/1215))
* Make Custom Result Index Name an Alias ([#1225](https://github.com/opensearch-project/anomaly-detection/pull/1225))
* Add custom result index lifecycle management ([#1232](https://github.com/opensearch-project/anomaly-detection/pull/1232))
* Merge Single-Stream and HC Detector Profiling Workflows ([#1237](https://github.com/opensearch-project/anomaly-detection/pull/1237))


### Opensearch Anomaly Detection Dashboards


* Update Frontend for Custom Result Index Query and Fix Issues ([#772](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/772))


### OpenSearch Build


* Enhance the stability of integration test runs, achieving passing test results on plugins of the distribution builds without requiring manual sign-offs.
  * Add condition for OSD integ tests on deb and rpm ([#4770](https://github.com/opensearch-project/opensearch-build/pull/4770))
  * Make endpoint_string one line for ccr test ([#4794](https://github.com/opensearch-project/opensearch-build/pull/4794))
  * Add ci-groups changes for OSD tests ([#4796](https://github.com/opensearch-project/opensearch-build/pull/4796))
  * Add cleanup for the data dir after integtests ([#4798](https://github.com/opensearch-project/opensearch-build/pull/4798))

### Opensearch Common Utils


* Add `start_time` and `end_time` filters to GetAlertsRequest. ([#655](https://github.com/opensearch-project/common-utils/pull/655))
* Added new models for Alerting Comments ([#663](https://github.com/opensearch-project/common-utils/pull/663), [#671](https://github.com/opensearch-project/common-utils/pull/671), [#674](https://github.com/opensearch-project/common-utils/pull/674) [#678](https://github.com/opensearch-project/common-utils/pull/678))


### Opensearch Flow Framework


* Add Workflow Step for Reindex from source index to destination ([#718](https://github.com/opensearch-project/flow-framework/pull/718))
* Add param to delete workflow API to clear status even if resources exist ([#719](https://github.com/opensearch-project/flow-framework/pull/719))
* Add additional default use cases ([#731](https://github.com/opensearch-project/flow-framework/pull/731))
* Add conversation search default use case with RAG tool ([#732](https://github.com/opensearch-project/flow-framework/pull/732))


### Opensearch Index Management Dashboards Plugin


* Specify `_all` as target in ClearCacheModal ([#1020](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1020))


### Opensearch ML Common


* Hanlde the throttling error in the response header ([#2442](https://github.com/opensearch-project/ml-commons/pull/2442))
* Implementing retry for remote connector to mitigate throttling issue ([#2462](https://github.com/opensearch-project/ml-commons/pull/2462))
* ML inference ingest processor support for local models ([#2508](https://github.com/opensearch-project/ml-commons/pull/2508))
* Add setting to allow private IP ([#2534](https://github.com/opensearch-project/ml-commons/pull/2534))
* Add IMMEDIATE refresh policy ([#2541](https://github.com/opensearch-project/ml-commons/pull/2541))


### Opensearch Neural Search


* Pass empty doc collector instead of top docs collector to improve hybrid query latencies by 20% ([#731](https://github.com/opensearch-project/neural-search/pull/731))
* Optimize parameter parsing in text chunking processor ([#733](https://github.com/opensearch-project/neural-search/pull/733))
* Use lazy initialization for priority queue of hits and scores to improve latencies by 20% ([#746](https://github.com/opensearch-project/neural-search/pull/746))
* Optimize max score calculation in the Query Phase of the Hybrid Search ([765](https://github.com/opensearch-project/neural-search/pull/765))
* Implement parallel execution of sub-queries for hybrid search ([#749](https://github.com/opensearch-project/neural-search/pull/749))


### Opensearch Security


* Replace BouncyCastle's OpenBSDBCrypt use with password4j for password hashing and verification ([#4428](https://github.com/opensearch-project/security/pull/4428))
* Adds validation for the action groups type key ([#4411](https://github.com/opensearch-project/security/pull/4411))
* Made sensitive header log statement more clear ([#4372](https://github.com/opensearch-project/security/pull/4372))
* Refactor ActionGroup REST API test and partial fix #4166 ([#4371](https://github.com/opensearch-project/security/pull/4371))
* Support multiple audience for jwt authentication ([#4363](https://github.com/opensearch-project/security/pull/4363))
* Configure masking algorithm default ([#4345](https://github.com/opensearch-project/security/pull/4345))
* Remove static metaFields list and get version-specific values from core ([#4412](https://github.com/opensearch-project/security/pull/4412))


### Opensearch Security Dashboards Plugin


* Remove tenant tab when disabled via yaml ([#1960](https://github.com/opensearch-project/security-dashboards-plugin/pull/1960))
* Always show security screen and shows error page when trying to access forbidden data-source ([#1964](https://github.com/opensearch-project/security-dashboards-plugin/pull/1964))
* Provide ability to view password ([#1980](https://github.com/opensearch-project/security-dashboards-plugin/pull/1980))
* Make login screen input feels consistent ([#1993](https://github.com/opensearch-project/security-dashboards-plugin/pull/1993))


### Opensearch k-NN


* Add KnnCircuitBreakerException and modify exception message ([#1688](https://github.com/opensearch-project/k-NN/pull/1688))
* Add stats for radial search ([#1684](https://github.com/opensearch-project/k-NN/pull/1684))
* Support script score when doc value is disabled and fix misusing DISI ([#1696](https://github.com/opensearch-project/k-NN/pull/1696))
* Add validation for pq m parameter before training starts ([#1713](https://github.com/opensearch-project/k-NN/pull/1713))
* Block delete model requests if an index uses the model ([#1722](https://github.com/opensearch-project/k-NN/pull/1722))


### OpenSearch SQL


* Add option to use LakeFormation in S3Glue data source ([#2624](https://github.com/opensearch-project/sql/pull/2624))
* Remove direct ClusterState access in LocalClusterState ([#2717](https://github.com/opensearch-project/sql/pull/2717))


## BUG FIXES


### OpenSearch Observability Dashboards


* (query assist) revert removing backticks ([#1898](https://github.com/opensearch-project/dashboards-observability/pull/1898))
* Minor bug fixes for trace analytics v2 (#1894) ([#1893](https://github.com/opensearch-project/dashboards-observability/pull/1893))
* Manual backport of otel-metrics pr ([#1892](https://github.com/opensearch-project/dashboards-observability/pull/1892))
* Fix traces index schema bug ([#1865](https://github.com/opensearch-project/dashboards-observability/pull/1865))
* Traces-analytics bug fix for missing MDS id in flyout ([#1857](https://github.com/opensearch-project/dashboards-observability/pull/1857))
* Raw Vpc schema integration (1.0.0 parquet ) ([#1853](https://github.com/opensearch-project/dashboards-observability/pull/1853))
* Fix flint skipping index syntax issues ([#1846](https://github.com/opensearch-project/dashboards-observability/pull/1846))
* Fix window start backtick during MV creation ([#1823](https://github.com/opensearch-project/dashboards-observability/pull/1823))
* Fix data connection api 404 error ([#1810](https://github.com/opensearch-project/dashboards-observability/pull/1810))
* Remove defaulting to query assist time range ([#1805](https://github.com/opensearch-project/dashboards-observability/pull/1805))
* Backport prometheus fix to 2.x ([#1782](https://github.com/opensearch-project/dashboards-observability/pull/1782))
* [Bug fix] Add conditional rendering for data connection page's tabs ([#1756](https://github.com/opensearch-project/dashboards-observability/pull/1756))
* Removed update button from explorer ([#1755](https://github.com/opensearch-project/dashboards-observability/pull/1755))
* (query assist) remove caching agent id ([#1734](https://github.com/opensearch-project/dashboards-observability/pull/1734))
* Added placeholder change for metrics picker ([#1906](https://github.com/opensearch-project/dashboards-observability/pull/1906))


### Opensearch Alerting


* Reduce log lever for informative message. ([#1218](https://github.com/opensearch-project/alerting/pull/1218))
* Update cron-utils. ([#1503](https://github.com/opensearch-project/alerting/pull/1503))


### Opensearch Alerting Dashboards Plugin


* Bug fix and mds support for AD Plugin APIs. ([#962](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/962))


### Opensearch Anomaly Detection Dashboards


* Fix handling of special characters in categorical values ([#757](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/757))
* Fix Warning Message About Custom Result Index Despite Existing Indices ([#759](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/759))
* Fix index field not getting populated when editing a detector ([#783](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/783))


### Opensearch Common Utils


* Bug fixes for correlation Alerts ([#670](https://github.com/opensearch-project/common-utils/pull/670), [#680](https://github.com/opensearch-project/common-utils/pull/680))


### Opensearch Dashboards Maps


* Add data source reference id in data layer search request ([#623](https://github.com/opensearch-project/dashboards-maps/pull/623))


### Opensearch Dashboards Notifications


* Bug fixes to support mds in getSeverFeatures API ([#205](https://github.com/opensearch-project/dashboards-notifications/pull/205))


### Opensearch Dashboards Reporting


* Update dompurify version ([#350](https://github.com/opensearch-project/dashboards-reporting/pull/350))
* Fix url parsing ([#353](https://github.com/opensearch-project/dashboards-reporting/pull/353))


### Opensearch Flow Framework


* Add user mapping to Workflow State index ([#705](https://github.com/opensearch-project/flow-framework/pull/705))


### Opensearch Index Management


* Step Metadata Update on Index Rollover Timeout ([#1174](https://github.com/opensearch-project/index-management/pull/1174))


### Opensearch Index Management Dashboards Plugin


* Cypress: modify test to check for inequality ([#1017](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1017))


### Opensearch ML Common


* Fix memory CB bugs and upgrade UTs to compatible with core changes ([#2469](https://github.com/opensearch-project/ml-commons/pull/2469))
* Fix error of ML inference processor in foreach processor ([#2474](https://github.com/opensearch-project/ml-commons/pull/2474))
* Fix error message with unwrapping the root cause ([#2458](https://github.com/opensearch-project/ml-commons/pull/2458))
* Adding immediate refresh to delete model group request ([#2514](https://github.com/opensearch-project/ml-commons/pull/2514))
* Fix model still deployed after calling undeploy API ([#2510](https://github.com/opensearch-project/ml-commons/pull/2510))
* Fix bedrock embedding generation issue ([#2495](https://github.com/opensearch-project/ml-commons/pull/2495))
* Fix init encryption master key ([#2554](https://github.com/opensearch-project/ml-commons/pull/2554))


### Opensearch Neural Search


* Total hit count fix in Hybrid Query ([756](https://github.com/opensearch-project/neural-search/pull/756))
* Fix map type validation issue in multiple pipeline processors ([#661](https://github.com/opensearch-project/neural-search/pull/661))


### Opensearch Performance Analyzer


* Fixed the bug in CacheConfigMetricsCollector ([#657](https://github.com/opensearch-project/performance-analyzer/pull/657))


### Opensearch Query Workbench


* Added fix for runAsync query without mds id ([#323](https://github.com/opensearch-project/dashboards-query-workbench/pull/323))


* Flakey unit tests fix ([#339](https://github.com/opensearch-project/dashboards-query-workbench/pull/339))


### Opensearch Security


* Add cat/alias support for DNFOF ([#4440](https://github.com/opensearch-project/security/pull/4440))
* Add support for ipv6 ip address in user injection ([#4409](https://github.com/opensearch-project/security/pull/4409))
* [Fix #4280] Introduce new endpoint `_plugins/_security/api/certificates` ([#4355](https://github.com/opensearch-project/security/pull/4355))


### Opensearch Security Analytics


* Fix chained findings monitor logic in update detector flow ([#1019](https://github.com/opensearch-project/security-analytics/pull/1019))
* Change default filter to time based fields ([#1030](https://github.com/opensearch-project/security-analytics/pull/1030))


### Opensearch Security Analytics Dashboards


* [MDS fixes] Select default data source on load; re-order router paths for correct data source component rendering. ([#1036](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1036))


### Opensearch Security Dashboards Plugin


* Fix bugs where pages were stuck in error state ([#1944](https://github.com/opensearch-project/security-dashboards-plugin/pull/1944))
* Fix issue when using OpenID Authentication with serverBasePath ([#1899](https://github.com/opensearch-project/security-dashboards-plugin/pull/1899))
* Fixes issue with expiryTime of OIDC cookie that causes refreshToken workflow to be skipped ([#1990](https://github.com/opensearch-project/security-dashboards-plugin/pull/1990))


### Opensearch k-NN


* Block commas in model description ([#1692](https://github.com/opensearch-project/k-NN/pull/1692))
* Update threshold value after new result is added ([#1715](https://github.com/opensearch-project/k-NN/pull/1715))


### OpenSearch SQL


* Handle create index with batch FlintJob ([#2734](https://github.com/opensearch-project/sql/pull/2734))


## INFRASTRUCTURE


### Opensearch Anomaly Detection


* dependabot: bump com.diffplug.spotless from 6.24.0 to 6.25.0 ([#1184](https://github.com/opensearch-project/anomaly-detection/pull/1184))


### OpenSearch Build


* Add additional workflows to central promotion workflows ([#4753](https://github.com/opensearch-project/opensearch-build/pull/4753))
* Add support to validate both docker and ECR as image source ([#4762](https://github.com/opensearch-project/opensearch-build/pull/4762)) 
* Update the lib to 6.5.0 and add gradle-check-flaky-test-issue-creation.jenkinsfile ([#4777](https://github.com/opensearch-project/opensearch-build/pull/4777))


### Opensearch Job Scheduler


* Refer to the version of Mockito from core's buildSrc/version.properties ([#630](https://github.com/opensearch-project/job-scheduler/pull/630)), ([#631](https://github.com/opensearch-project/job-scheduler/pull/631))
* Codecov GitHub Action changed back to v3 ([#622](https://github.com/opensearch-project/job-scheduler/pull/622)), ([#623](https://github.com/opensearch-project/job-scheduler/pull/623))


### Opensearch ML Common


* Add IT for flow agent with CatIndexTool ([#2425](https://github.com/opensearch-project/ml-commons/pull/2425))
* Remove strict version dependency to compile minimum compatible version ([#2486](https://github.com/opensearch-project/ml-commons/pull/2486))
* Add IT flow agent with search index tool ([#2460](https://github.com/opensearch-project/ml-commons/pull/2460))
* Fix flaky IT ([#2530](https://github.com/opensearch-project/ml-commons/pull/2530))
* Disable jvm memory circuit breaker for IT ([#2540](https://github.com/opensearch-project/ml-commons/pull/2540))
* Fix flaky test of PredictionITTests and RestConnectorToolIT ([#2437](https://github.com/opensearch-project/ml-commons/pull/2437))


### Opensearch Neural Search


* Disable memory circuit breaker for integ tests ([#770](https://github.com/opensearch-project/neural-search/pull/770))


### Opensearch Performance Analyzer


* Bump PA to use 1.4.0 PA commons lib ([#664](https://github.com/opensearch-project/performance-analyzer/pull/664))


### OpenSearch SQL


* Increment version to 2.15.0-SNAPSHOT ([#2650](https://github.com/opensearch-project/sql/pull/2650))


## DOCUMENTATION


### Opensearch Alerting


* Added 2.15 release notes. ([#1569](https://github.com/opensearch-project/alerting/pull/1569))


### Opensearch Alerting Dashboards Plugin


* Added v2.15 release notes. ([#972](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/972))


### Opensearch Common Utils


* Added 2.15.0.0 release notes. ([#672](https://github.com/opensearch-project/common-utils/pull/672))


### Opensearch Dashboards Notifications


* 2.15 release notes. ([#210](https://github.com/opensearch-project/dashboards-notifications/pull/210))


### Opensearch ML Common


* Add a connector blueprint for Amazon Comprehend APIs ([#2470](https://github.com/opensearch-project/ml-commons/pull/2470))
* Add titan embeeding v2 to blueprint ([#2480](https://github.com/opensearch-project/ml-commons/pull/2480))
* Tutorial: generate embedding for arrays of object ([#2477](https://github.com/opensearch-project/ml-commons/pull/2477))
* Small fix in blueprint docs ([#2501](https://github.com/opensearch-project/ml-commons/pull/2501))
* Titan Embedding Connector Blueprint content referenced by users of OpenSearch 2.11 version ([#2519](https://github.com/opensearch-project/ml-commons/pull/2519))


### Opensearch Notifications


* Add 2.15.0 release notes ([#926](https://github.com/opensearch-project/notifications/pull/926))


### Opensearch Security Analytics


* Added 2.15.0 release notes. ([#1061](https://github.com/opensearch-project/security-analytics/pull/1061))


### Opensearch Security Analytics Dashboards


* Added v2.15 release notes. ([#1037](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1037))


## MAINTENANCE


### OpenSearch Observability Dashboards


* Remove mocha from dependencies ([#1890](https://github.com/opensearch-project/dashboards-observability/pull/1890))
* Rename Flint instances to S3 Glue ([#1899](https://github.com/opensearch-project/dashboards-observability/pull/1899))
* Fix dead links ([#1872](https://github.com/opensearch-project/dashboards-observability/pull/1872))
* Refactor away integrations adaptor class ([#1825](https://github.com/opensearch-project/dashboards-observability/pull/1825))
* Updating security reachout email ([#1854](https://github.com/opensearch-project/dashboards-observability/pull/1854))
* Fix `S3_DATASOURCE_TYPE` naming typo in `plugin.tsx` ([#1799](https://github.com/opensearch-project/dashboards-observability/pull/1799))
* Adding test for clear cache on logout ([#1794](https://github.com/opensearch-project/dashboards-observability/pull/1794))


### Opensearch Alerting


* Increment version to 2.15.0-SNAPSHOT. ([#1543](https://github.com/opensearch-project/alerting/pull/1543))


### Opensearch Alerting Dashboards Plugin


* Increment version to 2.15.0.0 ([#960](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/960))


### Opensearch Anomaly Detection Dashboards


* Update 2.x to 2.15.0 ([#769](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/769))


### Opensearch Asynchronous Search


* Increment version to 2.15.0 ([#569](https://github.com/opensearch-project/asynchronous-search/pull/569))


### Opensearch Common Utils


* Increment version to 2.15.0-SNAPSHOT ([#651](https://github.com/opensearch-project/common-utils/pull/651))


### Opensearch Cross Cluster Replication


* Disabling docrep to remote store migration test for integTestRemote suite ([#1379](https://github.com/opensearch-project/cross-cluster-replication/pull/1379))


### Opensearch Dashboards Notifications


* Increment version to 2.15.0.0 ([#208](https://github.com/opensearch-project/dashboards-notifications/pull/208))


### Opensearch Dashboards Reporting


* Increment version to 2.15.0.0 ([#360](https://github.com/opensearch-project/dashboards-reporting/pull/360))


### Opensearch Dashboards Search Relevance


* [AUTO] Increment version to 2.15.0.0 ([#398](https://github.com/opensearch-project/dashboards-search-relevance/pull/398))


### Opensearch Dashboards Visualizations


* Increment version to 2.15.0.0 ([#370](https://github.com/opensearch-project/dashboards-visualizations/pull/370))


* Adding 2.15.0 release notes ([#371](https://github.com/opensearch-project/dashboards-visualizations/pull/371))


### Opensearch Job Scheduler


* Increment version to 2.15.0 ([#626](https://github.com/opensearch-project/job-scheduler/pull/626))
* dependabot: bump com.netflix.nebula.ospackage from 11.9.0 to 11.9.1 ([#634](https://github.com/opensearch-project/job-scheduler/pull/634)), ([#635](https://github.com/opensearch-project/job-scheduler/pull/635))


### Opensearch ML Common


* Updating security reachout email ([#2445](https://github.com/opensearch-project/ml-commons/pull/2445))


### Opensearch ML Commons Dashboards


* Increment version to 2.15.0.0 ([#330](https://github.com/opensearch-project/ml-commons-dashboards/pull/330))


### Opensearch Notifications


* Increment version to 2.15.0-SNAPSHOT ([#918](https://github.com/opensearch-project/notifications/pull/918))


### Opensearch Observability


* Increment version to 2.15.0-SNAPSHOT ([#1826](https://github.com/opensearch-project/observability/pull/1826))


* Adding 2.15 release notes ([#1832](https://github.com/opensearch-project/observability/pull/1832))


### Opensearch Query Workbench


* Updating security reachout email ([#324](https://github.com/opensearch-project/dashboards-query-workbench/pull/324))


### Opensearch Reporting


* Increment version to 2.15.0-SNAPSHOT ([#996](https://github.com/opensearch-project/reporting/pull/996))


### Opensearch Security


* Bump com.nimbusds:nimbus-jose-jwt from 9.37.3 to 9.40 ([#4337](https://github.com/opensearch-project/security/pull/4337))([#4353](https://github.com/opensearch-project/security/pull/4353))([#4396](https://github.com/opensearch-project/security/pull/4396))([#4424](https://github.com/opensearch-project/security/pull/4424))
* Bump Wandalen/wretry.action from 3.4.0 to 3.5.0 ([#4335](https://github.com/opensearch-project/security/pull/4335))
* Bump spring\_version from 5.3.34 to 5.3.36 ([#4352](https://github.com/opensearch-project/security/pull/4352))([#4368](https://github.com/opensearch-project/security/pull/4368))
* Bump org.apache.camel:camel-xmlsecurity from 3.22.1 to 3.22.2 ([#4324](https://github.com/opensearch-project/security/pull/4324))
* Bump com.google.errorprone:error\_prone\_annotations from 2.27.0 to 2.27.1 ([#4323](https://github.com/opensearch-project/security/pull/4323))
* Bump org.checkerframework:checker-qual from 3.42.0 to 3.43.0 ([#4322](https://github.com/opensearch-project/security/pull/4322))
* Bump org.scala-lang:scala-library from 2.13.13 to 2.13.14 ([#4321](https://github.com/opensearch-project/security/pull/4321))
* Bump commons-validator:commons-validator from 1.8.0 to 1.9.0 ([#4395](https://github.com/opensearch-project/security/pull/4395))
* Bump com.netflix.nebula.ospackage from 11.9.0 to 11.9.1 ([#4394](https://github.com/opensearch-project/security/pull/4394))
* Bump com.google.errorprone:error\_prone\_annotations from 2.27.1 to 2.28.0 ([#4389](https://github.com/opensearch-project/security/pull/4389))
* Bump commons-cli to 1.8.0 ([#4369](https://github.com/opensearch-project/security/pull/4369))
* Fix DelegatingRestHandlerTests ([#4435](https://github.com/opensearch-project/security/pull/4435))
* Extracted the user attr handling methods from ConfigModelV7 into its own class ([#4431](https://github.com/opensearch-project/security/pull/4431))
* Bump io.dropwizard.metrics:metrics-core and org.checkerframework:checker-qual ([#4425](https://github.com/opensearch-project/security/pull/4425))
* Bump gradle to 8.7 version ([#4377](https://github.com/opensearch-project/security/pull/4377))
* Updating security reachout email ([#4333](https://github.com/opensearch-project/security/pull/4333))
* REST API tests refactoring (#4252 and #4255) ([#4328](https://github.com/opensearch-project/security/pull/4328))
* Fix flaky tests ([#4331](https://github.com/opensearch-project/security/pull/4331))
* Move REST API tests into integration tests (Part 1) ([#4153](https://github.com/opensearch-project/security/pull/4153))
* Fix build errors caused by filterIndices method being moved from SnapshotUtils to IndexUtils ([#4319](https://github.com/opensearch-project/security/pull/4319))
* Extract route paths prefixes into constants ([#4358](https://github.com/opensearch-project/security/pull/4358))


### Opensearch Security Analytics


* Increment version to 2.15.0-SNAPSHOT. ([#1055](https://github.com/opensearch-project/security-analytics/pull/1055))
* Fix codecov calculation ([#1021](https://github.com/opensearch-project/security-analytics/pull/1021))
* Stabilize integ tests ([#1014](https://github.com/opensearch-project/security-analytics/pull/1014))


### Opensearch Security Analytics Dashboards


* Increment version to 2.15.0.0 ([#1035](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1035))
* Added checks for running husky install during post install. ([#1000](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1000))


### Opensearch Security Dashboards Plugin


* Updating security reachout email ([#1948](https://github.com/opensearch-project/security-dashboards-plugin/pull/1948))
* Bump ejs and express versions to address CVEs ([#1988](https://github.com/opensearch-project/security-dashboards-plugin/pull/1988))


### Opensearch Skills


* Increment version to 2.15.0.0.


### OpenSearch SQL


* Use EMR serverless bundled iceberg JAR ([#2632](https://github.com/opensearch-project/sql/pull/2632))
* Update maintainers list ([#2663](https://github.com/opensearch-project/sql/pull/2663))


## REFACTORING


### Opensearch Alerting Dashboards Plugin


* Refactored code to account for notifications server features API change. ([#966](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/966))


### Opensearch Security Analytics Dashboards


* Added addition check for filtering rendered rules. ([#1022](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1022))


### OpenSearch SQL


* Refactor SparkQueryDispatcher ([#2636](https://github.com/opensearch-project/sql/pull/2636))
* Refactor IndexDMLHandler and related classes ([#2644](https://github.com/opensearch-project/sql/pull/2644))
* Introduce FlintIndexStateModelService ([#2658](https://github.com/opensearch-project/sql/pull/2658))
* Add comments to async query handlers ([#2657](https://github.com/opensearch-project/sql/pull/2657))
* Extract SessionStorageService and StatementStorageService ([#2665](https://github.com/opensearch-project/sql/pull/2665))
* Make models free of XContent ([#2677](https://github.com/opensearch-project/sql/pull/2677))
* Remove unneeded datasourceName parameters ([#2683](https://github.com/opensearch-project/sql/pull/2683))
* Refactor data models to be generic to data storage ([#2687](https://github.com/opensearch-project/sql/pull/2687))
* Provide a way to modify spark parameters ([#2691](https://github.com/opensearch-project/sql/pull/2691))
* Change JobExecutionResponseReader to an interface ([#2693](https://github.com/opensearch-project/sql/pull/2693))
* Abstract queryId generation ([#2695](https://github.com/opensearch-project/sql/pull/2695))
* Introduce SessionConfigSupplier to abstract settings ([#2707](https://github.com/opensearch-project/sql/pull/2707))
* Add accountId to data models ([#2709](https://github.com/opensearch-project/sql/pull/2709))
* Pass down request context to data accessors ([#2715](https://github.com/opensearch-project/sql/pull/2715))






