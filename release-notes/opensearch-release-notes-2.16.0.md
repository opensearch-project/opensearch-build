# OpenSearch and OpenSearch Dashboards 2.16.0 Release Notes

## Release Highlights

OpenSearch 2.16 includes new and updated features to help you build and optimize your search applications, improve stability, availability, and resiliency, enhance ease of use, and more. The release also deprecates CentOS7 as a continuous integration build image and supported operating system.


### NEW AND UPDATED FEATURES
* Fast-filter optimization is now available for general range aggregations, offering the potential for performance improvements of 100x or more as measured against the NOAA workload.
* OpenSearch now supports byte vector quantization on-cluster as part of your indexing tasks, boosting efficiency for vector compression automation. Binary vector and Hamming distance support is also added, reducing memory requirements by enabling compression for vectors of up to 32x.
* A new sort search processor can be configured within a search pipeline to sort search responses, and a new split processor lets you split strings into arrays of substrings. These processors expand the capabilities of search pipelines and add support for more use cases.
* Updates to the AI connector framework make it possible to integrate any ML model into OpenSearch, allowing you to enable AI enrichments within search flows through the Search API by configuring ML inference search processors.
* Batch inference support for AI connectors allow connectors to run asynchronous batch inference jobs for ML inference applications in addition to the real-time, synchronous ML inference workloads that were already supported.
* Updates to the cluster manager, including network optimization of cluster manager APIs, compute optimization of pending task processing, and incremental read/writes for routing tables, are designed to reduce the load on the cluster manager. Along with optimizations to shard allocation, these updates can help you scale OpenSearch to more nodes and larger volumes of data
* Application-based templates have been added, providing default settings that can simplify tuning your indexes for compute and storage resource performance as well as for usability for common use cases.
* Support for multiple data sources is extended to two more Dashboards plugins—Notebooks and Snapshot—and all plugins now have version decoupling support in place to filter out incompatible data sources from the selection.
* In February 2024, OpenSearch issued a deprecation notice regarding CentOS Linux 7, which reached end-of-life on June 30, 2024. As of this release, OpenSearch is deprecating CentOS Linux 7 as a continuous integration build image and supported operating system.
* The Query Insights plugin is now bundled as a default plugin in the OpenSearch 2.16 distribution. You can use the [Top N Queries API](https://opensearch.org/docs/latest/observing-your-data/query-insights/top-n-queries/) to identify rogue queries more easily.

### EXPERIMENTAL FEATURES

OpenSearch 2.16.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.

* Batch inference support for AI connectors allow connectors to run asynchronous batch inference jobs for ML inference applications in addition to the real-time, synchronous ML inference workloads that were already supported.

## Release Details
[OpenSearch and OpenSearch Dashboards 2.16.0](https://opensearch.org/versions/opensearch-2-16-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.16/release-notes/opensearch.release-notes-2.16.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.16/release-notes/opensearch-dashboards.release-notes-2.16.0.md).

## FEATURES


### Dashboards Assistant


* Add feature to support text to visualization. ([#218](https://github.com/opensearch-project/dashboards-assistant/pull/218))


### Dashboards Observability


* Replace dashboards with the getting started dashboards ([#1963](https://github.com/opensearch-project/dashboards-observability/pull/1963))
* Observability Overview and GettingStarted ([#1957](https://github.com/opensearch-project/dashboards-observability/pull/1957))
* Version-decoupling for Observability ([#1953](https://github.com/opensearch-project/dashboards-observability/pull/1953))
* Remove integrations from new NavGroups ([#1950](https://github.com/opensearch-project/dashboards-observability/pull/1950))
* Add mds support for routers and fix the missing `callAsCurrentUser` ([#1942](https://github.com/opensearch-project/dashboards-observability/pull/1942))
* added changes for moving notebooks to .kibana ([#1937](https://github.com/opensearch-project/dashboards-observability/pull/1937))
* Register all plugins to NavGroups ([#1926](https://github.com/opensearch-project/dashboards-observability/pull/1926))
* Remove duplicate description for create s3 datasource flow ([#1915](https://github.com/opensearch-project/dashboards-observability/pull/1915))


### Opensearch Alerting Dashboards Plugin


* Plugin Version decoupling for MDS support ([#1003](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1003))
* Look & Feel use standard paragraph size ([#1000](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1000))
* Look & Feel Use small EuiTabs across the board ([#1001](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1001))
* Look & Feel use semantic header with correct size for page, modal and flyout ([#1002](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1002))
* Look & Feel apply missing pattern guidance to Alerting experience ([#1008](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1008))
* side nav changes for alerting ([#1007](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1007))
* Look & Feel Adjust helper text size across monitor page ([#1012](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1012))


### Opensearch Anomaly Detection


* Adding support for date\_nanos to Anomaly Detection ([#1238](https://github.com/opensearch-project/anomaly-detection/pull/1238))


### Opensearch Anomaly Detection Dashboards


* allow date\_nanos dates in timestamp selection ([#795](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/795))
* MDS version decoupling ([#806](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/806))
* AD side navigation redesign ([#810](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/810))


### Opensearch Custom Codecs


* Validating QAT Hardware Support before QAT Codecs are available


### Opensearch Dashboards Maps


* Add support new navigation for maps ([#635](https://github.com/opensearch-project/dashboards-maps/pull/635))
* 


### Opensearch Dashboards Search Relevance


* [Navigation] Register all plugins to NavGroups ([#406](https://github.com/opensearch-project/dashboards-search-relevance/pull/406)) ([#408](https://github.com/opensearch-project/dashboards-search-relevance/pull/408))
* version decoupling support for MDS ([#407](https://github.com/opensearch-project/dashboards-search-relevance/pull/407)) ([#409](https://github.com/opensearch-project/dashboards-search-relevance/pull/409))


## New Contributors


@tackadam made their first contribution in ([#406](https://github.com/opensearch-project/dashboards-search-relevance/pull/406))


### Opensearch ML Common


* Add initial MLInferenceSearchResponseProcessor (#2688)[https://github.com/opensearch-project/ml-commons/pull/2688]
* Add initial search request inference processor (#2731)[https://github.com/opensearch-project/ml-commons/pull/2731]
* Add Batch Prediction Mode in the Connector Framework for batch inference (#2661)[https://github.com/opensearch-project/ml-commons/pull/2661]


### Opensearch ML Commons Dashboards


* Register admin UI as AI models in data administration use case ([#337](https://github.com/opensearch-project/ml-commons-dashboards/pull/337))
* Add version decoupling meta for MDS ([#338](https://github.com/opensearch-project/ml-commons-dashboards/pull/338))
* Update navigation category to Machine learning ([#343](https://github.com/opensearch-project/ml-commons-dashboards/pull/343))


### Opensearch Neural Search


* Enable sorting and search\_after features in Hybrid Search [#827](https://github.com/opensearch-project/neural-search/pull/827)


### Opensearch Observability


* Register system index descriptors through SystemIndexPlugin.getSystemIndexDescriptors ([#1837](https://github.com/opensearch-project/observability/pull/1837))


### Opensearch Performance Analyzer


* Adds index\_uuid as a tag in node stats all shard metrics [#680](https://github.com/opensearch-project/performance-analyzer/pull/680)
* Adds the listener for resource utilization metrics [#687](https://github.com/opensearch-project/performance-analyzer/pull/687)


### Opensearch Security Analytics


* Threat Intel Analytics ([#1098](https://github.com/opensearch-project/security-analytics/pull/1098))


### Opensearch Security Analytics Dashboards


* Alerts in correlations ([#1048](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1048))
* [Threat intel platform][Part 1] UX to support threat intel platform ([#1050](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1050))
* Show fields for aliases when selected in correlation rule and threat intel monitor scan ([#1064](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1064))
* When sending partial alerts results extend them with the detector name and id as well ([#1033](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1033))
* [Threat intel][part 3] Support for source type URL\_Download and logic to activate/deactivate source ([#1068](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1068))
* [Threat intel] Fetch up to 10k source configs and iocs under source details ([#1071](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1071))
* plugin decoupling changes ([#1079](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1079))


### Opensearch Skills


* support nested query in neural sparse tool, vectorDB tool and RAG tool ([#350](https://github.com/opensearch-project/skills/pull/350))
* Add cluster setting to control ppl execution ([#344](https://github.com/opensearch-project/skills/pull/344))
* Add CreateAnomalyDetectorTool ([#348](https://github.com/opensearch-project/skills/pull/348))


### Opensearch k-NN


* Adds dynamic query parameter ef\_search [#1783](https://github.com/opensearch-project/k-NN/pull/1783)
* Adds dynamic query parameter ef\_search in radial search faiss engine [#1790](https://github.com/opensearch-project/k-NN/pull/1790)
* Adds dynamic query parameter nprobes [#1792](https://github.com/opensearch-project/k-NN/pull/1792)
* Add binary format support with HNSW method in Faiss Engine [#1781](https://github.com/opensearch-project/k-NN/pull/1781)
* Add script scoring support for knn field with binary data type [#1826](https://github.com/opensearch-project/k-NN/pull/1826)
* Add painless script support for hamming with binary vector data type [#1839](https://github.com/opensearch-project/k-NN/pull/1839)
* Add binary format support with IVF method in Faiss Engine [#1784](https://github.com/opensearch-project/k-NN/pull/1784)
* Add support for Lucene inbuilt Scalar Quantizer [#1848](https://github.com/opensearch-project/k-NN/pull/1848)


### Opensearch Dashboards Notifications


* Side navigation changes for notifications ([#222](https://github.com/opensearch-project/dashboards-notifications/pull/222))([#225](https://github.com/opensearch-project/dashboards-notifications/pull/225))
*  MDS version decoupling([#223](https://github.com/opensearch-project/dashboards-notifications/pull/223))


## ENHANCEMENTS


### Opensearch Alerting


* Enable cross-cluster monitor cluster setting ([#1612](https://github.com/opensearch-project/alerting/pull/1612))
* Register system index descriptors through SystemIndexPlugin.getSystemIndexDescriptors ([#1594](https://github.com/opensearch-project/alerting/pull/1594))
* commits to support remote monitors in alerting ([#1589](https://github.com/opensearch-project/alerting/pull/1589))


### Opensearch Anomaly Detection


* update BWC test version and enhance code coverage([#1253](https://github.com/opensearch-project/anomaly-detection/pull/1253))
* Register system index descriptors through SystemIndexPlugin.getSystemIndexDescriptors([#1251](https://github.com/opensearch-project/anomaly-detection/pull/1251))
* Add feature filtering in model validation ([#1258](https://github.com/opensearch-project/anomaly-detection/pull/1258))


### Opensearch Common Utils


* [Backport 2.x] Add support for remote monitors ([#694](https://github.com/opensearch-project/common-utils/pull/694))


### Opensearch Dashboards Reporting


* [Navigation] Register all plugins to NavGroups ([#369](https://github.com/opensearch-project/dashboards-reporting/pull/369))
* [Look&Feel] Adjust header and text sizes in reporting menu options ([#379](https://github.com/opensearch-project/dashboards-reporting/pull/379))


### Opensearch Flow Framework


* Register system index descriptors through SystemIndexPlugin.getSystemIndexDescriptors ([#750](https://github.com/opensearch-project/flow-framework/pull/750))


* Support editing of certain workflow fields on a provisioned workflow ([#757](https://github.com/opensearch-project/flow-framework/pull/757))
* Add allow\_delete parameter to Deprovision API ([#763](https://github.com/opensearch-project/flow-framework/pull/763))
* Improve Template and WorkflowState builders ([#778](https://github.com/opensearch-project/flow-framework/pull/778))


### Opensearch Index Management Dashboards Plugin


* New Navigation UX change ([#1085](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1085))
* Added dataVersionFilter support to MDS to enable version decoupling ([#1080](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1080))
* Add MDS support to snapshot pages ([#1084](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1084))


### Opensearch Job Scheduler


* Wrap interactions with `.opendistro-job-scheduler-lock` in `ThreadContext.stashContext` to ensure JS can read and write to the index [(#347)](https://github.com/opensearch-project/job-scheduler/pull/347) [(#647)](https://github.com/opensearch-project/job-scheduler/pull/647).


### Opensearch ML Common


* Automated model interface generation on aws llms (#2689)[https://github.com/opensearch-project/ml-commons/pull/2689]
* Increase execute thread pool size (#2691)[https://github.com/opensearch-project/ml-commons/pull/2691]
* Add multi modal default preprocess function (#2500)[https://github.com/opensearch-project/ml-commons/pull/2500]
* Add model input validation for local models in ml processor (#2610)[https://github.com/opensearch-project/ml-commons/pull/2610]
* Removing experimental from the Conversation memory feature(#2592)[https://github.com/opensearch-project/ml-commons/pull/2592]
* Pass all parameters including chat\_history to run tools (#2714)[https://github.com/opensearch-project/ml-commons/pull/2714]
* Feat: add bedrock runtime agent for knowledge base (#2651)[https://github.com/opensearch-project/ml-commons/pull/2651]
* change disk circuit breaker to cluster settings (#2634)[https://github.com/opensearch-project/ml-commons/pull/2634]


### Opensearch Neural Search


* InferenceProcessor inherits from AbstractBatchingProcessor to support sub batching in processor [#820](https://github.com/opensearch-project/neural-search/pull/820)


* Adds dynamic knn query parameters efsearch and nprobes [#814](https://github.com/opensearch-project/neural-search/pull/814/)
* Enable '.' for nested field in text embedding processor ([#811](https://github.com/opensearch-project/neural-search/pull/811))
* Enhance syntax for nested mapping in destination fields([#841](https://github.com/opensearch-project/neural-search/pull/841))


### Opensearch Query Insights


* Increment latency, cpu and memory histograms for multiple query types ([#30](https://github.com/opensearch-project/query-insights/pull/30))
* Always populate resource usage metrics for categorization ([#41](https://github.com/opensearch-project/query-insights/pull/41))


### Opensearch Query Workbench


* ### Enhancement


* added version decoupling for neo MDS support ([#353](https://github.com/opensearch-project/dashboards-query-workbench/pull/353))
* Moving Query Workbench to Dev Tools ([#349](https://github.com/opensearch-project/dashboards-query-workbench/pull/349))


### Opensearch Security


* Add support for PBKDF2 for password hashing & add support for configuring BCrypt and PBKDF2 ([#4524](https://github.com/opensearch-project/security/pull/4524))
* Separated DLS/FLS privilege evaluation from action privilege evaluation ([#4490](https://github.com/opensearch-project/security/pull/4490))
* Update PULL\_REQUEST\_TEMPLATE to include an API spec change in the checklist. ([#4533](https://github.com/opensearch-project/security/pull/4533))
* Update PATCH API to fail validation if nothing changes ([#4530](https://github.com/opensearch-project/security/pull/4530))
* Refactor InternalUsers REST API test ([#4481](https://github.com/opensearch-project/security/pull/4481))
* Refactor Role Mappings REST API test ([#4450](https://github.com/opensearch-project/security/pull/4450))
* Remove special handling for do\_not\_fail\_on\_forbidden on cluster actions ([#4486](https://github.com/opensearch-project/security/pull/4486))
* Add Tenants REST API test and partial fix ([#4166](https://github.com/opensearch-project/security/pull/4166))
* Refactor Roles REST API test and partial fix #4166 ([#4433](https://github.com/opensearch-project/security/pull/4433))
* New algorithm for resolving action groups ([#4448](https://github.com/opensearch-project/security/pull/4448))
* Check block request only if system index ([#4430](https://github.com/opensearch-project/security/pull/4430))
* Replaced uses of SecurityRoles by Set<String> mappedRoles where the SecurityRoles functionality is not needed ([#4432](https://github.com/opensearch-project/security/pull/4432))


### Opensearch Security Analytics


* added correlationAlert integ tests ([#1099](https://github.com/opensearch-project/security-analytics/pull/1099))
* add filter to list ioc api to fetch only from available and refreshing apis. null check for alias of ioc indices ([#1131](https://github.com/opensearch-project/security-analytics/pull/1131))
* Changes threat intel default store config model ([#1133](https://github.com/opensearch-project/security-analytics/pull/1133))
* adds new tif source config type - url download ([#1142](https://github.com/opensearch-project/security-analytics/pull/1142))


### Opensearch Security Dashboards Plugin


* [MDS] Adds datasource filter for version decoupling ([#2051](https://github.com/opensearch-project/security-dashboards-plugin/pull/2051))
* Update nextUrl validation to incorporate serverBasePath ([#2048](https://github.com/opensearch-project/security-dashboards-plugin/pull/2048))
* Conform to Navigation changes from OSD core ([#2022](https://github.com/opensearch-project/security-dashboards-plugin/pull/2022))
* feat: http proxy support for oidc ([#2024](https://github.com/opensearch-project/security-dashboards-plugin/pull/2024))
* Remove dependency on opensearch build repo libs from custom build.sh ([#2033](https://github.com/opensearch-project/security-dashboards-plugin/pull/2033))
* Add custom build script to support different cypress version ([#2027](https://github.com/opensearch-project/security-dashboards-plugin/pull/2027))


### Opensearch k-NN


* Switch from byte stream to byte ref for serde [#1825](https://github.com/opensearch-project/k-NN/pull/1825)


### SQL


* Added Setting to Toggle Data Source Management Code Paths ([#2811](https://github.com/opensearch-project/sql/pull/2811))
* Span in PPL statsByClause could be specified after fields ([#2810](https://github.com/opensearch-project/sql/pull/2810))
* Updating Grammer changes same as main branch ([#2850](https://github.com/opensearch-project/sql/pull/2850))


## BUG FIXES


### Dashboards Observability


* Add toast message for getting started / Fix Nav Bug for Traces ([#1977](https://github.com/opensearch-project/dashboards-observability/pull/1977))
* Unregister observability datasource from old and new nav group ([#1972](https://github.com/opensearch-project/dashboards-observability/pull/1972))
* UX copy changes for Notebooks with MDS ([#1971](https://github.com/opensearch-project/dashboards-observability/pull/1971))
* fix minor issues in query assist UI ([#1939](https://github.com/opensearch-project/dashboards-observability/pull/1939))
* Trace analytics scroll bar reset ([#1917](https://github.com/opensearch-project/dashboards-observability/pull/1917))
* #1466 - create observability dashboard after invalid name ([#1730](https://github.com/opensearch-project/dashboards-observability/pull/1730))
* fix redirection url in saved objects management page for notebooks([#1998](https://github.com/opensearch-project/dashboards-observability/pull/1998))


### Opensearch Alerting


* Fixing build script to only publish alerting zip ([#1605](https://github.com/opensearch-project/alerting/pull/1605))
* fix pluginzippublish issue ([#1604](https://github.com/opensearch-project/alerting/pull/1604))


### Opensearch Dashboards Maps


* Fixed broken wms custom layer update ([#601](https://github.com/opensearch-project/dashboards-maps/pull/631))


### Opensearch Dashboards Reporting


* Update dependency jsdom to v18 ([#381](https://github.com/opensearch-project/dashboards-reporting/pull/381))
* Update dependency ws to v7.5.10 ([#385](https://github.com/opensearch-project/dashboards-reporting/pull/385))
* Add braces v3.0.3 to resolution ([#388](https://github.com/opensearch-project/dashboards-reporting/pull/388))


### Opensearch Flow Framework


* Handle Not Found deprovision exceptions as successful deletions ([#805](https://github.com/opensearch-project/flow-framework/pull/805))


* Wrap CreateIndexRequest mappings in \_doc key as required ([#809](https://github.com/opensearch-project/flow-framework/pull/809))
* Have FlowFrameworkException status recognized by ExceptionsHelper ([#811](https://github.com/opensearch-project/flow-framework/pull/811))


### Opensearch Index Management Dashboards Plugin


* Persist dataSourceId across applications under new Nav change ([#1088](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1088))


### Opensearch ML Common


* Add stashcontext to connector getter (#2742)[https://github.com/opensearch-project/ml-commons/pull/2742]
* Excluding remote models from max node per node setting (#2732)[https://github.com/opensearch-project/ml-commons/pull/2732]
* Add logging for throttling and guardrail in connector (#2725)[https://github.com/opensearch-project/ml-commons/pull/2725]
* Add acknowledge check for index creation in missing places (#2715)[https://github.com/opensearch-project/ml-commons/pull/2715]
* Update config index mappings to use correct field types (#2710)[https://github.com/opensearch-project/ml-commons/pull/2710]
* Fix yaml test issue (#2700)[https://github.com/opensearch-project/ml-commons/pull/2700]
* Fix MLModelTool returns null if the response of LLM is a pure json object (#2675)[https://github.com/opensearch-project/ml-commons/pull/2675]
* Bump ml config index schema version (#2656)[https://github.com/opensearch-project/ml-commons/pull/2656]
* Fix final answer with extra meaningless symbol (#2676)[https://github.com/opensearch-project/ml-commons/pull/2676]
* Add XContentType to wrap the CreateIndexRequest mappings in \_doc key to fix v1 templates issue (#2759)[https://github.com/opensearch-project/ml-commons/pull/2759]
* Remove ignoreFailure and fix JsonArray Parsing Issue (#2770)[https://github.com/opensearch-project/ml-commons/pull/2770]
* Merge the existing parameters when updating connectors (#2784)[https://github.com/opensearch-project/ml-commons/pull/2784]


### Opensearch Neural Search


* Fix function names and comments in the gradle file for BWC tests ([#795](https://github.com/opensearch-project/neural-search/pull/795/files))


* Fix for missing HybridQuery results when concurrent segment search is enabled ([#800](https://github.com/opensearch-project/neural-search/pull/800))


### Opensearch Query Insights


* Validate lower bound for top n size ([#13](https://github.com/opensearch-project/query-insights/pull/13))
* Fix stream serialization issues for complex data structures ([#13](https://github.com/opensearch-project/query-insights/pull/13))


### Opensearch Security


* Fixed test failures in FlsAndFieldMaskingTests ([#4548](https://github.com/opensearch-project/security/pull/4548))
* Typo in securityadmin.sh hint ([#4526](https://github.com/opensearch-project/security/pull/4526))
* Fix NPE getting metaFields from mapperService on a close index request ([#4497](https://github.com/opensearch-project/security/pull/4497))
* Fixes flaky integration tests ([#4452](https://github.com/opensearch-project/security/pull/4452))


### Opensearch Security Analytics


* pass integ tests ([#1082](https://github.com/opensearch-project/security-analytics/pull/1082))
* set blank response when indexNotFound exception ([#1125](https://github.com/opensearch-project/security-analytics/pull/1125))
* throw error when no iocs are stored due to incompatible ioc types from S3 downloaded iocs file ([#1129](https://github.com/opensearch-project/security-analytics/pull/1129))
* fix findingIds filter on ioc findings search api ([#1130](https://github.com/opensearch-project/security-analytics/pull/1130))
* Adjusted IOCTypes usage ([#1156](https://github.com/opensearch-project/security-analytics/pull/1156))
* Fix the job scheduler parser, action listeners, and multi-node test ([#1157](https://github.com/opensearch-project/security-analytics/pull/1157))
* ListIOCs API to return number of findings per IOC ([#1163](https://github.com/opensearch-project/security-analytics/pull/1163))
* Ioc upload integ tests and fix update ([#1162](https://github.com/opensearch-project/security-analytics/pull/1162))
* [BUG] Resolve aliases in monitor input to concrete indices before computing ioc-containing fields from concrete index docs ([#1173](https://github.com/opensearch-project/security-analytics/pull/1173))
* Enum fix ([#1178](https://github.com/opensearch-project/security-analytics/pull/1178))
* fix bug: threat intel monitor finding doesnt contain all doc\_ids containing malicious IOC ([#1184](https://github.com/opensearch-project/security-analytics/pull/1184))
* Fixed bulk indexing for IOCs ([#1187](https://github.com/opensearch-project/security-analytics/pull/1187))
* Fix ioc upload update behavior and change error response ([#1192](https://github.com/opensearch-project/security-analytics/pull/1192))
* Catch and wrap exceptions. ([#1198](https://github.com/opensearch-project/security-analytics/pull/1198))


### Opensearch Security Analytics Dashboards


* Updated get findings & alerts to use duration filter and start showing results as they come in ([#1031](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1031))
* Backport 1051 to 2.x ([#1053](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1053))
* Updated IOCTypes. ([#1076](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1076))
* [Threat intel] Fixed ui issues ([#1080](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1080))
* side nav changes for SA ([#1084](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1084))


### Opensearch Security Dashboards Plugin


* Fix the bug of capabilities request not supporting carrying authinfo ([#2014](https://github.com/opensearch-project/security-dashboards-plugin/pull/2014))
* Fix URL duplication issue ([#2004](https://github.com/opensearch-project/security-dashboards-plugin/pull/2004))


### Opensearch k-NN


* Fixing the arithmetic to find the number of vectors to stream from java to jni layer.[#1804](https://github.com/opensearch-project/k-NN/pull/1804)
* Fixed LeafReaders casting errors to SegmentReaders when segment replication is enabled during search.[#1808](https://github.com/opensearch-project/k-NN/pull/1808)
* Release memory properly for an array type [#1820](https://github.com/opensearch-project/k-NN/pull/1820)
* FIX Same Suffix Cause Recall Drop to zero [#1802](https://github.com/opensearch-project/k-NN/pull/1802)


### SQL


* Temp use of older nodejs version before moving to Almalinux8 ([#2816](https://github.com/opensearch-project/sql/pull/2816))
* Fix yaml errors causing checks not to be run ([#2823](https://github.com/opensearch-project/sql/pull/2823))
* Well format the raw response when query parameter "pretty" enabled ([#2829](https://github.com/opensearch-project/sql/pull/2829))
* Add support for custom date format and openSearch date format for date fields as part of Lucene query ([#2762](https://github.com/opensearch-project/sql/pull/2762))
* Fix SparkExecutionEngineConfigClusterSetting deserialize issue ([#2838](https://github.com/opensearch-project/sql/pull/2838))
* Fix SparkSubmitParameterModifier issue ([#2837](https://github.com/opensearch-project/sql/pull/2837))


## INFRASTRUCTURE


### Opensearch Anomaly Detection


* set baseline JDK version to JDK-21 ([#1228](https://github.com/opensearch-project/anomaly-detection/pull/1228))


### Opensearch Anomaly Detection Dashboards


* Update Frontend CI to use JDK21 ([#798](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/798))


### Opensearch Job Scheduler


* Fix checkout action failure [(#650)](https://github.com/opensearch-project/job-scheduler/pull/650) [(#651)](https://github.com/opensearch-project/job-scheduler/pull/651).


### Opensearch ML Common


* Enable tests with mockStatic in MLEngineTest (#2582)[https://github.com/opensearch-project/ml-commons/pull/2582]
* Fix GA workflow that publishes Apache Maven artifacts (#2625)[https://github.com/opensearch-project/ml-commons/pull/2625]
* Temp use of older nodejs version before moving to Almalinux8 (#2628)[https://github.com/opensearch-project/ml-commons/pull/2628]
* Add more logs for automated model interface creation (#2778)[https://github.com/opensearch-project/ml-commons/pull/2778]


### Opensearch Neural Search


* Add BWC for batch ingestion ([#769](https://github.com/opensearch-project/neural-search/pull/769))


* Add backward test cases for neural sparse two phase processor ([#777](https://github.com/opensearch-project/neural-search/pull/777))
* Fix CI for JDK upgrade towards 21 ([#835](https://github.com/opensearch-project/neural-search/pull/835))
* Maven publishing workflow by upgrade jdk to 21 ([#837](https://github.com/opensearch-project/neural-search/pull/837))


### Opensearch Performance Analyzer


* Bump bouncycastle from 1.74 to 1.78.1 [#656](https://github.com/opensearch-project/performance-analyzer/pull/656)
* Bump PA to use 1.5.0 PA commons lib [#698](https://github.com/opensearch-project/performance-analyzer/pull/698)


### Opensearch Query Insights


* Configure Mend for query insights repo [#1](https://github.com/opensearch-project/query-insights/pull/1)
* Set up gradle and CI for query insights [#4](https://github.com/opensearch-project/query-insights/pull/4)
* Add build script to query insights plugin [#14](https://github.com/opensearch-project/query-insights/pull/14)
* Add backport GitHub actions [#17](https://github.com/opensearch-project/query-insights/pull/17)
* Add maven publish workflow [#24](https://github.com/opensearch-project/query-insights/pull/24)
* Add GitHub action for security enabled integration tests [#48](https://github.com/opensearch-project/query-insights/pull/48)
* Add code hygiene checks for query insights ([#51](https://github.com/opensearch-project/query-insights/pull/51))


### Opensearch Reporting


* Bump java to 21 ([#1014](https://github.com/opensearch-project/reporting/pull/1014))


### Opensearch k-NN


* Apply custom patch only once by comparing the last patch id [#1833](https://github.com/opensearch-project/k-NN/pull/1833)


### SQL


* Increment version to 2.16.0-SNAPSHOT ([#2743](https://github.com/opensearch-project/sql/pull/2743))
* Fix checkout action failure ([#2819](https://github.com/opensearch-project/sql/pull/2819))
* Fix MacOS workflow failure ([#2831](https://github.com/opensearch-project/sql/pull/2831))


## DOCUMENTATION


### Opensearch Alerting


* Added 2.16 release notes. ([#1619](https://github.com/opensearch-project/alerting/pull/1619))


### Opensearch Alerting Dashboards Plugin


* Added v2.16 release notes. ([#1019](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1019))


### Opensearch Common Utils


* Added 2.16.0.0 release notes. ([#700](https://github.com/opensearch-project/common-utils/pull/700))


### Opensearch Dashboards Notifications


* 2.16 release notes. ([#227](https://github.com/opensearch-project/dashboards-notifications/pull/227))


### Opensearch ML Common


* Add amazon textract blueprint (#2562)[https://github.com/opensearch-project/ml-commons/pull/2562]
* Make all Bedrock model blueprints in a tidier format (#2642)[https://github.com/opensearch-project/ml-commons/pull/2642]
* Fix remote inference blueprints (#2692)[https://github.com/opensearch-project/ml-commons/pull/2692]
* Add connector blueprint for cohere embedding models in bedrock (#2667)[https://github.com/opensearch-project/ml-commons/pull/2667]
* Update tutorials for caching secrets for non-aws models (#2637)[https://github.com/opensearch-project/ml-commons/pull/2637]
* Add tutuorial for cross-encoder model on sagemaker (#2607)[https://github.com/opensearch-project/ml-commons/pull/2607]
* Add offline batch inference connector blueprints (#2768)[https://github.com/opensearch-project/ml-commons/pull/2768]


### Opensearch Notifications


* Add 2.16.0 release notes (#[935](https://github.com/opensearch-project/notifications/pull/935))


### Opensearch Query Insights


* Update Readme file with user guide ([#5](https://github.com/opensearch-project/query-insights/pull/5))
* Added 2.16 release notes ([#52](https://github.com/opensearch-project/query-insights/pull/52))


### Opensearch Security Analytics


* Added 2.16.0 release notes. ([#1196](https://github.com/opensearch-project/security-analytics/pull/1196))


### Opensearch Security Analytics Dashboards


* Added v2.16 release notes. ([#1087](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1087))


### Opensearch k-NN


* Update dev guide to fix clang linking issue on arm [#1746](https://github.com/opensearch-project/k-NN/pull/1746)


## MAINTENANCE


### Dashboards Assistant


* Make ML Configuration Index Mapping be compatible with ml-commons plugin. ([#239](https://github.com/opensearch-project/dashboards-assistant/pull/239))


### Dashboards Observability


* updated java version from 11 to 21 ([#1940](https://github.com/opensearch-project/dashboards-observability/pull/1940))
* [Bug] Fix CVEs for ag-grid, ws and braces packages ([#1987](https://github.com/opensearch-project/dashboards-observability/pull/1987))
* [Bug] CVE fix for ag ([#1989](https://github.com/opensearch-project/dashboards-observability/pull/1989))
* [Bug] Remove ag grid package ([#2001](https://github.com/opensearch-project/dashboards-observability/pull/2001))


### Opensearch Alerting


* Increment version to 2.16.0-SNAPSHOT. ([#1589](https://github.com/opensearch-project/alerting/pull/1589))


### Opensearch Alerting Dashboards Plugin


* Increment version to 2.16.0.0 ([#1009](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1009))
* Increment version to 2.16.0.0 ([#978](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/978))


### Opensearch Anomaly Detection


* Update PULL\_REQUEST\_TEMPLATE to include an API spec change in the checklist ([#1262](https://github.com/opensearch-project/anomaly-detection/pull/1262))


### Opensearch Anomaly Detection Dashboards


* Update 2.x to 2.16.0 ([#769](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/808))


### Opensearch Asynchronous Search


* Increment version to 2.16.0 ([#586](https://github.com/opensearch-project/asynchronous-search/pull/586))


### Opensearch Common Utils


* Increment version to 2.16.0-SNAPSHOT ([#688](https://github.com/opensearch-project/common-utils/pull/688))


### Opensearch Dashboards Notifications


* Increment version to 2.16.0.0 ([#216](https://github.com/opensearch-project/dashboards-notifications/pull/216))
* Increment version to 2.16.0.0 ([#224](https://github.com/opensearch-project/dashboards-notifications/pull/224))


### Opensearch Dashboards Reporting


* Increment version to 2.16.0.0 ([#366](https://github.com/opensearch-project/dashboards-reporting/pull/366))


### Opensearch Dashboards Visualizations


* Increment version to 2.16.0.0 ([#375](https://github.com/opensearch-project/dashboards-visualizations/pull/375))


* Adding 2.16.0 release notes ([#380](https://github.com/opensearch-project/dashboards-visualizations/pull/380))


### Opensearch Index Management


* Increment version to 2.16.0-SNAPSHOT ([#1187](https://github.com/opensearch-project/index-management/pull/1187))
* Add publish in spi build.gradle ([#1207](https://github.com/opensearch-project/index-management/pull/1207))
* Fix github action ([#1208](https://github.com/opensearch-project/index-management/pull/1208))


### Opensearch Index Management Dashboards Plugin


* Bumped up braces package version to address CVE-2024-4068 ([#1091](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1091))
* Increment version to 2.16.0.0 ([#1089](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1089))


### Opensearch Job Scheduler


* Increment version to 2.16.0 ([#638](https://github.com/opensearch-project/job-scheduler/pull/638)).


### Opensearch ML Common


* Upgrade djl version to 0.28.0 (#2578)[https://github.com/opensearch-project/ml-commons/pull/2578]
* Register system index descriptors through SystemIndexPlugin.getSystemIndexDescriptors (#2586)[https://github.com/opensearch-project/ml-commons/pull/2586]


### Opensearch ML Commons Dashboards


* Increment version to 2.16.0.0 ([#335](https://github.com/opensearch-project/ml-commons-dashboards/pull/335))
* Bump braces from 3.0.2 to 3.0.3 ([#341](https://github.com/opensearch-project/ml-commons-dashboards/pull/341))


### Opensearch Notifications


* Increment version to 2.16.0-SNAPSHOT (#[929](https://github.com/opensearch-project/notifications/pull/929))


### Opensearch Observability


* Increment version to 2.16.0-SNAPSHOT ([#1834](https://github.com/opensearch-project/observability/pull/1834))


### Opensearch Query Insights


* Bootstrap query insights plugin repo with maintainers ([#2](https://github.com/opensearch-project/query-insights/pull/2))
* Fix linux ci build failure when upgrade Actions runner to use node 20 ([#15](https://github.com/opensearch-project/query-insights/pull/15))
* Move query categorization changes to plugin ([#16](https://github.com/opensearch-project/query-insights/pull/16))
* Fix build error in NodeRequest class for 2.x ([#18](https://github.com/opensearch-project/query-insights/pull/18))
* Fix query insights zip versioning ([#34](https://github.com/opensearch-project/query-insights/pull/34))
* Fix integration test failures when running with security plugin ([#45](https://github.com/opensearch-project/query-insights/pull/45))


### Opensearch Query Workbench


* Added Version bump ([#352](https://github.com/opensearch-project/dashboards-query-workbench/pull/352))


* Bump braces from 3.0.2 to 3.0.3 ([#345](https://github.com/opensearch-project/dashboards-query-workbench/pull/345))


### Opensearch Reporting


* Increment version to 2.16.0-SNAPSHOT ([#1006](https://github.com/opensearch-project/reporting/pull/1006))


### Opensearch Security


* Remove unused dependancy Apache CXF ([#4580](https://github.com/opensearch-project/security/pull/4580))
* Remove unnecessary return statements ([#4558](https://github.com/opensearch-project/security/pull/4558))
* Refactor and update existing ml roles ([#4151](https://github.com/opensearch-project/security/pull/4151))
* Replace JUnit assertEquals() with Hamcrest matchers assertThat() ([#4544](https://github.com/opensearch-project/security/pull/4544))
* Update Gradle to 8.9 ([#4553](https://github.com/opensearch-project/security/pull/4553))
* Bump org.checkerframework:checker-qual from 3.44.0 to 3.45.0 ([#4531](https://github.com/opensearch-project/security/pull/4531))
* Add security analytics threat intel action ([#4498](https://github.com/opensearch-project/security/pull/4498))
* Bump kafka\_version from 3.7.0 to 3.7.1 ([#4501](https://github.com/opensearch-project/security/pull/4501))
* Bump org.junit.jupiter:junit-jupiter from 5.10.2 to 5.10.3 ([#4503](https://github.com/opensearch-project/security/pull/4503))
* Bump com.fasterxml.woodstox:woodstox-core from 6.6.2 to 6.7.0 ([#4483](https://github.com/opensearch-project/security/pull/4483))
* Bump jjwt\_version from 0.12.5 to 0.12.6 ([#4484](https://github.com/opensearch-project/security/pull/4484))
* Bump org.eclipse.platform:org.eclipse.core.runtime from 3.31.0 to 3.3.1.100 ([#4467](https://github.com/opensearch-project/security/pull/4467))
* Bump spring\_version from 5.3.36 to 5.3.37 ([#4466](https://github.com/opensearch-project/security/pull/4466))
* Update to Gradle 8.8 ([#4459](https://github.com/opensearch-project/security/pull/4459))


### Opensearch Security Analytics


* Incremented version to 2.16.0. ([#1197](https://github.com/opensearch-project/security-analytics/pull/1197))
* Fix build CI error due to action runner env upgrade node 20 ([#1143](https://github.com/opensearch-project/security-analytics/pull/1143))


### Opensearch Security Analytics Dashboards


* Increment version to 2.16.0.0 ([#1046](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1046))


### Opensearch Security Dashboards Plugin


* Format package.json ([#2060](https://github.com/opensearch-project/security-dashboards-plugin/pull/2060))
* Addresses CVE-2024-4068 and updates yarn.lock ([#2039](https://github.com/opensearch-project/security-dashboards-plugin/pull/2039))


### Opensearch k-NN


* Bump faiss commit to 33c0ba5 [#1796](https://github.com/opensearch-project/k-NN/pull/1796)


## REFACTORING


### Opensearch ML Common


* Change multimodal connector name to bedrock multimodal connector (#2672)[https://github.com/opensearch-project/ml-commons/pull/2672]


### Opensearch Reporting


* Register system index descriptors through SystemIndexPlugin.getSystemIndexDescriptors ([#1009](https://github.com/opensearch-project/reporting/pull/1009))


### SQL


* Change DataSourceType from enum to class ([#2746](https://github.com/opensearch-project/sql/pull/2746))
* Fix code style issue ([#2745](https://github.com/opensearch-project/sql/pull/2745))
* Scaffold async-query-core and async-query module ([#2751](https://github.com/opensearch-project/sql/pull/2751))
* Move classes from spark to async-query-core and async-query ([#2750](https://github.com/opensearch-project/sql/pull/2750))
* Exclude integ-test, doctest and download task when built offline ([#2763](https://github.com/opensearch-project/sql/pull/2763))
* Abstract metrics to reduce dependency to legacy ([#2768](https://github.com/opensearch-project/sql/pull/2768))
* Remove AsyncQueryId ([#2769](https://github.com/opensearch-project/sql/pull/2769))
* Add README to async-query-core ([#2770](https://github.com/opensearch-project/sql/pull/2770))
* Separate build and validateAndBuild method in DataSourceMetadata ([#2752](https://github.com/opensearch-project/sql/pull/2752))
* Abstract FlintIndex client ([#2771](https://github.com/opensearch-project/sql/pull/2771))
* Fix statement to store requested langType ([#2779](https://github.com/opensearch-project/sql/pull/2779))
* Push down OpenSearch specific exception handling ([#2782](https://github.com/opensearch-project/sql/pull/2782))
* Implement integration test for async-query-core ([#2785](https://github.com/opensearch-project/sql/pull/2785))
* Fix SQLQueryUtils to extract multiple tables ([#2791](https://github.com/opensearch-project/sql/pull/2791))
* Eliminate dependency from async-query-core to legacy ([#2792](https://github.com/opensearch-project/sql/pull/2792))
* Pass accountId to EMRServerlessClientFactory.getClient ([#2822](https://github.com/opensearch-project/sql/pull/2822))
* Register system index descriptors through SystemIndexPlugin.getSystemIndexDescriptors ([#2817](https://github.com/opensearch-project/sql/pull/2817))
* Introduce SparkParameterComposerCollection ([#2824](https://github.com/opensearch-project/sql/pull/2824))
