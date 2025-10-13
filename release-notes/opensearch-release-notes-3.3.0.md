# OpenSearch and OpenSearch Dashboards 3.3.0 Release Notes


## FEATURES


### Opensearch Alerting


* Adds support for leveraging user custom attributes in Alerting monitors ([#1917](https://github.com/opensearch-project/alerting/pull/1917))


### Opensearch Anomaly Detection


* Add frequency scheduling in real time ([#1562](https://github.com/opensearch-project/anomaly-detection/pull/1562))
* Adding AD suggest API ([#1563](https://github.com/opensearch-project/anomaly-detection/pull/1563))


### Opensearch Anomaly Detection Dashboards Plugin


* Add Suggest parameters button + move operational settings to Configure Model ([#1098](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1098))


### Opensearch Dashboards Flow Framework


* Support agentic search ([#775](https://github.com/opensearch-project/dashboards-flow-framework/pull/775))


### Opensearch Dashboards Search Relevance


* Support semantic highlighting and dynamic image sizing ([#627](https://github.com/opensearch-project/dashboards-search-relevance/pull/627))


### Opensearch Index Management


* Add support in SM Plugin to delete snapshots created manually ([#1452](https://github.com/opensearch-project/index-management/pull/1452))


### Opensearch Job Scheduler


* Job History Service ([#814](https://github.com/opensearch-project/job-scheduler/pull/814))
* Create guice module to bind LockService interface from SPI to LockServiceImpl ([#833](https://github.com/opensearch-project/job-scheduler/pull/833))


### Opensearch K Nn


* Support native Maximal Marginal Relevance ([#2868](https://github.com/opensearch-project/k-NN/pull/2868))
* Support lateInteraction feature using painess script ([#2909](https://github.com/opensearch-project/k-NN/pull/2909))


### Opensearch ML Common


* Add WriteToScratchPad and ReadFromScratchPad tools ([#4192](https://github.com/opensearch-project/ml-commons/pull/4192))
* Add global resource support ([#4003](https://github.com/opensearch-project/ml-commons/pull/4003))
* Add ml-commons passthrough post process function ([#4111](https://github.com/opensearch-project/ml-commons/pull/4111))
* Add output transformation support with mean pooling for ML inference processors ([#4236](https://github.com/opensearch-project/ml-commons/pull/4236))
* Adding query planning tool search template validation and integration tests ([#4177](https://github.com/opensearch-project/ml-commons/pull/4177))
* Onboards to centralized resource access control mechanism for ml-model-group ([#3715](https://github.com/opensearch-project/ml-commons/pull/3715))
* Refactor Agentic Memory ([#4218](https://github.com/opensearch-project/ml-commons/pull/4218))
* Search Template Support for QueryPlanningTool ([#4154](https://github.com/opensearch-project/ml-commons/pull/4154))
* [Agentic Search] Support Query Planner Tool with Conversational Agent ([#4203](https://github.com/opensearch-project/ml-commons/pull/4203))
* [FEATURE] Add Index Insight Feature ([#4088](https://github.com/opensearch-project/ml-commons/pull/4088))
* [FEATURE] Agent Execute Stream ([#4212](https://github.com/opensearch-project/ml-commons/pull/4212))
* [FEATURE] Predict Stream ([#4187](https://github.com/opensearch-project/ml-commons/pull/4187))
* [MCP Connector] MCP Connectors for streamable HTTP ([#4169](https://github.com/opensearch-project/ml-commons/pull/4169))
* Add processor chain and add support for model and tool ([#4093](https://github.com/opensearch-project/ml-commons/pull/4093))
* Add create session API; add message id to working memory; fix update api ([#4246](https://github.com/opensearch-project/ml-commons/pull/4246))


### Opensearch Neural Search


* [SEISMIC] Support SEISMIC, a new sparse ANN algorithm ([#1581](https://github.com/opensearch-project/neural-search/pull/1581), [#1578](https://github.com/opensearch-project/neural-search/pull/1578), [#1577](https://github.com/opensearch-project/neural-search/pull/1577), [#1566](https://github.com/opensearch-project/neural-search/pull/1566), [#1565](https://github.com/opensearch-project/neural-search/pull/1565), [#1564](https://github.com/opensearch-project/neural-search/pull/1564), [#1563](https://github.com/opensearch-project/neural-search/pull/1563), [#1562](https://github.com/opensearch-project/neural-search/pull/1562), [#1559](https://github.com/opensearch-project/neural-search/pull/1559), [#1557](https://github.com/opensearch-project/neural-search/pull/1557), [#1555](https://github.com/opensearch-project/neural-search/pull/1555), [#1554](https://github.com/opensearch-project/neural-search/pull/1554), [#1553](https://github.com/opensearch-project/neural-search/pull/1553), [#1539](https://github.com/opensearch-project/neural-search/pull/1539), [#1538](https://github.com/opensearch-project/neural-search/pull/1538), [#1537](https://github.com/opensearch-project/neural-search/pull/1537), [#1536](https://github.com/opensearch-project/neural-search/pull/1536), [#1524](https://github.com/opensearch-project/neural-search/pull/1524), [#1514](https://github.com/opensearch-project/neural-search/pull/1514), [#1502](https://github.com/opensearch-project/neural-search/pull/1502))
* Support native MMR for neural query ([#1567](https://github.com/opensearch-project/neural-search/pull/1567))


### Opensearch Opensearch Remote Metadata Sdk


* Add global resource support ([#224](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/224))


### Opensearch Query Insights


* Add Workload Management (WLM) Group Filtering for Live Queries API ([#389](https://github.com/opensearch-project/query-insights/pull/389))


### Opensearch Query Insights Dashboards


* Enhance User Experience with Bi-Directional Navigation Between WLM and Live Queries ([#299](https://github.com/opensearch-project/query-insights-dashboards/pull/299))
* Add navigation for query insights and WLM dashboards ([#330](https://github.com/opensearch-project/query-insights-dashboards/pull/330))
* Add feature flag for wlm ([#348](https://github.com/opensearch-project/query-insights-dashboards/pull/348))
* MDS support for WLM ([#352](https://github.com/opensearch-project/query-insights-dashboards/pull/352))


### Opensearch Security


* [Rule-based Autotagging] Add logic to extract security attributes for rule-based autotagging ([#5606](https://github.com/opensearch-project/security/pull/5606))


### Opensearch Security Dashboards Plugin


* [Resource Sharing] Adds resource access management dashboard ([#2304](https://github.com/opensearch-project/security-dashboards-plugin/pull/2304))


### Opensearch Skills


* Log patterns analysis tool ([#625](https://github.com/opensearch-project/skills/pull/625))
* Data Distribution Tool ([#634](https://github.com/opensearch-project/skills/pull/634))


### SQL


* Change the default search sort tiebreaker to `_shard_doc` for PIT search ([#4378](https://github.com/opensearch-project/sql/pull/4378))
* Support direct query data sources ([#4375](https://github.com/opensearch-project/sql/pull/4375))
* Enable Calcite by default and implicit fallback the unsupported commands ([#4372](https://github.com/opensearch-project/sql/pull/4372))
* Enhance the cost computing mechanism and push down context ([#4353](https://github.com/opensearch-project/sql/pull/4353))
* Add error handling for known limitation of sql `JOIN` ([#4344](https://github.com/opensearch-project/sql/pull/4344))
* Optimize count aggregation performance by utilizing native doc\_count in v3 ([#4337](https://github.com/opensearch-project/sql/pull/4337))
* Date/Time based Span aggregation should always not present null bucket ([#4327](https://github.com/opensearch-project/sql/pull/4327))
* Add non-numeric field support for max/min functions ([#4281](https://github.com/opensearch-project/sql/pull/4281))
* Push down project operator with non-identity projections into scan ([#4279](https://github.com/opensearch-project/sql/pull/4279))
* Add `values` stats function with UDAF ([#4276](https://github.com/opensearch-project/sql/pull/4276))
* Support ISO8601-formatted string in PPL ([#4246](https://github.com/opensearch-project/sql/pull/4246))
* Push down limit operator into aggregation bucket size ([#4228](https://github.com/opensearch-project/sql/pull/4228))
* Support time modifiers in search command ([#4224](https://github.com/opensearch-project/sql/pull/4224))
* Support first/last aggregate functions for PPL ([#4223](https://github.com/opensearch-project/sql/pull/4223))
* `mvjoin` support in PPL Caclite ([#4217](https://github.com/opensearch-project/sql/pull/4217))
* Enable pushdown optimization for filtered aggregation ([#4213](https://github.com/opensearch-project/sql/pull/4213))
* Pushdown earliest/latest aggregate functions ([#4166](https://github.com/opensearch-project/sql/pull/4166))
* Add support for `list()` multi-value stats function ([#4161](https://github.com/opensearch-project/sql/pull/4161))
* [Enhancement] Enhance patterns command with additional sample\_logs output field ([#4155](https://github.com/opensearch-project/sql/pull/4155))
* Search command revamp. ([#4152](https://github.com/opensearch-project/sql/pull/4152))
* Add shortcut for count() ([#4142](https://github.com/opensearch-project/sql/pull/4142))
* Starter implementation for `spath` command ([#4120](https://github.com/opensearch-project/sql/pull/4120))
* strftime function implementation ([#4106](https://github.com/opensearch-project/sql/pull/4106))
* Add regex\_match function for PPL with Calcite engine support ([#4092](https://github.com/opensearch-project/sql/pull/4092))
* Support distinct\_count/dc in eventstats ([#4084](https://github.com/opensearch-project/sql/pull/4084))
* Add wildcard support for rename command ([#4019](https://github.com/opensearch-project/sql/pull/4019))
* Support timechart command with Calcite ([#3993](https://github.com/opensearch-project/sql/pull/3993))
* SUM aggregation enhancement on operations with literal ([#3971](https://github.com/opensearch-project/sql/pull/3971))
* Support join field list and join options ([#3803](https://github.com/opensearch-project/sql/pull/3803))
* Speed up aggregation pushdown for single group-by expression ([#3550](https://github.com/opensearch-project/sql/pull/3550))
* Add max/min eval functions ([#4333](https://github.com/opensearch-project/sql/pull/4333))
* Implementation of mode `sed` and `offset_field` in rex PPL command ([#4241](https://github.com/opensearch-project/sql/pull/4241))
* Add earliest/latest aggregate function for eventstats PPL command ([#4212](https://github.com/opensearch-project/sql/pull/4212))
* Core Implementation of `rex` Command In PPL ([#4109](https://github.com/opensearch-project/sql/pull/4109))
* Implementation of `regex` Command In PPL ([#4083](https://github.com/opensearch-project/sql/pull/4083))


## ENHANCEMENTS


### Opensearch Common Utils


* Update user attributes XContent parsing logic ([#878](https://github.com/opensearch-project/common-utils/pull/878))


### Opensearch Dashboards Search Relevance


* Improve color coding ([#632](https://github.com/opensearch-project/dashboards-search-relevance/pull/632))
* Allow more than 10 results for a query in pairwise comparison.([#637](https://github.com/opensearch-project/dashboards-search-relevance/pull/637))


### Opensearch Index Management


* Using Scripted Avg Class in AvgAggregationBuilder in place of double ([#1460](https://github.com/opensearch-project/index-management/pull/1460))
* Do not include global state in snapshot step ([#1480](https://github.com/opensearch-project/index-management/pull/1480))


### Opensearch Job Scheduler


* Make LockService an interface and replace usages of ThreadContext.stashContext ([#714](https://github.com/opensearch-project/job-scheduler/pull/714))
* Introduce a configurable remote metadata client AND migrate LockService to the client ([#831](https://github.com/opensearch-project/job-scheduler/pull/831))


### Opensearch K Nn


* Added engine as a top-level optional parameter while creating vector field ([#2736](https://github.com/opensearch-project/k-NN/pull/2736))
* Migrate k-NN plugin to use GRPC transport-grpc SPI interface ([#2833](https://github.com/opensearch-project/k-NN/pull/2833))


### Opensearch ML Common


* Add Get Agent to ML Client ([#4180](https://github.com/opensearch-project/ml-commons/pull/4180))
* Parameter Passing for Predict via Remote Connector ([#4121](https://github.com/opensearch-project/ml-commons/pull/4121))
* Support multi-tenancy for LocalRegexGuardrail ([#4120](https://github.com/opensearch-project/ml-commons/pull/4120))
* [MCP Server] Support Streamable HTTP and deprecate SSE in MCP server ([#4162](https://github.com/opensearch-project/ml-commons/pull/4162))
* [Memory] Add updated time to message ([#4201](https://github.com/opensearch-project/ml-commons/pull/4201))
* [Metrics] Introduce agent metrics & Add is\_hidden tag for model metrics ([#4221](https://github.com/opensearch-project/ml-commons/pull/4221))
* Update interaction with failure message on agent execution failure ([#4198](https://github.com/opensearch-project/ml-commons/pull/4198))
* Add PlainNumberAdapter and corresponding tests for Gson in SearchIndexTool ([#4133](https://github.com/opensearch-project/ml-commons/pull/4133))
* Move HttpClientFactory to common to expose to other components ([#4175](https://github.com/opensearch-project/ml-commons/pull/4175))
* Change the setting name to same naming convention with others ([#4215](https://github.com/opensearch-project/ml-commons/pull/4215))
* Enabling agentic memory feature by default as we are going GA ([#4240](https://github.com/opensearch-project/ml-commons/pull/4240))
* Add parameter to control delete memories when delete container ([#4238](https://github.com/opensearch-project/ml-commons/pull/4238))
* Refactor and add more validation to processor chain ([#4260](https://github.com/opensearch-project/ml-commons/pull/4260))
* [Agentic Search] Use same model for Agent and QPT ([#4262](https://github.com/opensearch-project/ml-commons/pull/4262))
* Improve semantic fact extraction prompt and add JSON enforcement ([#4282](https://github.com/opensearch-project/ml-commons/pull/4282))
* Improve user preference extraction prompt with XML-based structure ([#4288](https://github.com/opensearch-project/ml-commons/pull/4288))
* Enable execute tool feature flag by default ([#4296](https://github.com/opensearch-project/ml-commons/pull/4296))


### Opensearch Neural Search


* [Semantic Field] Support the sparse two phase processor for the semantic field
* [Stats] Add stats for agentic query and agentic query translator processor
* [Agentic Search] Adds validations and logging for agentic query
* [Performance Improvement] Introduce QueryCollectContextSpec in Hybrid Query to improve search performance
* [Agentic Search] Add support for conversational agent
* [Agentic Search] Add support for agent summary and memory id for conversational agent
* [Semantic Highlighting] Add semantic highlighting response processor with batch inference support ([#1520](https://github.com/opensearch-project/neural-search/pull/1520))


### Opensearch Opensearch Remote Metadata Sdk


* Add SeqNo and PrimaryTerm support to Put and Delete requests ([#234](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/234))


* Add RefreshPolicy and timeout support to Put, Update, Delete, and Bulk requests ([#244](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/244))


### Opensearch Performance Analyzer


* Use Subclass method for Versiona and Channel type which is understood… ([#845](https://github.com/opensearch-project/performance-analyzer/pull/845))


### Opensearch Query Insights Dashboards


* Added version decoupling for wlm dashboard ([#361](https://github.com/opensearch-project/query-insights-dashboards/pull/361))
* Version decouple unit test ([#363](https://github.com/opensearch-project/query-insights-dashboards/pull/363))


### Opensearch Security


* [Resource Sharing] Use DLS to automatically filter sharable resources for authenticated user based on `all_shared_principals` ([#5600](https://github.com/opensearch-project/security/pull/5600))
* [Resource Sharing] Keep track of list of principals for which sharable resource is visible for searching ([#5596](https://github.com/opensearch-project/security/pull/5596))
* [Resource Sharing] Keep track of tenant for sharable resources by persisting user requested tenant with sharing info ([#5588](https://github.com/opensearch-project/security/pull/5588))
* [SecurityPlugin Health Check] Add AuthZ initialization completion check in health check API ([#5626](https://github.com/opensearch-project/security/pull/5626))
* [Resource Sharing] Adds API to provide dashboards support for resource access management ([#5597](https://github.com/opensearch-project/security/pull/5597))
* Direct JWKS (JSON Web Key Set) support in the JWT authentication backend ([#5578](https://github.com/opensearch-project/security/pull/5578))
* Adds a list setting to explicitly specify resources to be protected ([#5671](https://github.com/opensearch-project/security/pull/5671))
* Make configuration setting for user custom attribute serialization dynamic ([#5657](https://github.com/opensearch-project/security/pull/5657))


### Opensearch Security Analytics


* Move rules to config directory from classpath resources ([#1580](https://github.com/opensearch-project/security-analytics/pull/1580))


### Opensearch Security Dashboards Plugin


* Add experimental direct query permissions ([#2315](https://github.com/opensearch-project/security-dashboards-plugin/pull/2315))


### Opensearch Skills


* Add more information in ppl tool when passing to sagemaker ([#636](https://github.com/opensearch-project/skills/pull/636))


## BUG FIXES


### Opensearch Alerting


* Update System.env syntax for Gradle 9 compatibility ([#1920](https://github.com/opensearch-project/alerting/pull/1920))


### Opensearch Anomaly Detection


* Make frequency optional; fix STOPPED state; add ecommerce tests ([#1565](https://github.com/opensearch-project/anomaly-detection/pull/1565))


### Opensearch Asynchronous Search


* Fix: Update System.env syntax for Gradle 9 compatibility ([#763](https://github.com/opensearch-project/asynchronous-search/pull/763))


### Opensearch Common Utils


* Fix: Update System.env syntax for Gradle 9 compatibility ([#867](https://github.com/opensearch-project/common-utils/pull/867))


### Opensearch Cross Cluster Replication


* Fix: Replication of large documents breaches the size limit (2GB) of ReleasableBytesStreamOutput ([#1580](https://github.com/opensearch-project/cross-cluster-replication/pull/1580))
* Fix: Update System.env syntax for Gradle 9 compatibility ([#1575](https://github.com/opensearch-project/cross-cluster-replication/pull/1575))


### Opensearch Custom Codecs


* Fix: Update System.env syntax for Gradle 9 compatibility ([#273](https://github.com/opensearch-project/custom-codecs/pull/273))


### Opensearch Dashboards Observability


* [Traces] Toast Error handling ([#2463](https://github.com/opensearch-project/dashboards-observability/pull/2463))
* Test fixes ([#2492](https://github.com/opensearch-project/dashboards-observability/pull/2492))


### Opensearch Dashboards Search Relevance


* Allow more than ten results in queryset comparison view when k > 10 ([#637](https://github.com/opensearch-project/dashboards-search-relevance/pull/637))
* Show first 10,000 experiment results ([#645](https://github.com/opensearch-project/dashboards-search-relevance/pull/645))


### Opensearch Flow Framework


* Pre-create ML Commons indices for Tenant Aware tests ([#1217](https://github.com/opensearch-project/flow-framework/pull/1217))


### Opensearch Geospatial


* fix: Update System.env syntax for Gradle 9 compatibility ([#791](https://github.com/opensearch-project/geospatial/pull/791))


### Opensearch Index Management


* Fix the build ([#1491](https://github.com/opensearch-project/index-management/pull/1491))
* Fix: Update System.env syntax for Gradle 9 compatibility ([#1474](https://github.com/opensearch-project/index-management/pull/1474))


### Opensearch Job Scheduler


* Fix: Update System.env syntax for Gradle 9 compatibility ([#821](https://github.com/opensearch-project/job-scheduler/pull/821))
* Revert "Introduce a configurable remote metadata client AND migrate LockService to the client (#831)" to avoid jarHell in downstream plugins. ([#836](https://github.com/opensearch-project/job-scheduler/pull/836))


### Opensearch K Nn


* Use queryVector length if present in MDC check ([#2867](https://github.com/opensearch-project/k-NN/pull/2867))
* Fix derived source deserialization bug on invalid documents ([#2882](https://github.com/opensearch-project/k-NN/pull/2882))
* Fix invalid cosine score range in LuceneOnFaiss ([#2892](https://github.com/opensearch-project/k-NN/pull/2892))
* Allows k to be nullable to fix filter bug ([#2836](https://github.com/opensearch-project/k-NN/issues/2836))
* Fix integer overflow for while estimating distance computations for efficient filtering ([#2903](https://github.com/opensearch-project/k-NN/pull/2903))
* Fix AVX2 detection on other platforms ([#2912](https://github.com/opensearch-project/k-NN/pull/2912))
* Fix byte[] radial search for faiss ([#2905](https://github.com/opensearch-project/k-NN/pull/2905))
* Use the unique doc id for MMR rerank rather than internal lucenue doc id which is not unique for multiple shards case. ([#2911](https://github.com/opensearch-project/k-NN/pull/2911))
* Fix local ref leak in JNI ([#2916](https://github.com/opensearch-project/k-NN/pull/2916))
* Fix rescoring logic for nested exact search ([#2921](https://github.com/opensearch-project/k-NN/pull/2921))


### Opensearch ML Common


* Fix NPE when execute flow agent with mutli tenancy is off ([#4189](https://github.com/opensearch-project/ml-commons/pull/4189))
* Fix claude model it ([#4167](https://github.com/opensearch-project/ml-commons/pull/4167))
* Fix error\_prone\_annotations jar hell ([#4214](https://github.com/opensearch-project/ml-commons/pull/4214))
* Fix failing UTs and increment version to 3.3.0-SNAPSHOT ([#4132](https://github.com/opensearch-project/ml-commons/pull/4132))
* Fix jdt formatter error ([#4151](https://github.com/opensearch-project/ml-commons/pull/4151))
* Fix missing RAG response from generative\_qa\_parameters ([#4118](https://github.com/opensearch-project/ml-commons/pull/4118))
* Fix model deploy issue and address other comments in #4003 ([#4207](https://github.com/opensearch-project/ml-commons/pull/4207))
* Fix: refactor memory delete by query API to avoid anti pattern ([#4234](https://github.com/opensearch-project/ml-commons/pull/4234))
* Fix MLTaskState enum serialization errors ([#4158](https://github.com/opensearch-project/ml-commons/pull/4158))
* Fix connector tool IT ([#4233](https://github.com/opensearch-project/ml-commons/pull/4233))
* Agent/Tool Parsing Fixes ([#4138](https://github.com/opensearch-project/ml-commons/pull/4138))
* [Metrics Framework] Fix version checking logic for starting the stats collector job ([#4220](https://github.com/opensearch-project/ml-commons/pull/4220))
* Fixing build issue in ml-commons ([#4210](https://github.com/opensearch-project/ml-commons/pull/4210))
* Fixing metrics correlation algorithm ([#4200](https://github.com/opensearch-project/ml-commons/pull/4200))
* Fixing validate access for multi-tenancy ([#4196](https://github.com/opensearch-project/ml-commons/pull/4196))
* Make MLSdkAsyncHttpResponseHandler return IllegalArgumentException ([#4182](https://github.com/opensearch-project/ml-commons/pull/4182))
* Skip the model interface validation for batch predict ([#4219](https://github.com/opensearch-project/ml-commons/pull/4219))
* Fix: use builtin BulkByScrollResponse parser to parse delete by query response in memories ([#4237](https://github.com/opensearch-project/ml-commons/pull/4237))
* Fix stream predict with security enabled ([#4248](https://github.com/opensearch-project/ml-commons/pull/4248))
* Fix wrong field name in get working memory API ([#4255](https://github.com/opensearch-project/ml-commons/pull/4255))
* Fix: allow only container owner to delete memory container ([#4258](https://github.com/opensearch-project/ml-commons/pull/4258))
* [Agent Framework] Exception handling for runtime exceptions during async execution ([#4263](https://github.com/opensearch-project/ml-commons/pull/4263))
* Fix json parsing error by extracing json first; add for each processor; support input processor ([#4278](https://github.com/opensearch-project/ml-commons/pull/4278))
* Fix: add validations during create and update memory container ([#4284](https://github.com/opensearch-project/ml-commons/pull/4284))
* Fix agent streaming with security enabled + error handling ([#4256](https://github.com/opensearch-project/ml-commons/pull/4256))
* Fix llm result path; convert message to user prompt string ([#4283](https://github.com/opensearch-project/ml-commons/pull/4283))
* Fix llm result path error ([#4292](https://github.com/opensearch-project/ml-commons/pull/4292))
* Fix dimension update flow to allow embedding type update ([#4297](https://github.com/opensearch-project/ml-commons/pull/4297))
* Verify llm before summarize session ([#4300](https://github.com/opensearch-project/ml-commons/pull/4300))


### Opensearch Neural Search


* Fix reversed order of values in nested list with embedding processor ([#1570](https://github.com/opensearch-project/neural-search/pull/1570))
* [Semantic Field] Fix not able to index the multiFields for the rawFieldType ([#1572](https://github.com/opensearch-project/neural-search/pull/1572))


### Opensearch Notifications


* Fix issue publishing maven snapshots by forcing slf4j version from gradle version catalog ([#1074](https://github.com/opensearch-project/notifications/pull/1074))
* Fix: Update System.env syntax for Gradle 9 compatibility ([#1069](https://github.com/opensearch-project/notifications/pull/1069))


### Opensearch Opensearch Learning To Rank Base


* Fix bad inclusion of log4j in this jar when bundled ([#226](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/226))
* Fix: Update System.env syntax for Gradle 9 compatibility ([#219](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/219))


### Opensearch Opensearch Remote Metadata Sdk


* Throw exception on empty string for put request ID ([#235](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/235))


### Opensearch Opensearch System Templates


* Fix: Update System.env syntax for Gradle 9 compatibility ([#95](https://github.com/opensearch-project/opensearch-system-templates/pull/95))


### Opensearch Query Insights


* Change matchQuery to termQuery to correctly determine if query IDs match ([#426](https://github.com/opensearch-project/query-insights/pull/426))
* Filter out shard-level tasks from live queries ([#420](https://github.com/opensearch-project/query-insights/pull/420))
* Fix missing check for time range validation that from timestamp is before to timestamp ([#413](https://github.com/opensearch-project/query-insights/pull/413))
* Fix validation check for positive size parameter in live queries ([#414](https://github.com/opensearch-project/query-insights/pull/414))
* Fix flaky testTopQueriesResponses by clearing stale records from queues when disabling metrics ([#430](https://github.com/opensearch-project/query-insights/pull/430))
* Fix: Update System.env syntax for Gradle 9 compatibility ([#407](https://github.com/opensearch-project/query-insights/pull/407))


### Opensearch Query Insights Dashboards


* Bug fix for filter and date picker [2.19] ([#338](https://github.com/opensearch-project/query-insights-dashboards/pull/338))
* Group by selector on Configuration page always shows "None" after refresh ([#366](https://github.com/opensearch-project/query-insights-dashboards/pull/366))
* Explicitly match query by id and fix q scope in retrieveQueryById ([#367](https://github.com/opensearch-project/query-insights-dashboards/pull/367))


### Opensearch Reporting


* Fix: Update System.env syntax for Gradle 9 compatibility ([#1120](https://github.com/opensearch-project/reporting/pull/1120))


### Opensearch Search Relevance


* Updated ImportJudgmentsProcessor to handle ratings in numeric as well as string formats ([#230](https://github.com/opensearch-project/search-relevance/pull/230))


### Opensearch Security


* Added new option skip\_users to client cert authenticator (clientcert\_auth\_domain.http\_authenticator.config.skip\_users in config.yml) ([#5525](https://github.com/opensearch-project/security/pull/5525))
* [Resource Sharing] Fixes accessible resource ids search by marking created\_by.user field as keyword search instead of text ([#5574](https://github.com/opensearch-project/security/pull/5574))
* [Resource Sharing] Reverts @Inject pattern usage for ResourceSharingExtension to client accessor pattern. ([#5576](https://github.com/opensearch-project/security/pull/5576))
* Inject user custom attributes when injecting user and role information to the thread context ([#5560](https://github.com/opensearch-project/security/pull/5560))
* Allow any plugin system request when `plugins.security.system_indices.enabled` is set to `false` ([#5579](https://github.com/opensearch-project/security/pull/5579))
* [Resource Sharing] Always treat GET \_doc request as indices request even when performed on sharable resource index ([#5631](https://github.com/opensearch-project/security/pull/5631))
* Fix JWT log spam when JWT authenticator is configured with an empty list for roles\_key ([#5640](https://github.com/opensearch-project/security/pull/5640))
* Updates resource visibility when handling PATCH api to update sharing record ([#5654](https://github.com/opensearch-project/security/pull/5654))
* Handles resource updates which otherwise may wipe out all\_shared\_principals ([#5658](https://github.com/opensearch-project/security/pull/5658))
* Makes initial share map mutable to allow multiple shares ([#5666](https://github.com/opensearch-project/security/pull/5666))
* Add the fallback logic to use 'ssl\_engine' if 'ssl\_handler' attribute is not available / compatible ([#5667](https://github.com/opensearch-project/security/pull/5667))
* Change incorrect licenses in Security Principal files ([#5675](https://github.com/opensearch-project/security/pull/5675))


### Opensearch Security Analytics


* Ensure that user attributes are in expected format attrKey=attrVal for testing ([#1583](https://github.com/opensearch-project/security-analytics/pull/1583))
* Remove direct reference to Job-Scheduler Lock Index in SAP repo ([#1577](https://github.com/opensearch-project/security-analytics/pull/1577))


### Opensearch Security Analytics Dashboards Plugin


* Security fix: upgrade js-yaml to v4.1 ([#1330](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1330))


### Opensearch Skills


* Delete-single-baseline ([#641](https://github.com/opensearch-project/skills/pull/641))
* Fix WebSearchTool issue ([#639](https://github.com/opensearch-project/skills/pull/639))


### Opensearch User Behavior Insights


* fix dependencies ([#128](https://github.com/opensearch-project/user-behavior-insights/pull/128))
* fix: Update System.env syntax for Gradle 9 compatibility ([#122](https://github.com/opensearch-project/user-behavior-insights/pull/122))


### SQL


* Fix the `count(*)` and `dc(field)` to be capped at MAX\_INTEGER #4416 ([#4418](https://github.com/opensearch-project/sql/pull/4418))
* Mod function should return decimal instead of float when handle the operands are decimal literal ([#4407](https://github.com/opensearch-project/sql/pull/4407))
* Fix numbered token bug and make it optional output in patterns command ([#4402](https://github.com/opensearch-project/sql/pull/4402))
* Scale of decimal literal should always be positive in Calcite ([#4401](https://github.com/opensearch-project/sql/pull/4401))
* Fix bug of missed analyzed node when pushdown filter for Search call ([#4388](https://github.com/opensearch-project/sql/pull/4388))
* Fix parse related functions return behavior in case of NULL input ([#4381](https://github.com/opensearch-project/sql/pull/4381))
* Prevent limit pushdown before action building instead of in action executing ([#4377](https://github.com/opensearch-project/sql/pull/4377))
* No index found with given index pattern should throw IndexNotFoundException ([#4369](https://github.com/opensearch-project/sql/pull/4369))
* Fix `ClassCastException` for value-storing aggregates on nested PPL fields ([#4360](https://github.com/opensearch-project/sql/pull/4360))
* change Anonymizer to mask PPL ([#4352](https://github.com/opensearch-project/sql/pull/4352))
* Fix alphanumeric search which starts with number ([#4334](https://github.com/opensearch-project/sql/pull/4334))
* Push down stats with bins on time field into auto\_date\_histogram ([#4329](https://github.com/opensearch-project/sql/pull/4329))
* Fix geopoint issue in complex data types ([#4325](https://github.com/opensearch-project/sql/pull/4325))
* Support serializing & deserializing UDTs when pushing down scripts ([#4245](https://github.com/opensearch-project/sql/pull/4245))
* Bugfix: SQL type mapping for legacy JDBC output ([#3613](https://github.com/opensearch-project/sql/pull/3613))


## INFRASTRUCTURE


### Opensearch Anomaly Detection


* Fix tests by adding the new node setting for protected types ([#1572](https://github.com/opensearch-project/anomaly-detection/pull/1572))


* Fix flaky ITs ([#1571](https://github.com/opensearch-project/anomaly-detection/pull/1571))
* Exclude long-running tests from integTestRemote ([#1579](https://github.com/opensearch-project/anomaly-detection/pull/1579))


### Opensearch Common Utils


* Update delete\_backport\_branch workflow to include release-chores branches ([#860](https://github.com/opensearch-project/common-utils/pull/860))


### Opensearch Dashboards Search Relevance


* Update delete-backport-branch workflow permissions to use contents:write instead of pull-requests:write


### Opensearch Index Management


* Dependabot: bump 1password/load-secrets-action from 2 to 3 ([#1473](https://github.com/opensearch-project/index-management/pull/1473))


### Opensearch Job Scheduler


* Run integ tests in the sample plugin with tests.security.manager set to true ([#809](https://github.com/opensearch-project/job-scheduler/pull/809))
* Update delete\_backport\_branch workflow to include release-chores branches ([#810](https://github.com/opensearch-project/job-scheduler/pull/810))


### Opensearch ML Common


* Update maintainer list ([#4139](https://github.com/opensearch-project/ml-commons/pull/4139))
* Downloads test certificates from security plugin ([#4245](https://github.com/opensearch-project/ml-commons/pull/4245))
* Update approver matching to be exact match ([#4247](https://github.com/opensearch-project/ml-commons/pull/4247))
* Fix approver parsing bug in require-approval workflow ([#4259](https://github.com/opensearch-project/ml-commons/pull/4259))


### Opensearch Neural Search


* [Unit Test] Enable mocking of final classes and static functions ([#1528](https://github.com/opensearch-project/neural-search/pull/1528))
* [BWC Test] Remove CodeQL from BWC's CI node to increase available disk size ([#1584](https://github.com/opensearch-project/neural-search/pull/1584))


### Opensearch Opensearch Learning To Rank Base


* Adding code coverage report generation ([#228](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/228))
* Switching to a hybrid method of comparing floats in our assertions ([#221](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/221))


### Opensearch Query Insights


* Add unit tests when clear the shared queue ([#435](https://github.com/opensearch-project/query-insights/pull/435))


### Opensearch Query Insights Dashboards


* Enable wlm mode in pipeline ([#336](https://github.com/opensearch-project/query-insights-dashboards/pull/336))
* Cypress-workflow-fix ([#329](https://github.com/opensearch-project/query-insights-dashboards/pull/329))
* Revert "cypress-workflow-fix (#329)" ([#335](https://github.com/opensearch-project/query-insights-dashboards/pull/335))
* Update delete-backport-branch workflow to include release-chores branches ([#327](https://github.com/opensearch-project/query-insights-dashboards/pull/327))


### Opensearch Search Relevance


* Updated System.env syntax for Gradle 9 compatibility ([#227](https://github.com/opensearch-project/search-relevance/pull/227))


### Opensearch Skills


* Update System.env syntax for Gradle 9 compatibility ([#630](https://github.com/opensearch-project/skills/pull/630))


### SQL


* Spotless precommit: apply instead of check ([#4320](https://github.com/opensearch-project/sql/pull/4320))
* Add spotless precommit hook + license check ([#4306](https://github.com/opensearch-project/sql/pull/4306))
* Fix doctest branch ([#4292](https://github.com/opensearch-project/sql/pull/4292))
* Doctest: Use 1.0 branch of CLI instead of main ([#4219](https://github.com/opensearch-project/sql/pull/4219))
* Add merge\_group trigger to test workflows ([#4216](https://github.com/opensearch-project/sql/pull/4216))
* Split up our test actions into unit, integ, and doctest. ([#4193](https://github.com/opensearch-project/sql/pull/4193))


## DOCUMENTATION


### Opensearch Common Utils


* Added release notes for 2.13 ([#869](https://github.com/opensearch-project/common-utils/pull/869))


### Opensearch ML Common


* Add colpali blueprint ([#4130](https://github.com/opensearch-project/ml-commons/pull/4130))
* Add tutorial for agentic search ([#4127](https://github.com/opensearch-project/ml-commons/pull/4127))
* Ollama connector blueprint ([#4160](https://github.com/opensearch-project/ml-commons/pull/4160))
* Tutorial on agentic memory with strands agents ([#4125](https://github.com/opensearch-project/ml-commons/pull/4125))
* Change suggested instance type in tutorial ([#4145](https://github.com/opensearch-project/ml-commons/pull/4145))


### Opensearch Security


* [Resource Sharing] Adds comprehensive documentation for Resource Access Control feature ([#5540](https://github.com/opensearch-project/security/pull/5540))


### SQL


* Update bin.rst and add `bin` to doctest ([#4384](https://github.com/opensearch-project/sql/pull/4384))
* Update timechart in SPL/PPL cheat sheet ([#4382](https://github.com/opensearch-project/sql/pull/4382))
* Enable doctest with Calcite ([#4379](https://github.com/opensearch-project/sql/pull/4379))
* Correct the comparision table for rex doc ([#4321](https://github.com/opensearch-project/sql/pull/4321))
* Updating coalesce documentation ([#4305](https://github.com/opensearch-project/sql/pull/4305))
* Updating documentation for `fields` and `table` commands ([#4177](https://github.com/opensearch-project/sql/pull/4177))
* Add documents on how to develop a UDF / UDAF ([#4094](https://github.com/opensearch-project/sql/pull/4094))
* Add splunk to ppl cheat sheet ([#3726](https://github.com/opensearch-project/sql/pull/3726))


## MAINTENANCE


### Opensearch Alerting


* [AUTO] Increment version to 3.3.0-SNAPSHOT ([#1918](https://github.com/opensearch-project/alerting/pull/1918))


### Opensearch Alerting Dashboards Plugin


* Increment version to 3.3.0.0 ([#1283](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1283))


### Opensearch Anomaly Detection Dashboards Plugin


* Bump axios from 1.8.2 to 1.12.1 ([#1094](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1094))
* Bump cipher-base from 1.0.4 to 1.0.6 ([#1084](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1084))
* Bump sha.js from 2.4.11 to 2.4.12 ([#1085](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1085))
* Increment version to 3.3.0.0 ([#1089](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1089))


### Opensearch Asynchronous Search


* Increment version to 3.3.0-SNAPSHOT ([#761](https://github.com/opensearch-project/asynchronous-search/pull/761))


### Opensearch Custom Codecs


* Update for Lucene 10.3 ([#277](https://github.com/opensearch-project/custom-codecs/pull/277))


### Opensearch Dashboards Assistant


* Add delete\_backport\_branch workflow to automatically delete branches that start with "backport/" or "release-chores/" after they are merged


### Opensearch Dashboards Maps


* Increment version to 3.3.0.0 ([#755](https://github.com/opensearch-project/dashboards-maps/pull/755))


### Opensearch Dashboards Notifications


* Increment version to 3.3.0.0 ([#371](https://github.com/opensearch-project/dashboards-notifications/pull/371))


### Opensearch Dashboards Observability


* Update cypress/requests ([#2507](https://github.com/opensearch-project/dashboards-observability/pull/2507))
* [AUTO] Increment version to 3.3.0.0 ([#2494](https://github.com/opensearch-project/dashboards-observability/pull/2494))


### Opensearch Dashboards Query Workbench


* Increment version to 3.3.0.0 ([#492](https://github.com/opensearch-project/dashboards-query-workbench/pull/492))
* Fixing CVE-2025-7783 ([#640](https://github.com/opensearch-project/dashboards-reporting/pull/640))


### Opensearch Dashboards Reporting


* Increment version to 3.3.0.0 ([#622](https://github.com/opensearch-project/dashboards-reporting/pull/622))
* Fixing CVE-2025-9287 CVE-2025-9288 ([#640](https://github.com/opensearch-project/dashboards-reporting/pull/640))


### Opensearch Geospatial


* Remove deprecated URL(String) usage ([#795](https://github.com/opensearch-project/geospatial/pull/795))
* Increment version to 3.3.0-SNAPSHOT ([#788](https://github.com/opensearch-project/geospatial/pull/788))


### Opensearch Index Management


* [AUTO] Increment version to 3.3.0-SNAPSHOT ([#1467](https://github.com/opensearch-project/index-management/pull/1467))


### Opensearch Index Management Dashboards Plugin


* Increment version to 3.3.0.0 ([#1347](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1347))


### Opensearch Job Scheduler


* Dependabot: bump actions/download-artifact from 4 to 5 ([#811](https://github.com/opensearch-project/job-scheduler/pull/811))
* Dependabot: bump actions/checkout from 4 to 5 ([#818](https://github.com/opensearch-project/job-scheduler/pull/818))
* Dependabot: bump 1password/load-secrets-action from 2 to 3 ([#819](https://github.com/opensearch-project/job-scheduler/pull/819))
* Dependabot: bump actions/setup-java from 1 to 4 ([#825](https://github.com/opensearch-project/job-scheduler/pull/825))
* Dependabot: bump actions/github-script from 7 to 8 ([#829](https://github.com/opensearch-project/job-scheduler/pull/829))
* Dependabot: bump actions/setup-java from 4 to 5 ([#830](https://github.com/opensearch-project/job-scheduler/pull/830))


### Opensearch K Nn


* Replace commons-lang with org.apache.commons:commons-lang3 ([#2863](https://github.com/opensearch-project/k-NN/pull/2863))
* Bump OpenSearch-Protobufs to 0.13.0 ([#2833](https://github.com/opensearch-project/k-NN/pull/2833))
* Bump Lucene version to 10.3 and fix build failures ([#2878](https://github.com/opensearch-project/k-NN/pull/2878))


### Opensearch ML Common


* Adding more unit tests ([#4124](https://github.com/opensearch-project/ml-commons/pull/4124))
* Adding more unit tests ([#4126](https://github.com/opensearch-project/ml-commons/pull/4126))
* Move common string ([#4173](https://github.com/opensearch-project/ml-commons/pull/4173))
* Fix Cohere IT ([#4174](https://github.com/opensearch-project/ml-commons/pull/4174))
* Updating gson version to resolve conflict coming from core ([#4176](https://github.com/opensearch-project/ml-commons/pull/4176))


### Opensearch ML Commons Dashboards


* [AUTO] Increment version to 3.3.0.0 ([#443](https://github.com/opensearch-project/ml-commons-dashboards/pull/443))
* Update delete\_backport\_branch workflow to include release-chores branches ([#442](https://github.com/opensearch-project/ml-commons-dashboards/pull/442))


### Opensearch Neural Search


* Remove commons-lang:commons-lang dependency and use gradle version catalog for commons-lang3 ([#1551](https://github.com/opensearch-project/neural-search/pull/1551))
* Update Lucene101 codec path to backward path & force errorprone version to 2.21.1 to resolve conflict ([#1574](https://github.com/opensearch-project/neural-search/pull/1574))
* Upgrade QA Gradle Dependency Version with commons-lang3 ([#1589](https://github.com/opensearch-project/neural-search/pull/1589))


### Opensearch Notifications


* [AUTO] Increment version to 3.3.0-SNAPSHOT ([#1064](https://github.com/opensearch-project/notifications/pull/1064))


### Opensearch Observability


* Increment version to 3.3.0-SNAPSHOT ([#1941](https://github.com/opensearch-project/observability/pull/1941))


### Opensearch Opensearch Learning To Rank Base


* Bump SLF4J to 2.0.17 ([#224](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/224))
* Upgrade spotless plugin and address build deprecations ([#222](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/222))
* [AUTO] Increment version to 3.3.0-SNAPSHOT ([#217](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/217))


### Opensearch Opensearch System Templates


* [AUTO] Increment version to 3.3.0-SNAPSHOT ([#93](https://github.com/opensearch-project/opensearch-system-templates/pull/93))


### Opensearch Performance Analyzer


* Increment to 3.3.0.0 and run ./gradlew updateSHAs and check in latest sha files ([#846](https://github.com/opensearch-project/performance-analyzer/pull/846))


### Opensearch Query Insights


* [AUTO] Increment version to 3.3.0-SNAPSHOT ([#404](https://github.com/opensearch-project/query-insights/pull/404))


### Opensearch Query Insights Dashboards


* Increment version to 3.3.0.0 ([#332](https://github.com/opensearch-project/query-insights-dashboards/pull/332))
* Update dependency pbkdf2 to v3.1.4 ([#375](https://github.com/opensearch-project/query-insights-dashboards/pull/375))
* Update dependency pbkdf2 to v3.1.5 ([#378](https://github.com/opensearch-project/query-insights-dashboards/pull/378))
* Fix form-data CVE-2025-7783 ([#380](https://github.com/opensearch-project/query-insights-dashboards/pull/380))


### Opensearch Reporting


* [AUTO] Increment version to 3.3.0-SNAPSHOT ([#1118](https://github.com/opensearch-project/reporting/pull/1118))


### Opensearch Security Analytics


* Adding toepkerd to MAINTAINERS.md ([#1585](https://github.com/opensearch-project/security-analytics/pull/1585))
* Increment version to 3.3.0-SNAPSHOT ([#1574](https://github.com/opensearch-project/security-analytics/pull/1574))


### Opensearch Security Analytics Dashboards Plugin


* [AUTO] Increment version to 3.3.0.0 ([#1325](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1325))


### Opensearch Security Dashboards Plugin


* Bump `actions/checkout` from 4 to 5 ([#2295](https://github.com/opensearch-project/security-dashboards-plugin/pull/2295))
* Bump `derek-ho/start-opensearch` from 7 to 8 ([#2309](https://github.com/opensearch-project/security-dashboards-plugin/pull/2309))
* Bump `actions/github-script` from 7 to 8 ([#2307](https://github.com/opensearch-project/security-dashboards-plugin/pull/2307))


### Opensearch Skills


* Increment version to 3.3.0-SNAPSHOT ([#626](https://github.com/opensearch-project/skills/pull/626))


### Opensearch User Behavior Insights


* Increment version to 3.3.0-SNAPSHOT ([#127](https://github.com/opensearch-project/user-behavior-insights/pull/127))


### SQL


* Avoid unnecessary security plugin download in integ-test ([#4368](https://github.com/opensearch-project/sql/pull/4368))
* Fix timezone dependent test failures ([#4367](https://github.com/opensearch-project/sql/pull/4367))
* Update grammar files and developer guide ([#4301](https://github.com/opensearch-project/sql/pull/4301))
* Introduce YAML formatter for better testing/debugging ([#4274](https://github.com/opensearch-project/sql/pull/4274))
* Print links to test logs after integTest ([#4273](https://github.com/opensearch-project/sql/pull/4273))
* Fix the IT issue caused by merging conflict ([#4270](https://github.com/opensearch-project/sql/pull/4270))
* Fix gitignore to ignore symbolic link ([#4263](https://github.com/opensearch-project/sql/pull/4263))
* Add gitignore for Cline ([#4258](https://github.com/opensearch-project/sql/pull/4258))
* Add Ryan as a maintainer ([#4257](https://github.com/opensearch-project/sql/pull/4257))


## REFACTORING


### Opensearch Anomaly Detection


* Updates search handler to consume resource authz and updates resource authz related tests ([#1546](https://github.com/opensearch-project/anomaly-detection/pull/1546))
* Adds resource types to DocRequests ([#1566](https://github.com/opensearch-project/anomaly-detection/pull/1566))


### Opensearch K Nn


* Refactored the KNN Stat files for better readability.


### Opensearch Opensearch Remote Metadata Sdk


* Remove unneeded enum uppercase workaround ([#185](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/185))


* Update argument type for ThreadContextAccess:doPrivileged ([#250](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/250))
* Use AccessController instead of ThreadContextAccess as it's for internal use ([#254](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/254))


### Opensearch Security


* [Resource Sharing] Match index settings of .kibana indices for resource sharing indices ([#5605](https://github.com/opensearch-project/security/pull/5605))


## NON-COMPLIANT


## ADDED


### Opensearch Security


* Introduced new experimental versioned security configuration management feature ([#5357](https://github.com/opensearch-project/security/pull/5357))
* Introduced View API and Rollback API for experimental versioned security configurations ([#5431](https://github.com/opensearch-project/security/pull/5431))


## DEPENDENCIES


### Opensearch Security


* Update delete\_backport\_branch workflow to include release-chores branches ([#5548](https://github.com/opensearch-project/security/pull/5548))
* Bump `1password/load-secrets-action` from 2 to 3 ([#5573](https://github.com/opensearch-project/security/pull/5573))
* Bump `actions/checkout` from 4 to 5 ([#5572](https://github.com/opensearch-project/security/pull/5572), [#5660](https://github.com/opensearch-project/security/pull/5660))
* Bump `jjwt_version` from 0.12.6 to 0.13.0 ([#5568](https://github.com/opensearch-project/security/pull/5568), [#5581](https://github.com/opensearch-project/security/pull/5581))
* Bump `org.mockito:mockito-core` from 5.18.0 to 5.20.0 ([#5566](https://github.com/opensearch-project/security/pull/5566), [#5650](https://github.com/opensearch-project/security/pull/5650))
* Bump `open_saml_version` from 5.1.4 to 5.1.6 ([#5567](https://github.com/opensearch-project/security/pull/5567), [#5614](https://github.com/opensearch-project/security/pull/5614))
* Bump `com.google.j2objc:j2objc-annotations` from 3.0.0 to 3.1 ([#5570](https://github.com/opensearch-project/security/pull/5570))
* Bump `spring_version` from 6.2.9 to 6.2.11 ([#5569](https://github.com/opensearch-project/security/pull/5569), [#5636](https://github.com/opensearch-project/security/pull/5636))
* Bump `com.github.spotbugs` from 6.2.4 to 6.4.1 ([#5584](https://github.com/opensearch-project/security/pull/5584), [#5611](https://github.com/opensearch-project/security/pull/5611), [#5637](https://github.com/opensearch-project/security/pull/5637))
* Bump `open_saml_shib_version` from 9.1.4 to 9.1.6 ([#5585](https://github.com/opensearch-project/security/pull/5585), [#5612](https://github.com/opensearch-project/security/pull/5612))
* Bump `org.springframework.kafka:spring-kafka-test` from 4.0.0-M3 to 4.0.0-M5 ([#5583](https://github.com/opensearch-project/security/pull/5583), [#5661](https://github.com/opensearch-project/security/pull/5661))
* Bump `net.bytebuddy:byte-buddy` from 1.17.6 to 1.17.7 ([#5586](https://github.com/opensearch-project/security/pull/5586))
* Bump `io.dropwizard.metrics:metrics-core` from 4.2.33 to 4.2.37 ([#5589](https://github.com/opensearch-project/security/pull/5589), [#5638](https://github.com/opensearch-project/security/pull/5638))
* Bump `com.nimbusds:nimbus-jose-jwt:9.48` from 9.48 to 10.4.2 ([#5595](https://github.com/opensearch-project/security/pull/5595))
* Bump `actions/github-script` from 7 to 8 ([#5610](https://github.com/opensearch-project/security/pull/5610))
* Bump `org.eclipse.platform:org.eclipse.core.runtime` from 3.33.100 to 3.34.0 ([#5628](https://github.com/opensearch-project/security/pull/5628))
* Bump `org.opensearch:protobufs` from 0.6.0 to 0.13.0 ([#5553](https://github.com/opensearch-project/security/pull/5553))
* Bump `org.checkerframework:checker-qual` from 3.49.5 to 3.51.0 ([#5627](https://github.com/opensearch-project/security/pull/5627))
* Bump `com.nimbusds:nimbus-jose-jwt` from 10.4.2 to 10.5 ([#5629](https://github.com/opensearch-project/security/pull/5629))
* Bump `derek-ho/start-opensearch` from 7 to 8 ([#5630](https://github.com/opensearch-project/security/pull/5630))
* Bump `actions/setup-java` from 4 to 5 ([#5582](https://github.com/opensearch-project/security/pull/5582), [#5664](https://github.com/opensearch-project/security/pull/5664))
* Bump `org.eclipse.platform:org.eclipse.equinox.common` from 3.20.100 to 3.20.200 ([#5651](https://github.com/opensearch-project/security/pull/5651))
* Bump `jakarta.xml.bind:jakarta.xml.bind-api` from 4.0.2 to 4.0.4 ([#5649](https://github.com/opensearch-project/security/pull/5649))
* Bump `com.google.errorprone:error_prone_annotations` from 2.41.0 to 2.42.0 ([#5648](https://github.com/opensearch-project/security/pull/5648))
* Bump `com.google.guava:guava` from 33.4.8-jre to 33.5.0-jre ([#5665](https://github.com/opensearch-project/security/pull/5665))
* Bump `com.typesafe.scala-logging:scala-logging_3` from 3.9.5 to 3.9.6 ([#5663](https://github.com/opensearch-project/security/pull/5663))
* Sync `org.opensearch:protobufs` version with core ([#5659](https://github.com/opensearch-project/security/pull/5659))


