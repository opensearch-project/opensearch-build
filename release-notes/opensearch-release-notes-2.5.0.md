# OpenSearch and OpenSearch Dashboards 2.5.0 Release Notes

## Release Highlights

The OpenSearch 2.5.0 release adds new tools and enhancements to help you advance your search, analytics, and observability workloads. This release includes the software’s first Debian distribution and first administrative user interface, along with support for multi-layered maps and the ability to analyze traces in the Jaeger schema. The release also includes indexing and search improvements for Lucene-based k-NN search functionality, and Security Analytics tools are now generally available. Following are some highlights for this release.

### New Features

* You can now perform common administrative operations on your OpenSearch indexes, such as CRUD (Create, Read, Update, and Delete) functions, through an admin user interface.
* OpenSearch 2.5.0 lets you analyze trace data collected by the open-source Jaeger solution. Select Data Prepper or Jaeger as your trace data source as part of the OpenSearch Dashboards Observability feature.
* With this release, Security Analytics for OpenSearch and OpenSearch Dashboards is generally available, offering a number of tools to help users protect their data and infrastructure.
* You can build multi-layer maps from multiple data sources, combining data from different indexes into a single visualization to identify correlations and gain insights into geospatial data.
* New Debian distributions let you deploy OpenSearch and OpenSearch Dashboards directly on servers running Debian-based Linux distributions.
* Administrators can now view the health of their cluster at the awareness attribute level when shard allocation awareness is configured.
* You can now search your rollup indexes using query string search queries.

### Experimental Features

