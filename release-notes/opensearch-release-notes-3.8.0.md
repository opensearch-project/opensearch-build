# OpenSearch and OpenSearch Dashboards 3.8.0 Release Notes


## FEATURES


### OpenSearch Alerting


* Add filter by backend roles access strategy setting to control how backend role filtering determines access to alerting objects ([#2034](https://github.com/opensearch-project/alerting/pull/2034))


### OpenSearch Alerting Dashboards Plugin


* Add dynamic capability-based coordination for Explore "Create monitor" menu entry ([#1461](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1461))
* Extract shared PPL monitor components and helpers, and fix miscellaneous PPL monitor bugs ([#1470](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1470))


### OpenSearch Anomaly Detection


* Add PPL as a source type for single-stream detectors, enabling runtime feature queries through PPL transport actions ([#1718](https://github.com/opensearch-project/anomaly-detection/pull/1718))


### OpenSearch Common Utils


* Implement DocRequest on notification config and alerting request classes to enable automatic resource-level access control ([#980](https://github.com/opensearch-project/common-utils/pull/980))


### OpenSearch Cross Cluster Replication


* Add bulk feature support for all replication APIs, enabling start, stop, pause, and resume operations on multiple indexes matching a pattern with a single API call ([#1699](https://github.com/opensearch-project/cross-cluster-replication/pull/1699))
* Add optional `follower_index_pattern` support to autofollow API, allowing follower index renaming using a `{{leader_index}}` placeholder to avoid name collisions ([#1705](https://github.com/opensearch-project/cross-cluster-replication/pull/1705))


### OpenSearch Dashboards Investigation


* Add Notebooks navPopover to the icon side navigation with "Create notebook" and "View all notebooks" actions ([#390](https://github.com/opensearch-project/dashboards-investigation/pull/390))
* Disable create\_investigation tool on the Search Relevance page to reduce irrelevant tool suggestions ([#388](https://github.com/opensearch-project/dashboards-investigation/pull/388))


### OpenSearch Dashboards Observability


* Add Prometheus metrics rule creation, editing, cloning, and deletion via the Cortex ruler API ([#2718](https://github.com/opensearch-project/dashboards-observability/pull/2718))


### OpenSearch Dashboards Search Relevance


* Add `/search-relevance` slash command with welcome message for AI-assisted search relevance tuning ([#843](https://github.com/opensearch-project/dashboards-search-relevance/pull/843))
* Add `chatCommandEnabled` feature flag to gate the `/search-relevance` slash command behind dynamic config ([#890](https://github.com/opensearch-project/dashboards-search-relevance/pull/890))
* Add experiment name and description support for create, display, and edit workflows ([#823](https://github.com/opensearch-project/dashboards-search-relevance/pull/823))
* Add description support for Search Configurations in create, detail, and listing views ([#854](https://github.com/opensearch-project/dashboards-search-relevance/pull/854))
* Show failed documents with status indicators in the Judgment ratings view ([#899](https://github.com/opensearch-project/dashboards-search-relevance/pull/899))


### OpenSearch Index Management


* Support mixed AND/OR rollover conditions via `any_of` grouped syntax ([#1667](https://github.com/opensearch-project/index-management/pull/1667))


### OpenSearch ML Commons


* Support MCP for Flow and Conversational Flow agents ([#4776](https://github.com/opensearch-project/ml-commons/pull/4776))
* Add REST API to list all tools available in an MCP server ([#4705](https://github.com/opensearch-project/ml-commons/pull/4705))
* Introduce gRPC streaming support for ML prediction and agent execution ([#4790](https://github.com/opensearch-project/ml-commons/pull/4790))
* Add memory retention policy data model, pinned field, and API wiring (1/2) ([#4914](https://github.com/opensearch-project/ml-commons/pull/4914))
* Add memory retention job, cluster defaults, and hardening (2/2) ([#4918](https://github.com/opensearch-project/ml-commons/pull/4918))


### OpenSearch Notifications


* Add filter by backend roles access strategy setting to control how backend role matching determines access to notification objects ([#1146](https://github.com/opensearch-project/notifications/pull/1146))


### OpenSearch Query Insights Dashboards


* Add dynamic column visibility system allowing users to show/hide columns in Top N Queries and Live Queries tables via a popover UI with localStorage persistence ([#569](https://github.com/opensearch-project/query-insights-dashboards/pull/569))


### OpenSearch Search Relevance


* Implement Mustache template support for search queries, enabling native OpenSearch ScriptService-based templating alongside legacy `%SearchText%` placeholders ([#342](https://github.com/opensearch-project/search-relevance/pull/342))
* Implement referential integrity validation for Search Relevance entities, ensuring referenced resources exist before creation or update operations proceed ([#360](https://github.com/opensearch-project/search-relevance/pull/360))
* Add experiment execution time input signatures (SHA-256 fingerprints of query set, judgments, and search configurations) and `GET /_plugins/_search_relevance/experiments/{id}/validate` for VALID / DRIFTED / UNAVAILABLE drift checks ([#456](https://github.com/opensearch-project/search-relevance/pull/456))
* Make LLM judgment generation provider-neutral, supporting any LLM provider through ml-commons connectors while maintaining backward compatibility with OpenAI-compatible connectors ([#515](https://github.com/opensearch-project/search-relevance/pull/515))
* Report LLM judgment success/failure counts and failed queries in judgment metadata, making unrated documents visible instead of silently dropping them ([#521](https://github.com/opensearch-project/search-relevance/pull/521))


### OpenSearch Security


* Implement standalone audit logging for SSL-only mode without requiring full security auth/RBAC ([#6304](https://github.com/opensearch-project/security/pull/6304))
* Add unified `disabled_categories` setting for audit logging ([#6271](https://github.com/opensearch-project/security/pull/6271))
* Allow read access on system indices marked with UnrestrictedSystemIndexDescriptor ([#6197](https://github.com/opensearch-project/security/pull/6197))
* Enforce 256 character limit on all text inputs for PUT/PATCH requests ([#6224](https://github.com/opensearch-project/security/pull/6224))
* Support query-based terms lookup queries in document-level security ([#6244](https://github.com/opensearch-project/security/pull/6244))
* Add support for `./gradlew run` task to allow running the plugin locally ([#6307](https://github.com/opensearch-project/security/pull/6307))


### OpenSearch k-NN


* Add search request processor to automatically exclude vector fields from `_source` in KNN queries ([#3152](https://github.com/opensearch-project/k-NN/pull/3152))


### SQL


* Add PPL `xyseries` command for pivoting row-oriented grouped results into wide tables ([#5343](https://github.com/opensearch-project/sql/pull/5343))
* Add PPL `timewrap` command for time-period comparison over timechart output ([#5241](https://github.com/opensearch-project/sql/pull/5241))
* Add PPL `foreach` command for iterating over field lists, multivalue fields, and JSON arrays ([#5613](https://github.com/opensearch-project/sql/pull/5613))
* Add PPL `makeresults` command for generating in-memory rows without an index scan ([#5622](https://github.com/opensearch-project/sql/pull/5622))


## ENHANCEMENTS


### OpenSearch Anomaly Detection Dashboards Plugin


* Filter AnalyticEngine data sources from AD and Forecasting pickers ([#1209](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1209))


### OpenSearch Custom Codecs


* Onboard new backport-pr reusable GitHub workflow for custom-codecs ([#349](https://github.com/opensearch-project/custom-codecs/pull/349))
* Update maven2 mirror repository URL order ([#352](https://github.com/opensearch-project/custom-codecs/pull/352))
* Upgrade qat-java to 2.5.0 and batch decompression into a single JNI call to reduce overhead on stored-fields reads ([#357](https://github.com/opensearch-project/custom-codecs/pull/357))


### OpenSearch Dashboards Flow Framework


* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#898](https://github.com/opensearch-project/dashboards-flow-framework/pull/898))
* Onboard new backport-pr reusable GitHub workflow, replacing obsolete backport workflows ([#896](https://github.com/opensearch-project/dashboards-flow-framework/pull/896))


### OpenSearch Dashboards Observability


* Add anomaly detection resources (detectors, forecasters) to Alert Manager ([#2721](https://github.com/opensearch-project/dashboards-observability/pull/2721))
* Add alert banner for legacy experience navigation ([#2772](https://github.com/opensearch-project/dashboards-observability/pull/2772))
* Persist APM time range selection across pages and reloads using session storage ([#2784](https://github.com/opensearch-project/dashboards-observability/pull/2784))
* Refine SLO suggest page with service-first selection, grouped preview, and UX improvements ([#2783](https://github.com/opensearch-project/dashboards-observability/pull/2783))


### OpenSearch Dashboards Query Workbench


* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#554](https://github.com/opensearch-project/dashboards-query-workbench/pull/554))
* Onboard new backport-pr reusable GitHub workflow, replacing obsolete backport-related workflows ([#568](https://github.com/opensearch-project/dashboards-query-workbench/pull/568))


### OpenSearch Dashboards Search Relevance


* Load experiment detail resources in parallel to reduce page latency ([#883](https://github.com/opensearch-project/dashboards-search-relevance/pull/883))
* Surface backend error message and HTTP status code instead of generic unknown error in list and detail views ([#874](https://github.com/opensearch-project/dashboards-search-relevance/pull/874))
* Surface backend error messages in detail views ([#895](https://github.com/opensearch-project/dashboards-search-relevance/pull/895))
* Render error state on Experiment Details page when experiment fails to load ([#901](https://github.com/opensearch-project/dashboards-search-relevance/pull/901))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#887](https://github.com/opensearch-project/dashboards-search-relevance/pull/887))
* Onboard new backport-pr reusable GitHub workflow ([#884](https://github.com/opensearch-project/dashboards-search-relevance/pull/884))
* Make Query Set description optional ([#852](https://github.com/opensearch-project/dashboards-search-relevance/pull/852))


### OpenSearch Geospatial


* Replace old backport workflow with new reusable backport-pr GitHub workflow ([#872](https://github.com/opensearch-project/geospatial/pull/872))


### OpenSearch Job Scheduler


* Onboard new backport-pr reusable GitHub workflow for job-scheduler ([#942](https://github.com/opensearch-project/job-scheduler/pull/942))


### OpenSearch ML Commons


* Support tool description override in MCP connector ([#4766](https://github.com/opensearch-project/ml-commons/pull/4766))
* Refine planner agent prompt ([#4822](https://github.com/opensearch-project/ml-commons/pull/4822))
* Add JSON logs to agent flow ([#4740](https://github.com/opensearch-project/ml-commons/pull/4740))
* Serve `/_plugins/_ml/mcp` on demand instead of a per-node cache ([#4907](https://github.com/opensearch-project/ml-commons/pull/4907))


### OpenSearch Neural Search


* Allow custom field name for storing previous rerank score to avoid overwriting existing document fields ([#1880](https://github.com/opensearch-project/neural-search/pull/1880))
* Improve hybrid query filter validation error message to provide guidance on combining multiple filters ([#1870](https://github.com/opensearch-project/neural-search/pull/1870))
* Skip two-phase rescore optimization for queries containing sort fields ([#1898](https://github.com/opensearch-project/neural-search/pull/1898))


### OpenSearch Query Insights


* Derive reader index names from date range instead of cluster state, avoiding cluster state calls ([#614](https://github.com/opensearch-project/query-insights/pull/614))
* Capture user identity (username, roles, backend roles) in query insights records Live Queries ([#645](https://github.com/opensearch-project/query-insights/pull/645))


### OpenSearch Query Insights Dashboards


* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#548](https://github.com/opensearch-project/query-insights-dashboards/pull/548))
* Onboard new backport-pr reusable GitHub workflow ([#545](https://github.com/opensearch-project/query-insights-dashboards/pull/545))


### OpenSearch Search Relevance


* Onboard new backport-pr reusable GitHub workflow to replace obsolete backport-related workflows ([#513](https://github.com/opensearch-project/search-relevance/pull/513))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#520](https://github.com/opensearch-project/search-relevance/pull/520))
* Optimize RBO calculation by maintaining prefix sets incrementally, reducing complexity from O(n²) to O(n) ([#500](https://github.com/opensearch-project/search-relevance/pull/500))
* Optimize Frequency Weighted similarity by replacing O(n²) list scan with HashSet-based single-pass computation ([#502](https://github.com/opensearch-project/search-relevance/pull/502))


### OpenSearch Security


* Scale legacy alias resolution with bounded indices-lookup access for improved performance on large clusters ([#6312](https://github.com/opensearch-project/security/pull/6312))
* Improve error message when unresolved user attributes are used in DLS to explicitly show "[none]" ([#6305](https://github.com/opensearch-project/security/pull/6305))
* Fix dynamic sign-in options by removing stale default and improving validation logic ([#6180](https://github.com/opensearch-project/security/pull/6180))
* Add `@Nullable` annotation to `assignResourceSharingClient` parameter to prevent NPE in Kotlin consumers ([#6301](https://github.com/opensearch-project/security/pull/6301))
* Address PR review feedback for standalone audit logging: add Sensitive property to settings, refactor index searcher wrapper, and use framework-level index resolution ([#6321](https://github.com/opensearch-project/security/pull/6321))


### OpenSearch Security Analytics


* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#1742](https://github.com/opensearch-project/security-analytics/pull/1742))
* Update maven2 mirror repository URL order ([#1744](https://github.com/opensearch-project/security-analytics/pull/1744))


### OpenSearch Security Dashboards Plugin


* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#2463](https://github.com/opensearch-project/security-dashboards-plugin/pull/2463))
* Onboard new backport-pr reusable GitHub workflow ([#2456](https://github.com/opensearch-project/security-dashboards-plugin/pull/2456))
* Enforce 256-character limit on all text input fields ([#2444](https://github.com/opensearch-project/security-dashboards-plugin/pull/2444))


### OpenSearch User Behavior Insights


* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#193](https://github.com/opensearch-project/user-behavior-insights/pull/193))
* Onboard new backport-pr reusable GitHub workflow ([#192](https://github.com/opensearch-project/user-behavior-insights/pull/192))


### OpenSearch k-NN


* Fall back to exact search when Lucene's search budget is exhausted during Memory Optimized Search ([#3354](https://github.com/opensearch-project/k-NN/pull/3354))
* Introduce BulkVectorScorer to consolidate exact-search scoring into a single reusable abstraction ([#3361](https://github.com/opensearch-project/k-NN/pull/3361))


### SQL


* Anonymize `xyseries` command and mark it as experimental in documentation ([#5643](https://github.com/opensearch-project/sql/pull/5643))
* Suggest similar field names in 'field not found' error messages ([#5402](https://github.com/opensearch-project/sql/pull/5402))
* Support `constant_keyword` field type in PPL, treating it as a string ([#5639](https://github.com/opensearch-project/sql/pull/5639))
* Decouple Calcite PPL planning from ExprType, operating on RelDataType directly ([#5633](https://github.com/opensearch-project/sql/pull/5633))
* Support bare-field join criteria shorthand (`join on <field>`) in PPL ([#5517](https://github.com/opensearch-project/sql/pull/5517))
* Classify unsupported-feature errors as client errors (4xx) on the SQL path ([#5569](https://github.com/opensearch-project/sql/pull/5569))
* Reject unsupported output formats on the analytics-engine route with a 4xx error ([#5570](https://github.com/opensearch-project/sql/pull/5570))
* Widen narrow integer operands in PPL arithmetic to prevent silent overflow ([#5603](https://github.com/opensearch-project/sql/pull/5603))
* Add configurable expression depth limit during AST building to prevent stack overflow ([#5602](https://github.com/opensearch-project/sql/pull/5602))
* Add `json_tree` machine-readable explain format accessible via `_explain?format=json_tree` ([#5576](https://github.com/opensearch-project/sql/pull/5576))
* Onboard new backport-pr reusable GitHub workflow ([#5586](https://github.com/opensearch-project/sql/pull/5586))
* Return all columns including struct and nested fields when using `head` command ([#5518](https://github.com/opensearch-project/sql/pull/5518))
* Bring `CalcitePPLBasicIT` to parity on the analytics-engine route ([#5542](https://github.com/opensearch-project/sql/pull/5542))
* Bring `CalciteWhereCommandIT` to parity on the analytics-engine route ([#5546](https://github.com/opensearch-project/sql/pull/5546))
* Stabilize order-dependent PPL ITs with explicit sort for multi-shard analytics runs ([#5537](https://github.com/opensearch-project/sql/pull/5537))
* Align `DateTimeComparisonIT` today's date computation to UTC for analytics-engine compatibility ([#5543](https://github.com/opensearch-project/sql/pull/5543))
* Fix NPE on `case()` with incompatible branch types, returning a clean 400 error ([#5575](https://github.com/opensearch-project/sql/pull/5575))
* Fix NPE when `rex` sits inside `appendcol` subsearch for the analytics engine ([#5574](https://github.com/opensearch-project/sql/pull/5574))


## BUG FIXES


### OpenSearch Alerting


* Avoid ScriptService fallback when multi-tenant trigger evaluation is enabled and remote trigger evaluation cannot run due to search input failure ([#2179](https://github.com/opensearch-project/alerting/pull/2179))


### OpenSearch Cross Cluster Replication


* Fix stale and negative counters in the follower\_stats API by deriving sync state from cluster metadata cross-referenced with live shard tasks ([#1717](https://github.com/opensearch-project/cross-cluster-replication/pull/1717))


### OpenSearch Dashboards Assistant


* Add @hapi/hoek module name mapper to Jest config for hapi 21 compatibility and fix CI with correct commit SHA ([#700](https://github.com/opensearch-project/dashboards-assistant/pull/700))


### OpenSearch Dashboards Maps


* Use CSP-safe MapLibre build and expose worker as a static asset to fix maps in strict Content Security Policy environments ([#842](https://github.com/opensearch-project/dashboards-maps/pull/842))
* Hide AnalyticEngine data source index patterns from layer config dropdowns ([#825](https://github.com/opensearch-project/dashboards-maps/pull/825))


### OpenSearch Dashboards Observability


* Fix SLO bugs including breadcrumb removal, template navigation, beta icon removal, and Alertmanager config error handling ([#2755](https://github.com/opensearch-project/dashboards-observability/pull/2755))
* Include Prometheus connection metadata in all PromQL chart queries to fix empty datasource errors ([#2726](https://github.com/opensearch-project/dashboards-observability/pull/2726))
* Allow colons in rule-detail ruleId path parameter for Prometheus SLO rules ([#2746](https://github.com/opensearch-project/dashboards-observability/pull/2746))
* Fix SLO status incorrectly degrading to no-data when optional alerts fetch fails ([#2747](https://github.com/opensearch-project/dashboards-observability/pull/2747))
* Pass real datasource context and wire persistence in CreateMetricsMonitor flyout ([#2773](https://github.com/opensearch-project/dashboards-observability/pull/2773))
* Use validate callback for length checks in alerting schemas to fix joi v17 compatibility ([#2730](https://github.com/opensearch-project/dashboards-observability/pull/2730))
* Clear stale histogram and patterns when switching to a stats query ([#2728](https://github.com/opensearch-project/dashboards-observability/pull/2728))
* Improve SLO creation flow with service-first guidance and fix Alert Manager severity/datasource issues ([#2758](https://github.com/opensearch-project/dashboards-observability/pull/2758))


### OpenSearch Dashboards Reporting


* Fix XLSX report download blocked by CSP connect-src directive by replacing fetch() with direct base64 decoding ([#762](https://github.com/opensearch-project/dashboards-reporting/pull/762))
* Replace showdown with marked to resolve ReDoS vulnerability CVE-2024-1899 ([#777](https://github.com/opensearch-project/dashboards-reporting/pull/777))
* Upgrade json-2-csv to ^5.5.11 to resolve CSV injection vulnerability CVE-2026-9673 ([#780](https://github.com/opensearch-project/dashboards-reporting/pull/780))


### OpenSearch Dashboards Search Relevance


* Fix failed queries being incorrectly treated as zero search results in the Search Evaluation view ([#849](https://github.com/opensearch-project/dashboards-search-relevance/pull/849))
* Fix metrics retention trimming to evict expired entries from all interval-keyed maps ([#880](https://github.com/opensearch-project/dashboards-search-relevance/pull/880))
* Fix infinite re-render loop in `useDataSourceUrlSync` when local cluster is selected ([#859](https://github.com/opensearch-project/dashboards-search-relevance/pull/859))
* Accept numeric `tokenLimit` in judgment route validation ([#891](https://github.com/opensearch-project/dashboards-search-relevance/pull/891))
* Display stored reference answers on Query Set Details page ([#856](https://github.com/opensearch-project/dashboards-search-relevance/pull/856))
* Poll judgment detail view while status is PROCESSING so ratings appear when async generation completes ([#858](https://github.com/opensearch-project/dashboards-search-relevance/pull/858))
* Hide AnalyticEngine data sources from DSL-dependent data source dropdowns ([#846](https://github.com/opensearch-project/dashboards-search-relevance/pull/846))


### OpenSearch Index Management


* Fix NoClassDefFoundError in ISM custom webhook error notifications by adding HttpClient 5 dependencies ([#1643](https://github.com/opensearch-project/index-management/pull/1643))
* Fix flaky NotificationActionListenerIT zero-notification assertions by waiting past the 5-second webhook delay ([#1688](https://github.com/opensearch-project/index-management/pull/1688))
* Fix flaky SMRunnerIT deletion pattern test by asserting only on pattern-matched snapshots ([#1692](https://github.com/opensearch-project/index-management/pull/1692))
* Fix Rollup/Transform security ITs failing after own\_index removal by granting cluster-level bulk permission ([#1666](https://github.com/opensearch-project/index-management/pull/1666))


### OpenSearch Index Management Dashboards Plugin


* Handle deletion-only snapshot management policies in the UI without crashing ([#1444](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1444))


### OpenSearch Job Scheduler


* Fix typo in log message: "occured" corrected to "occurred" ([#916](https://github.com/opensearch-project/job-scheduler/pull/916))


### OpenSearch ML Commons


* Fix MCP agent execution hang after MCP SDK 1.1.1 bump ([#4816](https://github.com/opensearch-project/ml-commons/pull/4816))
* Return HTTP 429 instead of 500 on connection pool acquire timeout ([#4852](https://github.com/opensearch-project/ml-commons/pull/4852))
* Fix `system_prompt` not reaching Bedrock Converse ([#4871](https://github.com/opensearch-project/ml-commons/pull/4871))
* Fix SearchIndexTool frequently failing ([#4530](https://github.com/opensearch-project/ml-commons/pull/4530))
* Retry transient HTTP errors from any remote service ([#4882](https://github.com/opensearch-project/ml-commons/pull/4882))
* Fix ModelGuardrail and LocalRegexGuardrail fail-open bugs (now fail-closed) ([#4904](https://github.com/opensearch-project/ml-commons/pull/4904))
* Fix gRPC stream double-termination ([#4927](https://github.com/opensearch-project/ml-commons/pull/4927))
* Validate model archives to block arbitrary code execution ([#4929](https://github.com/opensearch-project/ml-commons/pull/4929))
* Return correct HTTP status on memory-container failures instead of 500 ([#4930](https://github.com/opensearch-project/ml-commons/pull/4930))


### OpenSearch ML Commons Dashboards


* Fix test failure due to unresolved hapi import ([#492](https://github.com/opensearch-project/ml-commons-dashboards/pull/492))


### OpenSearch Neural Search


* Block hybrid query execution with `dfs_query_then_fetch` search type to prevent incorrect results ([#1873](https://github.com/opensearch-project/neural-search/pull/1873))
* Fix hybrid query explanation producing a single normalization block instead of per-sub-query blocks for indices with nested fields ([#1876](https://github.com/opensearch-project/neural-search/pull/1876))


### OpenSearch OpenSearch Learning To Rank Base


* Honor XGBoost per-node missing/default\_left direction at scoring time to fix ranking divergence from offline predictions ([#379](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/379))
* Disable Mustache partial template resolution to prevent file-based partial includes in search templates ([#386](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/386))
* Fix dependency resolution during snapshot builds by scoping snapshot repository to OpenSearch packages only ([#369](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/369))


### OpenSearch OpenSearch Remote Metadata Sdk


* Force netty and httpclient5 versions to address CVE-2026-33870, CVE-2026-33871, and CVE-2026-40542 ([#424](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/424))


### OpenSearch Query Insights


* Fix testNestedQueryType expectation for recursive nested query traversal ([#628](https://github.com/opensearch-project/query-insights/pull/628))
* Fix flaky grouper integration tests by waiting for settings propagation before searching ([#644](https://github.com/opensearch-project/query-insights/pull/644))


### OpenSearch Query Insights Dashboards


* Fix flaky top\_queries Timestamp-sort Cypress test by reloading until data populates ([#573](https://github.com/opensearch-project/query-insights-dashboards/pull/573))
* Fix main CI failures by bumping @babel/runtime to ^7.29.7 and removing unpinnable composite action from binary-install workflow ([#549](https://github.com/opensearch-project/query-insights-dashboards/pull/549))


### OpenSearch Reporting


* Accept nullable ResourceSharingClient to prevent NPE when resource-sharing feature is disabled ([#1204](https://github.com/opensearch-project/reporting/pull/1204))


### OpenSearch Search Relevance


* Fix experiment search requests wrapping query in base64-encoded wrapper, which broke search pipeline field path resolution for processors like `ml_inference` ([#490](https://github.com/opensearch-project/search-relevance/pull/490))
* Fix BWC SearchConfigMapping tests by creating referenced index before search config creation to satisfy referential integrity validation ([#497](https://github.com/opensearch-project/search-relevance/pull/497))


### OpenSearch Security


* Fix API token count results returning empty when DLS/FLS layer blocks authorized requests ([#6218](https://github.com/opensearch-project/security/pull/6218))
* Fix Argon2PasswordHasher locale-sensitive `toUpperCase` bug causing failures in Turkish/Azerbaijani locales ([#6208](https://github.com/opensearch-project/security/pull/6208))
* Fix ClassCastException for otherName SAN entries during inter-cluster handshake ([#6137](https://github.com/opensearch-project/security/pull/6137))
* Fix `_cat/indices` returning 403 when `securitytenant` header is present ([#6284](https://github.com/opensearch-project/security/pull/6284))
* Fix Kafka sink test compatibility with Kafka 4.3 by using KafkaClusterTestKit directly ([#6225](https://github.com/opensearch-project/security/pull/6225))


### OpenSearch Security Analytics


* Fix mutable script params for detector trigger actions ([#1722](https://github.com/opensearch-project/security-analytics/pull/1722))


### OpenSearch Security Dashboards Plugin


* Disable multi-tenancy in multi-data-source tests to fix credential lookup failures ([#2479](https://github.com/opensearch-project/security-dashboards-plugin/pull/2479))
* Update proxy-agent to v8 to resolve CVE-2026-44240 and CVE-2026-42338 ([#2440](https://github.com/opensearch-project/security-dashboards-plugin/pull/2440))


### OpenSearch Skills


* Fix compilation failure due to AD method signature change ([#758](https://github.com/opensearch-project/skills/pull/758))


### OpenSearch k-NN


* Fix FAISS SQ merge failure when a segment has no live vectors due to document deletion ([#3381](https://github.com/opensearch-project/k-NN/pull/3381))
* Fix inner-product score conversion for FAISS when Memory Optimized Search is enabled ([#3369](https://github.com/opensearch-project/k-NN/pull/3369))
* Fix incorrect FP16 validation being applied to SQ encoder with `bits=1` (x32 compression) ([#3366](https://github.com/opensearch-project/k-NN/pull/3366))
* Fix score corruption in multi-segment FAISS indices with ADC due to shared query vector mutation ([#3385](https://github.com/opensearch-project/k-NN/pull/3385))
* Fix NullPointerException in nested KNN search when index contains documents without the nested object ([#3368](https://github.com/opensearch-project/k-NN/pull/3368))


### SQL


* Fix `ClassCastException` in PPL multisearch on indexes with `@timestamp` alias field ([#5577](https://github.com/opensearch-project/sql/pull/5577))
* Fix PPL `foreach` JSON array type coercion to handle non-numeric elements gracefully ([#5637](https://github.com/opensearch-project/sql/pull/5637))
* Detect long (BIGINT) arithmetic overflow instead of silently wrapping ([#5604](https://github.com/opensearch-project/sql/pull/5604))
* Preserve SQL-layer profiling alongside the analytics-engine profile ([#5571](https://github.com/opensearch-project/sql/pull/5571))
* Propagate request-task cancellation into the analytics PPL route ([#5563](https://github.com/opensearch-project/sql/pull/5563))
* Return 4xx instead of 500 for unsupported window functions ([#5587](https://github.com/opensearch-project/sql/pull/5587))
* Fix `SHOW`/`DESCRIBE` statement routing under `cluster.pluggable.dataformat` setting ([#5528](https://github.com/opensearch-project/sql/pull/5528))
* Handle opaque `NullPointerException` for unresolvable alias-type field path with a clear error ([#5536](https://github.com/opensearch-project/sql/pull/5536))
* Fix invalid field or index error misclassified as internal 500 failures ([#5532](https://github.com/opensearch-project/sql/pull/5532))
* Fix `GROUP BY` expression resolution in `SELECT`/`HAVING`/`ORDER BY` ([#5548](https://github.com/opensearch-project/sql/pull/5548))
* Fix SQL window functions with `ORDER BY`/`LIMIT` on unified query path ([#5592](https://github.com/opensearch-project/sql/pull/5592))
* Fix dedup field name mapping to handle alias collision when rename and eval resolve to the same source field ([#5593](https://github.com/opensearch-project/sql/pull/5593))
* Allow partial pushdown for semi-scripted predicates so pushable filters are not blocked by unsupported ones ([#5565](https://github.com/opensearch-project/sql/pull/5565))
* Gracefully handle malformed documents in result scanning instead of crashing ([#5618](https://github.com/opensearch-project/sql/pull/5618))
* Honor PPL `fetch_size` on the analytics-engine route ([#5567](https://github.com/opensearch-project/sql/pull/5567))
* Strip analytics-engine-unsupported fields from test data and exclude affected ITs ([#5541](https://github.com/opensearch-project/sql/pull/5541))
* Repair two pre-existing IT failures on main (error type assertion and explain flake) ([#5545](https://github.com/opensearch-project/sql/pull/5545))


## INFRASTRUCTURE


### OpenSearch Alerting


* Pin GitHub Actions to commit SHAs for supply chain security ([#2156](https://github.com/opensearch-project/alerting/pull/2156))
* Onboard new backport-pr reusable GitHub workflow for alerting ([#2183](https://github.com/opensearch-project/alerting/pull/2183))
* Update maven2 mirror repository URL order ([#2188](https://github.com/opensearch-project/alerting/pull/2188))


### OpenSearch Alerting Dashboards Plugin


* Pin GitHub Actions to commit SHAs for supply chain security ([#1456](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1456))
* Adopt ESLint 10 flat config and remove legacy `.eslintrc` ([#1486](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1486))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#1490](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1490))
* Remove direct `@babel/plugin-transform-modules-commonjs` dependency and use transitive dependency from OSD ([#1491](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1491))
* Onboard new backport-pr reusable GitHub workflow ([#1478](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1478))


### OpenSearch Anomaly Detection


* Update opensearch-build reusable workflow references from pinned SHA to @main branch ([#1738](https://github.com/opensearch-project/anomaly-detection/pull/1738))


### OpenSearch Anomaly Detection Dashboards Plugin


* Pin GitHub Actions to commit SHAs for supply chain security ([#1201](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1201))
* Update GitHub actions to use official opensearch-project actions ([#1211](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1211))
* Improve test coverage for Daily Insights components and hooks ([#1192](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1192))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#1226](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1226))
* Adopt ESLint 10 with flat config format ([#1223](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1223))
* Onboard new backport-pr reusable GitHub workflow ([#1217](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1217))


### OpenSearch Common Utils


* Onboard new backport-pr reusable GitHub workflow ([#974](https://github.com/opensearch-project/common-utils/pull/974))
* Update opensearch-build workflow references from SHA to @main ([#971](https://github.com/opensearch-project/common-utils/pull/971))


### OpenSearch Cross Cluster Replication


* Onboard new backport-pr reusable GitHub workflow for cross-cluster-replication ([#1710](https://github.com/opensearch-project/cross-cluster-replication/pull/1710))
* Pin all GitHub Actions to full-length commit SHAs for supply-chain security compliance ([#1706](https://github.com/opensearch-project/cross-cluster-replication/pull/1706))


### OpenSearch Custom Codecs


* Update opensearch-build workflow references from commit SHA to main branch ([#346](https://github.com/opensearch-project/custom-codecs/pull/346))


### OpenSearch Dashboards Assistant


* Migrate Jest test suite to Jest 30 and jsdom 26 ([#717](https://github.com/opensearch-project/dashboards-assistant/pull/717))
* Adopt ESLint 10 flat config format ([#711](https://github.com/opensearch-project/dashboards-assistant/pull/711))
* Onboard new backport-pr reusable GitHub workflow ([#705](https://github.com/opensearch-project/dashboards-assistant/pull/705))
* Use correct OSD main branch reference in workflow ([#712](https://github.com/opensearch-project/dashboards-assistant/pull/712))


### OpenSearch Dashboards Flow Framework


* Pin GitHub Actions to commit SHAs to prevent supply chain attacks ([#890](https://github.com/opensearch-project/dashboards-flow-framework/pull/890))
* Adopt ESLint 10 with flat config format and apply Prettier 3 formatting ([#903](https://github.com/opensearch-project/dashboards-flow-framework/pull/903))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#906](https://github.com/opensearch-project/dashboards-flow-framework/pull/906))


### OpenSearch Dashboards Investigation


* Pin GitHub Actions to commit SHAs to prevent supply chain attacks ([#375](https://github.com/opensearch-project/dashboards-investigation/pull/375))
* Update GitHub actions to use official opensearch-project actions instead of personal forks ([#386](https://github.com/opensearch-project/dashboards-investigation/pull/386))
* Update opensearch-build workflow references from commit SHA to main branch ([#384](https://github.com/opensearch-project/dashboards-investigation/pull/384))
* Migrate ESLint configuration to ESLint 10 flat config format ([#398](https://github.com/opensearch-project/dashboards-investigation/pull/398))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#403](https://github.com/opensearch-project/dashboards-investigation/pull/403))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#391](https://github.com/opensearch-project/dashboards-investigation/pull/391))
* Onboard new backport-pr reusable GitHub workflow replacing obsolete backport workflows ([#389](https://github.com/opensearch-project/dashboards-investigation/pull/389))
* Downgrade codecov-action to v4 to fix intermittent GPG validation failures in CI ([#394](https://github.com/opensearch-project/dashboards-investigation/pull/394))


### OpenSearch Dashboards Maps


* Adopt ESLint 10 flat config to align with OpenSearch Dashboards core linting setup ([#847](https://github.com/opensearch-project/dashboards-maps/pull/847))
* Migrate Jest test suite to Jest 30 and jsdom 26 to match core OpenSearch Dashboards test infrastructure ([#852](https://github.com/opensearch-project/dashboards-maps/pull/852))


### OpenSearch Dashboards Notifications


* Migrate linting setup to ESLint 10 flat config ([#472](https://github.com/opensearch-project/dashboards-notifications/pull/472))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#475](https://github.com/opensearch-project/dashboards-notifications/pull/475))
* Onboard new backport-pr reusable GitHub workflow ([#464](https://github.com/opensearch-project/dashboards-notifications/pull/464))


### OpenSearch Dashboards Observability


* Update opensearch-build workflow references from commit SHA to main branch ([#2731](https://github.com/opensearch-project/dashboards-observability/pull/2731))
* Update GitHub actions to use official opensearch-project actions ([#2749](https://github.com/opensearch-project/dashboards-observability/pull/2749))
* Onboard new backport-pr reusable GitHub workflow ([#2760](https://github.com/opensearch-project/dashboards-observability/pull/2760))


### OpenSearch Dashboards Query Workbench


* Migrate ESLint configuration to ESLint 10 flat config format ([#574](https://github.com/opensearch-project/dashboards-query-workbench/pull/574))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#577](https://github.com/opensearch-project/dashboards-query-workbench/pull/577))


### OpenSearch Dashboards Reporting


* Pin GitHub Actions to commit SHAs to prevent supply chain attacks ([#752](https://github.com/opensearch-project/dashboards-reporting/pull/752))
* Adopt ESLint 10 flat config format, replacing legacy .eslintrc.js and .eslintignore ([#784](https://github.com/opensearch-project/dashboards-reporting/pull/784))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#787](https://github.com/opensearch-project/dashboards-reporting/pull/787))
* Onboard new backport-pr reusable GitHub workflow for dashboards-reporting ([#773](https://github.com/opensearch-project/dashboards-reporting/pull/773))


### OpenSearch Dashboards Search Relevance


* Add unit tests for metrics route handler ([#903](https://github.com/opensearch-project/dashboards-search-relevance/pull/903))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#909](https://github.com/opensearch-project/dashboards-search-relevance/pull/909))


### OpenSearch Index Management


* Add CI mirror repository to avoid Maven Central throttling during builds ([#1650](https://github.com/opensearch-project/index-management/pull/1650))
* Update opensearch-build workflow references from commit SHA to main branch ([#1672](https://github.com/opensearch-project/index-management/pull/1672))
* Replace deprecated tibdex/github-app-token with actions/create-github-app-token ([#1663](https://github.com/opensearch-project/index-management/pull/1663))
* Remove unused release-drafter workflow ([#1686](https://github.com/opensearch-project/index-management/pull/1686))
* Bump actions/checkout from 6.0.3 to 7.0.0 ([#1674](https://github.com/opensearch-project/index-management/pull/1674))
* Bump actions/download-artifact from 7.0.0 to 8.0.1 ([#1653](https://github.com/opensearch-project/index-management/pull/1653))
* Bump actions/setup-java from 5.2.0 to 5.4.0 ([#1684](https://github.com/opensearch-project/index-management/pull/1684))
* Bump aws-actions/configure-aws-credentials from 6.1.1 to 6.2.1 ([#1683](https://github.com/opensearch-project/index-management/pull/1683))
* Bump codecov/codecov-action from 4.6.0 to 7.0.0 ([#1682](https://github.com/opensearch-project/index-management/pull/1682))
* Bump release-drafter/release-drafter from 6.4.0 to 7.3.1 ([#1658](https://github.com/opensearch-project/index-management/pull/1658))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#1685](https://github.com/opensearch-project/index-management/pull/1685))
* Onboard new backport-pr reusable GitHub workflow ([#1678](https://github.com/opensearch-project/index-management/pull/1678))


### OpenSearch Index Management Dashboards Plugin


* Migrate Jest test suite to Jest 30 and jsdom 26 ([#1459](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1459))
* Adopt ESLint 10 flat config format ([#1455](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1455))
* Update GitHub actions to use official opensearch-project actions ([#1442](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1442))
* Pin GitHub Actions to main ref in build repo ([#1434](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1434))
* Pin GitHub Actions to full-length commit SHAs for supply chain security ([#1445](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1445))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#1450](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1450))
* Onboard new backport-pr reusable GitHub workflow ([#1447](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1447))


### OpenSearch Job Scheduler


* Update opensearch-build workflow references from commit SHA to main branch ([#938](https://github.com/opensearch-project/job-scheduler/pull/938))


### OpenSearch ML Commons


* Pin GitHub Actions to commit SHAs ([#4828](https://github.com/opensearch-project/ml-commons/pull/4828))
* Onboard new reusable backport-pr GitHub workflow ([#4873](https://github.com/opensearch-project/ml-commons/pull/4873))
* Update maven2 mirror repository URL order ([#4887](https://github.com/opensearch-project/ml-commons/pull/4887))
* Fix flaky IT `testChatAgentWithMcpStreamableHttpConnector` and add timeout ([#4851](https://github.com/opensearch-project/ml-commons/pull/4851))
* Retry integration tests on transient remote-service 5xx errors ([#4896](https://github.com/opensearch-project/ml-commons/pull/4896))
* Disable fail-fast on CI matrix so Java 21/25 jobs run independently ([#4899](https://github.com/opensearch-project/ml-commons/pull/4899))
* Fix flaky CI: httpbin dependency, MCP tool sync race, and SearchModelGroupITTests hang ([#4903](https://github.com/opensearch-project/ml-commons/pull/4903))
* Add `jiapingzeng` as maintainer ([#4910](https://github.com/opensearch-project/ml-commons/pull/4910))
* Bump bc-fips to 2.1.3 in plugin test classpath to fix CVE-2026-8149 ([#4923](https://github.com/opensearch-project/ml-commons/pull/4923))


### OpenSearch ML Commons Dashboards


* Adopt ESLint 10 with flat configuration and apply Prettier 3 formatting ([#505](https://github.com/opensearch-project/ml-commons-dashboards/pull/505))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#507](https://github.com/opensearch-project/ml-commons-dashboards/pull/507))
* Pin GitHub Actions to commit SHAs for supply chain security ([#487](https://github.com/opensearch-project/ml-commons-dashboards/pull/487))
* Update GitHub Actions to use official opensearch-project actions ([#496](https://github.com/opensearch-project/ml-commons-dashboards/pull/496))
* Update opensearch-build workflow references from commit SHA to main branch ([#495](https://github.com/opensearch-project/ml-commons-dashboards/pull/495))
* Onboard new backport-pr reusable GitHub workflow ([#501](https://github.com/opensearch-project/ml-commons-dashboards/pull/501))


### OpenSearch Neural Search


* Fix Check Workflow Events CI job by adding `pr_review.yml` to the allowlist and removing stray YAML fragment ([#1901](https://github.com/opensearch-project/neural-search/pull/1901))
* Fix flaky `HybridQueryExplainIT` explanation test by using per-document `_id` assertions ([#1900](https://github.com/opensearch-project/neural-search/pull/1900))
* Onboard new backport-pr reusable GitHub workflow ([#1881](https://github.com/opensearch-project/neural-search/pull/1881))


### OpenSearch Notifications


* Onboard new backport-pr reusable GitHub workflow to replace obsolete backport-related workflows ([#1240](https://github.com/opensearch-project/notifications/pull/1240))
* Pin GitHub Actions to commit SHAs to prevent supply chain attacks from mutable tag references ([#1231](https://github.com/opensearch-project/notifications/pull/1231))


### OpenSearch OpenSearch Learning To Rank Base


* Update opensearch-build GitHub Actions SHA references to fix security policy failures ([#343](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/343))
* Pin CI tasks to opensearch-build main branch instead of a specific commit ([#344](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/344))
* Update Codecov settings to use base branch coverage as target and add patch coverage requirements ([#339](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/339))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#318](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/318))
* Onboard new backport-pr reusable GitHub workflow ([#372](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/372))
* Update maven2 mirror repository URL order ([#375](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/375))


### OpenSearch OpenSearch Remote Metadata Sdk


* Update opensearch-build workflow references from commit SHA to main branch ([#412](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/412))


### OpenSearch Query Insights


* Fix GitHub Actions SHA-pinning policy failures for code-hygiene gradle action and opensearch-build ref ([#621](https://github.com/opensearch-project/query-insights/pull/621))
* Onboard new backport-pr reusable GitHub workflow ([#627](https://github.com/opensearch-project/query-insights/pull/627))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#632](https://github.com/opensearch-project/query-insights/pull/632))
* Bump httpclient5 to 5.6.1 to address CVE-2026-40542 ([#633](https://github.com/opensearch-project/query-insights/pull/633))
* Update maven2 mirror repository URL order ([#638](https://github.com/opensearch-project/query-insights/pull/638))


### OpenSearch Query Insights Dashboards


* Adopt ESLint 10 with flat config format, replacing legacy .eslintrc.js configuration ([#566](https://github.com/opensearch-project/query-insights-dashboards/pull/566))
* Pin get-ci-image-tag reusable workflow to a SHA with pinned nested actions to satisfy org SHA-pin policy ([#555](https://github.com/opensearch-project/query-insights-dashboards/pull/555))
* Replace start-opensearch composite action in WLM security Cypress workflow to satisfy SHA-pin policy ([#556](https://github.com/opensearch-project/query-insights-dashboards/pull/556))
* Use official opensearch-build start-opensearch action for OpenSearch startup in CI ([#559](https://github.com/opensearch-project/query-insights-dashboards/pull/559))
* Update opensearch-build workflow references from commit SHA to main branch ([#539](https://github.com/opensearch-project/query-insights-dashboards/pull/539))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#571](https://github.com/opensearch-project/query-insights-dashboards/pull/571))


### OpenSearch Reporting


* Pin GitHub Actions to commit SHAs for supply chain security ([#1187](https://github.com/opensearch-project/reporting/pull/1187))
* Onboard new backport-pr reusable GitHub workflow for reporting ([#1197](https://github.com/opensearch-project/reporting/pull/1197))
* Update maven2 mirror repository URL order ([#1201](https://github.com/opensearch-project/reporting/pull/1201))


### OpenSearch Security


* Adapt additional tests for testing conventions using randomized test base ([#6205](https://github.com/opensearch-project/security/pull/6205))
* Enable `bootstrap.serial_filter` in integration tests ([#6229](https://github.com/opensearch-project/security/pull/6229))
* Enable logger usage checks in security subprojects and update GitHub Actions Gradle steps ([#6210](https://github.com/opensearch-project/security/pull/6210))
* Enhance robustness of InternalOpenSearchSink tests through scenario-driven coverage and refactoring ([#6146](https://github.com/opensearch-project/security/pull/6146))
* Inline `get-opensearch-version` in create-bwc-build action to remove external dependency ([#6228](https://github.com/opensearch-project/security/pull/6228))
* Onboard new backport-pr reusable GitHub workflow ([#6250](https://github.com/opensearch-project/security/pull/6250))
* Replace `tibdex/github-app-token` with `actions/create-github-app-token` ([#6219](https://github.com/opensearch-project/security/pull/6219))
* Restore CI after setup-gradle v6 upgrade ([#6302](https://github.com/opensearch-project/security/pull/6302))
* Use opensearch-build start OpenSearch action in plugin install workflow ([#6216](https://github.com/opensearch-project/security/pull/6216))


### OpenSearch Security Analytics


* Pin GitHub Actions to full commit SHAs for supply chain security ([#1736](https://github.com/opensearch-project/security-analytics/pull/1736))
* Pin GitHub Actions to commit SHAs to prevent supply chain attacks ([#1727](https://github.com/opensearch-project/security-analytics/pull/1727))


### OpenSearch Security Analytics Dashboards Plugin


* Migrate ESLint configuration to ESLint 10 flat config format ([#1552](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1552))
* Migrate Jest test suite to Jest 30 and jsdom 26 for compatibility with OpenSearch Dashboards core ([#1555](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1555))


### OpenSearch Security Dashboards Plugin


* Use opensearch-build composite actions for OpenSearch and OpenSearch Dashboards setup in CI workflows ([#2443](https://github.com/opensearch-project/security-dashboards-plugin/pull/2443))
* Update opensearch-build action SHA to include OSD snapshot URL fix ([#2445](https://github.com/opensearch-project/security-dashboards-plugin/pull/2445))
* Switch whitesource configMode to AUTO for automatic branch scanning ([#2447](https://github.com/opensearch-project/security-dashboards-plugin/pull/2447))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#2475](https://github.com/opensearch-project/security-dashboards-plugin/pull/2475))
* Bump actions/checkout from 6.0.2 to 7.0.0 ([#2449](https://github.com/opensearch-project/security-dashboards-plugin/pull/2449))
* Bump actions/setup-java from 5.2.0 to 5.3.0 ([#2451](https://github.com/opensearch-project/security-dashboards-plugin/pull/2451))
* Bump actions/setup-java from 5.3.0 to 5.4.0 ([#2460](https://github.com/opensearch-project/security-dashboards-plugin/pull/2460))
* Bump lycheeverse/lychee-action to 39066c6 ([#2450](https://github.com/opensearch-project/security-dashboards-plugin/pull/2450))
* Bump lycheeverse/lychee-action to e747777 ([#2461](https://github.com/opensearch-project/security-dashboards-plugin/pull/2461))
* Bump opensearch-project/opensearch-build to 3d9a524 ([#2448](https://github.com/opensearch-project/security-dashboards-plugin/pull/2448))


### OpenSearch Skills


* Update actions/setup-java action to v5 ([#736](https://github.com/opensearch-project/skills/pull/736))
* Update opensearch-build workflow references from commit SHA to main branch ([#749](https://github.com/opensearch-project/skills/pull/749))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#764](https://github.com/opensearch-project/skills/pull/764))
* Onboard new backport-pr reusable GitHub workflow ([#759](https://github.com/opensearch-project/skills/pull/759))
* Update maven2 mirror repository URL order ([#767](https://github.com/opensearch-project/skills/pull/767))


### OpenSearch User Behavior Insights


* Update opensearch-build workflow references from commit SHA to main branch ([#189](https://github.com/opensearch-project/user-behavior-insights/pull/189))


### OpenSearch k-NN


* Parameterize integration tests based on compression level to ensure stability for 32x default compression ([#3416](https://github.com/opensearch-project/k-NN/pull/3416))


### SQL


* Bring `CalciteBinCommandIT` and `CalciteMultisearchCommandIT` to parity on the analytics-engine route ([#5551](https://github.com/opensearch-project/sql/pull/5551))
* Bring `CalcitePPLEnhancedCoalesceIT` to parity on the analytics-engine route ([#5552](https://github.com/opensearch-project/sql/pull/5552))
* Bring `CalcitePPLJoinIT` to parity on the analytics-engine route ([#5554](https://github.com/opensearch-project/sql/pull/5554))
* Stabilize `CalcitePPLConditionBuiltinFunctionIT` on the analytics-engine route ([#5556](https://github.com/opensearch-project/sql/pull/5556))
* Stabilize `CalciteStreamstatsCommandIT` on the analytics-engine route ([#5582](https://github.com/opensearch-project/sql/pull/5582))
* Stabilize PPL ITs on the analytics-engine route (array/map-path/datatype/basic) ([#5562](https://github.com/opensearch-project/sql/pull/5562))
* Stabilize PPL ITs on the analytics-engine route (case/string/full-text/like/appendpipe) ([#5561](https://github.com/opensearch-project/sql/pull/5561))
* Stabilize PPL ITs on the analytics-engine route (percentile/float/datetime/json/dedup/union/rename/chart) ([#5564](https://github.com/opensearch-project/sql/pull/5564))
* Stabilize PPL ITs on the analytics-engine route (sort/streamstats/IP-UDT/metadata/strip-verifier) ([#5566](https://github.com/opensearch-project/sql/pull/5566))
* Stabilize subquery PPL ITs on the analytics-engine route ([#5555](https://github.com/opensearch-project/sql/pull/5555))
* Recover concrete schema type for ANY-typed columns on the analytics route (fixes eval max/min) ([#5557](https://github.com/opensearch-project/sql/pull/5557))
* Fix SQL IT test queries, assertions, and data for engine-agnostic compatibility ([#5584](https://github.com/opensearch-project/sql/pull/5584))
* Gate analytics-engine incompatible IT tests with capability matrix annotations ([#5585](https://github.com/opensearch-project/sql/pull/5585))
* Decouple IT from execution backend with capability-based gating ([#5560](https://github.com/opensearch-project/sql/pull/5560))
* Fix doctest job-scheduler dependency resolution for 3.8.0 ([#5540](https://github.com/opensearch-project/sql/pull/5540))
* Bump Apache Calcite 1.41.0 → 1.42.0 (CVE-2026-46718) ([#5619](https://github.com/opensearch-project/sql/pull/5619))
* Bump `get-ci-image-tag.yml` ref to SHA-pinned opensearch-build commit to unblock CI ([#5583](https://github.com/opensearch-project/sql/pull/5583))
* Case test patches for missed optimizations ([#5531](https://github.com/opensearch-project/sql/pull/5531))
* Use engine-zone today in `DateTimeFunctionIT` now()-based assertions ([#5553](https://github.com/opensearch-project/sql/pull/5553))
* Update datetime tests to stay within analytics-engine epoch bounds ([#5534](https://github.com/opensearch-project/sql/pull/5534))


## DOCUMENTATION


### OpenSearch ML Commons


* Pass Gemini API key via header instead of URL in connector blueprint ([#4874](https://github.com/opensearch-project/ml-commons/pull/4874))
* Add LLM judgment connector blueprints ([#4878](https://github.com/opensearch-project/ml-commons/pull/4878))
* Use http instead of https for Ollama connector endpoint blueprint ([#4885](https://github.com/opensearch-project/ml-commons/pull/4885))


### OpenSearch k-NN


* Clarify changelog guidance to prevent incorrect release notes from stale entries ([#3380](https://github.com/opensearch-project/k-NN/pull/3380))


## MAINTENANCE


### OpenSearch Alerting


* Fix Jackson 3.x version conflict by aligning dependency versions with OpenSearch's jackson3 versions ([#2196](https://github.com/opensearch-project/alerting/pull/2196))


### OpenSearch Alerting Dashboards Plugin


* Resolve CVE-2026-2739, CVE-2025-69873, and GHSA-5c6j-r48x-rmvq by adding resolutions for bn.js and serialize-javascript ([#1476](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1476))


### OpenSearch Anomaly Detection Dashboards Plugin


* Bump axios from 1.15.2 to 1.17.0 ([#1206](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1206))
* Match jest-canvas-mock version with OpenSearch Dashboards core ([#1229](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1229))


### OpenSearch Common Utils


* Version bump to 3.8.0 ([#969](https://github.com/opensearch-project/common-utils/pull/969))


### OpenSearch Dashboards Assistant


* Bump ws from 8.20.0 to 8.21.0 to fix remote memory exhaustion DoS vulnerability ([#686](https://github.com/opensearch-project/dashboards-assistant/pull/686))


### OpenSearch Dashboards Investigation


* Clean up dependencies, remove Cypress, and fix CVE-2026-45736 by removing ws dependency ([#408](https://github.com/opensearch-project/dashboards-investigation/pull/408))
* Upgrade dompurify to comply with OSD version requirements ([#404](https://github.com/opensearch-project/dashboards-investigation/pull/404))


### OpenSearch Dashboards Maps


* Resolve transitive @types dependencies from Mapbox to MapLibre to remove Mapbox from the yarn lock file ([#849](https://github.com/opensearch-project/dashboards-maps/pull/849))


### OpenSearch Dashboards Notifications


* Remove qs dependency resolution and use it from OSD core ([#476](https://github.com/opensearch-project/dashboards-notifications/pull/476))


### OpenSearch Dashboards Observability


* Add APM, SLO, and Alerting nav popovers and rename Application Map to Topology Map ([#2762](https://github.com/opensearch-project/dashboards-observability/pull/2762))
* Adopt ESLint 10 flat config ([#2777](https://github.com/opensearch-project/dashboards-observability/pull/2777))
* Bump fast-uri from 3.1.0 to 3.1.2 ([#2673](https://github.com/opensearch-project/dashboards-observability/pull/2673))
* Bump js-yaml from 4.1.1 to 4.2.0 ([#2736](https://github.com/opensearch-project/dashboards-observability/pull/2736))
* Adopt dynamic feature flags for Alerts and SLO features ([#2719](https://github.com/opensearch-project/dashboards-observability/pull/2719))
* Increment version to 3.8.0 with Hapi compatibility fix and link checker hardening ([#2722](https://github.com/opensearch-project/dashboards-observability/pull/2722))
* Migrate Jest test suite to Jest 30 and jsdom 26 ([#2788](https://github.com/opensearch-project/dashboards-observability/pull/2788))
* Update dependency ajv to v8.20.0 to resolve CVE-2026-6321 and CVE-2026-6322 ([#2714](https://github.com/opensearch-project/dashboards-observability/pull/2714))
* Update dependency echarts to v6.1.0 to resolve CVE-2026-45249 ([#2715](https://github.com/opensearch-project/dashboards-observability/pull/2715))
* Update dependency isomorphic-dompurify to ~2.27.0 to resolve CVE-2026-45736 ([#2716](https://github.com/opensearch-project/dashboards-observability/pull/2716))
* Update dependency isomorphic-dompurify to ~2.28.0 ([#2735](https://github.com/opensearch-project/dashboards-observability/pull/2735))
* Update dependency isomorphic-dompurify to ~2.29.0 ([#2743](https://github.com/opensearch-project/dashboards-observability/pull/2743))
* Update dependency js-yaml to v4.3.0 to resolve CVE-2026-59869 ([#2782](https://github.com/opensearch-project/dashboards-observability/pull/2782))
* Bump uuid to ^11.1.1 to remediate CVE-2026-41907 ([#2765](https://github.com/opensearch-project/dashboards-observability/pull/2765))
* Pin picomatch and brace-expansion for CVE remediation ([#2751](https://github.com/opensearch-project/dashboards-observability/pull/2751))
* Bump dompurify from 3.4.10 to 3.4.12 ([#2752](https://github.com/opensearch-project/dashboards-observability/pull/2752))
* Exclude AnalyticEngine datasets from APM settings selectors ([#2727](https://github.com/opensearch-project/dashboards-observability/pull/2727))
* Update APM UI text and comments ([#2757](https://github.com/opensearch-project/dashboards-observability/pull/2757))
* Align EUI/OUI rule overrides with root OpenSearch Dashboards ESLint config ([#2785](https://github.com/opensearch-project/dashboards-observability/pull/2785))
* Remove direct js-yaml dependency and use core's bundled version ([#2791](https://github.com/opensearch-project/dashboards-observability/pull/2791))


### OpenSearch Index Management Dashboards Plugin


* Bump diff dependency to version 8 to align with OpenSearch Dashboards ([#1462](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1462))


### OpenSearch Job Scheduler


* Bump 1password/load-secrets-action from 4.0.0 to 4.0.1 ([#947](https://github.com/opensearch-project/job-scheduler/pull/947))
* Bump actions/checkout from 6.0.2 to 7.0.0 ([#954](https://github.com/opensearch-project/job-scheduler/pull/954))
* Bump actions/setup-java from 5.2.0 to 5.4.0 ([#944](https://github.com/opensearch-project/job-scheduler/pull/944))
* Bump actions/setup-java from 5.4.0 to 5.5.0 ([#956](https://github.com/opensearch-project/job-scheduler/pull/956))
* Bump actions/setup-java from 5.5.0 to 5.6.0 ([#959](https://github.com/opensearch-project/job-scheduler/pull/959))
* Bump aws-actions/configure-aws-credentials from 6.1.1 to 6.2.1 ([#949](https://github.com/opensearch-project/job-scheduler/pull/949))
* Bump aws-actions/configure-aws-credentials from 6.2.1 to 6.2.2 ([#955](https://github.com/opensearch-project/job-scheduler/pull/955))
* Bump lycheeverse/lychee-action to e7477775783ea5526144ba13e8db5eec57747ce8 ([#953](https://github.com/opensearch-project/job-scheduler/pull/953))
* Bump release-drafter/release-drafter from 7.3.0 to 7.5.1 ([#945](https://github.com/opensearch-project/job-scheduler/pull/945))


### OpenSearch OpenSearch Learning To Rank Base


* Upgrade RankyMcRankFace to 0.3.0 to address external entity DTD vulnerability ([#354](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/354))


### OpenSearch OpenSearch Remote Metadata Sdk


* Bump version to 3.8.0 ([#408](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/408))


### OpenSearch Query Insights Dashboards


* Bump form-data to 4.0.6 to address CVE-2026-12143 ([#550](https://github.com/opensearch-project/query-insights-dashboards/pull/550))
* Bump js-yaml to 4.3.0 to address CVE-2026-59869 ([#574](https://github.com/opensearch-project/query-insights-dashboards/pull/574))
* Bump js-yaml to 4.2.0 and qs to 6.15.2 to address CVE-2026-53550 and CVE-2026-8723 ([#564](https://github.com/opensearch-project/query-insights-dashboards/pull/564))
* Bump tmp to 0.2.7 and ws to 7.5.11 to address CVE-2026-44705 and CVE-2026-48779 ([#560](https://github.com/opensearch-project/query-insights-dashboards/pull/560))
* Update dependency echarts to v6.1.0 to address CVE-2026-45249 ([#532](https://github.com/opensearch-project/query-insights-dashboards/pull/532))


### OpenSearch Search Relevance


* Update updateVersion task and fix BWC version properties ([#475](https://github.com/opensearch-project/search-relevance/pull/475))
* Bump 1password/load-secrets-action from 4.0.0 to 4.0.1 ([#493](https://github.com/opensearch-project/search-relevance/pull/493))
* Bump actions/checkout from 6.0.3 to 7.0.0 ([#504](https://github.com/opensearch-project/search-relevance/pull/504))
* Bump actions/setup-java from 5.2.0 to 5.3.0 ([#505](https://github.com/opensearch-project/search-relevance/pull/505))
* Bump actions/setup-java from 5.3.0 to 5.4.0 ([#517](https://github.com/opensearch-project/search-relevance/pull/517))
* Bump actions/setup-java from 5.4.0 to 5.5.0 ([#526](https://github.com/opensearch-project/search-relevance/pull/526))
* Bump actions/setup-java from 5.5.0 to 5.6.0 ([#530](https://github.com/opensearch-project/search-relevance/pull/530))
* Bump aws-actions/configure-aws-credentials from 6.2.0 to 6.2.1 ([#516](https://github.com/opensearch-project/search-relevance/pull/516))
* Bump aws-actions/configure-aws-credentials from 6.2.1 to 6.2.2 ([#527](https://github.com/opensearch-project/search-relevance/pull/527))
* Bump com.diffplug.spotless:spotless-plugin-gradle from 8.6.0 to 8.7.0 ([#507](https://github.com/opensearch-project/search-relevance/pull/507))
* Bump com.diffplug.spotless:spotless-plugin-gradle from 8.7.0 to 8.8.0 ([#524](https://github.com/opensearch-project/search-relevance/pull/524))
* Bump com.google.errorprone:error\_prone\_annotations from 2.49.0 to 2.50.0 ([#491](https://github.com/opensearch-project/search-relevance/pull/491))
* Bump gradle-wrapper from 9.5.1 to 9.6.0 ([#506](https://github.com/opensearch-project/search-relevance/pull/506))
* Bump gradle-wrapper from 9.6.0 to 9.6.1 ([#518](https://github.com/opensearch-project/search-relevance/pull/518))
* Bump opensearch-project/opensearch-build/.github/workflows/get-ci-image-tag.yml ([#486](https://github.com/opensearch-project/search-relevance/pull/486))
* Bump org.javassist:javassist from 3.31.0-GA to 3.32.0-GA ([#508](https://github.com/opensearch-project/search-relevance/pull/508))
* Bump org.json:json from 20260522 to 20260719 ([#529](https://github.com/opensearch-project/search-relevance/pull/529))


### OpenSearch Security


* Add Rishav Kumar as a co-maintainer of the Security repo ([#6223](https://github.com/opensearch-project/security/pull/6223))
* Bump 1password/load-secrets-action from 4.0.0 to 4.0.1 ([#6234](https://github.com/opensearch-project/security/pull/6234))
* Bump actions/checkout from 6.0.2 to 7.0.0 ([#6231](https://github.com/opensearch-project/security/pull/6231))
* Bump actions/setup-java from 5.2.0 to 5.4.0 ([#6256](https://github.com/opensearch-project/security/pull/6256))
* Bump actions/setup-java from 5.4.0 to 5.5.0 ([#6290](https://github.com/opensearch-project/security/pull/6290))
* Bump at.yawk.lz4:lz4-java from 1.11.0 to 1.11.1 ([#6319](https://github.com/opensearch-project/security/pull/6319))
* Bump aws-actions/configure-aws-credentials from 6.1.1 to 6.2.1 ([#6258](https://github.com/opensearch-project/security/pull/6258))
* Bump aws-actions/configure-aws-credentials from 6.2.1 to 6.2.2 ([#6314](https://github.com/opensearch-project/security/pull/6314))
* Bump ch.qos.logback:logback-classic from 1.5.34 to 1.5.37 ([#6260](https://github.com/opensearch-project/security/pull/6260))
* Bump ch.qos.logback:logback-classic from 1.5.37 to 1.5.38 ([#6298](https://github.com/opensearch-project/security/pull/6298))
* Bump codecov/codecov-action from 4.6.0 to 7.0.0 ([#6257](https://github.com/opensearch-project/security/pull/6257))
* Bump com.autonomousapps.build-health from 3.10.0 to 3.15.0 ([#6238](https://github.com/opensearch-project/security/pull/6238))
* Bump com.autonomousapps.build-health from 3.15.0 to 3.16.0 ([#6282](https://github.com/opensearch-project/security/pull/6282))
* Bump com.autonomousapps.build-health from 3.16.0 to 3.16.1 ([#6300](https://github.com/opensearch-project/security/pull/6300))
* Bump com.autonomousapps.build-health from 3.16.1 to 3.17.0 ([#6318](https://github.com/opensearch-project/security/pull/6318))
* Bump com.github.spotbugs from 6.5.5 to 6.5.8 ([#6263](https://github.com/opensearch-project/security/pull/6263))
* Bump com.github.spotbugs from 6.5.8 to 6.5.9 ([#6297](https://github.com/opensearch-project/security/pull/6297))
* Bump commons-logging:commons-logging from 1.3.6 to 1.4.0 ([#6240](https://github.com/opensearch-project/security/pull/6240))
* Bump github/codeql-action from 4.36.0 to 4.36.2 ([#6233](https://github.com/opensearch-project/security/pull/6233))
* Bump github/codeql-action/analyze from 4.36.3 to 4.37.0 ([#6292](https://github.com/opensearch-project/security/pull/6292))
* Bump github/codeql-action/analyze from 4.37.0 to 4.37.1 ([#6315](https://github.com/opensearch-project/security/pull/6315))
* Bump github/codeql-action/init from 4.36.2 to 4.36.3 ([#6281](https://github.com/opensearch-project/security/pull/6281))
* Bump github/codeql-action/init from 4.36.3 to 4.37.0 ([#6289](https://github.com/opensearch-project/security/pull/6289))
* Bump github/codeql-action/init from 4.37.0 to 4.37.1 ([#6313](https://github.com/opensearch-project/security/pull/6313))
* Bump gradle-wrapper from 9.5.1 to 9.6.1 ([#6262](https://github.com/opensearch-project/security/pull/6262))
* Bump io.dropwizard.metrics:metrics-core from 4.2.38 to 4.2.39 ([#6239](https://github.com/opensearch-project/security/pull/6239))
* Bump io.projectreactor:reactor-core from 3.8.5 to 3.8.6 ([#6214](https://github.com/opensearch-project/security/pull/6214))
* Bump kafka\_version from 4.3.0 to 4.3.1 ([#6259](https://github.com/opensearch-project/security/pull/6259))
* Bump lycheeverse/lychee-action to 649b0e4890508ea3e11ea6b3ee35ce899a25afd5 ([#6291](https://github.com/opensearch-project/security/pull/6291))
* Bump net.bytebuddy:byte-buddy from 1.18.10 to 1.18.11 ([#6283](https://github.com/opensearch-project/security/pull/6283))
* Bump net.bytebuddy:byte-buddy from 1.18.8 to 1.18.10 ([#6261](https://github.com/opensearch-project/security/pull/6261))
* Bump open\_saml from 5.2.2 to 5.2.3 ([#6237](https://github.com/opensearch-project/security/pull/6237))
* Bump open\_saml\_shib from 9.2.2 to 9.2.3 ([#6235](https://github.com/opensearch-project/security/pull/6235))
* Bump org.bouncycastle:bcpkix-jdk18on from 1.84 to 1.85 ([#6294](https://github.com/opensearch-project/security/pull/6294))
* Bump org.eclipse.platform:org.eclipse.equinox.common from 3.20.300 to 3.20.400 ([#6211](https://github.com/opensearch-project/security/pull/6211))
* Bump org.springframework.kafka:spring-kafka-test from 4.0.5 to 4.1.0 ([#6213](https://github.com/opensearch-project/security/pull/6213))
* Bump release-drafter/release-drafter from 7.3.0 to 7.5.1 ([#6280](https://github.com/opensearch-project/security/pull/6280))
* Bump release-drafter/release-drafter from 7.5.1 to 7.6.0 ([#6317](https://github.com/opensearch-project/security/pull/6317))
* Bump spring\_framework from 7.0.7 to 7.0.8 ([#6212](https://github.com/opensearch-project/security/pull/6212))
* Bump stefanzweifel/git-auto-commit-action from 7.1.0 to 7.2.0 ([#6279](https://github.com/opensearch-project/security/pull/6279))


### OpenSearch Security Analytics Dashboards Plugin


* Resolve CVE-2026-2739, CVE-2025-69873, and GHSA-5c6j-r48x-rmv by updating bn.js and serialize-javascript dependencies ([#1541](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1541))
* Bump Babel packages to ^7.29.7 for OpenSearch Dashboards 3.8 compatibility ([#1556](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1556))


### OpenSearch Security Dashboards Plugin


* Adopt ESLint 10 flat config format and apply Prettier 3 formatting ([#2469](https://github.com/opensearch-project/security-dashboards-plugin/pull/2469))


### OpenSearch Skills


* Sync CODEOWNERS with maintainer list ([#755](https://github.com/opensearch-project/skills/pull/755))


### OpenSearch k-NN


* Upgrade to Lucene 10.5.0 ([#3411](https://github.com/opensearch-project/k-NN/pull/3411))


### SQL


* Fix flaky TPC-H Q15 floating-point assertion ([#5629](https://github.com/opensearch-project/sql/pull/5629))
* Fix lychee link checker ([#5451](https://github.com/opensearch-project/sql/pull/5451))


## REFACTORING


### OpenSearch Alerting Dashboards Plugin


* Drop unused `observabilityDashboards` optional plugin dependency and fix indentation ([#1464](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1464))


### OpenSearch Dashboards Investigation


* Refactor planner agent prompts to separate investigation-specific system prompts from common prompts and move dynamic fields to context ([#400](https://github.com/opensearch-project/dashboards-investigation/pull/400))
* Refactor plugin tests to instantiate InvestigationPlugin directly instead of re-implementing subscription logic ([#393](https://github.com/opensearch-project/dashboards-investigation/pull/393))


### OpenSearch Dashboards Observability


* Replace full-library lodash imports with path-based imports for tree-shaking ([#2748](https://github.com/opensearch-project/dashboards-observability/pull/2748))


### OpenSearch Dashboards Search Relevance


* Replace per-page data source selectors with a single global data source menu in the OSD chrome header, backed by URL-synced state ([#850](https://github.com/opensearch-project/dashboards-search-relevance/pull/850))
* Refactor GetSearchResults to single-query endpoint ([#868](https://github.com/opensearch-project/dashboards-search-relevance/pull/868))
* Remove debug console logging from production UI code ([#878](https://github.com/opensearch-project/dashboards-search-relevance/pull/878))
* Remove unused resource management home components ([#853](https://github.com/opensearch-project/dashboards-search-relevance/pull/853))


### OpenSearch Security


* Convert multi-line strings to text blocks in BasicAuditlogTest ([#6220](https://github.com/opensearch-project/security/pull/6220))


### OpenSearch Skills


* Use PPL instead of DSL match\_all query to fetch sample data in PPLTool ([#752](https://github.com/opensearch-project/skills/pull/752))


## NON-COMPLIANT


## BREAKING CHANGES


### OpenSearch Security


* Remove `own_index` default roles mapping, requiring explicit configuration if needed ([#6147](https://github.com/opensearch-project/security/pull/6147))

