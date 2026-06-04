# OpenSearch and OpenSearch Dashboards 3.7.0 Release Notes


## FEATURES


### OpenSearch Alerting


* Migrate all alerting persistence operations to SdkClient for remote metadata support ([#2093](https://github.com/opensearch-project/alerting/pull/2093))
* Add EventBridge Scheduler CRUD for external monitor scheduling ([#2096](https://github.com/opensearch-project/alerting/pull/2096))
* Add bucket-level trigger evaluation using standard bucket\_selector for multi-tenant environments ([#2098](https://github.com/opensearch-project/alerting/pull/2098))
* Block unsupported actions when multi-tenancy is enabled ([#2099](https://github.com/opensearch-project/alerting/pull/2099))
* Disable email, findings, and chained alert actions when multi-tenancy is enabled ([#2101](https://github.com/opensearch-project/alerting/pull/2101))
* Add MonitorJobPoller, ExternalSchedulerService, and SQS-based external monitor scheduling ([#2103](https://github.com/opensearch-project/alerting/pull/2103))
* Replace SchedulePayloadBuilder with ScheduleJobPayload for EB schedule target input ([#2104](https://github.com/opensearch-project/alerting/pull/2104))
* Add implementation for JobQueueAccountIdProvider ([#2105](https://github.com/opensearch-project/alerting/pull/2105))
* Use toXContentWithUser for SQS payload monitor serialization to include metadata and user context ([#2106](https://github.com/opensearch-project/alerting/pull/2106))
* Make MonitorJobPoller populate thread context for downstream request interception ([#2107](https://github.com/opensearch-project/alerting/pull/2107))
* Disable job scheduler indices when multi-tenancy is enabled ([#2108](https://github.com/opensearch-project/alerting/pull/2108))
* Add execution\_role\_arn setting for two-role EventBridge Scheduler model ([#2109](https://github.com/opensearch-project/alerting/pull/2109))
* Create SQS client in MonitorJobPoller.doStart when external scheduling is enabled ([#2110](https://github.com/opensearch-project/alerting/pull/2110))
* Add PPL alerting dependencies and cross-plugin communication utilities ([#2114](https://github.com/opensearch-project/alerting/pull/2114))
* Add AWS SDK dependencies with dynamic version ([#2116](https://github.com/opensearch-project/alerting/pull/2116))
* Preserve tenancy context across stashes and coroutines ([#2118](https://github.com/opensearch-project/alerting/pull/2118))
* Use role name and construct ARN at runtime for scheduler identities ([#2120](https://github.com/opensearch-project/alerting/pull/2120))
* Propagate tenant ID header in notification plugin client calls ([#2121](https://github.com/opensearch-project/alerting/pull/2121))
* Move delete monitor flow to remote metadata SDK ([#2125](https://github.com/opensearch-project/alerting/pull/2125))
* Add tenant ID to alerts service requests ([#2126](https://github.com/opensearch-project/alerting/pull/2126))
* Add PPL alerting monitor CRUD operations ([#2128](https://github.com/opensearch-project/alerting/pull/2128))
* Add PPL monitor execution support with RBAC checks for manual executions ([#2130](https://github.com/opensearch-project/alerting/pull/2130))
* Add tenant\_id to monitor metadata and propagate to AlertService SDK calls ([#2131](https://github.com/opensearch-project/alerting/pull/2131))
* Block non-PPL monitor CRUD on pluggable dataformat domains ([#2141](https://github.com/opensearch-project/alerting/pull/2141))
* Propagate tenant headers for remote monitor execution via ARN parsing ([#2143](https://github.com/opensearch-project/alerting/pull/2143))


### OpenSearch Alerting Dashboards Plugin


* Add workspace ACL authorization checks for Alerting and Monitor APIs ([#1415](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1415))
* Add icon-based sidebar navigation support for alerting plugin in Observability workspace ([#1418](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1418))


### OpenSearch Anomaly Detection Dashboards Plugin


* Add Daily Insights agent task polling, ML task API, and page stability fixes for async detector creation flow ([#1173](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1173))
* Add Daily Insights event detail modal with Discover deep links, per-anomaly navigation, and improved insight card UX ([#1184](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1184))
* Route AD results search through core `_search` on multi-tenant services where the AD backend plugin is unavailable ([#1190](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1190))
* Disable unsupported features (default result index, flattened result index, historical analysis) on multi-tenant services data sources ([#1189](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1189))
* Enforce workspace ACL and return 501 for unsupported routes on multi-tenant services data sources ([#1191](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1191))


### OpenSearch Common Utils


* Add ScheduleTranslator and MonitorPayloadBuilder for external monitor scheduling ([#939](https://github.com/opensearch-project/common-utils/pull/939))
* Add interface for SqsAccountIdProvider to retrieve account IDs for SQS job queues ([#942](https://github.com/opensearch-project/common-utils/pull/942))
* Add ScheduleJobPayload model for serializing externally scheduled monitor job payloads ([#943](https://github.com/opensearch-project/common-utils/pull/943))
* Add Target object for external data source support on Monitor and Alert models ([#941](https://github.com/opensearch-project/common-utils/pull/941))
* Add ARN field to Target for tenant header propagation to remote resources ([#956](https://github.com/opensearch-project/common-utils/pull/956))
* Add PPL-related models to support PPL Alerting behind existing Alerting APIs ([#940](https://github.com/opensearch-project/common-utils/pull/940))
* Add TenantContext extension for preserving tenancy context across coroutines ([#952](https://github.com/opensearch-project/common-utils/pull/952))
* Add helper to preserve tenant ID header across SecureClientWrapper thread context stash ([#953](https://github.com/opensearch-project/common-utils/pull/953))
* Expose bucketsPathsMap in BucketSelectorExtAggregationBuilder for remote trigger evaluation ([#949](https://github.com/opensearch-project/common-utils/pull/949))
* Add isIndexNotFoundException utility to AlertingException for SDK migration support ([#934](https://github.com/opensearch-project/common-utils/pull/934))


### OpenSearch Cross Cluster Replication


* Add support for clearing stale persistent tasks in Stop/Pause/Start/Resume APIs to prevent orphaned tasks from blocking replication operations ([#1629](https://github.com/opensearch-project/cross-cluster-replication/pull/1629))
* Add `cluster_manager_timeout` parameter support for all cross-cluster replication REST APIs ([#1638](https://github.com/opensearch-project/cross-cluster-replication/pull/1638))


### OpenSearch Dashboards Flow Framework


* Add agentic memory support for conversational agents ([#883](https://github.com/opensearch-project/dashboards-flow-framework/pull/883))
* Add embedding model ID configuration for agentic search ([#875](https://github.com/opensearch-project/dashboards-flow-framework/pull/875))
* Add fallback query configuration for QueryPlanningTool ([#872](https://github.com/opensearch-project/dashboards-flow-framework/pull/872))
* Add index alias support in agentic search UI ([#871](https://github.com/opensearch-project/dashboards-flow-framework/pull/871))


### OpenSearch Dashboards Investigation


* Support snapshot visualization in agentic notebook ([#369](https://github.com/opensearch-project/dashboards-investigation/pull/369))
* Support recoverable error handling for timeout and max retries failures ([#341](https://github.com/opensearch-project/dashboards-investigation/pull/341))
* Make default investigation initial goal configurable ([#361](https://github.com/opensearch-project/dashboards-investigation/pull/361))
* Add icon side nav branching for investigation notebooks in Observability workspace ([#368](https://github.com/opensearch-project/dashboards-investigation/pull/368))


### OpenSearch Dashboards Notifications


* Add workspace ACL authorization checks to notification APIs for workspace-level access control ([#445](https://github.com/opensearch-project/dashboards-notifications/pull/445))


### OpenSearch Dashboards Observability


* Add SLO/SLI foundation with saved-object schema, ruler client, routes, and minimal wizard behind feature flag ([#2676](https://github.com/opensearch-project/dashboards-observability/pull/2676))
* Add SLO/SLI follow-ups including ruler dual-write, wizard completeness, live status aggregator, listing facet filters, detail page, and APM integration ([#2689](https://github.com/opensearch-project/dashboards-observability/pull/2689))
* Add Alert Manager with Alerts, Rules, and Routing tabs backed by OpenSearch Alerting and Prometheus ([#2653](https://github.com/opensearch-project/dashboards-observability/pull/2653))


### OpenSearch Dashboards Search Relevance


* Add UI support for uploading Judgment Sets via CSV, enabling users to import judgments directly without manual API calls ([#715](https://github.com/opensearch-project/dashboards-search-relevance/pull/715))
* Render RRF variants in VariantDetailsModal by branching on combination type to display appropriate fields ([#836](https://github.com/opensearch-project/dashboards-search-relevance/pull/836))


### OpenSearch Flow Framework


* Add missing fields to workflow steps matching ml-commons builders, enabling MCP connector creation and unified agent interface ([#1360](https://github.com/opensearch-project/flow-framework/pull/1360))
* Add response processor to flow agent agentic search template for DSL query exposure ([#1367](https://github.com/opensearch-project/flow-framework/pull/1367))


### OpenSearch Index Management


* Add `reload_cached_resources` query parameter to `_refresh_search_analyzers` API for hot-reloading cached token filter resources (e.g., hunspell dictionaries) without node restart ([#1638](https://github.com/opensearch-project/index-management/pull/1638))


### OpenSearch ML Commons


* Add `provisioned_by` field to ML agents, connectors, and models for adoption metrics attribution ([#4754](https://github.com/opensearch-project/ml-commons/pull/4754))
* Enable dynamic header support in ML connectors using `${parameters.*}` placeholders for per-request values ([#4817](https://github.com/opensearch-project/ml-commons/pull/4817))
* Introduce V2 Chat Agent ([#4732](https://github.com/opensearch-project/ml-commons/pull/4732))


### OpenSearch Notifications


* Propagate tenant ID from REST header to SDK client requests for multi-tenant data isolation ([#1162](https://github.com/opensearch-project/notifications/pull/1162))


### OpenSearch Observability


* Support Jackson 3.x release line ([#1993](https://github.com/opensearch-project/observability/pull/1993))


### OpenSearch Query Insights


* Add recommendations parameter to Top Queries API for inline query recommendations ([#569](https://github.com/opensearch-project/query-insights/pull/569))


### OpenSearch Query Insights Dashboards


* Add Query Profiler tool to Dev Tools with visualization components for analyzing and visualizing query performance ([#475](https://github.com/opensearch-project/query-insights-dashboards/pull/475))
* Add Query Profiler tool integrated as a Dev Tools tab with split-pane editor for executing and viewing profiling output ([#472](https://github.com/opensearch-project/query-insights-dashboards/pull/472))
* Add remote S3 repository exporter to the configuration page for exporting query insights data ([#512](https://github.com/opensearch-project/query-insights-dashboards/pull/512))
* Add dynamic search bar with expression-based filtering to the Top N Queries page ([#510](https://github.com/opensearch-project/query-insights-dashboards/pull/510))
* Add task detail page with navigation from live queries ([#504](https://github.com/opensearch-project/query-insights-dashboards/pull/504))


### OpenSearch Reporting


* Support Jackson 3.x release line ([#1184](https://github.com/opensearch-project/reporting/pull/1184))


### OpenSearch Search Relevance


* Onboard z\_score normalization and RRF combination to HYBRID\_OPTIMIZER ([#465](https://github.com/opensearch-project/search-relevance/pull/465))


### OpenSearch Security


* Introduce API Tokens with cluster and index permissions directly associated with the token ([#5443](https://github.com/opensearch-project/security/pull/5443))
* Add general access field on sharing document to store a single access level for general access ([#6033](https://github.com/opensearch-project/security/pull/6033))
* Support fallback values in DLS/FLS variables ([#6111](https://github.com/opensearch-project/security/pull/6111))


### OpenSearch Security Dashboards Plugin


* Add security admin page to create, list, and revoke API keys ([#2388](https://github.com/opensearch-project/security-dashboards-plugin/pull/2388))


### OpenSearch Skills


* Add input\_schema to AbstractRetrieverTool and runtime parameter overrides to VectorDBTool for function calling and agentic search support ([#722](https://github.com/opensearch-project/skills/pull/722))


### OpenSearch k-NN


* Add base64 binary encoding as default format for knn\_vector docvalue\_fields, providing ~2x throughput improvement over array format ([#3324](https://github.com/opensearch-project/k-NN/pull/3324))
* Add capability to retrieve float data type vectors using doc\_values instead of reading \_source ([#3321](https://github.com/opensearch-project/k-NN/pull/3321))
* Support derived source for knn\_vector fields alongside other fields ([#3260](https://github.com/opensearch-project/k-NN/pull/3260))
* Add support for 1-bit scalar quantization with remote index build ([#3270](https://github.com/opensearch-project/k-NN/pull/3270))


### SQL


* Add Union command in PPL with type coercion and UNION ALL semantics ([#5240](https://github.com/opensearch-project/sql/pull/5240))
* Support SQL Vector Search via `vectorSearch()` table function with k-NN pushdown and filtering modes ([#5394](https://github.com/opensearch-project/sql/pull/5394))


## ENHANCEMENTS


### OpenSearch Anomaly Detection Dashboards Plugin


* Use `getIsIconSideNavEnabled` API for navigation registration in the Observability workspace ([#1187](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1187))


### OpenSearch Common Utils


* Hide metadata field from REST API responses using secure flag ([#948](https://github.com/opensearch-project/common-utils/pull/948))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#946](https://github.com/opensearch-project/common-utils/pull/946))
* Change max PPL Monitor name length from 30 to 100 ([#962](https://github.com/opensearch-project/common-utils/pull/962))


### OpenSearch Cross Cluster Replication


* Add diagnostic logging to improve troubleshooting of CCR replication failures ([#1659](https://github.com/opensearch-project/cross-cluster-replication/pull/1659))
* Onboard code diff analyzer/reviewer and issue deduplication workflows ([#1665](https://github.com/opensearch-project/cross-cluster-replication/pull/1665))


### OpenSearch Custom Codecs


* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#333](https://github.com/opensearch-project/custom-codecs/pull/333))


### OpenSearch Dashboards Investigation


* Improve investigation creation UX and optimize LLM response message ([#365](https://github.com/opensearch-project/dashboards-investigation/pull/365))
* Restrict visualization summary to JPEG format with image size limitation ([#358](https://github.com/opensearch-project/dashboards-investigation/pull/358))


### OpenSearch Dashboards Maps


* Use getIsIconSideNavEnabled API for navigation registration gating ([#814](https://github.com/opensearch-project/dashboards-maps/pull/814))


### OpenSearch Dashboards Observability


* Add time range selector to the Alerts page for filtering alerts by arbitrary time window ([#2675](https://github.com/opensearch-project/dashboards-observability/pull/2675))
* Refactor Alerts UI with renamed navigation, collapsible filter panel, and improved layout ([#2677](https://github.com/opensearch-project/dashboards-observability/pull/2677))
* Add icon-based side navigation support with Trace Analytics and APM categories ([#2655](https://github.com/opensearch-project/dashboards-observability/pull/2655))


### OpenSearch Flow Framework


* Validate name and description fields in ML Commons steps during workflow parsing using ML Commons validation methods ([#1368](https://github.com/opensearch-project/flow-framework/pull/1368))
* Set `provisioned_by` field on ML resources to enable adoption metrics attribution ([#1388](https://github.com/opensearch-project/flow-framework/pull/1388))


### OpenSearch ML Commons


* Add private IP security controls and ReDoS protection for ML connectors ([#4818](https://github.com/opensearch-project/ml-commons/pull/4818))
* Add structured output (constrained decoding) support for agentic memory fact extraction ([#4824](https://github.com/opensearch-project/ml-commons/pull/4824))
* Strengthen enforcement of `trusted_connector_endpoints_regex` across all outbound connector request paths ([#4826](https://github.com/opensearch-project/ml-commons/pull/4826))
* Simplify USER\_PREFERENCE extraction prompt to produce plain sentences, fixing silent JSON parse failures with smaller LLMs ([#4798](https://github.com/opensearch-project/ml-commons/pull/4798))


### OpenSearch Neural Search


* Fix batch semantic highlighting on inner\_hits fields by improving the batch processor and adding a request-level opt-in ([#1858](https://github.com/opensearch-project/neural-search/pull/1858))
* Propagate setMinCompetitiveScore to sub-query scorers in HybridBulkScorer to reduce collected documents and improve response time ([#1831](https://github.com/opensearch-project/neural-search/pull/1831))


### OpenSearch Security


* Make `opensearch_security.multitenancy.tenants.preferred` configurable dynamically via security config API ([#5986](https://github.com/opensearch-project/security/pull/5986))
* Add salt generation to demo security configuration ([#6022](https://github.com/opensearch-project/security/pull/6022))
* Facilitate FIPS-compliant keystore resolution in test infrastructure ([#6059](https://github.com/opensearch-project/security/pull/6059))
* Support Jackson 3.x release line ([#6078](https://github.com/opensearch-project/security/pull/6078))
* Ensure Netty4Http3ServerTransport uses configured HeaderVerifier and Decompressor instances ([#6108](https://github.com/opensearch-project/security/pull/6108))
* Validate password hashing algorithm for FIPS compliance ([#6126](https://github.com/opensearch-project/security/pull/6126))


### OpenSearch Security Dashboards Plugin


* Add support for URL parameter `?auto_login=false` to force display of login screen, with new `opensearch_security.auth.default_redirect_auth_type` setting ([#2384](https://github.com/opensearch-project/security-dashboards-plugin/pull/2384))
* Use `preferred_tenants` from DashboardInfo API when resolving tenant, enabling dynamic configuration without restart ([#2391](https://github.com/opensearch-project/security-dashboards-plugin/pull/2391))


### OpenSearch k-NN


* Add bulk scoring logic in Memory Optimized Search when K exceeds the number of docs in a segment for improved SIMD/vectorization performance ([#3285](https://github.com/opensearch-project/k-NN/pull/3285))
* Use KNN1040ScalarQuantizedVectorsFormat for Faiss SQ flat format to enable I/O prefetch during exact search rescoring ([#3302](https://github.com/opensearch-project/k-NN/pull/3302))
* Add support for binary and byte field support in doc\_values [#3340](https://github.com/opensearch-project/k-NN/pull/3340)


### SQL


* Add query-type whitelist to block non-query statements (DML/DDL) in unified SQL execution path ([#5330](https://github.com/opensearch-project/sql/pull/5330))
* Add time conversion functions (`ctime`, `mktime`, `mstime`, `dur2sec`) and `timeformat` parameter for the PPL convert command ([#5210](https://github.com/opensearch-project/sql/pull/5210))
* Add `tests.analytics.parquet_indices` toggle for analytics-engine integration test coverage ([#5436](https://github.com/opensearch-project/sql/pull/5436))
* Define unified SQL language spec with composable extensions for OpenSearch SQL syntax ([#5360](https://github.com/opensearch-project/sql/pull/5360))
* Register `LENGTH`, `REGEXP_REPLACE`, `DATE_TRUNC` in unified function spec for ClickBench query support ([#5419](https://github.com/opensearch-project/sql/pull/5419))
* Register missing SQL V2 relevance functions and aliases in Calcite function table ([#5440](https://github.com/opensearch-project/sql/pull/5440))
* Route unified SQL path through V2 ANTLR parser with `CalciteRelNodeVisitor` ([#5438](https://github.com/opensearch-project/sql/pull/5438))
* Resolve SQL unified query gaps for SELECT clauses, LIMIT/OFFSET, derived tables, and window functions ([#5450](https://github.com/opensearch-project/sql/pull/5450))
* Extend V2 SQL parser with `IN`/`EXISTS` subquery support for unified query path ([#5448](https://github.com/opensearch-project/sql/pull/5448))
* Extend V2 SQL parser with `JOIN` (INNER/LEFT/RIGHT/CROSS) for unified query path ([#5446](https://github.com/opensearch-project/sql/pull/5446))
* Add UDT support for IP and Binary types in analytics-engine response schema ([#5463](https://github.com/opensearch-project/sql/pull/5463))
* Add coercion rules and placeholder UDF to handle VARBINARY-to-VARCHAR comparisons for IP/binary fields ([#5443](https://github.com/opensearch-project/sql/pull/5443))
* Close gaps from top/rare analytics-engine wiring by forwarding `PPL_SYNTAX_LEGACY_PREFERRED` and adding stable tie-break ([#5433](https://github.com/opensearch-project/sql/pull/5433))
* Use `leastRestrictive` for `mvappend` element-type widening to fix analytics-engine Substrait serialization ([#5424](https://github.com/opensearch-project/sql/pull/5424))
* Lower `isempty`/`isblank` to `CHAR_LENGTH = 0` instead of multiset `IS_EMPTY` for analytics-engine compatibility ([#5439](https://github.com/opensearch-project/sql/pull/5439))
* Add `IS [NOT] NULL` predicate syntax support in PPL ([#5278](https://github.com/opensearch-project/sql/pull/5278))
* Allow `limit=N` keyword syntax for `head` and `top` commands ([#4249](https://github.com/opensearch-project/sql/pull/4249))
* Register `DISTINCT_COUNT_APPROX` logical marker in PPLFuncImpTable for unified/analytics-engine paths ([#5466](https://github.com/opensearch-project/sql/pull/5466))
* Fix singleton stack-corruption NPE in `DatetimeUdtNormalizeRule` by instantiating rules per `plan()` call ([#5458](https://github.com/opensearch-project/sql/pull/5458))
* Improve exception handling in `UnifiedQueryPlanner` with proper error classification and logging ([#5465](https://github.com/opensearch-project/sql/pull/5465))
* Create parquet-backed test indices for `spath` command analytics-engine route ([#5441](https://github.com/opensearch-project/sql/pull/5441))
* Improve error messages for invalid index mapping by formatting index patterns and including underlying error details ([#5370](https://github.com/opensearch-project/sql/pull/5370))
* Initial implementation of report-builder interface for richer error context in responses ([#5266](https://github.com/opensearch-project/sql/pull/5266))
* Validate materialized view subqueries against SQL grammar deny list ([#5485](https://github.com/opensearch-project/sql/pull/5485))


## BUG FIXES


### OpenSearch Alerting


* Set number\_of\_shards to 1 for plugin-created system indices ([#2091](https://github.com/opensearch-project/alerting/pull/2091))
* Keep alerting builds stable after PPL alerting common-utils changes ([#2111](https://github.com/opensearch-project/alerting/pull/2111))
* Gate system index lifecycle operations when multi-tenancy is enabled ([#2124](https://github.com/opensearch-project/alerting/pull/2124))
* Stash and re-inject thread context before executing monitor in poller ([#2132](https://github.com/opensearch-project/alerting/pull/2132))
* Handle typed\_keys prefix and remote target in bucket-level monitors ([#2146](https://github.com/opensearch-project/alerting/pull/2146))
* Add reinjectHeaders for PPL monitor execution path to fix header propagation in multi-tenant mode ([#2151](https://github.com/opensearch-project/alerting/pull/2151))
* Fix PPL monitor execution to skip base query when only custom triggers are present ([#2155](https://github.com/opensearch-project/alerting/pull/2155))


### OpenSearch Alerting Dashboards Plugin


* Fix monitor schedule edit workflow when ui\_metadata is not present ([#1421](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1421))


### OpenSearch Common Utils


* Change ScheduleJobPayload.jobStartTime from Instant to String to support both placeholders and timestamps ([#944](https://github.com/opensearch-project/common-utils/pull/944))


### OpenSearch Cross Cluster Replication


* Fix `isRemoteEnabledOrMigrating` to correctly detect remote-store clusters, resolving ~5 minute replication delays caused by stale checkpoint reads ([#1688](https://github.com/opensearch-project/cross-cluster-replication/pull/1688))
* Skip syncing `number_of_replicas` when follower has `auto_expand_replicas` active to prevent perpetual yellow cluster state ([#1664](https://github.com/opensearch-project/cross-cluster-replication/pull/1664))
* Fix security plugin compatibility for 3.7.0 by implementing `TransportIndicesResolvingAction` on metadata update action ([#1667](https://github.com/opensearch-project/cross-cluster-replication/pull/1667))


### OpenSearch Dashboards Assistant


* Bump dependency versions to resolve conflicts with OpenSearch-Dashboards ([#684](https://github.com/opensearch-project/dashboards-assistant/pull/684))
* Migrate plugin to TypeScript 6.0.2 compatibility ([#678](https://github.com/opensearch-project/dashboards-assistant/pull/678))


### OpenSearch Dashboards Flow Framework


* Fix flaky tests by replacing singleton store with mock store ([#878](https://github.com/opensearch-project/dashboards-flow-framework/pull/878))


### OpenSearch Dashboards Investigation


* Fix typo in initial goal ([#362](https://github.com/opensearch-project/dashboards-investigation/pull/362))
* Resolve stale closure preventing investigation title update ([#359](https://github.com/opensearch-project/dashboards-investigation/pull/359))
* Migrate plugin to TypeScript 6.0.2 compatibility ([#367](https://github.com/opensearch-project/dashboards-investigation/pull/367))
* Skip log pattern paragraph for clusters below 2.19.0 ([#371](https://github.com/opensearch-project/dashboards-investigation/pull/371))
* Bump dompurify and eslint versions to resolve dependency conflicts with OpenSearch-Dashboards ([#377](https://github.com/opensearch-project/dashboards-investigation/pull/377))


### OpenSearch Dashboards Observability


* Exclude text-only fields from default pattern field selection in Logs Explorer to prevent aggregation errors ([#2661](https://github.com/opensearch-project/dashboards-observability/pull/2661))
* Make SPAN() case-insensitive in visualization rendering to fix blank charts with uppercase usage ([#2659](https://github.com/opensearch-project/dashboards-observability/pull/2659))
* Register Alert Manager in side nav when enabled by threading the flag through nav registration functions ([#2668](https://github.com/opensearch-project/dashboards-observability/pull/2668))
* Fix ReferenceError caused by missing lodash import in Logs Explorer direct events hook ([#2660](https://github.com/opensearch-project/dashboards-observability/pull/2660))


### OpenSearch Dashboards Query Workbench


* Migrate plugin to TypeScript 6.0.2 compatibility by removing conflicting dependencies and regenerating yarn.lock ([#549](https://github.com/opensearch-project/dashboards-query-workbench/pull/549))


### OpenSearch Dashboards Reporting


* Migrate plugin to TypeScript 6.0.2 compatibility ([#744](https://github.com/opensearch-project/dashboards-reporting/pull/744))


### OpenSearch Flow Framework


* Handle ResourceAlreadyExistsException in FlowFrameworkIndicesHandler to fix race condition on multi-node clusters ([#1378](https://github.com/opensearch-project/flow-framework/pull/1378))


### OpenSearch Index Management


* Fix `_refresh_search_analyzers` failing with 403 on indices with METADATA\_WRITE block such as CCR follower indices ([#1635](https://github.com/opensearch-project/index-management/pull/1635))
* Don't fail transition condition verification when an empty conditions set is provided ([#1626](https://github.com/opensearch-project/index-management/pull/1626))


### OpenSearch Index Management Dashboards Plugin


* Fix CVE-2026-33671 and CVE-2026-33532 by updating to proper versions ([#1433](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1433))


### OpenSearch ML Commons


* Fix Jackson exception handling due to 3.x release line migration ([#4784](https://github.com/opensearch-project/ml-commons/pull/4784))
* Fix flaky `RestMLInferenceSearchResponseProcessorIT` connection pool timeout by optimizing test setup ([#4781](https://github.com/opensearch-project/ml-commons/pull/4781))
* Fix tool output JSON escape issue when replacing placeholders in connector request bodies ([#4794](https://github.com/opensearch-project/ml-commons/pull/4794))
* Propagate stream errors properly to callers instead of swallowing them ([#4792](https://github.com/opensearch-project/ml-commons/pull/4792))
* Fix `model_parameters` being silently ignored in inferenceConfig and incorrect SourceType error message in V2 agents ([#4833](https://github.com/opensearch-project/ml-commons/pull/4833))


### OpenSearch ML Commons Dashboards


* Migrate plugin to TypeScript 6.0.2 compatibility ([#482](https://github.com/opensearch-project/ml-commons-dashboards/pull/482))
* Fix data source picker to filter out unsupported engine types ([#488](https://github.com/opensearch-project/ml-commons-dashboards/pull/488))


### OpenSearch Neural Search


* Fix flaky integration test failure caused by ML memory circuit breaker during model deployment by adding deploy retry logic ([#1824](https://github.com/opensearch-project/neural-search/pull/1824))


### OpenSearch Query Insights Dashboards


* Fix filter bar not filling screen width when zooming in and out ([#493](https://github.com/opensearch-project/query-insights-dashboards/pull/493))
* Fix catch block variable references in index.ts where actively used error variables were incorrectly prefixed with underscore ([#515](https://github.com/opensearch-project/query-insights-dashboards/pull/515))


### OpenSearch Search Relevance


* Fixed QuerySet creation failing when query or answer text contains `#` or `:` characters ([#414](https://github.com/opensearch-project/search-relevance/pull/414))
* Fix race condition in index mapping migration that crashes nodes during rolling upgrades ([#443](https://github.com/opensearch-project/search-relevance/pull/443))
* Fix typo in log message: "occured" → "occurred" ([#461](https://github.com/opensearch-project/search-relevance/pull/461))
* Fix typo in log message: "occured" → "occurred" ([#462](https://github.com/opensearch-project/search-relevance/pull/462))


### OpenSearch Security


* Fix JWT attribute parsing of lists in AbstractHTTPJwtAuthenticator when using `jwks_uri` ([#6058](https://github.com/opensearch-project/security/pull/6058))
* Update RequestContentValidator to only validate fields from request payload, not pre-existing values in security index ([#6061](https://github.com/opensearch-project/security/pull/6061))
* Fix NPE in LDAPAuthorizationBackend when rolesearch is disabled ([#6112](https://github.com/opensearch-project/security/pull/6112))
* Preserve response headers across context restore in SecurityInterceptor ([#6123](https://github.com/opensearch-project/security/pull/6123))
* Fix SSL hot-reload to rebuild trust store instead of validating all CA dates ([#6136](https://github.com/opensearch-project/security/pull/6136))
* Implement skipsDeserialization() in RestoringTransportResponseHandler to fix Arrow Flight stream transport responses ([#6154](https://github.com/opensearch-project/security/pull/6154))


### OpenSearch Security Analytics Dashboards Plugin


* Migrate plugin to TypeScript 6.0.2 compatibility by removing conflicting dependencies ([#1525](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1525))


### OpenSearch Security Dashboards Plugin


* Allow readonly users to access opensearch\_dashboards\_overview to fix "Application not found" error ([#2415](https://github.com/opensearch-project/security-dashboards-plugin/pull/2415))
* Add issues write permission to untriaged label workflow to fix 403 error ([#2427](https://github.com/opensearch-project/security-dashboards-plugin/pull/2427))
* Fix CVE-2026-45736 by bumping ws to >=8.20.1 to address uninitialized memory disclosure vulnerability ([#2428](https://github.com/opensearch-project/security-dashboards-plugin/pull/2428))
* Fix CVE-2026-41907 by bumping uuid to >=14.0.0 to address out-of-range buffer write vulnerability ([#2431](https://github.com/opensearch-project/security-dashboards-plugin/pull/2431))


### OpenSearch User Behavior Insights


* Fix thread safety issue with date formatter and update for OpenSearch 3.7 compatibility ([#179](https://github.com/opensearch-project/user-behavior-insights/pull/179))


### SQL


* Fix `COALESCE(null, int)` returning string type by using `SqlTypeName.NULL` for substituted literals ([#5382](https://github.com/opensearch-project/sql/pull/5382))
* Fix `NOT IN` including null/missing rows by adding exists filter for three-valued logic compliance ([#5337](https://github.com/opensearch-project/sql/pull/5337))
* Fix `NOT LIKE` incorrectly including rows with null/missing fields ([#5338](https://github.com/opensearch-project/sql/pull/5338))
* Fix PPL mixed text/keyword field type across wildcard indices causing silently dropped documents ([#5358](https://github.com/opensearch-project/sql/pull/5358))
* Fix `bin`/`chart` NPE with null values by declaring nullable return type and adding nullsLast to sorts ([#5334](https://github.com/opensearch-project/sql/pull/5334))
* Fix chained `streamstats` with window causing NPE by replacing correlate-based plan with self-join ([#5359](https://github.com/opensearch-project/sql/pull/5359))
* Fix `eval` overwriting MAP root field when assigning multiple dotted-path names ([#5351](https://github.com/opensearch-project/sql/pull/5351))
* Fix `json_set` crash and `json_delete` no-op with `$.key` paths by preventing double-prefixing ([#5339](https://github.com/opensearch-project/sql/pull/5339))
* Fix multiple `appendpipe` error while revisiting parent AST by using relBuilder stack directly ([#5322](https://github.com/opensearch-project/sql/pull/5322))
* Fix `rename` with wildcard applying on hidden/metadata fields ([#5350](https://github.com/opensearch-project/sql/pull/5350))
* Fix sort order not preserved through `dedup` in Calcite engine ([#5353](https://github.com/opensearch-project/sql/pull/5353))
* Fix `transpose` command name collision with 'value' field ([#5352](https://github.com/opensearch-project/sql/pull/5352))
* Scope SQL cursor continuation to original query indices under Fine-Grained Access Control ([#5399](https://github.com/opensearch-project/sql/pull/5399))
* Normalize datetime types for unified query API with UDT rewrite and output cast rules ([#5408](https://github.com/opensearch-project/sql/pull/5408))
* Fix SQL query routing to analytics engine after V2 parser change ([#5456](https://github.com/opensearch-project/sql/pull/5456))
* Fix `SemanticCheckException` not thrown for invalid field in nested function ([#5239](https://github.com/opensearch-project/sql/pull/5239))
* Handle Prometheus `/api/v1/metadata` responses without `data` field for Cortex-backed datasources ([#5437](https://github.com/opensearch-project/sql/pull/5437))
* Use `ObjectInputFilter` allowlist for deserialization in cursor and script pushdown serializers ([#5469](https://github.com/opensearch-project/sql/pull/5469))


## INFRASTRUCTURE


### OpenSearch Alerting


* Add issues write permission to untriaged label workflow ([#2148](https://github.com/opensearch-project/alerting/pull/2148))


### OpenSearch Alerting Dashboards Plugin


* Add issues write permission to untriaged label workflow ([#1454](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1454))
* Migrate plugin to TypeScript 6.0.2 compatibility ([#1417](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1417))


### OpenSearch Anomaly Detection


* Add issues write permission to untriaged label workflow to fix 403 error when applying labels ([#1720](https://github.com/opensearch-project/anomaly-detection/pull/1720))
* Remove redundant Gradle tasks and fix inconsistent fail-fast settings across CI workflows ([#1693](https://github.com/opensearch-project/anomaly-detection/pull/1693))
* Support Jackson 3.x release line ([#1705](https://github.com/opensearch-project/anomaly-detection/pull/1705))


### OpenSearch Anomaly Detection Dashboards Plugin


* Add issues write permission to untriaged label workflow to fix 403 errors ([#1200](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1200))
* Increase unit test coverage for utility functions with 95 new tests across forecast and anomaly result utilities ([#1172](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1172))
* Optimize CI workflows with yarn caching, action version bumps, bug fixes, and dead code removal ([#1163](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1163))
* Match jest-canvas-mock version with core ([#1202](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1202))


### OpenSearch Asynchronous Search


* Add issues write permission to untriaged label workflow to fix 403 error when applying labels ([#833](https://github.com/opensearch-project/asynchronous-search/pull/833))
* Upgrade Gradle wrapper to 9.4.1 to meet GlobalBuildInfoPlugin requirements ([#835](https://github.com/opensearch-project/asynchronous-search/pull/835))


### OpenSearch Common Utils


* Add Maven cache mirror before mavenCentral to reduce 429 throttling errors in CI builds ([#957](https://github.com/opensearch-project/common-utils/pull/957))
* Add issues write permission to untriaged label workflow ([#959](https://github.com/opensearch-project/common-utils/pull/959))
* Pin GitHub Actions to commit SHAs for supply chain security ([#961](https://github.com/opensearch-project/common-utils/pull/961))
* Pin actions/github-script to exact commit SHA ([#960](https://github.com/opensearch-project/common-utils/pull/960))


### OpenSearch Custom Codecs


* Add issues write permission to untriaged label workflow to fix 403 error ([#338](https://github.com/opensearch-project/custom-codecs/pull/338))
* Pin all GitHub Actions to exact commit SHAs to prevent supply chain attacks ([#340](https://github.com/opensearch-project/custom-codecs/pull/340))
* Pin actions/github-script to exact commit SHA for immutable action references ([#339](https://github.com/opensearch-project/custom-codecs/pull/339))


### OpenSearch Dashboards Assistant


* Add GitHub workflow for labelling untriaged issues ([#682](https://github.com/opensearch-project/dashboards-assistant/pull/682))


### OpenSearch Dashboards Flow Framework


* Add issues write permission to untriaged label workflow ([#888](https://github.com/opensearch-project/dashboards-flow-framework/pull/888))
* Add unit tests for utility functions to increase test coverage ([#862](https://github.com/opensearch-project/dashboards-flow-framework/pull/862))
* Add yarn cache to setup-node step in CI workflow to reduce build times ([#887](https://github.com/opensearch-project/dashboards-flow-framework/pull/887))
* Clean up CI workflows: update actions, fix yarn version bug, and remove dead code ([#861](https://github.com/opensearch-project/dashboards-flow-framework/pull/861))


### OpenSearch Dashboards Investigation


* Add issues write permission to untriaged label workflow ([#373](https://github.com/opensearch-project/dashboards-investigation/pull/373))
* Pin actions/github-script to exact commit SHA for security hardening ([#374](https://github.com/opensearch-project/dashboards-investigation/pull/374))
* Fix stale backport cleanup GitHub Action by replacing with native implementation ([#346](https://github.com/opensearch-project/dashboards-investigation/pull/346))


### OpenSearch Dashboards Notifications


* Add issues write permission to untriaged label workflow to fix 403 error ([#452](https://github.com/opensearch-project/dashboards-notifications/pull/452))
* Update bug report template with instructions to not include sensitive information ([#450](https://github.com/opensearch-project/dashboards-notifications/pull/450))


### OpenSearch Dashboards Observability


* Add issues write permission to untriaged label workflow to fix 403 errors ([#2685](https://github.com/opensearch-project/dashboards-observability/pull/2685))
* Pin GitHub Actions to commit SHAs to prevent supply chain attacks ([#2690](https://github.com/opensearch-project/dashboards-observability/pull/2690))
* Stabilize Application Analytics Cypress and FTR tests with improved element targeting and error handling ([#2667](https://github.com/opensearch-project/dashboards-observability/pull/2667))
* Fix Traces Cypress tests by replacing fragile tick assertions and adding resilient node click handling ([#2671](https://github.com/opensearch-project/dashboards-observability/pull/2671))
* Fix link checker by updating Hapi Wreck URL ([#2664](https://github.com/opensearch-project/dashboards-observability/pull/2664))


### OpenSearch Dashboards Query Workbench


* Add issues write permission to untriaged label workflow to fix 403 error when applying labels ([#557](https://github.com/opensearch-project/dashboards-query-workbench/pull/557))
* Pin GitHub Actions to commit SHAs to prevent supply chain attacks from mutable tag references ([#558](https://github.com/opensearch-project/dashboards-query-workbench/pull/558))


### OpenSearch Dashboards Reporting


* Add issues write permission to untriaged label workflow ([#751](https://github.com/opensearch-project/dashboards-reporting/pull/751))


### OpenSearch Dashboards Search Relevance


* Fix Linux workflow Node.js setup for OpenSearch Dashboards compatibility ([#839](https://github.com/opensearch-project/dashboards-search-relevance/pull/839))


### OpenSearch Flow Framework


* Add Gradle cache to setup-java steps in CI workflows to reduce build times ([#1372](https://github.com/opensearch-project/flow-framework/pull/1372))


### OpenSearch Index Management


* Add issues write permission to untriaged label workflow to fix 403 error when applying labels ([#1645](https://github.com/opensearch-project/index-management/pull/1645))
* Fix flaky `RestGetRollupActionIT` and `RestGetTransformActionIT` by resetting cluster settings and retrying through transient shard recovery ([#1644](https://github.com/opensearch-project/index-management/pull/1644))
* Pin GitHub Actions to commit SHAs to prevent supply chain attacks ([#1648](https://github.com/opensearch-project/index-management/pull/1648))
* Pin `actions/github-script` to exact commit SHA for immutable CI references ([#1647](https://github.com/opensearch-project/index-management/pull/1647))
* Fix flaky `test multi-tier rollup with cardinality` by using `Locale.ROOT` for timestamp formatting and adding bulk response error checking ([#1574](https://github.com/opensearch-project/index-management/pull/1574))
* Fix flaky multi-node ISM tests by waiting for cluster GREEN health before index cleanup to prevent node lock corruption ([#1575](https://github.com/opensearch-project/index-management/pull/1575))


### OpenSearch Job Scheduler


* Add Maven cache mirror before mavenCentral to reduce HTTP 429 throttling errors in CI builds ([#918](https://github.com/opensearch-project/job-scheduler/pull/918))
* Add issues write permission to untriaged label workflow to fix 403 errors ([#919](https://github.com/opensearch-project/job-scheduler/pull/919))
* Fix Codecov configuration by removing duplicate sections and validating .codecov.yml ([#898](https://github.com/opensearch-project/job-scheduler/pull/898))
* Pin GitHub Actions to commit SHAs to prevent supply chain attacks ([#921](https://github.com/opensearch-project/job-scheduler/pull/921))
* Pin actions/github-script to exact commit SHA for improved security ([#920](https://github.com/opensearch-project/job-scheduler/pull/920))


### OpenSearch ML Commons


* Add issues write permission to untriaged label workflow ([#4827](https://github.com/opensearch-project/ml-commons/pull/4827))
* Update Gradle to 9.4.1 and Jacoco to 0.8.14 to fix CI build failures ([#4811](https://github.com/opensearch-project/ml-commons/pull/4811))
* Add `akolarkunnu` as maintainer ([#4788](https://github.com/opensearch-project/ml-commons/pull/4788))
* Update GitHub username reference from `rithin-pullela-aws` to `rithinpullela` ([#4825](https://github.com/opensearch-project/ml-commons/pull/4825))


### OpenSearch Neural Search


* Add Maven cache mirror before mavenCentral to reduce HTTP 429 Too Many Requests throttling in CI builds ([#1856](https://github.com/opensearch-project/neural-search/pull/1856))
* Add gRPC integration tests for hybrid query with normalization pipeline, sort, and collapse ([#1827](https://github.com/opensearch-project/neural-search/pull/1827))
* Pin actions/github-script to exact commit SHA for improved supply chain security ([#1860](https://github.com/opensearch-project/neural-search/pull/1860))


### OpenSearch Notifications


* Add issues write permission to untriaged label workflow to fix 403 error ([#1230](https://github.com/opensearch-project/notifications/pull/1230))


### OpenSearch Observability


* Add issues write permission to untriaged label workflow to fix label application errors ([#1995](https://github.com/opensearch-project/observability/pull/1995))


### OpenSearch Query Insights


* Add issues write permission to untriaged label workflow to fix 403 errors ([#612](https://github.com/opensearch-project/query-insights/pull/612))
* Pin GitHub Actions to commit SHAs to prevent supply chain attacks ([#613](https://github.com/opensearch-project/query-insights/pull/613))
* Upgrade Gradle to 9.4.1 and fix health stats test compatibility for OpenSearch 3.7 ([#609](https://github.com/opensearch-project/query-insights/pull/609))


### OpenSearch Query Insights Dashboards


* Add issues write permission to untriaged label workflow to fix 403 error when applying labels ([#521](https://github.com/opensearch-project/query-insights-dashboards/pull/521))
* Pin GitHub Actions to commit SHAs to prevent supply chain attacks from mutable tag references ([#524](https://github.com/opensearch-project/query-insights-dashboards/pull/524))


### OpenSearch Reporting


* Add issues write permission to untriaged label workflow to fix label application errors ([#1186](https://github.com/opensearch-project/reporting/pull/1186))


### OpenSearch Search Relevance


* Pin actions/github-script to exact commit SHA for reproducible builds ([#467](https://github.com/opensearch-project/search-relevance/pull/467))
* Bump 1password/load-secrets-action from 3 to 4 ([#431](https://github.com/opensearch-project/search-relevance/pull/431))
* Bump actions/github-script from 8 to 9 ([#445](https://github.com/opensearch-project/search-relevance/pull/445))
* Bump codecov/codecov-action from 5 to 6 ([#432](https://github.com/opensearch-project/search-relevance/pull/432))


### OpenSearch Security


* Fix automatic-merges to ensure GitHub workflows run automatically after bot-managed merges ([#6101](https://github.com/opensearch-project/security/pull/6101))
* Wait 45s before health check to resolve Windows plugin install flakiness ([#6125](https://github.com/opensearch-project/security/pull/6125))
* Improve cluster cleanup for in-memory integration test nodes to prevent thread leaks and port conflicts ([#6127](https://github.com/opensearch-project/security/pull/6127))
* Force netty resolution to fix version conflict issues ([#6133](https://github.com/opensearch-project/security/pull/6133))
* Add issues write permission to untriaged label workflow ([#6153](https://github.com/opensearch-project/security/pull/6153))
* Pin actions/github-script to exact commit SHA ([#6157](https://github.com/opensearch-project/security/pull/6157))
* Pin GitHub Actions to commit SHAs for supply chain security ([#6159](https://github.com/opensearch-project/security/pull/6159))


### OpenSearch Security Analytics Dashboards Plugin


* Add issues write permission to untriaged label workflow to fix 403 error ([#1529](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1529))


### OpenSearch Security Dashboards Plugin


* Pin actions/github-script to exact commit SHA for supply chain security ([#2429](https://github.com/opensearch-project/security-dashboards-plugin/pull/2429))
* Pin GitHub Actions to commit SHAs to prevent potential supply chain attacks ([#2430](https://github.com/opensearch-project/security-dashboards-plugin/pull/2430))
* Verify Cypress integration tests with Cypress 13 after upgrade in FTR repo ([#2422](https://github.com/opensearch-project/security-dashboards-plugin/pull/2422))


### OpenSearch Skills


* Add issues write permission to untriaged label workflow to fix 403 errors ([#739](https://github.com/opensearch-project/skills/pull/739))
* Pin actions/github-script to exact commit SHA for improved supply chain security ([#740](https://github.com/opensearch-project/skills/pull/740))


### OpenSearch k-NN


* Add issues write permission to untriaged label workflow to fix 403 errors ([#3332](https://github.com/opensearch-project/k-NN/pull/3332))


### SQL


* Add integration tests for analytics engine index-level authorization ([#5462](https://github.com/opensearch-project/sql/pull/5462))
* Add issues write permission to untriaged label workflow ([#5457](https://github.com/opensearch-project/sql/pull/5457))
* Add tiebreaker to stats sort-on-measure IT queries for deterministic results across engines ([#5435](https://github.com/opensearch-project/sql/pull/5435))
* Land analytics-engine PPL integration into main with query routing, explain, profiling, and async execution ([#5430](https://github.com/opensearch-project/sql/pull/5430))
* Fix distribution build by pinning `analytics-api` dependency to `3.7.0-SNAPSHOT` ([#5455](https://github.com/opensearch-project/sql/pull/5455))
* Pin GitHub Actions to commit SHAs for supply chain security ([#5464](https://github.com/opensearch-project/sql/pull/5464))
* Bump Gradle wrapper to 9.4.1 and workaround `@Ignore` test failure ([#5414](https://github.com/opensearch-project/sql/pull/5414))
* Fix link checker CI failure by excluding LinkedIn URLs ([#5461](https://github.com/opensearch-project/sql/pull/5461))
* Integration test cases for field-level security ([#5008](https://github.com/opensearch-project/sql/pull/5008))
* Skip `vectorSearch()` missing-plugin integration test when the k-NN plugin is installed, fixing the distribution integ-test run since distributions bundle k-NN ([#5492](https://github.com/opensearch-project/sql/pull/5492))


## DOCUMENTATION


### OpenSearch Alerting


* Update bug report template with instructions to not include sensitive information ([#2119](https://github.com/opensearch-project/alerting/pull/2119))


### OpenSearch Alerting Dashboards Plugin


* Add OpenAPI specification for Alerting Dashboards plugin APIs ([#1419](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1419))
* Add 4xx error responses to OpenAPI alerting specification ([#1420](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1420))
* Update bug report template with instructions to not include sensitive information ([#1422](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1422))


### OpenSearch Dashboards Notifications


* Add OpenAPI specification for Notification APIs covering configs, features, events, and test endpoints ([#448](https://github.com/opensearch-project/dashboards-notifications/pull/448))
* Add 4xx error responses to OpenAPI specification for notification APIs ([#449](https://github.com/opensearch-project/dashboards-notifications/pull/449))


### OpenSearch Index Management


* Update affiliation to Apple for Shivansh Arora ([#1627](https://github.com/opensearch-project/index-management/pull/1627))


### OpenSearch ML Commons


* Add Yandex Cloud AI Studio standard embedding connector blueprint ([#4810](https://github.com/opensearch-project/ml-commons/pull/4810))
* Add Yandex Cloud AI Studio embeddings connector blueprint ([#4469](https://github.com/opensearch-project/ml-commons/pull/4469))


### OpenSearch Notifications


* Update bug report template with instructions to not include sensitive information ([#1223](https://github.com/opensearch-project/notifications/pull/1223))


### OpenSearch Security


* Add BCFKS keystore generation utilities and documentation ([#6087](https://github.com/opensearch-project/security/pull/6087))
* Introduce an AGENTS.MD file for agentic development guidance ([#6156](https://github.com/opensearch-project/security/pull/6156))


### OpenSearch Security Analytics Dashboards Plugin


* Update bug report template with instructions to not include sensitive information ([#1526](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1526))


### OpenSearch Skills


* Add reference to opensearch-agent-skills in README ([#724](https://github.com/opensearch-project/skills/pull/724))


### SQL


* Update SQL docs for querying multiple indices with backtick-enclosed list syntax ([#5340](https://github.com/opensearch-project/sql/pull/5340))
* Update PPL command doc examples to use OpenTelemetry sample data ([#5303](https://github.com/opensearch-project/sql/pull/5303))


## MAINTENANCE


### OpenSearch Alerting


* Baselined maintainers list ([#2092](https://github.com/opensearch-project/alerting/pull/2092))
* Bumped gradle version to 9.4.1 ([#2122](https://github.com/opensearch-project/alerting/pull/2122))


### OpenSearch Alerting Dashboards Plugin


* Baseline maintainers list ([#1411](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1411))
* Resolve CVE-2026-27903, CVE-2026-27904, CVE-2026-33671, CVE-2026-33750, and CVE-2026-33532 ([#1425](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1425))


### OpenSearch Anomaly Detection Dashboards Plugin


* Bump axios from 1.13.5 to 1.15.0 ([#1180](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1180))
* Bump follow-redirects from 1.15.11 to 1.16.0 ([#1183](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1183))
* Bump picomatch and brace-expansion to resolve CVEs (CVE-2026-33750, CVE-2026-33671, CVE-2026-33672) ([#1161](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1161))
* Migrate plugin to TypeScript 6.0.2 compatibility ([#1186](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1186))


### OpenSearch Common Utils


* Baselined maintainers list ([#936](https://github.com/opensearch-project/common-utils/pull/936))
* Cleanup SafeSerializationUtils to remove unused Guava classes and add deserialization depth limit ([#958](https://github.com/opensearch-project/common-utils/pull/958))
* Remove unused SchedulePayloadBuilder superseded by ScheduleJobPayload ([#945](https://github.com/opensearch-project/common-utils/pull/945))


### OpenSearch Dashboards Investigation


* Bump fast-uri from 3.1.0 to 3.1.2 to address security vulnerabilities ([#370](https://github.com/opensearch-project/dashboards-investigation/pull/370))


### OpenSearch Dashboards Maps


* Fix linux build workflow ([#818](https://github.com/opensearch-project/dashboards-maps/pull/818))


### OpenSearch Dashboards Notifications


* Baseline maintainers list ([#442](https://github.com/opensearch-project/dashboards-notifications/pull/442))


### OpenSearch Dashboards Observability


* Fix typo in application deletion error toast: "occured" → "occurred" ([#2674](https://github.com/opensearch-project/dashboards-observability/pull/2674))
* Bump uuid to 3.4.0 to resolve CVE-2026-41907 in transitive dependency ([#2679](https://github.com/opensearch-project/dashboards-observability/pull/2679))
* Improve Alerts empty state with primary Rules button and updated layout ([#2686](https://github.com/opensearch-project/dashboards-observability/pull/2686))
* Migrate plugin to TypeScript 6.0.2 compatibility by removing conflicting dependencies ([#2652](https://github.com/opensearch-project/dashboards-observability/pull/2652))
* Skip histogram and patterns sub-queries when PPL query contains stats to prevent invalid PPL errors ([#2695](https://github.com/opensearch-project/dashboards-observability/pull/2695))
* Fix link checker CI failure by adding unreachable URLs to ignore list ([#2646](https://github.com/opensearch-project/dashboards-observability/pull/2646))
* Fix broken release notes link by pointing to existing commit SHA ([#2688](https://github.com/opensearch-project/dashboards-observability/pull/2688))


### OpenSearch Dashboards Query Workbench


* Apply lint auto-fixes across the codebase ([#552](https://github.com/opensearch-project/dashboards-query-workbench/pull/552))
* Apply additional lints with fixes and suppressions for remaining lint warnings ([#553](https://github.com/opensearch-project/dashboards-query-workbench/pull/553))
* Bump flatted version to address CVE-2026-32141 and CVE-2026-33228 ([#538](https://github.com/opensearch-project/dashboards-query-workbench/pull/538))
* Update uuid resolution version and fix babel configuration ([#551](https://github.com/opensearch-project/dashboards-query-workbench/pull/551))


### OpenSearch Flow Framework


* Support Jackson 3.x release line ([#1376](https://github.com/opensearch-project/flow-framework/pull/1376))


### OpenSearch Index Management


* Bump index management to OpenSearch 3.7 and update Gradle wrapper to 9.4.1 ([#1640](https://github.com/opensearch-project/index-management/pull/1640))
* Bump `1password/load-secrets-action` from 3 to 4 ([#1611](https://github.com/opensearch-project/index-management/pull/1611))
* Bump `aws-actions/configure-aws-credentials` from 5 to 6 ([#1583](https://github.com/opensearch-project/index-management/pull/1583))
* Bump `ch.qos.logback:logback-core` from 1.5.26 to 1.5.32 ([#1599](https://github.com/opensearch-project/index-management/pull/1599))


### OpenSearch Job Scheduler


* Bump actions/github-script from 8 to 9 ([#908](https://github.com/opensearch-project/job-scheduler/pull/908))
* Bump gradle-wrapper from 9.4.1 to 9.5.0 ([#913](https://github.com/opensearch-project/job-scheduler/pull/913))


### OpenSearch ML Commons


* Support Jackson 3.x release line and update MCP SDK to 1.1.1 and json-schema-validation to 3.0.4 ([#4795](https://github.com/opensearch-project/ml-commons/pull/4795))


### OpenSearch Neural Search


* Upgrade Gradle wrapper to 9.4.1 ([#1849](https://github.com/opensearch-project/neural-search/pull/1849))
* + Unwrap LeafReader to fix compatibility issue with core PR 21318 that wrapped SparsePostingsEnum into ExitablePostingsEnum ([#1855](https://github.com/opensearch-project/neural-search/pull/1855))


### OpenSearch Notifications


* Baselined maintainers list ([#1163](https://github.com/opensearch-project/notifications/pull/1163))
* Support Jackson 3.x release line ([#1217](https://github.com/opensearch-project/notifications/pull/1217))
* Version bump to 3.7 with accompanying dependency changes ([#1222](https://github.com/opensearch-project/notifications/pull/1222))


### OpenSearch OpenSearch Remote Metadata Sdk


* Migrate core and ddb-client modules from Jackson 2.x to Jackson 3.x (`tools.jackson`) ([#358](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/358))
* Fix CVE-2025-67030 by bumping plexus-utils from 3.3.0 to 3.6.1 to address directory traversal vulnerability ([#371](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/371))
* Add Gradle dependency caching to setup-java steps in CI workflows to reduce build times ([#364](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/364))


### OpenSearch Performance Analyzer


* Fix CVE-2025-67030 by pinning org.codehaus.plexus:plexus-utils to 4.0.2 ([#942](https://github.com/opensearch-project/performance-analyzer/pull/942))
* Upgrade Gradle wrapper to 9.4.1 ([#944](https://github.com/opensearch-project/performance-analyzer/pull/944))


### OpenSearch Query Insights Dashboards


* Bump yaml to ^2.8.3 and serialize-javascript to 7.0.5 to address CVE-2026-33532 and CVE-2026-34043 ([#522](https://github.com/opensearch-project/query-insights-dashboards/pull/522))
* Remove caret range for echarts-for-react to prevent risk from compromised packages ([#519](https://github.com/opensearch-project/query-insights-dashboards/pull/519))
* Migrate plugin to TypeScript 6.0.2 compatibility by removing conflicting dependencies and regenerating yarn.lock ([#508](https://github.com/opensearch-project/query-insights-dashboards/pull/508))
* Prefix unused caught error variables with underscore to satisfy lint rules ([#509](https://github.com/opensearch-project/query-insights-dashboards/pull/509))


### OpenSearch Search Relevance


* Add support for Jackson 3.x release line ([#469](https://github.com/opensearch-project/search-relevance/pull/469))
* Bump com.google.code.gson:gson from 2.13.1 to 2.14.0 ([#457](https://github.com/opensearch-project/search-relevance/pull/457))
* Bump com.google.errorprone:error\_prone\_annotations from 2.48.0 to 2.49.0 ([#446](https://github.com/opensearch-project/search-relevance/pull/446))
* Bump com.google.guava:guava from 33.4.8-jre to 33.6.0-jre ([#452](https://github.com/opensearch-project/search-relevance/pull/452))
* Bump gradle-wrapper from 9.4.0 to 9.4.1 ([#423](https://github.com/opensearch-project/search-relevance/pull/423))
* Bump gradle-wrapper from 9.4.1 to 9.5.0 ([#464](https://github.com/opensearch-project/search-relevance/pull/464))
* Bump io.freefair.gradle:lombok-plugin from 9.2.0 to 9.5.0 ([#463](https://github.com/opensearch-project/search-relevance/pull/463))
* Bump org.javassist:javassist from 3.30.2-GA to 3.31.0-GA ([#453](https://github.com/opensearch-project/search-relevance/pull/453))


### OpenSearch Security


* Remove unnecessary debug log message for JWT authentication ([#6086](https://github.com/opensearch-project/security/pull/6086))
* Cleanup SafeSerializationUtils to remove unused Guava classes ([#6152](https://github.com/opensearch-project/security/pull/6152))
* Remove passay and Guava BaseEncoding dependencies, replace with JDK equivalents ([#6160](https://github.com/opensearch-project/security/pull/6160))
* Bump OpenSAML to 5.2.2 and remove unused ZooKeeper test dependency ([#6149](https://github.com/opensearch-project/security/pull/6149))


### OpenSearch Security Analytics


* Update security-analytics-commons to 1.0.0, bump Netty to 4.1.133.Final, upgrade Gradle wrapper to 9.4.1, and resolve build failures from monitor data model changes ([#1719](https://github.com/opensearch-project/security-analytics/pull/1719))


### OpenSearch Security Analytics Dashboards Plugin


* Baseline maintainers list ([#1401](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1401))
* Resolve CVE-2026-33750 by bumping brace-expansion to ^5.0.5 ([#1407](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1407))
* Resolve CVE-2026-27904, CVE-2026-33532, and CVE-2026-33672 by bumping minimatch to ^3.1.4 ([#1431](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1431))


### OpenSearch Security Dashboards Plugin


* Migrate plugin to TypeScript 6.0.2 compatibility ([#2418](https://github.com/opensearch-project/security-dashboards-plugin/pull/2418))


### OpenSearch Skills


* Update dependency com.google.code.gson:gson from 2.10.1 to 2.14.0 ([#368](https://github.com/opensearch-project/skills/pull/368))
* Update dependency lombok from 1.18.38 to 1.18.44 ([#671](https://github.com/opensearch-project/skills/pull/671))


### OpenSearch User Behavior Insights


* Upgrade Jackson dependency to version 3.1.2 ([#174](https://github.com/opensearch-project/user-behavior-insights/pull/174))


### OpenSearch k-NN


* Bump Gradle to 9.4.1 and JaCoCo to 0.8.14 to align with core OpenSearch ([#3308](https://github.com/opensearch-project/k-NN/pull/3308))
* Clean up Changelog.md file after 3.6 release ([#3266](https://github.com/opensearch-project/k-NN/pull/3266))


### SQL


* Add PPL bugfix skill for Claude Code with automated triage, TDD-style fix, and PR creation ([#5307](https://github.com/opensearch-project/sql/pull/5307))
* Refactor the dedupe workflow by extracting a reusable workflow to opensearch-build ([#5319](https://github.com/opensearch-project/sql/pull/5319))
* Skip bot-created issues in dedupe detect workflow ([#5328](https://github.com/opensearch-project/sql/pull/5328))
* Update dedupe workflow to have correct name ([#5327](https://github.com/opensearch-project/sql/pull/5327))
* Version bump to OpenSearch 3.7 with Jackson 2 → 3 parser API and `_source` excludes serialization fixes ([#5361](https://github.com/opensearch-project/sql/pull/5361))


## REFACTORING


### OpenSearch Neural Search


* Unify highlight tag application logic into shared HighlightTagApplier utility with strict validation for invalid model output ([#1862](https://github.com/opensearch-project/neural-search/pull/1862))


### OpenSearch Security


* Refactor certificate revocation validation for improved testability and diagnostics ([#6042](https://github.com/opensearch-project/security/pull/6042))
* Combine RestApiPrivilegesEvaluator and RestApiAdminPrivilegesEvaluator into RestApiAuthorizationEvaluator ([#6072](https://github.com/opensearch-project/security/pull/6072))
* Elevate tenant to top-level field on resource sharing document ([#6074](https://github.com/opensearch-project/security/pull/6074))
* Simplify `UserAttributes#findUnresolvedAttributes` ([#6122](https://github.com/opensearch-project/security/pull/6122))
* Move logic to reject certain endpoints when using OBO from authenticator to endpoint validator ([#6132](https://github.com/opensearch-project/security/pull/6132))


