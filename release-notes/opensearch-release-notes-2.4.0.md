# OpenSearch and Dashboards 2.4.0 Release Notes

## Release Highlights

The OpenSearch 2.4.0 release adds a number of new capabilities to help you enhance your search, analytics, and observability solutions. This release also marks the debut of the software’s first distribution for Windows environments, first security analytics plugin, first semantic search tools, and first solution for ingesting metric data from logs, plus new functionality to enhance cluster resiliency and protect and restore your data. Following are some highlights for this release.

### New features

* New Windows x64 distributions let you deploy OpenSearch and OpenSearch Dashboards directly in your Windows environment.
* You can now ingest metric data into OpenSearch from Prometheus or from log data aggregated within OpenSearch, enabling you to analyze and correlate data across logs, traces, and metrics.
* A new log patterns feature lets you automatically generate patterns from log data for visualization and correlation, enabling you to monitor patterns over time and identify issues.
* Point-in-time search is accessible through an API, allowing you to run different queries against a dataset that is fixed in time.
* New functionality in OpenSearch Dashboards lets you restore data from existing snapshots. Previously, restoring snapshots required using the restore API.
* New geospatial functionality in OpenSearch Dashboards includes two new field types, making it possible to index and search geographic points represented as Cartesian coordinates or as Cartesian shapes. A new GeoHex grid aggregation feature supports datasets that use the Hexagonal Hierarchical Geospatial Indexing System (H3).
* Cluster manager task throttling supports cluster resiliency by allowing you to set limits on the volume of tasks that nodes can submit to the cluster manager.
* Search backpressure supports enhanced resiliency by protecting clusters against traffic surges and other issues that can overwhelm cluster resources.
* A weighted zonal search request routing policy allows you to configure policies to route search traffic away from zones that have degraded performance or failures.
* You can now create custom filters to refine your k-NN searches. The filtering is tightly integrated with the Lucene HNSW algorithm and allows you to apply k-NN searches more efficiently with better search results and performance.

### Experimental features

