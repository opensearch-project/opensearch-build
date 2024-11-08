# OpenSearch and OpenSearch Dashboards 2.18.0 Release Notes

## Release Highlights

OpenSearch 2.18 includes a number of updates that help you build machine learning (ML)-powered applications, increase performance and stability, and improve the way you and your teams collaborate using OpenSearch.

### NEW AND UPDATED FEATURES

* Enhancements to the ML inference search response processor improve the integration of ML models in search pipelines, enabling more sophisticated and context-aware document ranking and result augmentation.
* A new reranker type, ByField, has been added to the rerank processor, allowing you to perform a second-level rerank on search results, based on a specified target field, to achieve greater search relevance.
* New performance updates for vector search applications include optimizations for better memory and cache management for native libraries, an updated approach to creating vector data structures to accelerate index creation, and the integration of AVX512 SIMD support for the Faiss engine.
* You can now define the search pipeline parameter directly within the Multi-search API request body when building search pipelines, offering greater flexibility and control over search pipeline deployments.
* New paginated APIs for _cat/indices and _cat/shards let you take advantage of _cat APIs for troubleshooting at scale in larger clusters, avoiding performance constraints.
* Grouping top N queries by similarity now supports field names and data types, allowing you to group queries at a finer level of detail so that you can better identify and analyze resource-intensive query patterns across query types.
* Workspaces provide a new multi-tenant environment to increase team collaboration. Granular access controls let you manage or remove collaborators and control their access at the workspace level with role-based permissions.
* A redesigned homepage and navigation structure provide a centralized toolkit for accessing and creating Workspaces, with a more cleanly organized navigation bar that adapts to the selected workspace and supports tailored workflows
* Two new analyzers, [`phone` and `phone-search`](https://opensearch.org/docs/latest/analyzers/supported-analyzers/phone-analyzers/), have been added as an optional plugin to simplify the complex task of parsing global phone numbers.


### EXPERIMENTAL FEATURES

OpenSearch 2.18 includes the following experimental functionality. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.

* An updated Discover interface enhances the query experience and offers greater customization options. This release adds PPL and SQL as query options in Discover alongside Dashboards Query Language (DQL) and Lucene, and improvements to the data selector and the addition of autocomplete functionality further enhance usability.


## Release Details
[OpenSearch and OpenSearch Dashboards 2.18.0](https://opensearch.org/versions/opensearch-2-18-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.18/release-notes/opensearch.release-notes-2.18.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.18/release-notes/opensearch-dashboards.release-notes-2.18.0.md).


## FEATURES


### OpenSearch Dashboards Assistant


* Feat: Add new feature to support text to visualization([#264](https://github.com/opensearch-project/dashboards-assistant/pull/264),[#299](https://github.com/opensearch-project/dashboards-assistant/pull/299),[#310](https://github.com/opensearch-project/dashboards-assistant/pull/310),[#313](https://github.com/opensearch-project/dashboards-assistant/pull/313),[#325](https://github.com/opensearch-project/dashboards-assistant/pull/325),[#327](https://github.com/opensearch-project/dashboards-assistant/pull/327),[#330](https://github.com/opensearch-project/dashboards-assistant/pull/330),[#312](https://github.com/opensearch-project/dashboards-assistant/pull/312),[#350](https://github.com/opensearch-project/dashboards-assistant/pull/350),[#354](https://github.com/opensearch-project/dashboards-assistant/pull/354),[#351](https://github.com/opensearch-project/dashboards-assistant/pull/351))
* Feat: Take index pattern and user input to t2viz from discover([#349](https://github.com/opensearch-project/dashboards-assistant/pull/349))
* Feat: Add discovery summary API([#295](https://github.com/opensearch-project/dashboards-assistant/pull/295))
* Feat: Add metrics for alerting summary([#304](https://github.com/opensearch-project/dashboards-assistant/pull/304))
* Feat: Add log pattern for alerting summary.([#339](https://github.com/opensearch-project/dashboards-assistant/pull/339), [#341](https://github.com/opensearch-project/dashboards-assistant/pull/341))
* Feat: Add navigating to discover from alerting summary([#316](https://github.com/opensearch-project/dashboards-assistant/pull/316), [#337](https://github.com/opensearch-project/dashboards-assistant/pull/337),[#345](https://github.com/opensearch-project/dashboards-assistant/pull/345),[#347](https://github.com/opensearch-project/dashboards-assistant/pull/347))
* Feat: Add alerting insight with RAG([#266](https://github.com/opensearch-project/dashboards-assistant/pull/266),[#343](https://github.com/opensearch-project/dashboards-assistant/pull/343))
* Feat: Add an API to check if a give agent config name has agent id configured([#307](https://github.com/opensearch-project/dashboards-assistant/pull/307))
* Feat: Add assistant capabilities to control rendering components([#267](https://github.com/opensearch-project/dashboards-assistant/pull/267))


### Opensearch Custom Codecs


* Lucene 9.12.0 Upgrade ([#198](https://github.com/opensearch-project/custom-codecs/pull/198))


### Opensearch Dashboards Maps


* [Navigation]Feat: Update category to flatten menus in analytics(all) use case ([#674](https://github.com/opensearch-project/dashboards-maps/pull/674))


### Opensearch Dashboards Search Relevance


* Navigate to import\_sample\_data app when navGroupEnabled ([#457](https://github.com/opensearch-project/dashboards-search-relevance/pull/457))([#458](https://github.com/opensearch-project/dashboards-search-relevance/pull/458))


### Opensearch Flow Framework


* Add ApiSpecFetcher for Fetching and Comparing API Specifications ([#651](https://github.com/opensearch-project/flow-framework/issues/651))


* Add optional config field to tool step ([#899](https://github.com/opensearch-project/flow-framework/pull/899))


### Opensearch Neural Search


* Introduces ByFieldRerankProcessor for second level reranking on documents ([#932](https://github.com/opensearch-project/neural-search/pull/932))


### Opensearch Observability


* [Feature] Auto trigger schema setup in assets creation flow of get started page ([#2200](https://github.com/opensearch-project/dashboards-observability/pull/2200))


### Opensearch Security Analytics Dashboards


* Feat: Update category ([#1169](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1169))
* Fit and Finish UX Fixes ([#1174](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1174))
* [Fit&Finish] Security analytics overview page ([#1175](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1175))
* Added HOURS option for source refresh interval. ([#1197](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1197))


### Opensearch Skills


* Add LogPatternTool ([#413](https://github.com/opensearch-project/skills/pull/413))
* Optimize the default prompt and make prompt customizable for create anomaly detector tool ([#399](https://github.com/opensearch-project/skills/pull/399))


### Opensearch k-NN


* Add AVX512 support to k-NN for FAISS library ([#2069](https://github.com/opensearch-project/k-NN/pull/2069))


### OpenSearch SQL


* Backport #2981 to 2.x ([#3111](https://github.com/opensearch-project/sql/pull/3111))


## ENHANCEMENTS


### Opensearch Alerting Dashboards Plugin


* Context aware alert analysis ([#996](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/996))
* [Navigation]Feat: update category to flatten menus in analytics(all) use case ([#1114](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1114))
* Support top N log pattern data in summary context provider for visual editor monitor ([#1119](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1119))


### Opensearch Anomaly Detection


* Add rule validation in AnomalyDetector constructor ([#1341](https://github.com/opensearch-project/anomaly-detection/pull/1341))


### Opensearch Anomaly Detection Dashboards


* Report metrics for suggest anomaly detector ([#876](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/876))
* [Navigation]Feat: Update category to flatten menus in analytics(all) use case ([#883](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/883))
* Fallback to cluster health on remote info failure ([#886](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/886))
* Sync code from 2.x to mds-2.17 ([#900](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/900))


### Opensearch Common Utils


* Changes to support dynamic deletion of doc-level monitor query indices ([#734](https://github.com/opensearch-project/common-utils/pull/734))


### Opensearch Flow Framework


* Incrementally remove resources from workflow state during deprovisioning ([#898](https://github.com/opensearch-project/flow-framework/pull/898))


### Opensearch Index Management


* Allowing non-rollup and rollup indices to be searched together ([#1268](https://github.com/opensearch-project/index-management/pull/1268))


### Opensearch Index Management Dashboards Plugin


* Fit and Finish UX changes ([#1179](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1179))
* Replaced EuiText with EuiTitle for section headers in content areas ([#1182](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1182))
* Setting validation for transform APIs ([#1191](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1191))


### Opensearch ML Commons


* Filter out remote model auto redeployment ([#2976](https://github.com/opensearch-project/ml-commons/pull/2976))
* Allow llmQuestion to be optional when llmMessages is used. ([#3072](https://github.com/opensearch-project/ml-commons/pull/3072))
* Enhance batch job task management by adding default action types ([#3080](https://github.com/opensearch-project/ml-commons/pull/3080))
* Use connector credential in offline batch ingestion ([#2989](https://github.com/opensearch-project/ml-commons/pull/2989))
* Change to model group access for batch job task APIs ([#3098](https://github.com/opensearch-project/ml-commons/pull/3098))
* Add rate limiting for offline batch jobs, set default bulk size to 500 ([#3116](https://github.com/opensearch-project/ml-commons/pull/3116))
* Support ML Inference Search Processor Writing to Search Extension ([#3061](https://github.com/opensearch-project/ml-commons/pull/3061))
* Enable pass query string to input\_map in ml inference search response processor ([#2899](https://github.com/opensearch-project/ml-commons/pull/2899))
* Add config field in MLToolSpec for static parameters ([#2977](https://github.com/opensearch-project/ml-commons/pull/2977))
* Add textract and comprehend url to trusted endpoints ([#3154](https://github.com/opensearch-project/ml-commons/pull/3154))


### Opensearch ML Commons Dashboards


* Reduce machine learning table spacing when new home page enabled ([#377](https://github.com/opensearch-project/ml-commons-dashboards/pull/377))


### Opensearch Neural Search


* Implement `ignore_missing` field in text chunking processors ([#907](https://github.com/opensearch-project/neural-search/pull/907))
* Added rescorer in hybrid query ([#917](https://github.com/opensearch-project/neural-search/pull/917))


### Opensearch Observability


* GettingStarted Fit and Finish ([#2205](https://github.com/opensearch-project/dashboards-observability/pull/2205))
* GettingStarted Rework ([#2194](https://github.com/opensearch-project/dashboards-observability/pull/2194))
* Remove PPL viz & create observability dashboards in MDS environment ([#2194](https://github.com/opensearch-project/dashboards-observability/pull/2195))
* Update workflows to use real build cache ([#2196](https://github.com/opensearch-project/dashboards-observability/pull/2196))
* [Bug] Services Data Picker, UI Fixes ([#2177](https://github.com/opensearch-project/dashboards-observability/pull/2177))
* fit&finish ([#2186](https://github.com/opensearch-project/dashboards-observability/pull/2186))
* [Navigation]Feat: update category to flatten menus in analytics(all) use case ([#2182](https://github.com/opensearch-project/dashboards-observability/pull/2182))
* Update custom traces table with filters (#2178) ([#2178](https://github.com/opensearch-project/dashboards-observability/pull/2178))
* HeaderControl update style, UI Adjustments Integrations ([#2171](https://github.com/opensearch-project/dashboards-observability/pull/2171))


### Opensearch Observability


* [AUTO] Increment version to 2.18.0-SNAPSHOT ([#1866](https://github.com/opensearch-project/observability/pull/1866))


### Opensearch Query Insights


* Support time range parameter to get historical top n queries from local index ([#84](https://github.com/opensearch-project/query-insights/pull/84))
* Refactor query shape field data maps to support the WithFieldName interface ([#111](https://github.com/opensearch-project/query-insights/pull/111))
* Add data models for health stats API ([#120](https://github.com/opensearch-project/query-insights/pull/120))
* Create health\_stats API for query insights ([#122](https://github.com/opensearch-project/query-insights/pull/122))
* Add OpenTelemetry counters for error metrics ([#124](https://github.com/opensearch-project/query-insights/pull/124))
* Add grouping settings for query field name and type ([#135](https://github.com/opensearch-project/query-insights/pull/135))
* Add field type to query shape ([#140](https://github.com/opensearch-project/query-insights/pull/140))
* Adding cache eviction and listener for invalidating index field type mappings on index deletion/update ([#142](https://github.com/opensearch-project/query-insights/pull/142))


### Opensearch Security


* Improve error message when a node with an incorrectly configured certificate attempts to connect ([#4819](https://github.com/opensearch-project/security/pull/4819))
* Support datastreams as an AuditLog Sink ([#4756](https://github.com/opensearch-project/security/pull/4756))
* Auto-convert V6 configuration instances into V7 configuration instances (for OpenSearch 2.x only) ([#4753](https://github.com/opensearch-project/security/pull/4753))
* Add can trip circuit breaker override ([#4779](https://github.com/opensearch-project/security/pull/4779))
* Adding index permissions for remote index in AD ([#4721](https://github.com/opensearch-project/security/pull/4721))
* Fix env var password hashing for PBKDF2 ([#4778](https://github.com/opensearch-project/security/pull/4778))
* Add ensureCustomSerialization to ensure that headers are serialized correctly with multiple transport hops ([#4741](https://github.com/opensearch-project/security/pull/4741))


### Opensearch Security Dashboards Plugin


* Add JWT authentication type to MultipleAuthentication ([#2107](https://github.com/opensearch-project/security-dashboards-plugin/pull/2107))


### Opensearch k-NN


* Introducing a loading layer in FAISS ([#2033](https://github.com/opensearch-project/k-NN/issues/2033))
* Add short circuit if no live docs are in segments ([#2059](https://github.com/opensearch-project/k-NN/pull/2059))
* Optimize reduceToTopK in ResultUtil by removing pre-filling and reducing peek calls ([#2146](https://github.com/opensearch-project/k-NN/pull/2146))
* Update Default Rescore Context based on Dimension ([#2149](https://github.com/opensearch-project/k-NN/pull/2149))
* KNNIterators should support with and without filters ([#2155](https://github.com/opensearch-project/k-NN/pull/2155))
* Adding Support to Enable/Disble Share level Rescoring and Update Oversampling Factor ([#2172](https://github.com/opensearch-project/k-NN/pull/2172))
* Add support to build vector data structures greedily and perform exact search when there are no engine files ([#1942](https://github.com/opensearch-project/k-NN/issues/1942))
* Add CompressionLevel Calculation for PQ ([#2200](https://github.com/opensearch-project/k-NN/pull/2200))
* Remove FSDirectory dependency from native engine constructing side and deprecated FileWatcher ([#2182](https://github.com/opensearch-project/k-NN/pull/2182))
* Update approximate\_threshold to 15K documents ([#2229](https://github.com/opensearch-project/k-NN/pull/2229))
* Update default engine to FAISS ([#2221](https://github.com/opensearch-project/k-NN/pull/2221))


### Opensearch Dashboards Notifications


* [Fit & Finish] Updated Fit and Finish guidelines ([#256](https://github.com/opensearch-project/dashboards-notifications/pull/256))
* Fit and Finish UX Fixes ([#263](https://github.com/opensearch-project/dashboards-notifications/pull/263))
* Fit and Finish UX Fixes Pt 2. ([#270](https://github.com/opensearch-project/dashboards-notifications/pull/270))


## BUG FIXES


### Opensearch Alerting


* Delete query index only if put mappings throws an exception ([#1685](https://github.com/opensearch-project/alerting/pull/1685))
* Optimize bucket level monitor to resolve alias to query only those time-series indices that contain docs within timeframe of range query filter in search input ([#1701](https://github.com/opensearch-project/alerting/pull/1701))
* Fix number of shards of query index to 0 and auto expand replicas to 0-1 ([#1702](https://github.com/opensearch-project/alerting/pull/1702))


### Opensearch Alerting Dashboards Plugin


* Fit and Finish UX Fixes ([#1092](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1092))
* Fit and Finish UX changes Pt 2 ([#1099](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1099))
* Fix assistant plugin override issue and return dataSourceId in context ([#1102](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1102))
* add width for recent alerts card ([#1117](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1117))
* Fix ui\_metadata is not fetched when MDS client is used ([#1124](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1124))


### Opensearch Anomaly Detection


* Bump RCF Version and Fix Default Rules Bug in AnomalyDetector ([#1334](https://github.com/opensearch-project/anomaly-detection/pull/1334))


### Opensearch Anomaly Detection Dashboards


* Fix custom result index session not rendering issue ([#887](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/887))
* Fix issues in running historical analysis and custom result index section ([#889](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/889))
* Fix preview not considering rules and imputation options ([#898](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/898))


### Opensearch Dashboards Maps


* Fix: prevent overlay from overlapping new application header([#680] (https://github.com/opensearch-project/dashboards-maps/pull/680))
* Fix dynamic uses of i18n ([#678](https://github.com/opensearch-project/dashboards-maps/pull/678))


### Opensearch Dashboards Notifications


* Fix typo in recipient ([#287](https://github.com/opensearch-project/dashboards-notifications/pull/287))
* Fix ci ([#271](https://github.com/opensearch-project/dashboards-notifications/pull/271))
* Fix cache cypress ([#280](https://github.com/opensearch-project/dashboards-notifications/pull/280))
* Bug fix to switch to default datasource instead of local cluster when initial loading ([#290](https://github.com/opensearch-project/dashboards-notifications/pull/290))


### Opensearch Dashboards Reporting


* Fix missing imports in report\_settings ([#464](https://github.com/opensearch-project/dashboards-reporting/pull/464))


### Opensearch Dashboards Search Relevance


* Changed path for error handling in APIs ([#459](https://github.com/opensearch-project/dashboards-search-relevance/pull/459))([#461](https://github.com/opensearch-project/dashboards-search-relevance/pull/461))
* Removed default option in MDS selector ([#454](https://github.com/opensearch-project/dashboards-search-relevance/pull/454))([#455](https://github.com/opensearch-project/dashboards-search-relevance/pull/455))


### Opensearch Flow Framework


* Fixed Template Update Location and Improved Logger Statements in ReprovisionWorkflowTransportAction ([#918](https://github.com/opensearch-project/flow-framework/pull/918))


### Opensearch Index Management


* Fixing snapshot bug ([#1257](https://github.com/opensearch-project/index-management/pull/1257))


### Opensearch Index Management Dashboards Plugin


* bug-fix: Create snapshot policy button reloads the dashboard ([#1187](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1187))
* Fixing a bug with initial data source being set to local cluster ([#1189](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1189))


### Opensearch Job Scheduler


* Return lockService from createComponents [(#670)](https://github.com/opensearch-project/job-scheduler/pull/670) [(#672)](https://github.com/opensearch-project/job-scheduler/pull/672).


### Opensearch ML Commons


* Fix ml inference ingest processor always return list using JsonPath ([#2985](https://github.com/opensearch-project/ml-commons/pull/2985))
* Populate time fields for connectors on return ([#2922](https://github.com/opensearch-project/ml-commons/pull/2922))
* Fix for rag processor throwing NPE when optional parameters are not provided ([#3057](https://github.com/opensearch-project/ml-commons/pull/3057))
* Fix PR #2976 bug due to missing adding function_name and algorithm in querying models ([#3104](https://github.com/opensearch-project/ml-commons/pull/3104))
* Gracefully handle error when generative_qa_parameters is not provided ([#3100](https://github.com/opensearch-project/ml-commons/pull/3100))
* Fix error log to show the right agent type ([#2809](https://github.com/opensearch-project/ml-commons/pull/2809))
* Fix model stuck in deploying state during node crash/cluster restart ([#3137](https://github.com/opensearch-project/ml-commons/pull/3137))
* Increase the wait timeout to fetch the master key ([#3151](https://github.com/opensearch-project/ml-commons/pull/3151))
* Handle BWC for bedrock converse API ([#3173](https://github.com/opensearch-project/ml-commons/pull/3173))


### Opensearch ML Commons Dashboards


* Fix category order and description in data administration landing page ([#369](https://github.com/opensearch-project/ml-commons-dashboards/pull/369))


### Opensearch Neural Search


* Fixed incorrect document order for nested aggregations in hybrid query ([#956](https://github.com/opensearch-project/neural-search/pull/956))


### Opensearch Observability


* Fix getting started cards re-direction to integrations ([#2146](https://github.com/opensearch-project/dashboards-observability/pull/2146))
* [MDS][Bug]added changes for de registering plugins not in MDS and changed ([#2222](https://github.com/opensearch-project/dashboards-observability/pull/2222))
* Fixes span to logs redireciton, updates mds label when undefined ([#2225](https://github.com/opensearch-project/dashboards-observability/pull/2222))
* [Workspace] Fix non-workspace admin update observability:defaultDashboard ([#2223](https://github.com/opensearch-project/dashboards-observability/pull/2223))
* [BUG]Re direction fix for associated logs from traces ([#2219](https://github.com/opensearch-project/dashboards-observability/pull/2219))
* [BUG] Metrics fixes ([#2217](https://github.com/opensearch-project/dashboards-observability/pull/2217))
* Observability Overview page rework ([#2210](https://github.com/opensearch-project/dashboards-observability/pull/2210))
* Rotate x-Axis labels by 45 degree counter-wise to avoid common overlapping issue ([#2211](https://github.com/opensearch-project/dashboards-observability/pull/2211))
* Fix for missing else consition ([#2213](https://github.com/opensearch-project/dashboards-observability/pull/2213))
* Fix: Update getting started cards content and visual design ([#2209](https://github.com/opensearch-project/dashboards-observability/pull/2209))
* Update traces span redirection ([#2201](https://github.com/opensearch-project/dashboards-observability/pull/2201))
* [Bug Fix] Fix the VPC integration's MV creation query ([#22179](https://github.com/opensearch-project/dashboards-observability/pull/2201))


### Opensearch Query Insights


* Refactor parsing logic for Measurement ([#112](https://github.com/opensearch-project/query-insights/pull/112))


### Opensearch Query Workbench


* Fix workbench routes to support modal mounting ([#401](https://github.com/opensearch-project/dashboards-query-workbench/pull/401))


* [Bug] Added error handling for api calls ([#408](https://github.com/opensearch-project/dashboards-query-workbench/pull/408))


### Opensearch Security


* Handle non-flat yaml settings for demo configuration detection ([#4798](https://github.com/opensearch-project/security/pull/4798))
* Fix bug where admin can read system index ([#4775](https://github.com/opensearch-project/security/pull/4775))
* Ensure that dual mode enabled flag from cluster settings can get propagated to core ([#4830](https://github.com/opensearch-project/security/pull/4830))
* Remove failed login attempt for saml authenticator ([#4770](https://github.com/opensearch-project/security/pull/4770))
* Fix issue in HashingStoredFieldVisitor with stored fields ([#4827](https://github.com/opensearch-project/security/pull/4827))
* Fix issue with Get mappings on a Closed index ([#4777](https://github.com/opensearch-project/security/pull/4777))
* Changing comments permission for alerting\_ack\_alerts role ([#4723](https://github.com/opensearch-project/security/pull/4723))
* Fixed use of rolesMappingConfiguration in InternalUsersApiActionValidationTest ([#4754](https://github.com/opensearch-project/security/pull/4754))
* Use evaluateSslExceptionHandler() when constructing OpenSearchSecureSettingsFactory ([#4726](https://github.com/opensearch-project/security/pull/4726))


### Opensearch Security Analytics


* Remove redundant logic to fix OS launch exception and updates actions/upload-artifac2 to @V3 ([#1303](https://github.com/opensearch-project/security-analytics/pull/1303))
* Add null check while adding fetched iocs into per-indicator-type map ([#1335](https://github.com/opensearch-project/security-analytics/pull/1335))
* Fix notifications listener leak in threat intel monitor ([#1361](https://github.com/opensearch-project/security-analytics/pull/1361))
* [Bug] Fixed ListIOCs number of findings cap. ([#1373](https://github.com/opensearch-project/security-analytics/pull/1373))
* [Bug] Add exists check for IOCs index. ([#1392](https://github.com/opensearch-project/security-analytics/pull/1392))


### Opensearch Security Analytics Dashboards


* Fix findings page crash and rule severity correctness ([#1160](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1160))
* Bug fixes for threat intel, duplicate findings, and breadcrumbs path ([#1176](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1176))
* Edit correlation Alert Trigger fix ([#1180](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1180))
* Avoid showing unuseful error toast when ds is not yet selected ([1186](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1186))
* Fix: Update getting started cards content and visual design ([#1188](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1188))
* Fix: data source picker remount multiple times ([#1192](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1192))
* Testing default ds switch changes ([#1199](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1199))
* Make dataSource default cluster for threat alerts card ([#1200](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1200))


### Opensearch Security Dashboards Plugin


* Update category label for security plugin ([#2121](https://github.com/opensearch-project/security-dashboards-plugin/pull/2121))
* Fix button label ([#2130](https://github.com/opensearch-project/security-dashboards-plugin/pull/2130))


### Opensearch k-NN


* Add DocValuesProducers for releasing memory when close index ([#1946](https://github.com/opensearch-project/k-NN/pull/1946))
* KNN80DocValues should only be considered for BinaryDocValues fields ([#2147](https://github.com/opensearch-project/k-NN/pull/2147))
* Score Fix for Binary Quantized Vector and Setting Default value in case of shard level rescoring is disabled for oversampling factor ([#2183](https://github.com/opensearch-project/k-NN/pull/2183))
* Java Docs Fix For 2.x ([#2190](https://github.com/opensearch-project/k-NN/pull/2190))


### OpenSearch SQL


* Improve error handling for some more edge cases ([#3112](https://github.com/opensearch-project/sql/pull/3112))
* Resolve Alias Issues in Legacy SQL with Filters ([#3109](https://github.com/opensearch-project/sql/pull/3109))
* Bug Fixes for minor issues with SQL PIT refactor ([#3108](https://github.com/opensearch-project/sql/pull/3108))
* Correct regular expression range ([#3107](https://github.com/opensearch-project/sql/pull/3107))
* SQL pagination should work with the `pretty` parameter ([#3106](https://github.com/opensearch-project/sql/pull/3106))
* Improve error handling for malformed query cursors ([#3084](https://github.com/opensearch-project/sql/pull/3084))
* Remove scheduler index from SystemIndexDescriptor ([#3097](https://github.com/opensearch-project/sql/pull/3097))


## INFRASTRUCTURE


### Opensearch Anomaly Detection


* Forward port flaky test fix and add forecasting security tests ([#1329](https://github.com/opensearch-project/anomaly-detection/pull/1329))
* Updating several dependencies ([#1337](https://github.com/opensearch-project/anomaly-detection/pull/1337))


### Opensearch ML Commons


* Support index.auto_expand_replicas 0-all for .plugins-ml-config ([#3017](https://github.com/opensearch-project/ml-commons/pull/3017))
* Add Test Env Require Approval Action ([#3005](https://github.com/opensearch-project/ml-commons/pull/3005))
* Upgrading upload artifact to v4 ([#3162](https://github.com/opensearch-project/ml-commons/pull/3162))
* Bump actions/download-artifact from 3 to 4.1.7 in /.github/workflows ([#2881](https://github.com/opensearch-project/ml-commons/pull/2881))


### Opensearch Query Insights


* Upgrade deprecated actions/upload-artifact versions to v3 ([#117](https://github.com/opensearch-project/query-insights/pull/117))


## DOCUMENTATION


### Opensearch Alerting


* Added 2.18.0 release notes. ([#1718](https://github.com/opensearch-project/alerting/pull/1718))


### Opensearch Alerting Dashboards Plugin


* Added 2.18.0 release notes. ([#1132](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1132))


### Opensearch Common Utils


* Added 2.18.0.0 release notes. ([#750](https://github.com/opensearch-project/common-utils/pull/750))


### Opensearch Dashboards Notifications


* Added 2.18.0 release notes. ([#293](https://github.com/opensearch-project/dashboards-notifications/pull/293))


### Opensearch Flow Framework


* Add query assist data summary agent into sample templates ([#875](https://github.com/opensearch-project/flow-framework/pull/875))


### Opensearch ML Commons


* Add tutorial for cross-account model invocation on amazon managed cluster ([#3064](https://github.com/opensearch-project/ml-commons/pull/3064))
* Support role temporary credential in connector tutorial ([#3058](https://github.com/opensearch-project/ml-commons/pull/3058))
* Connector blueprint for amazon bedrock converse ([#2960](https://github.com/opensearch-project/ml-commons/pull/2960))
* Updates dev guide to inform the workflow approval step ([#3062](https://github.com/opensearch-project/ml-commons/pull/3062))
* Tune titan embedding model blueprint for v2 ([#3094](https://github.com/opensearch-project/ml-commons/pull/3094))
* Add bedrock multimodal build-in function usage example in doc ([#3073](https://github.com/opensearch-project/ml-commons/pull/3073))


### Opensearch Notifications


* Add 2.18.0 release notes ([#980](https://github.com/opensearch-project/notifications/pull/980))


### Opensearch Query Insights


* Add document for Query Insights health\_stats API and error counter metrics ([#8627](https://github.com/opensearch-project/documentation-website/pull/8627))
* Added 2.18 release notes ([#148](https://github.com/opensearch-project/query-insights/pull/))


### Opensearch Security Analytics


* Added 2.18.0 release notes. ([#1399](https://github.com/opensearch-project/security-analytics/pull/1399))


### Opensearch Security Analytics Dashboards


* Added 2.18.0 release notes. ([#1205](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1205))


### Opensearch k-NN


* Fix sed command in DEVELOPER\_GUIDE.md to append a new line character '\n'. ([#2181](https://github.com/opensearch-project/k-NN/pull/2181))


## MAINTENANCE


### OpenSearch Dashboards Assistant


* Increment version to 2.18.0.0([#315](https://github.com/opensearch-project/dashboards-assistant/pull/315))


### Opensearch Alerting


* Increment version to 2.18.0-SNAPSHOT. ([#1653](https://github.com/opensearch-project/alerting/pull/1653))


### Opensearch Alerting Dashboards Plugin


* Increment version to 2.18.0.0 ([#1098](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1098))


### Opensearch Anomaly Detection Dashboards


* [AUTO] Increment version to 2.18.0.0 ([#877](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/877))


### Opensearch Asynchronous Search


* Increment version to 2.18.0 ([#615](https://github.com/opensearch-project/asynchronous-search/pull/615))


### Opensearch Common Utils


* Increment version to 2.18.0-SNAPSHOT ([#729](https://github.com/opensearch-project/common-utils/pull/729))
* Update Gradle to 8.10.2 ([#746](https://github.com/opensearch-project/common-utils/pull/746))


### Opensearch Dashboards Notifications


* Increment version to 2.17.0.0 ([#278](https://github.com/opensearch-project/dashboards-notifications/pull/278))
* Upgrade to v4 ([#264](https://github.com/opensearch-project/dashboards-notifications/pull/264))


### Opensearch Dashboards Reporting


* [CVE] Bump dompurify to 3.0.11 ([#462](https://github.com/opensearch-project/dashboards-reporting/pull/462))


### Opensearch Dashboards Search Relevance


* Bumping actions/upload-artifact ([#450](https://github.com/opensearch-project/dashboards-search-relevance/pull/450))([#452](https://github.com/opensearch-project/dashboards-search-relevance/pull/452))
* Increment version to 2.18.0.0([#445](https://github.com/opensearch-project/dashboards-search-relevance/pull/445))
* Update to latest svg ([#449](https://github.com/opensearch-project/dashboards-search-relevance/pull/449)) ([#453](https://github.com/opensearch-project/dashboards-search-relevance/pull/453))


### Opensearch Dashboards Visualizations


* Increment version to 2.18.0.0 ([#396](https://github.com/opensearch-project/dashboards-visualizations/pull/396))


* Adding release notes for 2.18.0 ([#398](https://github.com/opensearch-project/dashboards-visualizations/pull/398))


### Opensearch Index Management


* Increment version to 2.18.0-SNAPSHOT ([#1241](https://github.com/opensearch-project/index-management/pull/1241))
* Upgrade upload-artifact to version 3 ([#1252](https://github.com/opensearch-project/index-management/pull/1252))
* Bump bwc version after 2.17 release ([#1259](https://github.com/opensearch-project/index-management/pull/1259))
* Move non-active maintainer to emeritus ([#1263](https://github.com/opensearch-project/index-management/pull/1263))
* Update CI check for integ-test-with-security to run all integ tests with security ([#1243](https://github.com/opensearch-project/index-management/pull/1243))
* Remove 2 instances wildcard imports ([#1251](https://github.com/opensearch-project/index-management/pull/1251))
* Updating baseline JDK version to JDK-21 ([#1276](https://github.com/opensearch-project/index-management/pull/1276))


### Opensearch Index Management Dashboards Plugin


* Increment version to 2.18.0.0 ([#1180](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1180))


### Opensearch Job Scheduler


* Increment version to 2.18.0 [#676](https://github.com/opensearch-project/job-scheduler/pull/676).
* Dependabot: bump org.gradle.test-retry from 1.5.10 to 1.6.0 [(#679)](https://github.com/opensearch-project/job-scheduler/pull/679) [(#681)](https://github.com/opensearch-project/job-scheduler/pull/681).
* Dependabot: bump com.google.googlejavaformat:google-java-format [(#684)](https://github.com/opensearch-project/job-scheduler/pull/684) [(#685)](https://github.com/opensearch-project/job-scheduler/pull/685).
* Gradle upgrade to 8.10.2 and run CI checks with JDK 23 [(#688)](https://github.com/opensearch-project/job-scheduler/pull/688) [(#689)](https://github.com/opensearch-project/job-scheduler/pull/689).


### Opensearch ML Commons


* Bump protobuf version to 3.25.5 to patch potential DOS ([#3083](https://github.com/opensearch-project/ml-commons/pull/3083))
* Removing api keys from the integ test log ([#3112](https://github.com/opensearch-project/ml-commons/pull/3112))
* Allowing backport prs to skip approval ([#3132](https://github.com/opensearch-project/ml-commons/pull/3132))
* Updating the approval requirement ([#3148](https://github.com/opensearch-project/ml-commons/pull/3148))
* Unblocking the integ test pipeline for release ([#3159](https://github.com/opensearch-project/ml-commons/pull/3159))


### Opensearch ML Commons Dashboards


* Increment version to 2.18.0.0 ([#370](https://github.com/opensearch-project/ml-commons-dashboards/pull/370))


### Opensearch Notifications


* Increment version to 2.18.0-SNAPSHOT ([#957](https://github.com/opensearch-project/notifications/pull/957))
* Updated workflows to fix CIs ([#965](https://github.com/opensearch-project/notifications/pull/965))


### Opensearch Observability


* [CVE] Bump the lint-staged from 13.1.0 to 15.2.10 ([#2138](https://github.com/opensearch-project/dashboards-observability/pull/2138))
* Add compile step before Cypress runs in CI ([#2187](https://github.com/opensearch-project/dashboards-observability/pull/2187))


### Opensearch Query Insights


* Enhanced security based integration tests ([#113](https://github.com/opensearch-project/query-insights/pull/113))
* Set default true for field name and type setting ([#144](https://github.com/opensearch-project/query-insights/pull/144))


### Opensearch Reporting


* Increment version to 2.18.0-SNAPSHOT ([#1037](https://github.com/opensearch-project/reporting/pull/1037))


### Opensearch Security


* Bump gradle to 8.10.2 ([#4829](https://github.com/opensearch-project/security/pull/4829))
* Bump ch.qos.logback:logback-classic from 1.5.8 to 1.5.11 ([#4807](https://github.com/opensearch-project/security/pull/4807)) ([#4825](https://github.com/opensearch-project/security/pull/4825))
* Bump org.passay:passay from 1.6.5 to 1.6.6 ([#4824](https://github.com/opensearch-project/security/pull/4824))
* Bump org.junit.jupiter:junit-jupiter from 5.11.0 to 5.11.2 ([#4767](https://github.com/opensearch-project/security/pull/4767)) ([#4811](https://github.com/opensearch-project/security/pull/4811))
* Bump io.dropwizard.metrics:metrics-core from 4.2.27 to 4.2.28 ([#4789](https://github.com/opensearch-project/security/pull/4789))
* Bump com.nimbusds:nimbus-jose-jwt from 9.40 to 9.41.2 ([#4737](https://github.com/opensearch-project/security/pull/4737)) ([#4787](https://github.com/opensearch-project/security/pull/4787))
* Bump org.ow2.asm:asm from 9.7 to 9.7.1 ([#4788](https://github.com/opensearch-project/security/pull/4788))
* Bump com.google.googlejavaformat:google-java-format from 1.23.0 to 1.24.0 ([#4786](https://github.com/opensearch-project/security/pull/4786))
* Bump org.xerial.snappy:snappy-java from 1.1.10.6 to 1.1.10.7 ([#4738](https://github.com/opensearch-project/security/pull/4738))
* Bump org.gradle.test-retry from 1.5.10 to 1.6.0 ([#4736](https://github.com/opensearch-project/security/pull/4736))
* Moves @cliu123 to emeritus status ([#4667](https://github.com/opensearch-project/security/pull/4667))
* Add Derek Ho (github: derek-ho) as a maintainer ([#4796](https://github.com/opensearch-project/security/pull/4796))
* Add deprecation warning for GET/POST/PUT cache ([#4776](https://github.com/opensearch-project/security/pull/4776))
* Fix for: CVE-2024-47554 ([#4792](https://github.com/opensearch-project/security/pull/4792))
* Move Stephen to emeritus ([#4804](https://github.com/opensearch-project/security/pull/4804))
* Undeprecate securityadmin script ([#4768](https://github.com/opensearch-project/security/pull/4768))
* Bump commons-io:commons-io from 2.16.1 to 2.17.0 ([#4750](https://github.com/opensearch-project/security/pull/4750))
* Bump org.scala-lang:scala-library from 2.13.14 to 2.13.15 ([#4749](https://github.com/opensearch-project/security/pull/4749))
* org.checkerframework:checker-qual and ch.qos.logback:logback-classic to new versions ([#4717](https://github.com/opensearch-project/security/pull/4717))
* Add isActionPaginated to DelegatingRestHandler ([#4765](https://github.com/opensearch-project/security/pull/4765))
* Refactor ASN1 call ([#4740](https://github.com/opensearch-project/security/pull/4740))
* Fix 'integTest' not called with test workflows during release ([#4815](https://github.com/opensearch-project/security/pull/4815))
* Fixed bulk index requests in BWC tests and hardened assertions ([#4831](https://github.com/opensearch-project/security/pull/4831))


### Opensearch Security Analytics


* Incremented version to 2.18.0 ([#1314](https://github.com/opensearch-project/security-analytics/pull/1314))
* Update to lucene 9.12 ([#1349](https://github.com/opensearch-project/security-analytics/pull/1349))


### Opensearch Security Analytics Dashboards


* Increment version to 2.18.0.0 ([#1163](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1163))
* Upgrade github workflow upload artifact to v4 ([#1167](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1167))


### Opensearch Skills


* Fix test failure due to external change ([#427](https://github.com/opensearch-project/skills/pull/427))
* Fix(deps): update dependency net.bytebuddy:byte-buddy-agent to v1.15.4 ([#279](https://github.com/opensearch-project/skills/pull/279))
* Fix(deps): update dependency net.bytebuddy:byte-buddy to v1.15.4 ([#43](https://github.com/opensearch-project/skills/pull/43))
* Fix(deps): update junit5 monorepo to v5.11.2 ([#363](https://github.com/opensearch-project/skills/pull/363))
* Chore(deps): update dependency gradle to v8.10.2 ([#432](https://github.com/opensearch-project/skills/pull/432))
* Chore(deps): update plugin io.freefair.lombok to v8.10.2 ([#434](https://github.com/opensearch-project/skills/pull/434))
* Fix(deps): update mockito monorepo to v5.14.2 ([#437](https://github.com/opensearch-project/skills/pull/437))


### Opensearch k-NN


* Remove benchmarks folder from k-NN repo ([#2127](https://github.com/opensearch-project/k-NN/pull/2127))
* Fix lucene codec after lucene version bumped to 9.12. ([#2195](https://github.com/opensearch-project/k-NN/pull/2195))


### OpenSearch SQL


* Bump commons-io to 2.14.0 ([#3091](https://github.com/opensearch-project/sql/pull/3091))
* Fix tests on 2.18 ([#3113](https://github.com/opensearch-project/sql/pull/3113))


## REFACTORING


### Opensearch Alerting


* Adding Alerting Comments system indices and Security ITs ([#1659](https://github.com/opensearch-project/alerting/pull/1659))
* Add logging for remote monitor execution flows ([#1663](https://github.com/opensearch-project/alerting/pull/1663))
* Separate doc-level monitor query indices for externally defined monitors ([#1664](https://github.com/opensearch-project/alerting/pull/1664))
* Move deletion of query index before its creation ([#1668](https://github.com/opensearch-project/alerting/pull/1668))
* Create query index at the time of monitor creation ([#1674](https://github.com/opensearch-project/alerting/pull/1674))


### Opensearch Flow Framework


* Update workflow state without using painless script ([#894](https://github.com/opensearch-project/flow-framework/pull/894))


### Opensearch Security Analytics


* Separate doc-level monitor query indices created by detectors ([#1324](https://github.com/opensearch-project/security-analytics/pull/1324))
* Update number of replicas of system indices to 1-20 and number of primary shards for system indices to 1 ([#1358](https://github.com/opensearch-project/security-analytics/pull/1358))
* Update min number of replicas to 0 ([#1364](https://github.com/opensearch-project/security-analytics/pull/1364))
* Updated dedicated query index settings to true ([#1365](https://github.com/opensearch-project/security-analytics/pull/1365))
* Set the refresh policy to IMMEDIATE when updating correlation alerts ([#1382](https://github.com/opensearch-project/security-analytics/pull/1382))


### Opensearch k-NN


* Does not create additional KNNVectorValues in NativeEngines990KNNVectorWriter when quantization is not needed ([#2133](https://github.com/opensearch-project/k-NN/pull/2133))
* Minor refactoring and refactored some unit test ([#2167](https://github.com/opensearch-project/k-NN/pull/2167))
