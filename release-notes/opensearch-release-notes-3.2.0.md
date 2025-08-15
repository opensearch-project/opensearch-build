# OpenSearch and OpenSearch Dashboards 3.2.0 Release Notes

## Release Highlights

### New and Updated Features
### Experimental Features


## Release Details
[OpenSearch and OpenSearch Dashboards 3.2.0](https://opensearch.org/artifacts/by-version/#release-3-2-0) includes the following breaking changes, features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.2.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.2.0.md).


## FEATURES


### OpenSearch Common Utils


* Add Seconds as a supported unit for IntervalSchedule ([#849](https://github.com/opensearch-project/common-utils/pull/849))


### OpenSearch Custom Codecs


* Adding support for composite index ([#263](https://github.com/opensearch-project/custom-codecs/pull/263))


### OpenSearch Search Relevance Dashboards


* Use Dashboards to visualize results of Evaluation and Hybrid Experiments ([#570](https://github.com/opensearch-project/dashboards-search-relevance/pull/570))
* Enable AutoPopulated Fields in SearchRelevance Query Compare Plugin Page ([#577](https://github.com/opensearch-project/dashboards-search-relevance/pull/577))
* Add polling mechanism to experiment\_listing and judgment\_listing view ([#594](https://github.com/opensearch-project/dashboards-search-relevance/pull/594))
* Add startDate and endDate for implicit judgment form ([#604](https://github.com/opensearch-project/dashboards-search-relevance/pull/604/files))
* Change default UI to the new SRW interface, preserve opt out option ([#614](https://github.com/opensearch-project/dashboards-search-relevance/pull/614))


### OpenSearch Flow Framework


* Add JsonToJson Recommender as a utility function ([#1168](https://github.com/opensearch-project/flow-framework/pull/1168))
* Add JsonToJson Transformer as a utility function ([#1176](https://github.com/opensearch-project/flow-framework/pull/1176))


### OpenSearch Index Management


* Support for no\_alias and min\_state\_age in ISM TransitionsFeature/ism enhancement ([#1440](https://github.com/opensearch-project/index-management/pull/1440))


### OpenSearch Job Scheduler


* Adds REST API to list jobs with an option to list them per node ([#786](https://github.com/opensearch-project/job-scheduler/pull/786))
* Support defining IntervalSchedule in seconds ([#796](https://github.com/opensearch-project/job-scheduler/pull/796))
* Rest API to list all locks with option to get a specific lock ([#802](https://github.com/opensearch-project/job-scheduler/pull/802))


### OpenSearch k-NN


* Support GPU indexing for FP16, Byte and Binary [#2819](https://github.com/opensearch-project/k-NN/pull/2819)
* Add random rotation feature to binary encoder for improving recall on certain datasets [#2718](https://github.com/opensearch-project/k-NN/pull/2718)
* Asymmetric Distance Computation (ADC) for binary quantized faiss indices [#2733](https://github.com/opensearch-project/k-NN/pull/2733)
* Extend transport-grpc module to support GRPC KNN queries [#2817](https://github.com/opensearch-project/k-NN/pull/2817)


### OpenSearch ML Commons


* Initiate query planning tool ([#4006](https://github.com/opensearch-project/ml-commons/pull/4006))
* Add Execute Tool API ([#4035](https://github.com/opensearch-project/ml-commons/pull/4035))
* Implement create and add memory container API ([#4050](https://github.com/opensearch-project/ml-commons/pull/4050))
* Enable AI-Oriented memory operation on Memory APIs (Add, Search, Update & Delete) ([#4055](https://github.com/opensearch-project/ml-commons/pull/4055))
* Support output filter, unify tool parameter handling and improve SearchIndexTool output parsing ([#4053](https://github.com/opensearch-project/ml-commons/pull/4053))
* Delete memory container API ([#4027](https://github.com/opensearch-project/ml-commons/pull/4027))
* GET memory API ([#4069](https://github.com/opensearch-project/ml-commons/pull/4069))


### OpenSearch Neural Search


* [Hybrid Query] Add upper bound parameter for min-max normalization technique ([#1431](https://github.com/opensearch-project/neural-search/pull/1431))
* [Experimental] Adds agentic search query clause and agentic query translator search request processor for agentic search ([#1484](https://github.com/opensearch-project/neural-search/pull/1484))


### OpenSearch Learning To Rank Base


* Add support to handle missing values for XGBoost models ([#206](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/206))


### OpenSearch Security


* Introduced new experimental versioned security configuration management feature ([#5357](https://github.com/opensearch-project/security/pull/5357))
* [Resource Sharing] Adds migrate API to move resource-sharing info to security plugin ([#5389](https://github.com/opensearch-project/security/pull/5389))
* Introduces support for the Argon2 Password Hashing Algorithm ([#5441](https://github.com/opensearch-project/security/pull/5441))
* Introduced permission validation support using query parameter without executing the request ([#5496](https://github.com/opensearch-project/security/pull/5496))
* Add support for configuring auxiliary transports for SSL only ([#5375](https://github.com/opensearch-project/security/pull/5375))
* Introduced SPIFFE X.509 SVID support via SPIFFEPrincipalExtractor ([#5521](https://github.com/opensearch-project/security/pull/5521))


## ENHANCEMENTS


### OpenSearch Anomaly Detection


* Support >1 hr intervals ([#1513](https://github.com/opensearch-project/anomaly-detection/pull/1513))
* Onboards to centralized resource access control for detectors and forecasters ([#1533](https://github.com/opensearch-project/anomaly-detection/pull/1533))


### OpenSearch Common Utils


* Add tenancy access info to serialized user in threadcontext ([#857](https://github.com/opensearch-project/common-utils/pull/857))


### OpenSearch Dashboards Assistant


* Update dashboards-assistant so natural language visualization can be display in the new dashboard ingress ([#589](https://github.com/opensearch-project/dashboards-assistant/pull/589))


### OpenSearch Flow Framework Dashboards


* Cleanly handle error states for backend connection issues ([#757](https://github.com/opensearch-project/dashboards-flow-framework/pull/757))


### OpenSearch Observability Dashboards


* [Traces] Make service map max nodes and max edges values user-configurable ([#2472](https://github.com/opensearch-project/dashboards-observability/pull/2472))


### OpenSearch Query Insights Dashboards


* [IMPROVEMENT] MDS support for Inflight Queries ([#217](https://github.com/opensearch-project/query-insights-dashboards/pull/217))
* Change Live Queries page default auto refresh to 30 seconds ([#304](https://github.com/opensearch-project/query-insights-dashboards/pull/304))


### OpenSearch Search Relevance Dashboards


* Fetch models from ml-commons and add validation ([#568](https://github.com/opensearch-project/dashboards-search-relevance/pull/568))
* Show names instead of ids for experiment creation pages ([#567](https://github.com/opensearch-project/dashboards-search-relevance/pull/567))
* Retrieve experiment results using the experimentId field ([#574](https://github.com/opensearch-project/dashboards-search-relevance/pull/574))
* Add tooltips for metrics ([#573](https://github.com/opensearch-project/dashboards-search-relevance/pull/573))
* Remove ids from experiment table and link type instead ([#572](https://github.com/opensearch-project/dashboards-search-relevance/pull/572))
* Publish metrics stats without authorization to make it accessible to monitoring systems ([#593](https://github.com/opensearch-project/dashboards-search-relevance/pull/593))


### OpenSearch Security Dashboards


* Changes to show all index patterns in index permission panel in role view ([#1303](https://github.com/opensearch-project/security-dashboards-plugin/issues/1303), [#1891](https://github.com/opensearch-project/security-dashboards-plugin/issues/1891))
* Added missing index permissions in the list ([#1969](https://github.com/opensearch-project/security-dashboards-plugin/issues/1969))


### OpenSearch Job Scheduler


* Make Lock service not final ([#792](https://github.com/opensearch-project/job-scheduler/pull/792))
* Move info about delay to the the schedule portion in List Jobs API ([#801](https://github.com/opensearch-project/job-scheduler/pull/801))


### OpenSearch k-NN


* Add KNN timing info to core profiler [#2785](https://github.com/opensearch-project/k-NN/pull/2785)
* Patch for supporting nested search in IndexBinaryHNSWCagra [#2824](https://github.com/opensearch-project/k-NN/pull/2824)
* Support Asymmetric Distance Computation in Lucene-on-Faiss [#2781](https://github.com/opensearch-project/k-NN/pull/2781)
* Added dynamic index thread quantity defaults based on processor sizes [#2806](https://github.com/opensearch-project/k-NN/pull/2806)


### OpenSearch ML Commons


* Add Default System Prompt for the query Planner tool ([#4046](https://github.com/opensearch-project/ml-commons/pull/4046))
* Add support for date time injection for agents ([#4008](https://github.com/opensearch-project/ml-commons/pull/4008))
* Expose message history limit for PER Agent ([#4016](https://github.com/opensearch-project/ml-commons/pull/4016))
* [Enhancement] Enhance validation for create connector API ([#3579](https://github.com/opensearch-project/ml-commons/pull/3579))
* [Enhancements] Sparse encoding/tokenize support TOKEN\_ID format embedding ([#3963](https://github.com/opensearch-project/ml-commons/pull/3963))
* Add validation for creating uri in connectors ([#3972](https://github.com/opensearch-project/ml-commons/pull/3972))
* Enhance tool input parsing and add agentic rag tutorial ([#4023](https://github.com/opensearch-project/ml-commons/pull/4023))
* Run auto deploy remote model in partially deployed status ([#3423](https://github.com/opensearch-project/ml-commons/pull/3423))
* [ExceptionHandling] Throw proper 400 errors instead of 500 for agent execute and MCP ([#3988](https://github.com/opensearch-project/ml-commons/pull/3988))
* Tuning PER Agent Prompts ([#4059](https://github.com/opensearch-project/ml-commons/pull/4059))
* Add feature flag for agentic search ([#4021](https://github.com/opensearch-project/ml-commons/pull/4021))
* Adding feature flag for agentic memory ([#4067](https://github.com/opensearch-project/ml-commons/pull/4067))
* Add feature flag to delete mem container ([#4072](https://github.com/opensearch-project/ml-commons/pull/4072))


### OpenSearch Neural Search


* [Semantic Field] Support configuring the auto-generated knn\_vector field through the semantic field. ([#1420](https://github.com/opensearch-project/neural-search/pull/1420))
* [Semantic Field] Support configuring the ingest batch size for the semantic field. ([#1438](https://github.com/opensearch-project/neural-search/pull/1438))
* [Semantic Field] Allow configuring prune strategies for sparse encoding in semantic fields. ([#1434](https://github.com/opensearch-project/neural-search/pull/1434))
* Enable inner hits within collapse parameter for hybrid query ([#1447](https://github.com/opensearch-project/neural-search/pull/1447))
* [Semantic Field] Support configuring the chunking strategies through the semantic field. ([#1446](https://github.com/opensearch-project/neural-search/pull/1446))
* [Semantic Field] Support configuring reusing existing embedding for the semantic field. ([#1480](https://github.com/opensearch-project/neural-search/pull/1480/files))
* Add setting for number of documents stored by HybridCollapsingTopDocsCollector ([#1471](https://github.com/opensearch-project/neural-search/pull/1471))


### OpenSearch Query Insights


* Increase reader search limit to 500 and fix sort by metric type ([#381](https://github.com/opensearch-project/query-insights/pull/381))


### OpenSearch Search Relevance


* Added date filtering for UBI events in implicit judgment calculations. ([#165](https://github.com/opensearch-project/search-relevance/pull/165))
* Added fields to experiment results to facilitate Dashboard visualization ([#174](https://github.com/opensearch-project/search-relevance/pull/174))
* Added tasks scheduling and management mechanism for hybrid optimizer experiments ([#139](https://github.com/opensearch-project/search-relevance/pull/139))
* Enabled tasks scheduling for pointwise experiments ([#167](https://github.com/opensearch-project/search-relevance/pull/167))


### OpenSearch Security


* Create a mechanism for plugins to explicitly declare actions they need to perform with their assigned PluginSubject ([#5341](https://github.com/opensearch-project/security/pull/5341))
* Moves OpenSAML jars to a Shadow Jar configuration to facilitate its use in FIPS enabled environments ([#5400](https://github.com/opensearch-project/security/pull/5404))
* [Resource Sharing] Adds a Resource Access Evaluator for standalone Resource access authorization ([#5408](https://github.com/opensearch-project/security/pull/5408))
* Replaced the standard distribution of BouncyCastle with BC-FIPS ([#5439](https://github.com/opensearch-project/security/pull/5439))
* Introduced setting `plugins.security.privileges_evaluation.precomputed_privileges.enabled` ([#5465](https://github.com/opensearch-project/security/pull/5465))
* Optimized wildcard matching runtime performance ([#5470](https://github.com/opensearch-project/security/pull/5470))
* Optimized performance for construction of internal action privileges data structure ([#5470](https://github.com/opensearch-project/security/pull/5470))
* Restricting query optimization via star tree index for users with queries on indices with DLS/FLS/FieldMasked restrictions ([#5492](https://github.com/opensearch-project/security/pull/5492))
* Handle subject in nested claim for JWT auth backends ([#5467](https://github.com/opensearch-project/security/pull/5467))
* Integration with stream transport ([#5530](https://github.com/opensearch-project/security/pull/5530))


### OpenSearch Skills


* Merge index schema meta ([#596](https://github.com/opensearch-project/skills/pull/596))
* Mask error message in PPLTool ([#609](https://github.com/opensearch-project/skills/pull/609))


### OpenSearch User Behavior Insights


* [Enhancement] Adding a field to store the A/B TDI configs per event in the data generator. ([#102](https://github.com/opensearch-project/user-behavior-insights/pull/102))


### SQL


* Add compare\_ip operator udfs ([#3821](https://github.com/opensearch-project/sql/pull/3821))
* Add issue template specific for PPL commands and queries ([#3962](https://github.com/opensearch-project/sql/pull/3962))
* Add missing command in index.rst ([#3943](https://github.com/opensearch-project/sql/pull/3943))
* Append limit operator for QUEERY\_SIZE\_LIMIT ([#3940](https://github.com/opensearch-project/sql/pull/3940))
* CVE-2025-48924: upgrade commons-lang3 to 3.18.0 ([#3895](https://github.com/opensearch-project/sql/pull/3895))
* Change compare logical when comparing date related fields with string literal ([#3798](https://github.com/opensearch-project/sql/pull/3798))
* Disable a failed PPL query fallback to v2 by default ([#3952](https://github.com/opensearch-project/sql/pull/3952))
* Filter script pushdown with RelJson serialization in Calcite ([#3859](https://github.com/opensearch-project/sql/pull/3859))
* Push down QUERY\_SIZE\_LIMIT ([#3880](https://github.com/opensearch-project/sql/pull/3880))
* Skipping codegen and compile for Scan only plan ([#3853](https://github.com/opensearch-project/sql/pull/3853))
* Support Sort pushdown ([#3620](https://github.com/opensearch-project/sql/pull/3620))
* Support aggregation push down with scripts ([#3916](https://github.com/opensearch-project/sql/pull/3916))
* Support casting to IP with Calcite ([#3919](https://github.com/opensearch-project/sql/pull/3919))
* Support filter push down for Sarg value ([#3840](https://github.com/opensearch-project/sql/pull/3840))
* Support function argument coercion with Calcite ([#3914](https://github.com/opensearch-project/sql/pull/3914))
* Support partial filter push down ([#3850](https://github.com/opensearch-project/sql/pull/3850))
* Support pushdown physical sort operator to speedup SortMergeJoin ([#3864](https://github.com/opensearch-project/sql/pull/3864))
* Support relevance query functions pushdown implementation in Calcite ([#3834](https://github.com/opensearch-project/sql/pull/3834))
* Support span push down ([#3823](https://github.com/opensearch-project/sql/pull/3823))


## BUG FIXES


### OpenSearch Alerting


* Fix MGet bug, randomize fan out distribution ([#1885](https://github.com/opensearch-project/alerting/pull/1885))
* Refactored consistent responses and fixed unrelated exceptions ([#1818](https://github.com/opensearch-project/alerting/pull/1818))


### OpenSearch Anomaly Detection


* Fixing concurrency bug on writer ([#1508](https://github.com/opensearch-project/anomaly-detection/pull/1508))
* Fix(forecast): advance past current interval & anchor on now ([#1528](https://github.com/opensearch-project/anomaly-detection/pull/1528))
* Changing search calls on interval calculation ([#1535](https://github.com/opensearch-project/anomaly-detection/pull/1535))


### OpenSearch Anomaly Detection Dashboards


* Improve indicator helper, fix zero-value plotting etc ([#1058](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1058))
* Allow stopping forecaster from FORECAST\_FAILURE state and minor cleanups ([#1054](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1054))
* Restrict Suggest anomaly detector to only show for OpenSearch datasets ([#1001](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1001))
* Wrap data filter in detector creation ([#1060](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1060))
* fix ribon encoding issue in contextual launch ([#1064](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1064))
* fix: fetch full forecaster list, and fix delete bug ([#1068](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1068))


### OpenSearch Common Utils


* Pinned the commons-beanutils dependency to fix CVE-2025-48734 ([#850](https://github.com/opensearch-project/common-utils/pull/850))
* Revert "updating PublishFindingsRequest to use a list of findings rather than… ([#847](https://github.com/opensearch-project/common-utils/pull/847))


### OpenSearch Cross Cluster Replication


* Add missing method for RemoteClusterRepository class ([#1564](https://github.com/opensearch-project/cross-cluster-replication/pull/1564))


### OpenSearch Dashboards Assistant


* Fix failed unit tests due to missing Worker ([#593](https://github.com/opensearch-project/dashboards-assistant/pull/593))


### OpenSearch Observability Dashboards


* [Bug] Traces error display ([#2475](https://github.com/opensearch-project/dashboards-observability/pull/2475))
* [Bug]fixed metrics viz not showing up ([#2478](https://github.com/opensearch-project/dashboards-observability/pull/2478))


### OpenSearch Query Insights Dashboards


* Fix-query-details-verbose-param ([#217](https://github.com/opensearch-project/query-insights-dashboards/pull/217))
* React-vis implementation for Live Queries Dashboards ([#243](https://github.com/opensearch-project/query-insights-dashboards/pull/243))
* Revert "Update renderApp to use default export to prevent initialization race condition" ([#247](https://github.com/opensearch-project/query-insights-dashboards/pull/247))
* Fix for ui bugs ([#258](https://github.com/opensearch-project/query-insights-dashboards/pull/258))
* Fix top queries table sorting with correct id ([#285](https://github.com/opensearch-project/query-insights-dashboards/pull/285))
* Search bar fix ([#267](https://github.com/opensearch-project/query-insights-dashboards/pull/267))
* Removed search bar Cypress ([#306](https://github.com/opensearch-project/query-insights-dashboards/pull/306))


### OpenSearch Dashboards Reportsdashboards


* Fix for tenant issue when redirecting from discover ([#599](https://github.com/opensearch-project/dashboards-reporting/pull/599))


### OpenSearch Search Relevance Dashboards


* Improve messaging when backend plugin is disabled ([#578](https://github.com/opensearch-project/dashboards-search-relevance/pull/578))
* Do not show Pipeline error if there are no pipelines yet ([#582](https://github.com/opensearch-project/dashboards-search-relevance/pull/582))
* Avoid validation results overflow in the creation of Search Configuration ([#585](https://github.com/opensearch-project/dashboards-search-relevance/pull/585))
* Fix wrong unique number of results in Venn diagram ([#586](https://github.com/opensearch-project/dashboards-search-relevance/pull/586))
* Bug fixes for error messages not render correctly for toast notifications ([#612](https://github.com/opensearch-project/dashboards-search-relevance/pull/612))


### OpenSearch Dashboards Securityanalyticsdashboards


* Remove correlated findings bar chart that uses vega ([#1313](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1313))
* Update API call to get IOC types ([#1312](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1312))


### OpenSearch Flow Framework


* Fix ApiSpecFetcher Memory Issues and Exception Handling ([#1185](https://github.com/opensearch-project/flow-framework/pull/1185))
* Better handling of Workflow Steps with Bad Request status ([#1190](https://github.com/opensearch-project/flow-framework/pull/1190))
* Update RegisterLocalCustomModelStep ([#1194](https://github.com/opensearch-project/flow-framework/pull/1194))
* Avoid race condition setting encryption key ([#1200](https://github.com/opensearch-project/flow-framework/pull/1200))
* Fixing connector name in default use case ([#1205](https://github.com/opensearch-project/flow-framework/pull/1205))


### OpenSearch Geospatial


* Block redirect in IP2Geo and move validation to transport action ([#782](https://github.com/opensearch-project/geospatial/pull/782))


### OpenSearch Index Management


* Add history index pattern to list of System Index descriptors ([#1444](https://github.com/opensearch-project/index-management/pull/1444))
* Fix Integration test and lint errors ([#1442](https://github.com/opensearch-project/index-management/pull/1442))


### OpenSearch Job Scheduler


* Ensure that dates are serialized in TransportGetScheduledInfoAction.nodeOperation ([#793](https://github.com/opensearch-project/job-scheduler/pull/793))


### OpenSearch k-NN


* [Remote Vector Index Build] Don't fall back to CPU on terminal failures [#2773](https://github.com/opensearch-project/k-NN/pull/2773)
* Fix @ collision in NativeMemoryCacheKeyHelper for vector index filenames containing @ characters [#2810](https://github.com/opensearch-project/k-NN/pull/2810)


### OpenSearch ML Commons


* Fix class cast exception for execute API ([#4010](https://github.com/opensearch-project/ml-commons/pull/4010))
* Fix delete connector/model group exception handling ([#4044](https://github.com/opensearch-project/ml-commons/pull/4044))
* Fix exposed connector URL in error message ([#3953](https://github.com/opensearch-project/ml-commons/pull/3953))
* Fix is\_async status of agent execution task ([#3960](https://github.com/opensearch-project/ml-commons/pull/3960))
* Fix update model config invalid error ([#3994](https://github.com/opensearch-project/ml-commons/pull/3994))
* [FIX] allow partial updates to llm and memory fields in MLAgentUpdateInput ([#4040](https://github.com/opensearch-project/ml-commons/pull/4040))
* Fix the error status code and message for empty response ([#3968](https://github.com/opensearch-project/ml-commons/pull/3968))
* [MLSyncUpCron] Change info log to debug log to reduce logging ([#3948](https://github.com/opensearch-project/ml-commons/pull/3948))
* Fixing unit test for user\_requested\_tenant\_access ([#4037](https://github.com/opensearch-project/ml-commons/pull/4037))
* Ensure chat agent returns response when max iterations are reached ([#4031](https://github.com/opensearch-project/ml-commons/pull/4031))


### OpenSearch Neural Search


* Fix for collapse bug with knn query not deduplicating results ([#1413](https://github.com/opensearch-project/neural-search/pull/1413))
* Fix the HybridQueryDocIdStream to properly handle upTo value ([#1414](https://github.com/opensearch-project/neural-search/pull/1414))
* Handle remote dense model properly during mapping transform for the semantic field ([#1427](https://github.com/opensearch-project/neural-search/pull/1427))
* Handle a hybrid query extended with DLS rules by the security plugin ([#1432](https://github.com/opensearch-project/neural-search/pull/1432))
* Fix the minimal supported version for neural sparse query analyzer field ([#1475](https://github.com/opensearch-project/neural-search/pull/1475))


### OpenSearch Opensearch Reports


* Create the report definitions and instances indices in the system context to avoid permissions issues ([#1108](https://github.com/opensearch-project/reporting/pull/1108))


### OpenSearch Search Relevance


* Bug fix on rest APIs error status for creations ([#176](https://github.com/opensearch-project/search-relevance/pull/176))
* Fixed pipeline parameter being ignored in pairwise metrics processing for hybrid search queries ([#187](https://github.com/opensearch-project/search-relevance/pull/187))
* Added queryText and referenceAnswer text validation from manual input ([#177](https://github.com/opensearch-project/search-relevance/pull/177))


### OpenSearch Security


* Fix compilation issue after change to Subject interface in core and bump to 3.2.0 ([#5423](https://github.com/opensearch-project/security/pull/5423))
* Provide SecureHttpTransportParameters to complement SecureTransportParameters counterpart ([#5432](https://github.com/opensearch-project/security/pull/5432))
* Use isClusterPerm instead of requestedResolved.isLocalAll() to determine if action is a cluster action ([#5445](https://github.com/opensearch-project/security/pull/5445))
* Fix config update with deprecated config types failing in mixed clusters ([#5456](https://github.com/opensearch-project/security/pull/5456))
* Fix usage of jwt\_clock\_skew\_tolerance\_seconds in HTTPJwtAuthenticator ([#5506](https://github.com/opensearch-project/security/pull/5506))
* Always install demo certs if configured with demo certs ([#5517](https://github.com/opensearch-project/security/pull/5517))
* [Resource Sharing] Restores client accessor pattern to fix compilation issues when security plugin is not installed ([#5541](https://github.com/opensearch-project/security/pull/5541))


### OpenSearch Skills


* Update parameter handling of tools ([#618](https://github.com/opensearch-project/skills/pull/618))


### SQL


* Byte number should treated as Long in doc values ([#3928](https://github.com/opensearch-project/sql/pull/3928))
* Convert like function call to wildcard query for Calcite filter pushdown ([#3915](https://github.com/opensearch-project/sql/pull/3915))
* Correct null order for `sort` command with Calcite ([#3835](https://github.com/opensearch-project/sql/pull/3835))
* Default to UTC for date/time functions across PPL and SQL ([#3854](https://github.com/opensearch-project/sql/pull/3854))
* Fix create PIT permissions issue ([#3921](https://github.com/opensearch-project/sql/pull/3921))
* Fix the count() only aggregation pushdown issue ([#3891](https://github.com/opensearch-project/sql/pull/3891))
* Increase the precision of sum return type ([#3974](https://github.com/opensearch-project/sql/pull/3974))
* Support casting date literal to timestamp ([#3831](https://github.com/opensearch-project/sql/pull/3831))
* Support struct field with dynamic disabled ([#3829](https://github.com/opensearch-project/sql/pull/3829))
* Support full expression in WHERE clauses ([#3849](https://github.com/opensearch-project/sql/pull/3849))
* Translate JSONException to 400 instead of 500 ([#3833](https://github.com/opensearch-project/sql/pull/3833))
* Fix incorrect push down for Sarg with nullAs is TRUE ([#3882](https://github.com/opensearch-project/sql/pull/3882))
* Fix relevance query function over optimization issue in ReduceExpressionsRule ([#3851](https://github.com/opensearch-project/sql/pull/3851))


## INFRASTRUCTURE


### OpenSearch Alerting


* Update the maven snapshot publish endpoint and credential ([#1869](https://github.com/opensearch-project/alerting/pull/1869))


### OpenSearch Anomaly Detection


* Bumping gradle and nebula versions ([#1537](https://github.com/opensearch-project/anomaly-detection/pull/1537))


### OpenSearch Asynchronous Search


* Bump gradle to 8.14.3 and use jdk 24 in ci workflow ([#754](https://github.com/opensearch-project/asynchronous-search/pull/754))
* Update the maven snapshot publish endpoint and credential ([#748](https://github.com/opensearch-project/asynchronous-search/pull/748))


### OpenSearch Common Utils


* Switch gradle to 8.14 and JDK to 24 ([#848](https://github.com/opensearch-project/common-utils/pull/848))
* Update Maven snapshots publishing endpoint and credential retrieval ([#841](https://github.com/opensearch-project/common-utils/pull/841))


### OpenSearch Cross Cluster Replication


* Bump gradle to 8.14, fix backport-deletion and support JDK24 ([#1563](https://github.com/opensearch-project/cross-cluster-replication/pull/1563))


### OpenSearch Custom Codecs


* Report code coverage to codecov ([#267](https://github.com/opensearch-project/custom-codecs/pull/267))
* Bump gradle to 8.14, fix backport-deletion and support JDK24 ([#266](https://github.com/opensearch-project/custom-codecs/pull/266))


### OpenSearch Index Management


* Bump gradle to 8.14, kotlin to 2.2.0 and use jdk 24 in ci workflow ([#1445](https://github.com/opensearch-project/index-management/pull/1445))


### OpenSearch Job Scheduler


* Add new Github workflow to run sample plugin tests in cluster with multiple nodes ([#795](https://github.com/opensearch-project/job-scheduler/pull/795))
* Add test that disables watcher job and verifies that it stops running, but metadata exists ([#797](https://github.com/opensearch-project/job-scheduler/pull/797))
* Bump gradle to 8.14 and use jdk 24 in ci workflow ([#798](https://github.com/opensearch-project/job-scheduler/pull/798))


### OpenSearch k-NN


* Bump JDK version to 24, gradle to 8.14 [#2792](https://github.com/opensearch-project/k-NN/pull/2792)
* Bump Faiss commit to 2929bf4 [#2815](https://github.com/opensearch-project/k-NN/pull/2815)
* Bump Faiss commit to 5617caa [#2824](https://github.com/opensearch-project/k-NN/pull/2824)
* Bump Gradle to 8.14.3 [#2828](https://github.com/opensearch-project/k-NN/pull/2828)


### OpenSearch ML Commons


* Bump gradle to 8.14 and update JDK to 24 ([#3983](https://github.com/opensearch-project/ml-commons/pull/3983))
* Updating gradle version ([#4064](https://github.com/opensearch-project/ml-commons/pull/4064))
* [FIX] Update lombok version for jdk24 ([#4026](https://github.com/opensearch-project/ml-commons/pull/4026))


### OpenSearch Neural Search


* Support multi node integration testing ([#1320](https://github.com/opensearch-project/neural-search/pull/1320))


### OpenSearch Opensearch Learning To Rank Base


* Adding codecov config file ([#204](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/204))
* Update CI to upload code coverage report ([#201](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/201))


### OpenSearch Opensearch Reports


* Add a PR check to run integ tests with security ([#1110](https://github.com/opensearch-project/reporting/pull/1110))
* Add integtest.sh to specifically run integTestRemote task ([#1112](https://github.com/opensearch-project/reporting/pull/1112))
* Upgrade gradle to 8.14.3 and run CI checks with JDK24 ([#1109](https://github.com/opensearch-project/reporting/pull/1109))
* Update the maven snapshot publish endpoint and credential ([#1103](https://github.com/opensearch-project/reporting/pull/1103))


### OpenSearch Opensearch System Templates


* Update the maven snapshot publish endpoint and credential ([#83](https://github.com/opensearch-project/opensearch-system-templates/pull/83))
* Bump gradle to 8.14, fix backport-deletion and support JDK24 ([#89](https://github.com/opensearch-project/opensearch-system-templates/pull/89))


### OpenSearch Performance Analyzer


* Bump gradle to 8.14, fix backport-deletion and support JDK24 ([#831](https://github.com/opensearch-project/performance-analyzer/pull/831))


### OpenSearch Query Insights


* Update the maven endpoint and bump up gradle, java version ([#392](https://github.com/opensearch-project/query-insights/pull/392))
* Fix codecov ([#393](https://github.com/opensearch-project/query-insights/pull/393))
* Use codecov v3 ([#394](https://github.com/opensearch-project/query-insights/pull/394))


### OpenSearch Search Relevance


* Added end to end integration tests for experiments ([#154](https://github.com/opensearch-project/search-relevance/pull/154))
* Enabled tasks scheduling for llm judgments ([#166](https://github.com/opensearch-project/search-relevance/pull/166))
* Upgrade gradle to 8.14 and higher JDK version to 24 ([#188](https://github.com/opensearch-project/search-relevance/pull/188))


### OpenSearch Security Analytics


* Upgrade gradle to 8.14 and run CI with JDK 24 ([#1560](https://github.com/opensearch-project/security-analytics/pull/1560))
* Update the maven snapshot publish endpoint and credential ([#1544](https://github.com/opensearch-project/security-analytics/pull/1544))


### OpenSearch User Behavior Insights


* Added end to end integration tests for experiments ([#154](https://github.com/opensearch-project/search-relevance/pull/154))
* Upgrade gradle to 8.14 and higher JDK version to 24 ([#106](https://github.com/opensearch-project/user-behavior-insights/pull/106))


### SQL


* Add 'testing' and 'security fix' to enforce-label-action ([#3897](https://github.com/opensearch-project/sql/pull/3897))
* Update the maven snapshot publish endpoint and credential ([#3806](https://github.com/opensearch-project/sql/pull/3806))
* Update the maven snapshot publish endpoint and credential ([#3886](https://github.com/opensearch-project/sql/pull/3886))


## DOCUMENTATION


### OpenSearch ML Commons


* Add multi modal tutorial using ml inference processor ([#3576](https://github.com/opensearch-project/ml-commons/pull/3576))
* Add blueprint for semantic highlighter model on AWS Sagemaker ([#3879](https://github.com/opensearch-project/ml-commons/pull/3879))
* Add Documentation for creating Neural Sparse Remote Model ([#3857](https://github.com/opensearch-project/ml-commons/pull/3857))
* Add tutorials for language\_identification during ingest ([#3966](https://github.com/opensearch-project/ml-commons/pull/3966))
* Update link to the model in the aleph alpha blueprint ([#3980](https://github.com/opensearch-project/ml-commons/pull/3980))
* Add agentic rag tutorial ([#4045](https://github.com/opensearch-project/ml-commons/pull/4045))
* Notebook for step by step in multi-modal search in ml-inference processor ([#3944](https://github.com/opensearch-project/ml-commons/pull/3944))


### SQL


* Update ppl documentation index for new functions ([#3868](https://github.com/opensearch-project/sql/pull/3868))
* Update the limitation docs ([#3801](https://github.com/opensearch-project/sql/pull/3801))


## MAINTENANCE


### OpenSearch Alerting


* Bumped gradle to 8.14, support JDK 24; fixed backport branch deletion ([#1911](https://github.com/opensearch-project/alerting/pull/1911))
* Increment version to 3.2.0-SNAPSHOT ([#1872](https://github.com/opensearch-project/alerting/pull/1872))
* Revert "now publishes a list of findings instead of an individual one ([#1881](https://github.com/opensearch-project/alerting/pull/1881))
* Moved the commons-beanutils pinning to the core gradle file ([#1892](https://github.com/opensearch-project/alerting/pull/1892))
* Pinned the commons-beanutils dependency to 1.11.0 version ([#1887](https://github.com/opensearch-project/alerting/pull/1887))


### OpenSearch Asynchronous Search


* [AUTO] Increment version to 3.2.0-SNAPSHOT ([#751](https://github.com/opensearch-project/asynchronous-search/pull/751))


### OpenSearch Custom Codecs


* [AUTO] Increment version to 3.2.0-SNAPSHOT ([#262](https://github.com/opensearch-project/custom-codecs/pull/262))


### OpenSearch Alerting Dashboards Plugin


* Increment version to 3.2.0.0 ([#1271](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1271))


### OpenSearch Flow Framework Dashboards


* Change jsonpath dep to jsonpath-plus ([#756](https://github.com/opensearch-project/dashboards-flow-framework/pull/756))


### OpenSearch Dashboards Indexmanagementdashboards


* Increment version to 3.2.0.0 ([#1332](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1332))


### OpenSearch ML Commons Dashboards


* Increment version to 3.2.0.0 ([#437](https://github.com/opensearch-project/ml-commons-dashboards/pull/437))


### OpenSearch Notifications Dashboards


* [AUTO] Increment version to 3.2.0.0 ([#365](https://github.com/opensearch-project/dashboards-notifications/pull/365))


### OpenSearch Observability Dashboards


* Increment version to 3.2.0.0 + Snapshots update ([#2481](https://github.com/opensearch-project/dashboards-observability/pull/2481))


### OpenSearch Query Insights Dashboards


* CVE-2020-28469 Updated package.json and yarn.lock ([#270](https://github.com/opensearch-project/query-insights-dashboards/pull/270))
* 2.19.3 Release Notes ([#280](https://github.com/opensearch-project/query-insights-dashboards/pull/280))
* [AUTO] Increment version to 3.2.0.0 ([#295](https://github.com/opensearch-project/query-insights-dashboards/pull/295))
* [AUTO] Add release notes for 3.2.0 ([#302](https://github.com/opensearch-project/query-insights-dashboards/pull/302))
* CVE-2025-7783 and CVE-2025-6545 Updated package.json and yarn.lock ([#309](https://github.com/opensearch-project/query-insights-dashboards/pull/309))


### OpenSearch Dashboards Queryworkbenchdashboards


* Increment version to 3.2.0.0 ([#485](https://github.com/opensearch-project/dashboards-query-workbench/pull/485))


### OpenSearch Dashboards Reportsdashboards


* Increment version to 3.2.0.0 ([#603](https://github.com/opensearch-project/dashboards-reporting/pull/603))


### OpenSearch Search Relevance Dashboards


* Adding @fen-qin and @epugh as maintainers ([#569](https://github.com/opensearch-project/dashboards-search-relevance/pull/569))
* Update Maintainers for dashboards-search-relevance repository ([#576](https://github.com/opensearch-project/dashboards-search-relevance/pull/576))
* Add issue template and codecov to add test coverage reports ([#601](https://github.com/opensearch-project/dashboards-search-relevance/pull/601))


### OpenSearch Dashboards Securityanalyticsdashboards


* [AUTO] Increment version to 3.2.0.0 ([#1316](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1316))


### OpenSearch Security Dashboards


* Bump `actions/checkout` from 2 to 4 ([#2260](https://github.com/opensearch-project/security-dashboards-plugin/pull/2260))
* Bump `codecov/codecov-action` from 4 to 5 ([#2263](https://github.com/opensearch-project/security-dashboards-plugin/pull/2263))
* Bump `SvanBoxel/delete-merged-branch` from b77e873cee00b09f55cc553bd24aae5f8dfc9157 to 2b5b058e3db41a3328fd9a6a58fd4c2545a14353 ([#2265](https://github.com/opensearch-project/security-dashboards-plugin/pull/2265))
* Bump `actions/github-script` from 6 to 7 ([#2259](https://github.com/opensearch-project/security-dashboards-plugin/pull/2259))
* Bump `tibdex/github-app-token` from 1.5.0 to 2.1.0 ([#2262](https://github.com/opensearch-project/security-dashboards-plugin/pull/2262))
* Bump `stefanzweifel/git-auto-commit-action` from 5 to 6 ([#2268](https://github.com/opensearch-project/security-dashboards-plugin/pull/2268))
* Bump `derek-ho/start-opensearch` from 6 to 7 ([#2267](https://github.com/opensearch-project/security-dashboards-plugin/pull/2267))


### OpenSearch Geospatial


* Upgrade gradle to 8.14.3 and run CI checks with JDK24 ([#776](https://github.com/opensearch-project/geospatial/pull/776))


### OpenSearch Index Management


* [AUTO] Increment version to 3.2.0-SNAPSHOT ([#1435](https://github.com/opensearch-project/index-management/pull/1435))


### OpenSearch ML Commons


* Increase mcp code coverage and address comments in PR: #3883 ([#3908](https://github.com/opensearch-project/ml-commons/pull/3908))
* Fix: change log level for sync up job ([#3948](https://github.com/opensearch-project/ml-commons/pull/3948))
* Keep .plugins-ml-config index for Integration test ([#3989](https://github.com/opensearch-project/ml-commons/pull/3989))
* Adding unit tests for create and get memory container functionalities ([#4056](https://github.com/opensearch-project/ml-commons/pull/4056))
* Adding more unit tests and upgrading jacoco ([#4057](https://github.com/opensearch-project/ml-commons/pull/4057))
* CVE fix: beanutils ([#4062](https://github.com/opensearch-project/ml-commons/pull/4062))


### OpenSearch Notifications


* Updated gradle, jdk and other dependencies ([#1057](https://github.com/opensearch-project/notifications/pull/1057))


### OpenSearch Learning To Rank Base


* Bump gradle to 8.14, codecov to v5 and support JDK24 ([#202](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/202))
* Updating ULP for similarity score comparisons to 30000 to avoid flaky tests ([#205](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/205))
* [AUTO] Increment version to 3.2.0-SNAPSHOT ([#191](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/191))


### OpenSearch Observability


* [AUTO] Increment version to 3.2.0-SNAPSHOT ([#1933](https://github.com/opensearch-project/opensearch-observability/pull/1933))
* Update the maven snapshot publish endpoint and credential ([#1931](https://github.com/opensearch-project/opensearch-observability/pull/1931))
* Upgrade gradle to 8.14.3 and run CI checks with JDK24 ([#1937](https://github.com/opensearch-project/opensearch-observability/pull/1937))


### OpenSearch Reports


* [AUTO] Increment version to 3.2.0-SNAPSHOT ([#1105](https://github.com/opensearch-project/reporting/pull/1105))


### OpenSearch System Templates


* [AUTO] Increment version to 3.2.0-SNAPSHOT ([#86](https://github.com/opensearch-project/opensearch-system-templates/pull/86))


### OpenSearch Performance Analyzer


* Bump spotbug to 6.2.2 and checkstyle 10.26.1 ([#826](https://github.com/opensearch-project/performance-analyzer/pull/826))
* Increment version to 3.2.0-SNAPSHOT ([#823](https://github.com/opensearch-project/performance-analyzer/pull/823))


### OpenSearch Query Insights


* [AUTO] Increment version to 3.2.0-SNAPSHOT ([#380](https://github.com/opensearch-project/query-insights/pull/380))
* [AUTO] Add release notes for 3.2.0 ([#395](https://github.com/opensearch-project/query-insights/pull/395))


### OpenSearch Search Relevance


* Adding template for feature technical design ([#201](https://github.com/opensearch-project/search-relevance/issues/201))


### OpenSearch Security Analytics


* [AUTO] Increment version to 3.2.0-SNAPSHOT ([#1552](https://github.com/opensearch-project/security-analytics/pull/1552))


### OpenSearch Skills


* Update the maven snapshot publish endpoint and credential ([#601](https://github.com/opensearch-project/skills/pull/601))
* Bump gradle, java, lombok and fix ad configrequest change ([#615](https://github.com/opensearch-project/skills/pull/615))
* Bump version to 3.2.0.0 ([#605](https://github.com/opensearch-project/skills/pull/605))


### SQL


* Add enforce-labels action ([#3816](https://github.com/opensearch-project/sql/pull/3816))
* Bump gradle to 8.14 and java to 24 ([#3875](https://github.com/opensearch-project/sql/pull/3875))
* Update commons-lang exclude rule to exclude it everywhere ([#3932](https://github.com/opensearch-project/sql/pull/3932))
* Add release notes for 2.19.3 ([#3910](https://github.com/opensearch-project/sql/pull/3910))


## REFACTORING


### OpenSearch Search Relevance Dashboards


* Code Refactor + Unit tests for query\_set\_create ([#580](https://github.com/opensearch-project/dashboards-search-relevance/pull/580))
* Code Refactor + Unit tests for search\_configuration\_create ([#587](https://github.com/opensearch-project/dashboards-search-relevance/pull/587))
* Code Refactor + Unit tests for judgment\_create ([#588](https://github.com/opensearch-project/dashboards-search-relevance/pull/588))
* Code Refactor + Unit Tests for query\_set\_listing and query\_set\_view ([#595](https://github.com/opensearch-project/dashboards-search-relevance/pull/595))
* Code Refactor + Unit Tests for search\_configuration and judgment ([#602](https://github.com/opensearch-project/dashboards-search-relevance/pull/602))
* Code Refactor + Unit Tests for experiment ([#613](https://github.com/opensearch-project/dashboards-search-relevance/pull/613))


### OpenSearch Geospatial


* Replace usages of ThreadContext.stashContext with pluginSubject.runAs ([#715](https://github.com/opensearch-project/geospatial/pull/715))


### OpenSearch Job Scheduler


* Use Text Blocks when defining multi-line strings ([#790](https://github.com/opensearch-project/job-scheduler/pull/790))


### OpenSearch Security


* Refactor JWT Vendor to take a claims builder and rename oboEnabled to be enabled ([#5436](https://github.com/opensearch-project/security/pull/5436))
* Remove ASN1 reflection methods ([#5454](https://github.com/opensearch-project/security/pull/5454))
* Remove provider reflection code ([#5457](https://github.com/opensearch-project/security/pull/5457))
* Add tenancy access info to serialized user in threadcontext ([#5519](https://github.com/opensearch-project/security/pull/5519))


### OpenSearch Security Analytics


* Use instance of LockService instantiated in JobScheduler through Guice ([#1555](https://github.com/opensearch-project/security-analytics/pull/1555))