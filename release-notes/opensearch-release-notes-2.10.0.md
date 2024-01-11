OpenSearch and OpenSearch Dashboards 2.10.0 Release Notes

## Release Highlights

OpenSearch 2.10.0 includes a number of new features for search, security, and machine learning applications, as well as user interface improvements and new options for durable data storage. This release also includes new experimental tools to boost search performance and build conversational search applications.

### New Features

* Remote-backed storage is now generally available, offering a production-ready alternative to snapshots or replica copies for durable data backup.
* Segment replication is now fully integrated with remote-backed storage. This allows users to select remote-backed storage as the source for replication, with the potential to reduce compute resources on ingest.
* New hybrid query functionality and a built-in normalization processor offer a way to improve relevance for search results. Now, you can combine and normalize the relevance scores of lexical queries with natural language-based k-NN vector search queries within OpenSearch.
* You can now define custom log types with Security Analytics and use them as you would other log data to build detectors, create custom rules, provide additional mappings, and more.
* A new visual theme for OpenSearch Dashboards includes changes to typography, colors, and actions for light mode and dark mode designs, providing an updated user experience.
* Updates to the Discover tool in OpenSearch Dashboards include usability improvements designed to make the tool more intuitive and cohesive.
* A new IP2Geo processor accesses location data based on IP addresses using external databases, allowing OpenSearch to enrich data with up-to-date geographical location information.
* With  this release, OpenSearch Dashboards is upgraded to version 18 of Node.js, with backward-compatible support for Node.js versions 14 and 16. Users have the flexibility to choose from these versions to run the web application. As a result of this update, the Docker images for OpenSearch and OpenSearch Dashboards now use Amazon Linux 2023 as the base image, changed from Amazon Linux 2.

### Experimental Features

OpenSearch 2.10.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.

* Build conversational search applications with new tools as part of ML Commons, including new APIs that enable conversational search and conversational memory as well as integrations with search pipelines that allow the use of conversational memory and large language models (LLMs) to answer questions.
* Concurrent segment search gives you the option to query index segments in parallel at the shard level. This can deliver improved latency for many types of search queries.