OpenSearch 2.4.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, see the version history (https://opensearch.org/docs/latest/version-history/) page for links to the documentation.

* Semantic search tools let you use machine learning (ML) to enhance document search results. The release adds functionality that enables OpenSearch to learn an ML model tuned to your documents. Using a pretrained query generator, you can create query-response pairs tailored to your documents, which an ML model can use to learn to order search results based on your data.
* A new search relevance plugin lets you compare different search ranking techniques (including semantic search) side by side in the UI, so you can identify opportunities to fine-tune your results.
* A new model serving framework allows you to upload your own ML models to OpenSearch.
* OpenSearch Dashboards now supports multiple OpenSearch endpoints as data sources, allowing you to visualize data across different clusters in an environment through a single pane of glass.
* A new security analytics plugin for OpenSearch and OpenSearch Dashboards includes tools to help you analyze security event logs, identify attack signatures, visualize threat patterns, and create security alerts.
* With searchable snapshots, you can now search indexes that are stored as snapshots within remote repositories without needing to download all of the index data ahead of time.


## Release Details

[OpenSearch and OpenSearch Dashboards 2.4.0](https://opensearch.org/versions/opensearch-2-4-0.html) includes the following features, experimental features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.4/release-notes/opensearch.release-notes-2.4.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.4/release-notes/opensearch-dashboards.release-notes-2.4.0.md).


## FEATURES

### OpenSearch Dashboards Search Relevance
* Add workflows for backport and linkchecker ([#11](https://github.com/opensearch-project/dashboards-search-relevance/pull/11))
* Initial version of relevance tools with Search Comparison UI ([#5](https://github.com/opensearch-project/dashboards-search-relevance/pull/5))
* Updating Workflows Location ([#17](https://github.com/opensearch-project/dashboards-search-relevance/pull/17))
* Bump to 3.0.0.0 ([#18](https://github.com/opensearch-project/dashboards-search-relevance/pull/18))
* Changing name to camel case: searchRelevanceDashboards ([#23](https://github.com/opensearch-project/dashboards-search-relevance/pull/23))
* Fixing badly merged README.md ([#25](https://github.com/opensearch-project/dashboards-search-relevance/pull/25))
* Search Results UI ([#26](https://github.com/opensearch-project/dashboards-search-relevance/pull/26))
* Add an initial integration test ([#30](https://github.com/opensearch-project/dashboards-search-relevance/pull/30))
* Updating backport to 2.0 ([#34](https://github.com/opensearch-project/dashboards-search-relevance/pull/34))
* Moving PULL_REQUEST_TEMPLATE.md to .github dir ([#35](https://github.com/opensearch-project/dashboards-search-relevance/pull/35))
* Fix styling conflicts ([#59](https://github.com/opensearch-project/dashboards-search-relevance/pull/59))
* Fix backport delete action; Adding Badges for Build and Link Checker ([#54](https://github.com/opensearch-project/dashboards-search-relevance/pull/54))
* Release notes for 2.4.0 ([#65](https://github.com/opensearch-project/dashboards-search-relevance/pull/65))
* Remove beta1 from the release notes file name for 2.4.0 ([#70](https://github.com/opensearch-project/dashboards-search-relevance/pull/70))
* Update the release notes folder name for consistency with other repos ([#73](https://github.com/opensearch-project/dashboards-search-relevance/pull/73))
* Unit test ([#83](https://github.com/opensearch-project/dashboards-search-relevance/pull/83))
* Issue fix ([#82](https://github.com/opensearch-project/dashboards-search-relevance/pull/82))
* Unit test ([#88](https://github.com/opensearch-project/dashboards-search-relevance/pull/88))
* Change results number to displayed results number ([#55](https://github.com/opensearch-project/dashboards-search-relevance/pull/55))


### OpenSearch Geospatial
* Support Uber's H3 geospatial indexing system as geohex_grid ([#179](https://github.com/opensearch-project/geospatial/pull/179))
* Add geojson support for XYPoint  ([#162](https://github.com/opensearch-project/geospatial/pull/162))
* Add XYPoint Field Type to index and query documents that contains cartesian points ([#130](https://github.com/opensearch-project/geospatial/pull/130))
* Add XYShapeQueryBuilder ([#82](https://github.com/opensearch-project/geospatial/pull/82))
* Add parameter to randomly include z coordinates to geometry ([#79](https://github.com/opensearch-project/geospatial/pull/79))
* Add shape processor ([#74](https://github.com/opensearch-project/geospatial/pull/74))
* Add shape field mapper ([#70](https://github.com/opensearch-project/geospatial/pull/70))
* Add ShapeIndexer to create indexable fields ([#68](https://github.com/opensearch-project/geospatial/pull/68))


### OpenSearch Index Management Dashboards Plugin
* Add Snapshot Restore functionality and UI([#338](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/338))


### OpenSearch Ml Commons
* Add profile APIs for model and task ([#446](https://github.com/opensearch-project/ml-commons/pull/446))
* Support the generic ml ppl command. ([#484](https://github.com/opensearch-project/ml-commons/pull/484))


### OpenSearch Observability
* Add metrics ([#1234](https://github.com/opensearch-project/observability/pull/1234))
* Add log pattern table ([#1212](https://github.com/opensearch-project/observability/pull/1212))


### OpenSearch Security Analytics
* Sigma Rules, Rule Engine Parser ([#6](https://github.com/opensearch-project/security-analytics/pull/6), [#8](https://github.com/opensearch-project/security-analytics/pull/8), [#26](https://github.com/opensearch-project/security-analytics/pull/26), [#27](https://github.com/opensearch-project/security-analytics/pull/27))
* Threat Detector Lifecycle Management (CRUD), Pre-packaged/Custom Rule Lifecycle Management (CRUD) ([#32](https://github.com/opensearch-project/security-analytics/pull/32), [#40](https://github.com/opensearch-project/security-analytics/pull/40), [#43](https://github.com/opensearch-project/security-analytics/pull/43), [#48](https://github.com/opensearch-project/security-analytics/pull/48), [#52](https://github.com/opensearch-project/security-analytics/pull/52), [#80](https://github.com/opensearch-project/security-analytics/pull/80))
* Mapping Logs/Rule fields to ECS(Elastic Common Schema) format ([#30](https://github.com/opensearch-project/security-analytics/pull/30), [#35](https://github.com/opensearch-project/security-analytics/pull/35), [#46](https://github.com/opensearch-project/security-analytics/pull/46), [#46](https://github.com/opensearch-project/security-analytics/pull/46), [#89](https://github.com/opensearch-project/security-analytics/pull/89))
* Integrate Findings (Lifecycle Management including Rollovers), Triggers, Alerts(Lifecycle Management) ([#39](https://github.com/opensearch-project/security-analytics/pull/39), [#54](https://github.com/opensearch-project/security-analytics/pull/54), [#67](https://github.com/opensearch-project/security-analytics/pull/67), [#70](https://github.com/opensearch-project/security-analytics/pull/70), [#70](https://github.com/opensearch-project/security-analytics/pull/70), [#82](https://github.com/opensearch-project/security-analytics/pull/82))
* Integrate with Notifications, Acknowledge Alerts ([#71](https://github.com/opensearch-project/security-analytics/pull/71), [#75](https://github.com/opensearch-project/security-analytics/pull/75), [#85](https://github.com/opensearch-project/security-analytics/pull/85))
* Integrate with Security, implement RBAC, backend roles filtering ([#78](https://github.com/opensearch-project/security-analytics/pull/78))


### OpenSearch Security Analytics Dashboards
* Added create detectors UI pages. ([#15](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/15)
* Added get mappings API service wrappers. ([#22](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/22))
* Added overview page UI. ([#24](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/24))
* Added configure alerts UI page. ([#25](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/25))
* Added rules UI pages. ([#55](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/55))
* Added toast notifications. ([#70](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/70))


### OpenSearch Security Dashboards Plugin
* Initial commit for multiple authentication ([#1110](https://github.com/opensearch-project/security-dashboards-plugin/pull/1110))
* Saved Object Aggregation View ([#1146](https://github.com/opensearch-project/security-dashboards-plugin/pull/1146))
* [Saved Object Aggregation View] Use namespace registry to add tenant filter ([#1169](https://github.com/opensearch-project/security-dashboards-plugin/pull/1169))
* Move tenant-related utils to common folder ([#1184](https://github.com/opensearch-project/security-dashboards-plugin/pull/1184))


### OpenSearch SQL
* Add patterns and grok command ([#813](https://github.com/opensearch-project/sql/pull/813))
* Add category_field to AD command in PPL ([#952](https://github.com/opensearch-project/sql/pull/952))
* A Generic ML Command in PPL ([#971](https://github.com/opensearch-project/sql/pull/971))
* Catalog Implementation ([#819](https://github.com/opensearch-project/sql/pull/819))
* Catalog to Datasource changes ([#1027](https://github.com/opensearch-project/sql/pull/1027))
* Prometheus Connector Initial Code ([#878](https://github.com/opensearch-project/sql/pull/878))
* Restricted catalog name to [a-zA-Z0-9_-] characters ([#876](https://github.com/opensearch-project/sql/pull/876))
* Table function for supporting prometheus query_range function ([#875](https://github.com/opensearch-project/sql/pull/875))
* List tables/metrics using information_schema in source command. ([#914](https://github.com/opensearch-project/sql/pull/914))
* [Backport 2.4] Prometheus select metric and stats queries. ([#1020](https://github.com/opensearch-project/sql/pull/1020))


## Experimental Features

### OpenSearch Ml Commons
* Tune ML model to support custom model ([#471](https://github.com/opensearch-project/ml-commons/pull/471))
* Add input/output for custom model ([#473](https://github.com/opensearch-project/ml-commons/pull/473))
* Refactor ML algorithm package for supporting custom model ([#474](https://github.com/opensearch-project/ml-commons/pull/474))
* Add text embedding model ([#477](https://github.com/opensearch-project/ml-commons/pull/477))
* Add custom model transport action, request/response to common package ([#479](https://github.com/opensearch-project/ml-commons/pull/479))
* Add custom model public APIs: upload/load/unload ([#488](https://github.com/opensearch-project/ml-commons/pull/488))
* Tune interface to support predicting loaded built-in algorithms; remove stale task in cache ([#491](https://github.com/opensearch-project/ml-commons/pull/491))
* Refactor model cache and thread pool ([#496](https://github.com/opensearch-project/ml-commons/pull/496))
* Add custom model size limit ([#503](https://github.com/opensearch-project/ml-commons/pull/503))
* Tune thread pool size; add more unit test ([#506](https://github.com/opensearch-project/ml-commons/pull/503))
* Changes to custom model chunk upload api ([#495](https://github.com/opensearch-project/ml-commons/pull/495))
* Support multi-gpu; fix inference duration queue bug ([#515](https://github.com/opensearch-project/ml-commons/pull/515))
* Add trusted URL regex ([#518](https://github.com/opensearch-project/ml-commons/pull/518))
* Add description field when upload model; tune log level ([#531](https://github.com/opensearch-project/ml-commons/pull/531))


### OpenSearch Neural Search
* Add MLCommonsClientAccessor and MLPredict TransportAction for accessing the MLClient's predict API ([#16](https://github.com/opensearch-project/neural-search/pull/16))
* Add parsing logic for neural query ([#15](https://github.com/opensearch-project/neural-search/pull/15))
* Integrate model inference to build neural query ([#20](https://github.com/opensearch-project/neural-search/pull/20))
* Add text embedding processor to neural search ([#18](https://github.com/opensearch-project/neural-search/pull/18))


## ENHANCEMENTS

### OpenSearch Alerting
* Support multiple data sources ([#558](https://github.com/opensearch-project/alerting/pull/558]))
* Use custom query index in update monitor flow ([#591](https://github.com/opensearch-project/alerting/pull/591]))
* Enhance Get Alerts and Get Findings for list of monitors in bulk ([#590](https://github.com/opensearch-project/alerting/pull/590]))
* Support fetching alerts by list of alert ids in Get Alerts Action ([#608](https://github.com/opensearch-project/alerting/pull/608]))
* Ack alerts - allow moving alerts to history index with custom datasources ([#626](https://github.com/opensearch-project/alerting/pull/626]))
* Enabled parsing of bucket level monitors ([#631](https://github.com/opensearch-project/alerting/pull/631]))
* Custom history indices ([#616](https://github.com/opensearch-project/alerting/pull/616]))
* Adds filtering on owner field in search monitor action ([#641](https://github.com/opensearch-project/alerting/pull/641]))
* Support to specify backend roles for monitors ([#635](https://github.com/opensearch-project/alerting/pull/635]))
* Adds findings in bucket level monitor ([#636](https://github.com/opensearch-project/alerting/pull/636]))


### OpenSearch Common Utils
* Accept of list of monitor ids in findings and alerts request dtos ([#277](https://github.com/opensearch-project/common-utils/pull/277))
* Added legacy support for SNS messages. ([#269](https://github.com/opensearch-project/common-utils/pull/269))
* Add list of alert ids in get alerts request  ([#284](https://github.com/opensearch-project/common-utils/pull/284))
* Fix security-analytics alerting findings api integration ([#292](https://github.com/opensearch-project/common-utils/pull/292))
* Added params to Datasources ([#290](https://github.com/opensearch-project/common-utils/pull/290))
* Fix security-analytics to alerting integration ([#293](https://github.com/opensearch-project/common-utils/pull/293))
* Add findings enabled flag and findings field in bucket level monitor ([#305](https://github.com/opensearch-project/common-utils/pull/305))
* Support backend roles in indexMonitorRequest ([#308](https://github.com/opensearch-project/common-utils/pull/308))
* Added function for request recreation that considers the writeable request ([#303](https://github.com/opensearch-project/common-utils/pull/303))
* Adds owner field in monitor model ([#313](https://github.com/opensearch-project/common-utils/pull/313))


### OpenSearch Dashboards Search Relevance
* Add codeowner ([#43](https://github.com/opensearch-project/dashboards-search-relevance/pull/43))


### OpenSearch Geospatial
* Add groupId to pluginzip publication ([#167](https://github.com/opensearch-project/geospatial/pull/167))
* Flip X and Y coordinates for WKT and array formats in XYPoint ([#156](https://github.com/opensearch-project/geospatial/pull/156))


### OpenSearch Index Management
* Feature/184 introduce security tests ([#474](https://github.com/opensearch-project/index-management/pull/474))
* Alias in rollup target_index field ([#445](https://github.com/opensearch-project/index-management/pull/445))
* Adds an alias action ([#575](https://github.com/opensearch-project/index-management/pull/575))
* Error prevention / Action validation stage 1 ([#579](https://github.com/opensearch-project/index-management/pull/579))


### OpenSearch Index Management Dashboards Plugin
* feat: Add diff confirm modal in create wizard ([#323](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/323))
* feature: Add form generator & advanced settings to speed up development in common form case ([#329](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/329))


### OpenSearch k-NN
* Merge efficient filtering from feature branch ([#588](https://github.com/opensearch-project/k-NN/pull/588))
* Add groupId to pluginzip publication ([#578](https://github.com/opensearch-project/k-NN/pull/578))
* Added sample perf-test configs for faiss-ivf, faiss-ivfpq, lucene-hnsw ([#555](https://github.com/opensearch-project/k-NN/pull/555))
* Adding OSB index specification json for lucene hnsw ([#552](https://github.com/opensearch-project/k-NN/pull/552))
* Adding k-NN engine stat ([#523](https://github.com/opensearch-project/k-NN/pull/523))


### OpenSearch Ml Commons
* Do not return model content by default ([#458](https://github.com/opensearch-project/ml-commons/pull/458))
* Update delete model TransportAction to support custom model ([#497](https://github.com/opensearch-project/ml-commons/pull/497))
* Add disk circuit breaker, update deleteModel message format ([#498](https://github.com/opensearch-project/ml-commons/pull/498)))
* Return circuit breaker name in error messages ([#507](https://github.com/opensearch-project/ml-commons/pull/507))
* Change the max_ml_task_per_node into dynamic settings ([#530](https://github.com/opensearch-project/ml-commons/pull/530))


### OpenSearch Neural Search
* Change text embedding processor to async mode for better isolation ([#27](https://github.com/opensearch-project/neural-search/pull/27))


### OpenSearch Observability
* Change auto expand replicas to 0-2 for better availability ([#1186](https://github.com/opensearch-project/observability/pull/1186))
* Add anomaly count and config to patterns table ([#1216](https://github.com/opensearch-project/observability/pull/1216))
* Adding save functionality to metrics ([#1241](https://github.com/opensearch-project/observability/pull/1241))
* Persist redux state in browser ([#1178](https://github.com/opensearch-project/observability/pull/1178))
* UI changes for sidebar and update to PPL request ([#1246](https://github.com/opensearch-project/observability/pull/1246))
* Backtick supports ([#1250](https://github.com/opensearch-project/observability/pull/1250))
* Use in-memory count for total hits in patterns ratio ([#1254](https://github.com/opensearch-project/observability/pull/1254))
* Show metrics in events homepage ([#1232](https://github.com/opensearch-project/observability/pull/1232))
* Update Sidepanel ([#1230](https://github.com/opensearch-project/observability/pull/1230))
* Added dummy search field, panel push button ([#1227](https://github.com/opensearch-project/observability/pull/1227))
* Adding visualizations panel to metrics ([#1222](https://github.com/opensearch-project/observability/pull/1222))
* Add metrics api events ([#1214](https://github.com/opensearch-project/observability/pull/1214))


### OpenSearch Security Analytics
* Use of `custom datasources while creating alerting monitors` in `opensearch-security-analytics` ([#34](https://github.com/opensearch-project/security-analytics/pull/34), [#72](https://github.com/opensearch-project/security-analytics/pull/72), [#99](https://github.com/opensearch-project/security-analytics/pull/99))
* Add owner field in monitor to seggregate `opensearch-security-analytics` specific data from `opensearch-alerting` data. ([#110](https://github.com/opensearch-project/security-analytics/pull/110))


### OpenSearch Security
* Add install_demo_configuration Batch script for Windows ([#2161](https://github.com/opensearch-project/security/pull/2161)[#2203](https://github.com/opensearch-project/security/commit/51a286230f5ba1829dd7e62af1b626540eee3600)
* Add CI for Windows and MacOS platforms ([#2190](https://github.com/opensearch-project/security/pull/2190)[#2205](https://github.com/opensearch-project/security/pull/2205))
* Make ldap pool period and idle time configurable ([#2091](https://github.com/opensearch-project/security/commit/edd9f49e161739fe26f2d3652121e6c187636b79)[#2097](https://github.com/opensearch-project/security/pull/2097))
* Allow custom LDAP return attributes ([#2093](https://github.com/opensearch-project/security/pull/2093)[#2110](https://github.com/opensearch-project/security/pull/2110))
* Add bcpkix-jdk15on runtimeOnly dependency to read keys with bouncycastle ([#2191](https://github.com/opensearch-project/security/pull/2191)[#2200](https://github.com/opensearch-project/security/pull/2200))


### OpenSearch Security Dashboards Plugin
* Preserve URL Hash for SAML based login ([#1039](https://github.com/opensearch-project/security-dashboards-plugin/pull/1039))


### OpenSearch SQL
* Add datetime functions `FROM_UNIXTIME` and `UNIX_TIMESTAMP` ([#835](https://github.com/opensearch-project/sql/pull/835))
* Adding `CONVERT_TZ` and `DATETIME` functions to SQL and PPL  ([#848](https://github.com/opensearch-project/sql/pull/848))
* Add Support for Highlight Wildcard in SQL ([#827](https://github.com/opensearch-project/sql/pull/827))
* Update SQL CLI to use AWS session token. ([#918](https://github.com/opensearch-project/sql/pull/918))
* Add `typeof` function. ([#867](https://github.com/opensearch-project/sql/pull/867))
* Show catalogs ([#925](https://github.com/opensearch-project/sql/pull/925))
* Add functions `PERIOD_ADD` and `PERIOD_DIFF`. ([#933](https://github.com/opensearch-project/sql/pull/933))
* Add take() aggregation function in PPL ([#949](https://github.com/opensearch-project/sql/pull/949))
* Describe Table with catalog name. ([#989](https://github.com/opensearch-project/sql/pull/989))
* Catalog Enhancements ([#988](https://github.com/opensearch-project/sql/pull/988))
* Rework on error reporting to make it more verbose and human-friendly. ([#839](https://github.com/opensearch-project/sql/pull/839))


## BUG FIXES

### OpenSearch Alerting
* Add tags to trigger condition of doc-level monitor ([#598](https://github.com/opensearch-project/alerting/pull/598]))
* SearchAlert fix ([#613](https://github.com/opensearch-project/alerting/pull/598]))
* Fix Acknowledge Alert Request class loader issue ([#618](https://github.com/opensearch-project/alerting/pull/618]))
* Fix alias exists check in findings index creation ([#622](https://github.com/opensearch-project/alerting/pull/622]))
* Add tags to trigger condition of doc-level monitor ([#598](https://github.com/opensearch-project/alerting/pull/598]))
* Fix for windows ktlint issue ([#585](https://github.com/opensearch-project/alerting/pull/585]))


### OpenSearch Cross Cluster Replication
* Updated jackson databind version to 2.13.4.2 ([597](https://github.com/opensearch-project/cross-cluster-replication/pull/597))
* Include default index settings during leader setting validation ([601](https://github.com/opensearch-project/cross-cluster-replication/pull/601))


### OpenSearch Dashboards Reports
* Upgrade puppeteer ([#483](https://github.com/opensearch-project/dashboards-reports/pull/483))
* Upgrade jsdom, terser and jsoup ([#515](https://github.com/opensearch-project/dashboards-reports/pull/515))
* Upgrade ktlint ([#521](https://github.com/opensearch-project/dashboards-reports/pull/521))
* Upgrade minimatch ([#512](https://github.com/opensearch-project/dashboards-reports/pull/512))
* Upgrade detekt and snakeyaml ([#527](https://github.com/opensearch-project/dashboards-reports/pull/527))
* Upgrade loader-utils ([#524](https://github.com/opensearch-project/dashboards-reports/pull/524))


### OpenSearch Dashboards Search Relevance
* Make srdash compatible with default build script ([#46](https://github.com/opensearch-project/dashboards-search-relevance/pull/46))
* Fix default tab spacing ([#77](https://github.com/opensearch-project/dashboards-search-relevance/pull/77))


### OpenSearch Dashboards Visualizations
* Upgrade dependencies ([#122](https://github.com/opensearch-project/dashboards-visualizations/pull/122))
* Upgrade ansi-regex ([#123](https://github.com/opensearch-project/dashboards-visualizations/pull/123))


### OpenSearch Index Management
* Added rounding when using aggregate script for avg metric. ([#490](https://github.com/opensearch-project/index-management/pull/490))
* Adds plugin version sweep background job ([#434](https://github.com/opensearch-project/index-management/pull/434))
* Moved _doc_count from transform._doc_count to root of document ([#558](https://github.com/opensearch-project/index-management/pull/558))
* Bugfix/538 Adding timeout and retry to Transform '_search' API calls ([#576](https://github.com/opensearch-project/index-management/pull/576))


### OpenSearch Index Management Dashboards Plugin
* Add rel to link for external links, IM dashboards plugin ([#261](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/261))


### OpenSearch k-NN
* Fix NPE on null script context ([#560](https://github.com/opensearch-project/k-NN/pull/560))
* Add fix to fromXContent and toXContent in ModelGraveyard ([#618](https://github.com/opensearch-project/k-NN/pull/618))


### OpenSearch Ml Commons
* Bug fix: filter _source field in search model api ([#445](https://github.com/opensearch-project/ml-commons/pull/445))
* Fix profile bug ([#463](https://github.com/opensearch-project/ml-commons/pull/463))
* Fix running tasks when circuit breaker is open ([#542](https://github.com/opensearch-project/ml-commons/pull/542))
* Fix no permission bug when update index mapping ([#545](https://github.com/opensearch-project/ml-commons/pull/545))


### OpenSearch Neural Search
* Update the model function name from CUSTOM to TEXT_EMBEDDING as per the latest changes in MLCommons ([#17](https://github.com/opensearch-project/neural-search/pull/17))
* Fix the locale changes from locale.default to locale.ROOT to fix the tests failing on Windows ([#43](https://github.com/opensearch-project/neural-search/pull/43))


### OpenSearch Observability
* Fix column spacing and pattern table highlighting ([#1218](https://github.com/opensearch-project/observability/pull/1218))
* Fix filtered pattern selection ([#1236](https://github.com/opensearch-project/observability/pull/1236))
* Fixes for BWC issues, updated grammar ([#1235](https://github.com/opensearch-project/observability/pull/1235))
* Minor UI changes for sidebar ([#1237](https://github.com/opensearch-project/observability/pull/1237))
* Update minimatch version to 3.0.5 ([#1228](https://github.com/opensearch-project/observability/pull/1228))
* Update detekt version ([#1226](https://github.com/opensearch-project/observability/pull/1226))
* Fix metrics visualization regression ([#1244](https://github.com/opensearch-project/observability/pull/1244))
* Fix Prometheus Mappings ([#1242](https://github.com/opensearch-project/observability/pull/1242))
* Metrics bug fixes ([#1248](https://github.com/opensearch-project/observability/pull/1248))([#1253](https://github.com/opensearch-project/observability/pull/1253))
* Fix metrics switch ([#1247](https://github.com/opensearch-project/observability/pull/1247))


### OpenSearch Performance Analyzer
* Safeguard against appending origin twice ([#285](https://github.com/opensearch-project/performance-analyzer/pull/285))


### OpenSearch Security Analytics
* Fix bug to support aliasMappings in create mappings api ([#69](https://github.com/opensearch-project/security-analytics/pull/69))
* Fix for multi-node test faiures on rule ingestion ([#76](https://github.com/opensearch-project/security-analytics/pull/76))
* Fix bug on deleting/updating rule when it is not used by detectors ([#77](https://github.com/opensearch-project/security-analytics/pull/77))
* Fix build for delete detector api ([#97](https://github.com/opensearch-project/security-analytics/pull/97))
* FindingsDto assign detectorId bug ([#102](https://github.com/opensearch-project/security-analytics/pull/102))
* Update index monitor method to include namedWriteableRegistry for common utils interface ([#105](https://github.com/opensearch-project/security-analytics/pull/105))


### OpenSearch Security
* Point in time API security changes ([#2094](https://github.com/opensearch-project/security/pull/2094)[#2223](https://github.com/opensearch-project/security/pull/2223))
* Fix windows encoding issues ([#2206](https://github.com/opensearch-project/security/pull/2206)[#2218](https://github.com/opensearch-project/security/pull/2218))


### OpenSearch Security Dashboards Plugin
* Fix the tenant switching after timeout ([#1090](https://github.com/opensearch-project/security-dashboards-plugin/pull/1090))
* Fix the UI user flow of selecting custom teanant on tenant switch panel ([#1112](https://github.com/opensearch-project/security-dashboards-plugin/pull/1112))
* Fix for Tenancy info getting lost on re-login in SAML Authentication flow ([#1134](https://github.com/opensearch-project/security-dashboards-plugin/pull/1134))
* Remove multi-tenant path check in auth handler ([#1151](https://github.com/opensearch-project/security-dashboards-plugin/pull/1151))


### OpenSearch SQL
* Fix EqualsAndHashCode Annotation Warning Messages ([#847](https://github.com/opensearch-project/sql/pull/847))
* Remove duplicated png file ([#865](https://github.com/opensearch-project/sql/pull/865))
* Fix NPE with multiple queries containing DOT(.) in index name. ([#870](https://github.com/opensearch-project/sql/pull/870))
* Update JDBC driver version ([#941](https://github.com/opensearch-project/sql/pull/941))
* Fix result order of parse with other run time fields ([#934](https://github.com/opensearch-project/sql/pull/934))
* AD timefield name issue ([#919](https://github.com/opensearch-project/sql/pull/919))
* [Backport 2.4] Add function name as identifier in antlr ([#1018](https://github.com/opensearch-project/sql/pull/1018))
* [Backport 2.4] Fix incorrect results returned by `min`, `max` and `avg` ([#1022](https://github.com/opensearch-project/sql/pull/1022))


## INFRASTRUCTURE

### OpenSearch Alerting
* Disable ktlint for alerting as it has errors on Windows ([#570](https://github.com/opensearch-project/alerting/pull/570]))
* Remove plugin to OS min race condition ([#601](https://github.com/opensearch-project/alerting/pull/601]))


### OpenSearch Alerting Dashboards Plugin
* Support windows CI ([#354](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/354))


### OpenSearch Anomaly Detection
* Removed Github DCO action since DCO runs via Github App now ([#664](https://github.com/opensearch-project/anomaly-detection/pull/664))
* Add support for reproducible builds ([#579](https://github.com/opensearch-project/anomaly-detection/pull/579))
* Fix window delay test ([#674](https://github.com/opensearch-project/anomaly-detection/pull/674))
* Update jackson dependency version ([#678](https://github.com/opensearch-project/anomaly-detection/pull/678))
* Add groupId = org.opensearch.plugin ([#690](https://github.com/opensearch-project/anomaly-detection/pull/690))
* Bump jackson-databind to 2.13.4.2 ([#697](https://github.com/opensearch-project/anomaly-detection/pull/697))


### OpenSearch Common Utils
* Fix snakeyaml vulnerability issue by disabling detekt([#237](https://github.com/opensearch-project/common-utils/pull/237))
* Upgrade 2.x to 2.4 ([#246](https://github.com/opensearch-project/common-utils/pull/246))
* Remove force snakeyaml removal ([#263](https://github.com/opensearch-project/common-utils/pull/263))


### OpenSearch Cross Cluster Replication 
* Add support for windows & mac build ([591](https://github.com/opensearch-project/cross-cluster-replication/pull/591))
* Add groupId = org.opensearch.plugin ([589](https://github.com/opensearch-project/cross-cluster-replication/pull/589))
* Upgrade Snakeyml and Jackson ([574](https://github.com/opensearch-project/cross-cluster-replication/pull/574))


### OpenSearch Dashboards Maps
* Add windows and mac platform to run unit test  ([#74](https://github.com/opensearch-project/dashboards-maps/pull/74))


### OpenSearch Dashboards Reports
* Enable windows and macos build ([#504](https://github.com/opensearch-project/dashboards-reports/pull/504))
* Add group = org.opensearch.plugin ([#506](https://github.com/opensearch-project/dashboards-reports/pull/506))


### OpenSearch Dashboards Search Relevance
* Initial copy of files from .github with updates specific to this repo ([#1](https://github.com/opensearch-project/dashboards-search-relevance/pull/1))
* Adding ci workflow ([#12](https://github.com/opensearch-project/dashboards-search-relevance/pull/12))
* Add windows-latest back to test-and-build workflow ([#39](https://github.com/opensearch-project/dashboards-search-relevance/pull/39))
* Configure Mend for GitHub.com ([#49](https://github.com/opensearch-project/dashboards-search-relevance/pull/49))


### OpenSearch Dashboards Visualizations
* Add support for windows and macos ([#117](https://github.com/opensearch-project/dashboards-visualizations/pull/117))


### OpenSearch Geospatial
* Add window and mac platform in CI ([#173](https://github.com/opensearch-project/geospatial/pull/173))
* Fix integration test failure with security enabled cluster ([#138](https://github.com/opensearch-project/geospatial/pull/138))
* Remove explicit dco check ([#126](https://github.com/opensearch-project/geospatial/pull/126))
* Include feature branch in workflow to trigger CI ([#102](https://github.com/opensearch-project/geospatial/pull/102))


### OpenSearch Index Management
* Add group = org.opensearch.plugin ([#571](https://github.com/opensearch-project/index-management/pull/571))


### OpenSearch k-NN
* Fixed failing unit test ([#610](https://github.com/opensearch-project/k-NN/pull/610))
* Disable Code Coverage for Windows and Mac Platforms ([#603](https://github.com/opensearch-project/k-NN/pull/603))
* Update build script to publish to maven local ([#596](https://github.com/opensearch-project/k-NN/pull/596))
* Add Windows Build.sh Related Changes in k-NN ([#595](https://github.com/opensearch-project/k-NN/pull/595))
* Add mac platform to CI ([#590](https://github.com/opensearch-project/k-NN/pull/590))
* Add windows support ([#583](https://github.com/opensearch-project/k-NN/pull/583))


### OpenSearch Ml Commons
* Add groupId to pluginzip publication ([#468](https://github.com/opensearch-project/ml-commons/pull/468))
* Add UT for TransportLoadModelAction ([#490](https://github.com/opensearch-project/ml-commons/pull/490))
* Add integ tests for new APIs: upload/load/unload ([#500](https://github.com/opensearch-project/ml-commons/pull/500))
* Test windows build ([#504](https://github.com/opensearch-project/ml-commons/pull/504))
* Update new small torchscript model for integ test ([#508](https://github.com/opensearch-project/ml-commons/pull/508))
* Add test coverage to transportUploadModelAction ([#511](https://github.com/opensearch-project/ml-commons/pull/511))
* Add more test coverage to ModelHelper and FileUtils ([#510](https://github.com/opensearch-project/ml-commons/pull/510))
* Use small model to run integ test ([#509](https://github.com/opensearch-project/ml-commons/pull/509))
* Add more unit test coverage to output.model and input.parameter in co… ([#517](https://github.com/opensearch-project/ml-commons/pull/517))
* Add test coverage to common package ([#514](https://github.com/opensearch-project/ml-commons/pull/514))
* Add unit tests to improve test coverage in plugin package ([#516](https://github.com/opensearch-project/ml-commons/pull/516))
* Adds security IT for new upload and load APIs ([#529](https://github.com/opensearch-project/ml-commons/pull/529))
* Test coverage ratio changes for build.gradlew in plugin package ([#536](https://github.com/opensearch-project/ml-commons/pull/536))


### OpenSearch Neural Search
* Initial commit for setting up the neural search plugin ([#2](https://github.com/opensearch-project/neural-search/pull/2))
* Fix CI and Link Checker GitHub workflows ([#3](https://github.com/opensearch-project/neural-search/pull/3))
* Enable the K-NN plugin and ML plugin for integ test cluster ([#6](https://github.com/opensearch-project/neural-search/pull/6))
* Add dependency on k-NN plugin ([#10](https://github.com/opensearch-project/neural-search/pull/10))
* Switch pull_request_target to pull_request in CI ([#26](https://github.com/opensearch-project/neural-search/pull/26))
* Fix minor build.gradle issues ([#28](https://github.com/opensearch-project/neural-search/pull/28))
* Fix group id for ml-commons dependency ([#32](https://github.com/opensearch-project/neural-search/pull/32))
* Add Windows support for CI ([#40](https://github.com/opensearch-project/neural-search/pull/40))
* Add opensearch prefix to plugin name ([#38](https://github.com/opensearch-project/neural-search/pull/38))
* Add integration tests for neural query ([#36](https://github.com/opensearch-project/neural-search/pull/36))
* Switch processor IT to use Lucene ([#48](https://github.com/opensearch-project/neural-search/pull/48))
* Add release note draft automation ([#52](https://github.com/opensearch-project/neural-search/pull/52))


### OpenSearch Notifications
* Add groupId to pluginzip publication ([#552](https://github.com/opensearch-project/notifications/pull/552))
* Add build and test workflows for Mac and Windows ([#557](https://github.com/opensearch-project/notifications/pull/557))


### OpenSearch Observability
* Add groupId to pluginzip publication ([#1115](https://github.com/opensearch-project/observability/pull/1115))
* Enable windows and macos builds ([#1108](https://github.com/opensearch-project/observability/pull/1108))


### OpenSearch Security Analytics
* Initial commit for setting up the `opensearch-security-analytics` plugin ([#3](https://github.com/opensearch-project/security-analytics/pull/3))
* Add support for windows builds ([#84](https://github.com/opensearch-project/security-analytics/pull/84))
* Add backport workflow in GitHub workflows ([#93](https://github.com/opensearch-project/security-analytics/pull/93), [#113](https://github.com/opensearch-project/security-analytics/pull/113))
* Change `groupid` in `build.gradle` ([#91](https://github.com/opensearch-project/security-analytics/pull/91))
* Add `build.sh` to generate `maven artifacts` ([#87](https://github.com/opensearch-project/security-analytics/pull/87))


### OpenSearch Security Analytics Dashboards
* Added basic template files related to OpenSearch guidelines, GitHub workflows for running unit and integration tests, badges to the README, and developer guide and easy setup. ([#2](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/2))


### OpenSearch Security Dashboards Plugin
* Add SAML integration tests ([#1088](https://github.com/opensearch-project/security-dashboards-plugin/pull/1088))
* Support CI for Windows and MacOS ([#1164](https://github.com/opensearch-project/security-dashboards-plugin/pull/1164))


### OpenSearch SQL
* Fix failing ODBC workflow ([#828](https://github.com/opensearch-project/sql/pull/828))
* Reorganize GitHub workflows. ([#837](https://github.com/opensearch-project/sql/pull/837))
* Update com.fasterxml.jackson to 2.13.4 to match opensearch repo. ([#858](https://github.com/opensearch-project/sql/pull/858))
* Trigger build on pull request synchronize action. ([#873](https://github.com/opensearch-project/sql/pull/873))
* Update Jetty Dependency ([#872](https://github.com/opensearch-project/sql/pull/872))
* Fix manual CI workflow and add `name` option. ([#904](https://github.com/opensearch-project/sql/pull/904))
* Add groupId to pluginzip publication ([#906](https://github.com/opensearch-project/sql/pull/906))
* Enable ci for windows and macos ([#907](https://github.com/opensearch-project/sql/pull/907))
* Update group to groupId ([#908](https://github.com/opensearch-project/sql/pull/908))
* Enable ignored and disabled tests ([#926](https://github.com/opensearch-project/sql/pull/926))
* Update version of `jackson-databind` for `sql-jdbc` only ([#943](https://github.com/opensearch-project/sql/pull/943))
* Add security policy for ml-commons library ([#945](https://github.com/opensearch-project/sql/pull/945))
* Change condition to always upload coverage for linux workbench ([#967](https://github.com/opensearch-project/sql/pull/967))
* Bump ansi-regex for workbench ([#975](https://github.com/opensearch-project/sql/pull/975))
* Removed json-smart in the JDBC driver ([#978](https://github.com/opensearch-project/sql/pull/978))
* Update MacOS Version for ODBC Driver ([#987](https://github.com/opensearch-project/sql/pull/987))
* Update Jackson Databind version to 2.13.4.2 ([#992](https://github.com/opensearch-project/sql/pull/992))
* [Backport 2.4] Bump sql-cli version to 1.1.0 ([#1024](https://github.com/opensearch-project/sql/pull/1024))


## DOCUMENTATION

### OpenSearch Alerting
* Add 2.4 release notes ([#646](https://github.com/opensearch-project/alerting/pull/646))


### OpenSearch Alerting Dashboards Plugin
* Add 2.4 release notes ([#357](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/357))


### OpenSearch Common Utils
* Added 2.4 release notes. ([#316](https://github.com/opensearch-project/common-utils/pull/316))


### OpenSearch Index Management
* 2.4 release note ([#598](https://github.com/opensearch-project/index-management/pull/598))


### OpenSearch Index Management Dashboards Plugin
* Added release notes for 2.4 ([#346](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/346))


### OpenSearch Job Scheduler
* Added 2.4 release notes. ([#267](https://github.com/opensearch-project/job-scheduler/pull/267))


### OpenSearch k-NN
* Replace Forum link in k-NN plugin README.md ([#540](https://github.com/opensearch-project/k-NN/pull/540))
* Update dev guide with instructions for mac ([#518](https://github.com/opensearch-project/k-NN/pull/518))


### OpenSearch Ml Commons
* Fix readme: remove experimental words ([#431](https://github.com/opensearch-project/ml-commons/pull/431))


### OpenSearch Neural Search
* Add additional maintainers to repo ([#8](https://github.com/opensearch-project/neural-search/pull/8))
* Fix headers in README ([#13](https://github.com/opensearch-project/neural-search/pull/13))


### OpenSearch Security Analytics
* Update `README` ([#1](https://github.com/opensearch-project/security-analytics/pull/1))
* Add `MAINTAINERS.md` file ([#83](https://github.com/opensearch-project/security-analytics/pull/83))


### OpenSearch SQL
* Add Forum link in SQL plugin README.md ([#809](https://github.com/opensearch-project/sql/pull/809))
* Fix indentation of patterns example ([#880](https://github.com/opensearch-project/sql/pull/880))
* Update docs - missing changes for #754. ([#884](https://github.com/opensearch-project/sql/pull/884))
* Fix broken links ([#911](https://github.com/opensearch-project/sql/pull/911))
* Adding docs related to catalog. ([#963](https://github.com/opensearch-project/sql/pull/963))
* SHOW CATALOGS documentation and integ tests ([#977](https://github.com/opensearch-project/sql/pull/977))
* [Backport 2.4] Add document for ml command. ([#1017](https://github.com/opensearch-project/sql/pull/1017))


## MAINTENANCE

### OpenSearch Alerting Dashboards Plugin
* Bumped version to 2.4.0. ([#346](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/346))
* Bumped d3-color version. ([#350](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/350))


### OpenSearch Anomaly Detection
* Bump version to 2.4 ([#666](https://github.com/opensearch-project/anomaly-detection/pull/666))


### OpenSearch Anomaly Detection Dashboards
* Bump to 2.4 ([#328](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/328))


### OpenSearch Asynchronous Search
* Bump version to 2.4.0 ([#181](https://github.com/opensearch-project/asynchronous-search/pull/181))
* Add groupId = org.opensearch.plugin ([#192](https://github.com/opensearch-project/asynchronous-search/pull/192))


### OpenSearch Dashboards Maps
* Version bump to 2.4 for dependent packages ([#86](https://github.com/opensearch-project/dashboards-maps/pull/86))
* Bump version to 2.4.0.0 ([#70](https://github.com/opensearch-project/dashboards-maps/pull/70))


### OpenSearch Dashboards Reports
* Bump verison to 2.4.0 ([#499](https://github.com/opensearch-project/dashboards-reports/pull/499))


### OpenSearch Dashboards Visualizations
* Version bump to 2.4.0 ([#121](https://github.com/opensearch-project/dashboards-visualizations/pull/121))


### OpenSearch Geospatial
* Increment version to 2.4.0-SNAPSHOT ([#139](https://github.com/opensearch-project/geospatial/pull/139))
* Update to Gradle 7.5.1 ([#134](https://github.com/opensearch-project/geospatial/pull/134))


### OpenSearch Index Management
* Fix kotlin warnings ([#551](https://github.com/opensearch-project/index-management/pull/551))
* Update jackson to 2.13.4 ([#557](https://github.com/opensearch-project/index-management/pull/557))
* Increment version to 2.4.0-SNAPSHOT ([#573](https://github.com/opensearch-project/index-management/pull/573))
* Fix the compatibility issue of awareness replica validation ([#595](https://github.com/opensearch-project/index-management/pull/595))


### OpenSearch Index Management Dashboards Plugin
* Version bump 2.4.0 ([#283](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/283))
* Add windows mac OS in CI ([#325](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/325))
* Refactor: move api calls from components to containers ([#322](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/322))


### OpenSearch Job Scheduler
* Testing ci ([#264](https://github.com/opensearch-project/job-scheduler/pull/264)) ([#265](https://github.com/opensearch-project/job-scheduler/pull/265))
* Add slf4j which is the dep of cronutils. ([#256](https://github.com/opensearch-project/job-scheduler/pull/256)) ([#257](https://github.com/opensearch-project/job-scheduler/pull/257))
* Add group = org.opensearch.plugin. ([#251](https://github.com/opensearch-project/job-scheduler/pull/251)) ([#255](https://github.com/opensearch-project/job-scheduler/pull/255))
* Updating CronUtils due to glassfish CVE. ([#245](https://github.com/opensearch-project/job-scheduler/pull/245)) ([#246](https://github.com/opensearch-project/job-scheduler/pull/246))
* Increment version to 2.4.0-SNAPSHOT. ([#241](https://github.com/opensearch-project/job-scheduler/pull/241))


### OpenSearch k-NN
* Backport lucene changes ([#575](https://github.com/opensearch-project/k-NN/pull/575))
* Increment version to 2.4.0-SNAPSHOT ([#545](https://github.com/opensearch-project/k-NN/pull/545))


### OpenSearch Ml Commons
* Increment version to 2.4.0-SNAPSHOT ([#422](https://github.com/opensearch-project/ml-commons/pull/422))
* Address CVE-2022-42889 by updating commons-text ([#487](https://github.com/opensearch-project/ml-commons/pull/487))


### OpenSearch Neural Search
* Upgrade plugin to 2.4 and refactor zip dependencies ([#25](https://github.com/opensearch-project/neural-search/pull/25))


### OpenSearch Notifications
* Upgrade Notifications and Notifications Dashboards to 2.4 ([#536](https://github.com/opensearch-project/notifications/pull/536))


### OpenSearch Observability
* Bump version to 2.4.0 ([#1071](https://github.com/opensearch-project/observability/pull/1071))


### OpenSearch Performance Analyzer
* Update netty and gson ([#274](https://github.com/opensearch-project/performance-analyzer/pull/274)) ([#280](https://github.com/opensearch-project/performance-analyzer/pull/280))
* Update jackson to 2.13.4 ([#293](https://github.com/opensearch-project/performance-analyzer/pull/293))
* Add group = org.opensearch.plugin ([#304](https://github.com/opensearch-project/performance-analyzer/pull/304)) ([#305](https://github.com/opensearch-project/performance-analyzer/pull/305))
* Address CVE-2022-42003 ([#312](https://github.com/opensearch-project/performance-analyzer/pull/312))
* Deprecate master nomenclature in 2.x ([#319](https://github.com/opensearch-project/performance-analyzer/pull/319))


### OpenSearch Security Analytics Dashboards
* Added changes for releasing plugin with OSD as part of 2.4. ([#6](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/6))


### OpenSearch Security
* Add groupId = org.opensearch.plugin ([#2158](https://github.com/opensearch-project/security/pull/2158)[#2185](https://github.com/opensearch-project/security/pull/2185))
* Roles yml changes for security-analytics plugin ([#2192](https://github.com/opensearch-project/security/pull/2192)[#2225](https://github.com/opensearch-project/security/pull/2225))
* Upgrade Kafka Client to 3.0.2 ([#2123](https://github.com/opensearch-project/security/pull/2123)[#2126](https://github.com/opensearch-project/security/pull/2126))
* Log deprecation message on legacy ldap pool settings ([#2099](https://github.com/opensearch-project/security/pull/2099)[#2147](https://github.com/opensearch-project/security/pull/2147))
* Address CVE-2022-42889 by updating commons-text ([#2177](https://github.com/opensearch-project/security/pull/2177)[#2186](https://github.com/opensearch-project/security/pull/2186))
* Patch bump for scala dependency ([#2163](https://github.com/opensearch-project/security/pull/2163)[#2187](https://github.com/opensearch-project/security/commit/1f3de6a064696eb098749a340853c4f6af4c619f))
* Woodstox Version Bump to 6.4.0 ([#2197](https://github.com/opensearch-project/security/pull/2197)[#2199](https://github.com/opensearch-project/security/pull/2199))


### OpenSearch Security Dashboards Plugin
* Increment version to 2.4.0.0 ([#1096](https://github.com/opensearch-project/security-dashboards-plugin/pull/1096))
* Configure new ML plugin actions ([#1182](https://github.com/opensearch-project/security-dashboards-plugin/pull/1182))


## REFACTORING

### OpenSearch Alerting
* Moving over data models from alerting to common-utils ([#556](https://github.com/opensearch-project/alerting/pull/556]))
* Expose delete monitor api from alerting ([#568](https://github.com/opensearch-project/alerting/pull/568]))
* Use findings and alerts models, dtos from common utils ([#569](https://github.com/opensearch-project/alerting/pull/569]))
* Recreate request object from writeable for Get alerts and get findings ([#577](https://github.com/opensearch-project/alerting/pull/577]))
* Use acknowledge alert request,response, actions from common-utils dependencies ([#606](https://github.com/opensearch-project/alerting/pull/606]))
* Expose delete monitor api from alerting ([#568](https://github.com/opensearch-project/alerting/pull/568]))
* Refactored DeleteMonitor Action to be synchronious ([#628](https://github.com/opensearch-project/alerting/pull/628]))


### OpenSearch Common Utils
* Move Alerting data models over to common-utils ([#242](https://github.com/opensearch-project/common-utils/pull/242))
* Copy over monitor datasources config from alerting to common utils ([#247](https://github.com/opensearch-project/common-utils/pull/247))
* Expose delete monitor api from alerting ([#251](https://github.com/opensearch-project/common-utils/pull/251))
* Move Findings and Alerts action, request, response and models from alerting to common-utils ([#254](https://github.com/opensearch-project/common-utils/pull/254))
* Move acknowledge alerts dtos from alerting to common-utils ([#283](https://github.com/opensearch-project/common-utils/pull/282))


### OpenSearch Geospatial
* Remove optional to get features ([#177](https://github.com/opensearch-project/geospatial/pull/177))


### OpenSearch k-NN
* Refactor kNN codec related classes ([#582](https://github.com/opensearch-project/k-NN/pull/582))
* Refactor unit tests for codec ([#562](https://github.com/opensearch-project/k-NN/pull/562))


### OpenSearch Neural Search
* Refactor project package structure ([#55](https://github.com/opensearch-project/neural-search/pull/55))
