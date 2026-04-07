# OpenSearch and OpenSearch Dashboards 3.6.0 Release Notes

## Release Highlights

### New and Updated Features

#### Search Modernization
* **Automate search app development with OpenSearch Launchpad**: An AI-powered agent automatically provisions a complete local setup with optimal architecture and working UI based on your sample documents and conversational input. Launchpad can handle every technical decision—from semantic encoding to cluster configuration—and integrates natively with IDEs.

* **Simplify agent creation and standardize agent input**: A unified registration API collapses four manual steps (creating a connector, registering a model, configuring an agent, and mapping parameters) into single API call. New conversational_v2 agent type supports plain text, multimodal content blocks, and conversation history—no custom connector configuration required.

* **Build more robust agentic search applications**: New capabilities include alias support, embedding model configuration, fallback query options, reranking capabilities, and agentic memory for conversational, context-aware search experiences with improved relevance and precision.

* **Maximize storage efficiency with 1-bit Scalar Quantization**: 1-bit SQ delivers 32x compression across Faiss and Lucene engines with 24% better recall and 15% lower latency. Perform approximate and exact k-NN search directly on quantized vectors for metadata-heavy use cases.

* **Decrease latency with Faiss quantization optimizations**: New functionality leverages quantized flat vectors directly from graph files, offering a 40% reduction in latency for quantized index searches compared with FP32 flat vectors.

* **Reduce vector storage with metadata compression**: Zstandard compression for vectors reduces the disk footprint for metadata, enabling storage of more metadata-rich vectors on same hardware without compromising high-speed access needed for search and retrieval.

* **Reduce vector search latency 50%**: New prefetch functionality for ANN and exact search proactively loads vectors into memory before CPU needs them, minimizing idle cycles to deliver up to 2x search latency improvements for memory-constrained environments.

* **Streamline relevance tuning**: Ease-of-use enhancements to the Search Relevance Workbench simplify the work of organizing experiments, running experiments against multiple data sources, and creating query sets. Evaluate quality for different search scenarios with three new metrics: Recall@K, MRR, and DCG@K.
 
#### Observability and Analytics
* **Track and analyze distributed applications**: Built-in Application Performance Monitoring combines auto-generated service topology maps with RED metrics powered by OpenTelemetry and Data Prepper pipelines. A centralized services catalog offers per-operation and dependency performance breakdowns, and in-context correlations let you drill down to analyze root cause.

* **Monitor generative AI applications with Agent Traces**: Trace agent invocations, LLM calls, and tool executions across your AI stack using OpenTelemetry-based instrumentation. A Python SDK supports OpenAI, Anthropic, Bedrock, LangChain, and LlamaIndex with interactive DAG graphs and token usage tracking in Dashboards.

* **Deploy full-stack observability with one command**: This release supports the OpenSearch Observability Stack, which bundles OpenTelemetry Collector, Data Prepper, OpenSearch, Prometheus, and Dashboards into a single deployment to deliver comprehensive, open source observability.

* **Enhance PPL queries with new tools and commands**: This release brings a unified query library for third-party tools, search result highlighting, auto-extract mode for JSON fields, graphlookup for recursive graph traversal, and query cancellation for in-flight queries.
 
#### Scalability and Resiliency
* **Improve query debugging with user- and team-based access control**: A new filter mode enables self-service query debugging without admin privileges while maintaining data privacy for multi-tenant environments. Users see only their queries or queries from shared backend roles; administrators retain full visibility.

* **Enhance query insights with automated recommendations**: A new recommendation engine analyzes top N queries, identifies problems, and proposes solutions with confidence scores and estimated impacts. Recommendations are generated asynchronously off the search path with no impact to query performance.

* **Observe short-lived queries with cache layer**: A finished queries cache layer for the Live Queries API lets you retrieve recently completed queries alongside active ones, ideal for observing short-lived queries. A dynamic lifecycle model activates cache on demand to conserve resources.

* **Access remote storage for top N queries**: Query insights lets you move top N queries data to remote blob store repositories as a cost-effective, long-term storage option with support for Amazon S3 repositories in this release. Exported data is written as JSON files organized by timestamp with retention managed by bucket configuration.

* **Add visualizations to Top N Queries**: A new Stats & Visualizations panel displays P90 and P99 percentile stats with an interactive pie chart and table. A Performance Analysis section shows line chart and heatmap views to identify bottlenecks and understand query distribution.


### Experimental Features
OpenSearch 3.6 includes the following experimental functionality. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.
* **Optimize search results with OpenSearch Relevance Agent**: Automate search relevance tuning with multi-agent system integrated into OpenSearch Dashboards. The agent continuously analyzes user behavior, generates hypotheses, and validates improvements through offline evaluation to help you dramatically reduce optimization cycles.

