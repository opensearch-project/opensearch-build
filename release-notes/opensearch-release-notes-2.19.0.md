# OpenSearch and OpenSearch Dashboards 2.19.0 Release Notes

## Release Highlights

OpenSearch 2.19 includes a number of updates that help you build machine learning (ML)-powered applications, increase performance and stability, and improve the way you and your teams collaborate using OpenSearch.


#### NEW AND UPDATED FEATURES

* OpenSearch Flow helps developers build ML-powered applications, including generative AI applications, more quickly using OpenSearch Dashboards. Custom flows can be composed to support a range of use cases, such as retrieval-augmented generation and vector search applications.

* Binary vector functionality offers an efficient alternative to FP32 vectors, delivering a more than 90% reduction in memory and storage requirements while maintaining performance. This release adds support for Lucene binary vectors, complementing existing Faiss engine binary vector support.

* Cosine similarity support in the Faiss engine for k-NN and radial search eliminates the need for manual data normalization, offering benefits for use cases such as recommendation systems, fraud detection, and content-based search applications.

* Enhanced hybrid search introduces the `pagination_depth `parameter for improved management of large result sets.

* Reciprocal rank fusion provides an alternative approach to result combination that uses the positions or ranks of the documents rather than relying on their scores.

* The new `hybrid_score_explanation` processor offers debugging and troubleshooting capabilities for hybrid search operations, offering insights into score normalization and combination processes for search responses.

* A new version of the Faiss library adds advanced AVX-512 Single Instruction Multiple Data (SIMD) instructions for newer-generation processors, available on public clouds such as AWS for c/m/r 7i or newer instances. These SIMD instructions improve the query performance of binary vectors.

* The expanding library of search pipeline processors can make it challenging to track data through processors. A `verbose_pipeline` parameter for search pipelines provides a new tool for visualizing the flow of data across these processors, supporting troubleshooting, optimizing pipeline configurations, and providing transparency for search requests and responses.

* ML inference search request extensions allow you to pass additional input fields during search queries, making search requests more adaptable to different ML models and enhancing prediction capabilities during search operations.

* Feature-level anomaly detection now enables precise configuration of spike or dip detection for individual metrics, providing more targeted monitoring of specific data patterns across system resources.

* A new structured index architecture for anomaly detection results transforms values such as entity values and arrays into flattened formats, improving dashboard visualizations and query efficiency.

* Query insights dashboards introduces a new interface for monitoring and analyzing top N queries, with visualizations for historical data integration, detailed drill-down analysis, and streamlined retention management with configurable data expiration.

* A new mechanism used by plugins to access metadata  simplifies system index access, offering stronger security controls for privileged operations.

* New concurrency optimizations enable OpenSearch to download graph files in parallel so that they are ready to be loaded into the native memory cache. This enhances performance for remote-backed storage and searchable snapshot workloads, where the data is not readily available on disk.

* Filter performance is improved with the addition of a simple check in the `searchLeaf` query method that identifies whether the filters match all of the doc IDs in the segment. If confirmed, OpenSearch will proceed directly with ANN search and avoid unnecessary steps.

* Script scoring for k-NN binary vectors in Hamming space is optimized by eliminating unnecessary type conversions between `byte` and `float` arrays.

* Further performance optimizations include constant-time privilege evaluation and cost-based bitmap filtering selection, delivering improvements in query efficiency and cost.

* Users are no longer able to specify both the model ID and dimension in an index creation request. When the model ID is provided, k-NN search will refer to the dimension from the training index instead of the user-defined dimension in the mapping request body.

* The `fields` parameter is now supported for searches on knn_vector fields so that users will no longer experience failures when running searches using the `fields` parameter on indexes with a knn_vector field.

* A fix to the `rescore` parameter enables users to disable the rescore step when setting this parameter to `false` for searches of knn_vector fields.

* Updates to the index.knn setting fixed an issue whereby users could update the setting after an index had been created.

* Updates provide more detailed error messaging/validation for Faiss training than was previously available, which made it difficult to debug product quantization (PQ) and inverted file system (IVF). The enhancement provides improved error messages by adding explicit checks for the most common errors that cover 90% of training failures that occur.

* Updates to k-NN functionality ensure consistent results across filter queries that previously provided incorrect results.

* OpenSearch plugins traditionally store metadata in system indexes, which can lead to challenges related to version compatibility, resource constraints, and single-tenant limitations. This release introduces a repository wrapper that transitions plugin metadata from system indexes to stateless OpenSearch nodes using external storage like remote OpenSearch clusters or cloud providers.

* Multi-tenancy is available for key plugins like ML Commons and Flow Framework, enabling logical resource separation by tenant ID. This enables cloud providers to conceptualize plugins as a service to support delivery of scalable multi-tenant solutions.

* A built-in multimodal preprocessor function for Cohere lets users create a connector by providing a function name, simplifying development and avoiding complex Painless scripts.

* An enhancement to the conversational agent allows users to build tools using large language model (LLM)-generated inputs as search parameters.

* A new Learning to Rank plugin enhances search relevance by incorporating ML and behavioral data. It leverages lightweight ML models like XGBoost and RankLib to rescore search results, considering multiple factors in the ranking process to significantly improve the accuracy and relevance of results.

* A new `template` query type introduces placeholder variables in search queries that remain unresolved until a search request processor assigns their value, enabling more dynamic and secure search operations.


#### EXPERIMENTAL FEATURES

OpenSearch 2.19 includes the following experimental functionality. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.

* The experimental Discover view now supports the SQL and Piped Processing Language (PPL) query languages in addition to Dashboards Query Language (DQL) and Lucene, along with new autocomplete functionality and improved data selection to provide a more flexible and efficient query experience.

* Star-tree aggregation adds support for metric aggregations and date histograms with metric aggregations, delivering up to 100x query reduction and 30x lower cache utilization, with optimized binary search for multiple `terms` queries.

* Improvements to disk-tiered request cache performance divide the cache into multiple partitions, each protected by its own read/write lock, enabling multiple concurrent readers to access data without contention and multiple writers to operate simultaneously, providing higher write throughput.

* Experimental derived source functionality for k-NN vectors optimizes storage by removing vectors from the JSON source and dynamically injecting them when needed, supporting flat vector mappings, object fields, and single-level nested fields.

#### DEPRECATION NOTICES

