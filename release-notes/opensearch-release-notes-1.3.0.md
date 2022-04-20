# OpenSearch and Dashboards 1.3.0 Release Notes

## Release Highlights

### OpenSearch Ml Commons
* The new ML Commons plugin empowers users to train and apply machine learning models as a part of the OpenSearch 1.3.0 release.

## Release Details

OpenSearch and OpenSearch Dashboards 1.3.0 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.3.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.3.0.md).

## FEATURES

### OpenSearch Anomaly Detection
* Adding Model Type Validation to Validate API ("non-blocker") ([#384](https://github.com/opensearch-project/anomaly-detection/pull/384))


### OpenSearch Anomaly Detection Dashboards
* Non blocker ([#202](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/202))


### OpenSearch Index Management
* Continuous transforms ([#206](https://github.com/opensearch-project/index-management/pull/206))
* Refactor IndexManagement to support custom actions ([#288](https://github.com/opensearch-project/index-management/pull/288))


### OpenSearch Ml Commons
* Add anomaly localization implementation ([#103](https://github.com/opensearch-project/ml-commons/pull/103))
* Refactor ML task data model; add create ML task index method ([#116](https://github.com/opensearch-project/ml-commons/pull/116))
* Integration step 1 and 2 for anomaly localization ([#113](https://github.com/opensearch-project/ml-commons/pull/113))
* Anomaly localization integration step 3 ([#114](https://github.com/opensearch-project/ml-commons/pull/114))
* Support train ML model in either sync or async way ([#124](https://github.com/opensearch-project/ml-commons/pull/124))
* Anomaly localization integration step 4 and 5 ([#125](https://github.com/opensearch-project/ml-commons/pull/125))
* Add train and predict API ([#126](https://github.com/opensearch-project/ml-commons/pull/126))
* Add ML Model get API ([#117](https://github.com/opensearch-project/ml-commons/pull/117))
* Integrate tribuo anomaly detection based on libSVM ([#96](https://github.com/opensearch-project/ml-commons/pull/96))
* Add ML Delete model API ([#136](https://github.com/opensearch-project/ml-commons/pull/136))
* Add fixed in time rcf ([#138](https://github.com/opensearch-project/ml-commons/pull/138))
* Add ML Model Search API ([#140](https://github.com/opensearch-project/ml-commons/pull/140))
* Add circuit breaker ([#142](https://github.com/opensearch-project/ml-commons/pull/142))
* Add batch RCF for non-time-series data ([#145](https://github.com/opensearch-project/ml-commons/pull/145))
* Add ML Task GET/Delete API ([#146](https://github.com/opensearch-project/ml-commons/pull/146))
* Add Search Task API and Refactor search actions and handlers ([#149](https://github.com/opensearch-project/ml-commons/pull/149))
* Add minimum top contributor candidate queue size ([#151](https://github.com/opensearch-project/ml-commons/pull/151))
* Add more stats: request/failure/model count on algo/action level ([#159](https://github.com/opensearch-project/ml-commons/pull/159))
* Add tasks API in Client ([#200](https://github.com/opensearch-project/ml-commons/pull/200))


### OpenSearch Observability
* Feature latest observability ([#509](https://github.com/opensearch-project/observability/pull/509))
* Live tail - Event analytics  ([#494](https://github.com/opensearch-project/observability/pull/494))
* Add Events Flyout and Correlate Traces with logs ([#493](https://github.com/opensearch-project/observability/pull/493))
* Merge Application Analytics into main ([#454](https://github.com/opensearch-project/observability/pull/454))


### OpenSearch Performance Analyzer
* Add .whitesource configuration file ([#119](https://github.com/opensearch-project/performance-analyzer/pull/119))
* Add support for OPENSEARCH_JAVA_HOME ([#133](https://github.com/opensearch-project/performance-analyzer/pull/133))
* Adding auto backport ([#146](https://github.com/opensearch-project/performance-analyzer/pull/146))


### OpenSearch SQL
* Add parse command to PPL ([#411](https://github.com/opensearch-project/sql/pull/411))
* PPL integration with AD and ml-commons ([#468](https://github.com/opensearch-project/sql/pull/468))


## ENHANCEMENT

### OpenSearch Alerting
* Implemented support for ClusterMetrics monitors. ([#221](https://github.com/opensearch-project/alerting/pull/221))


### OpenSearch Alerting Dashboards Plugin
* Implemented a toast to display successful attempts to acknowledge alerts. Refactored alerts dashboard flyout to refresh its alerts table when alerts are acknowledged. ([#160](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/160))
* Refactored acknowledge alerts button on Alerts by trigger dashboard page to be a modal experience. ([#167](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/167))


### OpenSearch Anomaly Detection
* Check one feature query at a time - Validate API ([#412](https://github.com/opensearch-project/anomaly-detection/pull/412))


### OpenSearch Anomaly Detection Dashboards
* Improve error handling on missing result index errors on detector detail pages ([#158](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/158))


### OpenSearch Cross Cluster Replication
* Enhance Autofollow task to start replication jobs based on settings ([#307](https://github.com/opensearch-project/cross-cluster-replication/pull/321))


### OpenSearch Index Management
* Adds default action retries ([#212](https://github.com/opensearch-project/index-management/pull/212))
* Adds min rollover age as a transition condition ([#215](https://github.com/opensearch-project/index-management/pull/215))
* Adds min primary shard size rollover condition to the ISM rollover action ([#220](https://github.com/opensearch-project/index-management/pull/220))
* Not managing indices when matched certain pattern ([#255](https://github.com/opensearch-project/index-management/pull/255/files))
* Show applied policy in explain API ([#251](https://github.com/opensearch-project/index-management/pull/251))


### OpenSearch Index Management Dashboards Plugin
* Add refresh button to rollup page ([#132](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/132))
* Adds support for creating and displaying the transform continuous mode ([#153](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/153))
* Adds support on UI for min primary shard size rollover condition and min rollover age transition condition ([#159](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/159))


### OpenSearch k-NN
* Add Recall Tests ([#251](https://github.com/opensearch-project/k-NN/pull/251))
* Change serialization for knn vector from single array object to collection of floats ([#253](https://github.com/opensearch-project/k-NN/pull/253))
* Add ExtensiblePlugin to KNNPlugin ([#264](https://github.com/opensearch-project/k-NN/pull/264))
* Add gradle task for running integ tests in remote cluster ([#266](https://github.com/opensearch-project/k-NN/pull/266))
* Change benchmark ingest took metric to total time ([#268](https://github.com/opensearch-project/k-NN/pull/268))
* Make doc and query count configurable in benchmark ([#270](https://github.com/opensearch-project/k-NN/pull/270))


### OpenSearch Ml Commons
* Support float type in data frame ([#129](https://github.com/opensearch-project/ml-commons/pull/129))
* Support short and long type in data frame ([#131](https://github.com/opensearch-project/ml-commons/pull/131))
* Use threadpool in execute task runner ([#156](https://github.com/opensearch-project/ml-commons/pull/156))
* Do not return model and task id in response ([#171](https://github.com/opensearch-project/ml-commons/pull/171))
* More strict check on input parameters by applying non-coerce mode ([#173](https://github.com/opensearch-project/ml-commons/pull/173))
* Move anomaly localization to the last position to avoid BWC issue ([#189](https://github.com/opensearch-project/ml-commons/pull/189))


### OpenSearch Observability
* Disable duplicate visualization and enable edit panel ([#554](https://github.com/opensearch-project/observability/pull/554))
* Allow app creation with one composition ([#557](https://github.com/opensearch-project/observability/pull/557))
* Add ability to choose visualization for availability ([#552](https://github.com/opensearch-project/observability/pull/552))
* Added common visualization parser ([#550](https://github.com/opensearch-project/observability/pull/550))
* Converting datetime to utc from picker ([#551](https://github.com/opensearch-project/observability/pull/551))
* Feature/remove timestamp saving ([#546](https://github.com/opensearch-project/observability/pull/546))
* Feature convert browser time to utc time ([#542](https://github.com/opensearch-project/observability/pull/542))
* Replace viz icon ([#543](https://github.com/opensearch-project/observability/pull/543))
* Add availability metrics to app table ([#539](https://github.com/opensearch-project/observability/pull/539))
* Add autocomplete to panels, add parse command to app analytics ([#529](https://github.com/opensearch-project/observability/pull/529))
* Changes panel requests & date, traces link in events ([#533](https://github.com/opensearch-project/observability/pull/533))
* Include related services node under service filter ([#527](https://github.com/opensearch-project/observability/pull/527))
* Change availability level to have expression ([#525](https://github.com/opensearch-project/observability/pull/525))
* Feature/sort only datatable in flyout ([#522](https://github.com/opensearch-project/observability/pull/522))
* Add service map to services and trace view page ([#518](https://github.com/opensearch-project/observability/pull/518))
* Edit visualization in Application Analytics ([#519](https://github.com/opensearch-project/observability/pull/519))
* Add parse command back in autocompletion ([#517](https://github.com/opensearch-project/observability/pull/517))
* Add autocomplete enhancements ([#507](https://github.com/opensearch-project/observability/pull/507))
* Make base query immutable ([#500](https://github.com/opensearch-project/observability/pull/500))
* Redirect to trace tab, updateMappings once, etc ([#481](https://github.com/opensearch-project/observability/pull/481))
* Finish autocomplete logic for after where ([#480](https://github.com/opensearch-project/observability/pull/480))
* UI changes to Metrics Tab ([#476](https://github.com/opensearch-project/observability/pull/476))
* Add date_nanos to valid time fields ([#426](https://github.com/opensearch-project/observability/pull/426))
* Separate default filters and extra filters ([#474](https://github.com/opensearch-project/observability/pull/474))
* Saving time for individual applications ([#473](https://github.com/opensearch-project/observability/pull/473))
* Support lazy scroll and auto complete for PPL parse command ([#421](https://github.com/opensearch-project/observability/pull/421))
* Add observability visualization to notebooks  ([#351](https://github.com/opensearch-project/observability/pull/351))


### OpenSearch Security
* Adds CI support for Java 8, 11 and 14 ([#1580](https://github.com/opensearch-project/security/pull/1580))
* Updates the test retry-count to give flaky tests more chances to pass ([#1601](https://github.com/opensearch-project/security/pull/1601))
* Adds support for OPENSEARCH_JAVA_HOME ([#1603](https://github.com/opensearch-project/security/pull/1603))
* Adds auto delete workflow for backport branches ([#1604](https://github.com/opensearch-project/security/pull/1604))
* Create the plugin-descriptor programmatically ([#1623](https://github.com/opensearch-project/security/pull/1623))
* Add test to make sure exception causes aren't sent to callers ([#1639](https://github.com/opensearch-project/security/pull/1639))
* Switch gradle to info logging for improved test debugging ([#1646](https://github.com/opensearch-project/security/pull/1646))
* Remove artifact step from CI workflow ([#1645](https://github.com/opensearch-project/security/pull/1645))
* Adds ssl script ([#1530](https://github.com/opensearch-project/security/pull/1530))
* Adds Java-17 to CI matrix ([#1609](https://github.com/opensearch-project/security/pull/1609))
* Reverts ssl script PR ([#1637](https://github.com/opensearch-project/security/pull/1637))
* Remove java17 from 1.3 build matrix ([#1668](https://github.com/opensearch-project/security/pull/1668))


### OpenSearch Security Dashboards Plugin
* Add auto backport functionality to security plugin ([#887](https://github.com/opensearch-project/security-dashboards-plugin/pull/887))
* Adds auto delete workflow for backport branches ([#901](https://github.com/opensearch-project/security-dashboards-plugin/pull/901))
* Configure ML plugin actions ([#912](https://github.com/opensearch-project/security-dashboards-plugin/pull/912))


### OpenSearch SQL
* Support ISO 8601 Format in Date Format. ([#460](https://github.com/opensearch-project/sql/pull/460))
* Add Certificate Validation option ([#449](https://github.com/opensearch-project/sql/pull/449))
* Span expression should always be first in by list if exist ([#437](https://github.com/opensearch-project/sql/pull/437))
* Support multiple indices in PPL and SQL ([#408](https://github.com/opensearch-project/sql/pull/408))
* Support combination of group field and span in stats command ([#417](https://github.com/opensearch-project/sql/pull/417))
* Support In clause in SQL and PPL ([#420](https://github.com/opensearch-project/sql/pull/420))
* Add cast function to PPL ([#433](https://github.com/opensearch-project/sql/pull/433))
* [Enhancement] optimize sort rewrite logic ([#434](https://github.com/opensearch-project/sql/pull/434))


## BUG FIXES

### OpenSearch Alerting
* Fix running Alerting security tests in GitHub Actions. ([#252](https://github.com/opensearch-project/alerting/pull/252))


### OpenSearch Alerting Dashboards Plugin
* Fix error handling when config index is not found ([#173](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/173))
* Update getDestination response  ([#182](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/182))


### OpenSearch Anomaly Detection Dashboards
* Force heatmap y-axis to be category type ([#167](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/167))
* Fix custom expression filter cannot show ([#178](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/178))


### OpenSearch Cross Cluster Replication
* Bugfix: Stregthen validation checks for status API ([#317](https://github.com/opensearch-project/cross-cluster-replication/pull/317))


### OpenSearch Dashboards Reports
* Fix empty or multiple date values in csv ([#293](https://github.com/opensearch-project/dashboards-reports/pull/293))
* Fix reporting uuid parsing ([#300](https://github.com/opensearch-project/dashboards-reports/pull/300))


### OpenSearch Dashboards Visualizations
* Fix UT coverage on codecov ([#40](https://github.com/opensearch-project/dashboards-visualizations/pull/40))


### OpenSearch Index Management
* Successful deletes of an index still adds history document ([#160](https://github.com/opensearch-project/index-management/pull/160))
* Porting missing bugfixes ([#232](https://github.com/opensearch-project/index-management/pull/181))
* ISM Template Migration ([#237](https://github.com/opensearch-project/index-management/pull/237))
* Fixes flaky tests ([#211](https://github.com/opensearch-project/index-management/pull/211))
* Fixes flaky rollup/transform explain IT ([#247](https://github.com/opensearch-project/index-management/pull/247))
* Avoids restricted index warning check in blocked index pattern test ([#263](https://github.com/opensearch-project/index-management/pull/263))
* Porting missing logic ([#240](https://github.com/opensearch-project/index-management/pull/240))
* Fixes flaky continuous transforms test ([#276](https://github.com/opensearch-project/index-management/pull/276))
* Porting additional missing logic ([#275](https://github.com/opensearch-project/index-management/pull/275))
* Fixes test failures with security enabled ([#292](https://github.com/opensearch-project/index-management/pull/292))
* Enforces extension action parsers have custom flag ([#306](https://github.com/opensearch-project/index-management/pull/306))


### OpenSearch Index Management Dashboards Plugin
* Fixes default state not updating when changing state name ([#145](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/145))
* Changes the default policy of the visual editor to be an empty one ([#149](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/149))


### OpenSearch k-NN
* Set default space type to L2 to support bwc ([#267](https://github.com/opensearch-project/k-NN/pull/267))
* [BUG FIX] Add space type default and ef search parameter in warmup ([#276](https://github.com/opensearch-project/k-NN/pull/276))
* [FLAKY TEST] Fix codec test causing CI to fail ([#277](https://github.com/opensearch-project/k-NN/pull/277))
* [BUG FIX] Fix knn index shard to get bwc engine paths ([#309](https://github.com/opensearch-project/k-NN/pull/309))


### OpenSearch Ml Commons
* Use latest version of tribuo to fix modify thread group permission issue ([#112](https://github.com/opensearch-project/ml-commons/pull/112))
* Fix jarhell error from SQL build ([#137](https://github.com/opensearch-project/ml-commons/pull/137))
* Fix EpochMilli parse error in MLTask ([#147](https://github.com/opensearch-project/ml-commons/pull/147))
* Fix permission when accessing ML system indices ([#148](https://github.com/opensearch-project/ml-commons/pull/148))
* Fix system index permission issue in train/predict runner ([#150](https://github.com/opensearch-project/ml-commons/pull/150))
* Cleanup task cache once task done ([#152](https://github.com/opensearch-project/ml-commons/pull/152))
* Fix update task semaphore; don't return task id for sync request ([#153](https://github.com/opensearch-project/ml-commons/pull/153))
* Restore context after accessing system index to check user permission on non-system index ([#154](https://github.com/opensearch-project/ml-commons/pull/154))
* Fix verbose error message thrown by invalid enum ([#167](https://github.com/opensearch-project/ml-commons/pull/167))
* Fix no permission to create model/task index bug;add security IT for train/predict API ([#177](https://github.com/opensearch-project/ml-commons/pull/177))


### OpenSearch Observability
* Fix for datepicker issue ([#571](https://github.com/opensearch-project/observability/pull/571))
* Show saved time range when editing saved visualization ([#570](https://github.com/opensearch-project/observability/pull/570))
* Issue/query click ([#569](https://github.com/opensearch-project/observability/pull/569))
* Fix fields not showing up in panels autocomplete ([#566](https://github.com/opensearch-project/observability/pull/566))
* Pass in prop curSelectedTabId for live tail ([#567](https://github.com/opensearch-project/observability/pull/567))
* Added fix for threshold ([#568](https://github.com/opensearch-project/observability/pull/568))
* Fix interval selector issue, revert interval function changes ([#563](https://github.com/opensearch-project/observability/pull/563))
* Remove bold letter and extra pranthesis ([#559](https://github.com/opensearch-project/observability/pull/559))
* Issue horizontal bar ([#556](https://github.com/opensearch-project/observability/pull/556))
* Final live tail fixes ([#558](https://github.com/opensearch-project/observability/pull/558))
* Fix page flicker for live tail ([#541](https://github.com/opensearch-project/observability/pull/541))
* Fix multiple flyouts issue in explorer ([#538](https://github.com/opensearch-project/observability/pull/538))
* Flyout bugs ([#540](https://github.com/opensearch-project/observability/pull/540))
* Detete request and response changes for event and panels ([#530](https://github.com/opensearch-project/observability/pull/530))
* Issue/darkmode support viz config ([#521](https://github.com/opensearch-project/observability/pull/521))
* Visualizations do not follow set timerange ([#516](https://github.com/opensearch-project/observability/pull/516))
* Fix empty userConfigs stringify ([#513](https://github.com/opensearch-project/observability/pull/513))
* Fix lower margin of autocomplete being cut off ([#512](https://github.com/opensearch-project/observability/pull/512))
* Fix issue of clicking query caused crash ([#515](https://github.com/opensearch-project/observability/pull/515))
* Feature viz saving on missing fields ([#511](https://github.com/opensearch-project/observability/pull/511))
* Fix events flyout bugs and Styling ([#510](https://github.com/opensearch-project/observability/pull/510))
* Bump prismjs from 1.25.0 to 1.27.0 in /dashboards-observability ([#508](https://github.com/opensearch-project/observability/pull/508))
* Revert query pre-processing for parse command ([#497](https://github.com/opensearch-project/observability/pull/497))
* Fix create/edit page bug ([#475](https://github.com/opensearch-project/observability/pull/475))
* Fix queries being filtered out ([#472](https://github.com/opensearch-project/observability/pull/472))
* Guava package update ([#404](https://github.com/opensearch-project/observability/pull/404))
* CVE fix:json-schema, gson \& glob-parent ([#368](https://github.com/opensearch-project/observability/pull/368))


### OpenSearch Performance Analyzer
* Fix and lock link checker at lycheeverse/lychee-action ([#113](https://github.com/opensearch-project/performance-analyzer/pull/113))
* Upgrade plugin to 1.3.0 and log4j to 2.17.1 ([#118](https://github.com/opensearch-project/performance-analyzer/pull/118))
* Don't run opensearch-cli in a child process ([#126](https://github.com/opensearch-project/performance-analyzer/pull/126))
* Modify grpc-netty-shaded to grpc-netty ([#129](https://github.com/opensearch-project/performance-analyzer-rca/pull/129))
* Fixes grpc channel leak issue and vertex buffer issue on non active master ([#130](https://github.com/opensearch-project/performance-analyzer-rca/pull/130))
* Fixes RCA crash on active master ([#132](https://github.com/opensearch-project/performance-analyzer-rca/pull/132))


### OpenSearch Security
* Bumps JJWT version ([#1589](https://github.com/opensearch-project/security/pull/1589))
* Updates backport workflow with custom branch and github app ([#1597](https://github.com/opensearch-project/security/pull/1597))
* Always run checks on PRs ([#1615](https://github.com/opensearch-project/security/pull/1615))
* Adds 'opens' command-line argument for java.io libraries to unblock build ([#1616](https://github.com/opensearch-project/security/pull/1616))
* Adds jacoco report and pass the location to codecov ([#1617](https://github.com/opensearch-project/security/pull/1617))
* Fixes the settings of roles_separator ([#1618](https://github.com/opensearch-project/security/pull/1618))
* Use standard opensearch.version property ([#1622](https://github.com/opensearch-project/security/pull/1622))


### OpenSearch Security Dashboards Plugin
* Updates rule def for @osd/eslint/require-license-header ([#905](https://github.com/opensearch-project/security-dashboards-plugin/pull/905))
* Updates backport workflow with custom branch and github app ([#900](https://github.com/opensearch-project/security-dashboards-plugin/pull/900))


### OpenSearch SQL
* Fix certificate validation for ODBC driver ([#479](https://github.com/opensearch-project/sql/pull/479))
* Update dependency opensearch-ml-client group name ([#477](https://github.com/opensearch-project/sql/pull/477))
* Treating ExpressionEvaluationException as client Error. ([#459](https://github.com/opensearch-project/sql/pull/459))
* Version Bump: H2 1.x -> 2.x ([#444](https://github.com/opensearch-project/sql/pull/444))
* Version Bump: springframework and jackson ([#443](https://github.com/opensearch-project/sql/pull/443))
* Bug Fix, disable html escape when formatting response ([#412](https://github.com/opensearch-project/sql/pull/412))
* Jackson-databind bump to 2.12.6 ([#410](https://github.com/opensearch-project/sql/pull/410))
* Parse none type field as null instead of throw exception ([#406](https://github.com/opensearch-project/sql/pull/406))


## INFRASTRUCTURE

### OpenSearch Alerting Dashboards Plugin
* Remove node version declaration in package.json ([#166](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/166))


### OpenSearch Anomaly Detection
* ADD auto backport functionality to AD ([#368](https://github.com/opensearch-project/anomaly-detection/pull/368))
* Use admin client for system index updates in integ tests ([#372](https://github.com/opensearch-project/anomaly-detection/pull/372))
* Fixing Flaky Integration Tests ([#369](https://github.com/opensearch-project/anomaly-detection/pull/369))
* Adding auto delete workflow for backport branches ([#376](https://github.com/opensearch-project/anomaly-detection/pull/376))
* Using Github App to trigger CI on backport PRs ([#375](https://github.com/opensearch-project/anomaly-detection/pull/375))
* Add JDK 11 to CI test matrix ([#395](https://github.com/opensearch-project/anomaly-detection/pull/395))
* Fixing failing IT for validate API ([#402](https://github.com/opensearch-project/anomaly-detection/pull/402))


### OpenSearch Anomaly Detection Dashboards
* Add remote integ test workflow; clean up old integ test workflow ([#163](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/163))
* Reformat using Prettier CLI and add doc to developer guide ([#168](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/168))
* Remove Beta label from bug issue template ([#169](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/169))
* Add .whitesource and config files to activate whitesource integration ([#165](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/165))
* Using Github App to trigger CI on backport PRs ([#175](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/175))
* Adding auto delete workflow for backport branches ([#176](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/176))
* Remove cypress & all integration tests ([#174](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/174))
* Upgrade follow-redirect dependency ([#179](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/179))
* Add test IDs to components for integ tests ([#183](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/183))


### OpenSearch Asynchronous Search
* Added backwards compatibility tests for async search([#95](https://github.com/opensearch-project/asynchronous-search/pull/95))


### OpenSearch Common Utils
* Updates common-utils version to 1.3 ([#99](https://github.com/opensearch-project/common-utils/pull/99))
* Update build.sh script to include optional platform param. ([#95](https://github.com/opensearch-project/common-utils/pull/95))
* Update copyright notice and add DCO check workflow. ([#94](https://github.com/opensearch-project/common-utils/pull/94))


### OpenSearch Cross Cluster Replication
* [CI] Default CI Java Version to Java 11, run tests on 8, 11 and 17 ([#329](https://github.com/opensearch-project/cross-cluster-replication/pull/329))


### OpenSearch Dashboards Reports
* Remove jcenter repo from gradle build ([#278](https://github.com/opensearch-project/dashboards-reports/pull/278))
* Ws package update ([#283](https://github.com/opensearch-project/dashboards-reports/pull/283))
* Guava package update ([#282](https://github.com/opensearch-project/dashboards-reports/pull/282))
* Add auto-backport functionality for reporting ([#286](https://github.com/opensearch-project/dashboards-reports/pull/286))
* Add java 8 support in compile and test ([#304](https://github.com/opensearch-project/dashboards-reports/pull/304))
* Remove incorrect tag form issue template ([#294](https://github.com/opensearch-project/dashboards-reports/pull/294))
* Replace Centos links to fix link checker CI ([#297](https://github.com/opensearch-project/dashboards-reports/pull/297))


### OpenSearch Dashboards Visualizations
* Add Auto Backporting ([#48](https://github.com/opensearch-project/dashboards-visualizations/pull/48))
* Force cypress to use PDT time ([#41](https://github.com/opensearch-project/dashboards-visualizations/pull/41))


### OpenSearch Index Management
* Add support for codeowners to repo ([#195](https://github.com/opensearch-project/index-management/pull/195))
* Adds test and build workflow for mac and windows ([#210](https://github.com/opensearch-project/index-management/pull/210))
* Adding debug log to log the user object for all user callable transport actions ([#166](https://github.com/opensearch-project/index-management/pull/166))
* Added ISM policy backwards compatibility test ([#181](https://github.com/opensearch-project/index-management/pull/181))
* Add backport and auto delete workflow ([#283](https://github.com/opensearch-project/index-management/pull/283))
* Updates integTest gradle scripts to run via remote cluster independently ([#291](https://github.com/opensearch-project/index-management/pull/291))


### OpenSearch Index Management Dashboards Plugin
* Adds developer certificate of origin check workflow ([#129](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/129))
* Fixes retry failed managed index cypress test ([#125](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/125))


### OpenSearch Job Scheduler
* Run CI on JDK 8, 11, and 14. ([130](https://github.com/opensearch-project/job-scheduler/pull/130))
* Auto increment version after release. ([115](https://github.com/opensearch-project/job-scheduler/pull/115))
* Update build.gradle to include job-scheduler jar in staging maven publications ([117](https://github.com/opensearch-project/job-scheduler/pull/117))
* Using Github App token to trigger CI for version increment PRs ([126](https://github.com/opensearch-project/job-scheduler/pull/126))


### OpenSearch k-NN
* Remove jcenter repo from build related gradle files ([#261](https://github.com/opensearch-project/k-NN/pull/261))
* Add write permissions to backport action ([#262](https://github.com/opensearch-project/k-NN/pull/262))
* Add JDK 11 to CI and docs ([#271](https://github.com/opensearch-project/k-NN/pull/271))
* [Benchmark] Remove ingest results collection ([#272](https://github.com/opensearch-project/k-NN/pull/272))
* Update backport workflow to include custom branch name ([#273](https://github.com/opensearch-project/k-NN/pull/273))
* Add CI to run every night ([#278](https://github.com/opensearch-project/k-NN/pull/278))
* Use Github App to trigger CI on backport PRs ([#288](https://github.com/opensearch-project/k-NN/pull/288))
* Add auto delete workflow for backport branches ([#289](https://github.com/opensearch-project/k-NN/pull/289))
* Updates Guava versions to address CVE ([#292](https://github.com/opensearch-project/k-NN/pull/292))
* [CODE STYLE] Switch checkstyle to spotless ([#297](https://github.com/opensearch-project/k-NN/pull/297))
* Switch main to 2.0.0-SNAPSHOT, update to Gradle 7.3.3 ([#301](https://github.com/opensearch-project/k-NN/pull/301))
* Run CI on JDK 8 ([#302](https://github.com/opensearch-project/k-NN/pull/302))
* Update numpy version to 1.22.1 ([#305](https://github.com/opensearch-project/k-NN/pull/305))


### OpenSearch Ml Commons
* Add git ignore file ([#92](https://github.com/opensearch-project/ml-commons/pull/92))
* Change common utils to 1.2 snapshot;add more test ([#94](https://github.com/opensearch-project/ml-commons/pull/94))
* Remove jcenter dependency ([#121](https://github.com/opensearch-project/ml-commons/pull/121))
* Add integration test for train and predict API ([#157](https://github.com/opensearch-project/ml-commons/pull/157))
* Fix build/CI and add backport workflow ([#161](https://github.com/opensearch-project/ml-commons/pull/161))
* Publish ml client to maven ([#165](https://github.com/opensearch-project/ml-commons/pull/165))
* Add integ tests for model APIs ([#166](https://github.com/opensearch-project/ml-commons/pull/166))
* Add security IT ([#168](https://github.com/opensearch-project/ml-commons/pull/168))
* Fix maven group ([#170](https://github.com/opensearch-project/ml-commons/pull/170))
* Add more UT for ml-algorithms ([#182](https://github.com/opensearch-project/ml-commons/pull/182))
* Add java 8 to CI workflow ([#194](https://github.com/opensearch-project/ml-commons/pull/194))
* Add more UT and IT for rest actions ([#192](https://github.com/opensearch-project/ml-commons/pull/192))
* Add more UT to client module ([#203](https://github.com/opensearch-project/ml-commons/pull/203))
* Add more UT for task manager/runner ([#206](https://github.com/opensearch-project/ml-commons/pull/206))
* Create config and workflow files for release note ([#209](https://github.com/opensearch-project/ml-commons/pull/209))
* Use 1.3.0 docker to run CI ([#212](https://github.com/opensearch-project/ml-commons/pull/212))


### OpenSearch Observability
* Change to support java 8 in compile and runtime ([#575](https://github.com/opensearch-project/observability/pull/575))
* Update cypress test ([#564](https://github.com/opensearch-project/observability/pull/564))
* Fixed flaky panel test ([#565](https://github.com/opensearch-project/observability/pull/565))
* Feature flyout tests ([#553](https://github.com/opensearch-project/observability/pull/553))
* Add cypress tests for application analytics ([#544](https://github.com/opensearch-project/observability/pull/544))
* Update panels cypress ([#545](https://github.com/opensearch-project/observability/pull/545))
* Update cypress for trace analytics traces view ([#536](https://github.com/opensearch-project/observability/pull/536))
* Cypress fix for panels and events ([#531](https://github.com/opensearch-project/observability/pull/531))
* Updated panels flaky jest tests ([#505](https://github.com/opensearch-project/observability/pull/505))
* Change Default CI java version to 11 ([#504](https://github.com/opensearch-project/observability/pull/504))
* Update backport and add auto-delete workflows ([#496](https://github.com/opensearch-project/observability/pull/496))
* Add auto backporting functionality ([#491](https://github.com/opensearch-project/observability/pull/491))
* [main] jcenter removed from gradle.build ([#374](https://github.com/opensearch-project/observability/pull/374))
* Configure WhiteSource for GitHub.com ([#365](https://github.com/opensearch-project/observability/pull/365))


### OpenSearch SQL
* Disable flaky test in JdbcTestIT. ([#475](https://github.com/opensearch-project/sql/pull/475))


## DOCUMENTATION

### OpenSearch Alerting
* Added 1.3 release notes. ([#336](https://github.com/opensearch-project/alerting/pull/336))
* Updated DEVELOPER_GUIDE.md to reference changes to the supported JDKs. ([#338](https://github.com/opensearch-project/alerting/pull/338))


### OpenSearch Anomaly Detection Dashboards
* Reformat using Prettier CLI and add doc to developer guide ([#168](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/168))


### OpenSearch Common Utils
* Update copyright headers ([#117](https://github.com/opensearch-project/common-utils/pull/117))
* Add release notes for version 1.3.0.0 ([#132](https://github.com/opensearch-project/common-utils/pull/132))


### OpenSearch Index Management
* Add roadmap badge in README ([#295](https://github.com/opensearch-project/index-management/pull/295))


### OpenSearch Index Management Dashboards Plugin
* Add backport documentation link ([#161](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/161))


### OpenSearch Job Scheduler
* Add release notes for 1.3.0.0 ([#143](https://github.com/opensearch-project/job-scheduler/pull/143))


### OpenSearch Ml Commons
* Add support for codeowners to repo ([#91](https://github.com/opensearch-project/ml-commons/pull/91))
* Add how to develop new function doc to readme ([#95](https://github.com/opensearch-project/ml-commons/pull/95))
* Update license header ([#134](https://github.com/opensearch-project/ml-commons/pull/134))


### OpenSearch Observability
* Sync PPL commands doc with main repo ([#549](https://github.com/opensearch-project/observability/pull/549))
* Fixed documentation links ([#534](https://github.com/opensearch-project/observability/pull/534))
* Add parse command docs ([#535](https://github.com/opensearch-project/observability/pull/535))
* Updating readme and badges ([#352](https://github.com/opensearch-project/observability/pull/352))


### OpenSearch Performance Analyzer
* Modify license headers ([#153](https://github.com/opensearch-project/performance-analyzer-rca/pull/153))


### OpenSearch Security Dashboards Plugin
* Improves developer guide ([#889](https://github.com/opensearch-project/security-dashboards-plugin/pull/889))
* Adds back removed portion of developer guide ([#893](https://github.com/opensearch-project/security-dashboards-plugin/pull/893))
* Updates maintainers list ([#902](https://github.com/opensearch-project/security-dashboards-plugin/pull/902))


### OpenSearch SQL
* Add parse docs to PPL commands index ([#486](https://github.com/opensearch-project/sql/pull/486))
* Add limitation section in PPL docs ([#456](https://github.com/opensearch-project/sql/pull/456))
* Add how to setup aws credentials for ODBC Tableau ([#394](https://github.com/opensearch-project/sql/pull/394))


## MAINTENANCE

### OpenSearch Alerting
* Bumps to version 1.3. ([#248](https://github.com/opensearch-project/alerting/pull/248))
* Update GitHub Actions to run on all branches. ([#256](https://github.com/opensearch-project/alerting/pull/256))
* Added support for JDK 8 and 14. ([#335](https://github.com/opensearch-project/alerting/pull/335))


### OpenSearch Alerting Dashboards Plugin
* Bumping version to 1.3. ([#159](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/159))
* Adding CODEOWNERS file ([#150](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/150))
* Configure WhiteSource for GitHub.com ([#153](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/153))
* Adding basic unit tests ([#151](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/151))
* Updated copyright notices and headers. ([#168](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/168))
* Adding a few more basic unit tests ([#180](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/180))
* Add backport workflow ([#176](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/176))


### OpenSearch Anomaly Detection Dashboards
* Bump plugin to 1.3.0.0 ([#160](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/160))


### OpenSearch Asynchronous Search
* Removed jcenter([#94](https://github.com/opensearch-project/asynchronous-search/pull/94))


### OpenSearch Dashboards Visualizations
* Bump gantt chart for 1.3 release ([#51](https://github.com/opensearch-project/dashboards-visualizations/pull/51))


### OpenSearch Index Management
* Updating license headers ([#196](https://github.com/opensearch-project/index-management/pull/196))
* Configure WhiteSource for GitHub.com ([#244](https://github.com/opensearch-project/index-management/pull/244))
* Upgrades detekt version to 1.17.1 ([#252](https://github.com/opensearch-project/index-management/pull/252))
* Changes integ test java version from 14 to 11 ([#284](https://github.com/opensearch-project/index-management/pull/284))


### OpenSearch Index Management Dashboards Plugin
* Add support for codeowners to repo ([#131](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/131))
* Fixes copyright header ([#150](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/150))
* Updating license headers ([#130](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/130))
* Create backport workflow  ([#148](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/148))


### OpenSearch Job Scheduler
* Bump version to 1.3 ([#106](https://github.com/opensearch-project/job-scheduler/pull/106))
* Bumps cron-utils version ([111](https://github.com/opensearch-project/job-scheduler/pull/111))
* Update copyright notices ([87](https://github.com/opensearch-project/job-scheduler/pull/87))
* Add support for codeowners to repo ([100](https://github.com/opensearch-project/job-scheduler/pull/100))
* Fixes copyright header ([127](https://github.com/opensearch-project/job-scheduler/pull/127))


### OpenSearch Ml Commons
* Bump version to 1.2 ([#90](https://github.com/opensearch-project/ml-commons/pull/90))
* Bump to 1.2.3 ([#110](https://github.com/opensearch-project/ml-commons/pull/110))
* Bump to 1.3.0 ([#115](https://github.com/opensearch-project/ml-commons/pull/115))


### OpenSearch Observability
* Bump main to 1.3 ([#361](https://github.com/opensearch-project/observability/pull/361))


### OpenSearch Performance Analyzer
* Upgrade docker to 1.3 ([#114](https://github.com/opensearch-project/performance-analyzer-rca/pull/114))
* Upgrade plugin to 1.3.0 and log4j to 2.17.1 ([#118](https://github.com/opensearch-project/performance-analyzer/pull/118))
* Removing deprecated InitialBootClassLoaderMetaspaceSize JVM command line flag ([#124](https://github.com/opensearch-project/performance-analyzer/pull/124))
* Upgrade guava, protobuf version ([#127](https://github.com/opensearch-project/performance-analyzer/pull/127))
* Update jacksonVersion to 2.12.6 ([#129](https://github.com/opensearch-project/performance-analyzer/pull/129))
* Upgrade netty and bouncycastle versions ([#130](https://github.com/opensearch-project/performance-analyzer/pull/130))
* Remove jcenter ([#136](https://github.com/opensearch-project/performance-analyzer/pull/136))
* Update grpc licenses ([#139](https://github.com/opensearch-project/performance-analyzer/pull/139))


### OpenSearch Security
* Updates bug template ([#1582](https://github.com/opensearch-project/security/pull/1582))
* Updates jackson-databind library version ([#1584](https://github.com/opensearch-project/security/pull/1584))
* Upgrades Kafka version ([#1598](https://github.com/opensearch-project/security/pull/1598))
* Upgrades Guava version ([#1594](https://github.com/opensearch-project/security/pull/1594))
* Update maintainers list ([#1607](https://github.com/opensearch-project/security/pull/1607))
* Exclude velocity 1.7 from OpenSAML dependency ([#1606](https://github.com/opensearch-project/security/pull/1606))
* Migrate build system to gradle ([#1592](https://github.com/opensearch-project/security/pull/1592))
* Updates documentation for practices for maintainers ([#1611](https://github.com/opensearch-project/security/pull/1611))
* Remove jcenter repository ([#1625](https://github.com/opensearch-project/security/pull/1625))
* Remove '-SNAPSHOT' from opensearch.version in plugin descriptor ([#1634](https://github.com/opensearch-project/security/pull/1634))
* Add git ignore for VScode IDE settings ([#1629](https://github.com/opensearch-project/security/pull/1629))
* Remove netty-tcnative dependency to unblock security plugin build on ARM64 ([#1649](https://github.com/opensearch-project/security/pull/1649))
* Add plugin-descriptor.properties to .gitignore ([#1651](https://github.com/opensearch-project/security/pull/1651))
* Removes Github DCO action as it is replaced by Github app ([1657](https://github.com/opensearch-project/security/pull/1657))
* Configure ML reserved roles and system indices ([#1662](https://github.com/opensearch-project/security/pull/1662))
* Release Notes for 1.3.0.0 ([#1671](https://github.com/opensearch-project/security/pull/1671))


### OpenSearch Security Dashboards Plugin
* Bumps version to 1.3.0.0 ([#884](https://github.com/opensearch-project/security-dashboards-plugin/pull/884))
* Adds support for codeowners to repo ([#883](https://github.com/opensearch-project/security-dashboards-plugin/pull/883))
* Adds .whitesource and configs file to activate whitesource integration ([#885](https://github.com/opensearch-project/security-dashboards-plugin/pull/885))
* Uses 1.x branch of Dashboards for unit tests ([#890](https://github.com/opensearch-project/security-dashboards-plugin/pull/890))
* Makes PR template easier to fill in ([#888](https://github.com/opensearch-project/security-dashboards-plugin/pull/888))
* Adds release notes for 1.3.0.0 ([#918](https://github.com/opensearch-project/security-dashboards-plugin/pull/918))
* Updates release notes for 1.3.0.0 ([#920](https://github.com/opensearch-project/security-dashboards-plugin/pull/920))


### OpenSearch SQL
* Add JDK 8 to CI Matrix  ([#483](https://github.com/opensearch-project/sql/pull/483))
* Add CI Matrix for JDK 11 and 14 ([#451](https://github.com/opensearch-project/sql/pull/451))
* Update backport and add auto-delete workflows ([#446](https://github.com/opensearch-project/sql/pull/446))
* Add auto backport functionality for SQL ([#445](https://github.com/opensearch-project/sql/pull/445))
* Version bump to 1.3 ([#419](https://github.com/opensearch-project/sql/pull/419))
* Revert to windows 2019 for odbc CI ([#413](https://github.com/opensearch-project/sql/pull/413))


## REFACTORING

### OpenSearch k-NN
* Refactor benchmark dataset format and add big ann benchmark format ([#265](https://github.com/opensearch-project/k-NN/pull/265))


### OpenSearch Ml Commons
* Merge develop branch into main branch ([#87](https://github.com/opensearch-project/ml-commons/pull/87))
* Refactor API input/output/URL; add execute API for non-model based algorithm ([#93](https://github.com/opensearch-project/ml-commons/pull/93))
* Cleanup code and refactor ([#106](https://github.com/opensearch-project/ml-commons/pull/106))
* Support registering ML objects; refactor ML engine interface ([#108](https://github.com/opensearch-project/ml-commons/pull/108))
* Refactor persisting ML model ([#109](https://github.com/opensearch-project/ml-commons/pull/109))
* Refactor transport APIs;fix class cast exception ([#127](https://github.com/opensearch-project/ml-commons/pull/127))
* Add ML custom exceptions ([#133](https://github.com/opensearch-project/ml-commons/pull/133))
* Rename tribuo AD algorithm name ([#144](https://github.com/opensearch-project/ml-commons/pull/144))
