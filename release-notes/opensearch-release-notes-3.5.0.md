# OpenSearch and OpenSearch Dashboards 3.5.0 Release Notes

## Release Highlights

OpenSearch 3.5 delivers several features and enhancements designed to support your search, observability, and AI-powered applications, including new agentic AI tools, expanded Prometheus support, upgrades to the Search Relevance Workbench, and more.

### New and Updated Features

* **Agentic conversation memory**
  Maintains persistent, structured memory for AI agents, directly in OpenSearch, capturing conversation context and intermediate tool reasoning for more coherent follow-up answers. Built-in validation surfaces misconfigurations early for more reliable agent interactions.

* **Hook-based context management**
  Dynamically optimizes context before sending requests to LLMs, avoiding context window overflow and reducing token usage. Supports automatic truncation, summarization, and sliding window strategies at different agent execution stages.

* **Enhanced ML Commons connector framework**
  Supports custom-named actions and additional HTTP methods (PUT, DELETE) for more flexible integration with external REST APIs, enabling comprehensive CRUD operations through a single connector.

* **Bulk SIMD implementation**
  Achieves as much as 58% throughput improvement for FP16 vectors in multi-segment scenarios while maintaining 94% recall. Single-segment scenarios see up to 28% performance gains.

* **Expanded Prometheus support**
  Query and visualize Prometheus metrics data directly in OpenSearch Dashboards alongside logs and traces. Includes PromQL autocomplete and support for gauge metric types.

* **New Piped Processing Language (PPL) commands and functions**
  Six PPL commands and functions (mvcombine, mvzip, mvfind, mvmap, addtotals, streamstats) enable sophisticated data transformation and cumulative statistical calculations.

* **Upgraded gRPC functionality**
  Enhances gRPC support with circuit breaker protection, JWT authentication integration with the Security plugin, and a new contribution guide for developers looking to extend gRPC functionality.

* **Search Relevance Workbench enhancements**
  Automatically evaluate search results with “LLM as judge,” using customizable LLM prompts for enhanced query comparison UI. Schedule nightly or weekly evaluations for baseline search quality testing.

* **Enhanced query insights**
  Automatic capture of username and user role data for every query offers better operational visibility. New wrapper REST API endpoints enable fine-grained access control in multi-tenant environments.

* **Optimized storage for complex queries**
  Query sources are now stored as strings in the local index instead of as complex objects, offering as much as 58% reduction in storage for average queries and 49% for large queries. Configurable truncation available for additional optimization.

* **Workload management integration**
  WLM group assignments are now integrated into the query insights dashboard with filtering and sorting capabilities, enabling you to correlate query performance with resource allocation policies.

* **Vector engine bug fixes**
  Updates address overflow issues in warmup operations, reentrant search problems in byte indexes, and nested document queries when child documents lack vector fields, enhancing performance and reliability for vector search workloads.

### Experimental Features

OpenSearch 3.5 includes the following experimental functionality. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.

* **Agent-User Interaction (AG-UI) protocol**
  AG-UI standardizes how AI agents connect to user-facing applications with event-based streaming interactions, enabling development of context-aware chatbots fully within the OpenSearch platform.

* **New advanced settings for OpenSearch Dashboards**
  Enables you to access histogram breakdowns and field statistics within the OSD explore tools.

* **HTTP/3 support**
  Server-side support for the HTTP/3 protocol offers Improved network performance and resiliency compared to HTTP/2.

## FEATURES

### OpenSearch Alerting

