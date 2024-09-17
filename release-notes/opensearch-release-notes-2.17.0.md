# OpenSearch and OpenSearch Dashboards 2.17.0 Release Notes

## Release Highlights

OpenSearch 2.17 includes new and updated features to help you build and optimize your search applications, improve stability, availability, and resiliency, enhance ease of use, and more. 

### NEW AND UPDATED FEATURES

* Introduced as an experimental feature in OpenSearch 2.15, remote cluster state publication is now generally available in 2.17.
* To help users benefit from concurrent segment search for the right requests, OpenSearch 2.17 adds a new setting both at index and cluster level. These settings along with pluggable “decider” logic will give more granular control on the requests that will be executed using concurrent search.
* Adds support for encoding numeric term values as a Roaring bitmap. By encoding the values more efficiently, a search request can use a stored filter that matches over a million documents, with lower retrieval latency and less memory used.
* Introduces disk optimized vector search feature which significantly reduces the operational costs for vector workloads.
* Vector search introduces byte vector support to its Faiss engine. Faiss Byte vector is a memory-efficient encoding technique that reduces memory requirements by up to 75% with a minimal drop in recall, making it suitable for large-scale workloads.
* Introduces ML inference search processors, enabling users to run model predictions while conducting search queries.
* Introduces batch asynchronous ingestion, allowing users to trigger batch inference jobs, monitor job status, and ingest results once batch processing is complete.
* Flow Framework plugin now supports advanced user level security in 2.17. Users can now use backend roles to configure fine-grained access to individual workflows based on roles.
* ML inference search processors has now enhanced search response processors by allowing users to specify running model prediction for all documents in one request or running model prediction for each document.


### EXPERIMENTAL FEATURES

OpenSearch 2.17.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.

* OpenSearch 2.17 introduces application-based configuration templates. When enabled, this feature provides your cluster with a set of pre-defined component templates, streamlining the creation of indexes and index templates tailored to your specific needs.
* Introduces experimental mechanisms to achieve indexing and search isolation within a cluster by adding a new replica shard type that is intended only to serve search traffic.
* Improves performance of expensive queries using the approximation framework that brings new techniques to short-circuit long running queries by only scoring relevant documents in the query.
* Introduces a custom trace source that is based on the open telemetry schema and includes a redesigned overview page for traces and services.

