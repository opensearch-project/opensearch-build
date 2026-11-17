# OpenSearch and OpenSearch Dashboards 3.10.0 Release Notes

## FEATURES

### OpenSearch Alerting Dashboards Plugin

* Show data streams in the monitor index picker for local and cross-cluster monitors ([#1518](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1518))
* Display monitor creator from resource sharing in the monitors list ([#1537](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1537))

### OpenSearch Common Utils

* Add a shared PluginClient for running transport actions as a plugin's system subject ([#1023](https://github.com/opensearch-project/common-utils/pull/1023))

### OpenSearch Dashboards Investigation

* Gate the create\_investigation tool on AnalyticEngine data sources, returning a clear "not available" message instead of creating an investigation that would fail ([#429](https://github.com/opensearch-project/dashboards-investigation/pull/429))

### OpenSearch Dashboards Observability

* Add Amazon CloudWatch alarms as an experimental, opt-in datasource in the unified Alerts view with alarm detail flyout, state history, metric preview, and composite-alarm relationship graph ([#2905](https://github.com/opensearch-project/dashboards-observability/pull/2905))
* Add PPL look-back window and per-action notification throttling for logs alert rules, with large-query handling and UX/a11y improvements ([#2899](https://github.com/opensearch-project/dashboards-observability/pull/2899))

### OpenSearch Dashboards Search Relevance

* Rename `%SearchText%` placeholder to `%queryText%` to align with Search Configuration index nomenclature, with backward compatibility for existing scripts ([#774](https://github.com/opensearch-project/dashboards-search-relevance/pull/774))
* Display per-query OpenSearch search latency in experiment results for comparing query performance across runs ([#959](https://github.com/opensearch-project/dashboards-search-relevance/pull/959))
* Gate the `/search-relevance` chat command on data source availability, returning a clear message when no compatible data source exists in the workspace ([#970](https://github.com/opensearch-project/dashboards-search-relevance/pull/970))

### OpenSearch Job Scheduler

* Deschedule orphaned jobs whose document was deleted from remote-store backed indices ([#1006](https://github.com/opensearch-project/job-scheduler/pull/1006))

### OpenSearch ML Commons

* Add client certificate authentication support for MCP connectors ([#5003](https://github.com/opensearch-project/ml-commons/pull/5003))
* Add `SearchTemplateFillTool` for agentic search templates ([#5106](https://github.com/opensearch-project/ml-commons/pull/5106))
* Expose `index_name` in `QueryPlanningTool` default user prompt so the LLM knows which index it is planning a query for ([#5127](https://github.com/opensearch-project/ml-commons/pull/5127))
* Include aggregation results in `SearchIndexTool` output when `return_raw_response` is false ([#5194](https://github.com/opensearch-project/ml-commons/pull/5194))
* Validate ML search request fields against an allowlist, rejecting unsupported search features with HTTP 400 ([#5205](https://github.com/opensearch-project/ml-commons/pull/5205))

### OpenSearch Neural Search

* In-query fusion for the hybrid query, enabling coordinator-side fusion with normalization and combination techniques directly in the query ([#2036](https://github.com/opensearch-project/neural-search/pull/2036))
* Enable fusion mode by default for hybrid queries via `plugins.neural_search.hybrid.fusion.enabled` setting ([#2037](https://github.com/opensearch-project/neural-search/pull/2037))
* Accept `fusion.weights` for request-level combination weights in fused hybrid queries ([#2065](https://github.com/opensearch-project/neural-search/pull/2065))
* Accept `pagination_depth` in fused hybrid queries as the fusion window size ([#2058](https://github.com/opensearch-project/neural-search/pull/2058))

### OpenSearch Notifications

* Add a REST API to send a message to a notification channel ([#1280](https://github.com/opensearch-project/notifications/pull/1280))

### OpenSearch Query Insights

* Show running PPL queries as single entries in Live Queries instead of listing each child search separately ([#699](https://github.com/opensearch-project/query-insights/pull/699))

### OpenSearch Query Insights Dashboards

* Add Username, User Roles, Backend Roles, and Application ID columns to Query Insights UI ([#513](https://github.com/opensearch-project/query-insights-dashboards/pull/513))
* Make Live queries table columns sortable with default sort by time elapsed descending ([#614](https://github.com/opensearch-project/query-insights-dashboards/pull/614))

### OpenSearch Search Relevance

* Persist per-query search latency (`tookMs`) on experiment results for performance visibility ([#593](https://github.com/opensearch-project/search-relevance/pull/593))

### OpenSearch Security Dashboards Plugin

* Add opt-in configuration to allow read-only users to access Discover and Visualize ([#2416](https://github.com/opensearch-project/security-dashboards-plugin/pull/2416))

### OpenSearch k-NN

* Add support for 2-bit and 4-bit scalar quantization for `half_float` vectors ([#3603](https://github.com/opensearch-project/k-NN/pull/3603))
* Support knn queries in percolator fields using exact search ([#3556](https://github.com/opensearch-project/k-NN/pull/3556))
* Support rescoring with `expand_nested_docs` on the Lucene engine ([#3579](https://github.com/opensearch-project/k-NN/pull/3579))

### SQL

* Support `flat_object` field type in PPL queries ([#5830](https://github.com/opensearch-project/sql/pull/5830))
* Add asynchronous PPL query submission and result retrieval ([#5832](https://github.com/opensearch-project/sql/pull/5832))
* Add cancellation and deletion support for async PPL queries ([#5846](https://github.com/opensearch-project/sql/pull/5846))
* Add language-neutral query job lifecycle framework ([#5818](https://github.com/opensearch-project/sql/pull/5818))

## ENHANCEMENTS

### OpenSearch Alerting

* Deprecate `filter_by_backend_roles` setting, targeting removal in 4.0 in favor of the security plugin's resource sharing and access control ([#2234](https://github.com/opensearch-project/alerting/pull/2234))
* Register findings indices (`.opensearch-alerting-finding*`) as protected system indices when the security plugin is enabled ([#2310](https://github.com/opensearch-project/alerting/pull/2310))
* Repair history write aliases automatically after a snapshot restore to prevent alert, finding, and comment history write failures ([#2312](https://github.com/opensearch-project/alerting/pull/2312))
* Use the current query index for doc-level monitors when the saved query index no longer exists after a restore ([#2309](https://github.com/opensearch-project/alerting/pull/2309))

### OpenSearch Anomaly Detection

* Deprecate `filter_by_backend_roles` setting, targeting removal in 4.0 in favor of the security plugin's resource sharing and access control ([#1781](https://github.com/opensearch-project/anomaly-detection/pull/1781))

### OpenSearch Anomaly Detection Dashboards Plugin

* Fix AnalyticEngine source selection in anomaly detection and forecasting to support compatible sources and improve fallback behavior ([#1265](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1265))

### OpenSearch Asynchronous Search

* Guard eclipse() to spotless tasks and keep P2 mirror on pinned version ([#867](https://github.com/opensearch-project/asynchronous-search/pull/867))

### OpenSearch Cross Cluster Replication

* Seek to chunk offset on the leader during bootstrap instead of read-and-discard, reducing leader-side I/O from O(N²) to O(N) per file ([#1751](https://github.com/opensearch-project/cross-cluster-replication/pull/1751))
* Coalesce concurrent `_stop` replication cluster-state updates via TaskBatcher to eliminate timeout failures at high concurrency ([#1770](https://github.com/opensearch-project/cross-cluster-replication/pull/1770))
* Make `FollowerClusterStats` thread-safe with `ConcurrentHashMap` and null-guard stat reads to prevent shard failures during concurrent task start/stop ([#1771](https://github.com/opensearch-project/cross-cluster-replication/pull/1771))
* Expose leader translog generation threshold as a configurable follower cluster setting (`plugins.replication.follower.leader_translog_generation_threshold_size`) to reduce leader CPU overhead ([#1766](https://github.com/opensearch-project/cross-cluster-replication/pull/1766))
* Refresh `follower_checkpoint` from the live shard on every read-loop iteration so `follower_stats` no longer reports stale checkpoints on idle indices ([#1745](https://github.com/opensearch-project/cross-cluster-replication/pull/1745))

### OpenSearch Dashboards Observability

* Add unified APM service catalog and application map with typed external dependencies for databases, message brokers, and external endpoints ([#2898](https://github.com/opensearch-project/dashboards-observability/pull/2898))
* Allow AnalyticEngine-backed datasets in APM settings selectors now that AnalyticEngine supports APM queries ([#2914](https://github.com/opensearch-project/dashboards-observability/pull/2914))
* Add synced crosshair, time brush zoom, legend isolate, x-axis overlap fix, and open-in-metrics deep link to APM PromQL charts ([#2900](https://github.com/opensearch-project/dashboards-observability/pull/2900))
* Route GenAI span correlations from APM to Agent Traces when the Agent Traces app is available ([#2910](https://github.com/opensearch-project/dashboards-observability/pull/2910))
* Show dependency-type icons in the APM service catalog, details header, and map side panel ([#2927](https://github.com/opensearch-project/dashboards-observability/pull/2927))
* Apply consistent status and severity label casing, clear messaging for deleted-monitor alerts, and scoped deep-link search in the Alerting view ([#2944](https://github.com/opensearch-project/dashboards-observability/pull/2944))
* Log data connection route failures via plugin logger at appropriate levels instead of dumping full error objects to stderr ([#2915](https://github.com/opensearch-project/dashboards-observability/pull/2915))

### OpenSearch Dashboards Search Relevance

* Add missing tooltips for MRR, Recall, and DCG metrics on the experiment summary page ([#967](https://github.com/opensearch-project/dashboards-search-relevance/pull/967))

### OpenSearch Index Management Dashboards Plugin

* Wrap long index names and enable sorting by job status and data stream on the policy managed indexes page ([#1494](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1494))

### OpenSearch ML Commons

* Parse connector endpoint URLs before matching the allowlist and tighten default AWS patterns; also reported by Tony Piazza (@tonypiazza) ([#5192](https://github.com/opensearch-project/ml-commons/pull/5192))
* Address review feedback on connector endpoint validation: accept predict-time placeholders, sanitize rejected-URL log output, and update AWS default patterns ([#5196](https://github.com/opensearch-project/ml-commons/pull/5196))
* Apply the connector address policy to OpenAI- and Gemini-style HTTP streaming requests ([#5207](https://github.com/opensearch-project/ml-commons/pull/5207))
* Classify IPv6 unique-local, link-local, NAT64, and metadata addresses in the connector private-IP check; reported by Tony Piazza (@tonypiazza) ([#5208](https://github.com/opensearch-project/ml-commons/pull/5208))
* Keep model cache paths inside the cache root directory, rejecting absolute or path-traversal components ([#5198](https://github.com/opensearch-project/ml-commons/pull/5198))
* Validate Vertex AI `batch_predict` URL at connector-create time to prevent orphaned billing jobs ([#5188](https://github.com/opensearch-project/ml-commons/pull/5188))
* Return 409 when a model group is registered again with the same custom id ([#5155](https://github.com/opensearch-project/ml-commons/pull/5155))
* Serve predictions from deployed nodes when a local model is partially deployed instead of rejecting all requests ([#5142](https://github.com/opensearch-project/ml-commons/pull/5142))
* Omit Bedrock `toolConfig` when the agent has no tools to avoid Converse API rejection ([#5215](https://github.com/opensearch-project/ml-commons/pull/5215))
* Derive sortable-aware field enums from all target index mappings for agentic search templates ([#5122](https://github.com/opensearch-project/ml-commons/pull/5122))
* Correct derived parameter and template descriptions for agentic search templates ([#5123](https://github.com/opensearch-project/ml-commons/pull/5123))
* Only describe a `should` clause as scoring-only when its enclosing `bool` makes it optional in agentic search templates ([#5164](https://github.com/opensearch-project/ml-commons/pull/5164))
* Fill list parameters as JSON arrays in `SearchTemplateFillTool` ([#5163](https://github.com/opensearch-project/ml-commons/pull/5163))
* Return the proper not-found error body on metadata-only update of a missing agentic search template ([#5120](https://github.com/opensearch-project/ml-commons/pull/5120))

### OpenSearch Neural Search

* Allow `sort: [_score, <field>]` for hybrid queries with collapse for deterministic group-head selection ([#2010](https://github.com/opensearch-project/neural-search/pull/2010))
* Gate collapse distinct-groups collection behind an opt-in index setting `index.neural_search.hybrid_collapse_distinct_groups_enabled` ([#1956](https://github.com/opensearch-project/neural-search/pull/1956))
* Support lists and scalars with per-element fragments in semantic highlighting ([#2000](https://github.com/opensearch-project/neural-search/pull/2000))
* Expose neural sparse filters to query builder and Lucene visitors, and reject unsupported `method_parameters.filter` on `rank_features` fields explicitly ([#2044](https://github.com/opensearch-project/neural-search/pull/2044))
* Add routing support to the `skip_existing` lookup for inference processors (`text_embedding`, `sparse_encoding`, `text_image_embedding`) ([#2028](https://github.com/opensearch-project/neural-search/pull/2028))
* Reject non-numeric score-combination weights with HTTP 400 instead of HTTP 500 ([#2067](https://github.com/opensearch-project/neural-search/pull/2067))

### OpenSearch Notifications

* Deprecate `filter_by_backend_roles` setting, targeting removal in 4.0 in favor of resource sharing ([#1274](https://github.com/opensearch-project/notifications/pull/1274))

### OpenSearch Query Insights

* Read historical top queries as the plugin subject instead of borrowing the caller's thread context ([#694](https://github.com/opensearch-project/query-insights/pull/694))

### OpenSearch Reporting

* Deprecate `filter_by_backend_roles` setting, targeting removal in 4.0 in favor of security plugin resource sharing ([#1226](https://github.com/opensearch-project/reporting/pull/1226))

### OpenSearch Search Relevance

* Make `%queryText%` the default query placeholder and deprecate `%SearchText%` with backward-compatible fallback ([#613](https://github.com/opensearch-project/search-relevance/pull/613))

### OpenSearch Security Analytics

* Deprecate `filter_by_backend_roles` setting, targeting removal in 4.0 in favor of resource sharing and access control ([#1818](https://github.com/opensearch-project/security-analytics/pull/1818))

### OpenSearch Security Dashboards Plugin

* Include the tenant index name in migration failure log messages for easier troubleshooting ([#2538](https://github.com/opensearch-project/security-dashboards-plugin/pull/2538))

### OpenSearch k-NN

* Add SIMD kernels for SQ 2-bit and 4-bit distance computation during indexing for faster graph builds ([#3655](https://github.com/opensearch-project/k-NN/pull/3655))
* Avoid unnecessary FP16 → FP32 → FP16 round trip when merging `half_float` segments ([#3610](https://github.com/opensearch-project/k-NN/pull/3610))
* Honor query cancellation and timeout in memory-optimized Faiss search ([#3620](https://github.com/opensearch-project/k-NN/pull/3620))
* Remove synchronized keyword from KNNSettings instance creation to reduce lock contention on hot paths ([#3630](https://github.com/opensearch-project/k-NN/pull/3630))
* Score ADC queries from a precomputed per-query table for significantly faster 1-bit quantized scoring ([#3633](https://github.com/opensearch-project/k-NN/pull/3633))
* Send `half_float` vectors to the remote index build service as native FP16 to halve upload size ([#3608](https://github.com/opensearch-project/k-NN/pull/3608))
* Use a dedicated 1-bit SQ distance computer to restore 1-bit indexing performance ([#3652](https://github.com/opensearch-project/k-NN/pull/3652))

### SQL

* Fail PPL queries with HTTP 429 when the SQL worker pool is saturated instead of silently dropping them ([#5915](https://github.com/opensearch-project/sql/pull/5915))
* Support Unicode string literals in the Calcite PPL engine ([#5774](https://github.com/opensearch-project/sql/pull/5774))
* Support data streams and implicit time fields in index pruning ([#5908](https://github.com/opensearch-project/sql/pull/5908))
* Prune indices by request-level time bounds before the schema is resolved ([#5766](https://github.com/opensearch-project/sql/pull/5766))
* Raise default structural limits for the deserialization filter ([#5826](https://github.com/opensearch-project/sql/pull/5826))
* Report progress for asynchronous Calcite PPL queries ([#5910](https://github.com/opensearch-project/sql/pull/5910))
* Bound PPL `parse`/`rex` regex matching work with a configurable match limit ([#5921](https://github.com/opensearch-project/sql/pull/5921))
* Make the `flat_object` read depth cap configurable ([#5861](https://github.com/opensearch-project/sql/pull/5861))
* Optimize nested field removal to O(n), reducing query time from 40s to 600ms on large schemas ([#5913](https://github.com/opensearch-project/sql/pull/5913))
* Restore `SUM(narrow_int + literal)` aggregation pushdown for improved performance ([#5827](https://github.com/opensearch-project/sql/pull/5827))

## BUG FIXES

### OpenSearch Alerting

* Fix `ClassCastException` when updating a doc-level monitor whose metadata has an empty last run context ([#2271](https://github.com/opensearch-project/alerting/pull/2271))
* Fix PPL monitor failures when the SQL/PPL plugin returns a response without a `total` field ([#2270](https://github.com/opensearch-project/alerting/pull/2270))
* Record the creator on a workflow's sharing record so workflows are discoverable and shareable under resource sharing ([#2300](https://github.com/opensearch-project/alerting/pull/2300))
* Reset stale last run context for doc-level monitors after a snapshot restore so new documents are not silently skipped ([#2287](https://github.com/opensearch-project/alerting/pull/2287))

### OpenSearch Alerting Dashboards Plugin

* Fix monitor search for hyphenated names, PPL monitor card gating for unsupported data sources, Notifications plugin detection probe, and create-form reset on data source change ([#1523](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1523))
* Make look-back window editable when editing a PPL monitor ([#1516](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1516))

### OpenSearch Anomaly Detection

* Prevent historical high-cardinality anomaly detection analyses from remaining stuck in RUNNING state after task-slot scale-down ([#1782](https://github.com/opensearch-project/anomaly-detection/pull/1782))
* Fix PPL transport wire format mismatch and invalid test role permissions causing integration test failures on 3.10 ([#1798](https://github.com/opensearch-project/anomaly-detection/pull/1798))
* Fix flaky empty-index detector integration test by ensuring the source index maps the time field as `date` ([#1787](https://github.com/opensearch-project/anomaly-detection/pull/1787))

### OpenSearch Asynchronous Search

* Fix typo in log message: "occured" corrected to "occurred" ([#832](https://github.com/opensearch-project/asynchronous-search/pull/832))

### OpenSearch Cross Cluster Replication

* Fix continuous replica churn on follower indices using `auto_expand_replicas` by guarding `number_of_replicas` removal in the metadata-sync path ([#1772](https://github.com/opensearch-project/cross-cluster-replication/pull/1772))

### OpenSearch Dashboards Observability

* Improve SLO validation messages for rejected forDuration values and correctly classify wrapped ruler auth and conflict errors ([#2912](https://github.com/opensearch-project/dashboards-observability/pull/2912))
* Fix "Open in Discover metrics" button crashing Explore by sending only the required app state section ([#2946](https://github.com/opensearch-project/dashboards-observability/pull/2946))
* Fix stale sparkline shown for services with no data and empty sparklines on long time ranges with little history ([#2941](https://github.com/opensearch-project/dashboards-observability/pull/2941))
* Re-resolve relative time ranges on refresh and sync from/to with the URL across all APM pages ([#2909](https://github.com/opensearch-project/dashboards-observability/pull/2909))
* Scope Services page PromQL queries to active filters and eliminate duplicate fetches that caused slow loads and timeouts ([#2933](https://github.com/opensearch-project/dashboards-observability/pull/2933))
* Fix SLOs always showing No data or Source idle by recovering metric names from both PromQL series shapes and correcting span-derived SLI math ([#2934](https://github.com/opensearch-project/dashboards-observability/pull/2934))
* Restrict Explore's "Create alert rule" actions to supported dataset types and query languages ([#2928](https://github.com/opensearch-project/dashboards-observability/pull/2928))

### OpenSearch Dashboards Query Workbench

* Remove misleading "this query is not runnable" error suffix from non-permission failures ([#589](https://github.com/opensearch-project/dashboards-query-workbench/pull/589))
* Fix typo in invalid query ID error message: "Recieved" → "Received" ([#555](https://github.com/opensearch-project/dashboards-query-workbench/pull/555))

### OpenSearch Dashboards Search Relevance

* Escape formula-triggering characters in document scores CSV export to prevent spreadsheet injection ([#957](https://github.com/opensearch-project/dashboards-search-relevance/pull/957))

### OpenSearch Geospatial

* Fix ip2geo datasource refresh failure after snapshot restore by setting refresh policy on the BulkRequest instead of individual item requests ([#909](https://github.com/opensearch-project/geospatial/pull/909))

### OpenSearch Index Management

* Resume ISM policies after restoring the config index from a snapshot ([#1754](https://github.com/opensearch-project/index-management/pull/1754))
* Reconcile policy version mismatches instead of failing the managed index job ([#1746](https://github.com/opensearch-project/index-management/pull/1746))
* Skip initialization of orphaned managed index jobs whose document was deleted ([#1743](https://github.com/opensearch-project/index-management/pull/1743))
* Resolve plugin-injected index UUID in AttemptTransitionStep for re-attached indices ([#1757](https://github.com/opensearch-project/index-management/pull/1757))
* Report Snapshot Management snapshot creation as failed when the snapshot is missing ([#1759](https://github.com/opensearch-project/index-management/pull/1759))

### OpenSearch Index Management Dashboards Plugin

* Add `flat` as an explicit dependency to fix distribution build failures ([#1498](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1498))

### OpenSearch Job Scheduler

* Run scheduled jobs in a clean thread context to prevent inheriting the indexing writer's credentials ([#1028](https://github.com/opensearch-project/job-scheduler/pull/1028))
* Fix flaky tests in LockServiceIT ([#914](https://github.com/opensearch-project/job-scheduler/pull/914))

### OpenSearch ML Commons

* Clear cached master keys when the ML config index is replaced to prevent decryption failures after snapshot restore ([#5166](https://github.com/opensearch-project/ml-commons/pull/5166))
* Fix races in master key cache invalidation after config index replacement ([#5199](https://github.com/opensearch-project/ml-commons/pull/5199))
* Clear node model cache on remote deploy failure without evicting concurrent deploys ([#5193](https://github.com/opensearch-project/ml-commons/pull/5193))
* Fix deploy tasks and model state getting stuck after nodes leave or cluster manager changes ([#5209](https://github.com/opensearch-project/ml-commons/pull/5209))
* Fix model auto redeploy during node join bursts to prevent retry exhaustion and permanent exclusion ([#5217](https://github.com/opensearch-project/ml-commons/pull/5217))
* Keep deployed models when the deploy task's coordinating node leaves or nodes join during a deploy ([#5143](https://github.com/opensearch-project/ml-commons/pull/5143))
* Fix NPE when registering a `plan_execute_and_reflect` agent without a `parameters` block ([#5216](https://github.com/opensearch-project/ml-commons/pull/5216))
* Fix left-padded `LAST_TOKEN` pooling for decoder-only models and coerce attention mask dtype in the shared helper ([#4744](https://github.com/opensearch-project/ml-commons/pull/4744))
* Fix register task failure handling and legacy ML config mapping conflict that blocked remote model registration ([#5200](https://github.com/opensearch-project/ml-commons/pull/5200))
* Pass the calling user into model group delete access validation and return proper 403/404 status codes ([#5219](https://github.com/opensearch-project/ml-commons/pull/5219))
* Apply access mode consistently for model groups and connectors without an owner ([#5197](https://github.com/opensearch-project/ml-commons/pull/5197))
* Serialize non-String tool output in MCP server `tools/call` to fix `ClassCastException` ([#5214](https://github.com/opensearch-project/ml-commons/pull/5214))
* Fix typo in input/output map within ml-inference processor documentation ([#3556](https://github.com/opensearch-project/ml-commons/pull/3556))

### OpenSearch Neural Search

* Fix hybrid `collapse` sorted by ascending `_score` returning wrong documents and undercounted `hits.total` on shards with more than 4,096 matching documents ([#2026](https://github.com/opensearch-project/neural-search/pull/2026))
* Fix semantic field processor indexing documents without embeddings on inference failure by ensuring the error handler returns immediately ([#2033](https://github.com/opensearch-project/neural-search/pull/2033))
* Fix `ClassCastException` when a point-in-time slice or alias filter excludes a shard from a hybrid query ([#2045](https://github.com/opensearch-project/neural-search/pull/2045))
* Reject sorting a hybrid query by `_score` ascending or by `_score` more than once, which previously returned wrong results silently ([#2046](https://github.com/opensearch-project/neural-search/pull/2046))
* Reject unknown `combination.parameters` keys and unknown keys on inline `fusion` clauses instead of silently ignoring them ([#2069](https://github.com/opensearch-project/neural-search/pull/2069))
* Reject a hybrid query without fusion nested in a hybrid query with fusion, or vice versa, with a clear error ([#2051](https://github.com/opensearch-project/neural-search/pull/2051))
* Resolve fused hybrid legs before fan-out so a sub-query's inference runs once per request instead of twice ([#2074](https://github.com/opensearch-project/neural-search/pull/2074))
* Keep `agent_steps_summary` from the conversational agent's final output for OpenAI native function calling in agentic search ([#2071](https://github.com/opensearch-project/neural-search/pull/2071))
* Pass `_routing` to the semantic field `skip_existing_embedding` lookup so documents with custom routing are found correctly ([#2040](https://github.com/opensearch-project/neural-search/pull/2040))
* Fix `field_map` sibling key overwrite when multiple fields share a dotted prefix, which silently dropped embeddings ([#2052](https://github.com/opensearch-project/neural-search/pull/2052))
* Fix deep-merge of `field_map` target maps so nested siblings at any depth are preserved ([#2054](https://github.com/opensearch-project/neural-search/pull/2054))
* Stop logging customer document content on semantic field processor ingest failure; log only document identifiers ([#2057](https://github.com/opensearch-project/neural-search/pull/2057))
* Fix sparse ANN documents with token IDs at or above 32768 never matching on approximate search on the Lucene and native engines ([#2059](https://github.com/opensearch-project/neural-search/pull/2059))
* Fix batch semantic highlighting skipping `inner_hits` semantic highlight targets below `boosting` or `script_score` queries that wrap a compound query, such as `boosting > bool > nested` ([#2086](https://github.com/opensearch-project/neural-search/pull/2086))

### OpenSearch Query Insights

* Fix backend\_roles filter dropping top query records received from other nodes due to array type mismatch after transport serialization ([#702](https://github.com/opensearch-project/query-insights/pull/702))
* Reject empty or blank exporter type at settings validation time to prevent cluster-manager wedge ([#700](https://github.com/opensearch-project/query-insights/pull/700))

### OpenSearch Query Insights Dashboards

* Fix race condition where stale data source capability results could update the UI after switching data sources ([#598](https://github.com/opensearch-project/query-insights-dashboards/pull/598))
* Fix broken "Learn more" link on the Create workload group page by removing duplicated path segment ([#599](https://github.com/opensearch-project/query-insights-dashboards/pull/599))

### OpenSearch Search Relevance

* Add missing `slf4j-api` runtime dependency so LLM judgment no longer crashes the node with `NoClassDefFoundError` on the first completed remote-model predict call ([#322](https://github.com/opensearch-project/search-relevance/pull/322))
* Validate manual judgment rating edits on the server, rejecting non-finite and out-of-range values that previously broke metric evaluation ([#601](https://github.com/opensearch-project/search-relevance/pull/601))
* Force jspecify 1.0.1 to fix dependency version conflict ([#602](https://github.com/opensearch-project/search-relevance/pull/602))

### OpenSearch Security Analytics

* Guard against null and immutable map returns in RuleIndices and CustomLogType to prevent NPE and UnsupportedOperationException ([#1797](https://github.com/opensearch-project/security-analytics/pull/1797))
* Resolve index template by backing index for index-alias mappings to prevent component templates from attaching to the wrong template ([#1835](https://github.com/opensearch-project/security-analytics/pull/1835))
* Get alerts of all accessible detectors with server-side paging, sorting, and filtering instead of loading all alerts client-side ([#1837](https://github.com/opensearch-project/security-analytics/pull/1837))

### OpenSearch Security Analytics Dashboards Plugin

* Fix endless alert fetching, table flicker, and server-side paging/sorting/filtering for detection rule alerts ([#1593](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1593))

### OpenSearch Security Dashboards Plugin

* Derive login page title from branding `applicationTitle` instead of hardcoding "OpenSearch Dashboards" ([#2503](https://github.com/opensearch-project/security-dashboards-plugin/pull/2503))
* Preserve `nextUrl` query parameter when logging in with anonymous authentication ([#2524](https://github.com/opensearch-project/security-dashboards-plugin/pull/2524))
* Extend `validateNextUrl` validation to remaining redirect routes not covered by the 2024 sweep ([#2531](https://github.com/opensearch-project/security-dashboards-plugin/pull/2531))
* Prevent process exit when a single tenant index migration fails, allowing remaining tenants to proceed ([#2535](https://github.com/opensearch-project/security-dashboards-plugin/pull/2535))
* Re-validate the resource name field on change so validation errors clear as the user corrects input ([#2537](https://github.com/opensearch-project/security-dashboards-plugin/pull/2537))
* Honor `enable_private` setting from `opensearch_dashboards.yml` for private tenant availability ([#2578](https://github.com/opensearch-project/security-dashboards-plugin/pull/2578))
* Disable the custom tenant combo box when no custom tenants are available ([#2579](https://github.com/opensearch-project/security-dashboards-plugin/pull/2579))
* Trim leading and trailing spaces from backend roles and mapped users before saving ([#2580](https://github.com/opensearch-project/security-dashboards-plugin/pull/2580))
* Route JWT logout to the correct JWT logout endpoint instead of returning 404 ([#2581](https://github.com/opensearch-project/security-dashboards-plugin/pull/2581))

### OpenSearch k-NN

* Align field visibility across k-NN search paths so excluded fields behave consistently ([#3659](https://github.com/opensearch-project/k-NN/pull/3659))
* Fix SIGSEGV in Faiss SQ HNSW build caused by 32-bit offset overflow with large segments ([#3653](https://github.com/opensearch-project/k-NN/pull/3653))
* Fix derived source returning another document's nested vectors for parents with many nested docs ([#3624](https://github.com/opensearch-project/k-NN/pull/3624))
* Fix double free of off-heap vectors when a native index build fails, preventing JVM crash ([#3621](https://github.com/opensearch-project/k-NN/pull/3621))
* Fix explain NPE for Lucene engine rescore and `expand_nested_docs` queries ([#3641](https://github.com/opensearch-project/k-NN/pull/3641))
* Fix build compatibility issues from Lucene 10.5.2 upgrade ([#3631](https://github.com/opensearch-project/k-NN/pull/3631))
* Rethrow merge abort during native index write so Lucene drops the merge cleanly ([#3651](https://github.com/opensearch-project/k-NN/pull/3651))
* Return model-not-found error when getting a model before the model index exists ([#3598](https://github.com/opensearch-project/k-NN/pull/3598))

### SQL

* Fix HTTP 500 from `coalesce`, `mvappend`, `array`, and `percentile_approx` on `short`, `byte`, and `float` values ([#5874](https://github.com/opensearch-project/sql/pull/5874))
* Fix HTTP 500 from `sort` and `stats` on `object`, `nested`, `geo_point`, and `flat_object` fields ([#5858](https://github.com/opensearch-project/sql/pull/5858))
* Fix HTTP 500 and empty results from `binary` fields in Calcite pushdowns ([#5767](https://github.com/opensearch-project/sql/pull/5767))
* Fix HTTP 500 from `in`, `between`, `case`, and `coalesce` on `object` and `nested` fields ([#5870](https://github.com/opensearch-project/sql/pull/5870))
* Fix comma-separated sources failing with request-level time bounds ([#5852](https://github.com/opensearch-project/sql/pull/5852))
* Fix status code mislabeling in legacy engine responses ([#5850](https://github.com/opensearch-project/sql/pull/5850))
* Fix `count`/`dc` failing after a `fields` command that narrows the row ([#5783](https://github.com/opensearch-project/sql/pull/5783))
* Fix `expand` on non-column values reporting a `ClassCastException` instead of a user-friendly error ([#5841](https://github.com/opensearch-project/sql/pull/5841))
* Fix empty PPL query returning HTTP 500 instead of 400 ([#5868](https://github.com/opensearch-project/sql/pull/5868))
* Fix empty SQL query returning HTTP 500 instead of 400 ([#5880](https://github.com/opensearch-project/sql/pull/5880))
* Keep metadata fields hidden per input of `append`, `appendpipe`, `appendcol`, `union`, and `lookup` ([#5884](https://github.com/opensearch-project/sql/pull/5884))
* Fix node crash when PPL alerting monitor triggers due to missing `opensearch` module class ([#5924](https://github.com/opensearch-project/sql/pull/5924))
* Register background search tasks as children of parent to prevent zombie tasks on cancellation ([#5888](https://github.com/opensearch-project/sql/pull/5888))
* Resolve cross-cluster index schemas through the remote cluster's GetMappings API ([#5844](https://github.com/opensearch-project/sql/pull/5844))

## INFRASTRUCTURE

### OpenSearch Alerting

* Restore BWC upgrade tests and CI checks for rolling and full-restart upgrades ([#2305](https://github.com/opensearch-project/alerting/pull/2305))
* Restore the alerting unit test suite by fixing node startup when the SQS poller is enabled but unconfigured, and resolve all 77 pre-existing test failures on main ([#2314](https://github.com/opensearch-project/alerting/pull/2314))
* Fix seed-dependent failure in the bucket-level acknowledged-alert integration test ([#2315](https://github.com/opensearch-project/alerting/pull/2315))
* Correct the cause recorded for the acknowledged-alert test and remove a redundant action ([#2316](https://github.com/opensearch-project/alerting/pull/2316))

### OpenSearch Common Utils

* Add test for PluginClient listener that completes inside runAs on the calling thread ([#1027](https://github.com/opensearch-project/common-utils/pull/1027))

### OpenSearch Dashboards Maps

* Pin Cypress version in FTR E2E workflow to prevent breakage from upstream major releases ([#876](https://github.com/opensearch-project/dashboards-maps/pull/876))

### OpenSearch Dashboards Search Relevance

* Ignore test-only link in Lychee link checker to fix build ([#962](https://github.com/opensearch-project/dashboards-search-relevance/pull/962))
* Install the functional test repository's pinned Cypress version in the FTR E2E workflow to prevent breakage from upstream major releases ([#958](https://github.com/opensearch-project/dashboards-search-relevance/pull/958))
* Add unit tests for ExperimentMetadataFields, increasing coverage from 0% to 100% ([#968](https://github.com/opensearch-project/dashboards-search-relevance/pull/968))

### OpenSearch Job Scheduler

* Enable OpenSearch logger usage check for Job Scheduler plugin builds ([#933](https://github.com/opensearch-project/job-scheduler/pull/933))

### OpenSearch ML Commons

* Raise the REST integration test task wait cap to 60 seconds for slow CI runners ([#5195](https://github.com/opensearch-project/ml-commons/pull/5195))
* Skip `RestSearchTemplateFillToolIT` on the containerized cluster leg where the mock server is unreachable ([#5165](https://github.com/opensearch-project/ml-commons/pull/5165))

### OpenSearch Neural Search

* Register BWC test models from `raw.githubusercontent.com` directly, fixing restart-upgrade tests for OpenSearch 2.9–2.11 ([#2070](https://github.com/opensearch-project/neural-search/pull/2070))
* Match k-NN explanation by shape in explain integration tests to accommodate Lucene 10.6 wording changes ([#2079](https://github.com/opensearch-project/neural-search/pull/2079))

### OpenSearch Query Insights Dashboards

* Prevent Cypress readiness checks from hanging by adding connection and response timeouts to startup probes ([#581](https://github.com/opensearch-project/query-insights-dashboards/pull/581))

### OpenSearch Search Relevance

* Simplify model-group registration in `demo_hybrid_optimizer.sh` using idempotent register pattern ([#629](https://github.com/opensearch-project/search-relevance/pull/629))
* Suppress javadoc missing-comment warnings for internal classes while preserving real error detection ([#628](https://github.com/opensearch-project/search-relevance/pull/628))
* Update `systemProp.bwc.bundle.version` on minor version bumps ([#598](https://github.com/opensearch-project/search-relevance/pull/598))

### OpenSearch Security Analytics Dashboards Plugin

* Fix Cypress CI failures, TypeScript 6 compatibility, and detector toggle action bug ([#1603](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1603))

### OpenSearch Security Dashboards Plugin

* Isolate co-located CI test clusters to prevent accidental cluster merges during integration tests ([#2507](https://github.com/opensearch-project/security-dashboards-plugin/pull/2507))
* Test base Dashboards roles in tenant integration and Cypress suites ([#2564](https://github.com/opensearch-project/security-dashboards-plugin/pull/2564))
* Fix resource-sharing CI cluster startup by updating the start-opensearch action pin ([#2569](https://github.com/opensearch-project/security-dashboards-plugin/pull/2569))
* Build only the selected theme for security Cypress tests to reduce build time ([#2570](https://github.com/opensearch-project/security-dashboards-plugin/pull/2570))
* Use single theme build in tenancy-disabled and resource-sharing Cypress workflows ([#2571](https://github.com/opensearch-project/security-dashboards-plugin/pull/2571))
* Strengthen GitHub workflows with default token for releases, read-only permissions, and no persisted credentials ([#2583](https://github.com/opensearch-project/security-dashboards-plugin/pull/2583))

### OpenSearch k-NN

* Use clustered test vectors and the api-snapshot builder image so remote index build ITs pass on cuVS 26.08 ([#3627](https://github.com/opensearch-project/k-NN/pull/3627))

### SQL

* Add OpenTelemetry logs and traces data stream fixtures for mapping conflict integration tests ([#5831](https://github.com/opensearch-project/sql/pull/5831))
* Fix index pruning YAML test flakiness ([#5813](https://github.com/opensearch-project/sql/pull/5813))
* Report unit test coverage across modules using aggregated JaCoCo reports ([#5891](https://github.com/opensearch-project/sql/pull/5891))
* Split out CI assemble and lint steps for better caching and clarity ([#5365](https://github.com/opensearch-project/sql/pull/5365))
* Add `runWithSecurity` Gradle task for local development ([#5878](https://github.com/opensearch-project/sql/pull/5878))
* Run `AnalyticsEngineSecurityIT`/`ProfileIT` in CI and fix drifted AE plugin download URLs ([#5782](https://github.com/opensearch-project/sql/pull/5782))

## DOCUMENTATION

### OpenSearch Common Utils

* Document plugin-additional-permissions.yml format and usage on PluginClient ([#1026](https://github.com/opensearch-project/common-utils/pull/1026))

### OpenSearch Dashboards Investigation

* Remove broken README badges for workflows and tests that no longer exist ([#422](https://github.com/opensearch-project/dashboards-investigation/pull/422))

### OpenSearch Dashboards Observability

* Fix broken documentation links after opensearch.org to docs.opensearch.org migration ([#2886](https://github.com/opensearch-project/dashboards-observability/pull/2886))

### OpenSearch Neural Search

* Add changelog entry for field\_map sibling key overwrite fix ([#2053](https://github.com/opensearch-project/neural-search/pull/2053))

### OpenSearch Query Insights

* Document and add integration test coverage for Top Queries API permissions ([#662](https://github.com/opensearch-project/query-insights/pull/662))

### OpenSearch Query Insights Dashboards

* Add developer guide covering setup, building, running, testing, and troubleshooting the plugin ([#611](https://github.com/opensearch-project/query-insights-dashboards/pull/611))

### OpenSearch Search Relevance

* Add KNOWN\_ISSUES.md documenting known issues and workarounds ([#635](https://github.com/opensearch-project/search-relevance/pull/635))
* Fix broken search relevance documentation link in the README ([#603](https://github.com/opensearch-project/search-relevance/pull/603))
* Document repository best practices for contributors and maintainers ([#621](https://github.com/opensearch-project/search-relevance/pull/621))
* Add `demo_llm_as_judge.sh`, an LLM-as-a-judge demo script with local Ollama and OpenAI connector support ([#322](https://github.com/opensearch-project/search-relevance/pull/322))
* Fix GitHub Pages build by removing unsupported Liquid include tags and update design doc to reflect shipped implementation ([#633](https://github.com/opensearch-project/search-relevance/pull/633))

### SQL

* Improve `lookup` command documentation and fix doc loading bug ([#5824](https://github.com/opensearch-project/sql/pull/5824))

## MAINTENANCE

### OpenSearch Alerting Dashboards Plugin

* Bump decode-uri-component and qs to remediate CVE-2026-45822, CVE-2026-82417, and CVE-2026-82562 ([#1539](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1539))
* Update query-string to 9.5.1 to address CVEs in decode-uri-component ([#1532](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1532))

### OpenSearch Anomaly Detection Dashboards Plugin

* Update moment dependency to 2.31.0 to address CVEs ([#1260](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1260))

### OpenSearch Dashboards Assistant

* Update brace-expansion to 5.0.12 and dompurify to 3.4.17 to address CVEs ([#748](https://github.com/opensearch-project/dashboards-assistant/pull/748))

### OpenSearch Dashboards Investigation

* Update dompurify from 3.4.13 to 3.4.17 to address reported CVEs ([#426](https://github.com/opensearch-project/dashboards-investigation/pull/426))

### OpenSearch Dashboards Notifications

* Remediate CVEs in dashboards-notifications by bumping `qs` to 6.16.0 ([#502](https://github.com/opensearch-project/dashboards-notifications/pull/502))

### OpenSearch Dashboards Observability

* Defer Trace Analytics initial fetch until MDS data source resolves to prevent errors when no local cluster exists ([#2902](https://github.com/opensearch-project/dashboards-observability/pull/2902))
* Bump brace-expansion to 5.0.12 and fast-uri to 3.1.9 to fix multiple CVEs ([#2960](https://github.com/opensearch-project/dashboards-observability/pull/2960))
* Bump dompurify to 3.4.17 to fix critical template bypass and other security advisories ([#2938](https://github.com/opensearch-project/dashboards-observability/pull/2938))
* Bump dompurify from 3.4.13 to 3.4.16 ([#2913](https://github.com/opensearch-project/dashboards-observability/pull/2913))
* Bump source-map-js from 1.2.1 to 1.2.2 to fix CSP crash and denial-of-service CVE ([#2920](https://github.com/opensearch-project/dashboards-observability/pull/2920))

### OpenSearch Dashboards Query Workbench

* Bump `qs` to 6.16.1 to address CVE-2026-110816 (medium severity DoS) ([#615](https://github.com/opensearch-project/dashboards-query-workbench/pull/615))

### OpenSearch Dashboards Reporting

* Update brace-expansion to 1.1.21/2.1.7 and dompurify to 3.4.17 to address CVEs ([#831](https://github.com/opensearch-project/dashboards-reporting/pull/831))

### OpenSearch Flow Framework

* Deprecate `filter_by_backend_roles` setting, targeting removal in 4.0 in favor of security plugin resource sharing ([#1490](https://github.com/opensearch-project/flow-framework/pull/1490))

### OpenSearch Query Insights Dashboards

* Update brace-expansion dependency from 1.1.18 to 1.1.21 to address reported CVEs ([#604](https://github.com/opensearch-project/query-insights-dashboards/pull/604))

### OpenSearch Reporting

* Bump jsoup to 1.23.2 to address CVE-2026-75140 ([#1239](https://github.com/opensearch-project/reporting/pull/1239))

### OpenSearch Search Relevance

* Bump actions/download-artifact from 8.0.1 to 8.0.2 ([#614](https://github.com/opensearch-project/search-relevance/pull/614))
* Bump actions/setup-java from 6.0.0 to 6.0.1 ([#587](https://github.com/opensearch-project/search-relevance/pull/587))
* Bump actions/setup-java from 6.0.1 to 6.1.0 ([#626](https://github.com/opensearch-project/search-relevance/pull/626))
* Bump actions/upload-artifact from 7.0.1 to 7.0.2 ([#616](https://github.com/opensearch-project/search-relevance/pull/616))
* Bump aws-actions/configure-aws-credentials from 6.2.4 to 6.3.0 ([#594](https://github.com/opensearch-project/search-relevance/pull/594))
* Bump codecov/codecov-action from 7.0.0 to 7.1.1 ([#595](https://github.com/opensearch-project/search-relevance/pull/595))
* Bump com.diffplug.spotless:spotless-plugin-gradle from 8.10.2 to 8.10.4 ([#615](https://github.com/opensearch-project/search-relevance/pull/615))
* Bump com.google.errorprone:error\_prone\_annotations from 2.50.0 to 2.51.0 ([#631](https://github.com/opensearch-project/search-relevance/pull/631))
* Bump com.google.guava:guava from 33.7.1-jre to 33.7.2-jre ([#611](https://github.com/opensearch-project/search-relevance/pull/611))
* Bump de.thetaphi:forbiddenapis from 3.10 to 3.11 ([#606](https://github.com/opensearch-project/search-relevance/pull/606))
* Bump gradle-wrapper from 9.7.1 to 9.8.0 ([#605](https://github.com/opensearch-project/search-relevance/pull/605))
* Bump gradle-wrapper from 9.8.0 to 9.8.1 ([#617](https://github.com/opensearch-project/search-relevance/pull/617))
* Bump gradle-wrapper from 9.8.1 to 9.8.2 ([#632](https://github.com/opensearch-project/search-relevance/pull/632))
* Bump io.freefair.gradle:lombok-plugin from 9.5.0 to 9.8.0 ([#608](https://github.com/opensearch-project/search-relevance/pull/608))
* Bump io.freefair.gradle:lombok-plugin from 9.8.0 to 9.8.2 ([#625](https://github.com/opensearch-project/search-relevance/pull/625))

### OpenSearch Security Analytics

* Retrieve jackson-databind version from core ([#1819](https://github.com/opensearch-project/security-analytics/pull/1819))
* Bump jackson-databind to 2.18.8 to remediate five CVEs ([#1828](https://github.com/opensearch-project/security-analytics/pull/1828))

### OpenSearch Security Analytics Dashboards Plugin

* Bump qs to 6.16.0 to address CVE-2026-82562 ([#1580](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1580))
* Update brace-expansion, browserslist, moment, and qs to address CVEs ([#1595](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1595))

### OpenSearch Security Dashboards Plugin

* Bump `actions/setup-java` from 6.0.1 to 6.1.0 ([#2568](https://github.com/opensearch-project/security-dashboards-plugin/pull/2568))
* Bump `codecov/codecov-action` from 6.0.1 to 7.1.1 ([#2532](https://github.com/opensearch-project/security-dashboards-plugin/pull/2532))
* Bump `opensearch-project/opensearch-build/.github/actions/setup-opensearch-dashboards` to 350f76b ([#2573](https://github.com/opensearch-project/security-dashboards-plugin/pull/2573))
* Update `opensearch-project/opensearch-build/.github/actions/start-opensearch` to 350f76b ([#2574](https://github.com/opensearch-project/security-dashboards-plugin/pull/2574))
* Bump `basic-ftp` to 6.2.3 to address dependency check findings ([#2577](https://github.com/opensearch-project/security-dashboards-plugin/pull/2577))
* Bump `node-forge` to 1.4.3 to address CVE-2026-85393 ([#2597](https://github.com/opensearch-project/security-dashboards-plugin/pull/2597))
* Update `brace-expansion` to 1.1.21 and `ip-address` to 10.7.4 to address CVEs ([#2561](https://github.com/opensearch-project/security-dashboards-plugin/pull/2561))

### OpenSearch Skills

* Bump jsoup to 1.23.2 to address CVE-2026-75140 ([#811](https://github.com/opensearch-project/skills/pull/811))

### OpenSearch User Behavior Insights

* Update jackson-databind license SHA to version 3.2.4 ([#215](https://github.com/opensearch-project/user-behavior-insights/pull/215))

### SQL

* Bump Guava from 33.3.0-jre to 33.7.2-jre to address CVE-2026-102554 ([#5918](https://github.com/opensearch-project/sql/pull/5918))
* Fix flaky `CalciteFlattenCommandIT.testFlattenNullField` under non-Latin locales ([#5793](https://github.com/opensearch-project/sql/pull/5793))
* Remove the opt-in partial-result mode for mapping conflicts ([#5814](https://github.com/opensearch-project/sql/pull/5814))

## REFACTORING

### OpenSearch Dashboards Search Relevance

* Reduce O(n²) result matching in VisualComparison by replacing repeated array scans with precomputed ID lookup maps ([#910](https://github.com/opensearch-project/dashboards-search-relevance/pull/910))