**Deprecating support for Ubuntu Linux 20.04**
Please note that OpenSearch will deprecate support for Ubuntu Linux 20.04 as a continuous integration build image and supported operating system in an upcoming version, as Ubuntu Linux 20.04 will reach end-of-life with standard support as of April 2025 (refer to [this notice](https://ubuntu.com/blog/ubuntu-20-04-lts-end-of-life-standard-support-is-coming-to-an-end-heres-how-to-prepare) from Canonical Ubuntu). For a list of OpenSearch's compatible operating systems, [visit here](https://opensearch.org/docs/latest/install-and-configure/os-comp/).

**Deprecating support for features and plugins in OpenSearch 3.0.0**
Please note that OpenSearch and OpenSearch Dashboards will deprecate support for the following features and plugins in [OpenSearch 3.0.0](https://github.com/opensearch-project/opensearch-build/issues/3747):

* [Performance-Analyzer-Rca](https://github.com/opensearch-project/performance-analyzer-rca/issues/591): Will be replaced with the [Telemetry plugin](https://github.com/opensearch-project/performance-analyzer/issues/585).
* [Dashboards-Visualizations](https://github.com/opensearch-project/dashboards-visualizations/issues/430) (ganttCharts): Plugin will be removed as part of the OpenSearch Dashboards bundle artifact.
* [Dashboards-Observability](https://github.com/opensearch-project/dashboards-observability/issues/2311): Support will be removed for legacy notebooks from observability indexes.
* [SQL](https://github.com/opensearch-project/sql/issues/3248): OpenSearch 3.0.0 will deprecate the OpenSearch DSL format as well as several settings, remove the SparkSQL connector, and remove DELETE statement support in SQL.
* [k-NN](https://github.com/opensearch-project/k-NN/issues/2396): OpenSearch 3.0.0 will deprecate the NMSLIB engine. Users will be advised to use the Faiss or Lucene engines instead.


## Release Details
[OpenSearch and OpenSearch Dashboards 2.19.0](https://opensearch.org/versions/opensearch-2-19-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.0.md).


## FEATURES


### Dashboards Assistant


* Introduces Pipeline to execute asynchronous operations ([#376](https://github.com/opensearch-project/dashboards-assistant/pull/376))


* Add flags in the config to control trace view and feedback buttons in message bubbles ([#379](https://github.com/opensearch-project/dashboards-assistant/pull/379))
* Feat: only support visual editor alerts to navigate to discover([#368](https://github.com/opensearch-project/dashboards-assistant/pull/368))
* Feat: return 404 instead of 500 for missing agent config name([#384](https://github.com/opensearch-project/dashboards-assistant/pull/384))
* Feat: Update UI for In-context summarization in Alerts table([#392](https://github.com/opensearch-project/dashboards-assistant/pull/392))
* Feat: Hide "stop generation" and regenerate button based on feature flag([#394](https://github.com/opensearch-project/dashboards-assistant/pull/394))
* Feat: Chatbot entry UI redesign([#396](https://github.com/opensearch-project/dashboards-assistant/pull/396))
* Feat: Set logo config in assistant and read logo by config([#401](https://github.com/opensearch-project/dashboards-assistant/pull/401))
* Feat: Update dropdown list button label and remove popover title([#407](https://github.com/opensearch-project/dashboards-assistant/pull/407))
* Feat: Use feature flag to disable the delete conversation api([#409](https://github.com/opensearch-project/dashboards-assistant/pull/409))
* Feat: Disable the rename conversation api using feature flag([#410](https://github.com/opensearch-project/dashboards-assistant/pull/410))
* Add query assistant summary to the assistant dropdown list ([#395](https://github.com/opensearch-project/dashboards-assistant/pull/395))


### Opensearch Anomaly Detection


* Allow triggering anomaly only on drop or rise of features ([#1358](https://github.com/opensearch-project/anomaly-detection/pull/1358))
* Add flattens custom result index when enabled ([#1401](https://github.com/opensearch-project/anomaly-detection/pull/1401)), ([#1409](https://github.com/opensearch-project/anomaly-detection/pull/1409))


### Opensearch Anomaly Detection Dashboards


* Add feature direction and moving suppression rules to each feature ([#960](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/960))


### Opensearch Flow Framework


* Add multitenant remote metadata client ([#980](https://github.com/opensearch-project/flow-framework/pull/980))


* Add synchronous execution option to workflow provisioning ([#990](https://github.com/opensearch-project/flow-framework/pull/990))


### Opensearch Geospatial


* Introduce new Java artifact geospatial-client to facilitate cross plugin communication. ([#700](https://github.com/opensearch-project/geospatial/pull/700))


### Opensearch Neural Search


* Pagination in Hybrid query ([#1048](https://github.com/opensearch-project/neural-search/pull/1048))
* Implement Reciprocal Rank Fusion score normalization/combination technique in hybrid query ([#874](https://github.com/opensearch-project/neural-search/pull/874))


### Opensearch Observability


* Remove the maxFilesPerTrigger limits for VPC MV ([#2318](https://github.com/opensearch-project/dashboards-observability/pull/2318))


* Gantt chart / Span list rework ([#2283](https://github.com/opensearch-project/dashboards-observability/pull/2283))
* Update redirection/Focus field rework ([#2264](https://github.com/opensearch-project/dashboards-observability/pull/2264))
* Notebooks updates ([#2255](https://github.com/opensearch-project/dashboards-observability/pull/2255))
* Overview page add state for missing data source ([#2237](https://github.com/opensearch-project/dashboards-observability/pull/2237))
* Service map updates ([#2230](https://github.com/opensearch-project/dashboards-observability/pull/2230))


### Opensearch Remote Metadata Sdk


* Initial release of OpenSearch Remote Metadata SDK for Java


### Opensearch Skills


* Add CreateAlertTool ([#456](https://github.com/opensearch-project/skills/pull/456))


### Opensearch k-NN


* Add Support for Multi Values in innerHit for Nested k-NN Fields in Lucene and FAISS ([#2283](https://github.com/opensearch-project/k-NN/pull/2283))


* Add binary index support for Lucene engine. ([#2292](https://github.com/opensearch-project/k-NN/pull/2292))
* Add expand\_nested\_docs Parameter support to NMSLIB engine ([#2331](https://github.com/opensearch-project/k-NN/pull/2331))
* Add a new build mode, `FAISS_OPT_LEVEL=avx512_spr`, which enables the use of advanced AVX-512 instructions introduced with Intel[R] Sapphire Rapids ([#2404](https://github.com/opensearch-project/k-NN/pull/2404))
* Add cosine similarity support for faiss engine [(#2376](https://github.com/opensearch-project/k-NN/pull/2376))
* Add concurrency optimizations with native memory graph loading and force eviction ([#2265](https://github.com/opensearch-project/k-NN/pull/2345))
* Add derived source feature for vector fields ([#2449](https://github.com/opensearch-project/k-NN/pull/2449))


### Opensearch SQL


* Call updateState when query is cancelled ([#3139](https://github.com/opensearch-project/sql/pull/3139))


## ENHANCEMENTS


### Opensearch Anomaly Detection


* Changing replica count to up 2 for custom result index ([#1362](https://github.com/opensearch-project/anomaly-detection/pull/1362))


### Opensearch Anomaly Detection Dashboards


* Do not show suggestAD action if the data source has no AI agent ([#901](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/901))
* Update vis augmenter eligibility fn to async ([#938](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/938))


### Opensearch Index Management


* Use adminClient when searching system index in integ tests ([#1286](https://github.com/opensearch-project/index-management/pull/1286))


### Opensearch Index Management Dashboards Plugin


* Use cat snapshot to get the number of snapshot for a repo ([#1242](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1242))


### Opensearch Job Scheduler


* Run Rest Integ Tests with the Security plugin installed ([#645](https://github.com/opensearch-project/job-scheduler/pull/645)) ([#712](https://github.com/opensearch-project/job-scheduler/pull/712)).
* Fetch certs from security repo and remove locally checked in demo certs ([#713](https://github.com/opensearch-project/job-scheduler/pull/713)) ([#718](https://github.com/opensearch-project/job-scheduler/pull/718)).


### Opensearch ML Commons


* Adding multi-modal pre-processor for cohere ([3219](https://github.com/opensearch-project/ml-commons/pull/3219))
* [Enhancement] Fetch system index mappings from json file instead of string constants ([3153](https://github.com/opensearch-project/ml-commons/pull/3153))
* Retrieve remote model id from registration response in IT to avoid flaky ([3244](https://github.com/opensearch-project/ml-commons/pull/3244))
* [Refactor] Remove bloat due to unnecessary setup in test and add retry for potential flaky behavior due to timeout ([3259](https://github.com/opensearch-project/ml-commons/pull/3259/files))
* [Enhancement] Enhance validation for create connector API ([3260](https://github.com/opensearch-project/ml-commons/pull/3260))
* Add application_type to ConversationMeta; update tests ([3282](https://github.com/opensearch-project/ml-commons/pull/3282))
* Enhance Message and Memory API Validation and storage ([3283](https://github.com/opensearch-project/ml-commons/pull/3283))
* Use Adagrad optimiser for Linear regression by default ([3291](https://github.com/opensearch-project/ml-commons/pull/3291/files))
* [Enhancement] Add schema validation and placeholders to index mappings ([3240](https://github.com/opensearch-project/ml-commons/pull/3240))
* add action input as parameters for tool execution in conversational agent ([3200](https://github.com/opensearch-project/ml-commons/pull/3200))
* Remove ignore decorator for testCohereClassifyModel ([3324](https://github.com/opensearch-project/ml-commons/pull/3324))
* refactor: modifying log levels and adding more logs to display error details ([3337](https://github.com/opensearch-project/ml-commons/pull/3337))
* Primary setup for Multi-tenancy ([3307](https://github.com/opensearch-project/ml-commons/pull/3307))
* Apply multi-tenancy and sdk client in Connector (Create + Get + Delete) ([3382](https://github.com/opensearch-project/ml-commons/pull/3382))
* Adding multi-tenancy + sdk client related changes to model, model group and connector update ([3399](https://github.com/opensearch-project/ml-commons/pull/3399))
* Applying multi-tenancy to task apis, deploy, predict apis ([3416](https://github.com/opensearch-project/ml-commons/pull/3416))
* Adding tenantID to the request + undeploy request ([3425](https://github.com/opensearch-project/ml-commons/pull/3425))
* Check before delete ([3209](https://github.com/opensearch-project/ml-commons/pull/3209))
* Multi-tenancy + sdk client related changes in agents ([3432](https://github.com/opensearch-project/ml-commons/pull/3432))
* Introduce Ml Inference Search Request Extension ([3284](https://github.com/opensearch-project/ml-commons/pull/3284))
* Cherry-pick BWC fix for system prompt and user instructions ([3437](https://github.com/opensearch-project/ml-commons/pull/3437))
* Add deepseek as a trusted endpoint. ([3440](https://github.com/opensearch-project/ml-commons/pull/3440))
* Applying multi-tenancy in search [model, model group, agent, connector] ([3433](https://github.com/opensearch-project/ml-commons/pull/3433))
* Added amazon rekognition as a trust endpoint ([3419](https://github.com/opensearch-project/ml-commons/pull/3419))
* Adding multi-tenancy to config api and master key related changes ([3439](https://github.com/opensearch-project/ml-commons/pull/3439))
* Undeploy models with no WorkerNodes ([3380](https://github.com/opensearch-project/ml-commons/pull/3380))
* Support batch task management by periodically bolling the remote task via a cron job ([3421](https://github.com/opensearch-project/ml-commons/pull/3421))
* Add pre and post process functions for Bedrock Rerank API #3254 ([3339](https://github.com/opensearch-project/ml-commons/pull/3339))
* [Backport 2.19] [BACKPORT 2.x] applying multi-tenancy in search [model, model group, agent, connector] (#3433) ([3469](https://github.com/opensearch-project/ml-commons/pull/3469))
* [Backport 2.19] fixing connector validation ([3471](https://github.com/opensearch-project/ml-commons/pull/3471))
* [BACKPORT 2.x] applying multi-tenancy in search [model, model group, agent, connector] (#3433) (#3443) ([3469](https://github.com/opensearch-project/ml-commons/pull/3469))

### Opensearch Neural Search


* Explainability in hybrid query ([#970](https://github.com/opensearch-project/neural-search/pull/970))
* Support new knn query parameter expand\_nested ([#1013](https://github.com/opensearch-project/neural-search/pull/1013))
* Implement pruning for neural sparse ingestion pipeline and two phase search processor ([#988](https://github.com/opensearch-project/neural-search/pull/988))
* Support empty string for fields in text embedding processor ([#1041](https://github.com/opensearch-project/neural-search/pull/1041))
* Optimize ML inference connection retry logic ([#1054](https://github.com/opensearch-project/neural-search/pull/1054))
* Support for builder constructor in Neural Query Builder ([#1047](https://github.com/opensearch-project/neural-search/pull/1047))
* Validate Disjunction query to avoid having nested hybrid query ([#1127](https://github.com/opensearch-project/neural-search/pull/1127))


### Opensearch Opensearch Learning To Rank Base


* Add .ltrstore\* as system index and configure test suite to add Permissions to delete system indices ([#125](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/125))
* Feat: implemented rest endpoint to make stats available ([#90](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/90))
* Supplier plugin health and store usage after revert (([#89](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/89))
* Collect stats for usage and health ([#79](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/79))
* Implemented Settings ([#76](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/76))
* Feat: Implemented circuit breaker ([#71](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/71))


### Opensearch Query Insights


* Usage counter for Top N queries ([#153](https://github.com/opensearch-project/query-insights/pull/153))
* Add type attribute to search query record ([#157](https://github.com/opensearch-project/query-insights/pull/157))
* Make default window size valid for all metric types ([#156](https://github.com/opensearch-project/query-insights/pull/156))
* Top N indices auto deletion config & functionality ([#172](https://github.com/opensearch-project/query-insights/pull/172))
* Make sure query\_group\_hashcode is present in top\_queries response in all cases ([#187](https://github.com/opensearch-project/query-insights/pull/187))
* Model changes for hashcode and id ([#191](https://github.com/opensearch-project/query-insights/pull/191))
* Add fetch top queries by id API ([#195](https://github.com/opensearch-project/query-insights/pull/195))
* Add field type cache stats ([#193](https://github.com/opensearch-project/query-insights/pull/193))
* Always collect available metrics in top queries service ([#205](https://github.com/opensearch-project/query-insights/pull/205))
* Refactor Exporters and Readers ([#210](https://github.com/opensearch-project/query-insights/pull/210))


### Opensearch Query Insights Dashboards


* Top n queries overview page ([#7](https://github.com/opensearch-project/query-insights-dashboards/pull/7))
* Top n queries configuration page ([#8](https://github.com/opensearch-project/query-insights-dashboards/pull/8))
* Top n queries connected to api ([#10](https://github.com/opensearch-project/query-insights-dashboards/pull/10))
* Top n queries query details page ([#9](https://github.com/opensearch-project/query-insights-dashboards/pull/9))
* Remove records with grouping ([#26](https://github.com/opensearch-project/query-insights-dashboards/pull/26))
* Make sure API configuration changes are reflected on the UI ([#28](https://github.com/opensearch-project/query-insights-dashboards/pull/28))
* Revert "remove records with grouping ([#32](https://github.com/opensearch-project/query-insights-dashboards/pull/32))
* Cypress tests set up with e2e tests for all pages ([#34](https://github.com/opensearch-project/query-insights-dashboards/pull/34))
* Fix table strings and add unit tests ([#25](https://github.com/opensearch-project/query-insights-dashboards/pull/25))
* Query grouping dashboard changes and extensive tests ([#33](https://github.com/opensearch-project/query-insights-dashboards/pull/33))
* Cypress tests for query grouping ([#55](https://github.com/opensearch-project/query-insights-dashboards/pull/55))
* Changes to conform to new navigation and page header when feature flag enabled ([#60](https://github.com/opensearch-project/query-insights-dashboards/pull/60))
* Query/group details make API call to fetch data ([#63](https://github.com/opensearch-project/query-insights-dashboards/pull/63))
* MDS support for query insights dashboards ([#71](https://github.com/opensearch-project/query-insights-dashboards/pull/71))
* Add configuration section for exporter and delete\_after ([#53](https://github.com/opensearch-project/query-insights-dashboards/pull/53))
* Version decoupling and tests for MDS ([#74](https://github.com/opensearch-project/query-insights-dashboards/pull/74))


### Opensearch Security


* Allow skipping hot reload dn validation ([#4839](https://github.com/opensearch-project/security/pull/4839))
* Add validation of authority certificates ([#4862](https://github.com/opensearch-project/security/pull/4862))
* Add support for certificates hot reload ([#4880](https://github.com/opensearch-project/security/pull/4880))
* Optimize privilege evaluation for index permissions across '\*' index pattern (i.e. all\_access role) ([#4926](https://github.com/opensearch-project/security/pull/4926))
* Refactor SafeSerializationUtils for better performance ([#4977](https://github.com/opensearch-project/security/pull/4977))
* Optimized Privilege Evaluation: Action privileges ONLY, with feature flag ([#4998](https://github.com/opensearch-project/security/pull/4998))
* Implement new extension points in IdentityPlugin and add ContextProvidingPluginSubject ([#5028](https://github.com/opensearch-project/security/pull/5028))
* Implement new extension points in IdentityPlugin and add ContextProvidingPluginSubject - legacy authz code path ([#5037](https://github.com/opensearch-project/security/pull/5037))
* Ensure that plugin can search on system index when utilizing pluginSubject.runAs ([#5032](https://github.com/opensearch-project/security/pull/5032))
* Ensure that plugin can update on system index when utilizing pluginSubject.runAs ([#5055](https://github.com/opensearch-project/security/pull/5055))
* Add ingest pipeline and indices related permissions for anomaly\_full\_access role ([#5069](https://github.com/opensearch-project/security/pull/5069))
* Added roles for ltr read and full access ([#5070](https://github.com/opensearch-project/security/pull/5070))


### Opensearch Security Dashboards Plugin


* Add LTR transport actions to cluster permissions list ([#2170](https://github.com/opensearch-project/security-dashboards-plugin/pull/2170))


### Opensearch Skills


* Support pass prompt to CreateAlertTool ([#452](https://github.com/opensearch-project/skills/pull/452))
* CreateAnomalyDetectorTool supports empty model\_type ([#457](https://github.com/opensearch-project/skills/pull/457))
* Log pattern tool improvement ([#474](https://github.com/opensearch-project/skills/pull/474))
* Add multi tenacy support ([#489](https://github.com/opensearch-project/skills/pull/489))
* Add model related field for tools ([#491](https://github.com/opensearch-project/skills/pull/491))
* Support s3 using repackage ([#482](https://github.com/opensearch-project/skills/pull/482))


### Opensearch k-NN


* Introduced a writing layer in native engines where relies on the writing interface to process IO. ([#2241](https://github.com/opensearch-project/k-NN/pull/2241))
* Allow method parameter override for training based indices ([#2290](https://github.com/opensearch-project/k-NN/pull/2290))
* Optimizes lucene query execution to prevent unnecessary rewrites ([#2305](https://github.com/opensearch-project/k-NN/pull/2305))
* Added more detailed error messages for KNN model training ([#2378](https://github.com/opensearch-project/k-NN/pull/2378))
* Add check to directly use ANN Search when filters match all docs. ([#2320](https://github.com/opensearch-project/k-NN/pull/2320))
* Use one formula to calculate cosine similarity ([#2357](https://github.com/opensearch-project/k-NN/pull/2357))
* Make the build work for M series MacOS without manual code changes and local JAVA\_HOME config ([#2397](https://github.com/opensearch-project/k-NN/pull/2397))
* Remove DocsWithFieldSet reference from NativeEngineFieldVectorsWriter ([#2408](https://github.com/opensearch-project/k-NN/pull/2408))
* Remove skip building graph check for quantization use case ([#2430](https://github.com/opensearch-project/k-NN/2430))
* Removing redundant type conversions for script scoring for hamming space with binary vectors ([#2351](https://github.com/opensearch-project/k-NN/pull/2351))
* Update default to 0 to always build graph as default behavior ([#2452](https://github.com/opensearch-project/k-NN/pull/2452))
* Enabled concurrent graph creation for Lucene engine with index thread qty settings ([#2480](https://github.com/opensearch-project/k-NN/pull/2480))


### Opensearch SQL


* Add validation method for Flint extension queries and wire it into the dispatcher ([#3096](https://github.com/opensearch-project/sql/pull/3096))
* Add grammar validation for PPL ([#3167](https://github.com/opensearch-project/sql/pull/3167))
* Add validation for unsupported type/identifier/commands ([#3195](https://github.com/opensearch-project/sql/pull/3195))
* Fix the flaky test testExtractDatePartWithTimeType() ([#3225](https://github.com/opensearch-project/sql/pull/3225))
* Allow metadata fields in PPL query ([#2789](https://github.com/opensearch-project/sql/pull/2789))


## BUG FIXES


### Opensearch Alerting


* Force create last run context in monitor workflow metadata when workflow is re-enabled ([#1778](https://github.com/opensearch-project/alerting/pull/1778))
* Fix bucket selector aggregation writeable name. ([#1780](https://github.com/opensearch-project/alerting/pull/1780))


### Opensearch Alerting Dashboards Plugin


* [BUG] Change time format to UTC in notification message preview ([#1183](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1183))
* Fix: error toast message while configuring trigger while creating a monitor ([#1178](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1178))


### Opensearch Anomaly Detection


* Not blocking detector creation on unknown feature validation error ([#1366](https://github.com/opensearch-project/anomaly-detection/pull/1366))
* Fix exceptions in IntervalCalculation and ResultIndexingHandler ([#1379](https://github.com/opensearch-project/anomaly-detection/pull/1379))


### Opensearch Anomaly Detection Dashboards


* Fix mds bugs ([#915](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/915))


### Opensearch Common Utils


* Fix bucket selector aggregation writeable name. ([#773](https://github.com/opensearch-project/common-utils/pull/773))


### Opensearch Custom Codecs


* Wrap a call to QatZipper with AccessController.doPrivileged ([#211](https://github.com/opensearch-project/custom-codecs/pull/211))


### Opensearch Dashboards Maps


* Locked custom wms crs input to epsg-3857 ([#632](https://github.com/opensearch-project/dashboards-maps/pull/632))


### Opensearch Dashboards Reporting


* Sanitize markdown when previewing report header/footer ([#476](https://github.com/opensearch-project/dashboards-reporting/pull/476))
* [BUG] Csv report generation had missing nested Fields ([#502](https://github.com/opensearch-project/dashboards-reporting/pull/502))


### Opensearch Flow Framework


* Remove useCase and defaultParams field in WorkflowRequest ([#758](https://github.com/opensearch-project/flow-framework/pull/758))


* Fix RBAC fetching from workflow state when template is not present ([#998](https://github.com/opensearch-project/flow-framework/pull/998))


### Opensearch Index Management


* Fix 2.x build due to bug fix on update settings requests on read only indices in core ([#1315](https://github.com/opensearch-project/index-management/pull/1315))


### Opensearch Index Management Dashboards Plugin


* Bug-fix: Restore snapshot shouldn't restore index alias always ([#1206](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1206))
* Bug fixes in Snapshot Policy: Schedule Editing and Index Expression Display ([#1208](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1208))
* Bug fix: Snapshot restore always restores index alias ([#1214](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1214))
* Fixing bug in transform API validation to support index patterns ([#1241](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1241))
* Updating cypress version and fixing CVE-2024-21538 ([#1252](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1252))


### Opensearch ML Commons


* getFirst is not allowed in java 17 ([#3226](https://github.com/opensearch-project/ml-commons/pull/3226))
* Fix: ml/engine/utils/FileUtils casts long file length to int incorrectly ([3198](https://github.com/opensearch-project/ml-commons/pull/3198))
* Fix for sync up job not working in 2.17 when upgraded from previous versions ([3241](https://github.com/opensearch-project/ml-commons/pull/3241))
* Fix remote model with embedding input issue ([3289](https://github.com/opensearch-project/ml-commons/pull/3289))
* Adds preset contentRegistry for IngestProcessors ([3281](https://github.com/opensearch-project/ml-commons/pull/3281))
* Revert "Add application_type to ConversationMeta; update tests (#3282)" ([3315](https://github.com/opensearch-project/ml-commons/pull/3315))
* Revert "Filter out remote model auto redeployment (#2976)" and related commits (#3104, #3214) ([3368](https://github.com/opensearch-project/ml-commons/pull/3368))
* Fix JsonGenerationException error in Local Sample Calculator and Anomaly Localization Execution Response ([3434](https://github.com/opensearch-project/ml-commons/pull/3434))
* [Backport 2.19] Fix guardrail it for 2.19 ([3468](https://github.com/opensearch-project/ml-commons/pull/3468))
* Addressing client changes due to adding tenantId in the apis (#3474) ([3480](https://github.com/opensearch-project/ml-commons/pull/3480))


### Opensearch Neural Search


* Address inconsistent scoring in hybrid query results ([#998](https://github.com/opensearch-project/neural-search/pull/998))
* Fix bug where ingested document has list of nested objects ([#1040](https://github.com/opensearch-project/neural-search/pull/1040))
* Fixed document source and score field mismatch in sorted hybrid queries ([#1043](https://github.com/opensearch-project/neural-search/pull/1043))
* Update NeuralQueryBuilder doEquals() and doHashCode() to cater the missing parameters information ([#1045](https://github.com/opensearch-project/neural-search/pull/1045)).
* Fix bug where embedding is missing when ingested document has "." in field name, and mismatches fieldMap config ([#1062](https://github.com/opensearch-project/neural-search/pull/1062))


### Opensearch Observability


* [Bug] Add loading status to all pages in traces and services pages ([#2336](https://github.com/opensearch-project/dashboards-observability/pull/2336))
* Add MDS support for missing datasourceId in traceGroup requests ([#2333](https://github.com/opensearch-project/dashboards-observability/pull/2333))
* Traces - Filter Adjustment and DataGrid abstraction ([#2321](https://github.com/opensearch-project/dashboards-observability/pull/2321))
* Remove redundant traces call for related services ([#2315](https://github.com/opensearch-project/dashboards-observability/pull/2315))
* Traces/Services - Query optimization / UI setting / Bugfix ([#2310](https://github.com/opensearch-project/dashboards-observability/pull/2310))
* Update latest github links in maintainer doc ([#2304](https://github.com/opensearch-project/dashboards-observability/pull/2304))
* Traces custom source - Bug Fixes ([#2298](https://github.com/opensearch-project/dashboards-observability/pull/2298))
* Gantt Chart / Service Map followup ([#2294](https://github.com/opensearch-project/dashboards-observability/pull/2294))
* Fix flaky cypress tests ([#2293](https://github.com/opensearch-project/dashboards-observability/pull/2293))
* Fix SQL/PPL crash with incorrect query ([#2284](https://github.com/opensearch-project/dashboards-observability/pull/2284))
* Fix notebook routes for savedNotebook endpoints ([#2279](https://github.com/opensearch-project/dashboards-observability/pull/2279))
* Updated notebooks reporting button render ([#2278](https://github.com/opensearch-project/dashboards-observability/pull/2278))
* Fix fetching workspace visualizations error ([#2268](https://github.com/opensearch-project/dashboards-observability/pull/2268))
* Replace index mapping with field caps API for trace filters ([#2246](https://github.com/opensearch-project/dashboards-observability/pull/2246))
* Metrics datasource ([#2242](https://github.com/opensearch-project/dashboards-observability/pull/2242))
* Use savedObjects client to fetch notebook visualizations ([#2241](https://github.com/opensearch-project/dashboards-observability/pull/2241))
* Fix mds ref update on integration assets ([#2240](https://github.com/opensearch-project/dashboards-observability/pull/2240))
* Return 503 if opensearch calls failed ([#2238](https://github.com/opensearch-project/dashboards-observability/pull/2238))
* [BUG-Fixed] #1466 - create observability dashboard after invalid name ([#1928](https://github.com/opensearch-project/dashboards-observability/pull/1928))
* [Bug fix] Traces/Services bugfixes and UI update ([#2235](https://github.com/opensearch-project/dashboards-observability/pull/2235))


### Opensearch Opensearch Learning To Rank Base

* [Backport to 2.19] Refactor index refresh logic in ITs ([#135](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/135))
* Modify ITs to ignore transient warning ([#132](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/132))
* Stashed context for GET calls ([#129](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/129))
* [Backport 2.19] Modified Rest Handlers to stash context before modifying system indices ([#126](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/126))
* Fix: added initialization of ltr settings in LtrQueryParserPlugin ([#85](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/85))
* Fix: fixed namings of test classes ([#83](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/83))


### Opensearch Query Insights


* Fix parsing error in SearchQueryRecord ([#184](https://github.com/opensearch-project/query-insights/pull/184))
* Fix bug on node\_id missing in local index ([#207](https://github.com/opensearch-project/query-insights/pull/207))
* Fix null indexFieldMap bug & add UTs ([#214](https://github.com/opensearch-project/query-insights/pull/214))
* Fix toString on operational metrics ([#219](https://github.com/opensearch-project/query-insights/pull/219))
* Fix grouping integ tests ([#223](https://github.com/opensearch-project/query-insights/pull/223))


### Opensearch Query Insights Dashboards


* Fix broken jest tests ([#18](https://github.com/opensearch-project/query-insights-dashboards/pull/18))
* Fix bugs in UI and refactor code ([#15](https://github.com/opensearch-project/query-insights-dashboards/pull/15))
* Fix error thrown on overview page ([#24](https://github.com/opensearch-project/query-insights-dashboards/pull/24))
* Fix default strings across pages ([#51](https://github.com/opensearch-project/query-insights-dashboards/pull/51))
* Fix bugs on configuration pages and refactor code ([#49](https://github.com/opensearch-project/query-insights-dashboards/pull/49))
* Fix all filters on the main page ([#78](https://github.com/opensearch-project/query-insights-dashboards/pull/78))
* Fix cypress tests after changing the default values ([#82](https://github.com/opensearch-project/query-insights-dashboards/pull/82))


### Opensearch Security


* Fix issue with jwt attribute parsing of lists ([#4885](https://github.com/opensearch-project/security/pull/4885))
* Log io.netty.internal.tcnative.SSLContext availability warning only when OpenSSL is explicitly enabled but not available ([#4906](https://github.com/opensearch-project/security/pull/4906))
* Reduce log level in HttpJwtAuthenticator if request cannot be authenticated ([#4917](https://github.com/opensearch-project/security/pull/4917))
* Honor log\_request\_body setting in compliance audit log ([#4918](https://github.com/opensearch-project/security/pull/4918))
* Change log level for log line in OBO Authenticator if OBO is disabled ([#4956](https://github.com/opensearch-project/security/pull/4956))
* Set default value for key/trust store type as constant for JDK PKCS setup ([#5003](https://github.com/opensearch-project/security/pull/5003))
* Fix SSL config for JDK PKCS setup ([#5033](https://github.com/opensearch-project/security/pull/5033))
* Fix Netty4 header verifier inbound handler to deal with upgrade requests ([#5045](https://github.com/opensearch-project/security/pull/5045))
* Generate jacoco report for integTestRemote task ([#5050](https://github.com/opensearch-project/security/pull/5050))


### Opensearch Security Analytics


* Add validation for threat intel source config ([#1393](https://github.com/opensearch-project/security-analytics/pull/1393))
* fix detector to work for trigger conditions filtering on aggregation rules ([#1423](https://github.com/opensearch-project/security-analytics/pull/1423))
* fixes the duplicate alerts generated by Aggregation Sigma Roles ([#1424](https://github.com/opensearch-project/security-analytics/pull/1424))
* OCSF1.1 Fixes ([#1439](https://github.com/opensearch-project/security-analytics/pull/1439))
* Added catch for unexpected inputs. ([#1442](https://github.com/opensearch-project/security-analytics/pull/1442))
* Refactored flaky test. ([#1464](https://github.com/opensearch-project/security-analytics/pull/1464))


### Opensearch Security Dashboards Plugin


* Preserve query in nextUrl during openid login redirect ([#2140](https://github.com/opensearch-project/security-dashboards-plugin/pull/2140))
* Fix tenant defaulting incorrectly ([#2163](https://github.com/opensearch-project/security-dashboards-plugin/pull/2163))


### Opensearch Skills


* Fix compilation issue caused by AD change ([#458](https://github.com/opensearch-project/skills/pull/458))


### Opensearch k-NN


* Fixing the bug when a segment has no vector field present for disk based vector search ([#2282](https://github.com/opensearch-project/k-NN/pull/2282))
* Fixing the bug where search fails with "fields" parameter for an index with a knn\_vector field ([#2314](https://github.com/opensearch-project/k-NN/pull/2314))
* Fix for NPE while merging segments after all the vector fields docs are deleted ([#2365](https://github.com/opensearch-project/k-NN/pull/2365))
* Allow validation for non knn index only after 2.17.0 ([#2315](https://github.com/opensearch-project/k-NN/pull/2315))
* Fixing the bug to prevent updating the index.knn setting after index creation ([#2348](https://github.com/opensearch-project/k-NN/pull/2348))
* Release query vector memory after execution ([#2346](https://github.com/opensearch-project/k-NN/pull/2346))
* Fix shard level rescoring disabled setting flag ([#2352](https://github.com/opensearch-project/k-NN/pull/2352))
* Fix filter rewrite logic which was resulting in getting inconsistent / incorrect results for cases where filter was getting rewritten for shards ([#2359](https://github.com/opensearch-project/k-NN/pull/2359))
* Fixing it to retrieve space\_type from index setting when both method and top level don't have the value ([#2374](https://github.com/opensearch-project/k-NN/pull/2374))
* Fixing the bug where setting rescore as false for on\_disk knn\_vector query is a no-op ([#2399](https://github.com/opensearch-project/k-NN/pull/2399))
* Fixing the bug to prevent index.knn setting from being modified or removed on restore snapshot ([#2445](https://github.com/opensearch-project/k-NN/pull/2445))
* Fix Faiss byte vector efficient filter bug ([#2448](https://github.com/opensearch-project/k-NN/pull/2448))
* Fixing bug where mapping accepts both dimension and model-id ([#2410](https://github.com/opensearch-project/k-NN/pull/2410))
* Add version check for full field name validation ([#2477](https://github.com/opensearch-project/k-NN/pull/2477))
* Update engine for version 2.19 or above ([#2501](https://github.com/opensearch-project/k-NN/pull/2501))


### SQL


* Fix a regression issue of parsing datetime string with custom time format in Span ([#3079](https://github.com/opensearch-project/sql/pull/3079))
* Fix: CSV and Raw output, escape quotes ([#3063](https://github.com/opensearch-project/sql/pull/3063))
* Fix FilterOperator to cache next element and avoid repeated consumption on hasNext() calls ([#3123](https://github.com/opensearch-project/sql/pull/3123))
* Function str\_to\_date should work with two-digits year ([#2841](https://github.com/opensearch-project/sql/pull/2841))


## INFRASTRUCTURE


### Opensearch Anomaly Detection


* Bump codecov/codecov-action from 4 to 5 ([#1369](https://github.com/opensearch-project/anomaly-detection/pull/1369))
* Bump com.google.code.gson:gson from 2.8.9 to 2.11.0 ([#1375](https://github.com/opensearch-project/anomaly-detection/pull/1375))
* Bump jackson from 2.18.0 to 2.18.2 ([#1376](https://github.com/opensearch-project/anomaly-detection/pull/1376))
* Bump org.apache.commons:commons-lang3 from 3.13.0 to 3.17.0 ([#1377](https://github.com/opensearch-project/anomaly-detection/pull/1377))
* Bump org.objenesis:objenesis from 3.3 to 3.4 ([#1393](https://github.com/opensearch-project/anomaly-detection/pull/1393))
* Updating several dependencies ([#1368](https://github.com/opensearch-project/anomaly-detection/pull/1368))
* Update recency\_emphasis to be greater than 1 in test cases ([#1406](https://github.com/opensearch-project/anomaly-detection/pull/1406))


### Opensearch Geospatial


* Github ci-runner Node.js issue fix ([#701](https://github.com/opensearch-project/geospatial/pull/701))
* Github CI pipeline update to publish geospatial-client Jar ([#706](https://github.com/opensearch-project/geospatial/pull/706))


### Opensearch ML Common


* Enable custom start commands and options to resolve GHA issues ([#3223](https://github.com/opensearch-project/ml-commons/pull/3223))
* Add Spotless Check to maintain consistency ([#3386](https://github.com/opensearch-project/ml-commons/pull/3386))
* Add runs-on field to Spotless Check step in CI ([#3400](https://github.com/opensearch-project/ml-commons/pull/3400))
* Checkout code from pull request head for spotless ([#3422](https://github.com/opensearch-project/ml-commons/pull/3422))
* Fixes spotless on Java 11 ([#3449](https://github.com/opensearch-project/ml-commons/pull/3449))
* add spotless to all build.gradle files ([#3453](https://github.com/opensearch-project/ml-commons/pull/3453))
* Fixes Two Flaky IT classes RestMLGuardrailsIT & ToolIntegrationWithLLMTest ([#3253](https://github.com/opensearch-project/ml-commons/pull/3253))
* Improve test coverage for RemoteModel.java ([#3205](https://github.com/opensearch-project/ml-commons/pull/3205))
* Revert Text Block changes from "Enhance validation for create connector API" ([#3260](https://github.com/opensearch-project/ml-commons/pull/3260)) ([#3329](https://github.com/opensearch-project/ml-commons/pull/3329))


### Opensearch Observability


* Remove fallback restore keys from build cache ([#2228](https://github.com/opensearch-project/dashboards-observability/pull/2228))


### Opensearch Opensearch Learning To Rank Base


* Added builds against JAVA 11 and 17 ([#124](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/124))
* [Backport to 2.x] Support Integration Tests against an external test cluster with security plugin enabled ([#122](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/122))
* Backporting commits from main to 2.x ([#116](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/116))
* Modified build scripts to onboard LTR to OpenSearch ([#98](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/98))
* Merge main into 2.x ([#91](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/91))


### Opensearch Query Insights


* Fix 2.x github checks ([#171](https://github.com/opensearch-project/query-insights/pull/171))
* Fix github CI by adding eclipse dependency in build.gradle ([#181](https://github.com/opensearch-project/query-insights/pull/181))


### Opensearch Query Insights Dashboards


* Configure Mend for GitHub.com ([#1](https://github.com/opensearch-project/query-insights-dashboards/pull/1))
* Bootstrap query insights dashboards repo ([#2](https://github.com/opensearch-project/query-insights-dashboards/pull/2))
* Set up basic ci workflow for query insights dashboards ([#3](https://github.com/opensearch-project/query-insights-dashboards/pull/3))
* Fix eslint config and related linting issues ([#20](https://github.com/opensearch-project/query-insights-dashboards/pull/20))
* Add github workflow for backport ([#23](https://github.com/opensearch-project/query-insights-dashboards/pull/23))
* Set up github actions for 2.x ([#36](https://github.com/opensearch-project/query-insights-dashboards/pull/36))
* Query grouping dashboard changes and extensive tests ([#48](https://github.com/opensearch-project/query-insights-dashboards/pull/48))


### Opensearch Skills


* Fix github ci linux build and RAG tool missing return ([#477](https://github.com/opensearch-project/skills/pull/477))


### Opensearch k-NN


* Updated C++ version in JNI from c++11 to c++17 [#2259](https://github.com/opensearch-project/k-NN/pull/2259)
* Upgrade bytebuddy and objenesis version to match OpenSearch core and, update github ci runner for macos [#2279](https://github.com/opensearch-project/k-NN/pull/2279)


### Opensearch SQL


* [AUTO] Increment version to 2.19.0-SNAPSHOT ([#3119](https://github.com/opensearch-project/sql/pull/3119))
* Fix: CI Github Action ([#3177](https://github.com/opensearch-project/sql/pull/3177))
* Artifacts to upload should include the java version in its name to avoid conflicts ([#3239](https://github.com/opensearch-project/sql/pull/3239))


## DOCUMENTATION


### Opensearch Alerting


* Added 2.19.0 release notes. ([#1790](https://github.com/opensearch-project/alerting/pull/1790))


### Opensearch Alerting Dashboards Plugin


* Added 2.19.0 release notes. ([#1201](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1201))


### Opensearch Common Utils


* Added 2.19.0.0 release notes. ([#780](https://github.com/opensearch-project/common-utils/pull/780))


### Opensearch Dashboards Notifications


* Added 2.19.0 release notes. ([#321](https://github.com/opensearch-project/dashboards-notifications/pull/321))


### Opensearch ML Common


* Fix: typo in MLAlgoParams ([#3195](https://github.com/opensearch-project/ml-commons/pull/3195/files))
* Add tutorial for bge-reranker-m3-v2, multilingual cross-encoder model on SageMaker ([#2848](https://github.com/opensearch-project/ml-commons/pull/2848))
* [Backport main] adding blue print doc for cohere multi-modal model ([#3232](https://github.com/opensearch-project/ml-commons/pull/3232))
* Tutorial for using Asymmetric models ([#3258](https://github.com/opensearch-project/ml-commons/pull/3258))
* Add tutorials for cross encoder models on Amazon Bedrock ([#3278](https://github.com/opensearch-project/ml-commons/pull/3278))
* Fix typo ([#3234](https://github.com/opensearch-project/ml-commons/pull/3234))
* Tutorial for ml inference with cohere rerank model ([#3398](https://github.com/opensearch-project/ml-commons/pull/3398))
* Add DeepSeek connector blueprint ([#3436](https://github.com/opensearch-project/ml-commons/pull/3436))
* Fix post\_process\_function on rerank\_pipeline\_with\_bge-rerank-m3-v2\_model\_deployed\_on\_Sagemaker.md ([#3296](https://github.com/opensearch-project/ml-commons/pull/3296))


### Opensearch Notifications


* Add 2.19.0 release notes ([#996](https://github.com/opensearch-project/notifications/pull/996))


### Opensearch Observability


* SOP for Integration and Vended Dashabords Setup ([#2299](https://github.com/opensearch-project/dashboards-observability/pull/2299))


### Opensearch Query Insights


* 2.19 Release Notes ([#225](https://github.com/opensearch-project/query-insights/pull/225))


### Opensearch Query Insights Dashboards


* 2.19 Release Notes ([#90](https://github.com/opensearch-project/query-insights-dashboards/pull/90))


### Opensearch Security Analytics


* Added 2.19.0 release notes. ([#1468](https://github.com/opensearch-project/security-analytics/pull/1468))


### Opensearch Security Analytics Dashboards


* Added 2.19.0 release notes. ([#1256](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1256))


### Opensearch Skills


* Sync maintainers list ([#488](https://github.com/opensearch-project/skills/pull/488))


### SQL


* Added documentation for the plugins.query.field\_type\_tolerance setting ([#3118](https://github.com/opensearch-project/sql/pull/3118))


## MAINTENANCE


### Dashboards Assistant


* Increment version to 2.19.0.0([#375](https://github.com/opensearch-project/dashboards-assistant/pull/375))


* Bump cross-spawn from 6.0.5 and 7.0.3 to 7.0.5([#418](https://github.com/opensearch-project/dashboards-assistant/pull/418))
* Bump cross-spawn from 7.0.3 to 7.0.5([#421](https://github.com/opensearch-project/dashboards-assistant/pull/421))


### Opensearch Alerting


* Increment version to 2.19.0-SNAPSHOT. ([#1716](https://github.com/opensearch-project/alerting/pull/1716))
* Upgrade to upload-artifact v4 ([#1739](https://github.com/opensearch-project/alerting/pull/1739))


### Opensearch Alerting Dashboards Plugin


* Increment version to 2.19.0.0 ([#1168](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1168))
* Bumped cypress version to 12.17.4. Bump cross-spawn to 7.0.6 ([#1198](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1198))


### Opensearch Anomaly Detection Dashboards


* Remove unnecessary dependencies ([#908](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/908))
* Bump axios from 1.6.7 to 1.7.7 ([#911](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/911))
* Bump elliptic from 6.5.4 to 6.6.0 ([#923](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/923))
* Bump cross-spawn from 7.0.3 to 7.0.6 ([#935](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/935))


### Opensearch Asynchronous Search


* Increment version to 2.19.0 ([#648](https://github.com/opensearch-project/asynchronous-search/pull/648))


### Opensearch Common Utils


* Increment version to 2.19.0-SNAPSHOT ([#749](https://github.com/opensearch-project/common-utils/pull/749))
* Remove version workflow ([#455](https://github.com/opensearch-project/common-utils/pull/455))
* Updates sample cert and admin keystore ([#598](https://github.com/opensearch-project/common-utils/pull/598))
* Fix 2.x branch github CI workflow. ([#777](https://github.com/opensearch-project/common-utils/pull/777))


### Opensearch Dashboards Notifications


* Increment version to 2.19.0.0 ([#304](https://github.com/opensearch-project/dashboards-notifications/pull/304))
* Bump cross-spawn from 7.0.3 to 7.0.6 ([#301](https://github.com/opensearch-project/dashboards-notifications/pull/301))
* Bumped cypress version. ([#313](https://github.com/opensearch-project/dashboards-notifications/pull/313))


### Opensearch Dashboards Reporting


* Increment version to 2.19.0.0 ([#478](https://github.com/opensearch-project/dashboards-reporting/pull/478))
* Downgrade cypress to 12.17.4 ([#504](https://github.com/opensearch-project/dashboards-reporting/pull/504))
* [CVE-2024-21538] Bump cross-spawn from 6.0.5 and 7.0.3 to 7.0.5 ([#508](https://github.com/opensearch-project/dashboards-reporting/pull/508))
* [CVE-2024-47875] Bump dompurify to 3.2.4 ([#511](https://github.com/opensearch-project/dashboards-reporting/pull/511))


### Opensearch Dashboards Search Relevance


* Increment version to 2.19.0.0 ([#469](https://github.com/opensearch-project/dashboards-search-relevance/pull/469))
* Bump cross-spawn from 6.0.5 to 6.0.6 ([#468](https://github.com/opensearch-project/dashboards-search-relevance/pull/468)) ([#476](https://github.com/opensearch-project/dashboards-search-relevance/pull/476))


### Opensearch Dashboards Visualizations


* Increment version to 2.19.0.0 ([#407](https://github.com/opensearch-project/dashboards-visualizations/pull/407))


* Downgrade cypress to 12.17.4 ([#413](https://github.com/opensearch-project/dashboards-visualizations/pull/413))
* Bump cross-spawn to 7.0.5 ([#417](https://github.com/opensearch-project/dashboards-visualizations/pull/417))
* Adding release notes for 2.19.0 ([#427](https://github.com/opensearch-project/dashboards-visualizations/pull/427))
* [CVE-2024-21538] Update cross-spawn in yarn.lock([#423](https://github.com/opensearch-project/dashboards-visualizations/pull/423))


### Opensearch Index Management


* Update maintainers and codeowners of the repo ([#1316](https://github.com/opensearch-project/index-management/pull/1316))
* Revert "Update maintainers and codeowners of the repo" ([#1320](https://github.com/opensearch-project/index-management/pull/1320))
* dependabot: bump commons-codec:commons-codec from 1.13 to 1.17.2 ([#1335](https://github.com/opensearch-project/index-management/pull/1335))
* Added new maintainers to ISM ([#1339](https://github.com/opensearch-project/index-management/pull/1339))
* dependabot: bump com.puppycrawl.tools:checkstyle from 8.29 to 8.45.1 ([#1337](https://github.com/opensearch-project/index-management/pull/1337))
* bump ktlint 1.1.0 to 1.5.0 ([#1338](https://github.com/opensearch-project/index-management/pull/1338))


### Opensearch Index Management Dashboards Plugin


* Increment version to 2.19.0.0 ([#1218](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1218))
* Updating the maintainers and codeowners list ([#1223](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1223))
* Reverting the maintainers and codeowners list([#1234](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1234))
* Sync Maintainers to 2.x from main branch ([#1238](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1238))
* Backport 1258 to 2.19 ([#1260](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1260))


### Opensearch Job Scheduler


* Increment version to 2.19.0 ([#694](https://github.com/opensearch-project/job-scheduler/pull/694)).
* Enable custom start commands and options to resolve GHA issues ([#702](https://github.com/opensearch-project/job-scheduler/pull/702), [#703](https://github.com/opensearch-project/job-scheduler/pull/703)).
* dependabot: bump codecov/codecov-action from 4 to 5 ([#704](https://github.com/opensearch-project/job-scheduler/pull/704), [#705](https://github.com/opensearch-project/job-scheduler/pull/704)).
* dependabot: bump com.google.googlejavaformat:google-java-format from 1.24.0 to 1.25.0 ([#706](https://github.com/opensearch-project/job-scheduler/pull/706), [#707](https://github.com/opensearch-project/job-scheduler/pull/707)).
* dependabot: bump com.google.googlejavaformat:google-java-format from 1.25.0 to 1.25.2 ([#708](https://github.com/opensearch-project/job-scheduler/pull/708), [#709](https://github.com/opensearch-project/job-scheduler/pull/709)).
* dependabot: bump com.netflix.nebula.ospackage from 11.10.0 to 11.10.1 ([#710](https://github.com/opensearch-project/job-scheduler/pull/710), [#711](https://github.com/opensearch-project/job-scheduler/pull/711)).
* dependabot: bump org.gradle.test-retry from 1.6.0 to 1.6.1 ([#716](https://github.com/opensearch-project/job-scheduler/pull/716), [#717](https://github.com/opensearch-project/job-scheduler/pull/717)).
* dependabot: bump de.undercouch.download from 5.3.0 to 5.6.0 ([#719](https://github.com/opensearch-project/job-scheduler/pull/719), [#720](https://github.com/opensearch-project/job-scheduler/pull/720)).


### Opensearch ML Common


* Bump guava version to 32.1.3 ([#3300](https://github.com/opensearch-project/ml-commons/pull/3300))
* Update Gradle to 8.11.1 ([#3139](https://github.com/opensearch-project/ml-commons/pull/3139/files))
* Force version 3.29.0 of org.eclipse.core.runtime to mitigate CVE vulnerabilities ([#3313](https://github.com/opensearch-project/ml-commons/pull/3313))
* Upgraded software.amazon.awssdk from 2.25.40 to 2.29.0 to address CVE… ([#3320](https://github.com/opensearch-project/ml-commons/pull/3320))
* Adding back Mingshi as Maintainer. ([#3367](https://github.com/opensearch-project/ml-commons/pull/3367))
* updating sdk client version ([#3392](https://github.com/opensearch-project/ml-commons/pull/3392))
* downgrading codecov action ([#3409](https://github.com/opensearch-project/ml-commons/pull/3410))
* fix CVE from ai.djl dependency ([#3478](https://github.com/opensearch-project/ml-commons/pull/3482))


### Opensearch ML Commons Dashboards


* Increment version to 2.19.0.0 ([#387](https://github.com/opensearch-project/ml-commons-dashboards/pull/387))
* [CVE-2024-21538] Bump cross-spawn from 7.0.3 to 7.0.6 ([#385](https://github.com/opensearch-project/ml-commons-dashboards/pull/385))


### Opensearch Neural Search


* Add reindex integration tests for ingest processors ([#1075](https://github.com/opensearch-project/neural-search/pull/1075))
* Fix github CI by adding eclipse dependency in formatting.gradle ([#1079](https://github.com/opensearch-project/neural-search/pull/1079))


### Opensearch Notifications


* Add JDK-23 to the build matrix ([#977](https://github.com/opensearch-project/notifications/pull/977))


### Opensearch Observability


* Increment version to 2.19.0-SNAPSHOT ([#1874](https://github.com/opensearch-project/observability/pull/1874))


### Opensearch Observability


* Bump nanoid to 3.3.8 ([#2328](https://github.com/opensearch-project/dashboards-observability/pull/2328))


* Bump cross-spawn to 7.0.5 ([#2322](https://github.com/opensearch-project/dashboards-observability/pull/2322))
* Downgrade cypress to 12.17.4 ([#2306](https://github.com/opensearch-project/dashboards-observability/pull/2306))
* Configure OpenSearch Dashboards before running in CI ([#2291](https://github.com/opensearch-project/dashboards-observability/pull/2291))
* Panels updates ([#2285](https://github.com/opensearch-project/dashboards-observability/pull/2285))
* Fix flaky notebooks test ([#2280](https://github.com/opensearch-project/dashboards-observability/pull/2280))
* Event explorer updates ([#2275](https://github.com/opensearch-project/dashboards-observability/pull/2275))
* Metrics updates ([#2269](https://github.com/opensearch-project/dashboards-observability/pull/2269))
* Fix flaky render of spans table tests ([#2263](https://github.com/opensearch-project/dashboards-observability/pull/2263))
* App analytics updates ([#2261](https://github.com/opensearch-project/dashboards-observability/pull/2261))
* Separate uploaded cypress artifacts for actions/upload-artifact@v4 ([#2259](https://github.com/opensearch-project/dashboards-observability/pull/2259))
* Trace analytics updates ([#2251](https://github.com/opensearch-project/dashboards-observability/pull/2251))
* Increment version to 2.19.0.0 ([#2271](https://github.com/opensearch-project/dashboards-observability/pull/2271))
* Adding release notes for 2.19.0([#2343](https://github.com/opensearch-project/dashboards-observability/pull/2343))


### Opensearch Opensearch Learning To Rank Base


* 2.x issue93 ([#96](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/96))
* Fix: disabled gradle tasks forbiddenApisTest and testingConventions ([#94](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/94))
* Feat: Added JohannesDaniel in MAINTAINERS.md ([#53](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/53))
* Update CODEOWNERS ([#69](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/69))


### Opensearch Query Insights


* Remove local index custom name setting ([#166](https://github.com/opensearch-project/query-insights/pull/166))
* Migrate from Joda-Time to java.time API ([#176](https://github.com/opensearch-project/query-insights/pull/176))
* Change default values for window,n and exporter ([#196](https://github.com/opensearch-project/query-insights/pull/196))
* Bump up version for upload-artifact to fix the build ([#202](https://github.com/opensearch-project/query-insights/pull/202))
* Update default .enabled and exporter.type settings ([#217](https://github.com/opensearch-project/query-insights/pull/217))


### Opensearch Query Insights Dashboards


* Updates the defaults for frontend ([#76](https://github.com/opensearch-project/query-insights-dashboards/pull/76))
* Ensure constants and utils are under common ([#88](https://github.com/opensearch-project/query-insights-dashboards/pull/88))


### Opensearch Query Workbench


* Increment version to 2.19.0.0 ([#422](https://github.com/opensearch-project/dashboards-query-workbench/pull/422))


* Downgrade cypress to 12.17.4 ([#430](https://github.com/opensearch-project/dashboards-query-workbench/pull/430))
* [CVE-2024-21538] Bump cross-spawn from 6.0.5 and 7.0.3 to 7.0.5 ([434](https://github.com/opensearch-project/dashboards-query-workbench/pull/434))
* Update yarn.lock for cross-spawn ([441](https://github.com/opensearch-project/dashboards-query-workbench/pull/441))


### Opensearch Reporting


* Increment version to 2.19.0-SNAPSHOT ([#1044](https://github.com/opensearch-project/reporting/pull/1044))


### Opensearch Security


* Bump org.junit.jupiter:junit-jupiter-api from 5.11.2 to 5.11.3 ([#4856](https://github.com/opensearch-project/security/pull/4856))
* Bump ch.qos.logback:logback-classic from 1.5.11 to 1.5.12 ([#4857](https://github.com/opensearch-project/security/pull/4857))
* Bump com.google.errorprone:error\_prone\_annotations from 2.34.0 to 2.35.1 ([#4850](https://github.com/opensearch-project/security/pull/4850))
* Bump org.junit.jupiter:junit-jupiter from 5.11.2 to 5.11.3 ([#4861](https://github.com/opensearch-project/security/pull/4861))
* Bump Wandalen/wretry.action from 3.5.0 to 3.7.0 ([#4874](https://github.com/opensearch-project/security/pull/4874))
* Bump org.checkerframework:checker-qual from 3.48.1 to 3.48.2 ([#4875](https://github.com/opensearch-project/security/pull/4875))
* Bump com.nimbusds:nimbus-jose-jwt from 9.41.2 to 9.45 ([#4876](https://github.com/opensearch-project/security/pull/4876))
* Bump com.nimbusds:nimbus-jose-jwt from 9.45 to 9.46 ([#4890](https://github.com/opensearch-project/security/pull/4890))
* Bump Wandalen/wretry.action from 3.7.0 to 3.7.2 ([#4891](https://github.com/opensearch-project/security/pull/4891))
* Bump Zookeeper to 3.9.3 ([#4895](https://github.com/opensearch-project/security/pull/4895))
* Bump com.nimbusds:nimbus-jose-jwt from 9.46 to 9.47 ([#4916](https://github.com/opensearch-project/security/pull/4916))
* Update Gradle to 8.11 ([#4922](https://github.com/opensearch-project/security/pull/4922))
* Update Gradle to 8.11.1 ([#4925](https://github.com/opensearch-project/security/pull/4925))
* Bump com.google.googlejavaformat:google-java-format from 1.24.0 to 1.25.0 ([#4933](https://github.com/opensearch-project/security/pull/4933))
* Bump Wandalen/wretry.action from 3.7.2 to 3.7.3 ([#4932](https://github.com/opensearch-project/security/pull/4932))
* Bump commons-io:commons-io from 2.17.0 to 2.18.0 ([#4935](https://github.com/opensearch-project/security/pull/4935))
* Bump io.dropwizard.metrics:metrics-core from 4.2.28 to 4.2.29 ([#4941](https://github.com/opensearch-project/security/pull/4941))
* Fix typos ([#4951](https://github.com/opensearch-project/security/pull/4951))
* Bump com.carrotsearch.randomizedtesting:randomizedtesting-runner from 2.8.1 to 2.8.2 ([#4962](https://github.com/opensearch-project/security/pull/4962))
* Bump org.checkerframework:checker-qual from 3.48.2 to 3.48.3 ([#4958](https://github.com/opensearch-project/security/pull/4958))
* Bump org.eclipse.platform:org.eclipse.core.runtime from 3.31.100 to 3.32.0 ([#4964](https://github.com/opensearch-project/security/pull/4964))
* Bump org.apache.commons:commons-text from 1.12.0 to 1.13.0 ([#4971](https://github.com/opensearch-project/security/pull/4971))
* Bump com.google.googlejavaformat:google-java-format from 1.25.0 to 1.25.2 ([#4972](https://github.com/opensearch-project/security/pull/4972))
* Bump org.junit.jupiter:junit-jupiter from 5.11.3 to 5.11.4 ([#4985](https://github.com/opensearch-project/security/pull/4985))
* Bump com.nimbusds:nimbus-jose-jwt from 9.47 to 9.48 ([#4986](https://github.com/opensearch-project/security/pull/4986))
* Bump com.netflix.nebula.ospackage from 11.10.0 to 11.10.1 ([#4987](https://github.com/opensearch-project/security/pull/4987))
* Bump ch.qos.logback:logback-classic from 1.5.12 to 1.5.15 ([#4989](https://github.com/opensearch-project/security/pull/4989))
* Bump org.apache.camel:camel-xmlsecurity from 3.22.2 to 3.22.3 ([#4996](https://github.com/opensearch-project/security/pull/4996))
* Bump org.apache.santuario:xmlsec from 2.3.4 to 2.3.5 ([#5008](https://github.com/opensearch-project/security/pull/5008))
* Bump ch.qos.logback:logback-classic from 1.5.15 to 1.5.16 ([#5009](https://github.com/opensearch-project/security/pull/5009))
* Update Gradle to 8.12 ([#5018](https://github.com/opensearch-project/security/pull/5018))
* Bump commons-codec:commons-codec from 1.17.1 to 1.17.2 ([#5024](https://github.com/opensearch-project/security/pull/5024))
* Bump org.scala-lang:scala-library from 2.13.15 to 2.13.16 ([#5026](https://github.com/opensearch-project/security/pull/5026))
* Bump Wandalen/wretry.action from 3.7.3 to 3.8.0 ([#5025](https://github.com/opensearch-project/security/pull/5025))
* Bumps guava to 33.4.0-jre ([#5041](https://github.com/opensearch-project/security/pull/5041))
* Bump io.dropwizard.metrics:metrics-core from 4.2.29 to 4.2.30 ([#5043](https://github.com/opensearch-project/security/pull/5043))
* Remove deprecation comment for protected indices settings ([#5059](https://github.com/opensearch-project/security/pull/5059))
* Bump org.gradle.test-retry from 1.6.0 to 1.6.1 ([#5060](https://github.com/opensearch-project/security/pull/5060))


### Opensearch Security Analytics


* Incremented version to 2.19.0 ([#1444](https://github.com/opensearch-project/security-analytics/pull/1444))
* Fix CVE-2024-47535. ([#1460](https://github.com/opensearch-project/security-analytics/pull/1460))


### Opensearch Security Analytics Dashboards


* Increment version to 2.19.0.0 ([#1229](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1229))
* Bump cypress, and cross-spawn version. ([#1251](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1251))


### Opensearch Skills


* bump byte buddy version from 1.15.4 to 1.15.10 ([#466](https://github.com/opensearch-project/skills/pull/466))
fix(deps): update dependency org.scala-lang:scala-library to v2.13.9 ([#496](https://github.com/opensearch-project/skills/pull/496))


### Opensearch k-NN


* Select index settings based on cluster version ([#2236](https://github.com/opensearch-project/k-NN/pull/2236))
* Added periodic cache maintenance for QuantizationStateCache and NativeMemoryCache ([#2308](https://github.com/opensearch-project/k-NN/pull/2308))
* Added null checks for fieldInfo in ExactSearcher to avoid NPE while running exact search for segments with no vector field ([#2278](https://github.com/opensearch-project/k-NN/pull/2278))
* Added Lucene BWC tests ([#2313](https://github.com/opensearch-project/k-NN/pull/2313))
* Upgrade jsonpath from 2.8.0 to 2.9.0 ([#2325](https://github.com/opensearch-project/k-NN/pull/2325))
* Bump Faiss commit from 1f42e81 to 0cbc2a8 to accelerate hamming distance calculation using \_mm512\_popcnt\_epi64 intrinsic and also add avx512-fp16 instructions to boost performance ([#2381](https://github.com/opensearch-project/k-NN/pull/2381))
* Deprecate nmslib engine ([#2427](https://github.com/opensearch-project/k-NN/pull/2427))
* Add spotless mirror repo for fixing builds ([#2453](https://github.com/opensearch-project/k-NN/pull/2453))


### Opensearch SQL


* Fix spotless check failure for #3148 ([#3158](https://github.com/opensearch-project/sql/pull/3158))
* Fix coverage issue for #3063 ([#3155](https://github.com/opensearch-project/sql/pull/3155))
* Call LeaseManager for BatchQuery ([#3153](https://github.com/opensearch-project/sql/pull/3153))
* Make GrammarElement public ([#3161](https://github.com/opensearch-project/sql/pull/3161))
* Update grammar validation settings ([#3165](https://github.com/opensearch-project/sql/pull/3165))
* [Backport 2.x] Add release notes for 1.3.15 ([#2537](https://github.com/opensearch-project/sql/pull/2537))
* Fix DateTimeFunctionTest.testWeekOfYearWithTimeType and YearWeekTestt.testYearWeekWithTimeType Test Failures ([#3235](https://github.com/opensearch-project/sql/pull/3235))


## REFACTORING


### Opensearch Alerting


* optimize execution of workflow consisting of bucket-level followed by doc-level monitors ([#1729](https://github.com/opensearch-project/alerting/pull/1729))


### Opensearch Common Utils


* add should\_create\_single\_alert\_for\_findings field to security-analytics ([#757](https://github.com/opensearch-project/common-utils/pull/757))
* Monitor model changed to add an optional fanoutEnabled field ([#758](https://github.com/opensearch-project/common-utils/pull/758))


### Opensearch Flow Framework


* Replace String concatenation with Log4j ParameterizedMessage for readability ([#943](https://github.com/opensearch-project/flow-framework/pull/943))


### Opensearch Geospatial


* Use instance of LockService instantiated in JobScheduler through Guice ([#677](https://github.com/opensearch-project/geospatial/pull/677))


### Opensearch Opensearch Learning To Rank Base


* [Backport to 2.x] Deprecating Redundant and duplicated API and package. Refactor with the other package ([#118](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/118))


### Opensearch Security Analytics


* Optimize sigma aggregation rule based detectors execution workflow ([#1418](https://github.com/opensearch-project/security-analytics/pull/1418))
* Adding various OCSF 1.1 fields to log type static mappings ([#1403](https://github.com/opensearch-project/security-analytics/pull/1403))


### Opensearch Security Analytics Dashboards


* show selected rules on edit; options should only include enabled rules on edit ([#1231](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1231))
* Remove threat intel checkbox detector creation ([#1232](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1232))
* Updating Preview Message functionality while setting notifications in detector alerts ([#1241](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1241))