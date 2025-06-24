# OpenSearch and OpenSearch Dashboards 3.1.0 Release Notes

## Release Highlights

OpenSearch 3.1 delivers an array of upgrades to help you increase indexing performance, improve search results, dig deeper into your observability data, build more powerful agentic AI solutions, and more. 
 
### New and Updated Features

* GPU-accelerated index builds: Released as experimental in OpenSearch 3.0, GPU acceleration is production-ready in OpenSearch 3.1, unlocking parallel processing power for intensive index build operations that can reduce time-to-build by a factor of 9.3x while reducing costs by 3.75x compared to CPU-based solutions.
* New Update Agent API: Now users can make direct updates to existing agents via an API, eliminating the need to create new agents when modifying configurations such as model IDs, workflow tools, or prompts for streamlined agent management.
* ML Commons metrics integration: ML Commons is integrated with the OpenSearch metrics framework, enabling user-configurable, comprehensive monitoring capabilities with OpenTelemetry compatibility. Included are dynamic instrumentation that captures runtime metrics along critical code paths and static collection via scheduled jobs that report state-level metrics.
* Search Relevance Workbench: A new Search Relevance Workbench lets you explore, experiment with, and tune search strategies in OpenSearch. The toolset offers search algorithm comparison within the OpenSearch UI, along with the ability to evaluate search quality based on user activity via User Behavior Insights.
* Lucene HNSW on Faiss indexes: This release enables Lucene's HNSW graph search algorithm to run directly on existing Faiss indexes, unlocking partial byte loading and early termination for improved large-scale vector search efficiency in memory-constrained environments and up to 2x faster performance compared to Faiss C++.
* OpenSearch Flow enhancements: Upgrades to OpenSearch Flow include a redesigned workflow detail page that simplifies end-to-end configuration with a unified view of ingest and search components. A new workflow template for semantic search using sparse encoders simplifies deployment of search-by-text and ranks results by semantic similarity, improving the quality and relevance of search experiences.
* OnDisk 4x compression rescoring: Rescoring support is enabled by default for new indexes using 4x compression, allowing you to maintain high search recall quality while realizing the performance and efficiency benefits of compression. Users who prefer the previous behavior have the option to explicitly set rescore to false.
* New semantic field type: The semantic field streamlines semantic search setup. You can define a semantic field in your index mapping with an associated ML model ID, and OpenSearch can automatically create the appropriate embedding field based on the model's metadata. The neural query supports semantic fields, so you can query with plain text and let OpenSearch handle embedding generation and field resolution.
* Star-tree indexes in production: Now generally available, star-tree indexes can increase  the performance of aggregations by up to 100x, with support for a wide range of query and aggregation types.
* Workload management enhancements: Index-based auto-tagging allows you to manage groups of tenants and define rules for how they consume cluster resources, without the need to explicitly tag search requests via headers.
* Hybrid query performance improvements: Enhanced document collection and scoring techniques boost hybrid search performance, delivering improvements of up to 65% in query response times and up to 3.5x in throughput. These algorithmic improvements help optimize how OpenSearch identifies and ranks matching documents during the fusion of lexical and semantic search results for even more efficient hybrid search.
* Tracing and correlation for observability workloads: Support for custom index names containing OpenTelemetry spans, logs, and service maps helps users correlate logs and traces across multiple clusters. Users can also map custom fields for log indexes that do not follow the OpenTelemetry format. Cross-cluster search for traces enables analysis across cluster boundaries, and new features for trace-to-logs correlation make it easier to monitor, troubleshoot, and maintain distributed applications regardless of logging format or deployment architecture.
* PPL commands for nested JSON: New JSON functions and Piped Processing Language (PPL) commands for JSON help analysts extract specific values from deeply nested JSON objects or transform nested arrays into a more analyzable format, eliminating the need for complex workarounds and enabling sophisticated analysis of JSON data directly within OpenSearch.
* Native time-series forecasting: Apply a Random Cut Forest model to turn an index with a timestamped field into a self-updating signal. As the model retrains incrementally on each new point, it can adapt instantly to shifts while minimizing compute and storage overhead. Combine forecasts with Alerting for real-time notifications when a metric is predicted to cross a threshold so you can scale capacity or adjust spend before issues arise.
* Additional PPL commands and functions: More than 20 new PPL commands and functions offer additional ways to explore your data with OpenSearch's observability tools.
* Immutable user object for security authorization: The user object is now immutable in the Security plugin, reducing the number of serializations and deserializations required as this object is passed internally within the cluster while handling a request, resulting in lower performance overhead.
* Privilege optimization for tenants: This release incorporates updates to privilege evaluation as part of an ongoing optimization effort. Extending privilege evaluation to encompass tenant_permissions lets OpenSearch roles take full advantage of precomputed data structures for performance improvements, particularly for clusters using multi-tenancy with a large number of tenants.
* Collapse in hybrid query: This release extends hybrid query functionality with collapse parameter support, enabling document grouping and deduplication based on specified field values.
* New encoding of BPV 21 for DocIdsWriter: A new variation of an existing encoding algorithm offers optimized docId storage within the BKD index, resulting in reduced storage footprint across numeric, IP, and other fields using the BKD index while facilitating more efficient docId retrieval.

### Experimental Features

OpenSearch 3.1 includes the following experimental functionality. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.
 
* Resource sharing and access control: An experimental authorization framework moves the sharing and access authorization setup from individual plugins to the Security plugin to support improved security posture. Plugins will be required to onboard to this new feature; for this release, the Anomaly Detection plugin has been updated to support the new authorization framework.
* Model Context Protocol (MCP) enhancements: New update MCP tools and list MCP tools APIs add functionality to OpenSearch's MCP support. A new system index is also included, allowing the MCP tools to persist in the system index so that tools won't be lost after a restart at the cluster or node level.