## Release Details
[OpenSearch and OpenSearch Dashboards 3.6.0](https://opensearch.org/artifacts/by-version/#release-3-6-0) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.6.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.6.0.md).

## FEATURES


### OpenSearch Alerting


* Add configurable `plugins.alerting.monitor.max_triggers` cluster setting to limit the number of triggers per monitor ([#2036](https://github.com/opensearch-project/alerting/pull/2036))


### OpenSearch Alerting Dashboards Plugin


* Add lookback window frontend support for PPL/SQL monitors ([#1379](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1379))


### OpenSearch Anomaly Detection


* Add Terraform-based anomaly detection detector provisioning and lifecycle automation ([#1680](https://github.com/opensearch-project/anomaly-detection/pull/1680))


### OpenSearch Anomaly Detection Dashboards Plugin


* Update Daily Insights page to support new insight-results schema ([#1137](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1137))


### OpenSearch Common Utils


* Add Target object for external data source support on Monitor and Alert models ([#916](https://github.com/opensearch-project/common-utils/pull/916))


### OpenSearch Dashboards Investigation


* Add accept hypothesis feature ([#321](https://github.com/opensearch-project/dashboards-investigation/pull/321))
* Add duration tracking for investigations, steps, and sub-steps ([#320](https://github.com/opensearch-project/dashboards-investigation/pull/320))
* Add comprehensive telemetry metrics for investigation actions ([#342](https://github.com/opensearch-project/dashboards-investigation/pull/342))
* Add max length limit for visualization summary image size ([#326](https://github.com/opensearch-project/dashboards-investigation/pull/326))
* Allow log analysis to rerun during reinvestigation ([#322](https://github.com/opensearch-project/dashboards-investigation/pull/322))


### OpenSearch Dashboards Search Relevance


* Support manually creating a Query Set using plain text, key-value, or NDJSON input directly in the UI. ([#754](https://github.com/opensearch-project/dashboards-search-relevance/pull/754))
* Add Help flyout for Query Set creation with format documentation and downloadable sample files. ([#767](https://github.com/opensearch-project/dashboards-search-relevance/pull/767))
* Support multiple datasource in SRW ([#802](https://github.com/opensearch-project/dashboards-search-relevance/pull/802))
* Show a dismissible UI element to guide users to the relevance tuning agent if the chat plugin is enabled. ([#810](https://github.com/opensearch-project/dashboards-search-relevance/pull/810))


### OpenSearch ML Commons


* Introduce V2 Chat Agent with unified interface, multi-modal support, and simplified registration ([#4732](https://github.com/opensearch-project/ml-commons/pull/4732))
* Add semantic and hybrid search APIs for long-term memory retrieval in agentic memory ([#4658](https://github.com/opensearch-project/ml-commons/pull/4658))
* Add token usage tracking for Conversational, AG\_UI, and Plan-Execute-Reflect agents ([#4683](https://github.com/opensearch-project/ml-commons/pull/4683))
* Add LAST\_TOKEN pooling implementation for text embedding models used by decoder-only models ([#4711](https://github.com/opensearch-project/ml-commons/pull/4711))
* Add NONE pooling mode to support pre-pooled model outputs without redundant pooling computation ([#4710](https://github.com/opensearch-project/ml-commons/pull/4710))
* Add support for custom fallback query in QueryPlanningTool for agentic search ([#4729](https://github.com/opensearch-project/ml-commons/pull/4729))
* Support messages array in all memory types and chat history in AGUI agent ([#4645](https://github.com/opensearch-project/ml-commons/pull/4645))
* Add post-memory hook with structured message support for context managers ([#4687](https://github.com/opensearch-project/ml-commons/pull/4687))
* Improve EncryptorImpl with asynchronous handling for scalability and fix duplicate master key generation ([#3919](https://github.com/opensearch-project/ml-commons/pull/3919))
* Support aliases and wildcard index patterns in QueryPlanningTool ([#4726](https://github.com/opensearch-project/ml-commons/pull/4726))


### OpenSearch Neural Search


* [Agentic Search]: Support embedding model id in agentic query translator processor for neural queries ([#1800](https://github.com/opensearch-project/neural-search/pull/1800))


### OpenSearch Performance Analyzer


* Add shard operations collector and optimized node stats collector ([#824](https://github.com/opensearch-project/performance-analyzer/pull/824))


### OpenSearch Query Insights


* Add RemoteRepositoryExporter to support exporting top N queries to remote blob store repositories ([#541](https://github.com/opensearch-project/query-insights/pull/541))
* Add recommendation data models for rule-based recommendation engine ([#549](https://github.com/opensearch-project/query-insights/pull/549))
* Add shard-level task details to the live queries API for full distributed search visibility ([#548](https://github.com/opensearch-project/query-insights/pull/548))
* Add streaming dimension to query categorization metrics ([#551](https://github.com/opensearch-project/query-insights/pull/551))
* Implement access control for query insights data with username and backend role filtering ([#552](https://github.com/opensearch-project/query-insights/pull/552))
* Add rule-based recommendation service for analyzing search queries with actionable suggestions ([#555](https://github.com/opensearch-project/query-insights/pull/555))
* Track failed queries by tagging them with a failed attribute ([#540](https://github.com/opensearch-project/query-insights/pull/540))
* Add finished queries cache to the live queries API for retrieving recently completed searches ([#554](https://github.com/opensearch-project/query-insights/pull/554))


### OpenSearch Query Insights Dashboards


* Add visualizations to Top N Queries page including P90/P99 stats, queries by node/index/user/WLM group pie charts, and performance analysis line charts ([#473](https://github.com/opensearch-project/query-insights-dashboards/pull/473))
* Add heatmap visualization, interactive pie charts, collapsible sections, and sorting/pagination to Top N Queries page ([#486](https://github.com/opensearch-project/query-insights-dashboards/pull/486))


### OpenSearch Search Relevance


* Add optional name and description fields to experiments ([#408](https://github.com/opensearch-project/search-relevance/pull/408))
* Introduced dynamic percentile-based relevance thresholding for binary-dependent metrics (Precision, MAP) to replace hard-coded `j > 0` mapping ([#394](https://github.com/opensearch-project/search-relevance/pull/394))
* Added additional search evaluation metrics: Recall@K, Mean Reciprocal Rank (MRR), and Discounted Cumulative Gain (DCG@K) ([#397](https://github.com/opensearch-project/search-relevance/pull/397))


### OpenSearch Security


* Enable basic authentication for gRPC transport ([#6005](https://github.com/opensearch-project/security/pull/6005))
* Allow specifying parent type and parent ID field in ResourceProvider for parent-child resource authorization ([#5735](https://github.com/opensearch-project/security/pull/5735))


### OpenSearch Skills


* Add SearchAroundTool to search N documents around a given document ([#702](https://github.com/opensearch-project/skills/pull/702))
* Add MetricChangeAnalysisTool for detecting and analyzing metric changes via percentile comparison between baseline and selection periods ([#698](https://github.com/opensearch-project/skills/pull/698))


### OpenSearch k-NN


* Add 1-bit compression support for the Lucene Scalar Quantizer (BBQ integration) ([#3144](https://github.com/opensearch-project/k-NN/pull/3144))
* Add Faiss Scalar Quantization 1-bit support with memory-optimized search, SIMD acceleration, and codec integration ([#3208](https://github.com/opensearch-project/k-NN/pull/3208))
* Add support for Lucene BBQ Flat format with 1-bit (32x) compression ([#3154](https://github.com/opensearch-project/k-NN/pull/3154))
* Add support for pre-quantized vector exact search to avoid redundant quantization during queries ([#3095](https://github.com/opensearch-project/k-NN/pull/3095))
* Use pre-quantized vectors for Asymmetric Distance Computation (ADC) to improve search performance ([#3113](https://github.com/opensearch-project/k-NN/pull/3113))
* Add Hamming distance scorer for byte vectors to support memory-optimized binary vector search ([#3214](https://github.com/opensearch-project/k-NN/pull/3214))
* Add NestedBestChildVectorScorer and KnnBinaryDocValuesScorer for exact search when Lucene's built-in scorers are unavailable ([#3179](https://github.com/opensearch-project/k-NN/pull/3179))
* Add prefetch functionality for vectors during ANN search in memory-optimized search ([#3173](https://github.com/opensearch-project/k-NN/pull/3173))
* Add scorer-aware ByteVectorValues wrapper for FAISS index to enable scoring with external iterator support ([#3192](https://github.com/opensearch-project/k-NN/pull/3192))
* Introduce VectorScorers factory to create VectorScorer instances based on underlying vector storage format ([#3183](https://github.com/opensearch-project/k-NN/pull/3183))
* Support aborting native engine merges to prevent shard relocation and cluster stability issues ([#2529](https://github.com/opensearch-project/k-NN/pull/2529))


### OpenSearch SQL


* Update mend config to allow remediation ([#5287](https://github.com/opensearch-project/sql/pull/5287))
* Add unified query parser API ([#5274](https://github.com/opensearch-project/sql/pull/5274))
* Add profiling support to unified query API ([#5268](https://github.com/opensearch-project/sql/pull/5268))
* Add Calcite native SQL planning in UnifiedQueryPlanner ([#5257](https://github.com/opensearch-project/sql/pull/5257))
* Add query cancellation support via \_tasks/\_cancel API for PPL queries ([#5254](https://github.com/opensearch-project/sql/pull/5254))
* Support graphLookup with literal value as its start ([#5253](https://github.com/opensearch-project/sql/pull/5253))
* PPL Highlight Support ([#5234](https://github.com/opensearch-project/sql/pull/5234))
* Support creating/updating prometheus rules ([#5228](https://github.com/opensearch-project/sql/pull/5228))
* Change the final output result of struct from list to map ([#5227](https://github.com/opensearch-project/sql/pull/5227))
* added cloudwatch style contains operator ([#5219](https://github.com/opensearch-project/sql/pull/5219))
* Update graphlookup syntax ([#5209](https://github.com/opensearch-project/sql/pull/5209))
* Onboard code diff analyzer and reviewer (sql) ([#5183](https://github.com/opensearch-project/sql/pull/5183))
* Add grammar bundle generation API for PPL language features ([#5162](https://github.com/opensearch-project/sql/pull/5162))
* Support PPL queries when having trailing pipes and/or empty pipes ([#5161](https://github.com/opensearch-project/sql/pull/5161))
* Bump ANTLR Version to 4.13.2 ([#5159](https://github.com/opensearch-project/sql/pull/5159))
* feat: Implement PPL convert command with 5 conversion functions ([#5157](https://github.com/opensearch-project/sql/pull/5157))
* Make sql plugin aware of FIPS build param (-Pcrypto.standard=FIPS-140-3) ([#5155](https://github.com/opensearch-project/sql/pull/5155))
* PPL Command: MvExpand ([#5144](https://github.com/opensearch-project/sql/pull/5144))
* Add auto-extract mode for `spath` command ([#5140](https://github.com/opensearch-project/sql/pull/5140))
* Support bi-directional graph traversal command `graphlookup` ([#5138](https://github.com/opensearch-project/sql/pull/5138))
* Add nomv command ([#5130](https://github.com/opensearch-project/sql/pull/5130))
* Improve resource monitor errors ([#5129](https://github.com/opensearch-project/sql/pull/5129))
* Support fetch\_size API for PPL ([#5109](https://github.com/opensearch-project/sql/pull/5109))
* LAST/FIRST/TAKE aggregation should support TEXT type and Scripts ([#5091](https://github.com/opensearch-project/sql/pull/5091))
* fieldformat command implementation ([#5080](https://github.com/opensearch-project/sql/pull/5080))
* Implement `reverse` performance optimization ([#4775](https://github.com/opensearch-project/sql/pull/4775))


## ENHANCEMENTS


### OpenSearch Alerting


* Set `cancelAfterTimeInterval` on all remaining `SearchRequest` constructions in monitor runners to prevent premature search cancellation ([#2042](https://github.com/opensearch-project/alerting/pull/2042))
* Limit verbose log output on scheduled migration cancellation to reduce log noise during index creation ([#1738](https://github.com/opensearch-project/alerting/pull/1738))


### OpenSearch Common Utils


* Remove hardcoded trigger limit from Monitor data class and make trigger count per monitor configurable ([#913](https://github.com/opensearch-project/common-utils/pull/913))
* Validate that api\_type matches path in ClusterMetricsInput to prevent mismatched monitor configurations ([#912](https://github.com/opensearch-project/common-utils/pull/912))


### OpenSearch Custom Codecs


* Explicitly publish custom codecs zip to Maven local ([#321](https://github.com/opensearch-project/custom-codecs/pull/321))


### OpenSearch Dashboards Investigation


* Update investigation tool result style to align with chat ([#319](https://github.com/opensearch-project/dashboards-investigation/pull/319))
* Show absolute time in reinvestigation time picker and enlarge modal for full text display ([#318](https://github.com/opensearch-project/dashboards-investigation/pull/318))
* Update wording of investigation detail card and fix missing workspace in investigation URL ([#338](https://github.com/opensearch-project/dashboards-investigation/pull/338))
* Increase summary agent timeout to 60 seconds and enhance error handling ([#334](https://github.com/opensearch-project/dashboards-investigation/pull/334))
* Increase polling retry count for trace and step ([#327](https://github.com/opensearch-project/dashboards-investigation/pull/327))
* Improve error handling for invalid PPL queries and fix investigation steps style ([#335](https://github.com/opensearch-project/dashboards-investigation/pull/335))


### OpenSearch Dashboards Notifications


* Upgrade to React 18 and fix unit tests to accommodate the upgrade ([#419](https://github.com/opensearch-project/dashboards-notifications/pull/419))


### OpenSearch Dashboards Observability


* Use OpenSearch Dashboards core APM topology package instead of external npm dependency ([#2611](https://github.com/opensearch-project/dashboards-observability/pull/2611))
* Update lodash to 4.18.1 to address CVE-2026-4800 ([#2636](https://github.com/opensearch-project/dashboards-observability/pull/2636))


### OpenSearch Dashboards Search Relevance


* Proper support of .ndjson or .jsonl for Query Sets file uploads. ([#775](https://github.com/opensearch-project/dashboards-search-relevance/pull/775))
* Add resizable query editor boxes with drag handles for vertical expansion in Query Compare view. ([#791](https://github.com/opensearch-project/dashboards-search-relevance/pull/791))
* Standardize Action button tooltips across all listing pages (Search Configurations, Experiments, Judgments, Query Sets) using `EuiToolTip` for improved UX and accessibility. ([#782](https://github.com/opensearch-project/dashboards-search-relevance/pull/782))
* Remove milliseconds from timestamp display format across all listing tables. ([#799](https://github.com/opensearch-project/dashboards-search-relevance/pull/799))
* Change Single Query Comparison to Query Analysis ([#773](https://github.com/opensearch-project/dashboards-search-relevance/pull/773))


### OpenSearch ML Commons


* Add more detailed logging to Agent Workflow to enable debugging and metric collection ([#4681](https://github.com/opensearch-project/ml-commons/pull/4681))
* Allow overwrite during execute for inline create context management during agent register ([#4637](https://github.com/opensearch-project/ml-commons/pull/4637))
* Add helper method for Nova clean request ([#4676](https://github.com/opensearch-project/ml-commons/pull/4676))
* Override ValidatingObjectInputStream.resolveClass() to support plugin classloader fallback ([#4692](https://github.com/opensearch-project/ml-commons/pull/4692))
* Restore AGUI context for legacy interface agent ([#4720](https://github.com/opensearch-project/ml-commons/pull/4720))
* Escape tool name and description to handle quotation marks properly ([#4747](https://github.com/opensearch-project/ml-commons/pull/4747))


### OpenSearch Notifications


* Define mavenLocal ordering properly for both jars and zips ([#1152](https://github.com/opensearch-project/notifications/pull/1152))


### OpenSearch Query Insights Dashboards


* Switch latency graphs from Plotly to React ECharts for consistency ([#487](https://github.com/opensearch-project/query-insights-dashboards/pull/487))


### OpenSearch Search Relevance


* Allow demo scripts to be run from any directory and point to any OpenSearch server. ([#415](https://github.com/opensearch-project/search-relevance/pull/415))


### OpenSearch Security


* Optimize getFieldFilter to only return a predicate when an index has FLS restrictions for the user ([#5777](https://github.com/opensearch-project/security/pull/5777))
* Optimize string matching for RoleBasedActionPrivileges with prefix and exact pattern matching ([#5988](https://github.com/opensearch-project/security/pull/5988))
* Harden input validation for resource sharing APIs ([#5831](https://github.com/opensearch-project/security/pull/5831))
* Make encryption\_key optional for on-behalf-of token authenticator ([#6017](https://github.com/opensearch-project/security/pull/6017))
* Allow specifying default access level in resource access levels YAML file ([#6018](https://github.com/opensearch-project/security/pull/6018))
* Use custom action prefixes for sample resource plugin ([#6020](https://github.com/opensearch-project/security/pull/6020))
* Make security plugin aware of FIPS build parameter for BouncyCastle FIPS jar handling ([#5952](https://github.com/opensearch-project/security/pull/5952))


### OpenSearch Skills


* Add filter support for LogPatternAnalysisTool to enable log pattern analysis for specific services ([#707](https://github.com/opensearch-project/skills/pull/707))
* Update default tool descriptions for LogPatternAnalysisTool and DataDistributionTool to improve clarity for LLM usage ([#703](https://github.com/opensearch-project/skills/pull/703))


### OpenSearch k-NN


* Refactor ExactSearcher to use Lucene's VectorScorer API with batch scoring instead of ExactKNNIterator ([#3207](https://github.com/opensearch-project/k-NN/pull/3207))
* Integrate prefetch with FP16-based index for memory-optimized search ([#3195](https://github.com/opensearch-project/k-NN/pull/3195))
* Integrate prefetch for SparseFloatVectorValues with Faiss indices ([#3197](https://github.com/opensearch-project/k-NN/pull/3197))
* Decouple native SIMD scoring selection from FaissMemoryOptimizedSearcher into FlatVectorsScorer decorator ([#3184](https://github.com/opensearch-project/k-NN/pull/3184))
* Speed up FP16 bulk similarity by precomputing the tail mask, yielding up to 35% performance gain ([#3172](https://github.com/opensearch-project/k-NN/pull/3172))
* Adjust merge policy settings to make merges less aggressive, reducing CPU impact during concurrent search and indexing ([#3128](https://github.com/opensearch-project/k-NN/pull/3128))
* Use correct vector scorer when segments are initialized via SPI and correct maxConn for memory-optimized search ([#3117](https://github.com/opensearch-project/k-NN/pull/3117))
* Optimize ByteVectorIdsExactKNNIterator by moving float-to-byte array conversion to constructor ([#3171](https://github.com/opensearch-project/k-NN/pull/3171))
* Improve unit tests by tightening assertions ([#3112](https://github.com/opensearch-project/k-NN/pull/3112))


## BUG FIXES


### OpenSearch Alerting


* Preserve user authentication context when stashing thread context during alert notification sending, fixing SMTP STARTTLS failures ([#2027](https://github.com/opensearch-project/alerting/pull/2027))
* Fix NullPointerException when nested field type has no properties in doc-level monitor creation ([#2049](https://github.com/opensearch-project/alerting/pull/2049))
* Replace `_id` sort with `_seq_no` in JobSweeper to fix fielddata error when `indices.id_field_data.enabled` is false ([#2039](https://github.com/opensearch-project/alerting/pull/2039))


### OpenSearch Alerting Dashboards Plugin


* Fix acknowledge alerts modal to properly update table with acknowledged alerts instead of showing a stuck loading state ([#1363](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1363))
* Fix broken anomaly detector monitor definition method in OpenSearch UI ([#1371](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1371))


### OpenSearch Common Utils


* Normalize cluster metrics input URI path during validation to fix exception when path lacks leading slash ([#921](https://github.com/opensearch-project/common-utils/pull/921))
* Revert addition of Target object for external data source support on Monitor and Alert models ([#917](https://github.com/opensearch-project/common-utils/pull/917))


### OpenSearch Cross Cluster Replication


* Fix typo in `validFileNameExcludingAsterisk` to align with core OpenSearch fix ([#1639](https://github.com/opensearch-project/cross-cluster-replication/pull/1639))
* Fix ReplicationEngine to construct lightweight replica-origin copies of Index/Delete operations for non-primary planning path, resolving compilation and assertion failures after core refactor ([#1647](https://github.com/opensearch-project/cross-cluster-replication/pull/1647))


### OpenSearch Dashboards Investigation


* Fix JSON escape issue in Vega Express where backslash-n was parsed as real line breaks ([#328](https://github.com/opensearch-project/dashboards-investigation/pull/328))
* Fix chat integration type conflict to ensure correct chat instance is used ([#329](https://github.com/opensearch-project/dashboards-investigation/pull/329))
* Fix hypothesis detail buttons placement ([#339](https://github.com/opensearch-project/dashboards-investigation/pull/339))
* Remove duplicate confirm/reject buttons on finding ([#325](https://github.com/opensearch-project/dashboards-investigation/pull/325))
* Fix wrong datasource ID being passed from chat ([#337](https://github.com/opensearch-project/dashboards-investigation/pull/337))
* Use html2canvas-pro with CSP nonce to fix content security policy violation ([#313](https://github.com/opensearch-project/dashboards-investigation/pull/313))
* Redirect when opening a notebook with incorrect type in URL ([#306](https://github.com/opensearch-project/dashboards-investigation/pull/306))


### OpenSearch Dashboards Maps


* Fixed filter by map extent ignored for geo\_shape fields [798](https://github.com/opensearch-project/dashboards-maps/pull/798)


### OpenSearch Dashboards Observability


* Fix APM logs correlation query missing dataSource for external datasources, causing 503 errors ([#2625](https://github.com/opensearch-project/dashboards-observability/pull/2625))
* Fix APM UI pagination reset, settings modal layout, and chart rendering issues ([#2618](https://github.com/opensearch-project/dashboards-observability/pull/2618))
* Fix APM metric card calculations for fault rate, latency percentiles, and throughput display ([#2624](https://github.com/opensearch-project/dashboards-observability/pull/2624))
* Fix APM metrics accuracy with server-side filtering, chart-total consistency, and throughput normalization as req/s ([#2623](https://github.com/opensearch-project/dashboards-observability/pull/2623))
* Update APM PromQL queries to use time-range aggregation and custom step sizes for accurate metric display ([#2621](https://github.com/opensearch-project/dashboards-observability/pull/2621))
* Update APM service map PPL queries and response processors to support new Data Prepper index mappings ([#2596](https://github.com/opensearch-project/dashboards-observability/pull/2596))
* Replace deprecated ad command PPL query with MLCommons RCF service in Patterns tab ([#2601](https://github.com/opensearch-project/dashboards-observability/pull/2601))


### OpenSearch Dashboards Reporting


* Fix Discover context menu detection for Reporting and fix CI workflows ([#725](https://github.com/opensearch-project/dashboards-reporting/pull/725))
* Fix selected fields order to be preserved in CSV/Excel downloads from Discover ([#689](https://github.com/opensearch-project/dashboards-reporting/pull/689))


### OpenSearch Dashboards Search Relevance


* Fix scheduler failure when cron expression is null or empty in SRW experiments by adding proper validation and handling. ([#808](https://github.com/opensearch-project/dashboards-search-relevance/pull/808))
* Fix text alignment and excessive spacing in Query Analysis results view. ([#752](https://github.com/opensearch-project/dashboards-search-relevance/pull/752))
* Allow a single query setup to be executed in the search comparison UI. ([#746](https://github.com/opensearch-project/dashboards-search-relevance/pull/746))
* Fix error when deleting judgment ratings by ensuring the judgments list refreshes correctly and removes deleted entries from UI state. ([#751](https://github.com/opensearch-project/dashboards-search-relevance/pull/751))
* Fix generic error message when uploading malformed NDJSON query sets by surfacing detailed parsing error with line numbers. ([#776](https://github.com/opensearch-project/dashboards-search-relevance/pull/776))
* Fix LLM customized prompt template ([#811](https://github.com/opensearch-project/dashboards-search-relevance/pull/811))


### OpenSearch Geospatial


* Fix typo in `plugins.geospatial.geojson.max_multi_gemoetries` setting to `plugins.geospatial.geojson.max_multi_gemoetries` ([#837](https://github.com/opensearch-project/geospatial/pull/837))


### OpenSearch Index Management


* Fix flaky rollup test by stopping jobs before index cleanup to prevent race conditions with background coroutines ([#1530](https://github.com/opensearch-project/index-management/pull/1530))
* Fix typo in `validFileNameExcludingAsterisk` validation method ([#1608](https://github.com/opensearch-project/index-management/pull/1608))


### OpenSearch Index Management Dashboards Plugin


* Fix CVE-2025-13465 security vulnerability ([#1411](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1411))
* Fix CVE-2025-15284 security vulnerability ([#1410](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1410))
* Fix CVE-2026-2739 security vulnerability ([#1412](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1412))


### OpenSearch Job Scheduler


* Fix sort field in job metadata sweep query to use `_seq_no` instead of `_id` ([#896](https://github.com/opensearch-project/job-scheduler/pull/896))


### OpenSearch ML Commons


* Fix SdkAsyncHttpClient resource leak in connector executors causing connection pool exhaustion ([#4716](https://github.com/opensearch-project/ml-commons/pull/4716))
* Fix Tags.addTag() return value not captured after immutable Tags change, causing tags to be silently dropped ([#4712](https://github.com/opensearch-project/ml-commons/pull/4712))
* Fix connection\_timeout and read\_timeout defaults from 30000 to 30 to match seconds unit ([#4759](https://github.com/opensearch-project/ml-commons/pull/4759))
* Fix numeric type preservation in ML inference query template substitution ([#4656](https://github.com/opensearch-project/ml-commons/pull/4656))
* Fix early exit in stats collector job when a connector is fetched for model details ([#4560](https://github.com/opensearch-project/ml-commons/pull/4560))
* Fix RestChatAgentIT teardown failure when AWS credentials are absent ([#4772](https://github.com/opensearch-project/ml-commons/pull/4772))
* Fix agent\_id parameter conflict by renaming to agent\_id\_log for logging to prevent infinite loop in AgentTool ([#4762](https://github.com/opensearch-project/ml-commons/pull/4762))
* Fix MCP connector setting not being respected for Agent V2 ([#4739](https://github.com/opensearch-project/ml-commons/pull/4739))
* Fix incorrect error codes when deleting memory containers and context management templates ([#4723](https://github.com/opensearch-project/ml-commons/pull/4723))
* Fix error handling to use OpenSearchException instead of OpenSearchStatusException for broader 4XX client error coverage ([#4725](https://github.com/opensearch-project/ml-commons/pull/4725))
* Fix error code for delete context management template API to return 404 instead of 500 ([#4701](https://github.com/opensearch-project/ml-commons/pull/4701))
* Fix context restoration bug where user information was missing ([#4730](https://github.com/opensearch-project/ml-commons/pull/4730))
* Fix unsupported operation issue when putting agent ID into immutable map ([#4733](https://github.com/opensearch-project/ml-commons/pull/4733))
* Fix Cohere integration test timeouts by increasing timeout to 120s and adding reachability checks ([#4767](https://github.com/opensearch-project/ml-commons/pull/4767))


### OpenSearch Neural Search


* Fix rerank processor unable to extract text from nested and dot-notation fields in document\_fields ([#1805](https://github.com/opensearch-project/neural-search/pull/1805))
* [HYBRID]: Fix relevancy bugs in hybrid query collapse ([#1753](https://github.com/opensearch-project/neural-search/pull/1753))
* [Neural] Fix issue where remote symmetric models are not supported ([#1767](https://github.com/opensearch-project/neural-search/pull/1767))
* [HYBRID]: Fix profiler support for hybrid query by unwrapping ProfileScorer to access HybridSubQueryScorer ([#1754](https://github.com/opensearch-project/neural-search/pull/1754))
* [HYBRID]: Fix missing results and ranking issue in hybrid query collapse([#1763](https://github.com/opensearch-project/neural-search/pull/1763))
* [HYBRID]: Fix HybridQueryDocIdStream by adding intoArray overridden method from upstream ([#1780](https://github.com/opensearch-project/neural-search/pull/1780))
* [HYBRID]: Block hybrid query nested inside compound queries like function\_score, constant\_score, and script\_score ([#1791](https://github.com/opensearch-project/neural-search/pull/1791))
* [HYBRID]: Replace per-group collection with flat queue in hybrid query collapse to fix score and totalHits inconsistencies ([#1787](https://github.com/opensearch-project/neural-search/pull/1787))
* [HYBRID]: Fix empty results when using profiler with hybrid query sort, pagination, or collapse ([#1794](https://github.com/opensearch-project/neural-search/pull/1794))


### OpenSearch Notifications


* Exclude transitive Bouncy Castle dependencies to resolve jar hell issue ([#1141](https://github.com/opensearch-project/notifications/pull/1141))
* Fix build failure due to Jackson version conflict ([#1151](https://github.com/opensearch-project/notifications/pull/1151))


### OpenSearch Learning To Rank Base


* Fix `LoggingSearchExtBuilder.toXContent` missing field name, which caused a `JsonGenerationException` when LTR feature logging was used with search pipelines that re-serialize the request ([#290](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/290))


### OpenSearch Performance Analyzer


* Fix CVE-2025-68161 by force resolving log4j dependencies ([#932](https://github.com/opensearch-project/performance-analyzer/pull/932))


### OpenSearch Query Insights


* Fix IS\_STREAMING\_TAG not propagated in incrementAggCounter due to immutable Tags object ([#570](https://github.com/opensearch-project/query-insights/pull/570))
* Fix MultiIndexDateRangeIT test failure ([#558](https://github.com/opensearch-project/query-insights/pull/558))
* Fix exporter retry logic for MapperParsingException by moving detection to onResponse callback ([#556](https://github.com/opensearch-project/query-insights/pull/556))
* Fix grouping field\_name/field\_type settings being overwritten to false on initialization ([#578](https://github.com/opensearch-project/query-insights/pull/578))
* Fix cluster setting validation by moving it to Setting definitions to prevent invalid persistent values ([#487](https://github.com/opensearch-project/query-insights/pull/487))
* Stop fetching security snapshot artifacts in non-snapshot builds ([#560](https://github.com/opensearch-project/query-insights/pull/560))


### OpenSearch Query Insights Dashboards


* Fix CVE-2026-26996 (minimatch ReDoS), CVE-2025-13465 (lodash prototype pollution), and CVE-2025-15284 (qs arrayLimit bypass DoS) via yarn resolutions ([#489](https://github.com/opensearch-project/query-insights-dashboards/pull/489))
* Bump serialize-javascript to 7.0.3 to address GHSA-5c6j-r48x-rmvq ([#491](https://github.com/opensearch-project/query-insights-dashboards/pull/491))
* Update lodash to 4.18.1 to address CVE-2026-4800 ([#496](https://github.com/opensearch-project/query-insights-dashboards/pull/496))


### OpenSearch Reporting


* Renamed resource-action-groups.yml to resource-access-levels.yml to fix security checks ([#1163](https://github.com/opensearch-project/reporting/pull/1163))


### OpenSearch Search Relevance


* Fixed thread pool starvation in LLM judgment processing ([#387](https://github.com/opensearch-project/search-relevance/pull/387))


### OpenSearch Security


* Fix propagation issue for security context ([#6006](https://github.com/opensearch-project/security/pull/6006))
* Fix audit log writing errors for rollover-enabled alias indices ([#5900](https://github.com/opensearch-project/security/pull/5900))
* Fix unprocessed X-Request-Id header in security plugin ([#5954](https://github.com/opensearch-project/security/pull/5954))
* Fix audit log NONE sentinel value not respected in dynamic configuration and misleading unknown setting error ([#6021](https://github.com/opensearch-project/security/pull/6021))
* Improve error message for DLS queries referencing undefined user attributes ([#5975](https://github.com/opensearch-project/security/pull/5975))


### OpenSearch Security Analytics


* Fix failure when deleting a detector with no associated rules due to empty monitor ID list ([#1648](https://github.com/opensearch-project/security-analytics/pull/1648))


### OpenSearch Security Analytics Dashboards Plugin


* Fix empty severity column in findings table ([#1392](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1392))
* Fix empty alerts table, detector creation failure propagation, blank details page redirect after successful creation, and silent failures ([#1376](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1376))


### OpenSearch k-NN


* Fix derived source with dynamic templates causing vectors to be incorrectly returned during bulk indexing ([#3035](https://github.com/opensearch-project/k-NN/pull/3035))
* Fix FaissIdMap to honor given acceptOrds for sparse case by removing double ordinal-to-docID mapping ([#3196](https://github.com/opensearch-project/k-NN/pull/3196))
* Fix radial search returning 0 results for IndexHNSWCagra by adding proper range\_search override ([#3201](https://github.com/opensearch-project/k-NN/pull/3201))
* Fix score conversion logic for filtered radial exact search with cosine space type ([#3110](https://github.com/opensearch-project/k-NN/pull/3110))
* Fix random entry point generation for CagraIndex in memory-optimized search when numVectors is less than entryPoints ([#3161](https://github.com/opensearch-project/k-NN/pull/3161))
* Fix optimistic search bugs on nested Cagra index including duplicate entry points and incorrect second deep-dive behavior ([#3155](https://github.com/opensearch-project/k-NN/pull/3155))
* Fix default encoder to SQ 1-bit for Faiss 32x compression ([#3210](https://github.com/opensearch-project/k-NN/pull/3210))
* Fix prefetch failure due to out-of-bound exception in FaissScorableByteVectorValues ([#3240](https://github.com/opensearch-project/k-NN/pull/3240))
* Fix Lucene reduce to topK when rescoring is enabled, preventing premature result reduction before rescoring phase ([#3124](https://github.com/opensearch-project/k-NN/pull/3124))
* Fix integer overflow for memory-optimized search when converting Faiss HNSW offsets from long to int ([#3130](https://github.com/opensearch-project/k-NN/pull/3130))


### OpenSearch SQL


* Fix flaky TPC-H Q1 test due to bugs in `MatcherUtils.closeTo()` ([#5283](https://github.com/opensearch-project/sql/pull/5283))
* Fix typo: rename renameClasue to renameClause ([#5252](https://github.com/opensearch-project/sql/pull/5252))
* Fix `isnotnull()` not being pushed down when combined with multiple `!=` conditions ([#5238](https://github.com/opensearch-project/sql/pull/5238))
* Fix memory leak: ExecutionEngine recreated per query appending to global function registry ([#5222](https://github.com/opensearch-project/sql/pull/5222))
* Fix PIT (Point in Time) resource leaks in v2 query engine ([#5221](https://github.com/opensearch-project/sql/pull/5221))
* Fix MAP path resolution for `top/rare`, `join`, `lookup` and `streamstats` ([#5206](https://github.com/opensearch-project/sql/pull/5206))
* Fix #5163: Return null for double overflow to Infinity in arithmetic ([#5202](https://github.com/opensearch-project/sql/pull/5202))
* Fix MAP path resolution for symbol-based PPL commands ([#5198](https://github.com/opensearch-project/sql/pull/5198))
* Fix #5176: Return actual null from JSON\_EXTRACT for missing/null paths ([#5196](https://github.com/opensearch-project/sql/pull/5196))
* Fix multisearch UDT type loss through UNION (#5145, #5146, #5147) ([#5154](https://github.com/opensearch-project/sql/pull/5154))
* Fix path navigation on map columns for `spath` command ([#5149](https://github.com/opensearch-project/sql/pull/5149))
* Fix pitest dependency resolution with stable runtime version ([#5143](https://github.com/opensearch-project/sql/pull/5143))
* Fix #5114: preserve head/TopK semantics for sort-expression pushdown ([#5135](https://github.com/opensearch-project/sql/pull/5135))
* Fix fallback error handling to show original Calcite error ([#5133](https://github.com/opensearch-project/sql/pull/5133))
* Fix the bug when boolean comparison condition is simplifed to field ([#5071](https://github.com/opensearch-project/sql/pull/5071))
* Fix issue connecting with prometheus by wrapping with AccessController.doPrivilegedChecked ([#5061](https://github.com/opensearch-project/sql/pull/5061))


## INFRASTRUCTURE


### OpenSearch Alerting


* Replace `Thread.sleep` with `OpenSearchTestCase.waitUntil` in integration tests for more reliable test execution ([#2041](https://github.com/opensearch-project/alerting/pull/2041))


### OpenSearch Anomaly Detection


* Add integration test coverage reporting and Codecov README badge ([#1679](https://github.com/opensearch-project/anomaly-detection/pull/1679))


### OpenSearch Anomaly Detection Dashboards Plugin


* Update delete\_backport\_branch workflow to also clean up release-chores branches after merge ([#1080](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1080))


### OpenSearch Common Utils


* Update shadow plugin usage to replace deprecated API in preparation for dependency upgrade ([#904](https://github.com/opensearch-project/common-utils/pull/904))


### OpenSearch Custom Codecs


* Update Gradle to 9.4.1 ([#320](https://github.com/opensearch-project/custom-codecs/pull/320))
* Update delete-backport-branch workflow to include release-chores branches ([#270](https://github.com/opensearch-project/custom-codecs/pull/270))


### OpenSearch Dashboards Reporting


* Remove unused React 16 dependencies to fix distribution build after React 18 migration ([#700](https://github.com/opensearch-project/dashboards-reporting/pull/700))


### OpenSearch Flow Framework


* Add gradle.properties file to build with FIPS 140-3 crypto standard by default ([#1344](https://github.com/opensearch-project/flow-framework/pull/1344))
* Set bc-fips dependency to compileOnly to avoid runtime conflicts ([#1346](https://github.com/opensearch-project/flow-framework/pull/1346))


### OpenSearch Index Management


* Add Remote Store integration test infrastructure with SearchOnlyActionIT for ISM testing against Remote Store enabled clusters ([#1589](https://github.com/opensearch-project/index-management/pull/1589))
* Update shadow plugin usage to replace deprecated Gradle API ([#1587](https://github.com/opensearch-project/index-management/pull/1587))


### OpenSearch Job Scheduler


* Fix integration tests with security plugin by providing FIPS build parameter ([#887](https://github.com/opensearch-project/job-scheduler/pull/887))


### OpenSearch ML Commons


* Fix ML build to adapt to Gradle shadow plugin v9 upgrade and make ml-commons FIPS build param aware ([#4654](https://github.com/opensearch-project/ml-commons/pull/4654))
* Enable FIPS flag by default on build/run ([#4719](https://github.com/opensearch-project/ml-commons/pull/4719))
* Onboard code diff analyzer and reviewer for ml-commons ([#4666](https://github.com/opensearch-project/ml-commons/pull/4666))
* Optimize integration test setup to eliminate redundant per-test work, reducing execution time by ~50% ([#4667](https://github.com/opensearch-project/ml-commons/pull/4667))
* Quote FIPS crypto standard parameter in CI workflow files for consistency ([#4659](https://github.com/opensearch-project/ml-commons/pull/4659))
* Improve CI test stability by skipping unreachable OpenAI tests and fixing flaky IndexUtilsTests ([#4668](https://github.com/opensearch-project/ml-commons/pull/4668))
* Prevent SearchModelGroupITTests timeout by disabling dedicated masters and fix Bedrock connection pool exhaustion ([#4665](https://github.com/opensearch-project/ml-commons/pull/4665))
* Upgrade Bedrock Claude models in integration tests for higher rate limits ([#4742](https://github.com/opensearch-project/ml-commons/pull/4742))
* Rename resource-action-groups.yml to resource-access-levels.yml to fix security checks ([#4737](https://github.com/opensearch-project/ml-commons/pull/4737))


### OpenSearch Neural Search


* [GRPC] Add Integration test for Hybrid Query ([#1734](https://github.com/opensearch-project/neural-search/pull/1734))
* Fix gRPC integration test port discovery for reliable local and CI execution ([#1814](https://github.com/opensearch-project/neural-search/pull/1814))
* Fix integration test health check failures in remote clusters by dynamically discovering node count and using >= syntax for wait\_for\_nodes ([#1776](https://github.com/opensearch-project/neural-search/pull/1776))


### OpenSearch Notifications


* Allow publishing plugin zip to Maven local by removing exclusion of publishPluginZipPublicationToMavenLocal task ([#1063](https://github.com/opensearch-project/notifications/pull/1063))
* Update shadow plugin usage to replace deprecated API ([#1138](https://github.com/opensearch-project/notifications/pull/1138))


### OpenSearch Learning To Rank Base


* Fix Windows CI build failure by removing Spotless P2 mirror dependency and resolving from Maven Central instead ([#305](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/305))


### OpenSearch Performance Analyzer


* Disable dependencyLicenses check to align with other plugin repos ([#926](https://github.com/opensearch-project/performance-analyzer/pull/926))
* Make performance-analyzer plugin aware of FIPS build parameter for proper BouncyCastle dependency handling ([#915](https://github.com/opensearch-project/performance-analyzer/pull/915))


### OpenSearch Query Insights


* Enable internalClusterTest and yamlRestTest tasks and fix uncovered test issues ([#522](https://github.com/opensearch-project/query-insights/pull/522))
* Exclude RemoteRepositoryExporterIT and TopQueriesRbacIT from integTestRemote ([#577](https://github.com/opensearch-project/query-insights/pull/577))
* Fix integTestRemote task spinning up unnecessary test cluster nodes by changing task type ([#587](https://github.com/opensearch-project/query-insights/pull/587))
* Revert cluster health check before running integration tests ([#594](https://github.com/opensearch-project/query-insights/pull/594))
* Add cluster health check before running integration tests to prevent connection failures ([#588](https://github.com/opensearch-project/query-insights/pull/588))
* Pin LocalStack version to v4.4 and increase health check timeout for CI stability ([#572](https://github.com/opensearch-project/query-insights/pull/572))


### OpenSearch Query Insights Dashboards


* Remove flaky verbose=false API schema test from Cypress that was failing due to timing sensitivity ([#480](https://github.com/opensearch-project/query-insights-dashboards/pull/480))
* Use poll-based check in Cypress beforeEach for improved test reliability ([#482](https://github.com/opensearch-project/query-insights-dashboards/pull/482))
* Pin Gradle wrapper version in Cypress workflows to prevent Gradle 9.x download and fix related CI issues ([#484](https://github.com/opensearch-project/query-insights-dashboards/pull/484))


### OpenSearch Search Relevance


* Fix flaky DCG and MRR assertions in integration tests ([#427](https://github.com/opensearch-project/search-relevance/pull/427))


### OpenSearch Security Analytics Dashboards Plugin


* Upgrade to React 18 and update unit tests to accommodate the upgrade ([#1376](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1376))


### OpenSearch k-NN


* Fix k-NN build and run compatibility with Lucene 10.4.0 upgrade ([#3135](https://github.com/opensearch-project/k-NN/pull/3135))


### OpenSearch SQL


* Add gradle.properties file to build sql with -Pcrypto.standard=FIPS-140-3 by default ([#5231](https://github.com/opensearch-project/sql/pull/5231))
* Fix the flaky yamlRestTest caused by order of sample\_logs ([#5119](https://github.com/opensearch-project/sql/pull/5119))
* Fix the filter of integTestWithSecurity ([#5098](https://github.com/opensearch-project/sql/pull/5098))


## DOCUMENTATION


### OpenSearch SQL


* Apply docs website feedback to ppl functions ([#5207](https://github.com/opensearch-project/sql/pull/5207))


## MAINTENANCE


### OpenSearch Alerting


* Change Gradle wrapper from 9.2.0 to 9.4.0 ([#2040](https://github.com/opensearch-project/alerting/pull/2040))
* Update shadow plugin usage to replace deprecated API ([#2022](https://github.com/opensearch-project/alerting/pull/2022))
* Remove experimental PPL alerting feature assets pending refactoring for a future release ([#2017](https://github.com/opensearch-project/alerting/pull/2017))
* Inject SdkClient into transport actions for SDK persistence support ([#2052](https://github.com/opensearch-project/alerting/pull/2052))
* Integrate remote metadata SDK client with alerting plugin ([#2047](https://github.com/opensearch-project/alerting/pull/2047))
* Revert SdkClient changes merged during code freeze ([#2057](https://github.com/opensearch-project/alerting/pull/2057))


### OpenSearch Alerting Dashboards Plugin


* Resolve CVE-2026-26996 and CVE-2026-2739 ([#1393](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1393))
* Update lodash to 4.18.1 to address CVE-2026-4800 ([#1400](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1400))
* Update lodash to 4.18.1 follow-up fix for CVE-2026-4800 ([#1404](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1404))
* Upgrade to React 18 and fix unit tests to accommodate the upgrade ([#1369](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1369))


### OpenSearch Anomaly Detection Dashboards Plugin


* Bump axios from 1.12.1 to 1.13.5 to address security and bug fixes ([#1145](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1145))
* Bump brace-expansion and elliptic to resolve CVE-2025-5889 and CVE-2025-14505 ([#1148](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1148))
* Bump minimatch and bn.js to resolve CVE-2026-26996 and CVE-2026-2739 ([#1152](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1152))
* Upgrade minimatch to 10.2.4 to fix CVE-2026-27903 and CVE-2026-27904 ([#1158](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1158))
* Update lodash to 4.18.1 to address CVE-2026-4800 ([#1165](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1165))
* Upgrade anomaly detection plugin to React 18 ([#1144](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1144))


### OpenSearch Common Utils


* Bump logback from 1.5.19 to 1.5.32 ([#907](https://github.com/opensearch-project/common-utils/pull/907))


### OpenSearch Cross Cluster Replication


* Upgrade filelock to 3.20.3 to address CVE-2025-68146 and CVE-2026-22701 race condition vulnerabilities ([#1637](https://github.com/opensearch-project/cross-cluster-replication/pull/1637))
* Fix CVE-2026-25645 and CVE-2026-24400 ([#1650](https://github.com/opensearch-project/cross-cluster-replication/pull/1650))


### OpenSearch Custom Codecs


* Bump QAT-Java to 2.4.0 and avoid unnecessary array copies in compression and decompression ([#319](https://github.com/opensearch-project/custom-codecs/pull/319))
* Update backward compatibility build framework version to OpenSearch 3.6 ([#322](https://github.com/opensearch-project/custom-codecs/pull/322))
* Update for Lucene 10.4 compatibility ([#311](https://github.com/opensearch-project/custom-codecs/pull/311))
* Add release notes for 2.19.5 ([#318](https://github.com/opensearch-project/custom-codecs/pull/318))


### OpenSearch Dashboards Assistant


* Bump dompurify from 3.2.4 to 3.3.2 ([#663](https://github.com/opensearch-project/dashboards-assistant/pull/663))
* Update lodash to 4.18.1 ([#667](https://github.com/opensearch-project/dashboards-assistant/pull/667))
* Bump ajv to 6.14.0, lodash to 4.17.23, and minimatch to 3.1.5 ([#656](https://github.com/opensearch-project/dashboards-assistant/pull/656))


### OpenSearch Dashboards Investigation


* Bump ajv from 8.12.0 to 8.18.0 ([#317](https://github.com/opensearch-project/dashboards-investigation/pull/317))
* Bump dompurify from 3.3.1 to 3.3.2 ([#333](https://github.com/opensearch-project/dashboards-investigation/pull/333))
* Resolve CVE-2026-26996 and CVE-2025-64718 ([#343](https://github.com/opensearch-project/dashboards-investigation/pull/343))
* Update lodash to 4.18.1 to address CVE-2026-4800 ([#348](https://github.com/opensearch-project/dashboards-investigation/pull/348))
* Force flatted to 3.4.2 to resolve CVE-2026-33228 ([#340](https://github.com/opensearch-project/dashboards-investigation/pull/340))


### OpenSearch Dashboards Maps


* React 18 compatibility updates for dashboards-maps plugin [#789](https://github.com/opensearch-project/dashboards-maps/pull/789)


### OpenSearch Dashboards Notifications


* Resolve CVE-2025-13465 and CVE-2025-15284 ([#432](https://github.com/opensearch-project/dashboards-notifications/pull/432))
* Update lodash to 4.18.1 to address CVE-2026-4800 ([#434](https://github.com/opensearch-project/dashboards-notifications/pull/434))


### OpenSearch Dashboards Observability


* Bump ajv from 8.12.0 to 8.18.0 ([#2595](https://github.com/opensearch-project/dashboards-observability/pull/2595))
* Bump picomatch from 2.3.1 to 2.3.2 to address CVE-2026-33671 and CVE-2026-33672 ([#2627](https://github.com/opensearch-project/dashboards-observability/pull/2627))
* Bump dompurify from 3.3.0 to 3.3.3 and minimatch to 3.1.5 ([#2632](https://github.com/opensearch-project/dashboards-observability/pull/2632))
* Bump serialize-javascript and scoped ajv transitive dependencies ([#2633](https://github.com/opensearch-project/dashboards-observability/pull/2633))
* Remove unused qs library ([#2605](https://github.com/opensearch-project/dashboards-observability/pull/2605))


### OpenSearch Dashboards Query Workbench


* Update lodash to 4.18.1 to address CVE-2026-4800 ([#539](https://github.com/opensearch-project/dashboards-query-workbench/pull/539))
* Bump qs version to resolve CVE-2025-15284 ([#537](https://github.com/opensearch-project/dashboards-query-workbench/pull/537))
* Bump ajv, minimatch, lodash, and picomatch dependencies ([#533](https://github.com/opensearch-project/dashboards-query-workbench/pull/533))


### OpenSearch Dashboards Reporting


* Bump bn.js from 4.12.0 to 4.12.3 ([#693](https://github.com/opensearch-project/dashboards-reporting/pull/693))
* Bump dompurify from 3.3.1 to 3.3.3 ([#699](https://github.com/opensearch-project/dashboards-reporting/pull/699))
* Bump jspdf from 4.1.0 to 4.2.1 to address security vulnerabilities ([#698](https://github.com/opensearch-project/dashboards-reporting/pull/698))
* Bump lodash from 4.17.21 to 4.17.23 ([#672](https://github.com/opensearch-project/dashboards-reporting/pull/672))
* Bump picomatch from 2.3.1 to 2.3.2 to address security vulnerabilities ([#714](https://github.com/opensearch-project/dashboards-reporting/pull/714))
* Bump qs dependency to 6.15.0 to resolve CVE-2025-15284 ([#720](https://github.com/opensearch-project/dashboards-reporting/pull/720))
* Bump yaml from 2.3.4 to 2.8.3 ([#713](https://github.com/opensearch-project/dashboards-reporting/pull/713))
* Update lodash to 4.18.1 to resolve CVE-2026-4800 ([#729](https://github.com/opensearch-project/dashboards-reporting/pull/729))
* Bump minimatch to 3.1.5 ([#715](https://github.com/opensearch-project/dashboards-reporting/pull/715))


### OpenSearch Dashboards Search Relevance


* React 18 compatibility updates for dashboards-search-relevance plugin ([#741](https://github.com/opensearch-project/dashboards-search-relevance/pull/741))


### OpenSearch Index Management


* Bump commons-codec:commons-codec from 1.17.2 to 1.21.0 ([#1578](https://github.com/opensearch-project/index-management/pull/1578))


### OpenSearch Index Management Dashboards Plugin


* Update lodash to 4.18.1 to address CVE-2026-4800 ([#1418](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1418))
* Upgrade React from 16 to 18, fixing CVE-2025-64718 and resolving failing Cypress tests ([#1391](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1391))


### OpenSearch Job Scheduler


* Update shadow plugin usage to replace deprecated API ([#884](https://github.com/opensearch-project/job-scheduler/pull/884))
* Bump `actions/download-artifact` from 7 to 8 ([#886](https://github.com/opensearch-project/job-scheduler/pull/886))
* Bump `actions/upload-artifact` from 6 to 7 ([#885](https://github.com/opensearch-project/job-scheduler/pull/885))
* Bump `aws-actions/configure-aws-credentials` from 5 to 6 ([#883](https://github.com/opensearch-project/job-scheduler/pull/883))
* Bump `de.undercouch.download` from 5.6.0 to 5.7.0 ([#882](https://github.com/opensearch-project/job-scheduler/pull/882))
* Bump gradle-wrapper from 9.2.0 to 9.4.0 ([#891](https://github.com/opensearch-project/job-scheduler/pull/891))
* Bump gradle-wrapper from 9.4.0 to 9.4.1 ([#894](https://github.com/opensearch-project/job-scheduler/pull/894))
* Bump `release-drafter/release-drafter` from 6 to 7 ([#893](https://github.com/opensearch-project/job-scheduler/pull/893))


### OpenSearch ML Commons Dashboards


* Bump picomatch from 2.3.1 to 2.3.2 to address security vulnerabilities ([#475](https://github.com/opensearch-project/ml-commons-dashboards/pull/475))


### OpenSearch Neural Search


* [HYBRID]: Clean up dead code and add missing test coverage for HybridQueryDocIdStream intoArray method ([#1786](https://github.com/opensearch-project/neural-search/pull/1786))


### OpenSearch Notifications


* Add multi\_tenancy\_enabled setting and update settings prefix ([#1148](https://github.com/opensearch-project/notifications/pull/1148))


### OpenSearch Observability


* Fix CI checks by downloading plugin snapshots for testing from ci.opensearch.org ([#1973](https://github.com/opensearch-project/observability/pull/1973))
* Replace java.security.AccessController with org.opensearch.secure\_sm.AccessController ([#1974](https://github.com/opensearch-project/observability/pull/1974))
* Bump assertj-core to 3.27.7 ([#1981](https://github.com/opensearch-project/observability/pull/1981))


### OpenSearch Reporting


* Bump assertj-core to 3.27.7 ([#1166](https://github.com/opensearch-project/reporting/pull/1166))


### OpenSearch Security


* Bump actions/download-artifact from 7 to 8 ([#5979](https://github.com/opensearch-project/security/pull/5979))
* Bump actions/upload-artifact from 6 to 7 ([#5980](https://github.com/opensearch-project/security/pull/5980))
* Bump at.yawk.lz4:lz4-java from 1.10.3 to 1.10.4 ([#5994](https://github.com/opensearch-project/security/pull/5994))
* Bump at.yawk.lz4:lz4-java from 1.10.3 to 1.10.4 ([#6028](https://github.com/opensearch-project/security/pull/6028))
* Bump aws-actions/configure-aws-credentials from 5 to 6 ([#5946](https://github.com/opensearch-project/security/pull/5946))
* Bump ch.qos.logback:logback-classic from 1.5.26 to 1.5.28 ([#5948](https://github.com/opensearch-project/security/pull/5948))
* Bump ch.qos.logback:logback-classic from 1.5.28 to 1.5.32 ([#5995](https://github.com/opensearch-project/security/pull/5995))
* Bump com.autonomousapps.build-health from 3.5.1 to 3.6.1 ([#6029](https://github.com/opensearch-project/security/pull/6029))
* Bump com.carrotsearch.randomizedtesting:randomizedtesting-runner from 2.8.3 to 2.8.4 ([#5993](https://github.com/opensearch-project/security/pull/5993))
* Bump com.github.seancfoley:ipaddress from 5.5.1 to 5.6.1 ([#5949](https://github.com/opensearch-project/security/pull/5949))
* Bump com.github.seancfoley:ipaddress from 5.6.1 to 5.6.2 ([#6010](https://github.com/opensearch-project/security/pull/6010))
* Bump com.google.googlejavaformat:google-java-format from 1.33.0 to 1.34.1 ([#5947](https://github.com/opensearch-project/security/pull/5947))
* Bump com.google.googlejavaformat:google-java-format from 1.34.1 to 1.35.0 ([#6011](https://github.com/opensearch-project/security/pull/6011))
* Bump com.nimbusds:nimbus-jose-jwt from 10.7 to 10.8 ([#6030](https://github.com/opensearch-project/security/pull/6030))
* Bump gradle-wrapper from 9.2.0 to 9.4.0 ([#5996](https://github.com/opensearch-project/security/pull/5996))
* Bump jakarta.xml.bind:jakarta.xml.bind-api from 4.0.4 to 4.0.5 ([#5978](https://github.com/opensearch-project/security/pull/5978))
* Bump kafka\_version from 4.1.1 to 4.2.0 ([#5968](https://github.com/opensearch-project/security/pull/5968))
* Bump net.bytebuddy:byte-buddy from 1.18.4 to 1.18.7 ([#6012](https://github.com/opensearch-project/security/pull/6012))
* Bump open\_saml\_shib\_version from 9.2.0 to 9.2.1 ([#5982](https://github.com/opensearch-project/security/pull/5982))
* Bump open\_saml\_version from 5.1.6 to 5.2.1 ([#5965](https://github.com/opensearch-project/security/pull/5965))
* Bump org.checkerframework:checker-qual from 3.53.0 to 3.53.1 ([#5955](https://github.com/opensearch-project/security/pull/5955))
* Bump org.checkerframework:checker-qual from 3.53.1 to 3.54.0 ([#6009](https://github.com/opensearch-project/security/pull/6009))
* Bump org.eclipse.platform:org.eclipse.core.runtime from 3.34.100 to 3.34.200 ([#6027](https://github.com/opensearch-project/security/pull/6027))
* Bump org.junit.jupiter:junit-jupiter-api from 5.14.2 to 5.14.3 ([#5956](https://github.com/opensearch-project/security/pull/5956))
* Bump org.springframework.kafka:spring-kafka-test from 4.0.2 to 4.0.3 ([#5981](https://github.com/opensearch-project/security/pull/5981))
* Bump org.springframework.kafka:spring-kafka-test from 4.0.3 to 4.0.4 ([#6026](https://github.com/opensearch-project/security/pull/6026))
* Bump release-drafter/release-drafter from 6 to 7 ([#6007](https://github.com/opensearch-project/security/pull/6007))
* Bump spring\_version from 7.0.3 to 7.0.4 ([#5957](https://github.com/opensearch-project/security/pull/5957))
* Bump spring\_version from 7.0.4 to 7.0.5 ([#5967](https://github.com/opensearch-project/security/pull/5967))
* Bump spring\_version from 7.0.5 to 7.0.6 ([#6008](https://github.com/opensearch-project/security/pull/6008))


### OpenSearch Security Analytics


* Update security-analytics-commons jar to address CVE-2025-67735 ([#1653](https://github.com/opensearch-project/security-analytics/pull/1653))
* Update security-analytics-commons jar to address CVE-2026-33871 and CVE-2026-33870 ([#1685](https://github.com/opensearch-project/security-analytics/pull/1685))


### OpenSearch Security Analytics Dashboards Plugin


* Resolve CVE-2026-26996, CVE-2026-2739, and CVE-2025-15284 ([#1389](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1389))
* Update lodash to 4.18.1 to address CVE-2026-4800 ([#1394](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1394))


### OpenSearch Security Dashboards Plugin


* Force resolution of basic-ftp to 5.2.0 to address dependency issue ([#2374](https://github.com/opensearch-project/security-dashboards-plugin/pull/2374))
* Upgrade to React 18 and adapt unit tests for compatibility ([#2371](https://github.com/opensearch-project/security-dashboards-plugin/pull/2371))
* Update lodash to 4.18.1 to address CVE-2026-4800 ([#2402](https://github.com/opensearch-project/security-dashboards-plugin/pull/2402))


### OpenSearch Skills


* Update Apache Spark dependencies (spark-common-utils\_2.13) from 3.5.4 to 3.5.8 ([#713](https://github.com/opensearch-project/skills/pull/713))


### OpenSearch k-NN


* Update changelog ([#3252](https://github.com/opensearch-project/k-NN/pull/3252))
* Fix KNN1030Codec to properly support delegation for non-default codecs on the read path ([#3093](https://github.com/opensearch-project/k-NN/pull/3093))


### OpenSearch SQL


* Move some maintainers from active to Emeritus ([#5260](https://github.com/opensearch-project/sql/pull/5260))
* Add CLAUDE.md ([#5259](https://github.com/opensearch-project/sql/pull/5259))
* Add songkant-aws as maintainer ([#5244](https://github.com/opensearch-project/sql/pull/5244))
* Add ahkcs as maintainer ([#5223](https://github.com/opensearch-project/sql/pull/5223))
* Fix bc-fips jar hell by marking dependency as compileOnly ([#5158](https://github.com/opensearch-project/sql/pull/5158))
* Revert dynamic column support ([#5139](https://github.com/opensearch-project/sql/pull/5139))
* Increment version to 3.6.0-SNAPSHOT ([#5115](https://github.com/opensearch-project/sql/pull/5115))
* Upgrade assertj-core to 3.27.7 ([#5100](https://github.com/opensearch-project/sql/pull/5100))


## REFACTORING


### OpenSearch Alerting Dashboards Plugin


* Refactor PPL alerting APIs to use v1 endpoints ([#1378](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1378))
* Remove legacy and PPL alerting separation ([#1392](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1392))


### OpenSearch Search Relevance


* Extract reusable BatchedAsyncExecutor; migrate LlmJudgmentTaskManager and ExperimentTaskManager to use it ([#392](https://github.com/opensearch-project/search-relevance/pull/392))


### OpenSearch k-NN


* Simplify DerivedSourceReaders lifecycle by removing manual ref-counting and aligning with Lucene's ownership model ([#3138](https://github.com/opensearch-project/k-NN/pull/3138))


