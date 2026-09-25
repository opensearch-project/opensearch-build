# OpenSearch and OpenSearch Dashboards 3.9.0 Release Notes

## FEATURES

### OpenSearch Alerting

* Onboard Alerting plugin to centralized resource authorization ([#2180](https://github.com/opensearch-project/alerting/pull/2180))

### OpenSearch Alerting Dashboards Plugin

* Integrate centralized resource-sharing share button for monitors and workflows ([#1496](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1496))

### OpenSearch Anomaly Detection Dashboards Plugin

* Add centralized resource-sharing share button for anomaly detectors and forecasters ([#1238](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1238))

### OpenSearch Dashboards Assistant

* Add configurable `assistant.chat.traceMaxResults` setting to control the number of agent trace steps returned ([#730](https://github.com/opensearch-project/dashboards-assistant/pull/730))

### OpenSearch Dashboards Flow Framework

* Integrate centralized resource-sharing share button for workflows ([#909](https://github.com/opensearch-project/dashboards-flow-framework/pull/909))

### OpenSearch Dashboards Notifications

* Integrate centralized resource-sharing share button for notification configs ([#479](https://github.com/opensearch-project/dashboards-notifications/pull/479))
* Show notification channel management in observability workspaces ([#488](https://github.com/opensearch-project/dashboards-notifications/pull/488))

### OpenSearch Dashboards Observability

* Add APM setup wizard for one-click onboarding, replacing manual dataset and configuration wiring ([#2805](https://github.com/opensearch-project/dashboards-observability/pull/2805))
* Add correlated dashboards support to APM services and topology map nodes (experimental) ([#2892](https://github.com/opensearch-project/dashboards-observability/pull/2892))
* Add generic error classification and surfacing layer with stable categories, redaction, and correlation ids ([#2819](https://github.com/opensearch-project/dashboards-observability/pull/2819))

### OpenSearch Dashboards Query Workbench

* Support single-version OSD Query Workbench against Elasticsearch and OpenDistro backends ([#600](https://github.com/opensearch-project/dashboards-query-workbench/pull/600))

### OpenSearch Dashboards Reporting

* Integrate centralized resource-sharing share button for report definitions ([#792](https://github.com/opensearch-project/dashboards-reporting/pull/792))

### OpenSearch Dashboards Search Relevance

* Add reuse existing judgments and retry failed documents to LLM judgment UI ([#916](https://github.com/opensearch-project/dashboards-search-relevance/pull/916))

### OpenSearch Index Management

* Add opt-in setting to allow ISM actions to run on a red cluster, enabling recovery-oriented actions like delete while restricting resource-intensive operations ([#1691](https://github.com/opensearch-project/index-management/pull/1691))
* Publish finalized field-domain metadata from ISM for managed write-blocked indices to enhance search shard pruning ([#1719](https://github.com/opensearch-project/index-management/pull/1719))

### OpenSearch Index Management Dashboards Plugin

* Add dashboard support for the `convert_index_to_remote` action, including options for `include_aliases`, `ignore_index_settings`, `number_of_replicas`, `delete_original_index`, and `rename_pattern` ([#1373](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1373))

### OpenSearch ML Commons

* Add CRUD API for agentic search templates ([#4945](https://github.com/opensearch-project/ml-commons/pull/4945))
* Add agentic search template param-schema derivation from Mustache template bodies ([#4944](https://github.com/opensearch-project/ml-commons/pull/4944))
* Add optional user-specified custom IDs for ML resources (models, connectors, agents, model groups, memory containers) ([#4974](https://github.com/opensearch-project/ml-commons/pull/4974))
* Add server-side cross-request batch inference queue for the online predict path ([#4996](https://github.com/opensearch-project/ml-commons/pull/4996))
* Add server-side size-based batch inference splitting for ingest predict requests ([#4898](https://github.com/opensearch-project/ml-commons/pull/4898))
* Add structural enrichment of agentic search template param-schemas with descriptions and enums at register time ([#4982](https://github.com/opensearch-project/ml-commons/pull/4982))
* Add client certificate (mutual TLS) authentication support for ML connectors ([#4731](https://github.com/opensearch-project/ml-commons/pull/4731))
* Add GCP Vertex AI connector with automatic OAuth2 token management via `google_cloud` auth strategy ([#4921](https://github.com/opensearch-project/ml-commons/pull/4921))
* Add on-demand memory retention execution and support for self-hosted multi-tenancy ([#4973](https://github.com/opensearch-project/ml-commons/pull/4973))
* Add dynamic retention job interval updates and dry-run API for memory retention ([#4952](https://github.com/opensearch-project/ml-commons/pull/4952))
* Enable unified agent API by default ([#4951](https://github.com/opensearch-project/ml-commons/pull/4951))

### OpenSearch Neural Search

* Add `model_selection` parameter to semantic field to resolve model ID from operator-configured cluster settings instead of requiring an explicit `model_id` ([#1919](https://github.com/opensearch-project/neural-search/pull/1919))
* Add JNI bridge layer for the native sparse ANN engine (neural-sparse-cpp) with CMake/Gradle build wiring ([#1972](https://github.com/opensearch-project/neural-search/pull/1972))
* Wire the native sparse engine into the plugin with codec, query, mapper, and feature-flag support ([#1974](https://github.com/opensearch-project/neural-search/pull/1974))
* Ship native sparse engine SIMD variants and OpenMP runtime in the distribution build with CPU feature detection ([#1978](https://github.com/opensearch-project/neural-search/pull/1978))
* Report sparse vector field adoption counts (indices, fields, native vs. lucene engine) as neural info stats ([#1996](https://github.com/opensearch-project/neural-search/pull/1996))

### OpenSearch Notifications

* Onboard notifications plugin to centralized resource authorization ([#1237](https://github.com/opensearch-project/notifications/pull/1237))

### OpenSearch Query Insights Dashboards

* Add toggle to hide remote repository registration in the configuration page ([#576](https://github.com/opensearch-project/query-insights-dashboards/pull/576))

### OpenSearch Search Relevance

* Add retry endpoint for failed judgments, `existingJudgements` parameter for reusing prior ratings, and remove global judgment cache ([#528](https://github.com/opensearch-project/search-relevance/pull/528))

### OpenSearch Security

* Enable standalone audit logging when security is fully disabled (`plugins.security.disabled: true`) for compliance without TLS or authentication ([#6341](https://github.com/opensearch-project/security/pull/6341))
* Add `audit_request_id` correlation field to all audit events for cross-event request tracing ([#6343](https://github.com/opensearch-project/security/pull/6343))
* Add `user_agent`, `user_roles`, and `auth_method` fields to audit events for improved investigability ([#6344](https://github.com/opensearch-project/security/pull/6344))
* Add API path filtering for request body logging in audit events to reduce log volume for high-throughput actions ([#6347](https://github.com/opensearch-project/security/pull/6347))
* Enrich Log4j MDC with audit event attributes to enable native log routing by category, user, or action ([#6349](https://github.com/opensearch-project/security/pull/6349))
* Add audit logging for resource sharing authorization events with dedicated categories for access granted, denied, and sharing changes ([#6352](https://github.com/opensearch-project/security/pull/6352))
* Add workspace-aware sharing records so resource visibility can be driven by workspace membership ([#6374](https://github.com/opensearch-project/security/pull/6374))
* Support request header attributes as substitutions in document-level security queries ([#6310](https://github.com/opensearch-project/security/pull/6310))
* Support wildcard matching in WLM principal username and role auto-tagging rules ([#6324](https://github.com/opensearch-project/security/pull/6324))
* Support multiple `ResourceProvider` registrations per shared resource index ([#6323](https://github.com/opensearch-project/security/pull/6323))

### OpenSearch Security Analytics

* Onboard security-analytics plugin to centralized resource authorization ([#1735](https://github.com/opensearch-project/security-analytics/pull/1735))
* Register detector and correlation-rule indices as system indices for resource-sharing framework support ([#1749](https://github.com/opensearch-project/security-analytics/pull/1749))

### OpenSearch Security Dashboards Plugin

* Add centralized embeddable share button for resource-sharing consumer plugins ([#2491](https://github.com/opensearch-project/security-dashboards-plugin/pull/2491))
* Expose per-data-source resource-sharing availability check via the SPI ([#2520](https://github.com/opensearch-project/security-dashboards-plugin/pull/2520))

### OpenSearch k-NN

* Add `half_float` as a vector data type for Flat and HNSW ([#3578](https://github.com/opensearch-project/k-NN/pull/3578))
* Enable `half_float` vector data type for remote vector index build ([#3575](https://github.com/opensearch-project/k-NN/pull/3575))
* Add Intel SVS (Scalable Vector Search) as a sandbox tenant engine with svs\_vamana method, flat/sq/lvq/leanvec encoders, and query-time parameters ([#3551](https://github.com/opensearch-project/k-NN/pull/3551))
* Add multi-bit scalar quantization (2-bit and 4-bit) for Faiss, and make flat method engine-agnostic with x16/x8 support ([#3544](https://github.com/opensearch-project/k-NN/pull/3544))
* Add radial search method that applies post-filtering on quantized indices using size × oversample\_factor top-K ([#3491](https://github.com/opensearch-project/k-NN/pull/3491))
* Introduce resolved index spec for centralized index configuration resolution ([#3499](https://github.com/opensearch-project/k-NN/pull/3499))
* Support `index.knn.advanced.approximate_threshold` for the Lucene engine to control HNSW graph construction ([#3451](https://github.com/opensearch-project/k-NN/pull/3451))
* Add BF16 scalar quantization support for FAISS-backed k-NN indices. ([#3190](https://github.com/opensearch-project/k-NN/pull/3190)))

### SQL

* Add SQL `histogram` and `date_histogram` bucket functions ([#5700](https://github.com/opensearch-project/sql/pull/5700))
* Add a generic, extensible REST endpoint provider SPI for the PPL `rest` command ([#5656](https://github.com/opensearch-project/sql/pull/5656))
* Add `include_metadata` request parameter for PPL queries to include `_id`, `_index`, `_score`, and other metadata fields ([#5412](https://github.com/opensearch-project/sql/pull/5412))
* Add `percentfield` and `showperc` options to `top` and `rare` PPL commands ([#5642](https://github.com/opensearch-project/sql/pull/5642))
* Support `RANK()` and `DENSE_RANK()` window functions in unified SQL ([#5720](https://github.com/opensearch-project/sql/pull/5720))
* Support `UNION` (distinct) for unified SQL on the analytics-engine route ([#5741](https://github.com/opensearch-project/sql/pull/5741))
* Add a dedicated thread pool for complex/slow PPL queries to keep the cluster responsive ([#5628](https://github.com/opensearch-project/sql/pull/5628))

## ENHANCEMENTS

### OpenSearch Common Utils

* Override `DocRequest.type()` on alerting request classes and tolerate ancillary top-level fields in `ScheduledJob.parse` for resource-sharing framework support ([#981](https://github.com/opensearch-project/common-utils/pull/981))

### OpenSearch Dashboards Flow Framework

* Gate resource-sharing Access column on per-data-source availability ([#914](https://github.com/opensearch-project/dashboards-flow-framework/pull/914))

### OpenSearch Dashboards Observability

* Add detector and forecaster management to Alerts Manager for anomaly detection and forecasting rules ([#2804](https://github.com/opensearch-project/dashboards-observability/pull/2804))
* Add classic-experience escape hatches for unsupported monitor types in the alerting UI ([#2823](https://github.com/opensearch-project/dashboards-observability/pull/2823))
* Improve Alerts Manager empty state with capability cards for Alerting, Anomaly Detection, and Forecasting ([#2822](https://github.com/opensearch-project/dashboards-observability/pull/2822))
* Stop clamping pre-window alerts into bucket 0 on the alerts timeline and label the y-axis ([#2828](https://github.com/opensearch-project/dashboards-observability/pull/2828))
* Align forecaster edit gate with the shared running-state predicate and humanize update errors ([#2837](https://github.com/opensearch-project/dashboards-observability/pull/2837))
* Add shared alerting primitives for i18n enum labels, timezone-aware timestamps, and theme color tokens ([#2826](https://github.com/opensearch-project/dashboards-observability/pull/2826))
* Surface unified-alerts errors as toasts with per-datasource indicators in the filter facet ([#2820](https://github.com/opensearch-project/dashboards-observability/pull/2820))
* Unify Create metrics rule flyouts across Alert Manager and Metrics page into a single shared component ([#2817](https://github.com/opensearch-project/dashboards-observability/pull/2817))
* Add SLO onboarding empty state with services-aware suggestions, toolbar button, and tidier catalog rows ([#2821](https://github.com/opensearch-project/dashboards-observability/pull/2821))
* Add SLO edit path with wizard prefill and update support ([#2838](https://github.com/opensearch-project/dashboards-observability/pull/2838))
* Improve SLO detail page with header layout fix, not-found state, rule health re-poll, and View alerts pivot ([#2831](https://github.com/opensearch-project/dashboards-observability/pull/2831))
* Humanize SLO listing state labels, stabilize numeric formatting, fix paginated sort, and add skeleton rows ([#2830](https://github.com/opensearch-project/dashboards-observability/pull/2830))
* Localize SLO percent formatting and make SLO\_PRECISION the single precision policy ([#2836](https://github.com/opensearch-project/dashboards-observability/pull/2836))
* Make SLO overview firing/breached tiles consistent, clamp budget hero at 0, and improve KPI accessibility ([#2833](https://github.com/opensearch-project/dashboards-observability/pull/2833))
* Remove nested interactive controls, enforce minimum 24px touch targets, and add aria-expanded to tree controls ([#2834](https://github.com/opensearch-project/dashboards-observability/pull/2834))
* Refine correlated dashboards flyout table caption to match spans/logs tab descriptions ([#2893](https://github.com/opensearch-project/dashboards-observability/pull/2893))
* Copy Explore PromQL query into metrics rule flyout with real range-query preview ([#2862](https://github.com/opensearch-project/dashboards-observability/pull/2862))
* Add optimistic pending-rule cache so newly created Prometheus rules appear immediately in the rules list ([#2866](https://github.com/opensearch-project/dashboards-observability/pull/2866))
* Add point-and-click PromQL condition builder with lossless Builder/Code round-trip for metric rules ([#2870](https://github.com/opensearch-project/dashboards-observability/pull/2870))
* Redesign Prometheus rule creation flyout with Builder/Code toggle, rule group configuration, and safe group merging ([#2796](https://github.com/opensearch-project/dashboards-observability/pull/2796))

### OpenSearch Dashboards Query Workbench

* Add single-version OSD capability gating for query workbench to support OpenSearch backends from 1.3.2 through 3.x ([#586](https://github.com/opensearch-project/dashboards-query-workbench/pull/586))

### OpenSearch ML Commons Dashboards

* Integrate centralized resource-sharing share button for model groups via DOM-marker SPI ([#512](https://github.com/opensearch-project/ml-commons-dashboards/pull/512))
* Gate resource-sharing Access column on per-data-source availability instead of local capability check ([#517](https://github.com/opensearch-project/ml-commons-dashboards/pull/517))

### OpenSearch Neural Search

* Add conversion from `heap_factor` query parameter to native engine `k_prime` block budget for disk-based sparse indexes ([#1997](https://github.com/opensearch-project/neural-search/pull/1997))
* Add support for 64-bit CSR forward-index offsets in the native sparse engine, allowing single segments with more than 2.1 billion non-zeros ([#2001](https://github.com/opensearch-project/neural-search/pull/2001))
* Expose neural query embedded filters to `QueryBuilderVisitor` traversal for cross-plugin compatibility ([#1992](https://github.com/opensearch-project/neural-search/pull/1992))
* Reject unsupported combination techniques (e.g., `arithmetic_mean`) in the score-ranker-processor at pipeline creation time instead of failing with a `NullPointerException` at search time ([#1949](https://github.com/opensearch-project/neural-search/pull/1949))

### OpenSearch OpenSearch Learning To Rank Base

* Add model-level `missing_as_zero` flag for XGBoost ranker ([#389](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/389))
* Make `ltr.caches.max_mem` a dynamic setting and scale its default with heap size ([#397](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/397))

### OpenSearch Query Insights Dashboards

* Disable username and role inputs in WLM rule forms when the Security plugin is unavailable ([#533](https://github.com/opensearch-project/query-insights-dashboards/pull/533))

### OpenSearch Search Relevance

* Replace scheduled job sleep with polling for test results ([#340](https://github.com/opensearch-project/search-relevance/pull/340))
* Exclude vector fields from LLM judgment prompts when `contextFields` is unset to avoid wasting tokens on embeddings ([#565](https://github.com/opensearch-project/search-relevance/pull/565))
* Stop re-fetching judgment documents on every query for Hybrid and Pointwise experiments ([#560](https://github.com/opensearch-project/search-relevance/pull/560))

### OpenSearch Security

* Graduate resource sharing feature out of experimental, renaming settings to drop the `.experimental` segment ([#6348](https://github.com/opensearch-project/security/pull/6348))
* Keep the pre-graduation resource sharing setting names working, deprecated ([#6513](https://github.com/opensearch-project/security/pull/6513))
* Add setting to ignore source cluster security roles on cross-cluster search requests for independent remote access control ([#6402](https://github.com/opensearch-project/security/pull/6402))
* Allow standalone granular REST API permissions without requiring `roles_enabled` membership ([#6493](https://github.com/opensearch-project/security/pull/6493))
* Add missing index actions (`point_in_time/create`, `point_in_time/delete`, `resolve/index`, `field_caps*`) to `ppl_full_access` role ([#6471](https://github.com/opensearch-project/security/pull/6471))
* Expose dynamic audit configuration via cluster settings in SSL-only mode so the dashboards plugin can read current state ([#6392](https://github.com/opensearch-project/security/pull/6392))
* Create parent-linked sharing entries for child resources written without an authenticated user context ([#6373](https://github.com/opensearch-project/security/pull/6373))
* Support neural and k-NN queries with hybrid document-level security ([#6428](https://github.com/opensearch-project/security/pull/6428))
* Keep hybrid DLS safe across mixed-version clusters by replacing the sentinel value with a dedicated header ([#6451](https://github.com/opensearch-project/security/pull/6451))
* Copy security tools scripts to `bin/` directory in assembly to preserve executable permissions after plugin installation ([#6023](https://github.com/opensearch-project/security/pull/6023))
* Reject JWT subjects that use reserved internal `plugin:` or API-token `token:` prefixes ([#6494](https://github.com/opensearch-project/security/pull/6494))
* Preserve authentication for self-referential cross-cluster search connections ([#6474](https://github.com/opensearch-project/security/pull/6474))
* Retry API token metadata loading during startup when cluster is temporarily blocked or master not yet discovered ([#6472](https://github.com/opensearch-project/security/pull/6472))
* Return HTTP 403 when API tokens feature is disabled instead of allowing unusable token creation ([#6351](https://github.com/opensearch-project/security/pull/6351))
* Use `User` directly as authenticated `Subject` and `Principal`, removing the redundant `UserSubjectImpl` wrapper ([#6419](https://github.com/opensearch-project/security/pull/6419))

### OpenSearch Skills

* Add input schema to SearchAlertsTool for improved parameter discovery ([#769](https://github.com/opensearch-project/skills/pull/769))

### OpenSearch k-NN

* Add NEON SIMD kernel for FP16 L2 similarity with ~20% throughput improvement on ARM Graviton3 ([#3512](https://github.com/opensearch-project/k-NN/pull/3512))
* Add native SIMD cosine scoring for FP16 and SQ formats, eliminating post-hoc score conversion in the memory-optimized search path ([#3386](https://github.com/opensearch-project/k-NN/pull/3386))
* Add memory prefetching for Lucene engine's fp32 and binary vector HNSW query-scoring path to reduce cache-miss stalls ([#3504](https://github.com/opensearch-project/k-NN/pull/3504))
* Enable approximate graph threshold for Faiss SQ x32 to allow skipping HNSW graph construction for small segments ([#3434](https://github.com/opensearch-project/k-NN/pull/3434))
* Move document vector conversion out of the query-vector loop in late interaction scoring, significantly reducing allocations for ColBERT-style workloads ([#3453](https://github.com/opensearch-project/k-NN/pull/3453))
* Flip default compression for 16x and 8x to SQ 2-bit and 4-bit respectively ([#3561](https://github.com/opensearch-project/k-NN/pull/3561))
* Terminate remote index build early when the associated merge is aborted ([#3488](https://github.com/opensearch-project/k-NN/pull/3488))
* Skip warmup on warm indices since data is fetched on demand from remote store ([#3565](https://github.com/opensearch-project/k-NN/pull/3565))
* Add configurable nproc count to native library build script for parallel compilation ([#3539](https://github.com/opensearch-project/k-NN/pull/3539))

### SQL

* Add opt-in partial-result mode for aggregations on text/keyword mapping conflicts, returning fast partial answers with warnings instead of slow full scans ([#5657](https://github.com/opensearch-project/sql/pull/5657))
* Avoid PIT context exhaustion by pruning indices that cannot match the query's time range before opening a PIT ([#5727](https://github.com/opensearch-project/sql/pull/5727))
* Enable index pruning (`plugins.query.pruning.enabled`) by default ([#5759](https://github.com/opensearch-project/sql/pull/5759))
* Surface PIT-context exhaustion with an actionable error message naming the `search.max_open_pit_context` setting and remediation steps ([#5631](https://github.com/opensearch-project/sql/pull/5631))
* Map Calcite `ROW` type to `STRUCT` so analytics-engine object fields report the correct type instead of `unknown` ([#5737](https://github.com/opensearch-project/sql/pull/5737))
* Type nested field access as the field's own type instead of the whole row, fixing `Unsupported conversion for Relational Data type: ROW` on the analytics engine ([#5764](https://github.com/opensearch-project/sql/pull/5764))
* Override the `profile` endpoint with an `analyze` endpoint providing operator tree and rule-based query optimization recommendations ([#5568](https://github.com/opensearch-project/sql/pull/5568))
* Clean up the `analyze` endpoint response and add rule-based recommendations ([#5658](https://github.com/opensearch-project/sql/pull/5658))
* Register missing `TAN` function for the Calcite and analytics-engine paths ([#5717](https://github.com/opensearch-project/sql/pull/5717))
* Add structural limits (`maxdepth`, `maxrefs`, `maxbytes`) for the deserialization filter, configurable via dynamic cluster settings ([#5721](https://github.com/opensearch-project/sql/pull/5721))
* Forward cluster planning settings (e.g. `plugins.query.size_limit`, pattern settings) to the analytics-engine unified query path ([#5611](https://github.com/opensearch-project/sql/pull/5611))
* Reject object and array fields in `timechart`/`chart` split and `cast` expressions with a clear 400 error instead of a 500 plan dump ([#5751](https://github.com/opensearch-project/sql/pull/5751))
* Add PPL OpenTelemetry tracing integration across the Calcite query execution pipeline ([#5708](https://github.com/opensearch-project/sql/pull/5708))
* Push down aggregation on text fields without a `.keyword` sub-field using a Calcite script that reads from `_source` ([#5646](https://github.com/opensearch-project/sql/pull/5646))

## BUG FIXES

### OpenSearch Alerting

* Apply Index Monitor API input validation to the Execute Monitor API ([#2225](https://github.com/opensearch-project/alerting/pull/2225))

### OpenSearch Alerting Dashboards Plugin

* Accept v1-shape monitor body in PPL update guard and toV1MonitorBody to prevent query loss on enable/disable toggle ([#1505](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1505))
* Fix empty notification channels and Alerts view for local cluster when Multi-Data-Source is enabled ([#1511](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1511))
* Use sliding lookback window instead of frozen absolute timestamps for PPL monitors and fix query preview on monitor edit ([#1501](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1501))
* Fix test notifications for PPL monitors and prevent silent erasure of PPL query on monitor updates ([#1500](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1500))
* Prevent auto-running monitor preview query before index and time field are set on create monitor page ([#1499](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1499))

### OpenSearch Common Utils

* Fix `ScheduledJob.parse` type overload broken by shared-parse refactor, restoring correct parser position handling for the sweeper path ([#984](https://github.com/opensearch-project/common-utils/pull/984))
* Align `WORKFLOW_RESOURCE_TYPE` constant with alerting's registered resource type (`alerting-workflow`) to ensure proper security gating of workflow requests ([#1003](https://github.com/opensearch-project/common-utils/pull/1003))

### OpenSearch Cross Cluster Replication

* Fix replication stall when dynamic batch-size reduction was not applied to replayed (missing) batches, causing follower checkpoint to wedge under parallel readers ([#1746](https://github.com/opensearch-project/cross-cluster-replication/pull/1746))
* Fix data loss during bootstrap when in-flight writes caused sequence number gaps that were incorrectly filled with no-ops by the replication engine ([#1735](https://github.com/opensearch-project/cross-cluster-replication/pull/1735))
* Fix `removeStaleTasksForIndex` incorrectly deleting actively-running replication tasks when a transient `ListTasks` query failure was treated as "no tasks running" ([#1725](https://github.com/opensearch-project/cross-cluster-replication/pull/1725))
* Fix stop replication failing for restored follower indices that carry replication settings but lack a metadata document, leaving the index in a partially mutated state ([#1740](https://github.com/opensearch-project/cross-cluster-replication/pull/1740))
* Make autofollow pattern REMOVE idempotent so that double-removes or retries after partial removal no longer fail or orphan pattern metadata ([#1739](https://github.com/opensearch-project/cross-cluster-replication/pull/1739))
* Version-gate `FailedState` `errorMsg` serialization to prevent stream corruption during mixed-cluster rolling upgrades between pre-3.7 and 3.7+ nodes ([#1749](https://github.com/opensearch-project/cross-cluster-replication/pull/1749))

### OpenSearch Dashboards Assistant

* Remove manual sidecar CSS patch for flyout and bottom bar, deferring to global overlay-offset CSS variables ([#715](https://github.com/opensearch-project/dashboards-assistant/pull/715))

### OpenSearch Dashboards Investigation

* Fix unbounded notebook bulk-delete to prevent event-loop exhaustion by capping input size and using Set-based filtering ([#415](https://github.com/opensearch-project/dashboards-investigation/pull/415))
* Remove manual sidecar padding hack from flyouts in favor of global overlay-offset CSS variables ([#401](https://github.com/opensearch-project/dashboards-investigation/pull/401))

### OpenSearch Dashboards Maps

* Fix basemap rendering above document layers by enforcing layer order after late tile loads ([#860](https://github.com/opensearch-project/dashboards-maps/pull/860))

### OpenSearch Dashboards Notifications

* Guard the Access column against a data-source staleness race ([#487](https://github.com/opensearch-project/dashboards-notifications/pull/487))

### OpenSearch Dashboards Observability

* Harden APM Services, Overview, Operations, Dependencies, and Topology pages for high cardinality at scale ([#2860](https://github.com/opensearch-project/dashboards-observability/pull/2860))
* Consolidate unified-alerting accessibility, theme, and i18n fixes for alerts list, flyout, and rules table ([#2879](https://github.com/opensearch-project/dashboards-observability/pull/2879))
* Fix SLO listing filters, workspace-scoped coverage, and extract shared TruncatedLabel component ([#2810](https://github.com/opensearch-project/dashboards-observability/pull/2810))
* Remove broken Maximize panel action on notebook visualizations ([#2824](https://github.com/opensearch-project/dashboards-observability/pull/2824))
* Fix clone and edit of monitors in the unified Alerts view, including cluster-metrics and per-bucket types ([#2871](https://github.com/opensearch-project/dashboards-observability/pull/2871))
* Add Builder/Code toggle and overwrite guard to the Prometheus edit flyout to prevent silent expression data loss ([#2882](https://github.com/opensearch-project/dashboards-observability/pull/2882))
* Fix clone and edit from corrupting Prometheus rule expressions and silently overwriting rules ([#2877](https://github.com/opensearch-project/dashboards-observability/pull/2877))
* Left-align facet filter titles and keep group count inline ([#2885](https://github.com/opensearch-project/dashboards-observability/pull/2885))
* Fix correlated logs and spans filters to search all results instead of only the visible page ([#2891](https://github.com/opensearch-project/dashboards-observability/pull/2891))
* Fix service detail tables re-rendering and re-fetching charts on latency percentile switch ([#2842](https://github.com/opensearch-project/dashboards-observability/pull/2842))
* Exclude exponentiation-operator Babel transform to fix BigInt test failures ([#2802](https://github.com/opensearch-project/dashboards-observability/pull/2802))
* Fix Trace Analytics dashboard latencyTrends request using wrong data source on external clusters ([#2803](https://github.com/opensearch-project/dashboards-observability/pull/2803))
* Fix notification channel picker not loading channels by using the correct notifications API route ([#2848](https://github.com/opensearch-project/dashboards-observability/pull/2848))
* Tolerate text/plain wrapped empty-namespace 404 on first Prometheus rule creation ([#2884](https://github.com/opensearch-project/dashboards-observability/pull/2884))
* Bind sample notebook paragraphs to the data source selected in the modal ([#2865](https://github.com/opensearch-project/dashboards-observability/pull/2865))
* Fix sample notebook visualizations failing to render due to literal "undefined" saved object id ([#2861](https://github.com/opensearch-project/dashboards-observability/pull/2861))
* Fix duplicated Observability Dashboard sharing the original's id, preventing deletion ([#2869](https://github.com/opensearch-project/dashboards-observability/pull/2869))
* Preserve table page across latency percentile switch in APM Operations and Dependencies ([#2851](https://github.com/opensearch-project/dashboards-observability/pull/2851))

### OpenSearch Dashboards Query Workbench

* Fix TS5011 compilation error in Cypress E2E tests by setting rootDir explicitly ([#579](https://github.com/opensearch-project/dashboards-query-workbench/pull/579))

### OpenSearch Dashboards Reporting

* Guard the Access column against a data-source staleness race during data-source switches ([#808](https://github.com/opensearch-project/dashboards-reporting/pull/808))

### OpenSearch Dashboards Search Relevance

* Surface specific error messages when deleting query sets, judgments, or search configurations that are in use ([#926](https://github.com/opensearch-project/dashboards-search-relevance/pull/926))
* Fix search configuration validation always reporting no results on multi-data-source deployments ([#926](https://github.com/opensearch-project/dashboards-search-relevance/pull/926))
* Fix experiment visualization deep-dive and dashboard install detection on multi-data-source deployments ([#926](https://github.com/opensearch-project/dashboards-search-relevance/pull/926))
* Fix listing search cache so clearing the search box restores full results instead of showing stale filtered data ([#933](https://github.com/opensearch-project/dashboards-search-relevance/pull/933))
* Gate workbench on data source readiness and warn when the selected data source lacks the Search Relevance plugin ([#940](https://github.com/opensearch-project/dashboards-search-relevance/pull/940))
* Pass dataSourceId in Hybrid Optimizer and Pairwise experiment result queries on multi-data-source deployments ([#921](https://github.com/opensearch-project/dashboards-search-relevance/pull/921))
* Scope experiment result dashboards to the active workspace so each workspace gets independent copies ([#928](https://github.com/opensearch-project/dashboards-search-relevance/pull/928))
* Scope search configuration dropdown to the selected data source in Query Analysis setup ([#923](https://github.com/opensearch-project/dashboards-search-relevance/pull/923))
* Show clear validation error when UBI events data is unavailable for the COEC click model in judgment creation ([#923](https://github.com/opensearch-project/dashboards-search-relevance/pull/923))

### OpenSearch Flow Framework

* Declare workflow\_state as a child resource of workflow so state documents inherit access from their parent workflow ([#1455](https://github.com/opensearch-project/flow-framework/pull/1455))

### OpenSearch Index Management

* Allow mixed raw and rollup search to succeed when a queried field is missing from the rollup index ([#1712](https://github.com/opensearch-project/index-management/pull/1712))

### OpenSearch ML Commons

* Fix TEXT\_SIMILARITY ONNX inference failure for cross-encoder models without `token_type_ids` input ([#4946](https://github.com/opensearch-project/ml-commons/pull/4946))
* Fix deletion and management of remote models stored without `additional_config` ([#5000](https://github.com/opensearch-project/ml-commons/pull/5000))
* Fix false-positive ReDoS rejection of safe connector endpoint regex patterns ([#4972](https://github.com/opensearch-project/ml-commons/pull/4972))
* Fix models stuck in DEPLOYING state when a single model document fails to parse during sync-up ([#5012](https://github.com/opensearch-project/ml-commons/pull/5012))
* Fix V1 conversational agent with native function calling leaving unresolved `tool_descriptions`/`tool_names` placeholders ([#4931](https://github.com/opensearch-project/ml-commons/pull/4931))
* Defer `.plugins-ml-jobs` index creation until rolling upgrade completes and gate retention job on `retention_enabled` ([#4937](https://github.com/opensearch-project/ml-commons/pull/4937))
* Use exact-match queries for id-based lookups so removing one MCP tool no longer deletes tools with similar names and connectors with hyphenated ids remain deletable and updatable ([#5034](https://github.com/opensearch-project/ml-commons/pull/5034))
* Require a non-blank name when registering an MCP tool ([#5034](https://github.com/opensearch-project/ml-commons/pull/5034))
* Fix HTTP 500 on model register/deploy against security 3.9+ clusters by avoiding a Jackson 3 self-reference cycle in `isSuperAdminUser` ([#4994](https://github.com/opensearch-project/ml-commons/pull/4994))
* Fail batch inference when a sub-batch result count does not match its item count, and tighten `batch_queue` setting and `batch_inference_config` validation ([#5040](https://github.com/opensearch-project/ml-commons/pull/5040))
* Pin `google_cloud` connector `token_uri` to the default HTTPS port so a signed JWT cannot be sent to a non-default port ([#5041](https://github.com/opensearch-project/ml-commons/pull/5041))
* Reject counted repetition of a quantified group in trusted-endpoint regex validation ([#5042](https://github.com/opensearch-project/ml-commons/pull/5042))
* Delete the auto-created model when unified agent registration fails, instead of leaving an orphaned model holding the request credentials ([#5043](https://github.com/opensearch-project/ml-commons/pull/5043))
* Read the stored script and target index mapping as the calling user when registering an agentic search template ([#5044](https://github.com/opensearch-project/ml-commons/pull/5044))
* Validate connector protocol, opt-in protocol settings, and `mutual_tls_enabled` on connector update, model register with inline connector, and model update — not only on connector create ([#5045](https://github.com/opensearch-project/ml-commons/pull/5045))

### OpenSearch Neural Search

* Fix `SemanticHighlighterExtBuilder.toXContent` to produce the enclosing field name expected by `SearchExtBuilder` ([#1907](https://github.com/opensearch-project/neural-search/pull/1907))
* Fix `NoSuchElementException` in hybrid query when using `search_after` with `sort` and a shard returns no results ([#1939](https://github.com/opensearch-project/neural-search/pull/1939))
* Fix sparse vector token IDs folding into the negative signed-short range, which caused `NegativeArraySizeException` and incorrect scoring ([#1926](https://github.com/opensearch-project/neural-search/pull/1926))
* Skip sparse cache cleanup for closed index shards to prevent reopened indexes from becoming permanently unassigned ([#1983](https://github.com/opensearch-project/neural-search/pull/1983))
* Fix `HybridQueryScorer` reading stale document and sub-match state from a frozen priority queue, which caused wrong per-sub-query scores under profiling, aggregation filters, nested queries, and document-level security ([#1950](https://github.com/opensearch-project/neural-search/pull/1950))

### OpenSearch Notifications

* Fix Dispatchers.IO starvation deadlock in the notification send path that could permanently hang all Notifications APIs under sustained concurrent sends ([#1248](https://github.com/opensearch-project/notifications/pull/1248))
* Fix SES/SNS NoClassDefFoundError caused by Jackson 3 and HttpClient5 migration by restoring required classic Jackson 2 and HttpClient4 dependencies ([#1257](https://github.com/opensearch-project/notifications/pull/1257))
* Fix Microsoft Teams notifications to use Adaptive Card schema (v1.2) and support Logic Apps and Power Automate webhook domains ([#1107](https://github.com/opensearch-project/notifications/pull/1107))

### OpenSearch Observability

* Fix node crash on `GET /_observability/_local/stats` caused by Jackson 2.x classpath mismatch after Jackson 3.x migration ([#2025](https://github.com/opensearch-project/observability/pull/2025))

### OpenSearch Query Insights

* Validate remote exporter base path at settings-validation time to prevent invalid paths from being committed to cluster state ([#661](https://github.com/opensearch-project/query-insights/pull/661))

### OpenSearch Query Insights Dashboards

* Fix Top N Cypress sort assertions that always passed due to incorrect column extraction ([#589](https://github.com/opensearch-project/query-insights-dashboards/pull/589))

### OpenSearch Reporting

* Declare report-instance as child resource of report-definition so scheduled report instances inherit access from their parent definition ([#1213](https://github.com/opensearch-project/reporting/pull/1213))

### OpenSearch Search Relevance

* Return correct HTTP status codes for delete operations and honor `querySetSize` for PPTSS sampling ([#542](https://github.com/opensearch-project/search-relevance/pull/542))
* Report a missing UBI events index as HTTP 400 and name the `ubiEventsIndex` parameter in the error message ([#558](https://github.com/opensearch-project/search-relevance/pull/558))
* Fix transport-thread blocking and unhandled listener failure in async flows ([#559](https://github.com/opensearch-project/search-relevance/pull/559))

### OpenSearch Security

* Fix parent-child query detection across classloaders by matching on registered writeable names instead of `instanceof` ([#6346](https://github.com/opensearch-project/security/pull/6346))
* Fix Apache HttpClient 5.6 hostname verification so `NoopHostnameVerifier` works correctly for SecurityAdmin `-nhnv` and test clients ([#6407](https://github.com/opensearch-project/security/pull/6407))
* Fix Bouncy Castle 1.85.2 upgrade by keeping `bcpkix-jdk18on` and `bcutil-jdk18on` at compatible 1.85 versions ([#6488](https://github.com/opensearch-project/security/pull/6488))
* Fix ML model registration failure caused by Jackson 3 self-referential serialization of `User.getPrincipal()` ([#6460](https://github.com/opensearch-project/security/pull/6460))
* Require explicit opt-in (`enable_standalone: true`) for standalone audit logging to prevent unintended audit index writes from stale demo configuration ([#6368](https://github.com/opensearch-project/security/pull/6368))
* Deduplicate bulk audit events by only iterating sub-items at the `BulkShardRequest` level ([#6390](https://github.com/opensearch-project/security/pull/6390))
* Add missing `enable_standalone` setting to `StandaloneAuditBodyLoggingExclusionTest` to fix deterministic test failures ([#6372](https://github.com/opensearch-project/security/pull/6372))

### OpenSearch Security Analytics

* Fix authorization bypass via stashContext() by adding pre-flight index permission checks and blocking cross-index terms lookup queries ([#1760](https://github.com/opensearch-project/security-analytics/pull/1760))

### OpenSearch Security Dashboards Plugin

* Always start the Share button DOM-marker SPI to fix empty Access columns in multi-data-source deployments ([#2525](https://github.com/opensearch-project/security-dashboards-plugin/pull/2525))

### OpenSearch Skills

* Add null check for mapping properties in PPLTool to prevent NullPointerException on indices with empty mappings ([#773](https://github.com/opensearch-project/skills/pull/773))

### OpenSearch k-NN

* Fix `_source` bloat on merge when derived source is used with `_source.excludes`/`_source.includes` ([#3465](https://github.com/opensearch-project/k-NN/pull/3465))
* Fix derived source ingestion failure for non-JSON (CBOR/SMILE) encoded documents ([#3529](https://github.com/opensearch-project/k-NN/pull/3529))
* Fix dimension-based oversampling not applying for 32x BQ compression when shard-level rescoring is enabled ([#3460](https://github.com/opensearch-project/k-NN/pull/3460))
* Fix exact search scoring with L2 instead of the configured space type for model-based and pre-3.0 Faiss/Nmslib fields ([#3537](https://github.com/opensearch-project/k-NN/pull/3537))
* Fix k-NN query against a field alias silently returning zero hits ([#3485](https://github.com/opensearch-project/k-NN/pull/3485))
* Fix native thread leak in Lucene HNSW merge executor caused by unbounded thread pool accumulation ([#3533](https://github.com/opensearch-project/k-NN/pull/3533))
* Fix shared mutable `PerLeafResult.EMPTY_RESULT` singleton causing NPE across concurrent queries ([#3534](https://github.com/opensearch-project/k-NN/pull/3534))
* Fix `FileNotFoundException` on quantization state file when BQ segment has no live vectors ([#3511](https://github.com/opensearch-project/k-NN/pull/3511))
* Fix SQ flat prefetch reading `.veq` instead of `.vec` by dropping `HasIndexSlice` from `ScalarQuantizedFloatVectorValues` ([#3486](https://github.com/opensearch-project/k-NN/pull/3486))
* Preserve raw non-XContent `_source` fields (e.g., no-op tombstones) when derived source is enabled ([#3402](https://github.com/opensearch-project/k-NN/pull/3402))

### SQL

* Accept plain Calcite types against UDT operand signatures, fixing false type-mismatch errors for `list()`, `values()`, and similar aggregations on date/time/IP/binary fields ([#5675](https://github.com/opensearch-project/sql/pull/5675))
* Carry the `partial_result` per-request override off `ThreadContext` so it survives the security plugin's thread handoff ([#5758](https://github.com/opensearch-project/sql/pull/5758))
* Detect `BIGINT` overflow in `SUM` and fix wrong `AVG` results on the Calcite engine ([#5612](https://github.com/opensearch-project/sql/pull/5612))
* Fix `IllegalStateException` in `UnifiedQueryPlanner.preserveCollation` on plans with composite (multi-key) collations ([#5650](https://github.com/opensearch-project/sql/pull/5650))
* Fix PPL `search` command ignoring wildcards and over-matching quoted values ([#5697](https://github.com/opensearch-project/sql/pull/5697))
* Fix `dedup` 500 error on cross-index object/scalar mapping conflicts by gracefully degrading scalar-under-object values to null ([#5732](https://github.com/opensearch-project/sql/pull/5732))
* Fix partial-result warnings gate lost across the security plugin's thread handoff ([#5743](https://github.com/opensearch-project/sql/pull/5743))
* Fix zero-offset limit consuming the first deduplicated row ([#5701](https://github.com/opensearch-project/sql/pull/5701))
* Force `snakeyaml-engine` version to resolve dependency conflict ([#5762](https://github.com/opensearch-project/sql/pull/5762))
* Fix PPL `LIKE` function so `\\` correctly escapes the escape character ([#5653](https://github.com/opensearch-project/sql/pull/5653))
* Resolve dotted source paths in pushed-down Calcite scripts so object subfields no longer silently return null ([#5724](https://github.com/opensearch-project/sql/pull/5724))
* Shadow stale mapped leaf columns when `spath` or `eval` overrides an object parent field ([#5726](https://github.com/opensearch-project/sql/pull/5726))
* Fix `dedup` 500 on the analytics-engine route by skipping the dedup-simplify rule before the engine handoff ([#5695](https://github.com/opensearch-project/sql/pull/5695))
* Fix `mvindex()` failure when `plugins.calcite.pushdown.enabled=true` ([#5689](https://github.com/opensearch-project/sql/pull/5689))
* Avoid running the `analyze` measurement path for `profile`-only queries, fixing ~800% performance regression ([#5688](https://github.com/opensearch-project/sql/pull/5688))

## INFRASTRUCTURE

### OpenSearch Alerting

* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#2185](https://github.com/opensearch-project/alerting/pull/2185))

### OpenSearch Alerting Dashboards Plugin

* Fix CI: migrate binary-installation workflow to official opensearch-build actions ([#1507](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1507))
* Fix code-coverage action ([#1509](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1509))
* Onboard code diff analyzer/reviewer and issue dedupe workflows ([#1480](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1480))

### OpenSearch Anomaly Detection

* Upgrade to OpenSearch 3.9, fix build and integration compatibility including Jackson 2 dependency restoration, PPL wire format alignment, HTTPS connection pool cleanup, and unmapped detector-type aggregation handling ([#1775](https://github.com/opensearch-project/anomaly-detection/pull/1775))

### OpenSearch Anomaly Detection Dashboards Plugin

* Use locked Cypress dependency in remote integration tests ([#1246](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1246))

### OpenSearch Asynchronous Search

* Fix code coverage upload action ([#869](https://github.com/opensearch-project/asynchronous-search/pull/869))

### OpenSearch Cross Cluster Replication

* Fix code coverage upload action ([#1750](https://github.com/opensearch-project/cross-cluster-replication/pull/1750))

### OpenSearch Custom Codecs

* Upgrade Codecov action to v7 to resolve rate limiting errors during coverage uploads ([#362](https://github.com/opensearch-project/custom-codecs/pull/362))

### OpenSearch Dashboards Flow Framework

* Pin Cypress to pre-16 in remote integration test workflow to fix `Cypress.env() was removed` failure ([#915](https://github.com/opensearch-project/dashboards-flow-framework/pull/915))

### OpenSearch Dashboards Observability

* Fix code-coverage GitHub Action ([#2888](https://github.com/opensearch-project/dashboards-observability/pull/2888))
* Fix date-picker double-write 409 that flakes the PPL-filter Cypress test ([#2858](https://github.com/opensearch-project/dashboards-observability/pull/2858))
* Pin Cypress to 13.17.0 in FTR e2e workflow to fix CI failures from Cypress 16 breaking changes ([#2854](https://github.com/opensearch-project/dashboards-observability/pull/2854))
* Mock serviceNodeKey in services\_home test to fix broken build-linux ([#2890](https://github.com/opensearch-project/dashboards-observability/pull/2890))

### OpenSearch Dashboards Query Workbench

* Replace third-party GitHub Actions with SHA-pinned equivalents to unblock CI ([#580](https://github.com/opensearch-project/dashboards-query-workbench/pull/580))
* Fix code-coverage GitHub Action configuration ([#598](https://github.com/opensearch-project/dashboards-query-workbench/pull/598))
* Install the FTR repo's lockfile-pinned Cypress instead of the latest release to fix Cypress 16 incompatibility ([#601](https://github.com/opensearch-project/dashboards-query-workbench/pull/601))

### OpenSearch Dashboards Reporting

* Install a locked pre-16 Cypress in the FTR e2e workflow to fix `Cypress.env() was removed` failure ([#800](https://github.com/opensearch-project/dashboards-reporting/pull/800))
* Install the Cypress binary in the cypress-e2e workflow to unblock E2E checks ([#802](https://github.com/opensearch-project/dashboards-reporting/pull/802))

### OpenSearch Dashboards Search Relevance

* Stabilize search-relevance chat command unit test by avoiding transitive loading of @osd/monaco ([#927](https://github.com/opensearch-project/dashboards-search-relevance/pull/927))

### OpenSearch Flow Framework

* Always use 1 shard for system indexes ([#1468](https://github.com/opensearch-project/flow-framework/pull/1468))

### OpenSearch Index Management

* Bump `actions/setup-java` from 5.4.0 to 5.6.0 ([#1700](https://github.com/opensearch-project/index-management/pull/1700))
* Bump `actions/setup-java` from 5.6.0 to 5.7.0 ([#1713](https://github.com/opensearch-project/index-management/pull/1713))
* Bump `actions/setup-java` from 5.7.0 to 6.0.0 ([#1731](https://github.com/opensearch-project/index-management/pull/1731))
* Bump `actions/setup-java` from 6.0.0 to 6.0.1 ([#1735](https://github.com/opensearch-project/index-management/pull/1735))
* Bump `aws-actions/configure-aws-credentials` from 6.2.1 to 6.2.3 ([#1706](https://github.com/opensearch-project/index-management/pull/1706))

### OpenSearch ML Commons

* Ignore flaky `RestChatAgentWithMcpConnectorIT.testChatAgentWithMcpStreamableHttpConnector` test ([#4943](https://github.com/opensearch-project/ml-commons/pull/4943))
* Use the admin client for the retention job index in `RestMemoryRetentionJobIntervalIT` ([#5024](https://github.com/opensearch-project/ml-commons/pull/5024))
* Skip the gRPC integration test when test files are not present ([#4970](https://github.com/opensearch-project/ml-commons/pull/4970))
* Onboard the issue dedupe GitHub workflow ([#4804](https://github.com/opensearch-project/ml-commons/pull/4804))
* Bump `1password/load-secrets-action` to v5.0.1 ([#4984](https://github.com/opensearch-project/ml-commons/pull/4984))

### OpenSearch Neural Search

* Add end-to-end remote dense model integration test for semantic field mapping transformer using TorchServe Docker mock ([#1966](https://github.com/opensearch-project/neural-search/pull/1966))
* Add cross-plugin integration tests for hybrid queries with document-level security ([#1957](https://github.com/opensearch-project/neural-search/pull/1957))
* Pin two-phase processor integration test index to a single shard to fix flaky assertion under non-default shard counts ([#1959](https://github.com/opensearch-project/neural-search/pull/1959))

### OpenSearch Notifications

* Fix Notifications CI dependency failures by aligning AWS SDK STS/Netty versions and adding missing Jackson 2 core dependency ([#1268](https://github.com/opensearch-project/notifications/pull/1268))
* Fix code-coverage action to correctly report missing coverage ([#1269](https://github.com/opensearch-project/notifications/pull/1269))

### OpenSearch OpenSearch System Templates

* Bump `1password/load-secrets-action` to v5.0.1 for improved supply chain security ([#159](https://github.com/opensearch-project/opensearch-system-templates/pull/159))
* Guard `eclipse()` to spotless tasks and pin P2 mirror to a fixed version ([#165](https://github.com/opensearch-project/opensearch-system-templates/pull/165))

### OpenSearch Query Insights Dashboards

* Bump code coverage action to V7 ([#591](https://github.com/opensearch-project/query-insights-dashboards/pull/591))
* Fix OpenSearch-Dashboards branch resolution for push events in CI ([#592](https://github.com/opensearch-project/query-insights-dashboards/pull/592))
* Shorten GitHub Actions check names for readability ([#583](https://github.com/opensearch-project/query-insights-dashboards/pull/583))

### OpenSearch Search Relevance

* Retry the search-config write in the restart-upgrade BWC test until the upgraded cluster settles ([#564](https://github.com/opensearch-project/search-relevance/pull/564))
* Stabilize flaky restart-upgrade BWC tests by waiting for a stable cluster-manager and raising fault-detection tolerances ([#562](https://github.com/opensearch-project/search-relevance/pull/562))

### OpenSearch Security

* Only provision Eclipse JDT formatter when running a spotless task to prevent intermittent CI failures from P2 mirror timeouts ([#6438](https://github.com/opensearch-project/security/pull/6438))
* Stabilize parallel test cluster startup with worker-specific port bands and improved collision handling ([#6466](https://github.com/opensearch-project/security/pull/6466))
* Stabilize resource test Reactor Netty client to honor protocol configuration and bound resource usage ([#6467](https://github.com/opensearch-project/security/pull/6467))
* Harden migrate tests for single-provider resources with no `typeField` ([#6454](https://github.com/opensearch-project/security/pull/6454))
* Group CodeQL dependency updates together to prevent individual PR failures ([#6509](https://github.com/opensearch-project/security/pull/6509))
* Replace `RestHighLevelClient` with OpenSearch Java Client in tests ([#6420](https://github.com/opensearch-project/security/pull/6420))
* Replace `RestHighLevelClient` with `OpenSearchClient` in `HttpClient` ([#6489](https://github.com/opensearch-project/security/pull/6489))
* Replace `RestHighLevelClient` with `OpenSearchClient` in `SecurityAdmin` and remove `opensearch-rest-high-level-client` dependency ([#6492](https://github.com/opensearch-project/security/pull/6492))
* Switch from `snakeyaml` to `snakeyaml-engine` for YAML processing to align with Jackson 3.x ([#6408](https://github.com/opensearch-project/security/pull/6408))

### OpenSearch Security Analytics

* Fix code coverage upload action ([#1810](https://github.com/opensearch-project/security-analytics/pull/1810))

### OpenSearch Security Dashboards Plugin

* Pin Cypress to pre-16 in CI to fix `Cypress.env() was removed` failures ([#2523](https://github.com/opensearch-project/security-dashboards-plugin/pull/2523))

### OpenSearch Skills

* Update actions/checkout digest ([#771](https://github.com/opensearch-project/skills/pull/771))
* Remove Pull Request Labeler workflow to fix CI error ([#774](https://github.com/opensearch-project/skills/pull/774))

### OpenSearch User Behavior Insights

* Add SPDX license header checker and missing headers to source files ([#207](https://github.com/opensearch-project/user-behavior-insights/pull/207))

### OpenSearch k-NN

* Stabilize Remote Index Build integration tests after libcuvs 26.06 upgrade by using graph-friendly test data ([#3557](https://github.com/opensearch-project/k-NN/pull/3557))
* Fix flaky BWC test `WarmupIT.testKNNWarmupCustomLegacyFieldMapping` ([#3419](https://github.com/opensearch-project/k-NN/pull/3419))

### SQL

* Publish the `ppl-rest-spi` snapshot artifact so external consumers can resolve `unified-query-opensearch` dependencies ([#5676](https://github.com/opensearch-project/sql/pull/5676))
* Exclude suites from `integTestRemote` that require analytics-engine plugins, Prometheus, or datasource encryption keys ([#5709](https://github.com/opensearch-project/sql/pull/5709))
* Exclude `HighlightFunctionIT` from license-header checks to work around RAT 0.18 charset misdetection ([#5733](https://github.com/opensearch-project/sql/pull/5733))

## DOCUMENTATION

### OpenSearch Security

* Clarify that demo installer password checks are independent of REST API password validation settings ([#6449](https://github.com/opensearch-project/security/pull/6449))

### OpenSearch Security Dashboards Plugin

* Update Peter Nied maintainer metadata ([#2516](https://github.com/opensearch-project/security-dashboards-plugin/pull/2516))

### SQL

* Add DataFusion backend support column to the PPL command reference ([#5679](https://github.com/opensearch-project/sql/pull/5679))
* Remove redundant pointer to bucket functions from the function list ([#5714](https://github.com/opensearch-project/sql/pull/5714))

## MAINTENANCE

### OpenSearch Alerting

* Fix backend build against 3.x snapshot: declare jackson-core direct dependencies and pin httpcore5 ([#2228](https://github.com/opensearch-project/alerting/pull/2228))
* Fix codecoverage upload action ([#2229](https://github.com/opensearch-project/alerting/pull/2229))
* Rename resource sharing feature flag to the non-experimental key ([#2231](https://github.com/opensearch-project/alerting/pull/2231))

### OpenSearch Alerting Dashboards Plugin

* Clean up resolutions and dependencies, align with OpenSearch Dashboards 3.8, and address CVEs ([#1494](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1494))

### OpenSearch Anomaly Detection Dashboards Plugin

* Clean up resolutions and dependencies, and address CVEs ([#1234](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1234))

### OpenSearch Dashboards Assistant

* Bump brace-expansion from 5.0.8 to 5.0.9 ([#728](https://github.com/opensearch-project/dashboards-assistant/pull/728))
* Bump dompurify to ^3.4.12 to match OSD core and fix babel preset-env test config for BigInt compatibility ([#725](https://github.com/opensearch-project/dashboards-assistant/pull/725))
* Clean up resolutions and dependencies, align with OpenSearch Dashboards 3.8, and address CVEs ([#722](https://github.com/opensearch-project/dashboards-assistant/pull/722))

### OpenSearch Dashboards Flow Framework

* Clean up resolutions and dependencies, align with OpenSearch Dashboards 3.8, and address CVEs ([#908](https://github.com/opensearch-project/dashboards-flow-framework/pull/908))

### OpenSearch Dashboards Investigation

* Bump dompurify from 3.4.12 to 3.4.13 to address hook removal and DOM clobbering fixes ([#416](https://github.com/opensearch-project/dashboards-investigation/pull/416))
* Clean up outdated resolutions and dependencies, align with OpenSearch Dashboards 3.8, and address CVEs ([#412](https://github.com/opensearch-project/dashboards-investigation/pull/412))

### OpenSearch Dashboards Notifications

* Clean up resolutions and dependencies, and address CVEs ([#478](https://github.com/opensearch-project/dashboards-notifications/pull/478))

### OpenSearch Dashboards Observability

* Add Riya Saxena (riysaxen-amzn) as a maintainer ([#2857](https://github.com/opensearch-project/dashboards-observability/pull/2857))
* Improve APM Services environment filter UX with search, truncation, and scroll ([#2880](https://github.com/opensearch-project/dashboards-observability/pull/2880))
* Improve APM Topology Map environment filter UX to match Services page filters ([#2887](https://github.com/opensearch-project/dashboards-observability/pull/2887))
* Simplify Alerts Manager routing tab header by removing redundant status panel ([#2818](https://github.com/opensearch-project/dashboards-observability/pull/2818))
* Bump linkify-it to 5.0.2 and fast-uri to 3.1.7 to remediate six high-severity CVEs ([#2873](https://github.com/opensearch-project/dashboards-observability/pull/2873))
* Bump brace-expansion from 1.1.15 to 1.1.16 ([#2793](https://github.com/opensearch-project/dashboards-observability/pull/2793))
* Bump dompurify from 3.4.12 to 3.4.13 ([#2806](https://github.com/opensearch-project/dashboards-observability/pull/2806))
* Bump fast-uri from 3.1.2 to 3.1.4 ([#2792](https://github.com/opensearch-project/dashboards-observability/pull/2792))
* Bump js-yaml from 4.3.0 to 4.3.1 ([#2807](https://github.com/opensearch-project/dashboards-observability/pull/2807))
* Bump js-yaml from 4.3.1 to 4.3.2 ([#2875](https://github.com/opensearch-project/dashboards-observability/pull/2875))
* Increment version to 3.9.0.0 ([#2808](https://github.com/opensearch-project/dashboards-observability/pull/2808))
* Clean up dependency resolutions, align with OpenSearch Dashboards 3.8, and address CVEs ([#2800](https://github.com/opensearch-project/dashboards-observability/pull/2800))
* Fix release notes link checker by replacing nonexistent PR link with commit link ([#2852](https://github.com/opensearch-project/dashboards-observability/pull/2852))
* Promote APM range-filter gate flags from refs to state and add re-render regression tests ([#2856](https://github.com/opensearch-project/dashboards-observability/pull/2856))

### OpenSearch Dashboards Query Workbench

* Bump qs to 6.16.0 to address CVE-2026-82562 and CVE-2026-82417 ([#594](https://github.com/opensearch-project/dashboards-query-workbench/pull/594))
* Clean up resolutions and dependencies, align with OpenSearch Dashboards 3.8, and address CVEs ([#585](https://github.com/opensearch-project/dashboards-query-workbench/pull/585))

### OpenSearch Dashboards Reporting

* Clean up dependency resolutions and address CVEs in brace-expansion and dompurify ([#793](https://github.com/opensearch-project/dashboards-reporting/pull/793))

### OpenSearch Flow Framework

* Rename resource sharing feature flag settings to the non-experimental key ([#1482](https://github.com/opensearch-project/flow-framework/pull/1482))

### OpenSearch Index Management Dashboards Plugin

* Upgrade `qs` from 6.15.3 to 6.16.0 to address CVEs ([#1473](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1473))
* Clean up dependency resolutions and align with OpenSearch Dashboards 3.8 to address CVEs ([#1467](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1467))

### OpenSearch Job Scheduler

* Bump `org.slf4j:slf4j-api` from 2.0.18 to 2.0.19 ([#991](https://github.com/opensearch-project/job-scheduler/pull/991))
* Bump `org.gradle.test-retry` from 1.6.5 to 1.6.6 ([#995](https://github.com/opensearch-project/job-scheduler/pull/995))
* Bump `com.diffplug.spotless` from 8.10.1 to 8.10.2 ([#996](https://github.com/opensearch-project/job-scheduler/pull/996))

### OpenSearch ML Commons

* Force awssdk STS version to resolve build conflict from DynamoDB client transitive dependency ([#4998](https://github.com/opensearch-project/ml-commons/pull/4998))
* Force snakeyaml\_engine version alignment in ml-commons ([#5007](https://github.com/opensearch-project/ml-commons/pull/5007))
* Update ml-commons build.sh to include `publishPluginZipPublicationToMavenLocal` for neural-search ([#5004](https://github.com/opensearch-project/ml-commons/pull/5004))
* Use Jackson 3.x for JSON processing ([#4981](https://github.com/opensearch-project/ml-commons/pull/4981))
* Rename resource sharing feature flag to the non-experimental key ([#5013](https://github.com/opensearch-project/ml-commons/pull/5013))
* Force jspecify to 1.0.1 to fix yamlRestTest dependency conflict ([#5023](https://github.com/opensearch-project/ml-commons/pull/5023))
* Add Eclipse P2 mirror to avoid `download.eclipse.org` outages ([#4980](https://github.com/opensearch-project/ml-commons/pull/4980))
* Guard `eclipse()` to spotless tasks and keep the P2 mirror on the pinned version ([#5001](https://github.com/opensearch-project/ml-commons/pull/5001))
* Add `ci.opensearch.org/m2/` mirror for plugin resolution ([#4949](https://github.com/opensearch-project/ml-commons/pull/4949))

### OpenSearch ML Commons Dashboards

* Clean up dependency resolutions, align with OpenSearch Dashboards 3.8, and address CVEs ([#509](https://github.com/opensearch-project/ml-commons-dashboards/pull/509))

### OpenSearch Notifications

* Rename resource sharing feature flag to the non-experimental key for security plugin graduation ([#1271](https://github.com/opensearch-project/notifications/pull/1271))

### OpenSearch OpenSearch Learning To Rank Base

* Bump to 3.9.0-SNAPSHOT and fix `JsonStringEncoder` import for Jackson 3 compatibility ([#411](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/411))
* Move jngz-es to emeritus maintainer status ([#408](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/408))

### OpenSearch Query Insights Dashboards

* Update brace-expansion to 1.1.18 to address CVE-2026-14257 and CVE-2026-69152 ([#582](https://github.com/opensearch-project/query-insights-dashboards/pull/582))
* Update qs to 6.16.0 and browserslist to 4.28.9 to address CVEs ([#590](https://github.com/opensearch-project/query-insights-dashboards/pull/590))
* Clean up dependency resolutions and align with OpenSearch Dashboards 3.8, addressing CVEs ([#578](https://github.com/opensearch-project/query-insights-dashboards/pull/578))

### OpenSearch Reporting

* Rename resource sharing feature flag from experimental to non-experimental key ([#1223](https://github.com/opensearch-project/reporting/pull/1223))

### OpenSearch Search Relevance

* Bump 1password/load-secrets-action from 4.0.1 to 4.1.1 ([#537](https://github.com/opensearch-project/search-relevance/pull/537))
* Bump 1password/load-secrets-action from 4.1.1 to 5.0.0 ([#548](https://github.com/opensearch-project/search-relevance/pull/548))
* Bump actions/checkout from 7.0.0 to 7.0.1 ([#536](https://github.com/opensearch-project/search-relevance/pull/536))
* Bump actions/setup-java from 5.6.0 to 5.7.0 ([#549](https://github.com/opensearch-project/search-relevance/pull/549))
* Bump actions/setup-java from 5.7.0 to 6.0.0 ([#577](https://github.com/opensearch-project/search-relevance/pull/577))
* Bump aws-actions/configure-aws-credentials from 6.2.2 to 6.2.3 ([#538](https://github.com/opensearch-project/search-relevance/pull/538))
* Bump aws-actions/configure-aws-credentials from 6.2.3 to 6.2.4 ([#585](https://github.com/opensearch-project/search-relevance/pull/585))
* Bump com.diffplug.spotless:spotless-plugin-gradle from 8.8.0 to 8.9.0 ([#550](https://github.com/opensearch-project/search-relevance/pull/550))
* Bump com.diffplug.spotless:spotless-plugin-gradle from 8.10.1 to 8.10.2 ([#579](https://github.com/opensearch-project/search-relevance/pull/579))
* Bump com.google.guava:guava from 33.6.0-jre to 33.7.1-jre ([#571](https://github.com/opensearch-project/search-relevance/pull/571))
* Bump gradle-wrapper from 9.6.1 to 9.7.0 ([#555](https://github.com/opensearch-project/search-relevance/pull/555))
* Bump gradle-wrapper from 9.7.0 to 9.7.1 ([#572](https://github.com/opensearch-project/search-relevance/pull/572))
* Bump org.javassist:javassist from 3.32.0-GA to 3.33.0-GA ([#578](https://github.com/opensearch-project/search-relevance/pull/578))
* Bump org.json:json from 20260719 to 20260814 ([#570](https://github.com/opensearch-project/search-relevance/pull/570))

### OpenSearch Security

* Bump com.google.guava:guava from 33.6.0-jre to 33.7.1-jre ([#6429](https://github.com/opensearch-project/security/pull/6429))
* Bump at.yawk.lz4:lz4-java from 1.11.1 to 1.11.2 ([#6386](https://github.com/opensearch-project/security/pull/6386))
* Bump ch.qos.logback:logback-classic from 1.5.38 to 1.6.0 ([#6328](https://github.com/opensearch-project/security/pull/6328))
* Bump ch.qos.logback:logback-classic from 1.6.0 to 1.6.1 ([#6366](https://github.com/opensearch-project/security/pull/6366))
* Bump ch.qos.logback:logback-classic from 1.6.1 to 1.6.3 ([#6403](https://github.com/opensearch-project/security/pull/6403))
* Bump commons-codec:commons-codec from 1.22.0 to 1.22.1 ([#6365](https://github.com/opensearch-project/security/pull/6365))
* Bump commons-validator:commons-validator from 1.10.1 to 1.11.0 ([#6387](https://github.com/opensearch-project/security/pull/6387))
* Bump com.google.googlejavaformat:google-java-format from 1.35.0 to 1.36.1 ([#6364](https://github.com/opensearch-project/security/pull/6364))
* Bump com.diffplug.spotless from 8.10.1 to 8.10.2 ([#6491](https://github.com/opensearch-project/security/pull/6491))
* Bump com.github.spotbugs from 6.5.9 to 6.5.10 ([#6379](https://github.com/opensearch-project/security/pull/6379))
* Bump com.github.spotbugs from 6.5.10 to 6.5.11 ([#6443](https://github.com/opensearch-project/security/pull/6443))
* Bump com.autonomousapps.build-health from 3.17.0 to 3.18.0 ([#6363](https://github.com/opensearch-project/security/pull/6363))
* Bump com.autonomousapps.build-health from 3.18.0 to 3.19.1 ([#6446](https://github.com/opensearch-project/security/pull/6446))
* Bump io.dropwizard.metrics:metrics-core from 4.2.39 to 4.2.40 ([#6483](https://github.com/opensearch-project/security/pull/6483))
* Bump io.github.vishwakarma:zjsonpatch from 0.6.2 to 0.6.3 ([#6334](https://github.com/opensearch-project/security/pull/6334))
* Bump io.projectreactor:reactor-core from 3.8.6 to 3.8.7 ([#6484](https://github.com/opensearch-project/security/pull/6484))
* Bump net.bytebuddy:byte-buddy from 1.18.11 to 1.18.12 ([#6425](https://github.com/opensearch-project/security/pull/6425))
* Bump net.bytebuddy:byte-buddy from 1.18.12 to 1.18.13 ([#6485](https://github.com/opensearch-project/security/pull/6485))
* Bump org.bouncycastle:bcprov-jdk18on from 1.85.2 to 1.86 ([#6510](https://github.com/opensearch-project/security/pull/6510))
* Bump org.codehaus.plexus:plexus-utils from 3.6.1 to 3.6.2 ([#6423](https://github.com/opensearch-project/security/pull/6423))
* Bump org.eclipse.platform:org.eclipse.core.runtime from 3.34.200 to 3.35.0 ([#6496](https://github.com/opensearch-project/security/pull/6496))
* Bump org.eclipse.platform:org.eclipse.equinox.common from 3.20.400 to 3.21.0 ([#6500](https://github.com/opensearch-project/security/pull/6500))
* Bump org.gradle.test-retry from 1.6.5 to 1.6.6 ([#6502](https://github.com/opensearch-project/security/pull/6502))
* Bump org.scala-lang:scala3-library\_3 from 3.8.4 to 3.9.0 ([#6440](https://github.com/opensearch-project/security/pull/6440))
* Bump spring\_framework from 7.0.8 to 7.0.9 ([#6427](https://github.com/opensearch-project/security/pull/6427))
* Bump gradle-wrapper from 9.6.1 to 9.7.0 ([#6389](https://github.com/opensearch-project/security/pull/6389))
* Bump gradle-wrapper from 9.7.0 to 9.7.1 ([#6447](https://github.com/opensearch-project/security/pull/6447))

### OpenSearch Security Analytics

* Rename resource sharing feature flag to the non-experimental key ([#1815](https://github.com/opensearch-project/security-analytics/pull/1815))
* Switch from snakeyaml to snakeyaml-engine for YAML processing ([#1812](https://github.com/opensearch-project/security-analytics/pull/1812))

### OpenSearch Security Dashboards Plugin

* Update ip-address to 10.5.0, socks to 2.8.9, and brace-expansion to 1.1.18 to address CVEs ([#2497](https://github.com/opensearch-project/security-dashboards-plugin/pull/2497))
* Update qs to 6.16.0 and @xmldom/xmldom to 0.8.15 to address CVEs ([#2522](https://github.com/opensearch-project/security-dashboards-plugin/pull/2522))
* Clean up resolutions and dependencies, align with OpenSearch Dashboards 3.8, and address CVEs ([#2489](https://github.com/opensearch-project/security-dashboards-plugin/pull/2489))

### OpenSearch Skills

* Bump 1password/load-secrets-action to v5.0.1 ([#784](https://github.com/opensearch-project/skills/pull/784))

### OpenSearch k-NN

* Clean up changelog after 3.8 release ([#3500](https://github.com/opensearch-project/k-NN/pull/3500))
* Fix multiple forbidden API warnings in the codebase for build log clarity ([#3507](https://github.com/opensearch-project/k-NN/pull/3507))

### SQL

* Update the expensive-sort analyze rule to account for `CalciteEnumerableTopK` and add integration tests ([#5710](https://github.com/opensearch-project/sql/pull/5710))
* Migrate to Jackson 3.x APIs ([#5703](https://github.com/opensearch-project/sql/pull/5703))
* Preserve plugin-managed indices during integration test cleanup to avoid repeated recreation of audit and system indices ([#5630](https://github.com/opensearch-project/sql/pull/5630))

## REFACTORING

### OpenSearch Dashboards Observability

* Dead-code sweep of the unified Alerts view, removing ~4,500 lines of unreachable code ([#2876](https://github.com/opensearch-project/dashboards-observability/pull/2876))
* Remove unreachable schema defaults in notebook paraRouter ([#2872](https://github.com/opensearch-project/dashboards-observability/pull/2872))
* Rename 'Cortex' references to 'Prometheus' for consistent terminology ([#2853](https://github.com/opensearch-project/dashboards-observability/pull/2853))

### OpenSearch Dashboards Search Relevance

* Merge single\_search route into search route and read dataSourceId from query parameter consistently ([#935](https://github.com/opensearch-project/dashboards-search-relevance/pull/935))

### OpenSearch Neural Search

* Compute RRF rank scores with exact integer arithmetic, eliminating per-document `BigDecimal` allocations with bit-identical results ([#1942](https://github.com/opensearch-project/neural-search/pull/1942))
* Use `QueryBuilderVisitor` in `HighlightConfigResolver` instead of manually walking the query tree ([#1915](https://github.com/opensearch-project/neural-search/pull/1915))
* Bump neural-sparse-cpp submodule for the DiskSeismic mmap madvise fix ([#2005](https://github.com/opensearch-project/neural-search/pull/2005))

### OpenSearch Security

* Clarify cluster node request classification by renaming `isInterClusterRequest` to `isLocalClusterNodeRequest` and `isTrustedClusterRequest` to `isRemoteClusterNodeRequest` ([#6326](https://github.com/opensearch-project/security/pull/6326))
* Rename authenticated user transport variables to remove legacy `Subject`-oriented naming ([#6432](https://github.com/opensearch-project/security/pull/6432))
* Clarify transport security request flow by extracting header filtering, cross-cluster decoration, and incoming request helpers ([#6476](https://github.com/opensearch-project/security/pull/6476))
* Centralize transport identity propagation into `TransportIdentityContext` for direct, remote, and stream requests ([#6477](https://github.com/opensearch-project/security/pull/6477))