## Release Details
[OpenSearch and OpenSearch Dashboards 3.1.0](https://opensearch.org/artifacts/by-version/#release-3-1-0) includes the following breaking changes, features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.1.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.1.0.md).


## BREAKING CHANGES


### SQL


* Switch percentile implementation to MergingDigest to align with OpenSearch ([#3698](https://github.com/opensearch-project/sql/pull/3698))
* Support decimal literal with Calcite ([#3673](https://github.com/opensearch-project/sql/pull/3673))


## FEATURES


### OpenSearch Alerting


* Use transport service timeout instead of custom impl ([#1856](https://github.com/opensearch-project/alerting/pull/1856))
* Now publishes a list of findings instead of an individual one ([#1860](https://github.com/opensearch-project/alerting/pull/1860))


### OpenSearch Alerting Dashboards Plugin


* Add alert insight to alerts card on overview page ([#1248](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1248))


### OpenSearch Anomaly Detection Dashboards


* Forecasting frontend ([#1038](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1038))


### OpenSearch Common Utils


* Updating PublishFindingsRequest to use a list of findings ([#832](https://github.com/opensearch-project/common-utils/pull/832))


### OpenSearch Custom Codecs


* Add QAT-Accelerated Zstandard Compression Support ([#238](https://github.com/opensearch-project/custom-codecs/pull/238))


### OpenSearch Dashboards Search Relevance


* Add search relevance workbench features ([#533](https://github.com/opensearch-project/dashboards-search-relevance/pull/533))


### OpenSearch Flow Framework Dashboards


* Integrate preview panel into inspector panel ([#722](https://github.com/opensearch-project/dashboards-flow-framework/pull/722))
* Refactor form navigation to left panel ([#737](https://github.com/opensearch-project/dashboards-flow-framework/pull/737))
* Added workflow template for Semantic Search using Sparse Encoders ([#742](https://github.com/opensearch-project/dashboards-flow-framework/pull/742))


### OpenSearch Neural Search


* Implement analyzer based neural sparse query ([#1088](https://github.com/opensearch-project/neural-search/pull/1088) [#1279](https://github.com/opensearch-project/neural-search/pull/1279))
* [Semantic Field] Add semantic mapping transformer. ([#1276](https://github.com/opensearch-project/neural-search/pull/1276))
* [Semantic Field] Add semantic ingest processor. ([#1309](https://github.com/opensearch-project/neural-search/pull/1309))
* [Semantic Field] Implement the query logic for the semantic field. ([#1315](https://github.com/opensearch-project/neural-search/pull/1315))
* [Semantic Field] Enhance semantic field to allow to enable/disable chunking. ([#1337](https://github.com/opensearch-project/neural-search/pull/1337))
* [Semantic Field] Implement the search analyzer support for semantic field at query time. ([#1341](https://github.com/opensearch-project/neural-search/pull/1341))
* Add `FixedCharLengthChunker` for character length-based chunking ([#1342](https://github.com/opensearch-project/neural-search/pull/1342))
* [Semantic Field] Implement the search analyzer support for semantic field at semantic field index creation time. ([#1367](https://github.com/opensearch-project/neural-search/pull/1367))
* [Hybrid] Add collapse functionality to hybrid query ([#1345](https://github.com/opensearch-project/neural-search/pull/1345))


### OpenSearch Search Relevance


* Added new experiment type for hybrid search ([#26](https://github.com/opensearch-project/search-relevance/pull/26))
* Added feature flag for search relevance workbench ([#34](https://github.com/opensearch-project/search-relevance/pull/34))
* Added validation for hybrid query structure ([#40](https://github.com/opensearch-project/search-relevance/pull/40))
* Add support for importing judgments created externally from SRW ([#42](https://github.com/opensearch-project/search-relevance/pull/42))
* Changing URL for plugin APIs to /_plugin/_search_relevance [backend] ([#62](https://github.com/opensearch-project/search-relevance/pull/62))
* Add stats API ([#63](https://github.com/opensearch-project/search-relevance/pull/63))


### OpenSearch Security


* [Resource Permissions] Introduces Centralized Resource Access Control Framework ([#5281](https://github.com/opensearch-project/security/pull/5281))


### OpenSearch Skills


* Add data source type in the request body from PPL tool to meet the requirement of Text2Spark PPL ([#587](https://github.com/opensearch-project/skills/pull/587))


### OpenSearch k-NN


* Introduce memory optimized search for Faiss binary index types [#2735](https://github.com/opensearch-project/k-NN/pull/2735)
* Create RescoreKnnVectorQuery to support rescore after executing inner vector search query [#2709](https://github.com/opensearch-project/k-NN/pull/2709)


### SQL


* Support ResourceMonitor with Calcite ([#3738](https://github.com/opensearch-project/sql/pull/3738))
* Support `flatten` command with Calcite ([#3747](https://github.com/opensearch-project/sql/pull/3747))
* Support `expand` command with Calcite ([#3745](https://github.com/opensearch-project/sql/pull/3745))
* Support trendline command in Calcite ([#3741](https://github.com/opensearch-project/sql/pull/3741))
* Support `appendcol` command with Calcite ([#3729](https://github.com/opensearch-project/sql/pull/3729))
* Support Grok command in Calcite engine ([#3678](https://github.com/opensearch-project/sql/pull/3678))
* Support match\_only\_text field type ([#3663](https://github.com/opensearch-project/sql/pull/3663))
* Add DISTINCT\_COUNT\_APPROX function ([#3654](https://github.com/opensearch-project/sql/pull/3654))
* Support merging object-type fields when fetching the schema from the index ([#3653](https://github.com/opensearch-project/sql/pull/3653))
* Support `top`, `rare` commands with Calcite ([#3647](https://github.com/opensearch-project/sql/pull/3647))
* Add earliest and latest in condition function ([#3640](https://github.com/opensearch-project/sql/pull/3640))
* Support `fillnull` command with Calcite ([#3634](https://github.com/opensearch-project/sql/pull/3634))
* Support function `coalesce` with Calcite ([#3628](https://github.com/opensearch-project/sql/pull/3628))
* Support functions `isempty`, `isblank` and `ispresent` with Calcite ([#3627](https://github.com/opensearch-project/sql/pull/3627))
* Support `describe` command with Calcite ([#3624](https://github.com/opensearch-project/sql/pull/3624))
* Support Limit pushdown ([#3615](https://github.com/opensearch-project/sql/pull/3615))
* Add UT for PredicateAnalyzer and AggregateAnalyzer ([#3612](https://github.com/opensearch-project/sql/pull/3612))
* Add a new row count estimation mechanism for CalciteIndexScan ([#3605](https://github.com/opensearch-project/sql/pull/3605))
* Implement `geoip` udf with Calcite ([#3604](https://github.com/opensearch-project/sql/pull/3604))
* Implement `cidrmatch` udf with Calcite ([#3603](https://github.com/opensearch-project/sql/pull/3603))
* Support `eventstats` command with Calcite ([#3585](https://github.com/opensearch-project/sql/pull/3585))
* Add lambda function and array related functions ([#3584](https://github.com/opensearch-project/sql/pull/3584))
* Implement cryptographic hash UDFs ([#3574](https://github.com/opensearch-project/sql/pull/3574))
* Calcite patterns command brain pattern method ([#3570](https://github.com/opensearch-project/sql/pull/3570))
* Add json functions ([#3559](https://github.com/opensearch-project/sql/pull/3559))


## ENHANCEMENTS


### Dashboards Assistant


* Style single metric in text2vis ([#539](https://github.com/opensearch-project/dashboards-assistant/pull/539))
* Buffer for special characters ([#549](https://github.com/opensearch-project/dashboards-assistant/pull/549))
* Save chatbot flyout visualize state to local storage ([#553](https://github.com/opensearch-project/dashboards-assistant/pull/553))
* T2viz supports reading time range from context ([#557](https://github.com/opensearch-project/dashboards-assistant/pull/557/))
* Prevent user from navigating to t2viz from discover if ppl return no results/error ([#546](https://github.com/opensearch-project/dashboards-assistant/pull/546))
* Improve the chatbot UX by scroll the user input message to the top after sending ([#545](https://github.com/opensearch-project/dashboards-assistant/pull/545))
* Add format instruction for alert summary ([#568](https://github.com/opensearch-project/dashboards-assistant/pull/568))
* Add the admin UI setting option for control all dashboard assistant features ([#578](https://github.com/opensearch-project/dashboards-assistant/pull/578))


### OpenSearch Anomaly Detection


* Use Centralized Resource Access Control framework provided by security plugin ([#1400](https://github.com/opensearch-project/anomaly-detection/pull/1400))
* Introduce state machine, separate config index, improve suggest/validate APIs, and persist cold-start results for run-once visualization ([#1479](https://github.com/opensearch-project/anomaly-detection/pull/1479))


### OpenSearch Anomaly Detection Dashboards


* Enable contextual launch in MDS OpenSearch UI ([#1041](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1041))


### OpenSearch Flow Framework


* Make thread pool sizes configurable ([#1139](https://github.com/opensearch-project/flow-framework/issues/1139))


### OpenSearch Flow Framework Dashboards


* Misc improvements IV ([#743](https://github.com/opensearch-project/dashboards-flow-framework/pull/743))
* Update README.md ([#744](https://github.com/opensearch-project/dashboards-flow-framework/pull/744))


### OpenSearch ML Common


* Support persisting MCP tools in system index ([#3874](https://github.com/opensearch-project/ml-commons/pull/3874))
* [Agent] PlanExecuteReflect: Return memory early to track progress ([#3884](https://github.com/opensearch-project/ml-commons/pull/3884))
* Add space type mapping for pre-trained embedding models, add new additional\_config field and BaseModelConfig class ([#3786](https://github.com/opensearch-project/ml-commons/pull/3786))
* support customized message endpoint and addressing comments ([#3810](https://github.com/opensearch-project/ml-commons/pull/3810))
* Add custom SSE endpoint for the MCP Client ([#3891](https://github.com/opensearch-project/ml-commons/pull/3891))
* Expose Update Agent API ([#3820](https://github.com/opensearch-project/ml-commons/pull/3902))
* Use function calling for existing LLM interfaces ([#3888](https://github.com/opensearch-project/ml-commons/pull/3888))
* Add error handling for plan&execute agent ([#3845](https://github.com/opensearch-project/ml-commons/pull/3845))
* Metrics framework integration with ml-commons ([#3661](https://github.com/opensearch-project/ml-commons/pull/3661))


### OpenSearch Neural Search


* [Performance Improvement] Add custom bulk scorer for hybrid query (2-3x faster) ([#1289](https://github.com/opensearch-project/neural-search/pull/1289))
* [Stats] Add stats for text chunking processor algorithms ([#1308](https://github.com/opensearch-project/neural-search/pull/1308))
* Support custom weights in RRF normalization processor ([#1322](https://github.com/opensearch-project/neural-search/pull/1322))
* [Stats] Add stats tracking for semantic highlighting ([#1327](https://github.com/opensearch-project/neural-search/pull/1327))
* [Stats] Add stats for text embedding processor with different settings ([#1332](https://github.com/opensearch-project/neural-search/pull/1332))
* Validate model id and analyzer should not be provided at the same time for the neural sparse query ([#1359](https://github.com/opensearch-project/neural-search/pull/1359))
* [Stats] Add stats for score based and rank based normalization processors ([#1326](https://github.com/opensearch-project/neural-search/pull/1326))
* [Stats] Add stats tracking for semantic field ([#1362](https://github.com/opensearch-project/neural-search/pull/1362))
* [Stats] Add stats for neural query enricher, neural sparse encoding, two phase, and reranker processors ([#1343](https://github.com/opensearch-project/neural-search/pull/1343))
* [Stats] Add `include_individual_nodes`, `include_all_nodes`, `include_info` parameters to stats API ([#1360](https://github.com/opensearch-project/neural-search/pull/1360))
* [Stats] Add stats for custom flags set in ingest processors ([#1378](https://github.com/opensearch-project/neural-search/pull/1378))


### OpenSearch Observability


* [Traces] Merge custom source and data prepper mode in trace analytics ([#2457](https://github.com/opensearch-project/dashboards-observability/pull/2457))
* [Traces] Span Flyout - support new format ([#2450](https://github.com/opensearch-project/dashboards-observability/pull/2450))


### OpenSearch Query Insights


* Add metric labels to historical data ([#326](https://github.com/opensearch-project/query-insights/pull/326))
* Consolidate grouping settings ([#336](https://github.com/opensearch-project/query-insights/pull/336))
* Add setting to exclude certain indices from insight query ([#308](https://github.com/opensearch-project/query-insights/pull/308))
* Asynchronous search operations in reader ([#344](https://github.com/opensearch-project/query-insights/pull/344))
* Added isCancelled field in Live Queries API ([#355](https://github.com/opensearch-project/query-insights/pull/355))


### OpenSearch Query Insights Dashboards


* Remove duplicate requests on overview page loading ([#179](https://github.com/opensearch-project/query-insights-dashboards/pull/179))
* New Live Queries Dashboard ([#199](https://github.com/opensearch-project/query-insights-dashboards/pull/199))
* New Workload Management dashboard ([#155](https://github.com/opensearch-project/query-insights-dashboards/pull/155))
* Add unit tests for wlm dashboard ([#209](https://github.com/opensearch-project/query-insights-dashboards/pull/209))


### OpenSearch k-NN


* Removing redundant type conversions for script scoring for hamming space with binary vectors [#2351](https://github.com/opensearch-project/k-NN/pull/2351)
* Apply mask operation in preindex to optimize derived source [#2704](https://github.com/opensearch-project/k-NN/pull/2704)
* [Remote Vector Index Build] Add tuned repository upload/download configurations per benchmarking results [#2662](https://github.com/opensearch-project/k-NN/pull/2662)
* [Remote Vector Index Build] Add segment size upper bound setting and prepare other settings for GA [#2734](https://github.com/opensearch-project/k-NN/pull/2734)
* [Remote Vector Index Build] Make `index.knn.remote_index_build.enabled` default to true [#2743](https://github.com/opensearch-project/k-NN/pull/2743)
* Update rescore context for 4X Compression [#2750](https://github.com/opensearch-project/k-NN/pull/2750)


### OpenSearch Search Relevance


* Extend data model to adopt different experiment options/parameters ([#29](https://github.com/opensearch-project/search-relevance/issues/29))


### OpenSearch Security


* Github workflow for changelog verification ([#5318](https://github.com/opensearch-project/security/pull/5318))
* Add flush cache endpoint for individual user ([#5337](https://github.com/opensearch-project/security/pull/5337))
* Handle roles in nested claim for JWT auth backends ([#5355](https://github.com/opensearch-project/security/pull/5355))
* Register cluster settings listener for `plugins.security.cache.ttl_minutes` ([#5324](https://github.com/opensearch-project/security/pull/5324)
* Integrate search-relevance functionalities with security plugin ([#5376](https://github.com/opensearch-project/security/pull/5376))
* Use extendedPlugins in integrationTest framework for sample resource plugin testing ([#5322](https://github.com/opensearch-project/security/pull/5322))
* Introduced new, performance-optimized implementation for tenant privileges ([#5339](https://github.com/opensearch-project/security/pull/5339))
* Performance improvements: Immutable user object ([#5212](https://github.com/opensearch-project/security/pull/5212))
* Include mapped roles when setting userInfo in ThreadContext ([#5369](https://github.com/opensearch-project/security/pull/5369))
* Adds details for debugging Security not initialized error([#5370](https://github.com/opensearch-project/security/pull/5370))
* [Resource Sharing] Store resource sharing info in indices that map 1-to-1 with resource index ([#5358](https://github.com/opensearch-project/security/pull/5358))


## BUG FIXES


### Dashboards Assistant


* Fix unnecessary embeddable in create new dropdown ([#579](https://github.com/opensearch-project/dashboards-assistant/pull/579))
* Log error body or message instead of the entire error object ([#548](https://github.com/opensearch-project/dashboards-assistant/pull/548))
* Fix http request for insights to be triggered only after view insights button is clicked ([#520](https://github.com/opensearch-project/dashboards-assistant/pull/520))
* Fix chat page conversation loading state ([#569](https://github.com/opensearch-project/dashboards-assistant/pull/569))


### OpenSearch Alerting


* Timebox doc level monitor execution ([#1850](https://github.com/opensearch-project/alerting/pull/1850))
* Prevent dry run execution of doc level monitor with index pattern ([#1854](https://github.com/opensearch-project/alerting/pull/1854))


### OpenSearch Anomaly Detection


* Fix incorrect task state handling in ForecastRunOnceTransportAction ([#1489](https://github.com/opensearch-project/anomaly-detection/pull/1489))
* Fix incorrect task state handling in ForecastRunOnceTransportAction ([#1493](https://github.com/opensearch-project/anomaly-detection/pull/1493))
* Refine cold-start, window delay, and task updates ([#1496](https://github.com/opensearch-project/anomaly-detection/pull/1496))


### OpenSearch Anomaly Detection Dashboards


* Fix a MDS bug ([#1039](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1039))
* Improve validation, error display, and run-once state handling ([#1047](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1047))
* Surface “missing data” error in test mode ([#1050](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1050))
* Improve Create Forecaster UI and cleanup logs ([#1052](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1052))


### OpenSearch Common Utils


* Validate that index patterns are not allowed in create/update doc level monitor ([#829](https://github.com/opensearch-project/common-utils/pull/829))
* Fix is doc level monitor check ([#835](https://github.com/opensearch-project/common-utils/pull/835))


### OpenSearch Custom Codecs


* Fix version on bwc test dependency ([#255](https://github.com/opensearch-project/custom-codecs/pull/255)) ([#256](https://github.com/opensearch-project/custom-codecs/pull/256))


### OpenSearch Flow Framework


* Fixing llm field processing in RegisterAgentStep ([#1151](https://github.com/opensearch-project/flow-framework/pull/1151))
* Include exception type in WorkflowState error field even if no cause ([#1154](https://github.com/opensearch-project/flow-framework/pull/1154))
* Pass llm spec params to builder ([#1155](https://github.com/opensearch-project/flow-framework/pull/1155))


### OpenSearch Geospatial


* Reset datasource metadata when failed to update it in postIndex and postDelete to force refresh it from the primary index shard. ([#761](https://github.com/opensearch-project/geospatial/pull/761))
* Refresh the Ip2Geo cache and retry one more time when we run into an issue. ([#766](https://github.com/opensearch-project/geospatial/pull/766))


### OpenSearch Index Management


* Removed unnecessary user notifications for version conflict exceptions in Snapshot Management ([#1413](https://github.com/opensearch-project/index-management/pull/1413))


### OpenSearch ML Common


* Fix connector private IP validation when executing agent without remote model ([#3862](https://github.com/opensearch-project/ml-commons/pull/3862))
* For inline model connector name isn't required ([#3882](https://github.com/opensearch-project/ml-commons/pull/3882))
* Fix the tutorial in AIConnectorHelper when fetching domain\_url ([#3852](https://github.com/opensearch-project/ml-commons/pull/3852))
* Adds Json Parsing to nested object during update Query step in ML Inference Request processor ([#3856](https://github.com/opensearch-project/ml-commons/pull/3856))
* Adding / as a valid character ([#3854](https://github.com/opensearch-project/ml-commons/pull/3854))
* Quick fix for guava noclass issue ([#3844](https://github.com/opensearch-project/ml-commons/pull/3844))
* Fix python client not able to connect to MCP server issue ([#3822](https://github.com/opensearch-project/ml-commons/pull/3822))
* Excluding circuit breaker for Agent ([#3814](https://github.com/opensearch-project/ml-commons/pull/3814))
* Adding tenantId to the connector executor when this is inline connector ([#3837](https://github.com/opensearch-project/ml-commons/pull/3837))
* Add validation for name and description for model group and connector resources ([#3805](https://github.com/opensearch-project/ml-commons/pull/3805))
* Don't convert schema-defined strings to other types during validation ([#3761](https://github.com/opensearch-project/ml-commons/pull/3761))
* Fixed NPE for connector retrying policy ([#3909](https://github.com/opensearch-project/ml-commons/pull/3909))
* Fix tool not found in MCP memory issue ([#3931](https://github.com/opensearch-project/ml-commons/pull/3931))
* Fix: Ensure proper format for Bedrock deepseek tool result ([#3933](https://github.com/opensearch-project/ml-commons/pull/3933))


### OpenSearch Neural Search


* Fix score value as null for single shard when sorting is not done on score field ([#1277](https://github.com/opensearch-project/neural-search/pull/1277))
* Return bad request for stats API calls with invalid stat names instead of ignoring them ([#1291](https://github.com/opensearch-project/neural-search/pull/1291))
* Add validation for invalid nested hybrid query ([#1305](https://github.com/opensearch-project/neural-search/pull/1305))
* Use stack to collect semantic fields to avoid stack overflow ([#1357](https://github.com/opensearch-project/neural-search/pull/1357))
* Filter requested stats based on minimum cluster version to fix BWC tests for stats API ([#1373](https://github.com/opensearch-project/neural-search/pull/1373))
* Fix some bugs for neural query with semantic field using sparse model. ([#1396](https://github.com/opensearch-project/neural-search/pull/1396))
* Fix neural radial search serialization in multi-node clusters ([#1393](https://github.com/opensearch-project/neural-search/pull/1393)))


### OpenSearch Observability


* [Bug] Fix jaeger end time processing ([#2460](https://github.com/opensearch-project/dashboards-observability/pull/2460))
* [Integration] NFW Integration Vega Vis Warning Msg Fix ([#2452](https://github.com/opensearch-project/dashboards-observability/pull/2452))


### OpenSearch Query Insights


* Fix a bug in creating node level top queries request ([#365](https://github.com/opensearch-project/query-insights/pull/365))


### OpenSearch Query Insights Dashboards


* Fix failing cypress tests ([#206](https://github.com/opensearch-project/query-insights-dashboards/pull/206))
* Improved the proper query status with updated live query response ([#210](https://github.com/opensearch-project/query-insights-dashboards/pull/210))


### OpenSearch Search Relevance


* Update demo setup to be include ubi and ecommerce data sets and run in OS 3.1 ([#10](https://github.com/opensearch-project/search-relevance/issues/10))
* Build search request with normal parsing and wrapper query ([#22](https://github.com/opensearch-project/search-relevance/pull/22))
* Change aggregation field from `action_name.keyword` to `action_name` to fix implicit judgments calculation ([#15](https://github.com/opensearch-project/search-relevance/issues/15))
* Fix COEC calculation: introduce rank in ClickthroughRate class, fix bucket size for positional aggregation, correct COEC calculation ([#23](https://github.com/opensearch-project/search-relevance/issues/23))
* LLM Judgment Processor Improvement ([#27](https://github.com/opensearch-project/search-relevance/pull/27))
* Deal with experiment processing when no experiment variants exist ([#45](https://github.com/opensearch-project/search-relevance/pull/45))
* Enable Search Relevance backend plugin as part of running demo scripts ([#60](https://github.com/opensearch-project/search-relevance/pull/60))
* Move from Judgments being "scores" to Judgments being "ratings" ([#64](https://github.com/opensearch-project/search-relevance/pull/64))
* Added lazy index creation for all APIs ([#65](https://github.com/opensearch-project/search-relevance/pull/65))
* Extend hybrid search optimizer demo script to use models ([#69](https://github.com/opensearch-project/search-relevance/pull/69))
* Set limit for number of fields programmatically during index creation ([#74](https://github.com/opensearch-project/search-relevance/pull/74))
* Change model for Judgment entity ([#77](https://github.com/opensearch-project/search-relevance/pull/77))
* Fix judgment handling for implicit judgments to be aligned with data model for Judgment again ([#93](https://github.com/opensearch-project/search-relevance/pull/93))
* Change model for Experiment and Evaluation Result entities ([#99](https://github.com/opensearch-project/search-relevance/pull/99))
* Refactor and fix LLM judgment duplication issue ([#98](https://github.com/opensearch-project/search-relevance/pull/98))
* Add text validation and query set file size check ([#116](https://github.com/opensearch-project/search-relevance/pull/116))
* Fixed missing variants in Hybrid Optimizer ([#124](https://github.com/opensearch-project/search-relevance/pull/124))


### OpenSearch Security Analytics Dashboards


* Replace deprecated safeDump with dump ([#1281](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1281))
* Change browser to firefox, fix integ tests ([#1280](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1280))


### OpenSearch Security

* Corrections in DlsFlsFilterLeafReader regarding PointVales and object valued attributes ([#5303](https://github.com/opensearch-project/security/pull/5303))
* Fixes issue computing diffs in compliance audit log when writing to security index ([#5279](https://github.com/opensearch-project/security/pull/5279))
* Fixes dependabot broken pull_request workflow for changelog update ([#5331](https://github.com/opensearch-project/security/pull/5331))
* Fixes assemble workflow failure during Jenkins build ([#5334](https://github.com/opensearch-project/security/pull/5334))
* Fixes security index stale cache issue post snapshot restore ([#5307](https://github.com/opensearch-project/security/pull/5307))
* Only log Invalid Authentication header when HTTP Basic auth challenge is called ([#5377](https://github.com/opensearch-project/security/pull/5377))


### OpenSearch Security Dashboards Plugin


* Changes to prevent page reload on entering invalid current password and to disable reset button when current or new password is empty ([#2238](https://github.com/opensearch-project/security-dashboards-plugin/pull/2238))


### OpenSearch Skills


* Fix fields bug in PPL tool ([#581](https://github.com/opensearch-project/skills/pull/581))


### OpenSearch k-NN


* [BUGFIX] Fix KNN Quantization state cache have an invalid weight threshold [#2666](https://github.com/opensearch-project/k-NN/pull/2666)
* [BUGFIX] Fix enable rescoring when dimensions > 1000. [#2671](https://github.com/opensearch-project/k-NN/pull/2671)
* [BUGFIX] Honors slice counts for non-quantization cases [#2692](https://github.com/opensearch-project/k-NN/pull/2692)
* [BUGFIX] Block derived source enable if index.knn is false [#2702](https://github.com/opensearch-project/k-NN/pull/2702)
* Block mode and compression for indices created before version 2.17.0 [#2722](https://github.com/opensearch-project/k-NN/pull/2722)
* [BUGFIX] Avoid opening of graph file if graph is already loaded in memory [#2719](https://github.com/opensearch-project/k-NN/pull/2719)
* [BUGFIX] [Remote Vector Index Build] End remote build metrics before falling back to CPU, exception logging [#2693](https://github.com/opensearch-project/k-NN/pull/2693)
* [BUGFIX] Fix RefCount and ClearCache in some race conditions [#2728](https://github.com/opensearch-project/k-NN/pull/2728)
* [BUGFIX] Fix nested vector query at efficient filter scenarios [#2641](https://github.com/opensearch-project/k-NN/pull/2641)
* [BUGFIX] Fix memory optimized searcher to use a sliced index input [#2739](https://github.com/opensearch-project/k-NN/pull/2739)


### SQL


* Fix error when pushing down script filter with struct field ([#3693](https://github.com/opensearch-project/sql/pull/3693))
* Fix alias type referring to nested field ([#3674](https://github.com/opensearch-project/sql/pull/3674))
* Fix: Long IN-lists causes crash ([#3660](https://github.com/opensearch-project/sql/pull/3660))
* Add a trimmed project before aggregate to avoid NPE in Calcite ([#3621](https://github.com/opensearch-project/sql/pull/3621))
* Fix field not found issue in join output when column names are ambiguous ([#3760](https://github.com/opensearch-project/sql/pull/3760))
* Fix: correct ATAN(x, y) and CONV(x, a, b) functions bug ([#3748](https://github.com/opensearch-project/sql/pull/3748))
* Return double with correct precision for `UNIX_TIMESTAMP` ([#3679](https://github.com/opensearch-project/sql/pull/3679))
* Prevent push down limit with offset reach maxResultWindow ([#3713](https://github.com/opensearch-project/sql/pull/3713))
* Fix pushing down filter with nested filed of the text type ([#3645](https://github.com/opensearch-project/sql/pull/3645))
* Make query.size\_limit only affect the final results ([#3623](https://github.com/opensearch-project/sql/pull/3623))
* Revert stream pattern method in V2 and implement SIMPLE\_PATTERN in Calcite ([#3553](https://github.com/opensearch-project/sql/pull/3553))
* Remove the duplicated timestamp row in data type mapping table ([#2617](https://github.com/opensearch-project/sql/pull/2617))


## INFRASTRUCTURE


### Dashboards Assistant


* Fix(ci): fixed failed ci due to path alias ([#580](https://github.com/opensearch-project/dashboards-assistant/pull/580))


### OpenSearch Anomaly Detection Dashboards


* Update `@testing-library/user-event` dependency ([#1042](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1042))


### OpenSearch Flow Framework


* Conditionally include ddb-client dependency only if env variable set ([#1141](https://github.com/opensearch-project/flow-framework/issues/1141))


### OpenSearch Job Scheduler


* Add a CHANGELOG and changelog\_verifier workflow ([#778](https://github.com/opensearch-project/job-scheduler/pull/778)).


### OpenSearch ML Common


* Change release note ([#3811](https://github.com/opensearch-project/ml-commons/pull/3811))
* Update the maven snapshot publish endpoint and credential ([#3929](https://github.com/opensearch-project/ml-commons/pull/3929))


### OpenSearch Neural Search


* [3.0] Update neural-search for OpenSearch 3.0 beta compatibility ([#1245](https://github.com/opensearch-project/neural-search/pull/1245))


### OpenSearch Observability


* Workflows - Version bump to 3.1.0 ([#2451](https://github.com/opensearch-project/dashboards-observability/pull/2451))


### OpenSearch Query Insights Dashboards


* Fix version mismatch between OpenSearch and Dashboards in CI binary installation workflow ([#205](https://github.com/opensearch-project/query-insights-dashboards/pull/205))


### OpenSearch Remote Metadata Sdk


* CVE fix for CVE-2025-27820 [#195](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/195)


### OpenSearch Search Relevance



* Run integTests with security as a PR check ([#136](https://github.com/opensearch-project/search-relevance/pull/136))
* Realistic test data set based on ESCI (products, queries, judgements) ([#70](https://github.com/opensearch-project/search-relevance/pull/70))


### OpenSearch k-NN


* Add testing support to run all ITs with remote index builder [#2659](https://github.com/opensearch-project/k-NN/pull/2659)
* Fix KNNSettingsTests after change in MockNode constructor [#2700](https://github.com/opensearch-project/k-NN/pull/2700)


## DOCUMENTATION


### OpenSearch ML Common


* Replace the usage of elasticsearch with OpenSearch in README ([#3876](https://github.com/opensearch-project/ml-commons/pull/3876))
* Added blueprint for Bedrock Claude v4 ([#3871](https://github.com/opensearch-project/ml-commons/pull/3871))


## MAINTENANCE


### Dashboards Assistant


* Bump version to 3.1.0.0 ([#572](https://github.com/opensearch-project/dashboards-assistant/pull/572))


### OpenSearch Alerting


* [AUTO] Increment version to 3.1.0-SNAPSHOT ([#1837](https://github.com/opensearch-project/alerting/pull/1837))


### OpenSearch Alerting Dashboards Plugin


* Upgrade java version to 21 for binary ci ([#1249](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1249))
* Increment version to 3.1.0.0 ([#1251](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1251))
* Add error handling for extract log pattern ([#1256](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1256))


### OpenSearch Asynchronous Search


* Increment version to 3.1.0 ([#726](https://github.com/opensearch-project/asynchronous-search/pull/726))


### OpenSearch Common Utils


* [AUTO] Increment version to 3.1.0-SNAPSHOT ([#820](https://github.com/opensearch-project/common-utils/pull/820))


### OpenSearch Dashboards Maps


* Increment version to 3.1.0.0 [#735](https://github.com/opensearch-project/dashboards-maps/pull/735)


### OpenSearch Dashboards Notifications


* Increment version to 3.1.0.0. ([#357](https://github.com/opensearch-project/dashboards-notifications/pull/357))


### OpenSearch Dashboards Reporting


* Increment version to 3.1.0.0 ([#579](https://github.com/opensearch-project/dashboards-reporting/pull/579))
* Adding release notes for 3.1.0 ([#587](https://github.com/opensearch-project/dashboards-reporting/pull/587))


### OpenSearch Dashboards Search Relevance


* Increment version to 3.1.0.0 ([#534](https://github.com/opensearch-project/dashboards-search-relevance/pull/534))
* Fix schema validation in POST Query Sets endpoint ([#542](https://github.com/opensearch-project/dashboards-search-relevance/pull/542))


### OpenSearch Flow Framework


* Feat: add data summary with log pattern agent template ([#1137](https://github.com/opensearch-project/flow-framework/pull/1137))


### OpenSearch Flow Framework Dashboards


* Remove legacy tutorial doc ([#747](https://github.com/opensearch-project/dashboards-flow-framework/pull/747))


### OpenSearch Geospatial


* Fix a unit test and update github workflow to use actions/setup-java@v3.


### OpenSearch Index Management


* [AUTO] Increment version to 3.1.0-SNAPSHOT ([#1414](https://github.com/opensearch-project/index-management/pull/1414))


### OpenSearch Index Management Dashboards Plugin


* Increment version to 3.1.0.0 ([#1313](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1313))
* Updated @testing-library/user-event dependency ([#1321](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1321))


### OpenSearch Job Scheduler


* Increment version to 3.1.0 ([#766](https://github.com/opensearch-project/job-scheduler/pull/766)).
* Remove guava dependency ([#770](https://github.com/opensearch-project/job-scheduler/pull/770)).


### OpenSearch ML Common


* [Code Quality] Adding test cases for PlanExecuteReflect Agent ([#3778](https://github.com/opensearch-project/ml-commons/pull/3778))
* Add Unit Tests for MCP feature ([#3787](https://github.com/opensearch-project/ml-commons/pull/3787))
* Exclude trusted connector check for hidden model ([#3838](https://github.com/opensearch-project/ml-commons/pull/3838))
* Add more logging to deploy/undeploy flows for better debugging ([#3825](https://github.com/opensearch-project/ml-commons/pull/3825))
* Remove libs folder ([#3824](https://github.com/opensearch-project/ml-commons/pull/3824))
* Downgrade MCP version to 0.9 ([#3821](https://github.com/opensearch-project/ml-commons/pull/3821))
* Upgrade http client to version align with core ([#3809](https://github.com/opensearch-project/ml-commons/pull/3809))
* Use stream optional enum set from core in MLStatsInput ([#3648](https://github.com/opensearch-project/ml-commons/pull/3648))
* Change SearchIndexTool arguments parsing logic ([#3883](https://github.com/opensearch-project/ml-commons/pull/3883))
* Force runtime class path commons-beanutils:commons-beanutils:1.11.0 to avoid transitive dependency ([#3935](https://github.com/opensearch-project/ml-commons/pull/3935))


### OpenSearch ML Commons Dashboards


* Bump version to 3.1.0.0 ([#426](https://github.com/opensearch-project/ml-commons-dashboards/pull/426))


### OpenSearch Neural Search


* Update Lucene dependencies ([#1336](https://github.com/opensearch-project/neural-search/pull/1336))


### OpenSearch Notifications


* Upgrade javax to jakarta to avoid version conflicts ([#1036](https://github.com/opensearch-project/notifications/pull/1036))
* Increment version to 3.1.0-SNAPSHOT ([#1027](https://github.com/opensearch-project/notifications/pull/1027))


### OpenSearch Observability


* Increment version to 3.1.0.0 ([#2443](https://github.com/opensearch-project/dashboards-observability/pull/2443))
* Adding release notes for 3.1.0 ([#2464](https://github.com/opensearch-project/dashboards-observability/pull/2464))


### OpenSearch Observability


* [AUTO] Increment version to 3.1.0-SNAPSHOT ([#1922](https://github.com/opensearch-project/observability/pull/1922))


* Adding release notes for 3.1.0 ([#1929](https://github.com/opensearch-project/observability/pull/1929))


### OpenSearch Learning To Rank Base


* Lucene 10.2 upgrade changes ([#186](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/186))


### OpenSearch Query Insights


* Fix flaky integ tests ([#364](https://github.com/opensearch-project/query-insights/pull/364))


### OpenSearch Query Insights Dashboards


* Increment version to 3.1.0.0 ([#194](https://github.com/opensearch-project/query-insights-dashboards/pull/194))


### OpenSearch Query Workbench


* Increment version to 3.1.0.0 ([#475](https://github.com/opensearch-project/dashboards-query-workbench/pull/475))
* Adding release notes for 3.1.0 ([#482](https://github.com/opensearch-project/dashboards-query-workbench/pull/482))


### OpenSearch Reporting


* [AUTO] Increment version to 3.1.0-SNAPSHOT ([#1092](https://github.com/opensearch-project/reporting/pull/1092))
* Adding release notes for 3.1.0 ([#1101]https://github.com/opensearch-project/reporting/pull/1101)


### OpenSearch Security


* Add forecast roles and permissions ([#5386](https://github.com/opensearch-project/security/pull/5386))
* Add missing cluster:monitor permission ([#5405](https://github.com/opensearch-project/security/pull/5405))
* Add missing mapping get permission ([#5412](https://github.com/opensearch-project/security/pull/5412))
* Bump `guava_version` from 33.4.6-jre to 33.4.8-jre ([#5284](https://github.com/opensearch-project/security/pull/5284))
* Bump `spring_version` from 6.2.5 to 6.2.7 ([#5283](https://github.com/opensearch-project/security/pull/5283), [#5345](https://github.com/opensearch-project/security/pull/5345))
* Bump `com.google.errorprone:error_prone_annotations` from 2.37.0 to 2.38.0 ([#5285](https://github.com/opensearch-project/security/pull/5285))
* Bump `org.mockito:mockito-core` from 5.15.2 to 5.18.0 ([#5296](https://github.com/opensearch-project/security/pull/5296), [#5362](https://github.com/opensearch-project/security/pull/5362))
* Bump `com.carrotsearch.randomizedtesting:randomizedtesting-runner` from 2.8.2 to 2.8.3 ([#5294](https://github.com/opensearch-project/security/pull/5294))
* Bump `org.ow2.asm:asm` from 9.7.1 to 9.8 ([#5293](https://github.com/opensearch-project/security/pull/5293))
* Bump `commons-codec:commons-codec` from 1.16.1 to 1.18.0 ([#5295](https://github.com/opensearch-project/security/pull/5295))
* Bump `net.bytebuddy:byte-buddy` from 1.15.11 to 1.17.5 ([#5313](https://github.com/opensearch-project/security/pull/5313))
* Bump `org.awaitility:awaitility` from 4.2.2 to 4.3.0 ([#5314](https://github.com/opensearch-project/security/pull/5314))
* Bump `org.springframework.kafka:spring-kafka-test` from 3.3.4 to 3.3.5 ([#5315](https://github.com/opensearch-project/security/pull/5315))
* Bump `com.fasterxml.jackson.core:jackson-databind` from 2.18.2 to 2.19.0 ([#5292](https://github.com/opensearch-project/security/pull/5292))
* Bump `org.apache.commons:commons-collections4` from 4.4 to 4.5.0 ([#5316](https://github.com/opensearch-project/security/pull/5316))
* Bump `com.google.googlejavaformat:google-java-format` from 1.26.0 to 1.27.0 ([#5330](https://github.com/opensearch-project/security/pull/5330))
* Bump `io.github.goooler.shadow` from 8.1.7 to 8.1.8 ([#5329](https://github.com/opensearch-project/security/pull/5329))
* Bump `commons-io:commons-io` from 2.18.0 to 2.19.0 ([#5328](https://github.com/opensearch-project/security/pull/5328))
* Upgrade kafka_version from 3.7.1 to 4.0.0 ([#5131](https://github.com/opensearch-project/security/pull/5131))
* Bump `io.dropwizard.metrics:metrics-core` from 4.2.30 to 4.2.32 ([#5361](https://github.com/opensearch-project/security/pull/5361))
* Bump `org.junit.jupiter:junit-jupiter` from 5.12.2 to 5.13.1 ([#5371](https://github.com/opensearch-project/security/pull/5371), [#5382](https://github.com/opensearch-project/security/pull/5382))
* Bump `bouncycastle_version` from 1.80 to 1.81 ([#5380](https://github.com/opensearch-project/security/pull/5380))
* Bump `org.junit.jupiter:junit-jupiter-api` from 5.13.0 to 5.13.1 ([#5383](https://github.com/opensearch-project/security/pull/5383))
* Bump `org.checkerframework:checker-qual` from 3.49.3 to 3.49.4 ([#5381](https://github.com/opensearch-project/security/pull/5381))


### OpenSearch Security Analytics


* Switch guava deps from compileOnly to implementation ([#1530](https://github.com/opensearch-project/security-analytics/pull/1530))
* Increment version to 3.1.0-SNAPSHOT ([#1517](https://github.com/opensearch-project/security-analytics/pull/1517))


### OpenSearch Security Analytics Dashboards


* Increment version to 3.1.0.0. ([#1301](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1301))


### OpenSearch Security Dashboards Plugin


* Adds forecasting transport actions to the static dropdown list ([#2253](https://github.com/opensearch-project/security-dashboards-plugin/pull/2253))
* Bump dev dependencies to resolve CVE-2024-52798 ([#2231](https://github.com/opensearch-project/security-dashboards-plugin/pull/2231))


### OpenSearch Skills


* Fix conflict in dependency versions ([#575](https://github.com/opensearch-project/skills/pull/575))
* Fix mode deploy failure due to ml-commons update ([#588](https://github.com/opensearch-project/skills/pull/588))


### SQL


* Migrate existing UDFs to PPLFuncImpTable ([#3576](https://github.com/opensearch-project/sql/pull/3576))
* Modified workflow: Grammar Files & Async Query Core ([#3715](https://github.com/opensearch-project/sql/pull/3715))
* Bump setuptools to 78.1.1 ([#3671](https://github.com/opensearch-project/sql/pull/3671))
* Update PPL Limitation Docs ([#3656](https://github.com/opensearch-project/sql/pull/3656))
* Create a new directory org/opensearch/direct-query/ ([#3649](https://github.com/opensearch-project/sql/pull/3649))
* Implement Parameter Validation for PPL functions on Calcite ([#3626](https://github.com/opensearch-project/sql/pull/3626))
* Add a TPC-H PPL query suite ([#3622](https://github.com/opensearch-project/sql/pull/3622))


## REFACTORING


### OpenSearch k-NN


* Refactor Knn Search Results to use TopDocs [#2727](https://github.com/opensearch-project/k-NN/pull/2727)


