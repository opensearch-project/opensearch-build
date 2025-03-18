# OpenSearch and OpenSearch Dashboards 3.0.0-alpha1 Release Notes

## Release Highlights
* Lucene 10 is now used in OpenSearch 3.0.0-alpha1
* This is an early-stage preview of the 3.0.0 version, so expect potential bugs and unfinished features. This release is for testing purposes only, and we highly encourage users to try it out and report any issues or feedback. Please refer to the [release schedule](https://opensearch.org/releases.html) for GA release information.

### DEPRECATION NOTICES

**Deprecating support for Ubuntu Linux 20.04**
Please note that OpenSearch and OpenSearch Dashboards will deprecate support for Ubuntu Linux 20.04 as a continuous integration build image and supported operating system in an upcoming version, as Ubuntu Linux 20.04 will reach end-of-life with standard support as of April 2025 (refer to [this notice](https://ubuntu.com/blog/ubuntu-20-04-lts-end-of-life-standard-support-is-coming-to-an-end-heres-how-to-prepare) from Canonical Ubuntu). For a list of the compatible operating systems, [visit here](https://opensearch.org/docs/latest/install-and-configure/os-comp/).

**Deprecating support for Amazon Linux 2 on OpenSearch Dashboards**
Please note that OpenSearch Dashboards will deprecate support for Amazon Linux 2 as a continuous integration build image and supported operating system in an upcoming version, as Node.js 18 will reach end-of-life with support as of April 2025 (refer to [this notice](https://nodejs.org/en/blog/announcements/v18-release-announce) from nodejs.org) and newer version of Node.js LTS version (20+) will not support runtime on Amazon Linux 2. For a list of the compatible operating systems, [visit here](https://opensearch.org/docs/latest/install-and-configure/os-comp/).

## Breaking Changes
* For a full list of breaking changes and deprecated/removed features in version 3.0.0, please see details in the [meta issues](https://github.com/opensearch-project/opensearch-build/issues/5243).

### Opensearch ML Common

* Use \_list/indices API instead of \_cat/index API in CatIndexTool (#3243)[https://github.com/opensearch-project/ml-commons/pull/3243]


### Opensearch Security


* Optimized Privilege Evaluation ([#4380](https://github.com/opensearch-project/security/pull/4380))
* Fix Blake2b hash implementation ([#5089](https://github.com/opensearch-project/security/pull/5089))


### Opensearch k-NN


* Remove ef construction from Index Seeting [#2564](https://github.com/opensearch-project/k-NN/pull/2564)
* Remove m from Index Setting [#2564](https://github.com/opensearch-project/k-NN/pull/2564)
* Remove space type from index setting [#2564](https://github.com/opensearch-project/k-NN/pull/2564)
* Remove Knn Plugin enabled setting [#2564](https://github.com/opensearch-project/k-NN/pull/2564)

### OpenSearch SQL


* [Release 3.0] Bump gradle 8.10.2 / JDK23 / 3.0.0.0-alpha1 on SQL plugin ([#3319](https://github.com/opensearch-project/sql/pull/3319))
* [v3.0.0] Remove SparkSQL support ([#3306](https://github.com/opensearch-project/sql/pull/3306))
* [v3.0.0] Remove opendistro settings and endpoints ([#3326](https://github.com/opensearch-project/sql/pull/3326))
* [v3.0.0] Deprecate SQL Delete statement ([#3337](https://github.com/opensearch-project/sql/pull/3337))
* [v3.0.0] Deprecate scroll API usage ([#3346](https://github.com/opensearch-project/sql/pull/3346))
* [v3.0.0] Deprecate OpenSearch DSL format ([#3367](https://github.com/opensearch-project/sql/pull/3367))

## Release Details
[OpenSearch and OpenSearch Dashboards 3.0.0-alpha1](https://opensearch.org/versions/opensearch-3-0-0-alpha1.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.0.0-alpha1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.0.0-alpha1.md).


## FEATURES


### OpenSearch Dashboards Assistant


* Expose chatEnabled flag to capabilities ([#398](https://github.com/opensearch-project/dashboards-assistant/pull/398))
* Update chatbot UI to align with new look ([#435](https://github.com/opensearch-project/dashboards-assistant/pull/435))
* Add data to summary response post processing ([#436](https://github.com/opensearch-project/dashboards-assistant/pull/436))
* Add flag to control if display conversation list ([#438](https://github.com/opensearch-project/dashboards-assistant/pull/438))
* When open chatbot, load the last conversation automatically ([#439](https://github.com/opensearch-project/dashboards-assistant/pull/439))
* Add index type detection ([#454](https://github.com/opensearch-project/dashboards-assistant/pull/454))
* Add error handling when open chatbot and loading conversation ([#485](https://github.com/opensearch-project/dashboards-assistant/pull/485))
* Generate visualization on t2v page mount ([#505](https://github.com/opensearch-project/dashboards-assistant/pull/505))
* Update insight badge ([#507](https://github.com/opensearch-project/dashboards-assistant/pull/507))


### OpenSearch Common Utils


* Adding replication (CCR) plugin interface and classes to common-utils ([#667](https://github.com/opensearch-project/common-utils/pull/667))


### OpenSearch Custom Codecs


* Upgrade to Lucene 10.1.0 and Introduce new Codec implementation for the upgrade ([#228](https://github.com/opensearch-project/custom-codecs/pull/228))


### OpenSearch Dashboards Maps


* Introduce cluster layer in maps-dashboards ([#703](https://github.com/opensearch-project/dashboards-maps/pull/703))


### OpenSearch Flow Framework Dashboards


* Add fine-grained error handling ([#598](https://github.com/opensearch-project/dashboards-flow-framework/pull/598))
* Change ingestion input to JSON lines format ([#639](https://github.com/opensearch-project/dashboards-flow-framework/pull/639))


### OpenSearch Index Management


* Adding unfollow action in ism to invoke stop replication for ccr ([#1198](https://github.com/opensearch-project/index-management/pull/1198))


### OpenSearch Security Analytics


* Adds support for uploading threat intelligence in Custom Format ([#1493](https://github.com/opensearch-project/security-analytics/pull/1493))


### OpenSearch Security Analytics Dashboards


* Add support for custom ioc schema in threat intel source ([#1266](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1266))


### OpenSearch k-NN


* Introduce Remote Native Index Build feature flag, settings, and initial skeleton [#2525](https://github.com/opensearch-project/k-NN/pull/2525)
* Implement vector data upload and vector data size threshold setting [#2550](https://github.com/opensearch-project/k-NN/pull/2550)
* Implement data download and IndexOutput write functionality [#2554](https://github.com/opensearch-project/k-NN/pull/2554)
* Introduce Client Skeleton + basic Build Request implementation [#2560](https://github.com/opensearch-project/k-NN/pull/2560)
* Add concurrency optimizations with native memory graph loading and force eviction [#2345](https://github.com/opensearch-project/k-NN/pull/2345)


### OpenSearch SQL


* PPL: Add `json` function and `cast(x as json)` function ([#3243](https://github.com/opensearch-project/sql/pull/3243))


## ENHANCEMENTS


### OpenSearch Dashboards Assistant


* Remove os\_insight agent ([#452](https://github.com/opensearch-project/dashboards-assistant/pull/452))
* Hide the assistant entry when there isn't data2summary agent ([#417](https://github.com/opensearch-project/dashboards-assistant/pull/417))
* Adjust buttons' padding inside alert in-context insight popover ([#467](https://github.com/opensearch-project/dashboards-assistant/pull/467))
* Add a space to the left of the AI action menu button ([#486](https://github.com/opensearch-project/dashboards-assistant/pull/486))
* Add a tooltip for disabled assistant action button ([#490](https://github.com/opensearch-project/dashboards-assistant/pull/490))
* Improve the text to visualization error handling ([#491](https://github.com/opensearch-project/dashboards-assistant/pull/491))
* Optimize source selector width in t2v page ([#497](https://github.com/opensearch-project/dashboards-assistant/pull/497))
* Show error message if PPL query does not contain aggregation ([#499](https://github.com/opensearch-project/dashboards-assistant/pull/499))
* Adjust the overall style of alert summary popover ([#501](https://github.com/opensearch-project/dashboards-assistant/pull/501))
* Add http error instruction for t2ppl task ([#502](https://github.com/opensearch-project/dashboards-assistant/pull/502))
* Change the background color, button position and text for alert summary popover ([#506](https://github.com/opensearch-project/dashboards-assistant/pull/506))
* Collect metrics for when t2viz triggered ([#510](https://github.com/opensearch-project/dashboards-assistant/pull/510))
* Chatbot dock bottom border top ([#511](https://github.com/opensearch-project/dashboards-assistant/pull/511))
* Update the no aggregation PPL error message ([#512](https://github.com/opensearch-project/dashboards-assistant/pull/512))


### OpenSearch Flow Framework Dashboards


* Integrate legacy presets with quick-configure fields ([#602](https://github.com/opensearch-project/dashboards-flow-framework/pull/602))
* Simplify RAG presets, add bulk API details ([#610](https://github.com/opensearch-project/dashboards-flow-framework/pull/610))
* Improve RAG preset experience ([#617](https://github.com/opensearch-project/dashboards-flow-framework/pull/617))
* Update model options and callout ([#622](https://github.com/opensearch-project/dashboards-flow-framework/pull/622))
* Added popover to display links to suggested models ([#625](https://github.com/opensearch-project/dashboards-flow-framework/pull/625))
* Implicitly update input maps defined on non-expanded queries (common cases) ([#632](https://github.com/opensearch-project/dashboards-flow-framework/pull/632))
* Show interim JSON provision flow even if provisioned ([#633](https://github.com/opensearch-project/dashboards-flow-framework/pull/633))
* Add functional buttons in form headers, fix query parse bug ([#649](https://github.com/opensearch-project/dashboards-flow-framework/pull/649))
* Block simulate API calls if datasource version is missing ([#657](https://github.com/opensearch-project/dashboards-flow-framework/pull/657))
* Update default queries, update quick config fields, misc updates ([#660](https://github.com/opensearch-project/dashboards-flow-framework/pull/660))
* Update visible plugin name to 'AI Search Flows' ([#662](https://github.com/opensearch-project/dashboards-flow-framework/pull/662))
* Update plugin name and rearrange Try AI Search Flows card ([#664](https://github.com/opensearch-project/dashboards-flow-framework/pull/664))


### OpenSearch ML Common


* Support sentence highlighting QA model (#3600)[https://github.com/opensearch-project/ml-commons/pull/3600]


### OpenSearch Neural Search


* Set neural-search plugin 3.0.0 baseline JDK version to JDK-21 ([#838](https://github.com/opensearch-project/neural-search/pull/838))
* Support different embedding types in model's response ([#1007](https://github.com/opensearch-project/neural-search/pull/1007))


### OpenSearch Query Insights


* Add default index template for query insights local index ([#254](https://github.com/opensearch-project/query-insights/pull/254))
* Change local index replica count to 0 ([#257](https://github.com/opensearch-project/query-insights/pull/257))
* Use ClusterStateRequest with index pattern when searching for expired local indices ([#262](https://github.com/opensearch-project/query-insights/pull/262))
* Add strict hash check on top queries indices ([#266](https://github.com/opensearch-project/query-insights/pull/266))


### OpenSearch Query Insights Dashboards


* Unit test for QueryUtils, application, plugin ([#96](https://github.com/opensearch-project/query-insights-dashboards/pull/96))
* Bump to 3.0.0-alpha1 ([#127](https://github.com/opensearch-project/query-insights-dashboards/pull/127))


### Opensearch k-NN


* Introduce node level circuit breakers for k-NN [#2509](https://github.com/opensearch-project/k-NN/pull/2509)
* Added more detailed error messages for KNN model training [#2378](https://github.com/opensearch-project/k-NN/pull/2378)


### OpenSearch SQL

* Add other functions to SQL query validator ([#3304](https://github.com/opensearch-project/sql/pull/3304))
* Improved patterns command with new algorithm ([#3263](https://github.com/opensearch-project/sql/pull/3263))
* Clean up syntax error reporting ([#3278](https://github.com/opensearch-project/sql/pull/3278))

### Opensearch Security


* Add support for CIDR ranges in `ignore_hosts` setting ([#5099](https://github.com/opensearch-project/security/pull/5099))
* Add 'good' as a valid value for `plugins.security.restapi.password_score_based_validation_strength` ([#5119](https://github.com/opensearch-project/security/pull/5119))
* Adding stop-replication permission to `index_management_full_access` ([#5160](https://github.com/opensearch-project/security/pull/5160))
* Replace password generator step with a secure password generator action ([#5153](https://github.com/opensearch-project/security/pull/5153))

## BUG FIXES


### OpenSearch Dashboards Assistant


* Fixed incorrect message id field used ([#378](https://github.com/opensearch-project/dashboards-assistant/pull/378))
* Improve alert summary with backend log pattern experience ([#389](https://github.com/opensearch-project/dashboards-assistant/pull/389))
* fixed in context feature returning 500 error if workspace is invalid to returning 4XX ([#429](https://github.com/opensearch-project/dashboards-assistant/pull/429))([#458](https://github.com/opensearch-project/dashboards-assistant/pull/458))
* fix incorrect insight API response ([#473](https://github.com/opensearch-project/dashboards-assistant/pull/473/files))
* Improve error handling for index type detection ([#472](https://github.com/opensearch-project/dashboards-assistant/pull/472))
* Fix header button input sending messages to active conversation ([#481](https://github.com/opensearch-project/dashboards-assistant/pull/481))
* Shrink source selector in t2v page ([#492](https://github.com/opensearch-project/dashboards-assistant/pull/492))
* Increase search selector width in t2v page ([#495](https://github.com/opensearch-project/dashboards-assistant/pull/495))
* Fix bottom spacing for chatbot flyout's input box ([#496](https://github.com/opensearch-project/dashboards-assistant/pull/496))
* Fix incontext insight popover close ([#498](https://github.com/opensearch-project/dashboards-assistant/pull/498))
* Fix error handling for data source connection errors ([#500](https://github.com/opensearch-project/dashboards-assistant/pull/500))
* Fix bug by hiding alert summary when clicking alert name ([#482](https://github.com/opensearch-project/dashboards-assistant/pull/482))
* Fix alert summary message action position when no discover button ([#504](https://github.com/opensearch-project/dashboards-assistant/pull/504))
* Remove text in badge to make it compatible with small screen ([#509](https://github.com/opensearch-project/dashboards-assistant/pull/509))


### OpenSearch Alerting


* Fix bucket selector aggregation writeable name. ([#1780](https://github.com/opensearch-project/alerting/pull/1780))


### OpenSearch Common Utils


* Fix imports related to split package of org.opensearch.transport ([#790](https://github.com/opensearch-project/common-utils/pull/790))


### OpenSearch Cross Cluster Replication


* Disabling knn validation checks ([#1515](https://github.com/opensearch-project/cross-cluster-replication/pull/1515))


### OpenSearch Dashboards Maps


* Fix layer config panel background color inconsistency ([#704](https://github.com/opensearch-project/dashboards-maps/pull/704))


### OpenSearch Dashboards Reporting


* [Bug]Support for date range in report generation ([#524](https://github.com/opensearch-project/dashboards-reporting/pull/524))


### OpenSearch Flow Framework Dashboards


* Fix error that local cluster cannot get version ([#606](https://github.com/opensearch-project/dashboards-flow-framework/pull/606))
* UX fit-n-finish updates XI ([#613](https://github.com/opensearch-project/dashboards-flow-framework/pull/613))
* UX fit-n-finish updates XII ([#618](https://github.com/opensearch-project/dashboards-flow-framework/pull/618))
* Bug fixes XIII ([#630](https://github.com/opensearch-project/dashboards-flow-framework/pull/630))
* Various bug fixes & improvements ([#644](https://github.com/opensearch-project/dashboards-flow-framework/pull/644))
* Fixed bug related to Search Index in Local Cluster scenario ([#654](https://github.com/opensearch-project/dashboards-flow-framework/pull/654))


### OpenSearch Index Management


* Target Index Settings if create index during rollup ([#1377](https://github.com/opensearch-project/index-management/pull/1377))
* Fixed CVE upgrade logback-core to 1.5.13 ([#1388](https://github.com/opensearch-project/index-management/pull/1388))


### OpenSearch Index Management Dashboards Plugin


* Fix wrong urls to documentation ([#1278](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1278))
* Fixed CVE in glob-parent and braces dependencies ([#1287](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1287))


### OpenSearch Job Scheduler


* Fix job-scheduler with OpenSearch Refactoring [#730](https://github.com/opensearch-project/job-scheduler/pull/730).
* Fetch certs from security repo and remove locally checked in demo certs [#713](https://github.com/opensearch-project/job-scheduler/pull/713).
* Only download demo certs when integTest run with `-Dsecurity.enabled=true` [#737](https://github.com/opensearch-project/job-scheduler/pull/737).


### OpenSearch ML Common


* Fix building error due to a breaking change from core (#3617)[https://github.com/opensearch-project/ml-commons/pull/3617]


### OpenSearch Neural Search


* Fix a bug to unflatten the doc with list of map with multiple entries correctly ([#1204](https://github.com/opensearch-project/neural-search/pull/1204)).


### OpenSearch Observability


* [Bug] Traces/Services remove toast message on empty data ([#2346] (https://github.com/opensearch-project/dashboards-observability/pull/2346))


* Restore spans limit to 3000 in trace view ([#2353] (https://github.com/opensearch-project/dashboards-observability/pull/2353))
* [BUG] Updated cache for the sub tree in Workbench ([#2351] (https://github.com/opensearch-project/dashboards-observability/pull/2351))
* Trace Groups Optimization - Remove duplicate filters ([#2368] (https://github.com/opensearch-project/dashboards-observability/pull/2368))
* [Bug] Traces redirection while QA enabled ([#2369] (https://github.com/opensearch-project/dashboards-observability/pull/2369))


### OpenSearch Query Insights


* Fix github upload artifact error ([#229](https://github.com/opensearch-project/query-insights/pull/229))
* Fix default exporter settings ([#234](https://github.com/opensearch-project/query-insights/pull/234))
* Fix unit test SearchQueryCategorizerTests.testFunctionScoreQuery ([#270](https://github.com/opensearch-project/query-insights/pull/270))


### OpenSearch Query Insights Dashboards


* Fix: duplicated requests on refreshing the overview ([#138](https://github.com/opensearch-project/query-insights-dashboards/pull/138))
* Fix: Placeholder ${metric} Not Replaced with Actual Metric Type ([#140](https://github.com/opensearch-project/query-insights-dashboards/pull/140))


### OpenSearch Query Workbench


* [Bug]Side tree flyout fix in async operations ([#448] (https://github.com/opensearch-project/dashboards-query-workbench/pull/448))


### OpenSearch Remote Metadata Sdk


* Fix version conflict check for update ([#114](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/114))


### OpenSearch Security Analytics


* Refactored flaky test. ([#1467](https://github.com/opensearch-project/security-analytics/pull/1467))


### OpenSearch k-NN


* Fix derived source for binary and byte vectors [#2533](https://github.com/opensearch-project/k-NN/pull/2533/)


* Fix the put mapping issue for already created index with flat mapper [#2542](https://github.com/opensearch-project/k-NN/pull/2542)
* Fixing the bug to prevent index.knn setting from being modified or removed on restore snapshot [#2445](https://github.com/opensearch-project/k-NN/pull/2445)


### Opensearch Security

* Fix version matcher string in demo config installer ([#5157](https://github.com/opensearch-project/security/pull/5157))



## INFRASTRUCTURE


### OpenSearch Dashboards Maps


* Increment version to 3.0.0-alpha1 ([#708](https://github.com/opensearch-project/dashboards-maps/pull/708))


### OpenSearch Flow Framework


* Set Java target compatibility to JDK 21 ([#730](https://github.com/opensearch-project/flow-framework/pull/730))


### OpenSearch Neural Search


* [3.0] Update neural-search for OpenSearch 3.0 compatibility ([#1141](https://github.com/opensearch-project/neural-search/pull/1141))


### OpenSearch Observability


* Improve the test results for Integrations internals ([#2376] (https://github.com/opensearch-project/dashboards-observability/pull/2376))


### OpenSearch Query Insights


* Fix pipeline on main branch ([#274](https://github.com/opensearch-project/query-insights/pull/274))


### OpenSearch Query Insights Dashboards

* Bump to 3.0.0-alpha1 ([#127](https://github.com/opensearch-project/query-insights-dashboards/pull/127))


### OpenSearch Skills


* Replace `ml-common-client` build dependency to `ml-common-common` and `ml-common-spi` (#529)[https://github.com/opensearch-project/skills/pull/529]


### OpenSearch k-NN


* Removed JDK 11 and 17 version from CI runs [#1921](https://github.com/opensearch-project/k-NN/pull/1921)
* Upgrade min JDK compatibility to JDK 21 [#2422](https://github.com/opensearch-project/k-NN/pull/2422)


## DOCUMENTATION


### OpenSearch Flow Framework


* Add text to visualization agent template ([#936](https://github.com/opensearch-project/flow-framework/pull/936))


### OpenSearch ML Common


* Add tutorial for RAG of openai and bedrock (#2975)[https://github.com/opensearch-project/ml-commons/pull/2975]
* Fix template query link (#3612)[https://github.com/opensearch-project/ml-commons/pull/3612]


### OpenSearch Neural Search


* Adding code guidelines ([#502](https://github.com/opensearch-project/neural-search/pull/502))


### OpenSearch Query Insights


* 3.0.0.0-Alpha1 Release Notes ([#278](https://github.com/opensearch-project/query-insights/pull/278))


### OpenSearch Query Insights Dashboards


* 3.0.0.0-Alpha1 Release Notes ([#147](https://github.com/opensearch-project/query-insights-dashboards/pull/147))


### OpenSearch Skills


* Add tutorial to build and test custom tool (#521)[https://github.com/opensearch-project/skills/pull/521]


## MAINTENANCE


### OpenSearch Dashboards Assistant


* Bump version to 3.0.0.0-alpha1 ([#450](https://github.com/opensearch-project/dashboards-assistant/pull/450))
* Chore(deps): update dependency dompurify to v3.2.4 ([#461](https://github.com/opensearch-project/dashboards-assistant/pull/461))
* Chore(deps): update dependency dompurify to v3.2.3 ([#383](https://github.com/opensearch-project/dashboards-assistant/pull/383))


### OpenSearch Alerting


* Increment version to 3.0.0.0-alpha1 ([#1786](https://github.com/opensearch-project/alerting/pull/1786))
* CVE fix for ktlint ([#1802](https://github.com/opensearch-project/alerting/pull/1802))
* Fix security-enabled test configurations for 3.0-alpha1. ([#1807](https://github.com/opensearch-project/alerting/pull/1807))


### OpenSearch Alerting Dashboards Plugin


* [Release 3.0] Add alpha1 qualifier. ([#1218](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1218))
* Fix CVE. ([#1223](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1223))


### OpenSearch Anomaly Detection


* Fix breaking changes for 3.0.0 release ([#1424](https://github.com/opensearch-project/anomaly-detection/pull/1424))


### OpenSearch Anomaly Detection Dashboards


* Bump to version 3.0.0.0-alpha1 ([#985](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/985))


### OpenSearch Asynchronous Search


* Update main branch for 3.0.0.0-alpha1 / gradle 8.10.2 / JDK23 ([#698](https://github.com/opensearch-project/asynchronous-search/pull/698))


### OpenSearch Common Utils


* Update common-utils shadow plugin repo and bump to 3.0.0.0-alpha1 ([#775](https://github.com/opensearch-project/common-utils/pull/775))


### OpenSearch Cross Cluster Replication


* Version bump to opensearch-3.0.0-alpha1 and replaced usage of deprecated classes
* Update CCR with gradle 8.10.2 and support JDK23 ([#1496](https://github.com/opensearch-project/cross-cluster-replication/pull/1496))


### OpenSearch Dashboards Notifications


* [Release 3.0] Add alpha1 qualifier. ([#333](https://github.com/opensearch-project/dashboards-notifications/pull/333))


### OpenSearch Dashboards Reporting


* Change dompurify version to 3.0.11 to match OSD ([#516](https://github.com/opensearch-project/dashboards-reporting/pull/516))
* Bump jspdf to 3.0 to fix CVE-2025-26791 ([#529](https://github.com/opensearch-project/dashboards-reporting/pull/529))
* Bump dashboards reporting to version 3.0.0.0-alpha1 ([#536](https://github.com/opensearch-project/dashboards-reporting/pull/536))
* CVE fix for elliptic and update release notes ([#550](https://github.com/opensearch-project/dashboards-reporting/pull/550))


### OpenSearch Dashboards Search Relevance


* Increment version to 3.0.0.0-alpha1 ([#486](https://github.com/opensearch-project/dashboards-search-relevance/pull/486))


### OpenSearch Flow Framework


* Fix breaking changes for 3.0.0 release ([#1026](https://github.com/opensearch-project/flow-framework/pull/1026))


### OpenSearch Flow Framework Dashboards


* Support 2.17 BWC with latest backend integrations ([#612](https://github.com/opensearch-project/dashboards-flow-framework/pull/612))


### OpenSearch Geospatial


* Set geospatial plugin 3.0.0 baseline JDK version to JDK-21 ([#695](https://github.com/opensearch-project/geospatial/pull/695))
* Bump gradle 8.10.2 / JDK 23 / 3.0.0.0-alpha1 support on geospatial ([#723](https://github.com/opensearch-project/geospatial/pull/723))


### OpenSearch Index Management


* dependabot: bump com.netflix.nebula.ospackage from 11.10.1 to 11.11.1 ([#1374](https://github.com/opensearch-project/index-management/pull/1374))
* dependabot: bump commons-beanutils:commons-beanutils ([#1375](https://github.com/opensearch-project/index-management/pull/1375))
* dependabot: bump io.gitlab.arturbosch.detekt:detekt-gradle-plugin ([#1381](https://github.com/opensearch-project/index-management/pull/1381))
* [Release 3.0.0] Bump Version to 3.0.0-alpha1 and updated shadowPlugin ([#1384](https://github.com/opensearch-project/index-management/pull/1384))


### OpenSearch Index Management Dashboards Plugin


* Index Management Dashboards plugin to version 3.0.0.0-alpha1 ([#1265](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1265))
* Updated Micromatch new version ([#1273](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1273))


### OpenSsearch Job Scheduler


* Increment version to 3.0.0-alpha1 [#722](https://github.com/opensearch-project/job-scheduler/pull/722).
* Update shadow plugin to `com.gradleup.shadow` [#722](https://github.com/opensearch-project/job-scheduler/pull/722).
* Enable custom start commands and options to resolve GHA issues [#702](https://github.com/opensearch-project/job-scheduler/pull/702).
* Fix delete merged branch workflow [#693](https://github.com/opensearch-project/job-scheduler/pull/693).
* Update `PULL_REQUEST_TEMPLATE` to include an API spec change in the checklist [#649](https://github.com/opensearch-project/job-scheduler/pull/649).
* Fix checkout action failure [#650](https://github.com/opensearch-project/job-scheduler/pull/650).


### OpenSearch ML Common


* Update CB setting to 100 to bypass memory check (#3627)[https://github.com/opensearch-project/ml-commons/pull/3627]
* Use model type to check local or remote model (#3597)[https://github.com/opensearch-project/ml-commons/pull/3597]
* Fixing security integ test (#3646)[https://github.com/opensearch-project/ml-commons/pull/3646]


### OpenSearch ML Commons Dashboards


* Bump version to 3.0.0.0-alpha1 ([#400](https://github.com/opensearch-project/ml-commons-dashboards/pull/400))


### OpenSearch Notifications


* [Release 3.0] Add alpha1 qualifier. ([#1002](https://github.com/opensearch-project/notifications/pull/1002))
* Get bwc version dynamically ([#987](https://github.com/opensearch-project/notifications/pull/987))
* bump logback to 1.5.16 ([#1003](https://github.com/opensearch-project/notifications/pull/1003))
* Fix security-enabled test workflow. ([#1007](https://github.com/opensearch-project/notifications/pull/1007))


### OpenSearch Observability


* TraceView - Optimization of queries ([#2349] (https://github.com/opensearch-project/dashboards-observability/pull/2349))


* [Integration] Remove maxFilesPerTrigger from all the integrations queries ([#2354] (https://github.com/opensearch-project/dashboards-observability/pull/2354))
* Bump dashboards observability to version 3.0.0.0-alpha1 ([#2364] (https://github.com/opensearch-project/dashboards-observability/pull/2364))
* ServiceMap Query Optimizations ([#2367] (https://github.com/opensearch-project/dashboards-observability/pull/2367))
* Increase dashboards timeout & store logs on failure ([#2371] (https://github.com/opensearch-project/dashboards-observability/pull/2371))
* Clear ADMINS.md. ([#2363] (https://github.com/opensearch-project/dashboards-observability/pull/2363))


### OpenSearch Observability


* Bump version 3.0.0-alpha1-SNAPSHOT ([#1904] (https://github.com/opensearch-project/observability/pull/1904))
* Bump jdk to 21 for maven snapshot build ([#1909] (https://github.com/opensearch-project/observability/pull/1909))


### OpenSearch Learning To Rank Base


* Update for Lucene 10 changes ((#144)[https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/144])


### OpenSearch Performance Analyzer


* Bumps OS to 3.0.0-alpha1 and JDK 21 ([#791](https://github.com/opensearch-project/performance-analyzer/pull/791))


### OpenSearch Query Insights


* Bump version to 3.0.0-alpha1 & upgrade to gradle 8.10.2 ([#247](https://github.com/opensearch-project/query-insights/pull/247))


### OpenSearch Query Insights Dashboards


* Update @babel/helpers ([#139](https://github.com/opensearch-project/query-insights-dashboards/pull/139))
* Delete package-lock.json as it is duplicate with yarn.lock ([#133](https://github.com/opensearch-project/query-insights-dashboards/pull/133))
* Upgrade actions/cache to v4 ([#130](https://github.com/opensearch-project/query-insights-dashboards/pull/130))
* Updated package.json ([#126](https://github.com/opensearch-project/query-insights-dashboards/pull/126))
* Updated-glob-parent-version([#134](https://github.com/opensearch-project/query-insights-dashboards/pull/134))


### OpenSearch Query Workbench


* Update yarn.lock for cross-spawn ([#441] (https://github.com/opensearch-project/dashboards-query-workbench/pull/441))


* Bump dashboards query workbench to version 3.0.0.0-alpha1 ([#444] (https://github.com/opensearch-project/dashboards-query-workbench/pull/444))
* update CIs to install job-scheduler plugin ([#453] (https://github.com/opensearch-project/dashboards-query-workbench/pull/453))


### OpenSearch Reporting


* Bump version 3.0.0-alpha1-SNAPSHOT ([#1073] (https://github.com/opensearch-project/reporting/pull/1073))
* Update gradle version to 8.12.0 for JDK23 support ([#1077] (https://github.com/opensearch-project/reporting/pull/1077))


### OpenSearch Security Analytics


* [Release 3.0] Add alpha1 qualifier. ([#1490](https://github.com/opensearch-project/security-analytics/pull/1490))
* Updated commons jar with CVE fixes. ([#1481](https://github.com/opensearch-project/security-analytics/pull/1481))
* Update gradle 8.10.2 and support jdk23 ([#1492](https://github.com/opensearch-project/security-analytics/pull/1492))
* Fix security-enabled test workflow for 3.0-alpha1. ([#1494](https://github.com/opensearch-project/security-analytics/pull/1494/))


### OpenSearch Security Analytics Dashboards


* [Release 3.0] Add alpha1 qualifier. ([#1218](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1218))
* Fix CVE. ([#1270](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1270))


### OpenSearch Security Dashboards Plugin


* Fix alpha bump ([#2190](https://github.com/opensearch-project/security-dashboards-plugin/pull/2190))
* Bump xlm-crypto and elliptic ([#2196](https://github.com/opensearch-project/security-dashboards-plugin/pull/2196))


### OpenSearch k-NN


* Update package name to fix compilation issue [#2513](https://github.com/opensearch-project/k-NN/pull/2513)


* Update gradle to 8.13 to fix command exec on java 21 [#2571](https://github.com/opensearch-project/k-NN/pull/2571)
* Add fix for nmslib pragma on arm [#2574](https://github.com/opensearch-project/k-NN/pull/2574)
* Removes Array based vector serialization [#2587](https://github.com/opensearch-project/k-NN/pull/2587)
* Enabled indices.breaker.total.use\_real\_memory setting via build.gradle for integTest Cluster to catch heap CB in local ITs and github CI actions [#2395](https://github.com/opensearch-project/k-NN/pull/2395/)
* Fixing Lucene912Codec Issue with BWC for Lucene 10.0.1 upgrade[#2429](https://github.com/opensearch-project/k-NN/pull/2429)
* Enabled idempotency of local builds when using `./gradlew clean` and nest `jni/release` directory under `jni/build` for easier cleanup [#2516](https://github.com/opensearch-project/k-NN/pull/2516)


### OpenSearch SQL


* Build: Centralise dependencies version - Pt1 ([#3294](https://github.com/opensearch-project/sql/pull/3294))
* Remove dependency from async-query-core to datasources ([#2891](https://github.com/opensearch-project/sql/pull/2891))

### Opensearch Security

* Update AuditConfig.DEPRECATED\_KEYS deprecation message to match 4.0 ([#5155](https://github.com/opensearch-project/security/pull/5155))
* Update deprecation message for `_opendistro/_security/kibanainfo` API ([#5156](https://github.com/opensearch-project/security/pull/5156))
* Update DlsFlsFilterLeafReader to reflect Apache Lucene 10 API changes ([#5123](https://github.com/opensearch-project/security/pull/5123))
* Adapt to core changes in `SecureTransportParameters` ([#5122](https://github.com/opensearch-project/security/pull/5122))
* Format SSLConfigConstants.java and fix typos ([#5145](https://github.com/opensearch-project/security/pull/5145))
* Remove typo in `AbstractAuditlogUnitTest` ([#5130](https://github.com/opensearch-project/security/pull/5130))
* Update Andriy Redko's affiliation ([#5133](https://github.com/opensearch-project/security/pull/5133))
* Upgrade common-utils version to `3.0.0.0-alpha1-SNAPSHOT` ([#5137](https://github.com/opensearch-project/security/pull/5137))
* Bump Spring version ([#5173](https://github.com/opensearch-project/security/pull/5173))
* Bump org.checkerframework:checker-qual from 3.49.0 to 3.49.1 ([#5162](https://github.com/opensearch-project/security/pull/5162))
* Bump org.mockito:mockito-core from 5.15.2 to 5.16.0 ([#5161](https://github.com/opensearch-project/security/pull/5161))
* Bump org.apache.camel:camel-xmlsecurity from 3.22.3 to 3.22.4 ([#5163](https://github.com/opensearch-project/security/pull/5163))
* Bump ch.qos.logback:logback-classic from 1.5.16 to 1.5.17 ([#5149](https://github.com/opensearch-project/security/pull/5149))
* Bump org.awaitility:awaitility from 4.2.2 to 4.3.0 ([#5126](https://github.com/opensearch-project/security/pull/5126))
* Bump org.springframework.kafka:spring-kafka-test from 3.3.2 to 3.3.3 ([#5125](https://github.com/opensearch-project/security/pull/5125))
* Bump org.junit.jupiter:junit-jupiter from 5.11.4 to 5.12.0 ([#5127](https://github.com/opensearch-project/security/pull/5127))
* Bump Gradle to 8.13 ([#5148](https://github.com/opensearch-project/security/pull/5148))
* Bump Spring version to fix CVE-2024-38827 ([#5173](https://github.com/opensearch-project/security/pull/5173))


## REFACTORING


### OpenSearch Alerting Dashboards Plugin


* Only use latest active alert for alert summary context ([#1220](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1220))


### OpenSearch Flow Framework Dashboards


* Refactor quick configure components, improve processor error handling ([#604](https://github.com/opensearch-project/dashboards-flow-framework/pull/604))
* Hide search query section when version is less than 2.19 ([#605](https://github.com/opensearch-project/dashboards-flow-framework/pull/605))


### OpenSearch Neural Search


* Encapsulate KNNQueryBuilder creation within NeuralKNNQueryBuilder ([#1183](https://github.com/opensearch-project/neural-search/pull/1183))


### OpenSearch Remote Metadata Sdk


* Update o.o.client imports to o.o.transport.client ([#73](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/73))


### OpenSearch Security Analytics Dashboards


* Temporarily removed visualizations for 3.0-alpha1. ([#1272](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1272))


### OpenSearch k-NN


* Small Refactor Post Lucene 10.0.1 upgrade [#2541](https://github.com/opensearch-project/k-NN/pull/2541)


* Refactor codec to leverage backwards\_codecs [#2546](https://github.com/opensearch-project/k-NN/pull/2546)
* Blocking Index Creation using NMSLIB [#2573](https://github.com/opensearch-project/k-NN/pull/2573)
* Improve Streaming Compatibility Issue for MethodComponetContext and Remove OpenDistro URL [#2575](https://github.com/opensearch-project/k-NN/pull/2575)
* 3.0.0 Breaking Changes For KNN [#2564](https://github.com/opensearch-project/k-NN/pull/2564)
