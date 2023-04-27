# OpenSearch and OpenSearch Dashboards 2.7.0 Release Notes

## Release Highlights
OpenSearch 2.7.0 includes a number of new and enhanced features for your search, observability, and analytics workloads. This release delivers production-ready functionality for segment replication, searchable snapshots, and the ability to add multiple data sources to a single dashboard—features that were previously released as experimental. Also included are new flat object fields for more efficient indexing, integrated observability features within OpenSearch Dashboards, new geospatial functionality, and updates designed to simplify administration of indexes and clusters.

### New Features
* You can now choose segment replication as a data replication strategy for production workloads. Segment replication can yield improved indexing throughput and lower resource utilization at the expense of increased network utilization and refresh times.
* Searchable snapshots also move from experimental to production-ready with this release, allowing users to search indexes that are stored as snapshots within remote repositories in real time.
* The third feature moving out of experimental status is support for multiple data sources in OpenSearch Dashboards. Dynamically manage data sources across multiple OpenSearch clusters, combine visualizations into a single dashboard, and more.
* New flat object fields let you store complex JSON objects in an index without indexing all subfields separately, offering improved resource utilization.
* You can now access observability features from OpenSearch Dashboards, create your own observability dashboards, add event analytics visualizations, and more without leaving the Dashboards environment.
* Geospatial functionality receives upgrades as new shape-based filters let you filter your geospatial data by drawing a rectangle or polygon over a selected area of the map. This release also enables OpenSearch to display maps in local languages.
* OpenSearch makes managing multiple indexes simpler with the addition of component templates. These templates can help you abstract common index settings, mappings, and aliases into reusable building blocks.
* Another time-saving upgrade for OpenSearch administrators comes with the availability of dynamic tenants management in OpenSearch Dashboards. Admins can view, configure, and enable or disable tenancy within Dashboards and effect those changes without a restart.
* You can now use the Performance Analyzer plugin to identify hot shards within an index, so you can take action and mitigate potential impacts on performance and availability.

### Experimental Features
OpenSearch 2.7.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.

* A new correlation engine is added to the Security Analytics toolkit, enabling a knowledge graph that can be used to identify, store, and recall connected events data to help you identify patterns and investigate relationships.
* The experimental ML Framework gains a new automatic reloading mechanism for ML models, allowing you to auto-reload deployed models when a cluster restarts or when a node rejoins the cluster.


## Release Details

