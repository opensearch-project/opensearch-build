# OpenSearch and Dashboards 1.2.0 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 1.2.0 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-1.2.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-1.2.0.md).

## BREAKING CHANGES

### OpenSearch Trace Analytics
* Use observability specific permissions instead of notebooks ([#177](https://github.com/opensearch-project/trace-analytics/pull/177))


## FEATURES

### OpenSearch Alerting Dashboards Plugin
* Support creating monitor for anomaly detector with custom result index ([#143](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/143))


### OpenSearch Anomaly Detection
* Add multi-category top anomaly results API ([#261](https://github.com/opensearch-project/anomaly-detection/pull/261))
* Validation API - "Blocker" level validation ([#231](https://github.com/opensearch-project/anomaly-detection/pull/231))
* Support storing anomaly result to custom index ([#276](https://github.com/opensearch-project/anomaly-detection/pull/276))
* Support only searching results in custom result index ([#292](https://github.com/opensearch-project/anomaly-detection/pull/292))


### OpenSearch Anomaly Detection Dashboards
* Support storing detector result to custom result index ([#110](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/110))
* Support multi-category filtering of results ([#107](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/107))
* Integrating Validation API On Detector Creation Process ([#106](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/106))


### OpenSearch Job Scheduler
* Adds a delay parameter to the job scheduler ([#61](https://github.com/opensearch-project/job-scheduler/pull/61))


### OpenSearch k-NN
* Add support for faiss library to plugin ([#149](https://github.com/opensearch-project/k-NN/pull/149))


### OpenSearch Performance Analyzer
* AdmissionControl Split RCA ([#69](https://github.com/opensearch-project/performance-analyzer-rca/pull/69))


### OpenSearch SQL
* Add new protocol for visualization response format ([#251](https://github.com/opensearch-project/sql/pull/251))


### OpenSearch Trace Analytics
* Added ppl query filter, added router placeholder for panels ([#108](https://github.com/opensearch-project/trace-analytics/pull/108))
* Added Algolia Autocomplete Bar ([#110](https://github.com/opensearch-project/trace-analytics/pull/110))
* Merge notebooks frontend to observability ([#109](https://github.com/opensearch-project/trace-analytics/pull/109))
* Event Analytics  - Add index picker to explorer page ([#125](https://github.com/opensearch-project/trace-analytics/pull/125))
* Feature/operational panels backend ([#130](https://github.com/opensearch-project/trace-analytics/pull/130))
* Feature/p1 release ([#133](https://github.com/opensearch-project/trace-analytics/pull/133))
* Feature/operational panel UI ([#132](https://github.com/opensearch-project/trace-analytics/pull/132))
* Feature timestamp ([#152](https://github.com/opensearch-project/trace-analytics/pull/152))
* Feature toasts errors handling ([#155](https://github.com/opensearch-project/trace-analytics/pull/155))
* Feature query bar ([#166](https://github.com/opensearch-project/trace-analytics/pull/166))
* Feature bug fixes ([#168](https://github.com/opensearch-project/trace-analytics/pull/168))
* Home table ([#169](https://github.com/opensearch-project/trace-analytics/pull/169))
* Feature vis fix override button ([#172](https://github.com/opensearch-project/trace-analytics/pull/172))
* Visualizations theming ([#171](https://github.com/opensearch-project/trace-analytics/pull/171))
* Added find auto interval ([#167](https://github.com/opensearch-project/trace-analytics/pull/167))
* Feature available fields timestamp ([#179](https://github.com/opensearch-project/trace-analytics/pull/179))
* Added aggregate functions to autocomplete ([#185](https://github.com/opensearch-project/trace-analytics/pull/185))
* Feature event analytics imporovements and fixes ([#199](https://github.com/opensearch-project/trace-analytics/pull/199))
* Added support for sample panels ([#200](https://github.com/opensearch-project/trace-analytics/pull/200))
* Feature couple of features and fixes ([#202](https://github.com/opensearch-project/trace-analytics/pull/202))
* Add match command to AutoComplete ([#203](https://github.com/opensearch-project/trace-analytics/pull/203))
* Add error handler when fetching ppl in event explorer ([#204](https://github.com/opensearch-project/trace-analytics/pull/204))
* Support dark mode for notebooks and other style improvements ([#206](https://github.com/opensearch-project/trace-analytics/pull/206))
* Add toggle dark mode in observability side bar ([#209](https://github.com/opensearch-project/trace-analytics/pull/209))
* Panel bug fixes4 and PPL Reference Manual ([#211](https://github.com/opensearch-project/trace-analytics/pull/211))
* Added Samples, help text, standardized tables ([#217](https://github.com/opensearch-project/trace-analytics/pull/217))
* Autocomplete for data values ([#245](https://github.com/opensearch-project/trace-analytics/pull/245))


## ENHANCEMENTS

### OpenSearch Alerting
* Admin Users must be able to access all monitors #139 ([#220](https://github.com/opensearch-project/alerting/pull/220))
* Add valid search filters. ([#194](https://github.com/opensearch-project/alerting/pull/194))


### OpenSearch Anomaly Detection
* Improve HCAD cold start ([#272](https://github.com/opensearch-project/anomaly-detection/pull/272))
* Support custom result indices in multi-category filtering API ([#281](https://github.com/opensearch-project/anomaly-detection/pull/281))
* Add extra fields to anomaly result index ([#268](https://github.com/opensearch-project/anomaly-detection/pull/268))
* Skipping checking create index permission for Validate API ([#285](https://github.com/opensearch-project/anomaly-detection/pull/285))


### OpenSearch Anomaly Detection Dashboards
* Remove old copyright ([#118](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/118))
* Search monitors using custom result index ([#125](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/125))
* Search only custom result index on detector detail page ([#126](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/126))


### OpenSearch Cross Cluster Replication
* Added support for start replication block ([#250](https://github.com/opensearch-project/cross-cluster-replication/pull/250))
* Handled case for _start replication with leader cluster at higher version than the follower cluster ([#247](https://github.com/opensearch-project/cross-cluster-replication/pull/247))
* Handled stop replication when remote cluster is removed ([#241](https://github.com/opensearch-project/cross-cluster-replication/pull/241))
* Filtered out replication exceptions from retrying ([#238](https://github.com/opensearch-project/cross-cluster-replication/pull/238))
* Using time out in cluster state observer as we are reusing the observer ([#215](https://github.com/opensearch-project/cross-cluster-replication/pull/215))
* Renewing retention lease with global-ckp + 1 , as we want operations from that seq number ([#206](https://github.com/opensearch-project/cross-cluster-replication/pull/206))
* Derive security context information when security plugin fails to populate user info ([#204](https://github.com/opensearch-project/cross-cluster-replication/pull/204))
* Provide a custom TranslogDeletionPolicy for translog pruning based on retention leases ([#209](https://github.com/opensearch-project/cross-cluster-replication/pull/209))


### OpenSearch Dashboards Reports
* Add metrics for notifications ([#173](https://github.com/opensearch-project/dashboards-reports/pull/173))
* Add logic to build report detail page link and send as part of message for non-email channels ([#182](https://github.com/opensearch-project/dashboards-reports/pull/182))
* Forward all cookies while using headless Chromium ([#194](https://github.com/opensearch-project/dashboards-reports/pull/194))
* Catch Notifications Errors on Details Pages ([#197](https://github.com/opensearch-project/dashboards-reports/pull/197))
* Remove notifications integration from Details pages ([#210](https://github.com/opensearch-project/dashboards-reports/pull/210))
* Refactor logic for creating DSL from saved object using `buildOpensearchQuery()` ([#213](https://github.com/opensearch-project/dashboards-reports/pull/213))
* Use advanced settings for csv separator and visual report timezone ([#209](https://github.com/opensearch-project/dashboards-reports/pull/209))
* Build email message from template with reports links ([#184](https://github.com/opensearch-project/dashboards-reports/pull/184))
* Use advanced settings for date format in csv reports ([#186](https://github.com/opensearch-project/dashboards-reports/pull/186))
* Remove Notifications from Create/Edit ([#212](https://github.com/opensearch-project/dashboards-reports/pull/212))
* Remove calling notifications in reports scheduler ([#211](https://github.com/opensearch-project/dashboards-reports/pull/211))
* Taking RBAC settings from Alerting plugin default to false ([#165](https://github.com/opensearch-project/dashboards-reports/pull/165))
* Support range filters for csv reports ([#185](https://github.com/opensearch-project/dashboards-reports/pull/185))
* Integrate notifications backend ([#129](https://github.com/opensearch-project/dashboards-reports/pull/129))


### OpenSearch Index Management
* Making snapshot name to scripted input in template ([#77](https://github.com/opensearch-project/index-management/pull/77))
* Adds setting to search all rollup jobs on a target index ([#165](https://github.com/opensearch-project/index-management/pull/165))
* Adds cluster setting to configure index state management jitter ([#153](https://github.com/opensearch-project/index-management/pull/153))
* Allows out of band rollovers on an index without causing ISM to fail ([#180](https://github.com/opensearch-project/index-management/pull/180))


### OpenSearch k-NN
* Include Model Index status as part of Stats API ([#179](https://github.com/opensearch-project/k-NN/pull/179))
* Split jnis into 2 libs and add common lib ([#181](https://github.com/opensearch-project/k-NN/pull/181))
* Generalize error message set in model metadata ([#184](https://github.com/opensearch-project/k-NN/pull/184))
* Delete local references when looping over map ([#185](https://github.com/opensearch-project/k-NN/pull/185))
* Add caching of java classes/methods ([#186](https://github.com/opensearch-project/k-NN/pull/186))
* Add more helpful validation messages ([#183](https://github.com/opensearch-project/k-NN/pull/183))
* Include index model degraded status as stats for given node ([#188](https://github.com/opensearch-project/k-NN/pull/188))
* Add training stats and library initialized stats ([#191](https://github.com/opensearch-project/k-NN/pull/191))


### OpenSearch Performance Analyzer
* Update commons-io version ([#73](https://github.com/opensearch-project/performance-analyzer-rca/pull/73))
* Adds Thread_Waited_Time and Thread_Waited_Event metrics ([#70](https://github.com/opensearch-project/performance-analyzer-rca/pull/70))


### OpenSearch Security
* Add observability permissions and index ([#1484](https://github.com/opensearch-project/security/pull/1484))
* Add AD validate, multi-category results API permissions to AD read access ([#1480](https://github.com/opensearch-project/security/pull/1480))


### OpenSearch Security Dashboards Plugin
* Add AD validate, multi-category results API cluster permissions ([#849](https://github.com/opensearch-project/security-dashboards-plugin/pull/849))
* Add observability cluster permissions ([#851](https://github.com/opensearch-project/security-dashboards-plugin/pull/851))


### OpenSearch SQL
* Add conversion support for datetime as per https://github.com/kylepbi… ([#267](https://github.com/opensearch-project/sql/pull/267))
* Optimized type converting in DSL filters ([#272](https://github.com/opensearch-project/sql/pull/272))


### OpenSearch Trace Analytics
* Adding plugin backend adaptor ([#126](https://github.com/opensearch-project/trace-analytics/pull/126))
* Update notebooks to use observability backend ([#129](https://github.com/opensearch-project/trace-analytics/pull/129))
* Add minimal plugin for backend observability ([#143](https://github.com/opensearch-project/trace-analytics/pull/143))
* Add models for objects and requests ([#144](https://github.com/opensearch-project/trace-analytics/pull/144))
* Add CRUD actions and index operations for observability objects ([#145](https://github.com/opensearch-project/trace-analytics/pull/145))
* Panels' visualization design change ([#149](https://github.com/opensearch-project/trace-analytics/pull/149))
* Operational Panels UI changes ([#153](https://github.com/opensearch-project/trace-analytics/pull/153))
* Changed to support query without 'search' prefix ([#158](https://github.com/opensearch-project/trace-analytics/pull/158))
* Changes for adopting new sql artifact ([#165](https://github.com/opensearch-project/trace-analytics/pull/165))
* Improve reindex handling for .opensearch-notebooks ([#163](https://github.com/opensearch-project/trace-analytics/pull/163))
* Inherited datepicker format from settings ([#164](https://github.com/opensearch-project/trace-analytics/pull/164))
* Added refresh datepicker button ([#182](https://github.com/opensearch-project/trace-analytics/pull/182))
* Field suggestions update to match changed index in query ([#176](https://github.com/opensearch-project/trace-analytics/pull/176))
* Adding colors version2 ([#181](https://github.com/opensearch-project/trace-analytics/pull/181))
* Home table update ([#174](https://github.com/opensearch-project/trace-analytics/pull/174))
* Icon that redirects to PPL Documentation next to Search Bar ([#183](https://github.com/opensearch-project/trace-analytics/pull/183))
* Suggestions are shown in dark mode if settings change ([#187](https://github.com/opensearch-project/trace-analytics/pull/187))
* Case insensitive Autocomplete ([#207](https://github.com/opensearch-project/trace-analytics/pull/207))
* Adjust wording and margin for dark toggle button ([#210](https://github.com/opensearch-project/trace-analytics/pull/210))
* Space after field for more balanced looking query ([#213](https://github.com/opensearch-project/trace-analytics/pull/213))
* Add border around suggestions ([#214](https://github.com/opensearch-project/trace-analytics/pull/214))
* Suggestions width match search bar ([#220](https://github.com/opensearch-project/trace-analytics/pull/220))
* search bar related changes ([#222](https://github.com/opensearch-project/trace-analytics/pull/222))
* Add some space between last paragraph and action button ([#225](https://github.com/opensearch-project/trace-analytics/pull/225))
* Add event analytics permission toast ([#226](https://github.com/opensearch-project/trace-analytics/pull/226))
* Homepage moved to event analytics ([#227](https://github.com/opensearch-project/trace-analytics/pull/227))
* Source as the only first command ([#235](https://github.com/opensearch-project/trace-analytics/pull/235))
* Run query with shift enter ([#239](https://github.com/opensearch-project/trace-analytics/pull/239))
* Add correct erroring in Event Analytics ([#248](https://github.com/opensearch-project/trace-analytics/pull/248))
* Changed error message ([#257](https://github.com/opensearch-project/trace-analytics/pull/257))
* Feature ppl link ([#258](https://github.com/opensearch-project/trace-analytics/pull/258))


## BUG FIXES

### OpenSearch Alerting
* Fixed a bug that was preventing the AcknowledgeAlerts API from acknowledging more than 10 alerts at once. ([#205](https://github.com/opensearch-project/alerting/pull/205))
* Remove user from the responses ([#201](https://github.com/opensearch-project/alerting/pull/201))


### OpenSearch Alerting Dashboards Plugin
* Fixes flaky test and removes local publishing of plugin dependencies ([#135](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/135))
* Update copyright notice ([#140](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/140))


### OpenSearch Anomaly Detection
* Fix flaky REST IT test ([#259](https://github.com/opensearch-project/anomaly-detection/pull/259))
* Fixed a bug when door keepers unnecessarily reset their states ([#262](https://github.com/opensearch-project/anomaly-detection/pull/262))
* Fix task cache expiration bug ([#269](https://github.com/opensearch-project/anomaly-detection/pull/269))
* Fixed unit test by changing name of method to most up to date ([#287](https://github.com/opensearch-project/anomaly-detection/pull/287))
* Fix Instant parsing bug in multi category filtering API ([#289](https://github.com/opensearch-project/anomaly-detection/pull/289))
* Wait for some time to get semaphore when set HC detector task as done ([#300](https://github.com/opensearch-project/anomaly-detection/pull/300))
* Added switch case for general settings issues ([#305](https://github.com/opensearch-project/anomaly-detection/pull/305))


### OpenSearch Anomaly Detection Dashboards
* Fix bug of detector task calls failing if no state index ([#120](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/120))
* Fix chart range bug of non-HC anomaly and feature charts ([#122](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/122))
* Support create monitor with custom result index ([#123](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/123))
* Fix bug of HC historical results not auto-refreshing ([#131](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/131))
* Fix bug of missing annotations on feature charts ([#136](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/136))

### OpenSearch Asynchronous Search
* Add checkstyle plugin reference ([#60](https://github.com/opensearch-project/asynchronous-search/pull/60))
* Correct copyright notices to reflect Copyright OpenSearch Contributors ([#61](https://github.com/opensearch-project/asynchronous-search/pull/61))


### OpenSearch Cross Cluster Replication
* Refactored replication specific translog policy and addressed flaky tests ([#236](https://github.com/opensearch-project/cross-cluster-replication/pull/236))
* Rename translog pruning setting to match 1.1 convention and addressed behavior for translog deletion to be same as 1.1 ([#234](https://github.com/opensearch-project/cross-cluster-replication/pull/234))
* Changes to ensure replication tasks are not failing prematurely ([#231](https://github.com/opensearch-project/cross-cluster-replication/pull/231))
* Replication task fails to initialize due to state parsing failure ([#226](https://github.com/opensearch-project/cross-cluster-replication/pull/226))


### OpenSearch Dashboards Reports
* Fix quoting and url-encoding ([#153](https://github.com/opensearch-project/dashboards-reports/pull/153))
* Remove hard coded localhost when calling API ([#172](https://github.com/opensearch-project/dashboards-reports/pull/172))
* Fix Report Creation after Report Definition Creation ([#196](https://github.com/opensearch-project/dashboards-reports/pull/196))
* Fix csv missing fields issue and empty csv on _source fields ([#206](https://github.com/opensearch-project/dashboards-reports/pull/206))
* Revert backend paths to opendistro  ([#218](https://github.com/opensearch-project/dashboards-reports/pull/218))


### OpenSearch Index Management
* Adds implementation for the delay feature in rollup jobs ([#147](https://github.com/opensearch-project/index-management/pull/147))
* Remove policy API on read only indices ([#182](https://github.com/opensearch-project/index-management/pull/182))
* In explain API not showing the total count to all users ([#185](https://github.com/opensearch-project/index-management/pull/185))


### OpenSearch Index Management Dashboards Plugin
* Fixes editing rollup delay ([#82](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/82))
* Fixed Transforms geo_point bug and boolean render ([#93](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/93))
* Transform bug fixes ([#109](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/109))
* Fix the bugs in visual UI for legacy notification ([#111](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/111))
* Fix pagination of managed indices page ([#113](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/113))


### OpenSearch Job Scheduler
* Fixes possible negative jitter ([#78](https://github.com/opensearch-project/job-scheduler/pull/78))


### OpenSearch k-NN
* Fix library compile to package openblas statically ([#153](https://github.com/opensearch-project/k-NN/pull/153))
* Add validation to check max int limit in train API ([#159](https://github.com/opensearch-project/k-NN/pull/159))
* Support source filtering for model search ([#162](https://github.com/opensearch-project/k-NN/pull/162))
* Add super call to constructors in transport ([#169](https://github.com/opensearch-project/k-NN/pull/169))
* Return 400 on failed training request ([#168](https://github.com/opensearch-project/k-NN/pull/168))
* Add validation to check max k limit ([#178](https://github.com/opensearch-project/k-NN/pull/178))
* Fix bugs in parameter passing to JNI ([#189](https://github.com/opensearch-project/k-NN/pull/189))
* Clean up strings releated to faiss feature ([#190](https://github.com/opensearch-project/k-NN/pull/190))
* Fix issue passing parameters to native libraries ([#199](https://github.com/opensearch-project/k-NN/pull/199))
* Fix parameter validation for native libraries ([#202](https://github.com/opensearch-project/k-NN/pull/202))
* Fix field validation in VectorReader ([#207](https://github.com/opensearch-project/k-NN/pull/207))


### OpenSearch Performance Analyzer
* Add checkstyle plugin reference ([#79](https://github.com/opensearch-project/performance-analyzer/pull/79))
* Add snapshot variable when building RCA ([#83](https://github.com/opensearch-project/performance-analyzer/pull/83))
* Fix broken build and remove deb rpm files ([#85](https://github.com/opensearch-project/performance-analyzer/pull/85))
* Remove emitting the entry key with the METRICS_WRITE_ERROR metric ([#71](https://github.com/opensearch-project/performance-analyzer-rca/pull/71))
* Add log rotation and prevent noisy logs ([#87](https://github.com/opensearch-project/performance-analyzer-rca/pull/87))


### OpenSearch Security
* Fix to include hidden indices when resolving wildcards ([#1472](https://github.com/opensearch-project/security/pull/1472))


### OpenSearch Trace Analytics
* Redirect legacy notebooks URL to current observability one ([#141](https://github.com/opensearch-project/trace-analytics/pull/141))
* Autocomplete only displays current command ([#157](https://github.com/opensearch-project/trace-analytics/pull/157))
* Use JS API to redirect legacy notebooks URL ([#162](https://github.com/opensearch-project/trace-analytics/pull/162))
* Panels bug fix#1 ([#159](https://github.com/opensearch-project/trace-analytics/pull/159))
* Panels bug fix2 ([#170](https://github.com/opensearch-project/trace-analytics/pull/170))
* Timestamp fix ([#175](https://github.com/opensearch-project/trace-analytics/pull/175))
* Fix deleting all paragraphs for notebooks ([#184](https://github.com/opensearch-project/trace-analytics/pull/184))
* Fix for duplicate indices in suggestion ([#190](https://github.com/opensearch-project/trace-analytics/pull/190))
* Added panels modifications and bug fix ([#194](https://github.com/opensearch-project/trace-analytics/pull/194))
* Update plugin ID and bug fixes ([#195](https://github.com/opensearch-project/trace-analytics/pull/195))
* Feature autocomplete fix ([#208](https://github.com/opensearch-project/trace-analytics/pull/208))
* Use parent height instead of view port height for nav bar ([#212](https://github.com/opensearch-project/trace-analytics/pull/212))
* Correct suggestions after count command ([#215](https://github.com/opensearch-project/trace-analytics/pull/215))
* Explorer fixes ([#216](https://github.com/opensearch-project/trace-analytics/pull/216))
* Add missing itemName properties ([#218](https://github.com/opensearch-project/trace-analytics/pull/218))
* Tab issue and run button ([#219](https://github.com/opensearch-project/trace-analytics/pull/219))
* Fixed emoji renders for in PPL manual ([#221](https://github.com/opensearch-project/trace-analytics/pull/221))
* Throw exception if object type is inconsistent in update request ([#224](https://github.com/opensearch-project/trace-analytics/pull/224))
* Suggestions loaded after selection ([#228](https://github.com/opensearch-project/trace-analytics/pull/228))
* Panels backend call fix ([#232](https://github.com/opensearch-project/trace-analytics/pull/232))
* resolved conflicts and fixes ([#233](https://github.com/opensearch-project/trace-analytics/pull/233))
* Remove resetting query for autocomplete ([#234](https://github.com/opensearch-project/trace-analytics/pull/234))
* Update notebooks url redirect to use plugin id ([#242](https://github.com/opensearch-project/trace-analytics/pull/242))
* Tab close issue ([#243](https://github.com/opensearch-project/trace-analytics/pull/243))
* Fix undefined field error and where suggestions ([#246](https://github.com/opensearch-project/trace-analytics/pull/246))
* Switching tab tirgger unnecessary requests fix ([#247](https://github.com/opensearch-project/trace-analytics/pull/247))
* Panels bug fix4 ([#249](https://github.com/opensearch-project/trace-analytics/pull/249))


## INFRASTRUCTURE

### OpenSearch Alerting
* Update build to use public Maven repo ([#184](https://github.com/opensearch-project/alerting/pull/184))
* Publish notification JARs checksums. ([#196](https://github.com/opensearch-project/alerting/pull/196))
* Updates testCompile mockito version to match OpenSearch changes ([#204](https://github.com/opensearch-project/alerting/pull/204))
* Update maven publication to include cksums. ([#224](https://github.com/opensearch-project/alerting/pull/224))
* Updates alerting version to 1.2 ([#192](https://github.com/opensearch-project/alerting/pull/192))


### OpenSearch Anomaly Detection
* Adding support for integration tests with remote cluster. ([#298](https://github.com/opensearch-project/anomaly-detection/pull/298))


### OpenSearch Anomaly Detection Dashboards
* Add DCO Check Workflow ([#103](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/103))
* Bump version to 1.2 ([#114](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/114))
* Fix e2e ([#116](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/116))


### OpenSearch Asynchronous Search
* Removes default integtest.sh ([#36](https://github.com/opensearch-project/asynchronous-search/pull/36))
* Updating CI workflows ([#41](https://github.com/opensearch-project/asynchronous-search/pull/41))


### OpenSearch Cross Cluster Replication
* [CI] Version bump to 1.2 ([#213](https://github.com/opensearch-project/cross-cluster-replication/pull/213))
* Add DCO chek workflow ([#212](https://github.com/opensearch-project/cross-cluster-replication/pull/212))


### OpenSearch Index Management
* Uses published daily snapshot dependencies ([#141](https://github.com/opensearch-project/index-management/pull/141))
* Removes default integtest.sh ([#148](https://github.com/opensearch-project/index-management/pull/148))
* Adds mavenLocal back to repositories ([#158](https://github.com/opensearch-project/index-management/pull/158))


### OpenSearch Index Management Dashboards Plugin
* Transforms unit and cypress tests ([#92](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/92))
* Fixes flakey tests ([#105](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/105))
* Disables jitter for managed_indices_spec Cypress tests ([#122](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/122))


### OpenSearch Job Scheduler
* Publish MD5 and SHA1 signatures ([#71](https://github.com/opensearch-project/job-scheduler/pull/71))


### OpenSearch k-NN
* Update workflow ([#109](https://github.com/opensearch-project/k-NN/pull/109))
* Use published daily snapshot dependencies ([#119](https://github.com/opensearch-project/k-NN/pull/119))
* Add DCO workflow check ([#120](https://github.com/opensearch-project/k-NN/pull/120))
* Update branch pattern ([#123](https://github.com/opensearch-project/k-NN/pull/123))
* Increment version on main to 1.2.0.0 ([#138](https://github.com/opensearch-project/k-NN/pull/138))
* Adding knn lib build script ([#154](https://github.com/opensearch-project/k-NN/pull/154))
* Add lib into knn zip during build ([#163](https://github.com/opensearch-project/k-NN/pull/163))
* Disable simd for arm faiss ([#166](https://github.com/opensearch-project/k-NN/pull/166))
* Add checkstyle plugin dependency ([#177](https://github.com/opensearch-project/k-NN/pull/177))
* Package openmp lib with knnlib in zip and minor fixes ([#175](https://github.com/opensearch-project/k-NN/pull/175))
* Update license and attributions for faiss addition ([#187](https://github.com/opensearch-project/k-NN/pull/187))
* Update license headers ([#194](https://github.com/opensearch-project/k-NN/pull/194))
* Update license headers in gradle files ([#201](https://github.com/opensearch-project/k-NN/pull/201))


### OpenSearch Trace Analytics
* Refactor trace analytics UT and IT, sync main branch ([#107](https://github.com/opensearch-project/trace-analytics/pull/107))
* Bump prismjs from 1.24.1 to 1.25.0 ([#137](https://github.com/opensearch-project/trace-analytics/pull/137))
* Bump immer from 9.0.5 to 9.0.6 ([#136](https://github.com/opensearch-project/trace-analytics/pull/136))
* Update data modal and enable CI ([#148](https://github.com/opensearch-project/trace-analytics/pull/148))
* Add integration tests for observability backend plugin ([#180](https://github.com/opensearch-project/trace-analytics/pull/180))
* Bump ansi-regex to 5.0.1 ([#241](https://github.com/opensearch-project/trace-analytics/pull/241))
* Add support for codeowners to repo ([#244](https://github.com/opensearch-project/trace-analytics/pull/244))
* Panels cypress test ([#256](https://github.com/opensearch-project/trace-analytics/pull/256))


## DOCUMENTATION

### OpenSearch Alerting
* Add release notes for 1.2.0.0 release ([#225](https://github.com/opensearch-project/alerting/pull/225))


### OpenSearch Anomaly Detection
* Correct copyright notice; remove old copyright from ODFE ([#257](https://github.com/opensearch-project/anomaly-detection/pull/257))
* Add DCO Check Workflow ([#273](https://github.com/opensearch-project/anomaly-detection/pull/273))


### OpenSearch Dashboards Reports
* Update validation for observability notebooks integration ([#174](https://github.com/opensearch-project/dashboards-reports/pull/174))
* Add dco and release drafter workflows ([#217](https://github.com/opensearch-project/dashboards-reports/pull/217))
* update README notification section ([#216](https://github.com/opensearch-project/dashboards-reports/pull/216))


### OpenSearch Dashboards Visualizations
* Update copyright notice in README and headers ([#35](https://github.com/opensearch-project/dashboards-visualizations/pull/35))


### OpenSearch Index Management
* Automatically provides license header for new files ([#142](https://github.com/opensearch-project/index-management/pull/142))


### OpenSearch Job Scheduler
* Add release notes for 1.2.0.0 ([#84](https://github.com/opensearch-project/job-scheduler/pull/84))


### OpenSearch k-NN
* Add support for codeowners to repo ([#206](https://github.com/opensearch-project/k-NN/pull/206))


### OpenSearch Performance Analyzer
* Update README.md ([#88](https://github.com/opensearch-project/performance-analyzer-rca/pull/88))


### OpenSearch SQL
* Create 1.2 release notes ([#268](https://github.com/opensearch-project/sql/pull/268))
* Update notice files ([#269](https://github.com/opensearch-project/sql/pull/269))
* Update license header ([#282](https://github.com/opensearch-project/sql/pull/282))
* Updated PPL user manual with relevance function limitations ([#283](https://github.com/opensearch-project/sql/pull/283))


### OpenSearch Trace Analytics
* Update docs for observability ([#188](https://github.com/opensearch-project/trace-analytics/pull/188))
* Add copyright to all files ([#231](https://github.com/opensearch-project/trace-analytics/pull/231))
* PPL manual update ([#236](https://github.com/opensearch-project/trace-analytics/pull/236))


## MAINTENANCE

### OpenSearch Alerting
* Update copyright notice ([#222](https://github.com/opensearch-project/alerting/pull/222))
* Update copyright notice and add DCO workflow ([#229](https://github.com/opensearch-project/alerting/pull/229))


### OpenSearch Alerting Dashboards Plugin
* Bumps version to 1.2 ([#128](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/128))
* Added 1.2 release notes. ([#141](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/141))


### OpenSearch Anomaly Detection
* Bump anomaly-detection version to 1.2 ([#286](https://github.com/opensearch-project/anomaly-detection/pull/286))


### OpenSearch Asynchronous Search
* Adds DCO check  ([#57](https://github.com/opensearch-project/asynchronous-search/pull/57))
* Incremented asynchronous search version to 1.2 [#53](https://github.com/opensearch-project/asynchronous-search/pull/53)

### OpenSearch Dashboards Reports
* Bump to version 1.2 ([#203](https://github.com/opensearch-project/dashboards-reports/pull/203))
* Bump tmpl from 1.0.4 to 1.0.5 in /dashboards-reports ([#164](https://github.com/opensearch-project/dashboards-reports/pull/164))
* rename plugin helper config file name to consistent with OSD ([#180](https://github.com/opensearch-project/dashboards-reports/pull/180))


### OpenSearch Dashboards Visualizations
* Remove explicit jest dependency ([#25](https://github.com/opensearch-project/dashboards-visualizations/pull/25))
* Rename plugin-helpers config file name to be consistent with OSD ([#31](https://github.com/opensearch-project/dashboards-visualizations/pull/31))
* Add project logo and correct links to LICENSE and NOTICE in README ([#35](https://github.com/opensearch-project/dashboards-visualizations/pull/35))
* Add DCO check to PRs ([#37](https://github.com/opensearch-project/dashboards-visualizations/pull/37))
* Bump version for OpenSearch 1.2.0 release ([#36](https://github.com/opensearch-project/dashboards-visualizations/pull/36))


### OpenSearch Index Management
* Updates index management version to 1.2 ([#157](https://github.com/opensearch-project/index-management/pull/157))
* Updates testCompile mockito version, adds AwaitsFix annotation to MetadataRegressionIT tests ([#168](https://github.com/opensearch-project/index-management/pull/168))


### OpenSearch Index Management Dashboards Plugin
* Bumps version to 1.2 ([#103](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/103))


### OpenSearch Job Scheduler
* Updates job scheduler version to 1.2 ([#68](https://github.com/opensearch-project/job-scheduler/pull/68))


### OpenSearch Performance Analyzer
* Add BWC tests for PA ([#69](https://github.com/opensearch-project/performance-analyzer/pull/69))
* Add DCO workflow and fix failing IT ([#78](https://github.com/opensearch-project/performance-analyzer/pull/78))
* Add DCO workflow ([#83](https://github.com/opensearch-project/performance-analyzer-rca/pull/83))


### OpenSearch Security
* Adding DCO check to repo ([#1468](https://github.com/opensearch-project/security/pull/1468))
* Moved dco.yml to workflows folder ([#1469](https://github.com/opensearch-project/security/pull/1469))
* Incremented version to 1.2.0.0-SNAPSHOT ([#1464](https://github.com/opensearch-project/security/pull/1464))
* Moved SNAPSHOTS repo to project level ([#1479](https://github.com/opensearch-project/security/pull/1479))
* Update OpenSearch core dependency version to 1.2.0 ([#1482](https://github.com/opensearch-project/security/pull/1482))
* Bump xmlsec from 2.2.0 to 2.2.3 ([#1450](https://github.com/opensearch-project/security/pull/1450))
* Create 1.2.0.0 release notes ([#1494](https://github.com/opensearch-project/security/pull/1494))
* Updated copyright notices ([#1477](https://github.com/opensearch-project/security/pull/1477))
* Updated release notes for 1.2 with copyright updates ([#1496](https://github.com/opensearch-project/security/pull/1496))


### OpenSearch Security Dashboards Plugin
* Removing default integtest.sh ([#829](https://github.com/opensearch-project/security-dashboards-plugin/pull/829))
* Bump version to 1.2.0.0 ([#850](https://github.com/opensearch-project/security-dashboards-plugin/pull/850))
* Adding DCO check to repo. Closes [#835](https://github.com/opensearch-project/security-dashboards-plugin/pull/835) ([#839](https://github.com/opensearch-project/security-dashboards-plugin/pull/839))
* Update release note for 1.2 ([#853](https://github.com/opensearch-project/security-dashboards-plugin/pull/853))
* Updated copyright notices ([#847](https://github.com/opensearch-project/security-dashboards-plugin/pull/847))
* Updated release notes for 1.2 with copyright updates ([#856](https://github.com/opensearch-project/security-dashboards-plugin/pull/856))
* Remove job building os core in integration test (#860) ([#863](https://github.com/opensearch-project/security-dashboards-plugin/pull/863))


### OpenSearch SQL
* Bumps version to 1.2 ([#254](https://github.com/opensearch-project/sql/pull/254))


### OpenSearch Trace Analytics
* Bump observability version for OpenSearch 1.2 release ([#189](https://github.com/opensearch-project/trace-analytics/pull/189))


## REFACTORING

### OpenSearch k-NN
* Make model id part of index ([#167](https://github.com/opensearch-project/k-NN/pull/167))
* Remove unused code from function ([#196](https://github.com/opensearch-project/k-NN/pull/196))


### OpenSearch Trace Analytics
* Merge observability into main branch ([#135](https://github.com/opensearch-project/trace-analytics/pull/135))
* Move observability frontend to a sub directory ([#142](https://github.com/opensearch-project/trace-analytics/pull/142))
* Remove app analytics ([#154](https://github.com/opensearch-project/trace-analytics/pull/154))