OpenSearch 2.5.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, see the version history (https://opensearch.org/docs/latest/version-history/) page which includes links to the documentation.
* Request-level durability allows you to deploy remote-backed storage on a per-index basis, supporting data durability for cloud-based backup and restore operations.
* As an enhancement to semantic search functionality, the model-serving framework now allows users to serve machine learning (ML) models on ML nodes that can take advantage of CUDA-compatible GPUs.

## Release Details

[OpenSearch and OpenSearch Dashboards 2.5.0](https://opensearch.org/versions/opensearch-2-5-0.html) includes the following feature, enhancement, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.5.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.5.0.md).


## FEATURE

### OpenSearch Dashboards Maps
* Add tooltip for hover ([#132](https://github.com/opensearch-project/dashboards-maps/pull/132))
* Introduce tooltip fields to document layer specification ([#124](https://github.com/opensearch-project/dashboards-maps/pull/124))
* Add support for WKT format ([#165](https://github.com/opensearch-project/dashboards-maps/pull/165))
* Add global time filter bar to maps ([#131](https://github.com/opensearch-project/dashboards-maps/pull/131))
* Support custom layer for maps ([#150](https://github.com/opensearch-project/dashboards-maps/pull/150))
* Support geo_shape visualization in documents layer ([#111](https://github.com/opensearch-project/dashboards-maps/pull/111))
* Introduce saved object plugin into maps plugin ([#67](https://github.com/opensearch-project/dashboards-maps/pull/67))
* Add new layer functions for OpenSearch map layer ([#66](https://github.com/opensearch-project/dashboards-maps/pull/66))
* Add map page and add basic layers panel ([#40](https://github.com/opensearch-project/dashboards-maps/pull/40))
* Add layer panel component ([#51](https://github.com/opensearch-project/dashboards-maps/pull/51))
* Add base map layer functions ([#62](https://github.com/opensearch-project/dashboards-maps/pull/62))
* Query with geo bounding box ([#148](https://github.com/opensearch-project/dashboards-maps/pull/148))
* Display search filters in map layer config panel ([#130](https://github.com/opensearch-project/dashboards-maps/pull/130))


### OpenSearch Observability Dashboards Plugin
* Add log pattern table ([#1187](https://github.com/opensearch-project/observability/pull/1187))
* Implementing search feature ([#1286](https://github.com/opensearch-project/observability/pull/1286))
* Add support for raw Jaeger schema data ([#150](https://github.com/opensearch-project/dashboards-observability/pull/150))


### OpenSearch Index Management Dashboards Plugin
* Add index administrative operations ([#537](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/537))


### OpenSearch Job Scheduler
* Support for spotlessApply for Job Scheduler ([#291](https://github.com/opensearch-project/job-scheduler/pull/291))


### OpenSearch ML Commons
* Add native memory circuit breaker. ([#689](https://github.com/opensearch-project/ml-commons/pull/689))


### OpenSearch Security Analytics
* Implement secure transport action for get alerts and ack alerts. ([#161](https://github.com/opensearch-project/security-analytics/pull/161))
* GetMappingsView API - index pattern/alias/datastream support. ([#245](https://github.com/opensearch-project/security-analytics/pull/245))
* Createmappings api index pattern support. ([#260](https://github.com/opensearch-project/security-analytics/pull/260))


### OpenSearch Security Analytics Dashboards
* Refactoring | Updates overview stats components to use EUI/Stats loading component. ([#194](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/194))
* Update chart legend font size and padding. ([#196](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/196))
* YAML Rule Editor Support. ([#201](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/201))
* Adds dynamic chart time unit based on the selected time span. ([#204](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/204))
* Rule YAML preview. ([#209](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/209))
* Feature/detector navigation to findings and alerts. ([#210](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/210))
* Show surrounding documents when index pattern is available; Finding flyout UI polish. ([#216](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/216))
* Rule flyout opening from Findings and Alerts page. ([#219](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/219))
* Show success toast when detector is updated. ([#224](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/224))
* Add chart tooltips. ([#225](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/225))
* Add interactive legend into charts. ([#226](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/226))
* Implement date/time picker on the overview page. ([#232](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/232))
* Rule details flyout on create rule page. ([#236](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/236))
* Add loading state for all tables visualizations on overview page. ([#237](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/237))
* Toggle all rules button on detector edit page. ([#239](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/239))
* Rule form validation on submit. ([#264](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/264))
* Feature/charts should show the entire time range selected in the filter. ([#265](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/265))
* Rule details flyout on detector create 4th step. ([#266](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/266))
* More validations on YAML rule editor. ([#279](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/279))
* Rule details flyout on detector view page. ([#292](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/292))
* Improve rules view in detector details. ([#310](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/310))
* Adds findings alerts legend in overview page. ([#318](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/318))
* Feature/hide view docs button. ([#320](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/320))
* Improved field mapping UX. ([#330](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/330))
* Data source single select field. ([#333](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/333))
* Suppressed unnecessary error toast for custom rules. ([#338](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/338))


## ENHANCEMENT

### OpenSearch Anomaly Detection
* Speed up cold start ([#753](https://github.com/opensearch-project/anomaly-detection/pull/753))


### OpenSearch Cross Cluster Replication
* Support for indices clean-up after the test runs ([625](https://github.com/opensearch-project/cross-cluster-replication/pull/625))
* Stopping replication before clean up of indices ([635](https://github.com/opensearch-project/cross-cluster-replication/pull/635))


### OpenSearch Dashboards Maps
* Support other geopoint formats ([#144](https://github.com/opensearch-project/dashboards-maps/pull/144))
* Add reorder handle inside layer panel ([#116](https://github.com/opensearch-project/dashboards-maps/pull/116))
* Update show/hide icon ([#114](https://github.com/opensearch-project/dashboards-maps/pull/114))
* Update basic layer settings ([#107](https://github.com/opensearch-project/dashboards-maps/pull/107))
* Delete layer modal ([#139](https://github.com/opensearch-project/dashboards-maps/pull/139))
* Add multi-layer support to map popup ([#140](https://github.com/opensearch-project/dashboards-maps/pull/140))
* Support overriding maps config from OSD config yml file ([#202](https://github.com/opensearch-project/dashboards-maps/pull/202))


### OpenSearch Dashboards Reporting
* Use front-end report generation instead of chromium ([#586](https://github.com/opensearch-project/reporting/pull/586))


### OpenSearch Index Management
* Added support for QueryStringQuery in rollups ([#616](https://github.com/opensearch-project/index-management/pull/616))


### OpenSearch k-NN
* Extend SystemIndexPlugin for k-NN model system index ([#630](https://github.com/opensearch-project/k-NN/pull/630))
* Add Lucene specific file extensions to core HybridFS ([#721](https://github.com/opensearch-project/k-NN/pull/721))


### OpenSearch ML Commons
* Add more parameters for text embedding model ([#640](https://github.com/opensearch-project/ml-commons/pull/640))
* Add more pooling method and refactor ([#672](https://github.com/opensearch-project/ml-commons/pull/672))
* Add ML task timeout setting and clean up expired tasks from cache ([#662](https://github.com/opensearch-project/ml-commons/pull/662))
* Change only run on ml node setting default value to true ([#686](https://github.com/opensearch-project/ml-commons/pull/686))


### OpenSearch Neural Search
* Add filter option for query type ([#88](https://github.com/opensearch-project/neural-search/pull/88))
* Add retry mechanism for neural search inference ([#91](https://github.com/opensearch-project/neural-search/pull/91))
* Enable core branching strategy and make Neural Plugin as extensible plugin. ([#87](https://github.com/opensearch-project/neural-search/pull/87))


### OpenSearch Job Scheduler
* Increasing thread sleep for tests to 100,000 ([#294](https://github.com/opensearch-project/job-scheduler/pull/294))


### OpenSearch Observability
* Add more metrics for backend plugin ([#1323](https://github.com/opensearch-project/observability/pull/1323))


### OpenSearch Observability Dashboards Plugin
* Add metrics framework for frontend and backend ([#1306](https://github.com/opensearch-project/observability/pull/1306))
* Add more metrics to frontend ([#1326](https://github.com/opensearch-project/observability/pull/1326))


### OpenSearch Security
* When excluding fields also exclude the term + .keyword ([#2377](https://github.com/opensearch-project/security/pull/2377))
* Update tool scripts to run in windows ([#2371](https://github.com/opensearch-project/security/pull/2371), [#2379](https://github.com/opensearch-project/security/pull/2379))
* Remove trimming of whitespace when extracting SAML backend roles ([#2381](https://github.com/opensearch-project/security/pull/2381), [#2383](https://github.com/opensearch-project/security/pull/2383))
* Add script for workflow version increment ([#2374](https://github.com/opensearch-project/security/pull/2374), [#2386](https://github.com/opensearch-project/security/pull/2386))


### OpenSearch Security Dashboards Plugin
* Enhance the stability of SAML integ test ([#1237](https://github.com/opensearch-project/security-dashboards-plugin/pull/1237), [#1272](https://github.com/opensearch-project/security-dashboards-plugin/pull/1272))
* Change the reference branch to 2.5 for Cypress test ([#1298](https://github.com/opensearch-project/security-dashboards-plugin/pull/1298))


### OpenSearch SQL
* Add low-level create table and table exists API ([#834](https://github.com/opensearch-project/sql/issues/834))
* Add time window and window assigner ([#950](https://github.com/opensearch-project/sql/issues/950))
* Add valueOf() to Expression ([#1055](https://github.com/opensearch-project/sql/issues/1055))
* Add Statement, QueryExecution and QueryManager ([#845](https://github.com/opensearch-project/sql/issues/845))
* Add Streaming Source Impl ([#994](https://github.com/opensearch-project/sql/issues/994))
* Add watermark generator ([#959](https://github.com/opensearch-project/sql/issues/959))
* Add stream context and window trigger ([#958](https://github.com/opensearch-project/sql/issues/958))
* Add micro batch streaming execution ([#1044](https://github.com/opensearch-project/sql/pull/1044))
* Add Streaming Plan Implementation ([#1068](https://github.com/opensearch-project/sql/issues/1068))
* Add CBRT to the V2 engine ([#1081](https://github.com/opensearch-project/sql/issues/1081))
* Add CBRT function to the PPL ([#1097](https://github.com/opensearch-project/sql/issues/1097))
* Add timeout option to SQL CLI tool. ([#1076](https://github.com/opensearch-project/sql/issues/1076))
* Add Day_Of_Year Function To OpenSearch ([#1128](https://github.com/opensearch-project/sql/issues/1128))
* Add Week_Of_Year Function To OpenSearch ([#1127](https://github.com/opensearch-project/sql/issues/1127))
* Add Month_Of_Year Function To OpenSearch ([#1129](https://github.com/opensearch-project/sql/issues/1129))
* Add Minute_Of_Day Function To SQL Plugin ([#1207](https://github.com/opensearch-project/sql/issues/1207) [#1214](https://github.com/opensearch-project/sql/issues/1214))
* Add Second_Of_Minute Function As An Alias Of The Second Function ([#1231](https://github.com/opensearch-project/sql/issues/1231) [#1237](https://github.com/opensearch-project/sql/issues/1237))
* Add Support For Legacy Syntax For Match Function In New Engine ([#1090](https://github.com/opensearch-project/sql/issues/1090))
* Add MatchPhraseQuery As Alternate Syntax for Match_Phrase Function ([#1103](https://github.com/opensearch-project/sql/issues/1103))
* Use query execution start time as the value of now-like functions. ([#1047](https://github.com/opensearch-project/sql/issues/1047))
* Add Support for Alternate Legacy MULTIMATCH syntax ([#1102](https://github.com/opensearch-project/sql/issues/1102))
* Add position() function to V2 engine  ([#1121](https://github.com/opensearch-project/sql/issues/1121))
* Add position() string function to PPL ([#1147](https://github.com/opensearch-project/sql/issues/1147))
* Add support for wildcard_query function to the new engine ([#156](https://github.com/opensearch-project/sql/issues/156) [#1108](https://github.com/opensearch-project/sql/issues/1108))
* Add reverse() string function to V2 SQL Engine([#1154](https://github.com/opensearch-project/sql/issues/1154))
* Add table write operator and builder ([#1094](https://github.com/opensearch-project/sql/issues/1094))
* Add BETWEEN expression in v2 engine ([#1163](https://github.com/opensearch-project/sql/issues/1163))
* Adding UTC_DATE, UTC_TIME, UTC_TIMESTAMP ([#1193](https://github.com/opensearch-project/sql/issues/1193) [#1198](https://github.com/opensearch-project/sql/issues/1198))
* Validate field and fields parameters in relevance search functions ([#1067](https://github.com/opensearch-project/sql/issues/1067) [#1199](https://github.com/opensearch-project/sql/issues/1199))
* Add `TIMEDIFF` and `DATEDIFF` functions. ([#131](https://github.com/opensearch-project/sql/issues/131) [#1195](https://github.com/opensearch-project/sql/issues/1195) [#1234](https://github.com/opensearch-project/sql/issues/1234))
* Add functions `ADDTIME` and `SUBTIME`. ([#132](https://github.com/opensearch-project/sql/issues/132) [#1194](https://github.com/opensearch-project/sql/issues/1194) [#1252](https://github.com/opensearch-project/sql/issues/1252))
* Add Day_Of_Week Function As An Alias Of DayOfWeek ([#190](https://github.com/opensearch-project/sql/issues/190) [#1228](https://github.com/opensearch-project/sql/issues/1228) [#1239](https://github.com/opensearch-project/sql/issues/1239))
* Add Minute_Of_Hour Function As An Alias Of Minute Function ([#1253](https://github.com/opensearch-project/sql/issues/1253))
* Add support for long value return for CEIL, CEILING and FLOOR math functions ([#1205](https://github.com/opensearch-project/sql/issues/1205))
* Add Alternate Syntax For Match_Query And Other Functions ([#1166](https://github.com/opensearch-project/sql/issues/1166))
* Add Support For `TIME` Type in DAY_OF_YEAR Functions ([#199](https://github.com/opensearch-project/sql/issues/199) [#1223](https://github.com/opensearch-project/sql/issues/1223) [1#258](https://github.com/opensearch-project/sql/issues/1258))
* Add Day_Of_Month Function As An Alias Of DayOfMonth ([#1227](https://github.com/opensearch-project/sql/issues/1227) [#1265](https://github.com/opensearch-project/sql/issues/1265))
* Add security patch for CVE-2020-15250 ([#1095](https://github.com/opensearch-project/sql/issues/1095))
* Add security patch for CVE-2022-45868 ([#1107](https://github.com/opensearch-project/sql/issues/1107))
* Add Hour_Of_Day Function As An Alias Of Hour ([#1226](https://github.com/opensearch-project/sql/issues/1226) [#1270](https://github.com/opensearch-project/sql/issues/1270))

## BUG FIXES

### OpenSearch Alerting
* Added support for "nested" mappings. ([#645](https://github.com/opensearch-project/alerting/pull/645))
* Create findingIndex bugfix. ([#653](https://github.com/opensearch-project/alerting/pull/653))
* Fix bucket level monitor findings to support term aggs in query. ([#666](https://github.com/opensearch-project/alerting/pull/666))
* Mappings traversal bug fix. ([#669](https://github.com/opensearch-project/alerting/pull/669))
* Set message when building LegacyCustomWebhookMessage. ([#670](https://github.com/opensearch-project/alerting/pull/670))
* Fix error message bug to show the correct destination ID that's missing. ([#685](https://github.com/opensearch-project/alerting/pull/685))
* Fix percolator mapping error when having field name 'type'. ([#726](https://github.com/opensearch-project/alerting/pull/726))


### OpenSearch Anomaly Detection
* Fix _source bug ([#749](https://github.com/opensearch-project/anomaly-detection/pull/749))
* Fix the discrepancy between Profile API and real time tasks API ([#770](https://github.com/opensearch-project/anomaly-detection/pull/770))


### OpenSearch Anomaly Detection Dashboards
* [Forward port to main] removed duplicate popout icon and ran prettier (#379) ([#382](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/382))
* Change detector out of time range modal warning into a callout warning ([#384](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/384))
* Fix undefined entity list when heatmap is empty ([#383](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/383))


### OpenSearch Cross Cluster Replication
* Updating multi-field mapping at follower ([686](https://github.com/opensearch-project/cross-cluster-replication/pull/686))


### OpenSearch Job Scheduler
* Fixing CI workflow to run on matrix.os ([#292](https://github.com/opensearch-project/job-scheduler/pull/292))


### OpenSearch Observability Dashboards Plugin
* Fix event analytics field blank margin ([#174](https://github.com/opensearch-project/dashboards-observability/pull/174))
* Correct ppl learn more link ([#154](https://github.com/opensearch-project/dashboards-observability/pull/154))
* Fixed PPL Error in containers \& added tool tip to date picker ([#179](https://github.com/opensearch-project/dashboards-observability/pull/179))
* Fix explorer dark mode issue and restructure scss ([#157](https://github.com/opensearch-project/dashboards-observability/pull/157))
* Few fixes regarding issues for visualization rendering ([#186](https://github.com/opensearch-project/dashboards-observability/pull/186))
* Fix bug with overriding patterns ([#1298](https://github.com/opensearch-project/observability/pull/1298))
* QS to 6.5.3 ([#1335](https://github.com/opensearch-project/observability/pull/1335))


### OpenSearch Query Workbench
* Bump json5 from 2.2.1 to 2.2.3 ([#20](https://github.com/opensearch-project/dashboards-query-workbench/pull/20))


### OpenSearch Dashboards Reporting
* Upgrade dompurify to 2.4.1  ([#587](https://github.com/opensearch-project/reporting/pull/587))
* Use advanced settings for leading wildcards in query for csv reports ([#549](https://github.com/opensearch-project/reporting/pull/549))
* Upgrade json5 and glob-parent ([#17](https://github.com/opensearch-project/dashboards-reporting/pull/17))


### OpenSearch Dashboards Visualizations
* [FIX-149] Sanitise duration value ([#150](https://github.com/opensearch-project/dashboards-visualizations/pull/150))


### OpenSearch Index Management Dashboards Plugin
* [Bugfix] filter data streams from rollover alias requirement ([#429](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/429))


### OpenSearch k-NN
* Add fix to fromXContent and toXContent in ModelGraveyard ([#624](https://github.com/opensearch-project/k-NN/pull/624))
* Allow mapping service to be null for scenarios of shard recovery from translog ([#685](https://github.com/opensearch-project/k-NN/pull/685))
* Add backward compatibility and validation checks to ModelGraveyard XContent bug fix ([#692](https://github.com/opensearch-project/k-NN/pull/692))


### OpenSearch Observability
* Removing explicit jackson dependencies ([#1352](https://github.com/opensearch-project/observability/pull/1352))
* Upgrade detekt for CVE fix ([#1353](https://github.com/opensearch-project/observability/pull/1353))

### OpenSearch Performance Analyzer
* Add Connection read timeout to prevent indefinite wait ([#354](https://github.com/opensearch-project/performance-analyzer/pull/354))


### OpenSearch Reporting
* Remove jackson-databind and jackson-annotations ([#587](https://github.com/opensearch-project/reporting/pull/587))
* Fix metrics tests and ClassNotFoundException when calling stats API ([#546](https://github.com/opensearch-project/reporting/pull/546))


### OpenSearch Security Analytics
* Fixed aliases being returned in unmapped_index_fields. ([#147](https://github.com/opensearch-project/security-analytics/pull/147))
* Fix vulnerability in yaml constructor. ([#198](https://github.com/opensearch-project/security-analytics/pull/198))
* Fix flaky integration tests for security analytics. ([#241](https://github.com/opensearch-project/security-analytics/pull/241))
* Fixed SecureFindingRestApiIT. Removed uppercasing of the detector type. ([#247](https://github.com/opensearch-project/security-analytics/pull/247))
* Fix ci builds for security-analytics. ([#253](https://github.com/opensearch-project/security-analytics/pull/253))


### OpenSearch Security Analytics Dashboards
* Alerts and Findings overview table should have even height. ([#250](https://github.com/opensearch-project/security-analytics-dashboards-plugin/issues/250))
* Fix cypress flaky tests. ([#261](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/261))
* Fetch only Rules matching Rule Types. ([#262](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/262))
* Edit detector rules table paging goes to page the first page. ([#270](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/270))
* Cypress windows tests fix. ([#296](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/296))
* Wait for field mapping creation to succeed before detector creation API call. ([#317](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/317))
* Fixed styling issues. ([#322](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/322))
* Patch missing detector_id with data already on UI. ([#328](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/328))


### OpenSearch Security
* Changing logging type to give warning for basic auth with no creds ([#2347](https://github.com/opensearch-project/security/pull/2347), [#2364](https://github.com/opensearch-project/security/pull/2364))


### OpenSearch Security Dashboards Plugin
* Fix tenant label for custom tenant when both Global and Private tenants are disabled ([#1277](https://github.com/opensearch-project/security-dashboards-plugin/pull/1277), [#1280](https://github.com/opensearch-project/security-dashboards-plugin/pull/1280))
* Fix openid redirect issue to use base_redirect_url when nextUrl is absent ([#1282](https://github.com/opensearch-project/security-dashboards-plugin/pull/1282), [#1283](https://github.com/opensearch-project/security-dashboards-plugin/pull/1283))
* Add Notifications cluster permissions ([#1290](https://github.com/opensearch-project/security-dashboards-plugin/pull/1290), [#1291](https://github.com/opensearch-project/security-dashboards-plugin/pull/1291))
* Fix regression in jwt url parameter by awaiting async getAdditionalAuthHeader ([#1292](https://github.com/opensearch-project/security-dashboards-plugin/pull/1292), [#1296](https://github.com/opensearch-project/security-dashboards-plugin/pull/1296))


### OpenSearch SQL
* Fix `FLOAT` -> `DOUBLE` cast. ([#1025](https://github.com/opensearch-project/sql/issues/1025))
* Fix error messaging from prometheus. ([#1029](https://github.com/opensearch-project/sql/issues/1029) [#1037](https://github.com/opensearch-project/sql/issues/1037))
* Add `query` function as alternate syntax to `query_string` function ([#1010](https://github.com/opensearch-project/sql/issues/1010))
* Deprecate span collector ([#990](https://github.com/opensearch-project/sql/issues/990))
* Back quote fix ([#1041](https://github.com/opensearch-project/sql/issues/1041) [#1050](https://github.com/opensearch-project/sql/issues/1050))
* Update DATE and TIME functions to parse string input as datetime ([#991](https://github.com/opensearch-project/sql/issues/991))
* Integ tests fix for arm64 ([#1069](https://github.com/opensearch-project/sql/issues/1069))
* Fix history file usage in SQL CLI tool. ([#1077](https://github.com/opensearch-project/sql/issues/1077))
* Update Jackson to 2.14.1 and fix dependency resolution issues ([#1150](https://github.com/opensearch-project/sql/issues/1150))
* Change LIKE operator case-insensitive match ([#1160](https://github.com/opensearch-project/sql/issues/1160))
* Fix arithmetic operator precedence ([#1172](https://github.com/opensearch-project/sql/issues/1172) [#1188](https://github.com/opensearch-project/sql/issues/1188))
* Fix back quoted alias of FROM subquery ([#1189](https://github.com/opensearch-project/sql/issues/1189) [#1208](https://github.com/opensearch-project/sql/issues/1208))
* Fix truncate function ([#1197](https://github.com/opensearch-project/sql/issues/1197) [#1213](https://github.com/opensearch-project/sql/issues/1213))
* Allow common keywords and scalar function name used as identifier ([#1191](https://github.com/opensearch-project/sql/issues/1191) [#1212](https://github.com/opensearch-project/sql/issues/1212))
* Suppress report uploading failure in CI. ([#1180](https://github.com/opensearch-project/sql/issues/1180) [#1220](https://github.com/opensearch-project/sql/issues/1220))
* Fixed error with single timestamp query ([#1244](https://github.com/opensearch-project/sql/issues/1244) [#1246](https://github.com/opensearch-project/sql/issues/1246) [#1249](https://github.com/opensearch-project/sql/issues/1249))
* Support JOIN query on object field with unexpanded name ([#1229](https://github.com/opensearch-project/sql/issues/1229) [#1250](https://github.com/opensearch-project/sql/issues/1250))
* Bug fix for less than and greater than operators on @timestamp ([#1267](https://github.com/opensearch-project/sql/issues/1267) [#1272](https://github.com/opensearch-project/sql/issues/1267))


## INFRASTRUCTURE

### OpenSearch Alerting Dashboards Plugin
* Refactored the help text elements displayed when users access the destinations list page after destinations deprecation. ([#413](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/413))


### OpenSearch Anomaly Detection
* Model Profile Test ([#748](https://github.com/opensearch-project/anomaly-detection/pull/748))
* Add option to run BWC tests in distribution level ([#766](https://github.com/opensearch-project/anomaly-detection/pull/766))


### OpenSearch Anomaly Detection Dashboards
* Add branch constants in CI workflow ([#345](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/345))
* Bump to 2.5.0; add constants in CI workflow ([#346](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/346))
* Bump decode-uri-component ([#359](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/359))
* Add windows env to integration test workflow ([#390](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/390))
* Bump json5 to 2.2.3 ([#393](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/393))


### OpenSearch Dashboards Search Relevance
* Unit Test Coverage Threshold ([#101](https://github.com/opensearch-project/dashboards-search-relevance/pull/101))


### OpenSearch Observability Dashboards Plugin
* Change github actions file and add necessary files ([#4](https://github.com/opensearch-project/dashboards-observability/pull/4))


### OpenSearch Query Workbench
* Add .whitesource configuration file ([#1](https://github.com/opensearch-project/dashboards-query-workbench/pull/17))


### OpenSearch Dashboards Reporting
* Fix windows and macos CI ([#569](https://github.com/opensearch-project/reporting/pull/569))


### OpenSearch k-NN
* Add benchmark workflow for queries with filters ([#598](https://github.com/opensearch-project/k-NN/pull/598))
* Fix failing codec unit test ([#610](https://github.com/opensearch-project/k-NN/pull/610))
* Update bwc tests for 2.5.0 ([#661](https://github.com/opensearch-project/k-NN/pull/661))
* Add release configs for lucene filtering ([#663](https://github.com/opensearch-project/k-NN/pull/663))
* Update backwards compatibility versions ([#701](https://github.com/opensearch-project/k-NN/pull/701))
* Update tests for backwards codecs ([#710](https://github.com/opensearch-project/k-NN/pull/710))


### OpenSearch ML Commons
* Unit tests coverage for load/unload/syncup ([#592](https://github.com/opensearch-project/ml-commons/pull/592))
* Add .whitesource configuration file ([#626](https://github.com/opensearch-project/ml-commons/pull/626))
* Bump djl to 0.20 and add onnxruntime-gpu dependency ([#644](https://github.com/opensearch-project/ml-commons/pull/644))
* Remove jackson-databind and jackson-annotations dependencies now coming from core ([#652](https://github.com/opensearch-project/ml-commons/pull/652))
* Revert "Remove jackson-databind and jackson-annotations dependencies now coming from core" ([#687](https://github.com/opensearch-project/ml-commons/pull/687))
* Adding backwards compatibility test for ml-commons plugin ([#681](https://github.com/opensearch-project/ml-commons/pull/681))
* Change the inheritance of the BWC test file ([#692](https://github.com/opensearch-project/ml-commons/pull/692))


### OpenSearch Observability
* Include integration tests in windows and macOS workflow ([#1375](https://github.com/opensearch-project/observability/pull/1375))
* Remove unnecessary scripts after repo split ([#1372](https://github.com/opensearch-project/observability/pull/1372))
* Add bwc tests in distribution level ([#1366](https://github.com/opensearch-project/observability/pull/1366))


### OpenSearch Reporting
* Include integration tests in windows and macOS workflow ([#624](https://github.com/opensearch-project/reporting/pull/624))
* Remove unnecessary scripts after repo split ([#622](https://github.com/opensearch-project/reporting/pull/622))
* Remove front end code([#620](https://github.com/opensearch-project/reporting/pull/620))


### OpenSearch Security Analytics Dashboards
* Remove mac os from unit test platforms. ([#211](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/211))
* Public Components Snapshot Tests. ([#218](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/218))
* Sort alerts in descending order of timestamp by default. ([#222](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/222))
* Filtered findings shown in alert details. ([#229](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/229))
* Cypress checking on rule YAML content. ([#248](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/248))
* Creating new object for alert condition initialization. ([#255](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/255))
* Added windows to cypress test runs. ([#259](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/259))
* Streamline rules request. ([#281](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/281))
* Detector must have at least one alert set. ([#289](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/289))
* Updated field mapping UX; disabled windows run for cypress. ([#307](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/307))
* Improve alert condition input placeholders. ([#308](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/308))
* Status chart colors update. ([#309](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/309))


### OpenSearch SQL
* Change ApplicationContext lifecycle to per node level ([#822](https://github.com/opensearch-project/sql/issues/822))
* Catalog to Datasource changes ([#1027](https://github.com/opensearch-project/sql/issues/1027) [#1049](https://github.com/opensearch-project/sql/issues/1049) [#1086](https://github.com/opensearch-project/sql/issues/1086))
* Bump jackson to 2.14.0 ([#1058](https://github.com/opensearch-project/sql/issues/1058))
* Add metadatalog interface and default in memory implementation ([#974](https://github.com/opensearch-project/sql/issues/974))
* Decouple function repository and DSL from IoC container for use anywhere ([#1085](https://github.com/opensearch-project/sql/issues/1085))
* Move DataSourceServiceImpl to core module ([#1084](https://github.com/opensearch-project/sql/issues/1084))
* Improve pushdown optimization and logical to physical transformation ([#1091](https://github.com/opensearch-project/sql/issues/1091))
* Using jackson and jackson_databind version defined in OpenSearch ([#1169](https://github.com/opensearch-project/sql/issues/1169) [#1173](https://github.com/opensearch-project/sql/issues/1173))
* Add BWC tests for running against distribution bundle.  ([#1209](https://github.com/opensearch-project/sql/issues/1209))

## DOCUMENTATION

### OpenSearch Alerting
* Added 2.5 release notes. ([#743](https://github.com/opensearch-project/alerting/pull/743))


### OpenSearch Alerting Dashboards Plugin
* Add 2.5.0 release notes. ([#440](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/440))


### OpenSearch Anomaly Detection
* Fix: typo in ohltyler. ([#760](https://github.com/opensearch-project/anomaly-detection/pull/760))
* Updated MAINTAINERS.md format. ([#771](https://github.com/opensearch-project/anomaly-detection/pull/771))


### OpenSearch Anomaly Detection Dashboards
* Updated MAINTAINERS.md format. ([#388](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/388))


### OpenSearch Dashboards Notifications
* Add 2.5.0 release notes. ([#6](https://github.com/opensearch-project/dashboards-notifications/pull/6))


### OpenSearch Dashboards Visualizations
* Add release notes for 2.5.0.0 ([#155](https://github.com/opensearch-project/dashboards-visualizations/pull/155))


### OpenSearch Index Management
* 2.5 release note ([#658](https://github.com/opensearch-project/index-management/pull/658))


### OpenSearch Index Management Dashboards Plugin
* 2.5 release note ([#561](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/561))


### OpenSearch k-NN
* Update MAINTAINERS.md format ([#709](https://github.com/opensearch-project/k-NN/pull/709))


### OpenSearch ML Commons
* Updated MAINTAINERS.md format ([#668](https://github.com/opensearch-project/ml-commons/pull/668))
* Updating maintainers list ([#663](https://github.com/opensearch-project/ml-commons/pull/663))
* Add doc about how to setup GPU ML node ([#677](https://github.com/opensearch-project/ml-commons/pull/677))


### OpenSearch Neural Search
* Update MAINTAINERS.md format ([#95](https://github.com/opensearch-project/neural-search/pull/95))
* Use short-form MAINTAINERS.md ([#84](https://github.com/opensearch-project/neural-search/pull/84))


### OpenSearch Notifications
* Add 2.5.0 release notes. ([#600](https://github.com/opensearch-project/notifications/pull/600))


### OpenSearch Observability
* Adding release notes for 2.4.1 ([#1343](https://github.com/opensearch-project/observability/pull/1343))


### OpenSearch Observability Dashboards Plugin
* Update 2.x to be the same as observability repo ([#158](https://github.com/opensearch-project/dashboards-observability/pull/158))
* Release notes for 2.4.0 ([#1259](https://github.com/opensearch-project/observability/pull/1259))
* Adding release notes for 2.4.1 ([#1343](https://github.com/opensearch-project/observability/pull/1343))


### OpenSearch Security Analytics
* Added 2.5 release notes. ([#268](https://github.com/opensearch-project/security-analytics/pull/268))


### OpenSearch Security Analytics Dashboards
* Updated UI text and spacing in create detector workflow. ([#150](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/150))
* Add 2.5.0 release notes. ([#329](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/329))


### OpenSearch SQL
* Support opensearch-sql:run and update developer_guide doc ([#1099](https://github.com/opensearch-project/sql/issues/1099))
* Updated MAINTAINERS.md to match recommended opensearch-project format. ([#1224](https://github.com/opensearch-project/sql/issues/1224) [#1233](https://github.com/opensearch-project/sql/issues/1233))

## MAINTENANCE

### OpenSearch Alerting
* [AUTO] Increment version to 2.5.0-SNAPSHOT ([#629](https://github.com/opensearch-project/alerting/pull/629))


### OpenSearch Alerting Dashboards Plugin
* Bumped version to 2.5. ([#437](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/437))


### OpenSearch Anomaly Detection
* Increment version to 2.5.0-SNAPSHOT ([#711](https://github.com/opensearch-project/anomaly-detection/pull/711))


### OpenSearch Asynchronous Search
* Bump version to 2.5.0 ([#196](https://github.com/opensearch-project/asynchronous-search/pull/196))
* Updated Maintainers.MD format ([#218](https://github.com/opensearch-project/asynchronous-search/pull/218))


### OpenSearch Dashboards Notifications
* Bumped version to 2.5. ([#571](https://github.com/opensearch-project/notifications/pull/571))


### OpenSearch Dashboards Search Relevance
* Updated MAINTAINERS.md format ([#108](https://github.com/opensearch-project/dashboards-search-relevance/pull/108))
* Add Mingshi Liu as a maintainer ([#112](https://github.com/opensearch-project/dashboards-search-relevance/pull/112))
* Add config rule in release note for security category ([#128](https://github.com/opensearch-project/dashboards-search-relevance/pull/128))
* Increment from 2.x to 2.5.0 ([#29](https://github.com/opensearch-project/dashboards-search-relevance/pull/29))
* Add release note for 2.5.0 ([#135](https://github.com/opensearch-project/dashboards-search-relevance/pull/135))
* Bump version for ansi-regex, gs, glob-parent and update yarn.lock ([#107](https://github.com/opensearch-project/dashboards-search-relevance/pull/107))([#113](https://github.com/opensearch-project/dashboards-search-relevance/pull/113))


### OpenSearch Dashboards Reporting
* Increment version to 2.5.0-SNAPSHOT ([#528](https://github.com/opensearch-project/reporting/pull/528))
* Add necessary files ([#4](https://github.com/opensearch-project/dashboards-reporting/pull/4))


### OpenSearch Dashboards Visualizations
* Bump version to 2.5.0 ([#144](https://github.com/opensearch-project/dashboards-visualizations/pull/144))


### OpenSearch Geospatial
* Increment version to 2.5.0-SNAPSHOT ([#184](https://github.com/opensearch-project/geospatial/pull/184))


### OpenSearch Index Management
* Fix all the compile warnings and detekt issues ([#603](https://github.com/opensearch-project/index-management/pull/603))
* Unify test clean logic ([#609](https://github.com/opensearch-project/index-management/pull/609))
* Security Workflow ([#611](https://github.com/opensearch-project/index-management/pull/611))
* Bump 2.5.0 ([#638](https://github.com/opensearch-project/index-management/pull/638))
* Updated MAINTAINERS.md format ([#650](https://github.com/opensearch-project/index-management/pull/650))


### OpenSearch Index Management Dashboards Plugin
* Change help text in "RestoreSnapshotAdvancedSettings" , documentation url in "IndexSettingsInput" ([#365](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/365))
* Bump loader-utils to 1.4.1 to address vulnerability alert, specify OSD 2.4.0 ([#381](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/381))
* Data stream selection popover auto adjust width ([#412](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/412))
* Version bump 2.4.1 ([#430](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/430))
* Feat: fix mac platform error ([#518](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/518))
* Updated MAINTAINERS.md format. ([#539](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/539))
* Bump to 2.5.0 ([#540](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/540))


### OpenSearch k-NN
* Fix the codec94 version import statements ([#684](https://github.com/opensearch-project/k-NN/pull/684))
* Add integ test for index close/open scenario ([#693](https://github.com/opensearch-project/k-NN/pull/693))
* Make version of lucene k-nn engine match lucene current version ([#691](https://github.com/opensearch-project/k-NN/pull/691))
* Increment version to 2.5.0-SNAPSHOT ([#632](https://github.com/opensearch-project/k-NN/pull/632))


### OpenSearch ML Commons
* Increment version to 2.5.0-SNAPSHOT ([#513](https://github.com/opensearch-project/ml-commons/pull/513))


### OpenSearch Neural Search
* Increment version to 2.5.0-SNAPSHOT ([#76](https://github.com/opensearch-project/neural-search/pull/76))


### OpenSearch Notifications
* Bumped version to 2.5. ([#571](https://github.com/opensearch-project/notifications/pull/571))


### OpenSearch Observability
* Increment version to 2.5.0-SNAPSHOT ([#1205](https://github.com/opensearch-project/observability/pull/1205))


### OpenSearch Query Workbench
* Merge 2.x changes into dashboards-query-workbench ([#17](https://github.com/opensearch-project/dashboards-query-workbench/pull/17))
* Updated MAINTAINERS.md format. ([#18](https://github.com/opensearch-project/dashboards-query-workbench/pull/18))


### OpenSearch Observability Dashboards Plugin
- Increment version to 2.5.0-SNAPSHOT ([#1205](https://github.com/opensearch-project/observability/pull/1205))


### OpenSearch Performance Analyzer
* Upgrade netty to 4.1.86 ([#352](https://github.com/opensearch-project/performance-analyzer/pull/352))
* Update jackson to 2.14.1 ([#369](https://github.com/opensearch-project/performance-analyzer/pull/369))


### OpenSearch Reporting
* Increment version to 2.5.0-SNAPSHOT [#528](https://github.com/opensearch-project/reporting/pull/528))


### OpenSearch Security Analytics
* Bumped version to 2.5. ([#215](https://github.com/opensearch-project/security-analytics/pull/215))
* Updated MAINTAINERS.md format. ([#240](https://github.com/opensearch-project/security-analytics/pull/240))


### OpenSearch Security Analytics Dashboards
* Made minor changes to polish the UI. ([#247](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/247))
* Bumped version to 2.5. ([#297](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/297))
* Updated MAINTAINERS.md format. ([#284](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/284))
* Bump json5 from 1.0.1 to 1.0.2. ([#285](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/285))
* Remove experimental banner. ([#303](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/303))


### OpenSearch Security
* Upgrade CXF to 3.5.5 to address CVE-2022-46363 ([#2350](https://github.com/opensearch-project/security/pull/2350), [#2357](https://github.com/opensearch-project/security/pull/2357))


## REFACTORING

### OpenSearch Alerting
* Added exception check once the .opendistro-alerting-config index is being created. ([#650](https://github.com/opensearch-project/alerting/pull/650))
* Set lastnotification time as created time for new bucket level monitor. ([#675](https://github.com/opensearch-project/alerting/pull/675))
* Separate variables for alert and finding scheduled rollovers. ([#705](https://github.com/opensearch-project/alerting/pull/705))
* Overriding defaultTitle with subject for SNS notifications. ([#708](https://github.com/opensearch-project/alerting/pull/708))
* QueryIndex rollover when field mapping limit is reached. ([#725](https://github.com/opensearch-project/alerting/pull/725))
* Added unwrapping exceptions from core. ([#728](https://github.com/opensearch-project/alerting/pull/728))


### OpenSearch ML Commons
* Change task worker node to list; add target worker node to cache ([#656](https://github.com/opensearch-project/ml-commons/pull/656)) 


### OpenSearch Neural Search
* Remove unused MLPredict Transport action from src ([#94](https://github.com/opensearch-project/neural-search/pull/94))


### OpenSearch Observability Dashboards Plugin
* Remove front end workflow and code ([#1362](https://github.com/opensearch-project/observability/pull/1362))
* Hot fixes and cypress test changes ([#1327](https://github.com/opensearch-project/observability/pull/1327))


### OpenSearch Security Analytics
* Search returns detector type in CAPS fix and integration tests. ([#174](https://github.com/opensearch-project/security-analytics/pull/174))
* Added dummy search when creating detector on the given indices. ([#197](https://github.com/opensearch-project/security-analytics/pull/197))
* Updated network mappings. ([#211](https://github.com/opensearch-project/security-analytics/pull/211))
* Updated windows mappings. ([#212](https://github.com/opensearch-project/security-analytics/pull/212))
* Updated ad_ldap mappings. ([#213](https://github.com/opensearch-project/security-analytics/pull/213))
* Removed create/delete queryIndex. ([#215](https://github.com/opensearch-project/security-analytics/pull/215))
* Update Linux mappings. ([#223](https://github.com/opensearch-project/security-analytics/pull/223))
* Changes to return empty search response for custom rules. ([#231](https://github.com/opensearch-project/security-analytics/pull/231))
* Service Returns Unhandled Error Response. ([#248](https://github.com/opensearch-project/security-analytics/pull/248))


### OpenSearch SQL
* The SQL Plugin was rearranged into separate repositories ([#640](https://github.com/opensearch-project/sql/issues/640) [#1263](https://github.com/opensearch-project/sql/issues/1263))
* Added SQL-Jdbc repository https://github.com/opensearch-project/sql-jdbc ([#964](https://github.com/opensearch-project/sql/issues/964))
* Added SQL-Jdbc maven artifact as a dependency ([#2692](https://github.com/opensearch-project/opensearch-build/issues/2692))
* Added SQL-Odbc repository https://github.com/opensearch-project/sql-odbc ([#965](https://github.com/opensearch-project/sql/issues/965))
* Added SQL-Cli repository  https://github.com/opensearch-project/sql-cli ([#966](https://github.com/opensearch-project/sql/issues/966))
* Added Workbench repository https://github.com/opensearch-project/dashboards-query-workbench ([#1266](https://github.com/opensearch-project/sql/issues/1266))

