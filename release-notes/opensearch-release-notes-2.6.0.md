# OpenSearch and OpenSearch Dashboards 2.6.0 Release Notes

## Release Highlights
The OpenSearch 2.6.0 release adds tools and enhancements to help you build, manage, and scale OpenSearch for a range of use cases. This release includes a new data schema for analytics and observability workloads as well as new functionality for machine learning-powered search, along with new index management capabilities, enhanced threat detection for security analytics, expanded functionality for map visualizations, and more. See below for the latest additions to the project and visit our downloads page to get started with the new distributions. You can explore OpenSearch Dashboards on the [Playground](https://playground.opensearch.org/), with no need to download.

### New Features
* With the new Simple Schema for Observability, OpenSearch introduces a standardized approach to accessing data from different sources. The schema supports a structured definition for major analytics and observability signals, including logs, traces, and metrics, conforming to OpenTelemetry standards.
* You can now create, view, and manage data  streams directly from the index management user interface. Admins also gain the ability to perform manual rollover operations and force merges for indexes or data streams from the UI.
* You can now use multiple indexes or index patterns to create threat detectors, rather than just a single source. Many detectors now include out-of-the-box dashboards to help you identify broader patterns in your security logs.
* The search backpressure feature can now cancel queries at the coordinator  level, offering more efficient protection against traffic surges that result from a small number of resource-intensive queries.
* You can now add maps to dashboard panels within OpenSearch Dashboards without leaving the Dashboards environment.


### Experimental Features
OpenSearch 2.6.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, refer to the [documentation](https://opensearch.org/docs/latest/) for the feature.

* A new model health dashboard lets you view the location and status of machine learning models, simplifying management of semantic search and other ML workloads.
* This release adds support for AWS Signature Version 4 (AWS SigV4) as a request authentication method for the experimental multiple data sources feature, which allows you to add multiple data sources to a single dashboard.


## Release Details

[OpenSearch and OpenSearch Dashboards 2.6.0](https://opensearch.org/versions/opensearch-2-6-0.html) includes the following feature, enhancement, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.6.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.6.0.md).

## FEATURES

### OpenSearch Geospatial
* Add limit to geojson upload API ([#218](https://github.com/opensearch-project/geospatial/pull/218))
* Allow API to accept any index name without suffix ([#182](https://github.com/opensearch-project/geospatial/pull/182))


### OpenSearch Index Management Dashboards
* Add index operation of force merge  ([#608](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/608))
* Add data stream management page  ([#605](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/605))
* Add index operation of rollover  ([#607](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/607))


### OpenSearch Observability Dashboards
* Add new page/route for notebooks create and rename ([#250](https://github.com/opensearch-project/dashboards-observability/pull/250))([#293](https://github.com/opensearch-project/dashboards-observability/pull/293))


### OpenSearch Ml Commons
* Enable prebuilt model ([#729](https://github.com/opensearch-project/ml-commons/pull/729))


### OpenSearch Performance Analyzer
* Cluster config api return verbose PA status ([#342](https://github.com/opensearch-project/performance-analyzer/pull/342))


### OpenSearch Alerting
* Multiple indices support in DocLevelMonitorInput ([#784](https://github.com/opensearch-project/alerting/pull/784))


### OpenSearch Security Analytics
* GetIndexMappings index pattern support ([#265](https://github.com/opensearch-project/security-analytics/pull/265))
* Added API to fetch all log types/rule categories ([#327](https://github.com/opensearch-project/security-analytics/pull/327))


### OpenSearch Security Analytics Dashboards
* Added new log types ([#439](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/439))
* Added create dashboard feature ([#437](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/437))
* Improvements for field mappings ([#432](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/432))
* Added multi select data source for creating detector ([#424](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/424))
* Chart vertical domain UX improvement ([#372](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/372))
* Various detectors page UX/UI improvements ([#387](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/387))
* Various findings page UX/UI improvements ([#369](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/369))
* Upgrade vega tooltips to use custom formatting ([#368](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/368))
* Adds validation for trigger name in creating alert flyout ([#367](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/367))
* Create index pattern ([#366](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/366))
* Provide all unmapped fields when editing Rule field mapping ([#353](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/353))


### OpenSearch Dashboards Maps
* Add map as embeddable to dashboard ([#231](https://github.com/opensearch-project/dashboards-maps/pull/231))
* Add maps saved object for sample datasets ([#240](https://github.com/opensearch-project/dashboards-maps/pull/240))


## ENHANCEMENTS

### OpenSearch Security Analytics
* Adds timestamp field alias and sets time range filter in bucket level monitor ([#262](https://github.com/opensearch-project/security-analytics/pull/262))
* Update others_application mappings ([#277](https://github.com/opensearch-project/security-analytics/pull/277))
* Update others_apt mappings. ([#278](https://github.com/opensearch-project/security-analytics/pull/278))
* Index template conflict resolve; GetIndexMappings API changes ([#283](https://github.com/opensearch-project/security-analytics/pull/283))
* Add nesting level to yaml constructor ([#286](https://github.com/opensearch-project/security-analytics/pull/286))
* Update others_cloud mappings ([#301](https://github.com/opensearch-project/security-analytics/pull/301))
* Update others_compliance mappings ([#302](https://github.com/opensearch-project/security-analytics/pull/302))
* Update others_web mappings ([#304](https://github.com/opensearch-project/security-analytics/pull/304))
* Log message change for debugging ([#321](https://github.com/opensearch-project/security-analytics/pull/321))


### OpenSearch Security
* Add actions cluster:admin/component_template/* to cluster_manage_index_templates ([#2409](https://github.com/opensearch-project/security/pull/2409))
* Publish snapshots to maven ([#2438](https://github.com/opensearch-project/security/pull/2438))
* Integrate k-NN functionality with security plugin ([#2274](https://github.com/opensearch-project/security/pull/2274))


### OpenSearch Security Dashboards Plugin
* Windows CI Support ([#1320](https://github.com/opensearch-project/security-dashboards-plugin/pull/1320))
* Add indices:admin/close* to list of permissible index permissions ([#1323](https://github.com/opensearch-project/security-dashboards-plugin/pull/1323))
* Synchronize all permissions from latest OpenSearch ([#1333](https://github.com/opensearch-project/security-dashboards-plugin/pull/1333))


### OpenSearch SQL
* Extend comparison methods to accept different datetime types ([#1196](https://github.com/opensearch-project/sql/pull/1196))
* Enable concat() string function to support multiple string arguments ([#1279](https://github.com/opensearch-project/sql/pull/1279))
* Add more keywords as identifier in PPL ([#1319](https://github.com/opensearch-project/sql/pull/1319))
* Update DATE_ADD/ADDDATE and DATE_SUB/SUBDATE functions ([#1182](https://github.com/opensearch-project/sql/pull/1182))
* Escape character support for string literals ([#1206](https://github.com/opensearch-project/sql/pull/1206))
* Updated EXPM1() and Tests to New Engine ([#1334](https://github.com/opensearch-project/sql/pull/1334))
* Update TIMESTAMP function implementation and signatures ([#1254](https://github.com/opensearch-project/sql/pull/1254))
* Add GET_FORMAT Function To OpenSearch SQL Plugin ([#1299](https://github.com/opensearch-project/sql/pull/1299))
* Add TIME_FORMAT() Function To SQL Plugin ([#1301](https://github.com/opensearch-project/sql/pull/1301))
* Support More Formats For GET_FORMAT Function ([#1343](https://github.com/opensearch-project/sql/pull/1343))
* Add last_day Function To OpenSearch SQL Plugin ([#1344](https://github.com/opensearch-project/sql/pull/1344))
* Add WeekOfYear Function To OpenSearch ([#1345](https://github.com/opensearch-project/sql/pull/1345))


### OpenSearch Cross Cluster Replication
* Stopping replication before clean up of indices ([635](https://github.com/opensearch-project/cross-cluster-replication/pull/635))


### OpenSearch Dashboards Maps
* Fix popup display while zoomed out ([#226](https://github.com/opensearch-project/dashboards-maps/pull/226))
* Limit max number of layers ([#216](https://github.com/opensearch-project/dashboards-maps/pull/216))
* Add close button to tooltip hover ([#263](https://github.com/opensearch-project/dashboards-maps/pull/263))
* Add scroll bar when more layers added ([#254](https://github.com/opensearch-project/dashboards-maps/pull/254))
* Align items in add new layer modal ([#256](https://github.com/opensearch-project/dashboards-maps/pull/256))
* Add indexPatterns to map embeddable output for dashboard filters ([#272](https://github.com/opensearch-project/dashboards-maps/pull/272))


### OpenSearch Anomaly Detection Dashboards
* Update cold start message ([#398](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/398))
* Changed required minimum intervals in cold start message ([#411](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/411))
* Remove `auto_expand_replicas` override in sample data indices ([#423](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/423))


## BUG FIXES

### OpenSearch Observability Dashboards
* Correct ppl leran more link ([#189](https://github.com/opensearch-project/dashboards-observability/pull/189))
* Few fixes regarding issues for visualization rendering ([#187](https://github.com/opensearch-project/dashboards-observability/pull/187))
* Debug CVE fix ([#223](https://github.com/opensearch-project/dashboards-observability/pull/223)) ([#263](https://github.com/opensearch-project/dashboards-observability/pull/263))
* Fix bugs related to trace analytics jaeger mode ([#237](https://github.com/opensearch-project/dashboards-observability/pull/237))([#271](https://github.com/opensearch-project/dashboards-observability/pull/271))([#280](https://github.com/opensearch-project/dashboards-observability/pull/280))
* Update error handling in viz container ([#252](https://github.com/opensearch-project/dashboards-observability/pull/252))
* Panels filter check for where clause ([#253](https://github.com/opensearch-project/dashboards-observability/pull/253))
* Fix explorer dark mode issue and restructure scss  ([#262](https://github.com/opensearch-project/dashboards-observability/pull/262))
* Operational panels cypress fix ([#274](https://github.com/opensearch-project/dashboards-observability/pull/274))
* Event Analytics Bug Fixes ([#291](https://github.com/opensearch-project/dashboards-observability/pull/291))
* Remove timeseries data validation to get back line chart support ([#292](https://github.com/opensearch-project/dashboards-observability/pull/292))
* Add missing changes for visualization config pane ([#294](https://github.com/opensearch-project/dashboards-observability/pull/294))
* Move performance now from a debug dependency to a runtime dependency ([#309](https://github.com/opensearch-project/dashboards-observability/pull/309))


### Opensearch Dashboards Visualizations
* Force resolve glob-parent and debug libraries ([#158](https://github.com/opensearch-project/dashboards-visualizations/pull/158))


### OpenSearch Dashboards Reporting
* Update scrollX and scrollY config for html2canvas ([#34](https://github.com/opensearch-project/dashboards-reporting/pull/34))


### OpenSearch Anomaly Detection
* Fixing dls/fls logic around numeric aggregations ([#800](https://github.com/opensearch-project/anomaly-detection/pull/800))
* Revert changes to exception message ([#803](https://github.com/opensearch-project/anomaly-detection/pull/803))


### OpenSearch Index Management Dashboards
* Remove inaccurate pre-check in shrink index page ([#570](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/570))
* Fix CVE-2022-46175. ([#586](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/586))


### OpenSearch k-NN
* Remove latestSettings cache from KNNSettings ([#727](https://github.com/opensearch-project/k-NN/pull/727))


### OpenSearch Notifications
* Update dependency com.google.code.gson:gson to v2.8.9 ([#626](https://github.com/opensearch-project/notifications/pull/626))


### OpenSearch Performance Analyzer
* Fix ShardEvents and ShardBulkDocs null metrics ([#283](https://github.com/opensearch-project/performance-analyzer-rca/pull/283))
* Fix and include unauthenticated user web server test ([#273](https://github.com/opensearch-project/performance-analyzer-rca/pull/273))


### OpenSearch Alerting
* Added document _id as param for terms query when searching alerts by their ids ([#753](https://github.com/opensearch-project/alerting/pull/753))
* Fix for ERROR alert state generation in doc-level monitors ([#768](https://github.com/opensearch-project/alerting/pull/768))
* ExecuteMonitor inserting metadata doc during dry run ([#758](https://github.com/opensearch-project/alerting/pull/758))
* Adjusting max field index setting dynamically for query index ([#776](https://github.com/opensearch-project/alerting/pull/776))
* Fix setting default title only when no subject has been set ([#750](https://github.com/opensearch-project/alerting/pull/750))


### OpenSearch Security Analytics
* Service Returns Unhandled Error Response ([#248](https://github.com/opensearch-project/security-analytics/pull/248))
* Correct linux mapping error ([#263](https://github.com/opensearch-project/security-analytics/pull/263))
* GetIndexMapping API timestamp alias bugfix ([#293](https://github.com/opensearch-project/security-analytics/pull/293))
* Query_field_names bugfix ([#335](https://github.com/opensearch-project/security-analytics/pull/335))


### OpenSearch Cross Cluster Replication
* Updating multi-field mapping at follower ([686](https://github.com/opensearch-project/cross-cluster-replication/pull/686))


### OpenSearch Security Analytics Dashboards
* Fixes bad breadcrumbs on page reload ([#395](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/395))
* Fixes UX/UI bugs for edit detector page ([#404](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/404))
* Add breadcrumbs for create detector page ([#394](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/394))
* Removes sidebar from edit detector page ([#388](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/388))
* Fixes interval field validation ([#379](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/379))
* Fixes chart tooltip delay ([#348](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/348))
* Fixes wrong alert colors ([#350](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/350))


### OpenSearch Security Dashboards Plugin
* Fix issue with jwt as url param after getAdditionalAuthHeader switched to async ([#1292](https://github.com/opensearch-project/security-dashboards-plugin/pull/1292))
* Update URLs referencing old docs-beta site ([#1231](https://github.com/opensearch-project/security-dashboards-plugin/pull/1231))
* Fix plugin configuration path ([#1304](https://github.com/opensearch-project/security-dashboards-plugin/pull/1304))


### OpenSearch SQL
* Allow literal in aggregation ([#1288](https://github.com/opensearch-project/sql/pull/1288))
* Datetime aggregation fixes ([#1061](https://github.com/opensearch-project/sql/pull/1061))
* Modified returning NaN to NULL ([#1341](https://github.com/opensearch-project/sql/pull/1341))
* Fix index not found reported as server error bug ([#1353](https://github.com/opensearch-project/sql/pull/1353))


### OpenSearch Dashboards Maps
* Fix custom layer render opacity config ([#289](https://github.com/opensearch-project/dashboards-maps/pull/289))


### OpenSearch Dashboards Notifications
* Fix CVE 2022-46175. ([#11](https://github.com/opensearch-project/dashboards-notifications/pull/11))
* Fix Node.js and Yarn installation in CI. ([#16](https://github.com/opensearch-project/dashboards-notifications/pull/16))


### OpenSearch Anomaly Detection Dashboards
* Upgrade filter bug ([#402](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/402))


## INFRASTRUCTURE

### OpenSearch Job Scheduler
* Added maven-publish.yml to decouple publishing of snapshots to Maven via Github Actions ([#320](https://github.com/opensearch-project/job-scheduler/pull/320))


### OpenSearch Anomaly Detection
* Dynamically set bwc current version from properties version ([#778](https://github.com/opensearch-project/anomaly-detection/pull/778))


### Opensearch Dashboards Visualizations
* Fix Node.js and Yarn installation in CI ([#166](https://github.com/opensearch-project/dashboards-visualizations/pull/166))


### OpenSearch Dashboards Reporting
* Fix Node.js and Yarn installation in CI ([#64](https://github.com/opensearch-project/dashboards-reporting/pull/64) [#68](https://github.com/opensearch-project/dashboards-reporting/pull/68))


### OpenSearch k-NN
* Add p99.9, p100 and num_of_segments metrics to perf-tool ([#739](https://github.com/opensearch-project/k-NN/pull/739))
* Update bwc to 2.6.0-SNAPSHOT ([#723](https://github.com/opensearch-project/k-NN/pull/723))
* Add Windows Support to BWC Tests ([#726](https://github.com/opensearch-project/k-NN/pull/726))
* Add test for KNNWeight ([#759](https://github.com/opensearch-project/k-NN/pull/759))
* Set NoMergePolicy for codec tests ([#754](https://github.com/opensearch-project/k-NN/pull/754))


### OpenSearch Alerting
* Fixed security tests. ([#484](https://github.com/opensearch-project/alerting/pull/484))
* Minor fix to prevent flaky tests in downstream plugins ([#804](https://github.com/opensearch-project/alerting/pull/804))
* Publish snapshots to maven via GHA ([#805](https://github.com/opensearch-project/alerting/pull/805))


### OpenSearch Notifications
* Publish snapshots to maven via GHA ([#627](https://github.com/opensearch-project/notifications/pull/627))


### OpenSearch Observability
* Add publish snapshots to maven via GHA ([#1423](https://github.com/opensearch-project/observability/pull/1423))
* Add support for structured Metrics & Traces index using Simple Schema for Observability ([#1427](https://github.com/opensearch-project/observability/pull/1427))


### Opensearch Reporting
* Remove unnecessary scripts after repo split  [#622](https://github.com/opensearch-project/reporting/pull/622))


### OpenSearch Security Analytics Dashboards
* Fix Node.js and Yarn installation in CI ([#446](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/446))
* Added untriaged issue workflow ([#410](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/410))


### OpenSearch SQL
* Upgrade sqlite to 3.32.3.3 ([#1283](https://github.com/opensearch-project/sql/pull/1283))
* Add publish snapshots to maven via GHA ([#1359](https://github.com/opensearch-project/sql/pull/1359))
* Added untriaged issue workflow ([#1338](https://github.com/opensearch-project/sql/pull/1338))
* Create custom integ test file for sql plugin ([#1330](https://github.com/opensearch-project/sql/pull/1330))
* Fix IT according to OpenSearch changes ([#1326](https://github.com/opensearch-project/sql/pull/1326))
* Fix ArgumentCaptor can't capture varargs ([#1320](https://github.com/opensearch-project/sql/pull/1320))
* Added Correctness Tests For Date And Time Functions ([#1298](https://github.com/opensearch-project/sql/pull/1298))
* Update usage of Strings.toString ([#1309](https://github.com/opensearch-project/sql/pull/1309))
* Update link checker CI workflow. ([#1304](https://github.com/opensearch-project/sql/pull/1304))
* Add micro benchmark by JMH ([#1278](https://github.com/opensearch-project/sql/pull/1278))
* Move PiTest to a new workflow. ([#1285](https://github.com/opensearch-project/sql/pull/1285))
* Adding mutation testing to build gradle with PiTest ([#1204](https://github.com/opensearch-project/sql/pull/1204))

### OpenSearch Dashboards Maps
* [Cypress fix] Wait map saved before open maps listing ([#218](https://github.com/opensearch-project/dashboards-maps/pull/218))


### OpenSearch Query Workbench
* Fix Node.js and Yarn installation in CI ([#46](https://github.com/opensearch-project/dashboards-query-workbench/pull/46))


### OpenSearch Anomaly Detection Dashboards
* Bump @sideway/formula to 3.0.1 ([#418](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/418))


## DOCUMENTATION

### OpenSearch Index Management
* 2.6 release note ([#693](https://github.com/opensearch-project/index-management/pull/693))


### OpenSearch Index Management Dashboards
* 2.6 release note ([#632](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/632))


### OpenSearch Ml Commons
* Update gpu doc with docker test ([#702](https://github.com/opensearch-project/ml-commons/pull/702))
* Add text embedding API example doc ([#710](https://github.com/opensearch-project/ml-commons/pull/710))
* Fix profile API in example doc ([#712](https://github.com/opensearch-project/ml-commons/pull/712))
* Change model url to public repo in text embedding model example doc ([#713](https://github.com/opensearch-project/ml-commons/pull/713))
* JSON listing of all the pretrianed models ([#730](https://github.com/opensearch-project/ml-commons/pull/730))


### OpenSearch Notifications
* Add 2.6.0 release notes ([#629](https://github.com/opensearch-project/notifications/pull/629))


### OpenSearch Security Analytics
* Added 2.6 release notes ([#353](https://github.com/opensearch-project/security-analytics/pull/353))


### OpenSearch Security Analytics Dashboards
* Readme update ([#363](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/363))
 

### OpenSearch Alerting
* Added 2.6 release notes. ([#809](https://github.com/opensearch-project/alerting/pull/809))


### OpenSearch SQL
* Reorganize development docs ([#1200](https://github.com/opensearch-project/sql/pull/1200))
* Remove obsolete links from README ([#1303](https://github.com/opensearch-project/sql/pull/1303))

### OpenSearch Dashboards Notifications
* Drafted 2.6 release notes. ([#21](https://github.com/opensearch-project/dashboards-notifications/pull/21))


### OpenSearch Alerting Dashboards
* Add 2.6.0 release notes. ([#493](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/493))


## MAINTENANCE

### OpenSearch Observability Dashboards
* Cypress test update and related linting fixes ([#220](https://github.com/opensearch-project/dashboards-observability/pull/220))
* upgrade cypress to 6 ([#249](https://github.com/opensearch-project/dashboards-observability/pull/249))
* Fix Node.js and Yarn installation in CI ([#299](https://github.com/opensearch-project/dashboards-observability/pull/299))


### Opensearch Dashboards Visualizations
* Bump version to 2.6.0 ([#160](https://github.com/opensearch-project/dashboards-visualizations/pull/160)) 


### OpenSearch Geospatial
* Upgrade snapshot version to 2.6 for 2.x ([#208](https://github.com/opensearch-project/geospatial/pull/208))


### OpenSearch Index Management
* [AUTO] Increment version to 2.6.0-SNAPSHOT ([#653](https://github.com/opensearch-project/index-management/pull/653))


### OpenSearch Index Management Dashboards
* Fix plugin version format. ([#567](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/567))
* Bumped version to 2.6. ([#630](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/630))


### OpenSearch k-NN
* Replace KnnQueryVector by KnnFloatVectorQuery for Lucene knn ([#767](https://github.com/opensearch-project/k-NN/pull/767))


### OpenSearch Ml Commons
* Increment version to 2.6.0-SNAPSHOT ([#671](https://github.com/opensearch-project/ml-commons/pull/671))


### OpenSearch Neural Search
* Increment version to 2.6.0-SNAPSHOT ([#117](https://github.com/opensearch-project/neural-search/pull/117))


### OpenSearch Notifications
* [AUTO] Increment version to 2.6.0-SNAPSHOT ([#596](https://github.com/opensearch-project/notifications/pull/596))


### OpenSearch Observability
* Revert "Removing explicit jackson dependencies ([#1381](https://github.com/opensearch-project/observability/pull/1381))
* Bump version to 2.6 ([#1391](https://github.com/opensearch-project/observability/pull/1391))


### OpenSearch Performance Analyzer
* Upgrade guava,protobuf minor versions ([#375](https://github.com/opensearch-project/performance-analyzer/pull/375))
* Update jackson ([#370](https://github.com/opensearch-project/performance-analyzer/pull/370))
* Pin bcel version to 6.6.1 ([#270](https://github.com/opensearch-project/performance-analyzer-rca/pull/270))


### OpenSearch Security Analytics
* Baselined MAINTAINERS and CODEOWNERS docs. ([#329](https://github.com/opensearch-project/security-analytics/pull/329))
* Bumped version to 2.6. ([#351](https://github.com/opensearch-project/security-analytics/pull/351))


### OpenSearch Security Analytics Dashboards
* Updated lint-staged for consistency with other plugins. ([#412](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/412))


### OpenSearch Security
* Updates toString calls affected by change in method signature ([#2418](https://github.com/opensearch-project/security/pull/2418))
* Updates DlsFlsFilterLeafReader with Lucene change and fix broken deprecation logger test ([#2429](https://github.com/opensearch-project/security/pull/2429))
* Add CODEOWNERS ([#2445](https://github.com/opensearch-project/security/pull/2445))


### OpenSearch Security Dashboards Plugin
* Switch to maven to download plugin ([#1331](https://github.com/opensearch-project/security-dashboards-plugin/pull/1331))


### OpenSearch Asynchronous Search
* Fix checkstyle version ([#237](https://github.com/opensearch-project/asynchronous-search/pull/237))


### OpenSearch Dashboards Notifications
* Bumped version to 2.6. ([#19](https://github.com/opensearch-project/dashboards-notifications/pull/19))


### OpenSearch Query Workbench
* Rename plugin_helpers to plugin-helpers ([#32](https://github.com/opensearch-project/dashboards-query-workbench/pull/32))
* Bump version to 2.6.0 ([#37](https://github.com/opensearch-project/dashboards-query-workbench/pull/37))
* Upgrade hapi-latest to fix CVE-2023-25166 ([#40](https://github.com/opensearch-project/dashboards-query-workbench/pull/40))


### OpenSearch Dashboards Search Relevance
* Updating CODEOWNERS as per issue #146 by @macohen in https://github.com/opensearch-project/dashboards-search-relevance/pull/148
* Add workflow for adding untriaged labels by @sejli in https://github.com/opensearch-project/dashboards-search-relevance/pull/141


### OpenSearch Alerting Dashboards
* Updated MAINTAINERS.md format. ([#435](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/435))
* Bumped version to 2.6. ([#492](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/492))


## REFACTORING

### OpenSearch Geospatial
* Fix compilation error and test failure ([#210](https://github.com/opensearch-project/geospatial/pull/210))
* Replace Locale.getDefault() with Local.ROOT ([#214](https://github.com/opensearch-project/geospatial/pull/214))


### OpenSearch Index Management
* Reduce code difference ([#670](https://github.com/opensearch-project/index-management/pull/670))


### OpenSearch Index Management Dashboards
* Minor UI changes. ([#559](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/559))
* Reduce code conflicts. ([#589](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/589))


### OpenSearch k-NN
* Refactor structure of stats module ([#736](https://github.com/opensearch-project/k-NN/pull/736))


### OpenSearch Ml Commons
* Add DL model class ([#722](https://github.com/opensearch-project/ml-commons/pull/722))


### OpenSearch Dashboards Maps
* Refactor add layer operations ([#222](https://github.com/opensearch-project/dashboards-maps/pull/222))
* Refactor layer operations ([#224](https://github.com/opensearch-project/dashboards-maps/pull/224))
* Refactor layer properties as own interface ([#225](https://github.com/opensearch-project/dashboards-maps/pull/225))