## Release Details
[OpenSearch and OpenSearch Dashboards 2.17.0](https://opensearch.org/versions/opensearch-2-17-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.17/release-notes/opensearch.release-notes-2.17.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.17/release-notes/opensearch-dashboards.release-notes-2.17.0.md).


## FEATURES


### Dashboards Assistant


* Use smaller and compressed varients of buttons and form components ([#250](https://github.com/opensearch-project/dashboards-assistant/pull/250))


### Opensearch Anomaly Detection


* Add Support for Handling Missing Data in Anomaly Detection ([#1274](https://github.com/opensearch-project/anomaly-detection/pull/1274))
* Adding remote index and multi-index checks in validation ([#1290](https://github.com/opensearch-project/anomaly-detection/pull/1290))


### Opensearch Anomaly Detection Dashboards


* [Look&Feel] Use smaller and compressed varients of buttons and form components ([#826](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/826))
* Header redesign ([#841](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/841))
* [Look&Feel] Consistency and density improvements ([#836](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/836))
* Add Missing Value Imputation Options and Update Shingle Size Limit ([#851](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/851))
* Add ignore rules comparing actual and expected values ([#859](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/859))
* Adding remote indices and multi index functionality ([#867](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/867))


### Opensearch Dashboards Maps


* Conditionally use the new Page Header variant on the Maps listing page ([#653](https://github.com/opensearch-project/dashboards-maps/pull/653))
* Conditionally use the new Application Header variant on the Maps visualization page ([#654](https://github.com/opensearch-project/dashboards-maps/pull/654))
* Conditionally use full width for Maps listing page table ([#655](https://github.com/opensearch-project/dashboards-maps/pull/655))


### Opensearch Dashboards Search Relevance


* Add compare queries card to search use case overview page ([#427](https://github.com/opensearch-project/dashboards-search-relevance/pull/427)) ([#431](https://github.com/opensearch-project/dashboards-search-relevance/pull/431))


### Opensearch Flow Framework


* Adds reprovision API to support updating search pipelines, ingest pipelines index settings ([#804](https://github.com/opensearch-project/flow-framework/pull/804))
* Adds user level access control based on backend roles ([#838](https://github.com/opensearch-project/flow-framework/pull/838))
* Support parsing connector\_id when creating tools ([#846](https://github.com/opensearch-project/flow-framework/pull/846))


### Opensearch ML Commons


* Offline batch ingestion API actions and data ingesters ([#2844](https://github.com/opensearch-project/ml-commons/pull/2844))
* Support get batch transform job status in get task API ([#2825](https://github.com/opensearch-project/ml-commons/pull/2825))


### Opensearch Observability


* [Page Header] New page header for metrics ([#2050](https://github.com/opensearch-project/dashboards-observability/pull/2050))
* [Look&Feel] Integrations Density and Consistency Improvements ([#2071](https://github.com/opensearch-project/dashboards-observability/pull/2071))
* [Feature] Multi-data Source Support for Getting Started ([#2048](https://github.com/opensearch-project/dashboards-observability/pull/2048))
* [Feature] Traces/Services UI update ([#2078](https://github.com/opensearch-project/dashboards-observability/pull/2078))
* [Page Header] New page header for applications and UI updates ([#2081](https://github.com/opensearch-project/dashboards-observability/pull/2081))
* [Feature] Observability dashboards UI update ([#2090](https://github.com/opensearch-project/dashboards-observability/pull/2090))
* [Feature] MDS support in Integrations for observability plugin ([#2051](https://github.com/opensearch-project/dashboards-observability/pull/2051))
* [Feature] Logs UI update ([#2092](https://github.com/opensearch-project/dashboards-observability/pull/2092))
* [Feature] Make createAssets API compatible with workspace ([#2101](https://github.com/opensearch-project/dashboards-observability/pull/2101))
* [Page Header] New page header for notebooks and UI updates ([#2099](https://github.com/opensearch-project/dashboards-observability/pull/2099), [#2103](https://github.com/opensearch-project/dashboards-observability/pull/2203))
* [Feature] OverviewPage made with Content Management ([#2077](https://github.com/opensearch-project/dashboards-observability/pull/2077))


### Opensearch Performance Analyzer


* Added cacheConfig Collector [#690](https://github.com/opensearch-project/performance-analyzer/pull/690)


### Opensearch Security Analytics Dashboards


* [Create detector] Update data source selection label and help text ([#1100](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1100))
* Use smaller and compressed varients of buttons and form components ([#1105](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1105))
* [navigation]fix: add threat detection header ([#1111](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1111))
* Page header updates to share common UI language in OSD ([#1117](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1117))
* Add threat alerts card for Analytics (All) workspace use case ([#1124](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1124))
* Update url with data source id; redirect on reload if ds id not present; minor fixes ([#1125](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1125))
* New home page related UI updates ([#1129](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1129))
* Fit and Finishes Changes for Security Analytics ([#1147](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1147))


### Opensearch System Templates

* Basic templates and addition of build steps ([#3](https://github.com/opensearch-project/opensearch-system-templates/pull/3))
* Onboarding New templates and adding zstd support ([#11](https://github.com/opensearch-project/opensearch-system-templates/pull/11))


### Opensearch k-NN


* Integrate Lucene Vector field with native engines to use KNNVectorFormat during segment creation ([#1945](https://github.com/opensearch-project/k-NN/pull/1945))
* k-NN query rescore support for native engines ([#1984](https://github.com/opensearch-project/k-NN/pull/1984))
* Add support for byte vector with Faiss Engine HNSW algorithm ([#1823](https://github.com/opensearch-project/k-NN/pull/1823))
* Add support for byte vector with Faiss Engine IVF algorithm ([#2002](https://github.com/opensearch-project/k-NN/pull/2002))
* Add mode/compression configuration support for disk-based vector search ([#2034](https://github.com/opensearch-project/k-NN/pull/2034))
* Add spaceType as a top level optional parameter while creating vector field. ([#2044](https://github.com/opensearch-project/k-NN/pull/2044))


### SQL


* Flint query scheduler part1 - integrate job scheduler plugin ([#2889](https://github.com/opensearch-project/sql/pull/2889))
* Flint query scheduler part 2 ([#2975](https://github.com/opensearch-project/sql/pull/2975))
* Add feature flag for async query scheduler ([#2989](https://github.com/opensearch-project/sql/pull/2989))


## ENHANCEMENTS


### Opensearch Dashboards Notifications


* [Navigation]feat: change parent item name ([#234](https://github.com/opensearch-project/dashboards-notifications/pull/234))
* Use smaller and compressed varients of buttons and form components ([#231](https://github.com/opensearch-project/dashboards-notifications/pull/231))
* Page header ([#236](https://github.com/opensearch-project/dashboards-notifications/pull/236))


### Opensearch Anomaly Detection


* Fix inference logic and standardize config index mapping ([#1284](https://github.com/opensearch-project/anomaly-detection/pull/1284))


### Opensearch Common Utils


* Updated pull request template to include API spec change in checklist ([#696](https://github.com/opensearch-project/common-utils/pull/696))


### Opensearch Dashboards Reporting


* Use smaller and compressed varients of buttons and form components ([#398](https://github.com/opensearch-project/dashboards-reporting/pull/398))
* [Enhancement] De-register reporting when MDS is enabled ([#411](https://github.com/opensearch-project/dashboards-reporting/pull/411))


### Opensearch Dashboards Search Relevance


* Use smaller and compressed varients of buttons and form components ([#421](https://github.com/opensearch-project/dashboards-search-relevance/pull/421))([#424](https://github.com/opensearch-project/dashboards-search-relevance/pull/424))
* New page header for search relevance ([#428](https://github.com/opensearch-project/dashboards-search-relevance/pull/428)) ([#430](https://github.com/opensearch-project/dashboards-search-relevance/pull/430))


### Opensearch Dashboards Visualizations


* Use smaller and compressed varients of buttons and form components ([#383](https://github.com/opensearch-project/dashboards-visualizations/pull/383))
* Update snapshots for OUI 1.10.0 ([#388](https://github.com/opensearch-project/dashboards-visualizations/pull/388))


### Opensearch Index Management Dashboards Plugin


* Update newHeader for Snapshot pages ([#1105](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1105))
* Reorder features and rename title and description in left nav bar ([#1106](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1106))
* Add MDS support in Notifications page ([#1121](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1121))
* Add Notification Modal in Indexes page ([#1143](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1143))
* Update new header for datastreams and rollups jobs ([#1115](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1115))
* Update newHeader for Index state management policies ([#1108](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1108))
* Update newHeader for component template pages ([#1122](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1122))
* Update new header for notification settings page ([#1126](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1126))
* Update new header for Alias, Index Templates, Policy Managed Indices, Indexes and Transform Jobs ([#1124](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1124))
* Use smaller and compressed varients of buttons and form components ([#1103](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1103))
* Making Look and Feel Changes in ISM pages ([#1123](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1123))
* Incorporate feel and look good guide changes for snapshots pages, datastreams, rollups and notification settings ([#1132](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1132))
* Add MDS support in Shrink page and fixing couple of bugs ([#1141](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1141))
* Fit and finish changes for Aliases, Templates and Policy managed Indices pages ([#1155](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1155))
* Consistency and Density Changes for Snapshot Management ([#1148](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1148))
* Fit and Finish changes for Indexes and Transform pages ([#1154](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1154))
* Fit and Finish Changes for DataStreams and Rollups ([#1153](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1153))
* Fit and finish changes for ISM policy & Composable template pages ([#1150](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1150))
* Fit and Finish Changes for Snapshot Management Pages ([#1157](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1157))
* Update rollup jobs and transform jobs title with total numbers of jobs ([#1164](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1164))
* Fixed bugs in history navigation in rollups and transform jobs pages and some UI changes ([#1166](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1166))


### Opensearch ML Commons


* Adding additional info for memory metadata ([#2750](https://github.com/opensearch-project/ml-commons/pull/2750))
* Support skip\_validating\_missing\_parameters in connector ([#2830](https://github.com/opensearch-project/ml-commons/pull/2830))
* Support one\_to\_one in ML Inference Search Response Processor ([#2801](https://github.com/opensearch-project/ml-commons/pull/2801))
* Expose ML Config API ([#2850](https://github.com/opensearch-project/ml-commons/pull/2850))


### Opensearch ML Commons Dashboards


* Use smaller and compressed varients of buttons and form components ([#349](https://github.com/opensearch-project/ml-commons-dashboards/pull/349))
* Support new page header API ([#351](https://github.com/opensearch-project/ml-commons-dashboards/pull/351))
* Align font size and style with UX guideline ([#355](https://github.com/opensearch-project/ml-commons-dashboards/pull/355))


### Opensearch Neural Search


* Adds rescore parameter support ([#885](https://github.com/opensearch-project/neural-search/pull/885))


### Opensearch Observability


* Update ndjson so workflow matches patterns created ([#2016](https://github.com/opensearch-project/dashboards-observability/pull/2016))
* Remove useless registration method ([#2044](https://github.com/opensearch-project/dashboards-observability/pull/2044))
* Use smaller and compressed varients of buttons and form components ([#2068](https://github.com/opensearch-project/dashboards-observability/pull/2068))
* [Enhancement] Deregister dashboards, applications, logs in MDS ([#2097](https://github.com/opensearch-project/dashboards-observability/pull/2097))
* Trace Analytics support for custom sources ([#2112](https://github.com/opensearch-project/dashboards-observability/pull/2112))
* [query assist] update api handler to accommodate new ml-commons config response ([#2111](https://github.com/opensearch-project/dashboards-observability/pull/2111))
* Update trace analytics landing page ([#2125](https://github.com/opensearch-project/dashboards-observability/pull/2125))
* [query assist] update ml-commons response schema ([#2124](https://github.com/opensearch-project/dashboards-observability/pull/2124))
* [MDS] Add support for register data sources during the absence of local cluster ([#2140](https://github.com/opensearch-project/dashboards-observability/pull/2140))


### Opensearch Observability


* Add allow unsecure node versions to CI .env ([#1861](https://github.com/opensearch-project/observability/pull/1861))


### Opensearch Query Insights


* Add ability to generate query shape for aggregation and sort portions of search body ([#44](https://github.com/opensearch-project/query-insights/pull/44))
* Query grouping framework for Top N queries and group by query similarity ([#66](https://github.com/opensearch-project/query-insights/pull/66))
* Minor enhancements to query categorization on tags and unit types ([#73](https://github.com/opensearch-project/query-insights/pull/73))


### Opensearch Query Workbench


* Use smaller and compressed varients of buttons and form components ([#370](https://github.com/opensearch-project/dashboards-query-workbench/pull/370))


### Opensearch Security


* Add `ignore_hosts` config option for auth failure listener ([#4538](https://github.com/opensearch-project/security/pull/4538))
* Added API roles for correlationAlerts ([#4689](https://github.com/opensearch-project/security/pull/4689))
* Allow multiple signing keys to be provided ([#4666](https://github.com/opensearch-project/security/pull/4666))
* Adding alerting comments security actions to roles.yml ([#4700](https://github.com/opensearch-project/security/pull/4700))
* Permission changes for correlationAlerts ([#4704](https://github.com/opensearch-project/security/pull/4704))


### Opensearch Security Analytics


* Added triggers in getDetectors API response ([#1226](https://github.com/opensearch-project/security-analytics/pull/1226))
* Secure rest tests for threat intel monitor apis ([#1212](https://github.com/opensearch-project/security-analytics/pull/1212))


### Opensearch Security Dashboards Plugin


* Adds page headers for updated UX ([#2083](https://github.com/opensearch-project/security-dashboards-plugin/pull/2083))
* Conditionally change where avatar shows up ([#2082](https://github.com/opensearch-project/security-dashboards-plugin/pull/2082))
* Use smaller and compressed varients of buttons and form components ([#2079](https://github.com/opensearch-project/security-dashboards-plugin/pull/2079))
* Use the `getRedirectUrl` from OSD to generate nextUrl ([#2072](https://github.com/opensearch-project/security-dashboards-plugin/pull/2072))
* Consistency and density improvements ([#2101](https://github.com/opensearch-project/security-dashboards-plugin/pull/2101))
* Add Proxy Auth to Multi Auth Options ([#2076](https://github.com/opensearch-project/security-dashboards-plugin/pull/2076))


### Opensearch k-NN


* Adds iterative graph build capability into a faiss index to improve the memory footprint during indexing and Integrates KNNVectorsFormat for native engines([#1950](https://github.com/opensearch-project/k-NN/pull/1950))
* Add model version to model metadata and change model metadata reads to be from cluster metadata ([#2005](https://github.com/opensearch-project/k-NN/pull/2005))


### SQL


* Change the default value of plugins.query.size\_limit to MAX\_RESULT\_WINDOW (10000) ([#2877](https://github.com/opensearch-project/sql/pull/2877))
* Support common format geo point ([#2896](https://github.com/opensearch-project/sql/pull/2896))
* Add TakeOrderedOperator ([#2906](https://github.com/opensearch-project/sql/pull/2906))
* IF function should support complex predicates in PPL ([#2970](https://github.com/opensearch-project/sql/pull/2970))
* Add flags for Iceberg and Lake Formation and Security Lake as a data source type ([#2978](https://github.com/opensearch-project/sql/pull/2978))
* Adds validation to allow only flint queries and sql SELECT queries to security lake type datasource ([#2977](https://github.com/opensearch-project/sql/pull/2977))
* Delegate Flint index vacuum operation to Spark ([#2995](https://github.com/opensearch-project/sql/pull/2995))


## BUG FIXES


### Opensearch Anomaly Detection


* Prevent resetting the latest flag of real-time when starting historical analysis ([#1287](https://github.com/opensearch-project/anomaly-detection/pull/1287))
* Correct handling of null max aggregation values in SearchResponse ([#1292](https://github.com/opensearch-project/anomaly-detection/pull/1292))


### Opensearch Alerting


* Fix monitor renew lock issue ([#1623](https://github.com/opensearch-project/alerting/pull/1623))
* Fix distribution builds ([#1637](https://github.com/opensearch-project/alerting/pull/1637))
* Fix distribution builds ([#1640](https://github.com/opensearch-project/alerting/pull/1640))


### Opensearch Alerting Dashboards Plugin


* Fixed cypress tests. ([#1027](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1027))
* [Navigation] Fix: remove the workspaceAvailability field to make alert visible within workspace ([#1028](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1028))
* Fix failed UT of AddAlertingMonitor.test.js ([#1040](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1040))
* Issue #671 Fix trigger name validation ([#794](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/794))
* Fix alerts card in all-use case overview page ([#1073](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1073))


### Opensearch Anomaly Detection Dashboards


* Fix an issue that causes dataSourceId to not show in the URL on Overview landing page ([#828](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/828))
* Remove dataSourceFilter that breaks DataSourceView ([#837](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/837))


### Opensearch Common Utils


* Added missing ctx variables ([#710](https://github.com/opensearch-project/common-utils/pull/710))
* Changed the names of security actions for Alerting Comments feature ([#724](https://github.com/opensearch-project/common-utils/pull/724))


### Opensearch Cross Cluster Replication


* Updating remote-migration IT with correct setting name ([#1412](https://github.com/opensearch-project/cross-cluster-replication/pull/1412))


### Opensearch Dashboards Notifications


* Fix link checker ([#242](https://github.com/opensearch-project/dashboards-notifications/pull/242))
* Persist dataSourceId across applications under new Nav change ([#244](https://github.com/opensearch-project/dashboards-notifications/pull/244))


### Opensearch Dashboards Reporting


* [Bugfix] Update UI and handle new navigation ([#416](https://github.com/opensearch-project/dashboards-reporting/pull/416))
* [Bug] Remove unused import ([#419](https://github.com/opensearch-project/dashboards-reporting/pull/419))


### Opensearch Dashboards Search Relevance


* Fix sass division warning ([#426](https://github.com/opensearch-project/dashboards-search-relevance/pull/426))([#435](https://github.com/opensearch-project/dashboards-search-relevance/pull/435))


### Opensearch Index Management


* Skipping execution based on cluster service ([#1219](https://github.com/opensearch-project/index-management/pull/1219))


### Opensearch Index Management Dashboards Plugin


* Fix for snapshot test race condition ([#1113](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1113))


### Opensearch Job Scheduler


* Fix system index compatibility with v1 templates [(#658)](https://github.com/opensearch-project/job-scheduler/pull/658) [(#659)](https://github.com/opensearch-project/job-scheduler/pull/659).


### Opensearch ML Commons


* Fix delete local model twice quickly get 500 response issue ([#2806](https://github.com/opensearch-project/ml-commons/pull/2806))
* Fix cohere model input interface cannot validate cohere input issue ([#2847](https://github.com/opensearch-project/ml-commons/pull/2847))
* Add processed function for remote inference input dataset parameters to convert it back to its original datatype ([#2852](https://github.com/opensearch-project/ml-commons/pull/2852))
* Use local\_regex as default type for guardrails ([#2853](https://github.com/opensearch-project/ml-commons/pull/2853))
* Agent execution error in json format ([#2858](https://github.com/opensearch-project/ml-commons/pull/2858))
* Fix custom prompt substitute with List issue in ml inference search response processor ([#2871](https://github.com/opensearch-project/ml-commons/pull/2871))
* Fix breaking changes in config index fields ([#2882](https://github.com/opensearch-project/ml-commons/pull/2882))
* Output only old fields in get config API ([#2892](https://github.com/opensearch-project/ml-commons/pull/2892))
* Fix http dependency in CancelBatchJobTransportAction ([#2898](https://github.com/opensearch-project/ml-commons/pull/2898))


### Opensearch ML Commons Dashboards


* Fix connector router response 500 ([#358](https://github.com/opensearch-project/ml-commons-dashboards/pull/358))


### Opensearch Neural Search


* Removing code to cut search results of hybrid search in the priority queue ([#867](https://github.com/opensearch-project/neural-search/pull/867))
* Fixed merge logic in hybrid query for multiple shards case ([#877](https://github.com/opensearch-project/neural-search/pull/877))


### Opensearch Observability


* [Bug] Trace Analytics bug fix for local cluster being rendered ([#2006](https://github.com/opensearch-project/dashboards-observability/pull/2006))
* Fix docker links & index patterns names ([#2017](https://github.com/opensearch-project/dashboards-observability/pull/2017))
* Traces and Spans tab Fix for application analytics ([#2023](https://github.com/opensearch-project/dashboards-observability/pull/2023))
* Link fixes for csv ([#2031](https://github.com/opensearch-project/dashboards-observability/pull/2031))
* Fix direct url load for trace analytics ([#2024](https://github.com/opensearch-project/dashboards-observability/pull/2024))
* [Bug] Trace Analytics bugfix for breadcrumbs and id pathing ([#2037](https://github.com/opensearch-project/dashboards-observability/pull/2037))
* Fix badge size for counters, change notebook delete, update test ([#2110](https://github.com/opensearch-project/dashboards-observability/pull/2110))
* [Bug] Fixed traces bug for missing MDS id ([#2100](https://github.com/opensearch-project/dashboards-observability/pull/2100))
* [BUG] Fix add sample notebooks ([#2108](https://github.com/opensearch-project/dashboards-observability/pull/2108))


### Opensearch Query Insights


* Make sure listener is started when query metrics enabled ([#74](https://github.com/opensearch-project/query-insights/pull/74))


### Opensearch Query Workbench


* Bug fix for missing id in old nav ([#382](https://github.com/opensearch-project/dashboards-query-workbench/pull/382))


### Opensearch Reporting


* Increase accuracy seconds while testing create on-demand report from definition ([#1022](https://github.com/opensearch-project/reporting/pull/1022))


### Opensearch Security


* Addresses a bug with `plugins.security.allow_unsafe_democertificates` setting ([#4603](https://github.com/opensearch-project/security/pull/4603))
* Fix covereage-report workflow ([#4684](https://github.com/opensearch-project/security/pull/4684), [#4683](https://github.com/opensearch-project/security/pull/4683))
* Handle the audit config being null ([#4664](https://github.com/opensearch-project/security/pull/4664))
* Fixes authtoken endpoint ([#4631](https://github.com/opensearch-project/security/pull/4631))
* Fixed READ\_ACTIONS required by TermsAggregationEvaluator ([#4607](https://github.com/opensearch-project/security/pull/4607))
* Sort the DNS Names in the SANs ([#4640](https://github.com/opensearch-project/security/pull/4640))


### Opensearch Security Analytics


* Adds user validation for threat intel transport layer classes and stashes the thread context for all system index interactions ([#1207](https://github.com/opensearch-project/security-analytics/pull/1207))
* Fix mappings integ tests ([#1213](https://github.com/opensearch-project/security-analytics/pull/1213))
* Bug fixes for threat intel ([#1223](https://github.com/opensearch-project/security-analytics/pull/1223))
* make threat intel run with standard detectors ([#1234](https://github.com/opensearch-project/security-analytics/pull/1234))
* Fixed searchString bug. Removed nested IOC mapping structure. ([#1239](https://github.com/opensearch-project/security-analytics/pull/1239))
* Adds toggling refresh disable/enable for deactivate/activate operation while updating URL\_DOWNLOAD type configs ([#1240](https://github.com/opensearch-project/security-analytics/pull/1240))
* Make threat intel source config release lock event driven ([#1254](https://github.com/opensearch-project/security-analytics/pull/1254))
* Fix S3 validation errors not caught by action listener ([#1257](https://github.com/opensearch-project/security-analytics/pull/1257))
* Clean up empty IOC indices created by failed source configs ([#1267](https://github.com/opensearch-project/security-analytics/pull/1267))
* Fix threat intel multinode tests ([#1274](https://github.com/opensearch-project/security-analytics/pull/1274))
* Update threat intel job mapping to new version ([#1272](https://github.com/opensearch-project/security-analytics/pull/1272))
* Stash context for List IOCs Api ([#1278](https://github.com/opensearch-project/security-analytics/pull/1278))


### Opensearch Security Analytics Dashboards


* [Navigation] Update nav category and workspaceAvailability ([#1093](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1093))
* Fix UI issues ([#1107](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1107))
* Bug fixes PageHeader and SideNav ([#1123](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1123))
* Added check for multi data source support when rendering threat alerts card in all use case workspace ([#1132](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1132))
* Made import more specific to avoid importing incorrect modules ([#1136](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1136))
* Remove import causing error ([#1144](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1144))
* Passthrough URL state and other params when updating search query ([#1149](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1149))


### Opensearch Security Dashboards Plugin


* Do not register tenancy app if disabled in yml ([#2057](https://github.com/opensearch-project/security-dashboards-plugin/pull/2057))
* Ux fixes for page header ([#2108](https://github.com/opensearch-project/security-dashboards-plugin/pull/2108))
* Fix a bug where basepath nextUrl is invalid when it should be valid ([#2096](https://github.com/opensearch-project/security-dashboards-plugin/pull/2096))
* Feat: update title and descriptions ([#2084](https://github.com/opensearch-project/security-dashboards-plugin/pull/2084))


### Opensearch k-NN


* Corrected search logic for scenario with non-existent fields in filter ([#1874](https://github.com/opensearch-project/k-NN/pull/1874))
* Add script\_fields context to KNNAllowlist ([#1917](https://github.com/opensearch-project/k-NN/pull/1917))
* Fix graph merge stats size calculation ([#1844](https://github.com/opensearch-project/k-NN/pull/1844))
* Disallow a vector field to have an invalid character for a physical file name. ([#1936](https://github.com/opensearch-project/k-NN/pull/1936))
* Fix memory overflow caused by cache behavior ([#2015](https://github.com/opensearch-project/k-NN/pull/2015))
* Use correct type for binary vector in ivf training ([#2086](https://github.com/opensearch-project/k-NN/pull/2086))
* Switch MINGW32 to MINGW64 ([#2090](https://github.com/opensearch-project/k-NN/pull/2090))


### SQL


* Restrict UDF functions ([#2884](https://github.com/opensearch-project/sql/pull/2884))
* Update SqlBaseParser ([#2890](https://github.com/opensearch-project/sql/pull/2890))
* Boolean function in PPL should be case insensitive ([#2842](https://github.com/opensearch-project/sql/pull/2842))
* Fix SparkExecutionEngineConfigClusterSetting deserialize issue ([#2972](https://github.com/opensearch-project/sql/pull/2972))
* Fix jobType for Batch and IndexDML query ([#2982](https://github.com/opensearch-project/sql/pull/2982))
* Fix handler for existing query ([#2983](https://github.com/opensearch-project/sql/pull/2983))


## INFRASTRUCTURE


### Opensearch Anomaly Detection Dashboards


* Fix monaco import issue in UTs ([#834](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/834))
* Address CVE-2024-4067 ([#864](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/864))


### Opensearch Dashboards Maps


* Use functional test repo to run maps integration test workflow ([#664](https://github.com/opensearch-project/dashboards-maps/pull/664))


### Opensearch ML Commons


* Test: recover search index tool it in multi node cluster ([#2407](https://github.com/opensearch-project/ml-commons/pull/2407))


### Opensearch Neural Search


* Update batch related tests to use batch\_size in processor & refactor BWC version check ([#852](https://github.com/opensearch-project/neural-search/pull/852))


### Opensearch Performance Analyzer


* Bump PA to use 1.6.0 PA commons lib ([#712](https://github.com/opensearch-project/performance-analyzer/pull/712))


### Opensearch Query Insights


* Add code hygiene checks for query insights ([#51](https://github.com/opensearch-project/query-insights/pull/51))
* Add configuration for publishing snapshot ([#90](https://github.com/opensearch-project/query-insights/pull/90))


### Opensearch k-NN


* Parallelize make to reduce build time ([#2006](https://github.com/opensearch-project/k-NN/pull/2006))


### SQL


* Increment version to 2.17.0-SNAPSHOT ([#2892](https://github.com/opensearch-project/sql/pull/2892))
* Fix :integ-test:sqlBwcCluster#fullRestartClusterTask ([#2996](https://github.com/opensearch-project/sql/pull/2996))


## DOCUMENTATION


### Opensearch Alerting


* Added 2.17 release notes. ([#1650](https://github.com/opensearch-project/alerting/pull/1650))


### Opensearch Alerting Dashboards Plugin


* Added 2.17 release notes. ([#1065](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1065))


### Opensearch Common Utils


* Added 2.17.0.0 release notes ([#727](https://github.com/opensearch-project/common-utils/pull/727))


### Opensearch Dashboards Notifications


* 2.17 release notes. ([#248](https://github.com/opensearch-project/dashboards-notifications/pull/248))


### Opensearch Dashboards Search Relevance


* Update Links in Documentation ([#420](https://github.com/opensearch-project/dashboards-search-relevance/pull/420))([#440](https://github.com/opensearch-project/dashboards-search-relevance/pull/440))
* Adding sumukhswamy as maintainer ([#437](https://github.com/opensearch-project/dashboards-search-relevance/pull/437))([#438](https://github.com/opensearch-project/dashboards-search-relevance/pull/438))


### Opensearch ML Commons


* Add tutorial for Bedrock Guardrails ([#2695](https://github.com/opensearch-project/ml-commons/pull/2695))


### Opensearch Notifications


* Add 2.17.0 release notes (#[947](https://github.com/opensearch-project/notifications/pull/947))


### Opensearch Query Insights


* Update GET top N api documentation about the type parameter ([#8139](https://github.com/opensearch-project/documentation-website/pull/8139))
* Added 2.17 release notes ([#91](https://github.com/opensearch-project/query-insights/pull/91))


### Opensearch Security Analytics


* Added 2.17.0 release notes. ([#1290](https://github.com/opensearch-project/security-analytics/pull/1290))


### Opensearch Security Analytics Dashboards


* Added v2.17 release notes. ([#1141](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1141))


## MAINTENANCE


### Dashboards Assistant


* Bump `micromatch` to 4.0.8 ([#269](https://github.com/opensearch-project/dashboards-assistant/pull/269))


### Opensearch Alerting


* Increment version to 2.17.0-SNAPSHOT. ([#1635](https://github.com/opensearch-project/alerting/pull/1635))
* Disabled non-security tests from executing during security-enabled CI workflows. ([#1632](https://github.com/opensearch-project/alerting/pull/1632))


### Opensearch Alerting Dashboards Plugin


* Increment version to 2.17.0.0 ([#1054](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1054))
* [CVE-2024-4068] Pinned package version for braces ([#1024](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1024))
* [CVE-2024-4067] Fix CVE-2024-4067. ([#1074](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1074))


### Opensearch Anomaly Detection Dashboards


* Update 2.x to 2.17.0 ([#844](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/844))


### Opensearch Asynchronous Search


* Increment version to 2.17.0 ([#602](https://github.com/opensearch-project/asynchronous-search/pull/602))


### Opensearch Common Utils


* Fixed Common-Utils CIs: ([#703](https://github.com/opensearch-project/common-utils/pull/703))


### Opensearch Dashboards Maps


* Deprecated maps multi data source display ([#651](https://github.com/opensearch-project/dashboards-maps/pull/651))


### Opensearch Dashboards Notifications


* [Backport 2.x] add riysaxen as maintainer ([#241](https://github.com/opensearch-project/dashboards-notifications/pull/241))
* Increment version to 2.17.0.0 ([#237](https://github.com/opensearch-project/dashboards-notifications/pull/241))


### Opensearch Dashboards Search Relevance


* Increment version to 2.17.0.0 ([#425](https://github.com/opensearch-project/dashboards-search-relevance/pull/425))


### Opensearch Dashboards Visualizations


* Increment version to 2.17.0.0 ([#386](https://github.com/opensearch-project/dashboards-visualizations/pull/386))
* Adding release notes for 2.17.0 ([#392](https://github.com/opensearch-project/dashboards-visualizations/pull/392))


### Opensearch Index Management


* Increment version to 2.17.0-SNAPSHOT ([#1221](https://github.com/opensearch-project/index-management/pull/1221))
* Use adminClient instead of client when interacting with system index in integTests ([#1222](https://github.com/opensearch-project/index-management/pull/1222))
* Move non-active maintainers to emeritus ([#1233](https://github.com/opensearch-project/index-management/pull/1233))


### Opensearch Index Management Dashboards Plugin


* Increment version to 2.17.0.0 ([#1127](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1127))


### Opensearch Job Scheduler


* Increment version to 2.17.0 ([#660](https://github.com/opensearch-project/job-scheduler/pull/660)).
* Dependabot: bump org.gradle.test-retry from 1.5.9 to 1.5.10 ([#653](https://github.com/opensearch-project/job-scheduler/pull/653)) ([#654](https://github.com/opensearch-project/job-scheduler/pull/654)).
* Dependabot: bump com.google.googlejavaformat:google-java-format ([#663](https://github.com/opensearch-project/job-scheduler/pull/663)) ([#664](https://github.com/opensearch-project/job-scheduler/pull/664)).
* Dependabot: bump org.slf4j:slf4j-api from 2.0.13 to 2.0.16 ([#666](https://github.com/opensearch-project/job-scheduler/pull/666)) ([#667](https://github.com/opensearch-project/job-scheduler/pull/667)).
* Dependabot: bump com.netflix.nebula.ospackage from 11.9.1 to 11.10.0 ([#668](https://github.com/opensearch-project/job-scheduler/pull/668)) ([#669](https://github.com/opensearch-project/job-scheduler/pull/669)).


### Opensearch ML Commons


* Applying spotless to common module ([#2815](https://github.com/opensearch-project/ml-commons/pull/2815))
* Fix Cohere test ([#2831](https://github.com/opensearch-project/ml-commons/pull/2831))


### Opensearch ML Commons Dashboards


* Increment version to 2.17.0.0 ([#353](https://github.com/opensearch-project/ml-commons-dashboards/pull/353))
* Bump micromatch from 4.0.5 to 4.0.8 ([#356](https://github.com/opensearch-project/ml-commons-dashboards/pull/356))


### Opensearch Notifications


* Increment version to 2.17.0-SNAPSHOT ([#939](https://github.com/opensearch-project/notifications/pull/939))


### Opensearch Observability


* Update getting-started links to match recent catalog PR merges ([#2012](https://github.com/opensearch-project/dashboards-observability/pull/2006))
* Fix Observability CI workflow checks ([#2046](https://github.com/opensearch-project/dashboards-observability/pull/2046))
* Bump org.json:json ([#1966](https://github.com/opensearch-project/dashboards-observability/pull/1966))
* Update the actions/upload-artifact from v1 to v4 ([#2133](https://github.com/opensearch-project/dashboards-observability/pull/2133))
* [CVE] Bump the lint-staged from 13.1.0 to 15.2.10 ([#2138](https://github.com/opensearch-project/dashboards-observability/pull/2138))


### Opensearch Query Insights


* Fix CVE-2023-2976 for checkstyle ([#58](https://github.com/opensearch-project/query-insights/pull/58))
* Fix security based integration tests ([#59](https://github.com/opensearch-project/query-insights/pull/59))
* Add query shape hash method ([#64](https://github.com/opensearch-project/query-insights/pull/64))
* Add more integration tests for query insights ([#71](https://github.com/opensearch-project/query-insights/pull/71))
* Query grouping integration tests ([#85](https://github.com/opensearch-project/query-insights/pull/85))
* Add additional grouping ITs and refactor ([#89](https://github.com/opensearch-project/query-insights/pull/89))


### Opensearch Query Workbench


* Increment version to 2.17.0.0 ([#376](https://github.com/opensearch-project/dashboards-query-workbench/pull/376))
* Add release notes for 2.17.0 ([#388](https://github.com/opensearch-project/dashboards-query-workbench/pull/388))
* [CVE] Bump the lint-staged from 13.1.0 to 15.2.10 ([#396](https://github.com/opensearch-project/dashboards-query-workbench/pull/396))


### Opensearch Security


* Bump com.google.errorprone:error\_prone\_annotations from 2.30.0 to 2.31.0 ([#4696](https://github.com/opensearch-project/security/pull/4696))
* Bump org.passay:passay from 1.6.4 to 1.6.5 ([#4682](https://github.com/opensearch-project/security/pull/4682))
* Bump spring\_version from 5.3.37 to 5.3.39 ([#4661](https://github.com/opensearch-project/security/pull/4661))
* Bump commons-cli:commons-cli from 1.8.0 to 1.9.0 ([#4659](https://github.com/opensearch-project/security/pull/4659))
* Bump org.junit.jupiter:junit-jupiter from 5.10.3 to 5.11.0 ([#4657](https://github.com/opensearch-project/security/pull/4657))
* Bump org.cryptacular:cryptacular from 1.2.6 to 1.2.7 ([#4656](https://github.com/opensearch-project/security/pull/4656))
* Update Gradle to 8.10 ([#4646](https://github.com/opensearch-project/security/pull/4646))
* Bump org.xerial.snappy:snappy-java from 1.1.10.5 to 1.1.10.6 ([#4639](https://github.com/opensearch-project/security/pull/4639))
* Bump com.google.googlejavaformat:google-java-format from 1.22.0 to 1.23.0 ([#4622](https://github.com/opensearch-project/security/pull/4622))
* Increment version to 2.17.0-SNAPSHOT ([#4615](https://github.com/opensearch-project/security/pull/4615))
* Backports PRs with `backport-failed` labels that weren't actually backported ([#4610](https://github.com/opensearch-project/security/pull/4610))
* Bump io.dropwizard.metrics:metrics-core from 4.2.26 to 4.2.27 ([#4660](https://github.com/opensearch-project/security/pull/4660))
* Bump com.netflix.nebula.ospackage from 11.9.1 to 11.10.0 ([#4681](https://github.com/opensearch-project/security/pull/4681))
* Interim build fix for PluginSubject related changes ([#4694](https://github.com/opensearch-project/security/pull/4694))
* Add Nils Bandener (Github: nibix) as a maintainer ([#4673](https://github.com/opensearch-project/security/pull/4673))
* Remove usages of org.apache.logging.log4j.util.Strings ([#4653](https://github.com/opensearch-project/security/pull/4653))
* Update backport section of PR template ([#4625](https://github.com/opensearch-project/security/pull/4625))
* Bump org.checkerframework:checker-qual from 3.45.0 to 3.46.0 ([#4623](https://github.com/opensearch-project/security/pull/4623))
* Refactor security provider instantiation ([#4611](https://github.com/opensearch-project/security/pull/4611))


### Opensearch Security Analytics


* Update build.gradle to use alerting-spi snapshot version ([#1217](https://github.com/opensearch-project/security-analytics/pull/1217))


### Opensearch Security Analytics Dashboards


* Updated snapshots to fix unit test CI ([#1095](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1095))
* Increment version to 2.17.0.0 ([#1120](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1120))
* Fixed CVEs. ([#1133](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1133))


### Opensearch Security Dashboards Plugin


* Updates backport workflow ([#2074](https://github.com/opensearch-project/security-dashboards-plugin/pull/2074))
* Fixes spacing in package.json ([#2068](https://github.com/opensearch-project/security-dashboards-plugin/pull/2068))
* Increment version to 2.17.0.0 ([#2090](https://github.com/opensearch-project/security-dashboards-plugin/pull/2090))


### Opensearch Skills


* Update dependency org.apache.logging.log4j:log4j-slf4j-impl to v2.23.1 ([#256](https://github.com/opensearch-project/skills/pull/256))
* Update dependency com.google.guava:guava to v33.2.1-jre ([#258](https://github.com/opensearch-project/skills/pull/258))
* Upgrade apache common lang version to 3.16 ([#371](https://github.com/opensearch-project/skills/pull/371))
* Update dependency gradle to v8.10 ([#389](https://github.com/opensearch-project/skills/pull/389))
* Update plugin io.freefair.lombok to v8.10 ([#393](https://github.com/opensearch-project/skills/pull/393))


### Opensearch k-NN


* Fix a flaky unit test:testMultiFieldsKnnIndex, which was failing due to inconsistent merge behaviors ([#1924](https://github.com/opensearch-project/k-NN/pull/1924))


## REFACTORING


### Opensearch Alerting Dashboards Plugin


* Support date\_nanos type when select time field for creating monitor ([#954](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/954))
* Updated all pages with new header UI ([#1056](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1056))
* Register alerts card with analytics workspace use case ([#1064](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1064))


### Opensearch Dashboards Maps


* Consistency and Desntiy changes ([#659](https://github.com/opensearch-project/dashboards-maps/pull/659))


### Opensearch Flow Framework


* Refactor workflow step resource updates to eliminate duplication ([#796](https://github.com/opensearch-project/flow-framework/pull/796))


### Opensearch ML Commons


* Code refactor not to occur nullpointer exception ([#2816](https://github.com/opensearch-project/ml-commons/pull/2816))


### Opensearch k-NN


* Introduce KNNVectorValues interface to iterate on different types of Vector values during indexing and search ([#1897](https://github.com/opensearch-project/k-NN/pull/1897))
* Integrate KNNVectorValues with vector ANN Search flow ([#1952](https://github.com/opensearch-project/k-NN/pull/1952))
* Clean up parsing for query ([#1824](https://github.com/opensearch-project/k-NN/pull/1824))
* Refactor engine package structure ([#1913](https://github.com/opensearch-project/k-NN/pull/1913))
* Refactor method structure and definitions ([#1920](https://github.com/opensearch-project/k-NN/pull/1920))
* Refactor KNNVectorFieldType from KNNVectorFieldMapper to a separate class for better readability. ([#1931](https://github.com/opensearch-project/k-NN/pull/1931))
* Generalize lib interface to return context objects ([#1925](https://github.com/opensearch-project/k-NN/pull/1925))
* Restructure mappers to better handle null cases and avoid branching in parsing ([#1939](https://github.com/opensearch-project/k-NN/pull/1939))
* Added Quantization Framework and implemented 1Bit and multibit quantizer ([#1889](https://github.com/opensearch-project/k-NN/issues/1889))
* Encapsulate dimension, vector data type validation/processing inside Library ([#1957](https://github.com/opensearch-project/k-NN/pull/1957))
* Add quantization state cache ([#1960](https://github.com/opensearch-project/k-NN/pull/1960))
* Add quantization state reader and writer ([#1997](https://github.com/opensearch-project/k-NN/pull/1997))


### SQL


* Add RequestContext parameter to verifyDataSourceAccessAndGetRawMetada method ([#2872](https://github.com/opensearch-project/sql/pull/2872))
* Add AsyncQueryRequestContext to QueryIdProvider parameter ([#2887](https://github.com/opensearch-project/sql/pull/2887))
* Add AsyncQueryRequestContext to FlintIndexMetadataService/FlintIndexStateModelService ([#2885](https://github.com/opensearch-project/sql/pull/2885))
* Add mvQuery attribute in IndexQueryDetails ([#2951](https://github.com/opensearch-project/sql/pull/2951))
* Add AsyncQueryRequestContext to update/get in StatementStorageService ([#2953](https://github.com/opensearch-project/sql/pull/2953))
* Extract validation logic from FlintIndexMetadataServiceImpl ([#2954](https://github.com/opensearch-project/sql/pull/2954))