## Release Details
[OpenSearch and OpenSearch Dashboards 2.10.0](https://opensearch.org/versions/opensearch-2-10-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.10/release-notes/opensearch.release-notes-2.10.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.10/release-notes/opensearch-dashboards.release-notes-2.10.0.md).

## FEATURES

### OpenSearch Alerting
* Add workflowIds field in getAlerts API  ([#1014](https://github.com/opensearch-project/alerting/pull/1014))
* Add alertId parameter in get chained alert API and paginate associated alerts if alertId param is mentioned ([#1071](https://github.com/opensearch-project/alerting/pull/1071))
* Chained Alert Behaviour Changes ([#1079](https://github.com/opensearch-project/alerting/pull/1079))


### OpenSearch Alerting Dashboards
* Updates for dark mode theme ([#695](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/695))
* Add default Notification subject  ([#701](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/701))


### OpenSearch Common Utils
* Common utils to support Microsoft teams in notifications ([#428](https://github.com/opensearch-project/common-utils/pull/428))
* Support list of monitor ids in Chained Monitor Findings ([#514](https://github.com/opensearch-project/common-utils/pull/514))


### OpenSearch Custom Codecs
* Moving ZSTD codec support from OpenSearch core to standalone plugin `custom-codecs`


### OpenSearch Dashboards Maps
* Allow filtering geo_shape fields around map extent ([#452](https://github.com/opensearch-project/dashboards-maps/pull/452))
* Support dark mode in maps-dashboards([#455](https://github.com/opensearch-project/dashboards-maps/pull/455))


### OpenSearch Dashboards Notifications
* Add microsoft teams support ([#44](https://github.com/opensearch-project/dashboards-notifications/pull/44))


### OpenSearch Dashboards Observability
* Integrations Improve label handling ([#936](https://github.com/opensearch-project/dashboards-observability/pull/936))


### OpenSearch Geospatial
* IP2Geo processor implementation ([#362](https://github.com/opensearch-project/geospatial/pull/362))


### OpenSearch Index Management
* Support copy alias in rollover. ([#892](https://github.com/opensearch-project/index-management/pull/892))
* Make control center index as system index. ([#919](https://github.com/opensearch-project/index-management/pull/919))


### OpenSearch k-NN
* ~~Add Clear Cache API ([#740](https://github.com/opensearch-project/k-NN/pull/740))~~ Feature was mistakenly added to the release notes, although it was not included in the release.


### OpenSearch ML Commons
* Conversations and Generative AI in OpenSearch ([#1150](https://github.com/opensearch-project/ml-commons/issues/1150))


### OpenSearch ML Commons Dashboards
* Add source field to distinguish local and external model. ([#239](https://github.com/opensearch-project/ml-commons-dashboards/pull/239))
* Support external models in deployed model list. ([#248](https://github.com/opensearch-project/ml-commons-dashboards/pull/248))
* Support external models in model preview panel. ([#252](https://github.com/opensearch-project/ml-commons-dashboards/pull/252))


### OpenSearch Neural Search
* Improved Hybrid Search relevancy by Score Normalization and Combination ([#241](https://github.com/opensearch-project/neural-search/pull/241/))


### OpenSearch Notifications
* Support SNS FIFO queues([#716](https://github.com/opensearch-project/notifications/pull/716))
* Supuport Microsoft teams([#676](https://github.com/opensearch-project/notifications/pull/676),[#746](https://github.com/opensearch-project/notifications/pull/746))
* Support auto upgrade mapping logic([#699](https://github.com/opensearch-project/notifications/pull/699))


### OpenSearch Security Analytics
* Custom log type implementation ([#500](https://github.com/opensearch-project/security-analytics/pull/500))
* Add mitre attack based auto-correlations support in correlation engine ([#532](https://github.com/opensearch-project/security-analytics/pull/532))
* Using alerting workflows in detectors ([#541](https://github.com/opensearch-project/security-analytics/pull/541))


### OpenSearch Security Analytics-Dashboards
* Added new log type for vpc flow. ([#653](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/653))
* [Custom log types] Show log types table, Log type creation workflow ([#674](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/674))
* [Custom log types] CRUD operations for log types. ([#675](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/675))
* [Custom log types] Support custom log types in detection rule creation and detector creation. ([#676](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/676))
* Make tags hyperlinks to mitre attack web pages in detection rules. ([#692](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/692))
* Added CIDR modifier for detection fields. ([#693](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/693))


### OpenSearch Job Scheduler
* Setting JobSweeper search preference against primary shard ([#483](https://github.com/opensearch-project/job-scheduler/pull/483)) ([#485](https://github.com/opensearch-project/job-scheduler/pull/485))
* Converts .opendistro-job-scheduler-lock index into a system index ([#478](https://github.com/opensearch-project/job-scheduler/pull/478))
* Public snapshots on all release branches ([#475](https://github.com/opensearch-project/job-scheduler/pull/475)) ([#476](https://github.com/opensearch-project/job-scheduler/pull/476))


## ENHANCEMENTS

### OpenSearch Anomaly Detection
* Defaults anomaly grade to 0 if negative. ([#977](https://github.com/opensearch-project/anomaly-detection/pull/977))
* Update RCF to v3.8 and Enable Auto AD with 'Alert Once' Option ([#979](https://github.com/opensearch-project/anomaly-detection/pull/979))
* Revert "Enforce DOCUMENT Replication for AD Indices" ([#1006](https://github.com/opensearch-project/anomaly-detection/pull/1006))


### OpenSearch Anomaly Detection-Dashboards
* Optimize fetching of augment-vis saved objects ([#562](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/562))
* Fix display of detector names ([#585](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/585))


### OpenSearch Dashboards Search Relevance
* Changing select index error message to be more informative ([#270](https://github.com/opensearch-project/dashboards-search-relevance/pull/270)) ([#275](https://github.com/opensearch-project/dashboards-search-relevance/pull/275))


### OpenSearch k-NN
* Enabled the IVF algorithm to work with Filters of K-NN Query. ([#1013](https://github.com/opensearch-project/k-NN/pull/1013))
* Improved the logic to switch to exact search for restrictive filters search for better recall. ([#1059](https://github.com/opensearch-project/k-NN/pull/1059))
* Added max distance computation logic to enhance the switch to exact search in filtered Nearest Neighbor Search. ([#1066](https://github.com/opensearch-project/k-NN/pull/1066))


### OpenSearch ML Commons
* Add feature flags for remote inference ([#1223](https://github.com/opensearch-project/ml-commons/pull/1223))
* Add eligible node role settings ([#1197](https://github.com/opensearch-project/ml-commons/pull/1197))
* Add more stats: connector count, connector/config index status ([#1180](https://github.com/opensearch-project/ml-commons/pull/1180))


### OpenSearch ML Commons Dashboards
* Mitigate styles to oui variables. ([#227](https://github.com/opensearch-project/ml-commons-dashboards/pull/227)) 


### OpenSearch Neural Search
* Changed format for hybrid query results to a single list of scores with delimiter ([#259](https://github.com/opensearch-project/neural-search/pull/259))
* Added validations for score combination weights in Hybrid Search ([#265](https://github.com/opensearch-project/neural-search/pull/265))
* Made hybrid search active by default ([#274](https://github.com/opensearch-project/neural-search/pull/274))


### OpenSearch Performance Analyzer
* Add Search Back Pressure Autotune Pipeline [#517](https://github.com/opensearch-project/performance-analyzer/pull/517)
* SearchBackPressure Service Node/Cluster RCA [#437](https://github.com/opensearch-project/performance-analyzer-rca/pull/437)
* SearchBackPressure Policy/Decider Generic Framework Added [#461](https://github.com/opensearch-project/performance-analyzer-rca/pull/461)
* Handle Reader thread termination gracefully [#476](https://github.com/opensearch-project/performance-analyzer-rca/pull/476)


### OpenSearch Security
* Add .plugins-ml-config to the demo configuration system indices ([#2993](https://github.com/opensearch-project/security/pull/2993))
* Add workflow cluster permissions to alerting roles ([#2994](https://github.com/opensearch-project/security/pull/2994))
* Include password regex for Dashboardsinfo to display to users ([#2999](https://github.com/opensearch-project/security/pull/2999))
* Add geospatial ip2geo to the demo configuration system indices and roles ([#3051](https://github.com/opensearch-project/security/pull/3051))
* Make invalid password message clearer ([#3057](https://github.com/opensearch-project/security/pull/3057))
* Service Accounts password is randomly generated ([#3077](https://github.com/opensearch-project/security/pull/3077))
* Exclude sensitive info from the jackson serialization stacktraces ([#3195](https://github.com/opensearch-project/security/pull/3195))
* Prevent raw request body as output in serialization error messages ([#3205](https://github.com/opensearch-project/security/pull/3205))
* Command cat/indices will filter results per the Do Not Fail On Forbidden setting ([#3236](https://github.com/opensearch-project/security/pull/3236))
* Generate new demo certs with IPv6 loopback added to SAN in node certificate ([#3268](https://github.com/opensearch-project/security/pull/3268))
* System index permissions ([#2887](https://github.com/opensearch-project/security/pull/2887))


### OpenSearch Security-Dashboards
* Security Getting Started page follows Dashboard themes ([#1538](https://github.com/opensearch-project/security-dashboards-plugin/pull/1538))
* Security Roles and Audit Log Settings follow Dashboard themes ([#1558](https://github.com/opensearch-project/security-dashboards-plugin/pull/1558))
* Support OpenSearch logo theming for light / dark modes ([#1568](https://github.com/opensearch-project/security-dashboards-plugin/pull/1568))


### SQL
* Added support of timestamp/date/time using curly brackets by @matthewryanwells in https://github.com/opensearch-project/sql/pull/1908


## BUG FIXES

### OpenSearch Alerting
* Fix get alerts alertState query filter ([#1064](https://github.com/opensearch-project/alerting/pull/1064))


### Cross-Cluster-Replication
* Settings are synced before syncing mapping ([#994](https://github.com/opensearch-project/cross-cluster-replication/pull/994))
* Handled OpenSearchRejectExecuteException, introduced new setting ```plugins.replication.follower.concurrent_writers_per_shard```. ([#1004](https://github.com/opensearch-project/cross-cluster-replication/pull/1004))
* Fixed tests relying on wait_for_active_shards, fixed test for single Node and consume numNodes ([#1091](https://github.com/opensearch-project/cross-cluster-replication/pull/1091))
* Excessive logging avoided during certain exception types such as OpensearchTimeoutException ([#1114](https://github.com/opensearch-project/cross-cluster-replication/pull/1114))


### OpenSearch Dashboards Observability
* Trace Analytics Fix trace-groups query and update UI ([#514](https://github.com/opensearch-project/dashboards-observability/pull/514))


### OpenSearch Dashboards Query Workbench
* Bump word-wrap from 1.2.3 to 1.2.4 ([#99](https://github.com/opensearch-project/dashboards-query-workbench/pull/99))


### OpenSearch Dashboards Reporting
* Upgrade tough-cookie and semver ([#135](https://github.com/opensearch-project/dashboards-reporting/pull/135))
* Update breadcrumb title of isDashboardNavMenu ([#146](https://github.com/opensearch-project/dashboards-reporting/pull/146))
* Bump word-wrap for cve fix ([#157](https://github.com/opensearch-project/dashboards-reporting/pull/157))
* Add @cypress/request resolution to fix CVE-2023-28155 ([#175](https://github.com/opensearch-project/dashboards-reporting/pull/175))
* Make the generated report use the correct background color ([#170](https://github.com/opensearch-project/dashboards-reporting/pull/170))


### OpenSearch Geospatial
* Revert datasource state when delete fails([#382](https://github.com/opensearch-project/geospatial/pull/382))
* Update ip2geo test data url([#389](https://github.com/opensearch-project/geospatial/pull/389))


### OpenSearch Index Management
* Fix debug log for missing ISM config index. ([#846](https://github.com/opensearch-project/index-management/pull/846))
* Handle NPE in isRollupIndex. ([#855](https://github.com/opensearch-project/index-management/pull/855))
* Fix for max & min aggregations when no metric property exist. ([#870](https://github.com/opensearch-project/index-management/pull/870))
* Fix intelliJ IDEA gradle sync error ([#916](https://github.com/opensearch-project/index-management/pull/916))


### OpenSearch Index Management-Dashboards
* Fix exports is undefined. ([#826](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/826))


### OpenSearch k-NN
* Update Faiss parameter construction to allow HNSW+PQ to work ([#1074](https://github.com/opensearch-project/k-NN/pull/1074))


### OpenSearch ML Commons
* Fixing metrics ([#1194](https://github.com/opensearch-project/ml-commons/pull/1194))
* Fix null pointer exception when input parameter is null. ([#1192](https://github.com/opensearch-project/ml-commons/pull/1192))
* Fix admin with no backend role on AOS unable to create restricted model group ([#1188](https://github.com/opensearch-project/ml-commons/pull/1188))
* Fix parameter parsing bug for create connector input ([#1185](https://github.com/opensearch-project/ml-commons/pull/1185))
* Handle escaping string parameters explicitly ([#1174](https://github.com/opensearch-project/ml-commons/pull/1174))
* Fix model count bug ([#1180](https://github.com/opensearch-project/ml-commons/pull/1180))
* Fix core package name to address compilation errors ([#1157](https://github.com/opensearch-project/ml-commons/pull/1157))


### OpenSearch ML Commons Dashboards
* Fix no model show up when search a model. ([#238](https://github.com/opensearch-project/ml-commons-dashboards/pull/238))
* Migrate style to oui attributes and add fallback dash. ([#254](https://github.com/opensearch-project/ml-commons-dashboards/pull/254))
* Replace dash with em dash. ([#255](https://github.com/opensearch-project/ml-commons-dashboards/pull/255))

### OpenSearch Reporting
* Update import from upstream breaking changes ([#739](https://github.com/opensearch-project/reporting/pull/739))
* Fix from upstream import changes ([#748](https://github.com/opensearch-project/reporting/pull/748))


### OpenSearch Security Analytics
* Fix for mappings of custom log types & other bug fixes ([#505](https://github.com/opensearch-project/security-analytics/pull/505))
* Fixes detectorType incompatibility with detector rules ([#524](https://github.com/opensearch-project/security-analytics/pull/524))


### OpenSearch Security
* Prevent raw request body as output in serialization error messages ([#3205](https://github.com/opensearch-project/security/pull/3205))
* Prevent flaky behavior when determining if an request will be executed on the current node. ([#3066](https://github.com/opensearch-project/security/pull/3066))
* Resolve a class of ConcurrentModificationException from during bulk requests ([#3094](https://github.com/opensearch-project/security/pull/3094))
* Fix Document GET with DLS terms query ([#3136](https://github.com/opensearch-project/security/pull/3136))
* Send log messages to log4j systems instead of system out / error ([#3231](https://github.com/opensearch-project/security/pull/3231))
* Fix roles verification for roles mapping and internal users ([#3278](https://github.com/opensearch-project/security/pull/3278))
* Prevent raw request body as output in serialization error messages ([#3205](https://github.com/opensearch-project/security/pull/3205))
* Fix permissions issues while reading keys in PKCS#1 format ([#3289](https://github.com/opensearch-project/security/pull/3289))


### OpenSearch Security-Dashboards
* When following a link that prompts sign in through SAML or Multi-Auth the destination page is not lost ([#1557](https://github.com/opensearch-project/security-dashboards-plugin/pull/1557))



### SQL
* [2.x] bump okhttp to 4.10.0 (#2043) by @joshuali925 in https://github.com/opensearch-project/sql/pull/2044
* Okio upgrade to 3.5.0 by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1963
* Fixed response codes For Requests With security exception. by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/2029
* Backport breaking changes by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1920
* [Manual Backport #1943] Fixing string format change #1943 by @MitchellGale in https://github.com/opensearch-project/sql/pull/1946
* Fix CVE by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1944
* Breaking change OpenSearch main project - Action movement (#1958) by @MitchellGale in https://github.com/opensearch-project/sql/pull/1965
* Update backport CI, add PR merged condition by @ps48 in https://github.com/opensearch-project/sql/pull/1970
* Fixed exception when datasource is updated with existing configuration. by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/2008


## INFRASTRUCTURE


### OpenSearch Alerting
* Upgrade the backport workflow ([#1028](https://github.com/opensearch-project/alerting/pull/1029))
* Updates demo certs used in integ tests ([#1115](https://github.com/opensearch-project/alerting/pull/1115))



### OpenSearch Anomaly Detection

* Adds auto release workflow ([#1003](https://github.com/opensearch-project/anomaly-detection/pull/1003))
* Upgrading commons-lang3 version to fix conflict issue ([#1014](https://github.com/opensearch-project/anomaly-detection/pull/1014))
* Updates demo certs for integ tests ([#1021](https://github.com/opensearch-project/anomaly-detection/pull/1021))
* Upgrade AD's bwc baseline version to 1.3.2 to resolve cluster join issue ([#1029](https://github.com/opensearch-project/anomaly-detection/pull/1029))



### OpenSearch Anomaly Detection Dashboards

* Remove version dependency in cypress workflow ([#554](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/554))
* Bumped semver to latest legacy version ([#565](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/565))
* Cypress workflow improvements ([#560](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/560))


### OpenSearch Asynchronous Search
* Updates demo certs used in rest tests ([#341](https://github.com/opensearch-project/asynchronous-search/pull/341))
* Adding release workflow for the asynchronous search ([#330](https://github.com/opensearch-project/asynchronous-search/pull/330))
* Refactoring changes in main ([#328](https://github.com/opensearch-project/asynchronous-search/pull/328))



### ### OpenSearch Dashboards Query Workbench

- Update backport CI, add PR merged condition ([#113](https://github.com/opensearch-project/dashboards-query-workbench/pull/113))



### OpenSearch Dashboards Reporting
* Update backport CI, add PR merged condition ([#169](https://github.com/opensearch-project/dashboards-reporting/pull/169))
* Update search snapshots from upstream ([#173](https://github.com/opensearch-project/dashboards-reporting/pull/173))


### OpenSearch Dashboards Search Relevance
* Changing anomaly-detection Dependency Back to search-processor ([#258](https://github.com/opensearch-project/dashboards-search-relevance/pull/258))([#259](https://github.com/opensearch-project/dashboards-search-relevance/pull/259))
* Resolve tough-cookie to 4.1.3 ([#271](https://github.com/opensearch-project/dashboards-search-relevance/pull/271)) ([#272](https://github.com/opensearch-project/dashboards-search-relevance/pull/272))
* Remove Cypress dependency ([#277](https://github.com/opensearch-project/dashboards-search-relevance/pull/277))


### OpenSearch Dashboards Visualizations
* Update backport CI, add PR merged condition ([#228](https://github.com/opensearch-project/dashboards-visualizations/pull/226))
* Update search bar snapshot according to upstream change ([#242](https://github.com/opensearch-project/dashboards-visualizations/pull/242))



### OpenSearch Geospatial
* Make jacoco report to be generated faster in local ([#267](https://github.com/opensearch-project/geospatial/pull/267))
* Exclude lombok generated code from jacoco coverage report ([#268](https://github.com/opensearch-project/geospatial/pull/268))



### OpenSearch Index Management
* Add auto github release workflow. ([#691](https://github.com/opensearch-project/index-management/pull/691))
* Fixed the publish maven workflow to execute after pushes to release branches. ([#837](https://github.com/opensearch-project/index-management/pull/837))
* Upgrade the backport workflow. ([#862](https://github.com/opensearch-project/index-management/pull/862))
* Updates demo certs used in integ tests. ([#921](https://github.com/opensearch-project/index-management/pull/921))



### OpenSearch Index Management Dashboards
* Upgrade the backport workflow. ([#821](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/821))



### OpenSearch ML Commons
* Updates demo certs used in integ tests ([#1291](https://github.com/opensearch-project/ml-commons/pull/1291))
* Add Auto Release Workflow ([#1306](https://github.com/opensearch-project/ml-commons/pull/1306))



### OpenSearch Notifications
* Fix core refactor: StreamIO from common to core.common([#707](https://github.com/opensearch-project/notifications/pull/707))
* Fix core XcontentFactory refactor([#732](https://github.com/opensearch-project/notifications/pull/732))
* Fix actions components after core([#739](https://github.com/opensearch-project/notifications/pull/739))
* Add auto release workflow([#731](https://github.com/opensearch-project/notifications/pull/731))
* Onboarding system and hidden index([#742](https://github.com/opensearch-project/notifications/pull/742))
* Updates demo certs used in integ tests([#756](https://github.com/opensearch-project/notifications/pull/756))



### OpenSearch Observability
* Update backport CI, add PR merged condition in https://github.com/opensearch-project/observability/pull/1587



### OpenSearch Performance Analyzer
* Update BWC version to 2.9.0 [#529](https://github.com/opensearch-project/performance-analyzer/pull/529)
* Update performance-analyzer-commons library version [#537](https://github.com/opensearch-project/performance-analyzer/pull/446)
* Upgrade gRPC protobug to mitigate connection termination issue [#471](https://github.com/opensearch-project/performance-analyzer-rca/pull/471)



### SQL
* Add _primary preference only for segment replication enabled indices by @opensearch-trigger-bot in
  Https://github.com/opensearch-project/sql/pull/2036
* Revert "Guarantee datasource read api is strong consistent read (#1815)" by @opensearch-trigger-bot in
* [Spotless] Adds new line at end of java files by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1925
* (#1506) Remove reservedSymbolTable and replace with HIDDEN_FIELD_NAME… by @acarbonetto in https://github.com/opensearch-project/sql/pull/1964


## DOCUMENTATION


### OpenSearch Alerting
* Added 2.10 release notes ([#1117](https://github.com/opensearch-project/alerting/pull/1117))

### OpenSearch Alerting Dashboards
* Add 2.10.0 release notes ([#707](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/707))

### OpenSearch Asynchronous Search
* Add 2.10.0 release notes ([#353](https://github.com/opensearch-project/asynchronous-search/pull/353))


### OpenSearch Common Utils
* Added 2.10.0.0 release notes ([#531](https://github.com/opensearch-project/common-utils/pull/531))

### OpenSearch Dashboards Notifications
* 2.10 release notes. ([#109](https://github.com/opensearch-project/dashboards-notifications/pull/109))

### OpenSearch Dashboards Search Relevance
* Adding a developer guide ([#268](https://github.com/opensearch-project/dashboards-search-relevance/pull/268)) ([#269](https://github.com/opensearch-project/dashboards-search-relevance/pull/269))



### OpenSearch Index Management
* Added 2.10 release notes. ([#925](https://github.com/opensearch-project/index-management/pull/925))

### OpenSearch Index Management Dashboards
* Added 2.10 release notes. ([#864](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/864))

### OpenSearch ML Commons
* Updating cohere blueprint doc ([#1213](https://github.com/opensearch-project/ml-commons/pull/1213))
* Fixing docs ([#1193](https://github.com/opensearch-project/ml-commons/pull/1193))
* Add model auto redeploy tutorial ([#1175](https://github.com/opensearch-project/ml-commons/pull/1175))
* Add remote inference tutorial ([#1158](https://github.com/opensearch-project/ml-commons/pull/1158))
* Adding blueprint examples for remote inference ([#1155](https://github.com/opensearch-project/ml-commons/pull/1155))
* Updating developer guide for CCI contributors ([#1049](https://github.com/opensearch-project/ml-commons/pull/1049))



### OpenSearch Notifications
* Add 2.10.0 release notes ([#755](https://github.com/opensearch-project/notifications/pull/755))


### OpenSearch Security Analytics
* Added 2.10.0 release notes. ([#555](https://github.com/opensearch-project/security-analytics/pull/555))

### SQL
* Fix doctest data by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1998


## MAINTENANCE


### OpenSearch Alerting
* Increment version to 2.10.0-SNAPSHOT. ([#1018](https://github.com/opensearch-project/alerting/pull/1018))
* Exclude < v32 version of google guava dependency from google java format and add google guava 32.0.1 to resolve CVE CVE-2023-2976 ([#1094](https://github.com/opensearch-project/alerting/pull/1094))


### OpenSearch Alerting Dashboards
* Incremented version to 2.10 ([#703](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/703))
* Bump @cypress/request to 3.0.0 due to CVE-2023-28155 ([#704](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/704))


### OpenSearch Asynchronous Search
* Upgrade Guava version to 32.0.1 ([#347](https://github.com/opensearch-project/asynchronous-search/pull/347))
* Increment version to 2.10.0 ([#321](https://github.com/opensearch-project/asynchronous-search/pull/321))


### OpenSearch Common Utils
* Upgrade the backport workflow ([#487](https://github.com/opensearch-project/common-utils/pull/487))
* Updates demo certs used in rest tests ([#518](https://github.com/opensearch-project/common-utils/pull/518))


### OpenSearch Dashboards Maps
* Bump cypress version to ^13.1.0 ([#462](https://github.com/opensearch-project/dashboards-maps/pull/462))


### OpenSearch Dashboards Notifications
* Bump semver from 5.7.1 to 5.7.2 ([#74](https://github.com/opensearch-project/dashboards-notifications/pull/74))
* Fix: CVE of tough-cookie and work-wrap ([#79](https://github.com/opensearch-project/dashboards-notifications/pull/79))
* Stabilize cypress test case  ([#89](https://github.com/opensearch-project/dashboards-notifications/pull/89))
* [AUTO] Increment version to 2.10.0.0 ([#96](https://github.com/opensearch-project/dashboards-notifications/pull/96))
* Add auto release workflow ([#97](https://github.com/opensearch-project/dashboards-notifications/pull/97))
* Fix: bump @cypress/request to 3.0.0 ([#106](https://github.com/opensearch-project/dashboards-notifications/pull/106))
* Remove unused semver version 6.x and 7.x ([#108](https://github.com/opensearch-project/dashboards-notifications/pull/108))


### OpenSearch Dashboards Query Workbench

* Increment version to 2.10.0.0 ([#100](https://github.com/opensearch-project/dashboards-query-workbench/pull/100))
* Update searchbar snapshots according to upstream changes ([#119](https://github.com/opensearch-project/dashboards-query-workbench/pull/119))

### OpenSearch Dashboards Reporting
* Increment version to 2.10.0.0 ([#152](https://github.com/opensearch-project/dashboards-reporting/pull/152))


### OpenSearch Dashboards Visualizations
* Upgrade tough-cookie to fix CVE-2023-26136 ([#198](https://github.com/opensearch-project/dashboards-visualizations/pull/198))
* Update word-wrap ([#217](https://github.com/opensearch-project/dashboards-visualizations/pull/217))
* Update semver ([#218](https://github.com/opensearch-project/dashboards-visualizations/pull/218))
* Add @cypress/request resolution to fix CVE-2023-28155 ([#245](https://github.com/opensearch-project/dashboards-visualizations/pull/245))


### OpenSearch Geospatial
* Change package for Strings.hasText ([#314](https://github.com/opensearch-project/geospatial/pull/314))
* Fixed compilation errors after refactoring in core foundation classes ([#380](https://github.com/opensearch-project/geospatial/pull/380))
* Version bump for spotlss and apache commons([#400](https://github.com/opensearch-project/geospatial/pull/400))


### OpenSearch Index Management
* Increment version to 2.10.0-SNAPSHOT. ([#852](https://github.com/opensearch-project/index-management/pull/852))


### OpenSearch Job Scheduler
* Update packages according to a change in OpenSearch core ([#422](https://github.com/opensearch-project/job-scheduler/pull/422)) ([#431](https://github.com/opensearch-project/job-scheduler/pull/431))
* Xcontent changes to ODFERestTestCase ([#440](https://github.com/opensearch-project/job-scheduler/pull/440))
* Update LifecycleListener import ([#445](https://github.com/opensearch-project/job-scheduler/pull/445))
* Bump slf4j-api to 2.0.7, ospackage to 11.4.0, google-java-format to 1.17.0, guava to 32.1.2-jre and spotless to 6.20.0 ([#453](https://github.com/opensearch-project/job-scheduler/pull/453))
* Fixing Strings import ([#459](https://github.com/opensearch-project/job-scheduler/pull/459))
* Bump com.cronutils:cron-utils from 9.2.0 to 9.2.1 ([#458](https://github.com/opensearch-project/job-scheduler/pull/458))
* React to changes in ActionListener and ActionFuture ([#467](https://github.com/opensearch-project/job-scheduler/pull/467))
* Bump com.diffplug.spotless from 6.20.0 to 6.21.0 ([#484](https://github.com/opensearch-project/job-scheduler/pull/484))


### OpenSearch k-NN
* Update Guava Version to 32.0.1 ([#1019](https://github.com/opensearch-project/k-NN/pull/1019))


### OpenSearch ML Commons
* Bump checkstyle version for CVE fix ([#1216](https://github.com/opensearch-project/ml-commons/pull/1216))
* Correct imports for new location with regard to core refactoring ([#1206](https://github.com/opensearch-project/ml-commons/pull/1206))
* Fix breaking change caused by opensearch core ([#1187](https://github.com/opensearch-project/ml-commons/pull/1187))
* Bump OpenSearch snapshot version to 2.10 ([#1157](https://github.com/opensearch-project/ml-commons/pull/1157))
* Bump aws-encryption-sdk-java to fix CVE-2023-33201 ([#1309](https://github.com/opensearch-project/ml-commons/pull/1309))


### OpenSearch Notifications
* [AUTO] Increment version to 2.10.0-SNAPSHOT([#706](https://github.com/opensearch-project/notifications/pull/706))


### OpenSearch Performance Analyzer
* Address core refactor changes for Task foundation classes and StreamIO [#522](https://github.com/opensearch-project/performance-analyzer/pull/522)
* Address xcontent changes in core [#526](https://github.com/opensearch-project/performance-analyzer/pull/526)
* Remove usage of deprecated "master" APIs [#513](https://github.com/opensearch-project/performance-analyzer/pull/513)
* Update docker-compose.yml [#465](https://github.com/opensearch-project/performance-analyzer-rca/pull/465)


### OpenSearch Reporting
* Fix CI ([#738](https://github.com/opensearch-project/reporting/pull/738))
* Update backport CI, add PR merged condition ([#745](https://github.com/opensearch-project/reporting/pull/745))


### OpenSearch Security Analytics
* Bump version to 2.10 and resolve compile issues ([#521](https://github.com/opensearch-project/security-analytics/pull/521))


### OpenSearch Security Analytics-Dashboards
* Bumped tough-cookie, and semver versions. ([#658](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/656))
* Update version of word-wrap ([#695](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/695))
* Bump @cypress/request to 3.0.0 due to CVE-2023-28155. ([#702](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/702))


### OpenSearch Security
* [Build Break] Update imports for files refactored in core PR #8157 ([#3003](https://github.com/opensearch-project/security/pull/3003))
* [Build Break] Fix build after Lucene upgrade and breaking XContentFactory changes ([#3069](https://github.com/opensearch-project/security/pull/3069))
* [Build Break] Update CircuitBreakerService and LifecycleComponent after core refactor in #9006 ([#3082](https://github.com/opensearch-project/security/pull/3082))
* [Build Break] React to changes in ActionListener and ActionResponse from #9082 ([#3153](https://github.com/opensearch-project/security/pull/3153))
* [Build Break] Disable gradlew build cache to ensure most up-to-date dependencies ([#3186](https://github.com/opensearch-project/security/pull/3186))
* Bump com.carrotsearch.randomizedtesting:randomizedtesting-runner from 2.7.1 to 2.8.1 ([#3109](https://github.com/opensearch-project/security/pull/3109))
* Bump com.diffplug.spotless from 6.19.0 to 6.21.0 ([#3108](https://github.com/opensearch-project/security/pull/3108))
* Bump com.fasterxml.woodstox:woodstox-core from 6.4.0 to 6.5.1 ([#3148](https://github.com/opensearch-project/security/pull/3148))
* Bump com.github.spotbugs from 5.0.14 to 5.1.3 ([#3251](https://github.com/opensearch-project/security/pull/3251))
* Bump com.github.wnameless.json:json-base from 2.4.0 to 2.4.2 ([#3062](https://github.com/opensearch-project/security/pull/3062))
* Bump com.github.wnameless.json:json-flattener from 0.16.4 to 0.16.5 ([#3296](https://github.com/opensearch-project/security/pull/3296))
* Bump com.google.errorprone:error_prone_annotations from 2.3.4 to 2.20.0 ([#3023](https://github.com/opensearch-project/security/pull/3023))
* Bump com.google.guava:guava from 32.1.1-jre to 32.1.2-jre ([#3149](https://github.com/opensearch-project/security/pull/3149))
* Bump commons-io:commons-io from 2.11.0 to 2.13.0 ([#3074](https://github.com/opensearch-project/security/pull/3074))
* Bump com.netflix.nebula.ospackage from 11.1.0 to 11.3.0 ([#3023](https://github.com/opensearch-project/security/pull/3023))
* Bump com.nulab-inc:zxcvbn from 1.7.0 to 1.8.0 ([#3023](https://github.com/opensearch-project/security/pull/3023))
* Bump com.unboundid:unboundid-ldapsdk from 4.0.9 to 4.0.14 ([#3143](https://github.com/opensearch-project/security/pull/3143))
* Bump io.dropwizard.metrics:metrics-core from 3.1.2 to 4.2.19 ([#3073](https://github.com/opensearch-project/security/pull/3073))
* Bump kafka_version from 3.5.0 to 3.5.1 ([#3041](https://github.com/opensearch-project/security/pull/3041))
* Bump net.minidev:json-smart from 2.4.11 to 2.5.0 ([#3120](https://github.com/opensearch-project/security/pull/3120))
* Bump org.apache.camel:camel-xmlsecurity from 3.14.2 to 3.21.0 ([#3023](https://github.com/opensearch-project/security/pull/3023))
* Bump org.apache.santuario:xmlsec from 2.2.3 to 2.3.3 ([#3210](https://github.com/opensearch-project/security/pull/3210))
* Bump org.checkerframework:checker-qual from 3.5.0 to 3.36.0 ([#3023](https://github.com/opensearch-project/security/pull/3023))
* Bump org.cryptacular:cryptacular from 1.2.4 to 1.2.5 ([#3071](https://github.com/opensearch-project/security/pull/3071))
* Bump org.gradle.test-retry from 1.5.2 to 1.5.4 ([#3072](https://github.com/opensearch-project/security/pull/3072))
* Bump org.junit.jupiter:junit-jupiter from 5.8.2 to 5.10.0 ([#3146](https://github.com/opensearch-project/security/pull/3146))
* Bump org.ow2.asm:asm from 9.1 to 9.5 ([#3121](https://github.com/opensearch-project/security/pull/3121))
* Bump org.scala-lang:scala-library from 2.13.9 to 2.13.11 ([#3119](https://github.com/opensearch-project/security/pull/3119))
* Bump org.slf4j:slf4j-api from 1.7.30 to 1.7.36 ([#3249](https://github.com/opensearch-project/security/pull/3249))
* Bump org.xerial.snappy:snappy-java from 1.1.10.1 to 1.1.10.3 ([#3106](https://github.com/opensearch-project/security/pull/3106))
* Bump actions/create-release from 1.0.0 to 1.1.4 ([#3141](https://github.com/opensearch-project/security/pull/3141))
* Bump actions/setup-java from 1 to 3 ([#3142](https://github.com/opensearch-project/security/pull/3142))
* Bump actions/upload-release-asset from 1.0.1 to 1.0.2 ([#3144](https://github.com/opensearch-project/security/pull/3144))
* Bump fernandrone/linelint from 0.0.4 to 0.0.6 ([#3211](https://github.com/opensearch-project/security/pull/3211))
* Bump tibdex/github-app-token from 1.5.0 to 1.8.0 ([#3147](https://github.com/opensearch-project/security/pull/3147))
* Remove log spam for files that are cleaned up ([#3118](https://github.com/opensearch-project/security/pull/3118))
* Updates integTestRemote task to dynamically fetch common-utils version from build.gradle ([#3122](https://github.com/opensearch-project/security/pull/3122))
* Switch CodeQL to assemble artifacts using the same build as the rest of CI ([#3132](https://github.com/opensearch-project/security/pull/3132))
* Only run the backport job on merged pull requests ([#3134](https://github.com/opensearch-project/security/pull/3134))
* Add code coverage exclusions on false positives ([#3196](https://github.com/opensearch-project/security/pull/3196))
* Enable jarhell check ([#3227](https://github.com/opensearch-project/security/pull/3227))
* Retry code coverage upload on failure ([#3242](https://github.com/opensearch-project/security/pull/3242))
* [Refactor] Adopt request builder patterns for SecurityRestApiActions for consistency and clarity ([#3123](https://github.com/opensearch-project/security/pull/3123))
* [Refactor] Remove json-path from deps and use JsonPointer instead ([#3262](https://github.com/opensearch-project/security/pull/3262))
* Use version of org.apache.commons:commons-lang3 defined in core ([#3306](https://github.com/opensearch-project/security/pull/3306))
* Fix checkstyle #3283
* Demo Configuration changes ([#3330](https://github.com/opensearch-project/security/pull/3330))


### OpenSearch Security-Dashboards
* Force resolution of selenium-webdriver to 4.10.0 ([#1541](https://github.com/opensearch-project/security-dashboards-plugin/pull/1541))
* Change the regex command in install dashboard GHA ([#1533](https://github.com/opensearch-project/security-dashboards-plugin/pull/1533))


## REFACTORING


### OpenSearch Alerting
* Update actionGet to SuspendUntil for ClusterMetrics ([#1067](https://github.com/opensearch-project/alerting/pull/1067))
* Resolve compile issues from core changes and update CIs ([#1100](https://github.com/opensearch-project/alerting/pull/1100))


### OpenSearch Anomaly Detection
* Refactor due to core updates: Replace and modify classes and methods. ([#974](https://github.com/opensearch-project/anomaly-detection/pull/974))


### OpenSearch Geospatial
* Refactor LifecycleComponent package path ([#377](https://github.com/opensearch-project/geospatial/pull/377))
* Refactor Strings utility methods to core library ([#379](https://github.com/opensearch-project/geospatial/pull/379))


### OpenSearch Index Management
* Fix after core #8157. ([#886](https://github.com/opensearch-project/index-management/pull/886))
* Fix breaking change by core refactor. ([#888](https://github.com/opensearch-project/index-management/pull/888))
* Handle core breaking change. ([#895](https://github.com/opensearch-project/index-management/pull/895))
* Set preference to _primary when searching control-center index. ([#911](https://github.com/opensearch-project/index-management/pull/911))
* Add primary first preference to all search requests. ([#912](https://github.com/opensearch-project/index-management/pull/912))


### OpenSearch k-NN
* Fix TransportAddress Refactoring Changes in Core ([#1020](https://github.com/opensearch-project/k-NN/pull/1020))


### OpenSearch ML Commons
* Renaming metrics ([#1224](https://github.com/opensearch-project/ml-commons/pull/1224))
* Changing messaging for IllegalArgumentException on duplicate model groups ([#1294](https://github.com/opensearch-project/ml-commons/pull/1294))
* Fixing some error message handeling ([#1222](https://github.com/opensearch-project/ml-commons/pull/1222)) 


### OpenSearch Observability
* Fix from upstream core.action changes in https://github.com/opensearch-project/observability/pull/1590
* Pull jackson,mockito versions from upstream in https://github.com/opensearch-project/observability/pull/1598
* Updates demo certs used in integ tests in https://github.com/opensearch-project/observability/pull/1600


### OpenSearch Security Analytics
* Fix google-java-format-1.17.0.jar: 1 vulnerabilities ([#526](https://github.com/opensearch-project/security-analytics/pull/526))
* Segment replication changes ([#529](https://github.com/opensearch-project/security-analytics/pull/529))
* Use core OpenSearch version of commons-lang3 ([#535](https://github.com/opensearch-project/security-analytics/pull/535))
* Force google guava to 32.0.1 ([#536](https://github.com/opensearch-project/security-analytics/pull/536))
* Updates demo certs used in integ tests ([#543](https://github.com/opensearch-project/security-analytics/pull/543))


### OpenSearch Security Analytics-Dashboards
* UI polish for correlations and custom log types. ([#683](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/683))
* [Correlations] Update node size and cursor in correlations graph ([#687](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/687))
* Updates to log types related UX. ([#694](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/694))


### SQL
* Applied formatting improvements to Antlr files based on spotless changes (#2017) by @MitchellGale in
* Statically init `typeActionMap` in `OpenSearchExprValueFactory`. by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1901
* (#1536) Refactor OpenSearchQueryRequest and move includes to builder by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1948
* [Spotless] Applying Google Code Format for core/src/main files #3 (#1932) by @MitchellGale in https://github.com/opensearch-project/sql/pull/1994
* Developer guide update with Spotless details by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/2004
* [Spotless] Applying Google Code Format for core/src/main files #4 #1933 by @MitchellGale in https://github.com/opensearch-project/sql/pull/1995
* [Spotless] Applying Google Code Format for core/src/main files #2 #1931 by @MitchellGale in https://github.com/opensearch-project/sql/pull/1993
* [Spotless] Applying Google Code Format for core/src/main files #1 #1930 by @MitchellGale in https://github.com/opensearch-project/sql/pull/1992
* [Spotless] Applying Google Code Format for core #5 (#1951) by @MitchellGale in https://github.com/opensearch-project/sql/pull/1996
* [spotless] Removes Checkstyle in favor of spotless by @MitchellGale in https://github.com/opensearch-project/sql/pull/2018
* [Spotless] Entire project running spotless by @MitchellGale in https://github.com/opensearch-project/sql/pull/2016