* Access control for results in trigger execution context ([#1991](https://github.com/opensearch-project/alerting/pull/1991))

### OpenSearch Anomaly Detection

* Correlating Anomalies via Temporal Overlap Similarity ([#1641](https://github.com/opensearch-project/anomaly-detection/pull/1641))

### OpenSearch Common Utils

* Add Mattermost as ConfigType for notifications channel ([#853](https://github.com/opensearch-project/common-utils/pull/853))

### OpenSearch Dashboards Notifications

* Add Mattermost as a notification channel destination ([#416](https://github.com/opensearch-project/dashboards-notifications/pull/416))

### OpenSearch Dashboards Observability

* Add APM Configuration page and server components ([#2556](https://github.com/opensearch-project/dashboards-observability/pull/2556))
* Add APM config and context provider ([#2557](https://github.com/opensearch-project/dashboards-observability/pull/2557))
* Add Application Map page for APM with topology visualization ([#2574](https://github.com/opensearch-project/dashboards-observability/pull/2574))
* Add Services landing page ([#2558](https://github.com/opensearch-project/dashboards-observability/pull/2558))
* Add hooks and utility functions for service details ([#2565](https://github.com/opensearch-project/dashboards-observability/pull/2565))
* Add service details pages for APM ([#2566](https://github.com/opensearch-project/dashboards-observability/pull/2566))
* Add support for correlations flyout in services pages. ([#2561](https://github.com/opensearch-project/dashboards-observability/pull/2561))

### OpenSearch Dashboards Reporting

* Use /api/observability/notebooks/savedNotebook for list notebooks route ([#666](https://github.com/opensearch-project/dashboards-reporting/pull/666))

### OpenSearch Dashboards Search Relevance

* Add FrontEnd Support for LLM Judgement Template Prompt ([#667](https://github.com/opensearch-project/dashboards-search-relevance/pull/667))
* Let me reuse my Search Configurations with the Single Query Comparison UI ([#727](https://github.com/opensearch-project/dashboards-search-relevance/pull/727))
* Add UBI sample dataset and dashboards ([#729](https://github.com/opensearch-project/dashboards-search-relevance/pull/729))

### OpenSearch Geospatial

* Add coordinate limit validation for lines, polygons, and holes ([#829](https://github.com/opensearch-project/geospatial/pull/829))

### OpenSearch Index Management

* Add optional `rename_pattern` parameter to convert\_index\_to\_remote action ([#1568](https://github.com/opensearch-project/index-management/pull/1568))
* Add search\_only ISM action for Reader/Writer Separation ([#1560](https://github.com/opensearch-project/index-management/pull/1560))
* Adding Cardinality as supported metric for Rollups ([#1567](https://github.com/opensearch-project/index-management/pull/1567))
* Adding support for multi-tier rollups in ISM ([#1533](https://github.com/opensearch-project/index-management/pull/1533))

### OpenSearch Neural Search

* Add support for asymmetric embedding models([#1605](https://github.com/opensearch-project/neural-search/pull/1605))
* Implement GRPC Hybrid Query ([#1665](https://github.com/opensearch-project/neural-search/pull/1665))
* Add support for min\_score param in hybrid search([#1726](https://github.com/opensearch-project/neural-search/pull/1726))

### OpenSearch Notifications

* Add Mattermost as ConfigType for notifications channel ([#1055](https://github.com/opensearch-project/notifications/pull/1055))

### OpenSearch Query Insights

* Add username and user roles to top n queries ([#508](https://github.com/opensearch-project/query-insights/pull/508))
* Add wrapper endpoints for query insights settings ([#491](https://github.com/opensearch-project/query-insights/pull/491))

### OpenSearch Query Insights Dashboards

* [Feature] Handle source as both string and json object ([#357](https://github.com/opensearch-project/query-insights-dashboards/pull/357))
* [Feature] TopNQueries - WLM Integration ([#432](https://github.com/opensearch-project/query-insights-dashboards/pull/432))

### OpenSearch Search Relevance

* Adds version-based index mapping update support to the Search Relevance plugin [#344](https://github.com/opensearch-project/search-relevance/pull/344)
* LLM Judgement Customized Prompt Template Implementation [#264](https://github.com/opensearch-project/search-relevance/pull/264)
* Add `_search` endpoint for searching for Search Configurations using OpenSearch DSL [#372](https://github.com/opensearch-project/search-relevance/pull/372)
* Add `_search` endpoint for searching for Judgments using OpenSearch DSL [#371](https://github.com/opensearch-project/search-relevance/pull/371)
* Add `_search` endpoint for searching for Query Sets using OpenSearch DSL [#362](https://github.com/opensearch-project/search-relevance/pull/362)
* Add `_search` endpoint for searching for Experiments using OpenSearch DSL ([#369](https://github.com/opensearch-project/search-relevance/pull/369))

### OpenSearch Security

* Allow configuring the timezone for audit log - Feature #5867 ([#5901](https://github.com/opensearch-project/security/pull/5901))
* Introduce new dynamic setting (`plugins.security.dls.write_blocked`) to block all writes when restrictions apply ([#5828](https://github.com/opensearch-project/security/pull/5828))
* JWT authentication for gRPC transport ([#5916](https://github.com/opensearch-project/security/pull/5916))
* Support for HTTP/3 (server side) ([#5886](https://github.com/opensearch-project/security/pull/5886))

### OpenSearch Security Analytics Dashboards Plugin

* Standardize the rule structure across API and UI, and handle the previous rule format to render already existing rules ([#1366](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1366))

### OpenSearch Security Dashboards Plugin

* Adds multi-datasource support in Resource Access Management app ([#2350](https://github.com/opensearch-project/security-dashboards-plugin/pull/2350))

### OpenSearch k-NN

* Index setting to disable exact search after ANN Search with Faiss efficient filters ([#3022](https://github.com/opensearch-project/k-NN/pull/3022))
* Bulk SIMD V2 Implementation ([#3075](https://github.com/opensearch-project/k-NN/pull/3075))

### SQL

* Feature tonumber : issue #4514 tonumber function as part of roadmap #4287 ([#4605](https://github.com/opensearch-project/sql/pull/4605))
* Feature addtotals and addcoltotals ([#4754](https://github.com/opensearch-project/sql/pull/4754))
* Support `mvzip` eval function ([#4805](https://github.com/opensearch-project/sql/pull/4805))
* Support `split` eval function ([#4814](https://github.com/opensearch-project/sql/pull/4814))
* Support `mvfind` eval function ([#4839](https://github.com/opensearch-project/sql/pull/4839))
* Support `mvmap` eval function ([#4856](https://github.com/opensearch-project/sql/pull/4856))
* [Feature] implement transpose command as in the roadmap #4786 ([#5011](https://github.com/opensearch-project/sql/pull/5011))
* Feature/mvcombine ([#5025](https://github.com/opensearch-project/sql/pull/5025))
* Implement spath command with field resolution ([#5028](https://github.com/opensearch-project/sql/pull/5028))

## ENHANCEMENTS

### OpenSearch Custom Codecs

* Migrate from CodecServiceFactory to AdditionalCodecs (so the custom codecs could be used with k-nn, neutral-search, ... plugins) ([#302](https://github.com/opensearch-project/custom-codecs/pull/302))

### OpenSearch Dashboards Flow Framework

* Remove experimental badging ([#832](https://github.com/opensearch-project/dashboards-flow-framework/pull/832))
* Update agent form field titles ([#836](https://github.com/opensearch-project/dashboards-flow-framework/pull/836))

### OpenSearch Dashboards Observability

* Update correlation object client, settings check ([#2570](https://github.com/opensearch-project/dashboards-observability/pull/2570))
* [Enhancement][Integration] Implement 1st MV Refresh Window For Integration ([#2546](https://github.com/opensearch-project/dashboards-observability/pull/2546))
* Feat: use capabilities to show notebook ([#2512](https://github.com/opensearch-project/dashboards-observability/pull/2512))

### OpenSearch Dashboards Search Relevance

* Add optional status=COMPLETED parameter for filtering judgments ([#674](https://github.com/opensearch-project/dashboards-search-relevance/pull/674))
* Add Search Pipeline to Search Configuration Detail page ([#699](https://github.com/opensearch-project/dashboards-search-relevance/issues/699))
* Improve UX of the Judgment Detail page ([#713](https://github.com/opensearch-project/dashboards-search-relevance/pull/713))
* Add agentic search UI/UX enhancements ([#728](https://github.com/opensearch-project/dashboards-search-relevance/pull/728))

### OpenSearch Neural Search

* [SEISMIC Query Explain]: Enable explain function within Sparse ANN query ([#1694](https://github.com/opensearch-project/neural-search/pull/1694))
* [SEISMIC]: Boost multi threads query efficiency ([#1712](https://github.com/opensearch-project/neural-search/pull/1712))
* Add ingest through sparse\_vector field metrics([#1715](https://github.com/opensearch-project/neural-search/pull/1715))
* [Agentic Search] Select explicit index for Agentic Query if returned from ListIndexTool([#1713](https://github.com/opensearch-project/neural-search/pull/1713))
* Include AdditionalCodecs argument to allow additional Codec registration ([#1741](https://github.com/opensearch-project/neural-search/pull/1741))

### OpenSearch Query Insights

* Better strategy to identify missing mapping fields ([#519](https://github.com/opensearch-project/query-insights/pull/519))
* Delay username and user roles extraction to after Top N Filtering ([#527](https://github.com/opensearch-project/query-insights/pull/527))
* Retain local indices on exporter type change ([#465](https://github.com/opensearch-project/query-insights/pull/465))
* Store source field as a string in local index to optimize query storage ([#483](https://github.com/opensearch-project/query-insights/pull/483))
* Truncate source string in local index to optimize query storage ([#484](https://github.com/opensearch-project/query-insights/pull/484))

### OpenSearch Search Relevance

* Added better version of ESCI demo dataset that has images and overlaps with our ESCI judgment data. More compelling demonstrations. ([#354](https://github.com/opensearch-project/search-relevance/pull/354))
* Add supports to parse custom UBI indexes [#364](https://github.com/opensearch-project/search-relevance/pull/364)
* Support for adding description in Search Configuration ([#370](https://github.com/opensearch-project/search-relevance/pull/370))

### OpenSearch Security

* Enable audit logging of document contents for DELETE operations ([#5914](https://github.com/opensearch-project/security/pull/5914))
* Skip hasExplicitIndexPrivilege check for plugin users accessing their own system indices ([#5858](https://github.com/opensearch-project/security/pull/5858))
* Fix-issue-5687 allow access to nested JWT claims via dot notation ([#5891](https://github.com/opensearch-project/security/pull/5891))
* Implement buildSecureClientTransportEngine with serverName parameter ([#5894](https://github.com/opensearch-project/security/pull/5894))
* Serialize Search Request object in DLS Filter Level Handler only when… ([#5883](https://github.com/opensearch-project/security/pull/5883))

### OpenSearch Security Analytics

* Include AdditionalCodecs argument to allow additional Codec registration ([#1636](https://github.com/opensearch-project/security-analytics/pull/1636))

### OpenSearch k-NN

* Correct ef\_search parameter for Lucene engine and reduce to top K ([#3037](https://github.com/opensearch-project/k-NN/pull/3037))
* Field exclusion in source indexing handling ([#3049](https://github.com/opensearch-project/k-NN/pull/3049))
* Join filter clauses of nested k-NN queries to root-parent scope ([#2990](https://github.com/opensearch-project/k-NN/pull/2990))
* Regex for derived source support ([#3031](https://github.com/opensearch-project/k-NN/pull/3031))
* Update validation for cases when k is greater than total results ([#3038](https://github.com/opensearch-project/k-NN/pull/3038))
* Include AdditionalCodecs and EnginePlugin::getAdditionalCodecs hook to allow additional Codec registration ([#3085](https://github.com/opensearch-project/k-NN/pull/3085))

### SQL

* ML command supports category\_field parameter ([#3909](https://github.com/opensearch-project/sql/pull/3909))
* Time Unit Unification for bin/stats ([#4450](https://github.com/opensearch-project/sql/pull/4450))
* Enhance doc and error message handling for `bins` on time-related fields ([#4713](https://github.com/opensearch-project/sql/pull/4713))
* Push down filters on nested fields as nested queries ([#4825](https://github.com/opensearch-project/sql/pull/4825))
* Support sort expression pushdown for SortMergeJoin ([#4830](https://github.com/opensearch-project/sql/pull/4830))
* Add unified query transpiler API ([#4871](https://github.com/opensearch-project/sql/pull/4871))
* Pushdown join with `max=n` option to TopHits aggregation ([#4929](https://github.com/opensearch-project/sql/pull/4929))
* Support pushdown dedup with expression ([#4957](https://github.com/opensearch-project/sql/pull/4957))
* Add scalar min/max to BuiltinFunctionName ([#4967](https://github.com/opensearch-project/sql/pull/4967))
* Add unified query compiler API ([#4974](https://github.com/opensearch-project/sql/pull/4974))
* Support nested aggregation when calcite enabled ([#4979](https://github.com/opensearch-project/sql/pull/4979))
* Support profile options for PPL - Part I Implement phases level metrics. ([#4983](https://github.com/opensearch-project/sql/pull/4983))
* Dedup pushdown (TopHits Agg) should work with Object fields ([#4991](https://github.com/opensearch-project/sql/pull/4991))
* Support enumerable TopK ([#4993](https://github.com/opensearch-project/sql/pull/4993))
* Prune old in operator push down rules ([#4992](https://github.com/opensearch-project/sql/pull/4992))
* RexCall and RelDataType standardization for script push down ([#4914](https://github.com/opensearch-project/sql/pull/4914))
* Introduce logical dedup operators for PPL ([#5014](https://github.com/opensearch-project/sql/pull/5014))
* Support read multi-values from OpenSearch if no codegen triggered ([#5015](https://github.com/opensearch-project/sql/pull/5015))
* Add unified function interface with function discovery API ([#5039](https://github.com/opensearch-project/sql/pull/5039))
* Support profile option for PPL - Part II Implement operator level metrics ([#5044](https://github.com/opensearch-project/sql/pull/5044))
* Support spath with dynamic fields ([#5058](https://github.com/opensearch-project/sql/pull/5058))
* Adopt appendcol, appendpipe, multisearch to spath ([#5075](https://github.com/opensearch-project/sql/pull/5075))
* Set `max=1` in join as default when `plugins.ppl.syntax.legacy.preferred=false` ([#5057](https://github.com/opensearch-project/sql/pull/5057))
* Add OUTPUT as an alias for REPLACE in Lookup ([#5049](https://github.com/opensearch-project/sql/pull/5049))
* Separate explain mode from format params ([#5042](https://github.com/opensearch-project/sql/pull/5042))

## BUG FIXES

### OpenSearch Alerting Dashboards Plugin

* Add missing import in TriggerNotifications.js ([#1345](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1345))
* Fix CVE-2025-57352 by resolving min-document ([#1343](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1343))
* Fix uuid import path not working for modern bundler ([#1339](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1339))

### OpenSearch Cross Cluster Replication

* Fix write index conflicts in bidirectional replication ([#1625](https://github.com/opensearch-project/cross-cluster-replication/pull/1625))
* Index Reopen Call should not be sent when index replication task restarts if the index is already open ([#1619](https://github.com/opensearch-project/cross-cluster-replication/pull/1619))
* Build failure fix for 3.5 ([#1624](https://github.com/opensearch-project/cross-cluster-replication/pull/1624))

### OpenSearch Dashboards Assistant

* Fix: disable input panel and allow user click new conversation in error mode ([#639](https://github.com/opensearch-project/dashboards-assistant/pull/639))

### OpenSearch Dashboards Flow Framework

* Automatically update LLM interface for known models ([#831](https://github.com/opensearch-project/dashboards-flow-framework/pull/831))

### OpenSearch Dashboards Observability

* APM UI bug fixes and improvements ([#2575](https://github.com/opensearch-project/dashboards-observability/pull/2575))
* Add support for metadata for prometheus data-connections ([#2580](https://github.com/opensearch-project/dashboards-observability/pull/2580))
* Catch authz issue for APM flag ([#2551](https://github.com/opensearch-project/dashboards-observability/pull/2551))
* Remove dev-icon dependency ([#2568](https://github.com/opensearch-project/dashboards-observability/pull/2568))
* Update sample data index names for trace analytics ([#2576](https://github.com/opensearch-project/dashboards-observability/pull/2576))

### OpenSearch Dashboards Reporting

* Bump jspdf to 3.0.4 to fix CVE-2025-68428 ([#675](https://github.com/opensearch-project/dashboards-reporting/pull/675))

### OpenSearch Dashboards Search Relevance

* Change timeRange 'to' value to 'now' ([#738](https://github.com/opensearch-project/dashboards-search-relevance/pull/738))
* Fix issue on pairwise experient view page ([#735](https://github.com/opensearch-project/dashboards-search-relevance/pull/735))

### OpenSearch Flow Framework

* Fix templates for OpenSearch 3.x by removing \_doc mapping ([#1301](https://github.com/opensearch-project/flow-framework/pull/1301))
* Fixes null Check where a template is created with an admin (null) user ([#1292](https://github.com/opensearch-project/flow-framework/pull/1292))

### OpenSearch Index Management

* Fix uncaught exception in explain API when invalid sortOrder is provided ([#1563](https://github.com/opensearch-project/index-management/pull/1563))
* Fix: don't call Alias API if aliasActions are empty ([#1489](https://github.com/opensearch-project/index-management/pull/1489))

### OpenSearch Index Management Dashboards Plugin

* Fixing CVE-2025-64718 ([#1383](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1383))

### OpenSearch Neural Search

* [SEISMIC]: Fix the memory usage track upon cache entry creation ([#1701](https://github.com/opensearch-project/neural-search/pull/1701))
* [HYBRID]: Fix for Hybrid Query with Collapse bugs([#1702](https://github.com/opensearch-project/neural-search/pull/1702))
* [HYBRID]: Fix position overflow of docIds in HybridBulkScorer to increase search relevance ([#1706](https://github.com/opensearch-project/neural-search/pull/1706))
* [HYBRID]: Fix logic of RRF score calculation as per document global rank in the subquery ([#1718](https://github.com/opensearch-project/neural-search/pull/1718))
* [HYBRID]: Fix runtime error when number of shards greater than default batch reduce size ([#1738](https://github.com/opensearch-project/neural-search/pull/1738))
* [HYBRID]: Fix CollapseTopFieldDocs logic when a segment has no collapsed fieldDocs but has totalHits > 0 ([#1740](https://github.com/opensearch-project/neural-search/pull/1740))
* [HYBRID]: Fix array\_index\_out\_of\_bound\_exception in case of docsPerGroupPerSubQuery greater or lesser than numHits ([#1742](https://github.com/opensearch-project/neural-search/pull/1742))
* [HYBRID]: Fix null instance handling for empty and skipped shards ([#1745](https://github.com/opensearch-project/neural-search/pull/1745))

### OpenSearch Query Insights

* Change timestamp field to date type ([#523](https://github.com/opensearch-project/query-insights/pull/523))
* Fix excluded indices integ test ([#495](https://github.com/opensearch-project/query-insights/pull/495))
* Remove expired indices check on start-up ([#521](https://github.com/opensearch-project/query-insights/pull/521))
* Fix flaky test testTimeFilterIncludesSomeRecords ([#518](https://github.com/opensearch-project/query-insights/pull/518))
* Fix flaky testTopQueriesResponses ([#513](https://github.com/opensearch-project/query-insights/pull/513))

### OpenSearch Query Insights Dashboards

* Fix CVE-2025-57352 ([#448](https://github.com/opensearch-project/query-insights-dashboards/pull/448))
* CVE-2025-64718 ([#452](https://github.com/opensearch-project/query-insights-dashboards/pull/452))
* Resolves version mismatch between plugin (^5.6.0) and OpenSearch-Dashboards core (^6.0.0) ([#443](https://github.com/opensearch-project/query-insights-dashboards/pull/443))

### OpenSearch Search Relevance

* Added `status` filter support to judgment listing API to prevent incomplete judgment groups from appearing in create experiment workflow ([#304](https://github.com/opensearch-project/search-relevance/pull/304))
* Fix yellow cluster status on single-node clusters ([#329](https://github.com/opensearch-project/search-relevance/issues/329))

### OpenSearch Security

* Bug fix: Fixing partial cache update post snapshot restore ([#5478](https://github.com/opensearch-project/security/pull/5478))
* Fix IllegalArgumentException when resolved indices are empty ([#5797](https://github.com/opensearch-project/security/pull/5797))
* Fix test failure related to change in core to add content-encoding to response headers ([#5897](https://github.com/opensearch-project/security/pull/5897))
* Fixed NPE in LDAP recursive role search ([#5861](https://github.com/opensearch-project/security/pull/5861))
* Make gRPC JWT header keys case insensitive ([#5929](https://github.com/opensearch-project/security/pull/5929))

### OpenSearch Security Analytics Dashboards Plugin

* Fixed CVE-2025-64718 by bumping js-yaml version. ([#1370](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1370))

### OpenSearch k-NN

* Changed warmup seek to use long instead of int to avoid overflow ([#3067](https://github.com/opensearch-project/k-NN/pull/3067))
* Fix MOS reentrant search bug in byte index. ([#3071](https://github.com/opensearch-project/k-NN/pull/3071))
* Fix nested docs query when some child docs has no vector field present ([#3051](https://github.com/opensearch-project/k-NN/pull/3051))
* Fix patch to have a valid score conversion for BinaryCagra. ([#2983](https://github.com/opensearch-project/k-NN/pull/2983))

### SQL

* Error handling for dot-containing field names ([#4907](https://github.com/opensearch-project/sql/pull/4907))
* Replace duplicated aggregation logic with aggregateWithTrimming() ([#4926](https://github.com/opensearch-project/sql/pull/4926))
* Remove GetAlias Call ([#4981](https://github.com/opensearch-project/sql/pull/4981))
* Fix PIT context leak in Legacy SQL for non-paginated queries ([#5009](https://github.com/opensearch-project/sql/pull/5009))
* [BugFix] Not between should use range query ([#5016](https://github.com/opensearch-project/sql/pull/5016))
* Move Calcite-only tests from CrossClusterSearchIT to CalciteCrossClusterSearchIT ([#5085](https://github.com/opensearch-project/sql/pull/5085))

## INFRASTRUCTURE

### OpenSearch Anomaly Detection

* Serialize integTestRemote on remote clusters to avoid index wipe races ([#1654](https://github.com/opensearch-project/anomaly-detection/pull/1654))
* Replace java.security.AccessController with OpenSearch replacement ([#1631](https://github.com/opensearch-project/anomaly-detection/pull/1631))

### OpenSearch Cross Cluster Replication

* Fix replication tests and increment version to 3.5.0 ([#1621](https://github.com/opensearch-project/cross-cluster-replication/pull/1621))
* [Flaky Test] Attempt to fix flaky test by allowing 500 error on stopAllReplication for MultiNode tests ([#1630](https://github.com/opensearch-project/cross-cluster-replication/pull/1630))

### OpenSearch Dashboards Search Relevance

* Enable CI workflows for automated backport PRs. ([#720](https://github.com/opensearch-project/dashboards-search-relevance/pull/720))

### OpenSearch Index Management

* Improve CI speed by refactoring RollupActionIT ([#1572](https://github.com/opensearch-project/index-management/pull/1572))
* Dependabot: bump actions/download-artifact from 5 to 7 ([#1549](https://github.com/opensearch-project/index-management/pull/1549))
* Dependabot: bump actions/upload-artifact from 4 to 6 ([#1551](https://github.com/opensearch-project/index-management/pull/1551))

### OpenSearch Job Scheduler

* Add integTest retry for sample-extension-plugin ([#872](https://github.com/opensearch-project/job-scheduler/pull/872))
* Rename CHANGELOG to CHANGELOG.md to ensure changelog\_verifier workflow works ([#843](https://github.com/opensearch-project/job-scheduler/pull/843))

### OpenSearch Neural Search

* [BWC]: Enable BWC tests after upgrading to Grade 9 ([#1729](https://github.com/opensearch-project/neural-search/pull/1729))
* [BWC]: Correct BWC tests between 3.5 and 2.19 ([#1737](https://github.com/opensearch-project/neural-search/pull/1737))
* [BWC]: Introduce BWC tests for nested field support with for Sparse ANN ([#1725](https://github.com/opensearch-project/neural-search/pull/1725))

### OpenSearch OpenSearch Remote Metadata Sdk

* Update to Gradle 8.12 ([#75](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/75))

### OpenSearch Query Insights

* Add integTest script in query insights to support multinode run on Jenkins ([#533](https://github.com/opensearch-project/query-insights/pull/533))
* Add integTestRemote target to support remote cluster testing ([#530](https://github.com/opensearch-project/query-insights/pull/530))

### OpenSearch Query Insights Dashboards

* Fix security plugin version mismatch in Cypress WLM Workflow ([#444](https://github.com/opensearch-project/query-insights-dashboards/pull/444))
* More reliable check on dashboards readiness in cypress test pipelines ([#451](https://github.com/opensearch-project/query-insights-dashboards/pull/451))

### OpenSearch Search Relevance

* Add BWC and Integration tests for index mapping update ([#349](https://github.com/opensearch-project/search-relevance/pull/349))

### OpenSearch Security

* Clear CHANGELOG post 3.4 release ([#5864](https://github.com/opensearch-project/security/pull/5864))

### OpenSearch k-NN

* Add IT and bwc test with indices containing both vector and non-vector docs ([#3064](https://github.com/opensearch-project/k-NN/pull/3064))
* Gradle ban System.loadLibrary ([#3033](https://github.com/opensearch-project/k-NN/pull/3033))
* Create build graph ([#3032](https://github.com/opensearch-project/k-NN/pull/3032))

### SQL

* Add workflow for SQL CLI integration tests ([#4770](https://github.com/opensearch-project/sql/pull/4770))
* Remove access controller step in Calcite script ([#4900](https://github.com/opensearch-project/sql/pull/4900))
* Adjust CodeRabbit review config ([#4901](https://github.com/opensearch-project/sql/pull/4901))
* Add micro benchmarks for unified query layer ([#5043](https://github.com/opensearch-project/sql/pull/5043))
* Improve coderabbit config ([#5048](https://github.com/opensearch-project/sql/pull/5048))
* Update CodeRabbit instructions ([#4962](https://github.com/opensearch-project/sql/pull/4962))
* Add feedback reminder for CodeRabbit ([#4932](https://github.com/opensearch-project/sql/pull/4932))

## DOCUMENTATION

### OpenSearch Query Insights

* Fix Installation Documentation ([#512](https://github.com/opensearch-project/query-insights/pull/512))

### SQL

* Migrate PPL Documentation from RST to Markdown ([#4912](https://github.com/opensearch-project/sql/pull/4912))
* [DOC] Callout the aggregation result may be approximate ([#4922](https://github.com/opensearch-project/sql/pull/4922))
* Show backticks in testing-doctest.md ([#4941](https://github.com/opensearch-project/sql/pull/4941))
* Escape underscore character in documentation for LIKE ([#4958](https://github.com/opensearch-project/sql/pull/4958))
* Apply feedback from documentation-website to PPL command docs ([#4997](https://github.com/opensearch-project/sql/pull/4997))
* Add PPL docs website exporter script ([#4950](https://github.com/opensearch-project/sql/pull/4950))
* Add version numbers for all settings in the docs ([#5019](https://github.com/opensearch-project/sql/pull/5019))
* Chore: add legacy ppl index.rst for backwards compatibility ([#5026](https://github.com/opensearch-project/sql/pull/5026))
* Add index.md for PPL functions documentation ([#5033](https://github.com/opensearch-project/sql/pull/5033))

## MAINTENANCE

### OpenSearch Anomaly Detection Dashboards Plugin

* Bump lodash from 4.17.21 to 4.17.23 ([#1135](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1135))
* Bump lodash-es from 4.17.21 to 4.17.23 ([#1134](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1134))

### OpenSearch Dashboards Flow Framework

* Bump lodash from 4.17.21 to 4.17.23 ([#840](https://github.com/opensearch-project/dashboards-flow-framework/pull/840))
* Bump lodash-es from 4.17.21 to 4.17.23 ([#838](https://github.com/opensearch-project/dashboards-flow-framework/pull/838))

### OpenSearch Dashboards Maps

* Increment version to 3.5.0.0 ([#783](https://github.com/opensearch-project/dashboards-maps/pull/783))

### OpenSearch Dashboards Notifications

* Feat: read opensearch version from opensearch dashboards version ([#414](https://github.com/opensearch-project/dashboards-notifications/pull/414))

### OpenSearch Dashboards Observability

* Bump lodash from 4.17.21 to 4.17.23 ([#2569](https://github.com/opensearch-project/dashboards-observability/pull/2569))
* Cypress Index testing fix ([#2560](https://github.com/opensearch-project/dashboards-observability/pull/2560))
* Traces cypress fix ([#2562](https://github.com/opensearch-project/dashboards-observability/pull/2562))
* Upgrade cypress-parallel for js-yaml CVE-2025-64718 fix ([#2577](https://github.com/opensearch-project/dashboards-observability/pull/2577))

### OpenSearch Dashboards Query Workbench

* Upgrade js-yaml CVE-2025-64718 ([#519](https://github.com/opensearch-project/dashboards-query-workbench/pull/519))

### OpenSearch Dashboards Reporting

* Upgrade jspdf to 4.0 ([#678](https://github.com/opensearch-project/dashboards-reporting/pull/678))

### OpenSearch Index Management

* Change min version for supporting source index in ISM rollups to 3.5.0 ([#1573](https://github.com/opensearch-project/index-management/pull/1573))
* Dependabot: bump ch.qos.logback:logback-classic from 1.5.22 to 1.5.23 ([#1554](https://github.com/opensearch-project/index-management/pull/1554))
* Dependabot: bump ch.qos.logback:logback-core from 1.5.23 to 1.5.24 ([#1569](https://github.com/opensearch-project/index-management/pull/1569))
* Dependabot: bump commons-beanutils:commons-beanutils from 1.10.1 to 1.11.0 ([#1562](https://github.com/opensearch-project/index-management/pull/1562))
* Dependabot: bump org.jacoco:org.jacoco.agent from 0.8.12 to 0.8.14 ([#1505](https://github.com/opensearch-project/index-management/pull/1505))

### OpenSearch Job Scheduler

* Dependabot: bump actions/download-artifact from 6 to 7 ([#868](https://github.com/opensearch-project/job-scheduler/pull/868))
* Dependabot: bump actions/upload-artifact from 5 to 6 ([#867](https://github.com/opensearch-project/job-scheduler/pull/867))

### OpenSearch Notifications

* Adding toepkerd to MAINTAINERS.md ([#1076](https://github.com/opensearch-project/notifications/pull/1076))

### OpenSearch Observability

* Upgrade to ktlint-cli 1.8.0 ([#1962](https://github.com/opensearch-project/observability/pull/1962))
* Decouple jackson annotation version ([#1968](https://github.com/opensearch-project/observability/pull/1968))

### OpenSearch OpenSearch Remote Metadata Sdk

* Onboard jenkins prod docker images to github actions ([#76](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/76))

### OpenSearch Performance Analyzer

* Consuming performance-analyzer-commons 2.1.0 on JDK21 with all versions bumped for OpenSearch 3.5 release. Takes in the following changes for 3.5 release.([#118](https://github.com/opensearch-project/performance-analyzer-commons/pull/118))

### OpenSearch Search Relevance

* Fix jackson annotations version ([#374](https://github.com/opensearch-project/search-relevance/pull/374))
* Bump actions/checkout from 4 to 6 ([#355](https://github.com/opensearch-project/search-relevance/pull/355))
* Bump actions/checkout from 4 to 6 ([#365](https://github.com/opensearch-project/search-relevance/pull/365))
* Bump com.diffplug.spotless:spotless-plugin-gradle from 8.1.0 to 8.2.0 ([#375](https://github.com/opensearch-project/search-relevance/pull/375))
* Bump com.google.errorprone:error\_prone\_annotations from 2.45.0 to 2.46.0 ([#366](https://github.com/opensearch-project/search-relevance/pull/366))
* Bump gradle-wrapper from 9.2.0 to 9.3.0 ([#376](https://github.com/opensearch-project/search-relevance/pull/376))
* Bump io.freefair.gradle:lombok-plugin from 9.1.0 to 9.2.0 ([#368](https://github.com/opensearch-project/search-relevance/pull/368))
* Bump org.json:json from 20250517 to 20251224 ([#361](https://github.com/opensearch-project/search-relevance/pull/361))
* [LINT] Remove extra import that isn't used. ([#352](https://github.com/opensearch-project/search-relevance/pull/352))

### OpenSearch Security

* Bump at.yawk.lz4:lz4-java from 1.10.1 to 1.10.2 ([#5874](https://github.com/opensearch-project/security/pull/5874))
* Bump ch.qos.logback:logback-classic from 1.5.21 to 1.5.23 ([#5888](https://github.com/opensearch-project/security/pull/5888))
* Bump ch.qos.logback:logback-classic from 1.5.23 to 1.5.24 ([#5902](https://github.com/opensearch-project/security/pull/5902))
* Bump ch.qos.logback:logback-classic from 1.5.24 to 1.5.25 ([#5912](https://github.com/opensearch-project/security/pull/5912))
* Bump ch.qos.logback:logback-classic from 1.5.25 to 1.5.26 ([#5919](https://github.com/opensearch-project/security/pull/5919))
* Bump com.nimbusds:nimbus-jose-jwt from 10.6 to 10.7 ([#5904](https://github.com/opensearch-project/security/pull/5904))
* Bump io.dropwizard.metrics:metrics-core from 4.2.37 to 4.2.38 ([#5922](https://github.com/opensearch-project/security/pull/5922))
* Bump io.projectreactor:reactor-core from 3.8.1 to 3.8.2 ([#5910](https://github.com/opensearch-project/security/pull/5910))
* Bump net.bytebuddy:byte-buddy from 1.18.2 to 1.18.3 ([#5877](https://github.com/opensearch-project/security/pull/5877))
* Bump net.bytebuddy:byte-buddy from 1.18.3 to 1.18.4 ([#5913](https://github.com/opensearch-project/security/pull/5913))
* Bump org.checkerframework:checker-qual from 3.52.1 to 3.53.0 ([#5906](https://github.com/opensearch-project/security/pull/5906))
* Bump org.cryptacular:cryptacular from 1.2.7 to 1.3.0 ([#5921](https://github.com/opensearch-project/security/pull/5921))
* Bump org.junit.jupiter:junit-jupiter-api from 5.14.1 to 5.14.2 ([#5903](https://github.com/opensearch-project/security/pull/5903))
* Bump org.mockito:mockito-core from 5.20.0 to 5.21.0 ([#5875](https://github.com/opensearch-project/security/pull/5875))
* Bump org.ow2.asm:asm from 9.9 to 9.9.1 ([#5876](https://github.com/opensearch-project/security/pull/5876))
* Bump org.springframework.kafka:spring-kafka-test from 4.0.0 to 4.0.1 ([#5873](https://github.com/opensearch-project/security/pull/5873))
* Bump org.springframework.kafka:spring-kafka-test from 4.0.1 to 4.0.2 ([#5918](https://github.com/opensearch-project/security/pull/5918))
* Bump spring\_version from 7.0.2 to 7.0.3 ([#5911](https://github.com/opensearch-project/security/pull/5911))
* Refer to version of error\_prone\_annotations from core's version catalog (2.45.0) ([#5890](https://github.com/opensearch-project/security/pull/5890))
* Remove MakeJava9Happy class that's not applicable in OS 3.X ([#5896](https://github.com/opensearch-project/security/pull/5896))
* Update Jackson to 2.20.1 ([#5892](https://github.com/opensearch-project/security/pull/5892))
* Upgrade eclipse dependencies ([#5863](https://github.com/opensearch-project/security/pull/5863))

### OpenSearch Security Analytics

* Upgrade SA Commons JAR to netty 4.1.30.Final ([#1638](https://github.com/opensearch-project/security-analytics/pull/1638))

### OpenSearch Security Analytics Dashboards Plugin

* Bumped lodash and lodash-es to 4.17.23. ([#1372](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1372))

### OpenSearch Skills

* Fix jackson version ([#683](https://github.com/opensearch-project/skills/pull/683))

### OpenSearch User Behavior Insights

* Increment version to 3.5.0-SNAPSHOT ([#156](https://github.com/opensearch-project/user-behavior-insights/pull/156))

### OpenSearch k-NN

* Added new exception type to signify expected warmup behavior ([#3070](https://github.com/opensearch-project/k-NN/pull/3070))

### SQL

* Remove all AccessController refs ([#4924](https://github.com/opensearch-project/sql/pull/4924))
* Extract unified query context for shared config management ([#4933](https://github.com/opensearch-project/sql/pull/4933))
* Remove shadow jar task from build file ([#4955](https://github.com/opensearch-project/sql/pull/4955))
* Add Frequently Used Big5 PPL Queries ([#4976](https://github.com/opensearch-project/sql/pull/4976))
* Increment version to 3.5.0 ([#5040](https://github.com/opensearch-project/sql/pull/5040))
* Upgrade assertj-core to 3.27.7 ([#5100](https://github.com/opensearch-project/sql/pull/5100))

## REFACTORING

### OpenSearch Query Insights

* Remove index template ([#479](https://github.com/opensearch-project/query-insights/pull/479))

### OpenSearch Security

* Refactor plugin system index tests to use parameterized test pattern ([#5895](https://github.com/opensearch-project/security/pull/5895))