[OpenSearch and OpenSearch Dashboards 2.7.0](https://opensearch.org/versions/opensearch-2-7-0.html) includes the following feature, enhancement, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.7.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.7.0.md).


## BREAKING CHANGES

### OpenSearch Ml Commons Dashboards
* Ml-commons introduced a API breaking change in 2.7 which changed the API response data, FE is updated accordingly. With this change, FE will no longer compatible with OpenSearch version < 2.7 ([#154](https://github.com/opensearch-project/ml-commons-dashboards/pull/154))


## FEATURES

### OpenSearch Alerting Dashboards
* Implemented support for configuring up to 10 data filters for query and bucket level monitors using the visual editor. ([#504](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/504))
* Implemented support for >, >=, <, and <= query operators for the doc level monitor visual editor. ([#508](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/508))


### OpenSearch Common Utils
* InjectSecurity - inject User object in UserInfo in threadContext. ([#396](https://github.com/opensearch-project/common-utils/pull/396))


### OpenSearch Dashboards Maps
* Add localization for opensearch base map ([#312](https://github.com/opensearch-project/dashboards-maps/pull/312))
* Add geo shape query filter ([#319](https://github.com/opensearch-project/dashboards-maps/pull/319))
* Support adding static label to document layer ([#322](https://github.com/opensearch-project/dashboards-maps/pull/322))
* Add shape filter UI button ([#329](https://github.com/opensearch-project/dashboards-maps/pull/329))
* Add tooltip to draw shape filter ([#330](https://github.com/opensearch-project/dashboards-maps/pull/330))
* Support adding field label to document layer ([#336](https://github.com/opensearch-project/dashboards-maps/pull/336))
* Add search query ability on map([#370](https://github.com/opensearch-project/dashboards-maps/pull/370))


### OpenSearch Dashboards Search Relevance
* [Feature] Exposing Metrics for Search Comparison Tool ([#162](https://github.com/opensearch-project/dashboards-search-relevance/pull/162))


### OpenSearch Index Management
* Error Prevention: Add close action. ([#728](https://github.com/opensearch-project/index-management/pull/728))
* Error Prevention: Add index priority action. ([#729](https://github.com/opensearch-project/index-management/pull/729))
* Error Prevention: Add notification, shrink, allocation and rollup. ([#732](https://github.com/opensearch-project/index-management/pull/732))
* Error Prevention: Add transition action. ([#744](https://github.com/opensearch-project/index-management/pull/744))
* Error Prevention: Add snapshot action. ([#745](https://github.com/opensearch-project/index-management/pull/745))


### OpenSearch Index Management Dashboards Plugin
* Feature: Enhancement of JSON validation on JSON editor of index mapping  ([#606](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/606))
* Feature: Enable component templates management and simulation  ([#662](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/662))


### OpenSearch Job Scheduler
* Adding name and description to org.opensearch.opensearch-job-scheduler pom ([#338](https://github.com/opensearch-project/job-scheduler/pull/338))
* Adding Decoupling snapshots ([#324](https://github.com/opensearch-project/job-scheduler/pull/324))
* Adding generatePomFileForPluginZipPublication as dependency of publishNebulaPublicationToSnapshotsRepository ([#360](https://github.com/opensearch-project/job-scheduler/pull/360))
* Adding groupId to pom section of build.gradle ([#363](https://github.com/opensearch-project/job-scheduler/pull/363))


### OpenSearch Observability
* Create first Nginx Integration bundle ([#1442](https://github.com/opensearch-project/observability/pull/1442))
* Add catalog meta info in the index template ([#1446](https://github.com/opensearch-project/observability/pull/1446))


### OpenSearch Observability Dashboards
* Observability Visualizations enabled to add to OpenSearch Dashboards / Dashboards [#353](https://github.com/opensearch-project/dashboards-observability/pull/353)
* Display Observability Dashboards in OpenSearch Dashboards / Dashboards listing [#355](https://github.com/opensearch-project/dashboards-observability/pull/355)
* Observability Left-Navigation now grouped at "first level" of OpenSearch Dashboards Left-Navigation fly-out [#354](https://github.com/opensearch-project/dashboards-observability/pull/354)


### OpenSearch Security Analytics
* New log types. ([#332](https://github.com/opensearch-project/security-analytics/pull/332))
* Support for multiple indices in detector input. ([#336](https://github.com/opensearch-project/security-analytics/pull/336))


### OpenSearch Security Analytics Dashboards
* Adds field mappings to edit detector pages. ([#490](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/490))
* Correlation engine UX. ([#536](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/536))


### OpenSearch Security
* Dynamic tenancy configurations ([#2607](https://github.com/opensearch-project/security/pull/2607))


### OpenSearch Security Dashboards Plugin
* Dynamic tenancy configurations ([#1394](https://github.com/opensearch-project/security-dashboards-plugin/pull/1394))


### OpenSearch SQL
* Create datasource API (#1458) ([#1479](https://github.com/opensearch-project/sql/pull/1479))
* REST API for GET,PUT and DELETE ([#1502](https://github.com/opensearch-project/sql/pull/1502))


## ENHANCEMENTS

### OpenSearch Anomaly Detection
* Giving admin priority over backendrole filtering. ([#850](https://github.com/opensearch-project/anomaly-detection/pull/850))


### OpenSearch Anomaly Detection Dashboards
* Run prettier command against all files ([#444](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/444))


### OpenSearch Dashboards Maps
* Enhance layer visibility status display ([#299](https://github.com/opensearch-project/dashboards-maps/pull/299))
* Introduce disable tooltip on hover property ([#313](https://github.com/opensearch-project/dashboards-maps/pull/313))
* Update tooltip behavior change ([#317](https://github.com/opensearch-project/dashboards-maps/pull/317))
* Update max supported layer count ([#332](https://github.com/opensearch-project/dashboards-maps/pull/332))
* BWC for document layer label textType ([#340](https://github.com/opensearch-project/dashboards-maps/pull/340))
* Add mapbox-gl draw mode ([#347](https://github.com/opensearch-project/dashboards-maps/pull/347))
* Add support to draw rectangle shape to filter documents ([#348](https://github.com/opensearch-project/dashboards-maps/pull/348))
* Avoid trigger tooltip from label ([#350](https://github.com/opensearch-project/dashboards-maps/pull/350))
* Remove cancel button on draw shape and use Escape to cancel draw ([#359](https://github.com/opensearch-project/dashboards-maps/pull/359))
* Add support to build GeoShapeFilterMeta and GeoShapeFilter ([#360](https://github.com/opensearch-project/dashboards-maps/pull/360))
* Update listener on KeyUp ([#364](https://github.com/opensearch-project/dashboards-maps/pull/364))
* Add geoshape filter while render data layers ([#365](https://github.com/opensearch-project/dashboards-maps/pull/365))
* Add filter bar to display global geospatial filters ([#371](https://github.com/opensearch-project/dashboards-maps/pull/371))
* Update draw filter shape ui properties ([#372](https://github.com/opensearch-project/dashboards-maps/pull/372))
* Change font opacity along with OpenSearch base map layer ([#373](https://github.com/opensearch-project/dashboards-maps/pull/373))
* Toast Warning Message if OpenSearch base map is used in conflicting regions ([#382](https://github.com/opensearch-project/dashboards-maps/pull/382))
* Add before layer id when adding documents label ([#387](https://github.com/opensearch-project/dashboards-maps/pull/387))


### OpenSearch k-NN
* Support .opensearch-knn-model index as system index with security enabled ([#827](https://github.com/opensearch-project/k-NN/pull/827))


### OpenSearch Ml Commons
* Add model auto deploy feature ([#852](https://github.com/opensearch-project/ml-commons/pull/852))
* Add memory consumption estimation for models in profile API ([#853](https://github.com/opensearch-project/ml-commons/pull/853))
* Add text docs ML input ([#830](https://github.com/opensearch-project/ml-commons/pull/830))
* Add allow custom deployment plan setting; add deploy to all nodes field in model index ([#818](https://github.com/opensearch-project/ml-commons/pull/818))
* Add exclude nodes setting. ([#813](https://github.com/opensearch-project/ml-commons/pull/813))
* set model state as partially loaded if unload model from partial nodes ([#806](https://github.com/opensearch-project/ml-commons/pull/806))


### OpenSearch Performance Analyzer
* Adding CIRCUIT_BREAKER_COLLECTOR_EXECUTION_TIME, CIRCUIT_BREAKER_COLLECTOR_ERROR, CLUSTER_MANAGER_METRICS_ERROR in StatExceptionCode ([420](https://github.com/opensearch-project/performance-analyzer/pull/420/))
* Adding Shard HotSpot feature in RCA ([295](https://github.com/opensearch-project/performance-analyzer-rca/pull/295))


### OpenSearch Security
* Clock skew tolerance for oidc token validation ([#2482](https://github.com/opensearch-project/security/pull/2482))
* Adding index template permissions to kibana_server role ([#2503](https://github.com/opensearch-project/security/pull/2503))
* Add a test in order to catch incorrect handling of index parsing during Snapshot Restoration ([#2384](https://github.com/opensearch-project/security/pull/2384))
* Expand Dls Tests for easier verification of functionality ([#2634](https://github.com/opensearch-project/security/pull/2634))
* New system index[.ql-datasources] for ppl/sql datasource configurations ([#2650](https://github.com/opensearch-project/security/pull/2650))
* Allows for configuration of LDAP referral following ([#2135](https://github.com/opensearch-project/security/pull/2135))


### OpenSearch Security Dashboards Plugin
* Replace legacy template with index template ([#1359](https://github.com/opensearch-project/security-dashboards-plugin/pull/1359))
* Add loginEndPointWithPath ([#1358](https://github.com/opensearch-project/security-dashboards-plugin/pull/1358))
* Add new actions for ppl and datasource apis ([#1395](https://github.com/opensearch-project/security-dashboards-plugin/pull/1395))
* Split up a value into multiple cookie payloads ([#1352](https://github.com/opensearch-project/security-dashboards-plugin/pull/1352))


### OpenSearch SQL
* [main]Changes in DataSourceService and DataSourceMetadataStorage interface ([#1414](https://github.com/opensearch-project/sql/pull/1414))
* Added SINH function to V2 engine ([#1437](https://github.com/opensearch-project/sql/pull/1437))
* Added RINT function to V2 engine  ([#1439](https://github.com/opensearch-project/sql/pull/1439))
* Add `sec_to_time` Function To OpenSearch SQL ([#1438](https://github.com/opensearch-project/sql/pull/1438))
* Add `WEEKDAY` Function to SQL Plugin ([#1440](https://github.com/opensearch-project/sql/pull/1440))
* Add `YEARWEEK` Function To OpenSearch SQL ([#1445](https://github.com/opensearch-project/sql/pull/1445))
* Add `EXTRACT` Function To OpenSearch SQL Plugin ([#1443](https://github.com/opensearch-project/sql/pull/1443))
* Add `STR_TO_DATE` Function To The SQL Plugin ([#1444](https://github.com/opensearch-project/sql/pull/1444))
* Add The `TO_SECONDS` Function To The SQL Plugin ([#1447](https://github.com/opensearch-project/sql/pull/1447))
* Added Arithmetic functions to V2 engine ([#1448](https://github.com/opensearch-project/sql/pull/1448))
* Added SIGNUM function to V2 engine ([#1442](https://github.com/opensearch-project/sql/pull/1442))
* Add `TIMESTAMPADD` Function To OpenSearch SQL Plugin ([#1453](https://github.com/opensearch-project/sql/pull/1453))
* Add `Timestampdiff` Function To OpenSearch SQL ([#1472](https://github.com/opensearch-project/sql/pull/1472))
* Add Nested Support in Select Clause (#1490) ([#1518](https://github.com/opensearch-project/sql/pull/1518))
* Fix null response from pow/power and added missing integration testing ([#1459](https://github.com/opensearch-project/sql/pull/1459))


## BUG FIXES


### OpenSearch Alerting
* Issue with percolate query transforming documents with object type fields. ([#844](https://github.com/opensearch-project/alerting/issues/844))
* Notification security fix. ([#852](https://github.com/opensearch-project/alerting/pull/852))


### OpenSearch Alerting Dashboards
* Anomaly detection UI bug fixes. ([#502](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/502))
* Fixed a bug with doc level trigger creation. ([#513](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/513))


### OpenSearch Common Utils
* Fix SNS regex for validation on notification channel to support SNS FIFO topics. ([#381](https://github.com/opensearch-project/common-utils/pull/381))


### OpenSearch Cross Cluster Replication
* Modified autofollow stats to rely on single source for failed indices ([#736](https://github.com/opensearch-project/cross-cluster-replication/pull/736))
* Update UpdateAutoFollowPatternIT "test auto follow stats" to wait for 60 seconds ([#745](https://github.com/opensearch-project/cross-cluster-replication/pull/745))
* Update imports from common to core package ([#761](https://github.com/opensearch-project/cross-cluster-replication/pull/761))
* Adding a proxy mode connection setup for CCR ([#795](https://github.com/opensearch-project/cross-cluster-replication/pull/795))
* Handled exception under multi-field mapping update ([#789](https://github.com/opensearch-project/cross-cluster-replication/pull/789))
* Handled batch requests for replication metadata update under cluster state ([#778](https://github.com/opensearch-project/cross-cluster-replication/pull/778))


### OpenSearch Dashboards Maps
* Fix: fixed filters not reset when index pattern changed ([#234](https://github.com/opensearch-project/dashboards-maps/pull/234))
* Fix property value undefined check ([#276](https://github.com/opensearch-project/dashboards-maps/pull/276))
* Show scroll bar when panel height reaches container bottom ([#295](https://github.com/opensearch-project/dashboards-maps/pull/295))
* Add custom layer visibility config to render ([#297](https://github.com/opensearch-project/dashboards-maps/pull/297))
* Fix color picker component issue ([#305](https://github.com/opensearch-project/dashboards-maps/pull/305))
* Fix: layer filter setting been reset unexpectedly ([#327](https://github.com/opensearch-project/dashboards-maps/pull/327))
* Fix data query in dashboard mode when enable around map filter ([#339](https://github.com/opensearch-project/dashboards-maps/pull/339))
* Sync maplibre layer order after layers rendered ([#353](https://github.com/opensearch-project/dashboards-maps/pull/353))


### OpenSearch Dashboards Notifications
* Fix CI flow. ([#33](https://github.com/opensearch-project/dashboards-notifications/pull/33))


### OpenSearch Dashboards Reporting
* Upgrade json2csv to fix missing value for nested field with false/0 ([#78](https://github.com/opensearch-project/dashboards-reporting/pull/78))
* Preserve chart legends in reports ([#81](https://github.com/opensearch-project/dashboards-reporting/pull/81))
* Add tesseract and foreign object rendering ([#86](https://github.com/opensearch-project/dashboards-reporting/pull/86))
* Update jsdom version to remove request dependency ([#89](https://github.com/opensearch-project/dashboards-reporting/pull/89))


### OpenSearch Dashboards Search Relevance
* [Bug][Build] Export config file ([#182](https://github.com/opensearch-project/dashboards-search-relevance/pull/183))
* Removing stats.yml until an alternate can be found that can publish P… ([#110](https://github.com/opensearch-project/dashboards-search-relevance/pull/110))


### OpenSearch Index Management
* Shrink action Fix. ([#718](https://github.com/opensearch-project/index-management/pull/718))


### OpenSearch Index Management Dashboards Plugin
* Fix link destination and make the link open in a new window. ([#652](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/652))
* Fix the alias deletion issue in security mode.([#704](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/704))
* Add downgrade logic when fetching indexes ([#684](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/684))
* Fix bugs during internal bugathon and fix the alias deletion issue in security mode. ([#704](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/704))


### OpenSearch k-NN
* Throw errors on model deletion failures ([#834](https://github.com/opensearch-project/k-NN/pull/834))


### OpenSearch Ml Commons
* Change to old method to fix missing method createParentDirectories ([#759](https://github.com/opensearch-project/ml-commons/pull/759))
* Fix delete model API ([#861](https://github.com/opensearch-project/ml-commons/pull/861))
* Fix breaking changes of Xcontent namespace change ([#838](https://github.com/opensearch-project/ml-commons/pull/838))
* Change the ziputil dependency to fix a potential security concern ([#824](https://github.com/opensearch-project/ml-commons/pull/824))
* Fix checkstyle version ([#792](https://github.com/opensearch-project/ml-commons/pull/792))
* Typo fix and minor improvement in maven-publish GHA workflow ([#757](https://github.com/opensearch-project/ml-commons/pull/757))


### OpenSearch Ml Commons Dashboards
* Fixed an issue that model status is displayed as `Not responding` while the model status is loading ([#146](https://github.com/opensearch-project/ml-commons-dashboards/pull/146))


### OpenSearch Notifications
* Convert empty httpEntity to {} to avoid DeliveryStatus initialization exception ([#648](https://github.com/opensearch-project/notifications/pull/648))


### OpenSearch Performance Analyzer
* Fix AdmissionControl class loading issue in Netty/PA communication ([#414](https://github.com/opensearch-project/performance-analyzer/pull/414))
* Fix GC metric not collected in RCA ([287](https://github.com/opensearch-project/performance-analyzer-rca/pull/287))
* Fix ShardEvents and ShardBulkDocs null metrics in RCA ([283](https://github.com/opensearch-project/performance-analyzer-rca/pull/283))


### OpenSearch Reporting
* Bump mockito-core version ([#678](https://github.com/opensearch-project/reporting/pull/678))
* Fix ci failures ([#681](https://github.com/opensearch-project/reporting/pull/681))


### OpenSearch Security Analytics
* Fix for integ test failures. ([#363](https://github.com/opensearch-project/security-analytics/pull/363))


### OpenSearch Security Analytics Dashboards
* Minor bug fixes. ([#505](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/505))
* Fixes few minor UX bugs. ([#525](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/525))
* Pinned babel traverse and core. ([#539](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/539))


### OpenSearch Security
* Support multitenancy for the anonymous user ([#2459](https://github.com/opensearch-project/security/pull/2459))
* Fix error message when system index is blocked ([#2525](https://github.com/opensearch-project/security/pull/2525))
* Fix of OpenSSLTest is not using the OpenSSL Provider ([#2301](https://github.com/opensearch-project/security/pull/2301))
* Add chmod 0600 to install_demo_configuration bash script ([#2550](https://github.com/opensearch-project/security/pull/2550))
* Fix SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder" ([#2564](https://github.com/opensearch-project/security/pull/2564))
* Fix lost privileges during auto initializing of the index ([#2498](https://github.com/opensearch-project/security/pull/2498))
* Fix NPE and add additional graceful error handling ([#2687](https://github.com/opensearch-project/security/pull/2687))


### OpenSearch Security Dashboards Plugin
* Fix No blank backend role before adding a new one in Create User page ([#1384](https://github.com/opensearch-project/security-dashboards-plugin/pull/1384))
* Fix "Get started" image is not adaptive to the browser window size. ([#1396](https://github.com/opensearch-project/security-dashboards-plugin/pull/1396))


### OpenSearch SQL
* Integ Test Refactoring ([#1383](https://github.com/opensearch-project/sql/pull/1383))
* Exclude OpenSearch system index when IT cleanup ([#1381](https://github.com/opensearch-project/sql/pull/1381))
* Ensure Nested Function Falls Back to Legacy Engine Where Not Supported ([#1549](https://github.com/opensearch-project/sql/pull/1549))
* adding reflections as a dependency ([#1559](https://github.com/opensearch-project/sql/pull/1559))


## INFRASTRUCTURE


### OpenSearch Alerting
* Use notification snapshot for integ test. ([#822](https://github.com/opensearch-project/alerting/pull/822))
* Use latest common-utils snapshot. ([#858](https://github.com/opensearch-project/alerting/pull/858))


### OpenSearch Alerting Dashboards
* Added untriaged issue workflow. ([#482](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/482))
* Fix Node.js and Yarn installation in CI. ([#496](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/496))


### OpenSearch Anomaly Detection
* Created untriaged issue workflow. ([#809](https://github.com/opensearch-project/anomaly-detection/pull/809))
* Update XContent imports. ([#854](https://github.com/opensearch-project/anomaly-detection/pull/854))
* Update NodeInfo constructor. ([#869](https://github.com/opensearch-project/anomaly-detection/pull/869))


### OpenSearch Common Utils
* Publish snapshots to maven via GHA. ([#365](https://github.com/opensearch-project/common-utils/pull/365))
* Add auto Github release workflow. ([#376](https://github.com/opensearch-project/common-utils/pull/376))


### OpenSearch Cross Cluster Replication
* Added support for running Integtest on Remote clusters ([#733](https://github.com/opensearch-project/cross-cluster-replication/pull/733))


### OpenSearch Dashboards Maps
* Add CHANGELOG ([#342](https://github.com/opensearch-project/dashboards-maps/pull/342))
* Add stats API for maps and layers in maps plugin ([#362](https://github.com/opensearch-project/dashboards-maps/pull/362))
* Fix cypress test failed due to OSD dashboard create button updated ([#393](https://github.com/opensearch-project/dashboards-maps/pull/393))


### OpenSearch Dashboards Reporting
* Fix Node.js and Yarn installation in CI ([#64](https://github.com/opensearch-project/dashboards-reporting/pull/64))


### OpenSearch Geospatial
* Publish snapshots to maven via GHA ([#233](https://github.com/opensearch-project/geospatial/pull/233))
* Update snapshot version and fix compilation issues ([#237](https://github.com/opensearch-project/geospatial/pull/237))
* Add CHANGELOG ([#238](https://github.com/opensearch-project/geospatial/pull/238))


### OpenSearch k-NN
* Add filter type to filtering release configs ([#792](https://github.com/opensearch-project/k-NN/pull/792))
* Add CHANGELOG ([#800](https://github.com/opensearch-project/k-NN/pull/800))
* Bump byte-buddy version from 1.12.22 to 1.14.2 ([#804](https://github.com/opensearch-project/k-NN/pull/804))
* Add 2.6.0 to BWC Version Matrix (([#810](https://github.com/opensearch-project/k-NN/pull/810)))
* Bump numpy version from 1.22.x to 1.24.2 ([#811](https://github.com/opensearch-project/k-NN/pull/811))
* Update BWC Version with OpenSearch Version Bump (([#813](https://github.com/opensearch-project/k-NN/pull/813)))
* Add GitHub action for secure integ tests ([#836](https://github.com/opensearch-project/k-NN/pull/836))
* Bump byte-buddy version to 1.14.3 ([#839](https://github.com/opensearch-project/k-NN/pull/839))
* Set gradle dependency scope for common-utils to testFixturesImplementation ([#844](https://github.com/opensearch-project/k-NN/pull/844))
* Add client setting to ignore warning exceptions ([#850](https://github.com/opensearch-project/k-NN/pull/850))


### OpenSearch Neural Search
* Avoid clearing settings after each test ([#159](https://github.com/opensearch-project/neural-search/pull/159))
* Add GHA to publish to maven repository ([#237](https://github.com/opensearch-project/neural-search/pull/130))
* Add reflection dependency ([#136](https://github.com/opensearch-project/neural-search/pull/136))
* Add CHANGELOG ([#135](https://github.com/opensearch-project/neural-search/pull/135))


### OpenSearch Notifications
* Fixed build failure due to OSCore xContent changes ([#646](https://github.com/opensearch-project/notifications/pull/646))
* Remove dashboards ([#640](https://github.com/opensearch-project/notifications/pull/640))


### OpenSearch Observability
- Automate releases based on tagging ([#1436](https://github.com/opensearch-project/observability/pull/1436))
- Fix maven branch ([#1449](https://github.com/opensearch-project/observability/pull/1449))
- Rename all SSO references to SS4O ([#1470](https://github.com/opensearch-project/observability/pull/1470))
- [BACKPORT 2.x] Fix 2.x imports ([#1483](https://github.com/opensearch-project/observability/pull/1483))


### OpenSearch Performance Analyzer
* Getting Jackson,JUnit, Log4j dependency version from core ([#417](https://github.com/opensearch-project/performance-analyzer/pull/417))
* Upgrade checkstyle to 9.3 ([#395](https://github.com/opensearch-project/performance-analyzer/pull/395))
* Publish snapshots to maven via GHA ([#385](https://github.com/opensearch-project/performance-analyzer/issues/385))


### OpenSearch Reporting
* Add publish snapshots to maven via GHA  ([#651](https://github.com/opensearch-project/reporting/pull/651))


### OpenSearch Security Analytics Dashboards
* Resolving json5 to latest version. ([#478](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/478))


### OpenSearch Security
* Add auto github release workflow ([#2450](https://github.com/opensearch-project/security/pull/2450))
* Use correct format for push trigger ([#2474](https://github.com/opensearch-project/security/pull/2474))


### OpenSearch Security Dashboards Plugin
* Add auto-release workflow ([#1339](https://github.com/opensearch-project/security-dashboards-plugin/pull/1339))


## DOCUMENTATION

### OpenSearch Alerting
* Added 2.7 release notes. ([#864](https://github.com/opensearch-project/alerting/pull/864))


### OpenSearch Alerting Dashboards
* Added 2.7 release notes. ([#530](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/530))


### OpenSearch Common Utils
* Added 2.7 release notes. ([#407](https://github.com/opensearch-project/common-utils/pull/407))


### OpenSearch Dashboards Notifications
* Drafted 2.7 release notes. ([#34](https://github.com/opensearch-project/dashboards-notifications/pull/34))


### OpenSearch Index Management
* Added 2.7 release notes. ([#755](https://github.com/opensearch-project/index-management/pull/755))


### OpenSearch Index Management Dashboards Plugin
* 2.7 release note ([#694](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/694))


### OpenSearch Ml Commons
* Add docker-compose file for starting cluster with dedicated ML node ([#799](https://github.com/opensearch-project/ml-commons/pull/799))


### OpenSearch Notifications
* Add 2.7.0 release notes ([#652](https://github.com/opensearch-project/notifications/pull/652))


### OpenSearch Security Analytics
* Added 2.7 release notes. ([#]())


### OpenSearch Security Analytics Dashboards
* Added 2.7 release notes. ([#523](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/523))


### OpenSearch Security
* Fix the format of the codeowners file ([#2469](https://github.com/opensearch-project/security/pull/2469))


### OpenSearch SQL
* Documentation and other papercuts for datasource api launch ([#1534](https://github.com/opensearch-project/sql/pull/1534))


## MAINTENANCE

### OpenSearch Alerting
* Increment version to 2.7. ([#823](https://github.com/opensearch-project/alerting/pull/823))


### OpenSearch Alerting Dashboards
* Bumped version to 2.7. ([#505](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/505))


### OpenSearch Asynchronous Search
* Fix maven and update 2.7.0 zip ([268](https://github.com/opensearch-project/asynchronous-search/pull/268))
* Publish snapshot to maven ([252](https://github.com/opensearch-project/asynchronous-search/pull/252))


### OpenSearch Common Utils
* Increment version to 2.7.0-SNAPSHOT. ([#371](https://github.com/opensearch-project/common-utils/pull/371))


### OpenSearch Dashboards Maps
* Bump to 2.7.0 version ([#356](https://github.com/opensearch-project/dashboards-maps/pull/356))


### OpenSearch Dashboards Notifications
* Bump version to 2.7. ([#28](https://github.com/opensearch-project/dashboards-notifications/pull/28))


### OpenSearch Dashboards Reporting
* Bump version 2.7.0 ([#75](https://github.com/opensearch-project/dashboards-reporting/pull/75))


### OpenSearch Dashboards Search Relevance
* New Maintainers - Sean Li and Louis Chu ([#172](https://github.com/opensearch-project/dashboards-search-relevance/pull/172))


### OpenSearch Dashboards Visualizations
* Added untriaged issue workflow ([#164](https://github.com/opensearch-project/dashboards-visualizations/pull/164)) 


### OpenSearch Index Management
* Bump mockito version. ([#701](https://github.com/opensearch-project/index-management/pull/701))
* Bump version to 2.7. ([#743](https://github.com/opensearch-project/index-management/pull/743))


### OpenSearch Index Management Dashboards Plugin
* Bumped version to 2.7. ([#695](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/695))


### OpenSearch Job Scheduler
* Update to Gradle 8.0.2 ([#348](https://github.com/opensearch-project/job-scheduler/pull/348))


### OpenSearch Ml Commons
* Increment version to 2.7.0-SNAPSHOT ([#742](https://github.com/opensearch-project/ml-commons/pull/742))
* Publish snapshots to maven via GHA ([#754](https://github.com/opensearch-project/ml-commons/pull/754))


### OpenSearch Notifications
* [AUTO] Increment version to 2.7.0-SNAPSHOT ([#636](https://github.com/opensearch-project/notifications/pull/636))


### OpenSearch Observability
* Bump snakeyaml version ([#1465](https://github.com/opensearch-project/observability/pull/1465))


### OpenSearch Performance Analyzer
* Modify namespace from xcontent common to core ([#410](https://github.com/opensearch-project/performance-analyzer/pull/410))


### OpenSearch Query Workbench
* Baseline repo groups ([#52](https://github.com/opensearch-project/dashboards-query-workbench/pull/52))


### OpenSearch Reporting
* Increment version to 2.7.0-SNAPSHOT ([#657](https://github.com/opensearch-project/reporting/pull/657))
* Bump snakeyaml to 2.0 ([#674](https://github.com/opensearch-project/reporting/pull/674))


### OpenSearch Security Analytics
* Bumped version to 2.7. ([#387](https://github.com/opensearch-project/security-analytics/pull/387))


### OpenSearch Security Analytics Dashboards
* Bumped version to 2.7. ([#508](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/508))


### OpenSearch Security
* Update kafka client to 3.4.0 ([#2484](https://github.com/opensearch-project/security/pull/2484))
* Update to gradle 8.0.2 ([#2520](https://github.com/opensearch-project/security/pull/2520))
* XContent Refactor ([#2598](https://github.com/opensearch-project/security/pull/2598))
* Update json-smart to 2.4.10 and update spring-core to 5.3.26 ([#2630](https://github.com/opensearch-project/security/pull/2630))
* Update certs for SecuritySSLReloadCertsActionTests ([#2679](https://github.com/opensearch-project/security/pull/2679))


### OpenSearch SQL
* Refactor AWSSigV4 auth to support different AWSCredentialProviders ([#1389](https://github.com/opensearch-project/sql/pull/1389))
* [AUTO] Increment version to 2.7.0-SNAPSHOT ([#1368](https://github.com/opensearch-project/sql/pull/1368))
* Update usage of Strings.toString ([#1404](https://github.com/opensearch-project/sql/pull/1404))
* Deprecated Spring IoC and using Guice instead (#1177) ([#1410](https://github.com/opensearch-project/sql/pull/1410))
* Bump backport version. ([#1009](https://github.com/opensearch-project/sql/pull/1009))
* Resolve table function based on StorageEngine provided function resolver ([#1424](https://github.com/opensearch-project/sql/pull/1424))
* Rework on `OpenSearchDataType`: parse, store and use mapping information ([#1455](https://github.com/opensearch-project/sql/pull/1455))
* Update to account for XContent refactor in 2.x ([#1485](https://github.com/opensearch-project/sql/pull/1485))
* Replace non-ASCII characters in code and docs. ([#1486](https://github.com/opensearch-project/sql/pull/1486))
* Add publish snapshots to maven via GHA ([#1496](https://github.com/opensearch-project/sql/pull/1496))
* Refactoring datasource changes to a new module. ([#1511](https://github.com/opensearch-project/sql/pull/1511))
* #639: Allow metadata fields and score opensearch function  (#228) ([#1509](https://github.com/opensearch-project/sql/pull/1509))


## REFACTORING

### OpenSearch Alerting
* Revert enabled field in source_to_query_index_mapping. ([#812](https://github.com/opensearch-project/alerting/pull/812))
* Fixed xContent dependencies due to OSCore changes. ([#839](https://github.com/opensearch-project/alerting/pull/839))
* Update config index schema if needed at the start of each monitor execution. ([#849](https://github.com/opensearch-project/alerting/pull/849))


### OpenSearch Common Utils
* Fixed xContent dependencies due to OSCore changes. ([#392](https://github.com/opensearch-project/common-utils/pull/392))


### OpenSearch Dashboards Maps
* Move zoom and coordinates as separate component ([#309](https://github.com/opensearch-project/dashboards-maps/pull/309))
* Move coordinates to footer ([#315](https://github.com/opensearch-project/dashboards-maps/pull/315))
* Refactor tooltip setup as component ([#320](https://github.com/opensearch-project/dashboards-maps/pull/320))
* Refactor get field options and add field label option on UI ([#328](https://github.com/opensearch-project/dashboards-maps/pull/328))


### OpenSearch Index Management
* Replace Set in org.opensearch.common.collect with java.util references. ([#717](https://github.com/opensearch-project/index-management/pull/717))
* Fixed xContent dependencies due to OSCore changes. ([#721](https://github.com/opensearch-project/index-management/pull/721))


### OpenSearch Index Management Dashboards Plugin
* Refractor e2e test to be the same structure as FTRepo ([#663](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/663))


### OpenSearch k-NN
* Replace Map, List, and Set in org.opensearch.common.collect with java.util references ([#816](https://github.com/opensearch-project/k-NN/pull/816))


### OpenSearch Ml Commons
* Rename API/function/variable names ([#822](https://github.com/opensearch-project/ml-commons/pull/822))
* Rename model meta/chunk API ([#827](https://github.com/opensearch-project/ml-commons/pull/827))


### OpenSearch Security Analytics
* Index template cleanup. ([#317](https://github.com/opensearch-project/security-analytics/pull/317))
* Handle monitor or monitor index not found during detector deletion. ([#384](https://github.com/opensearch-project/security-analytics/pull/384))
* Handle index not exists for detector search and delete. ([#396](https://github.com/opensearch-project/security-analytics/pull/396))


### OpenSearch Security Analytics Dashboards
* Show required field mappings only for enabled rules. ([#418](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/418))
* Fix reduced margin in Get started popup. ([#466](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/466))
* Empty states for Overview page. ([#467](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/467))
* Common data store for the rules. ([#474](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/474))
* Communicate to users when the detector is initializing. ([#487](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/487))
* Create global state object for async requests. ([#493](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/493))
* Provide empty states for Findings and Alerts page. ([#494](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/494))
* Refactor and move field mapping to first the page of create detector feature. ([#501](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/501))
* Create detector refactor alert triggers per mocks. ([#503](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/503))
* Update detector details component. ([#504](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/504))
* Deleting detectors should delete all related dashboards (including index patterns and visualisations). ([#515](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/515))


