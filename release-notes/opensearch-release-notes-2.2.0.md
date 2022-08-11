# OpenSearch and Dashboards 2.2.0 Release Notes

## Release Highlights
* OpenSearch 2.2.0 supports [logistic regression](https://github.com/opensearch-project/ml-commons/issues/318) and [RCFSummarize](https://github.com/opensearch-project/ml-commons/issues/356) machine learning algorithms.
* With the [addition of the Lucene implementation](https://github.com/opensearch-project/k-NN/issues/380) of the HNSW algorithm, you can now choose from Lucene or the C-based Nmslib and Faiss libraries for approximate k-NN search.
* You can now [search by relevance](https://github.com/opensearch-project/sql/issues/182) using SQL and PPL queries including [match_phrase_prefix](https://github.com/opensearch-project/sql/pull/661), [query_string](https://github.com/opensearch-project/sql/pull/675), and [highlight](https://github.com/opensearch-project/sql/pull/717).
* You can now [upload your own custom region maps](https://github.com/opensearch-project/geospatial/issues/122) in GeoJSON format and use them for visualizations in OpenSearch Dashboards. You can also draw your own geographic boundaries on a visualization.
* Several [rollup enhancements](https://github.com/opensearch-project/index-management/issues/408) allow you to roll up aggregated results from older data to dynamic target indexes and run one search query across multiple indexes.
* You can now view [feature attribution and expected value](https://github.com/opensearch-project/anomaly-detection/issues/299) on the anomaly detection details page.


## Release Details

OpenSearch and OpenSearch Dashboards 2.2.0 includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance, and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-2.2.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-2.2.0.md).

## FEATURES

### OpenSearch Dashboards Maps
* Remove plugin check logic and support offline working of importing custom geoJSON([#10](https://github.com/opensearch-project/dashboards-maps/pull/10))
* Add error modal and lint fixes([#13](https://github.com/opensearch-project/dashboards-maps/pull/13))
* Introduce refresh option to update the custom vector map list ([#14](https://github.com/opensearch-project/dashboards-maps/pull/14))
* Add OpenSearch Dashboards context to component and common folder changes ([#34](https://github.com/opensearch-project/dashboards-maps/pull/34))


### OpenSearch Geospatial
* Add feature processor to convert geo-json feature to geo-shape field ([#15](https://github.com/opensearch-project/geospatial/pull/15))
* Add rest handler for geo-json upload ([#25](https://github.com/opensearch-project/geospatial/pull/25))
* Create UploadGeoJSONRequest content as an object ([#32](https://github.com/opensearch-project/geospatial/pull/32))
* Add GeoJSON object of type FeatureCollection ([#33](https://github.com/opensearch-project/geospatial/pull/33))
* Include new route to support update index while upload ([#34](https://github.com/opensearch-project/geospatial/pull/34))
* Add uploader to upload user input ([#35](https://github.com/opensearch-project/geospatial/pull/35))
* Make field name as optional ([#37](https://github.com/opensearch-project/geospatial/pull/37))
* Use BulkResponse build error message ([#46](https://github.com/opensearch-project/geospatial/pull/46))
* Update upload API response structure ([#51](https://github.com/opensearch-project/geospatial/pull/51))
* Add metric and stat entity ([#54](https://github.com/opensearch-project/geospatial/pull/54))
* Create Upload Stats Service to build response for stats API ([#62](https://github.com/opensearch-project/geospatial/pull/62))
* Include stats api to provide upload metrics ([#64](https://github.com/opensearch-project/geospatial/pull/64))


### OpenSearch Index Management
* Ability to count the number of documents from source index ([#439](https://github.com/opensearch-project/index-management/pull/439)) and ([#3985](https://github.com/opensearch-project/OpenSearch/pull/3985))


### OpenSearch k-NN
* Lucene Based k-NN search support([#486](https://github.com/opensearch-project/k-NN/pull/486))


### OpenSearch ML Commons
* Add clustering function - RCFSummarize ([#355](https://github.com/opensearch-project/ml-commons/pull/355))
* Add Logistic Regression algorithm ([#383](https://github.com/opensearch-project/ml-commons/pull/383))


### OpenSearch SQL
* Add match_phrase_prefix ([#661](https://github.com/opensearch-project/sql/pull/661))
* `query_string` Relevance Function Implementation in SQL and PPL ([#675](https://github.com/opensearch-project/sql/pull/675))
* Add Highlight In SQL ([#717](https://github.com/opensearch-project/sql/pull/717))


## ENHANCEMENTS

### OpenSearch Anomaly Detection
* Make 1M1min possible ([#620](https://github.com/opensearch-project/anomaly-detection/pull/620))


### OpenSearch Anomaly Detection Dashboards
* Add feature attribution ([#296](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/296))


### OpenSearch Index Management
* Support mustache scripting of rollup.target_index field ([#435](https://github.com/opensearch-project/index-management/pull/435))
* Support searching multiple rollup indices with same mapping ([#440](https://github.com/opensearch-project/index-management/pull/440))


### OpenSearch k-NN
* Add KNN codec that is based on Lucene92 codec([#444](https://github.com/opensearch-project/k-NN/pull/444))
* Remove support for innerproduct for lucene engine([#488](https://github.com/opensearch-project/k-NN/pull/488))
* Increase max dimension to 16k for nmslib and faiss([#490](https://github.com/opensearch-project/k-NN/pull/490))


### OpenSearch Notifications
* Adding K8s service name as webhook destination ([#455](https://github.com/opensearch-project/notifications/pull/455))

### OpenSearch Security
* Adds a basic sanity test to run against a remote cluster ([#1958](https://github.com/opensearch-project/security/pull/1958))
* Create a manually started workflow for bulk run of integration tests ([#1937](https://github.com/opensearch-project/security/pull/1937))

### OpenSearch SQL
* Implement transport api for PPL inter-plugin communication ([#533](https://github.com/opensearch-project/sql/pull/533))
* Two single or double quote escapes single or double quote when string is surrounded by same type of quote ([#696](https://github.com/opensearch-project/sql/pull/696))


## BUG FIX

### OpenSearch Cross Cluster Replication
* Adding Index Settings validation before starting replication ([#461](https://github.com/opensearch-project/cross-cluster-replication/pull/461))

### OpenSearch k-NN
* Reject delete model request if model is in Training([#424](https://github.com/opensearch-project/k-NN/pull/424))
* Change call to Lucene VectorSimilarityFunction.convertToScore([#487](https://github.com/opensearch-project/k-NN/pull/487))

### OpenSearch ML Commons
* Fix jackson databind version: use same version as OpenSearch core ([#376](https://github.com/opensearch-project/ml-commons/pull/376))
* Fix index mapping ([#384](https://github.com/opensearch-project/ml-commons/pull/384))
* Increase the default epochs to 1000 for linear regression ([#394](https://github.com/opensearch-project/ml-commons/pull/394))

### OpenSearch Notifications
* Add security tests and workflow plus minor fix ([#470](https://github.com/opensearch-project/notifications/pull/470))
* Resolve hosts when checking against host deny list ([#496](https://github.com/opensearch-project/notifications/pull/496))

### OpenSearch Security
* Use Collections.synchronizedSet and Collections.synchronizedMap for roles, securityRoles and attributes in User ([#1970](https://github.com/opensearch-project/security/pull/1970))

### OpenSearch Security Dashboards Plugin
* Fix bug in SAML support after renaming ([#895](https://github.com/opensearch-project/security-dashboards-plugin/pull/895))" ([#1035](https://github.com/opensearch-project/security-dashboards-plugin/pull/1035))
* Fix bug in support for jwt.url_param customization ([#1025](https://github.com/opensearch-project/security-dashboards-plugin/pull/1025))
* Get security_tenant search param from URL ([#1024](https://github.com/opensearch-project/security-dashboards-plugin/pull/1024))
* Preserve URL Hash for SAML based login ([#1039](https://github.com/opensearch-project/security-dashboards-plugin/pull/1039))

### OpenSearch SQL
* Reverted UseSSL flag to false and removed invalid test case  ([#671](https://github.com/opensearch-project/sql/pull/671))
* Update BI connectors and drivers readme files ([#665](https://github.com/opensearch-project/sql/pull/665))
* Bump moment from 2.29.2 to 2.29.4 in /workbench ([#702](https://github.com/opensearch-project/sql/pull/702))


## INFRASTRUCTURE

### OpenSearch Alerting
* Add support for reproducible builds. ([#472](https://github.com/opensearch-project/alerting/pull/472))


### OpenSearch Anomaly Detection
* Fix zip fetching issue on version increment ([#611](https://github.com/opensearch-project/anomaly-detection/pull/611))
* Staging for version increment automation ([#608](https://github.com/opensearch-project/anomaly-detection/pull/608))
* Update BWC zip links ([#625](https://github.com/opensearch-project/anomaly-detection/pull/625))


### OpenSearch Anomaly Detection Dashboards
* Bump to 2.2 ([#293](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/293))


### OpenSearch Common Utils
* Execute version auto increment in staging ([#200](https://github.com/opensearch-project/common-utils/pull/200))
* Bump up the version to 2.2. ([#204](https://github.com/opensearch-project/common-utils/pull/204))


### OpenSearch Cross Cluster Replication
* Use the published zip for security plugin ([#455](https://github.com/opensearch-project/cross-cluster-replication/pull/455))


### OpenSearch Dashboards Maps
* Add basic template files related to OpenSearch guidelines([#2](https://github.com/opensearch-project/dashboards-maps/pull/2))
* Add GitHub workflow for running unit tests([#6](https://github.com/opensearch-project/dashboards-maps/pull/6))
* Add badges to README([#9](https://github.com/opensearch-project/dashboards-maps/pull/9))
* Add developer guide and easy setup([#12](https://github.com/opensearch-project/dashboards-maps/pull/12))
* Add changes for releasing plugin with OSD as part of 2.2 release([#20](https://github.com/opensearch-project/dashboards-maps/pull/20))


### OpenSearch Geospatial
* Create plugin using plugin template ([#3](https://github.com/opensearch-project/geospatial/pull/3))
* Add formatter config from OpenSearch ([#21](https://github.com/opensearch-project/geospatial/pull/21))
* Adding JDK 11 to CI matrix ([#31](https://github.com/opensearch-project/geospatial/pull/31))
* Add support to run integration tests with multiple nodes ([#57](https://github.com/opensearch-project/geospatial/pull/57))


### OpenSearch k-NN
* Add fix to flaky test in ModelDaoTests([#463](https://github.com/opensearch-project/k-NN/pull/463))
* Read BWC Version from GitHub workflow([#476](https://github.com/opensearch-project/k-NN/pull/476))
* Staging for version increment automation([#442](https://github.com/opensearch-project/k-NN/pull/442))
* Remove 1.0.0 for BWC test([#492](https://github.com/opensearch-project/k-NN/pull/492))


### OpenSearch Notifications
* Add backwards compatibility tests ([#475](https://github.com/opensearch-project/notifications/pull/475))
* Add tasks to publish zips for Notifications and Notifications Core plugins ([#484](https://github.com/opensearch-project/notifications/pull/484))
* Run Cypress tests as part of Notifications Dashboards GitHub Action workflow ([#483](https://github.com/opensearch-project/notifications/pull/483))
* Staging for version increment automation ([#476](https://github.com/opensearch-project/notifications/pull/476))


### OpenSearch SQL
* Staging for version increment automation ([#684](https://github.com/opensearch-project/sql/pull/684))
* Update tests and test data for relevancy search functions ([#707](https://github.com/opensearch-project/sql/pull/707))
* Remove ODFE BWC tests ([#721](https://github.com/opensearch-project/sql/pull/721))
* Github Actions fix for reference to OpenSearch-Dashboard not existing outside of main OS sql project ([#704](https://github.com/opensearch-project/sql/pull/704))


## DOCUMENTATION

### OpenSearch Alerting
* Added 2.2 release notes. ([#514](https://github.com/opensearch-project/alerting/pull/514))


### OpenSearch Alerting Dashboards Plugin
* Added 2.2 release notes. ([#302](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/302))


### OpenSearch Asynchronous Search
* Added 2.2 release notes. ([#164](https://github.com/opensearch-project/asynchronous-search/pull/164))


### OpenSearch Common Utils
* Added 2.2 release notes. ([#212](https://github.com/opensearch-project/common-utils/pull/212))


### OpenSearch Index Management Dashboards Plugin
* Updated rollup help text. ([#220](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/220))
* Added to 2.2 release notes. ([#222](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/222))


### OpenSearch Job Scheduler
* Added 2.2 release notes. ([#217](https://github.com/opensearch-project/job-scheduler/pull/217))


### OpenSearch ML Commons
* Remove comment which is not applicable now ([#369](https://github.com/opensearch-project/ml-commons/pull/369))


### OpenSearch SQL
* Update support link for Tableau connector ([#643](https://github.com/opensearch-project/sql/pull/643))
* Fix broken forum link ([#694](https://github.com/opensearch-project/sql/pull/694))
* Fix links in the doc file. ([#705](https://github.com/opensearch-project/sql/pull/705))


## MAINTENANCE

### OpenSearch Alerting
* Staging for version increment automation. ([#489](https://github.com/opensearch-project/alerting/pull/489))
* Bumping 2.x branch version from 2.1.0 to 2.2.0. ([#506](https://github.com/opensearch-project/alerting/pull/506))
* Refactored backwards compatibility tests to point to the OpenSearch 1.1.0.0 zip following deprecation of ODFE. ([#510](https://github.com/opensearch-project/alerting/pull/510))


### OpenSearch Alerting Dashboards Plugin
* Bumping 2.x branch from version 2.1 to 2.2. Bumped terser version to 4.8.1 to address CVE. ([#301](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/301)))


### OpenSearch Anomaly Detection
* Bump version to 2.2 ([#627](https://github.com/opensearch-project/anomaly-detection/pull/627))


### OpenSearch Asynchronous Search
* Bump version to 2.2.0 ([#163](https://github.com/opensearch-project/asynchronous-search/pull/163))
* Changed BWC tests to use 1.1.0 plugin version ([#162](https://github.com/opensearch-project/asynchronous-search/pull/162))


### OpenSearch Dashboards Maps
* Add version changes required for 2.2.0 release([#18](https://github.com/opensearch-project/dashboards-maps/pull/18))


### OpenSearch Dashboards Reports
* Bump version to 2.0.0 ([#412](https://github.com/opensearch-project/dashboards-reports/pull/412))


### OpenSearch Dashboards Visualizations
* Version bump to 2.2.0 ([#102](https://github.com/opensearch-project/dashboards-visualizations/pull/102))


### OpenSearch Geospatial
* Update OpenSearch upstream version to 2.2.0([#87](https://github.com/opensearch-project/geospatial/pull/87))


### OpenSearch Index Management
* Version upgrade to 2.2.0 ([#446](https://github.com/opensearch-project/index-management/pull/446))


### OpenSearch Index Management Dashboards Plugin
* Bumping 2.x branch from version 2.1 to 2.2. ([#218](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/218))


### OpenSearch Job Scheduler
* Bump version to 2.2.0 ([#215](https://github.com/opensearch-project/job-scheduler/pull/215))


### OpenSearch k-NN
* Bump OpenSearch version to 2.2.0([#471](https://github.com/opensearch-project/k-NN/pull/471))
* Bump Gradle version to 7.5([#472](https://github.com/opensearch-project/k-NN/pull/472))
* Bump default bwc version to 1.3.4([#477](https://github.com/opensearch-project/k-NN/pull/477))


### OpenSearch ML Commons
* Staging for version increment automation ([#362](https://github.com/opensearch-project/ml-commons/pull/362))
* Bump to 2.2 ([#387](https://github.com/opensearch-project/ml-commons/pull/387))


### OpenSearch Notifications
* Favor using OpenSearch's versions for httpclient and httpcore ([#477](https://github.com/opensearch-project/notifications/pull/477))
* Bump to version 2.2.0 ([#493](https://github.com/opensearch-project/notifications/pull/493))


### OpenSearch Observability
* Bump version to 2.2.0 ([#918](https://github.com/opensearch-project/observability/pull/918))


### OpenSearch Performance Analyzer
* Update version to 2.2 ([#200](https://github.com/opensearch-project/performance-analyzer-rca/pull/200))
* Fixing ODFE BWC links and upgrade to 2.2 ([#243](https://github.com/opensearch-project/performance-analyzer/pull/243))


### OpenSearch Security
* Update to Gradle 7.5 ([#1963](https://github.com/opensearch-project/security/pull/1963))
* Increment version to 2.2.0.0 ([#1948](https://github.com/opensearch-project/security/pull/1948))
* Force netty-transport-native-unix-common version ([#1945](https://github.com/opensearch-project/security/pull/1945))
* Add release notes for 2.2.0.0 release ([#1974](https://github.com/opensearch-project/security/pull/1974))
* Staging for version increment automation ([#1932](https://github.com/opensearch-project/security/pull/1932))
* Fix breaking API change introduced in Lucene 9.3.0 ([#1988](https://github.com/opensearch-project/security/pull/1988))
* Update indices resolution to be clearer ([#1999](https://github.com/opensearch-project/security/pull/1999))


### OpenSearch Security Dashboards Plugin
* Updates Dev guide ([#897](https://github.com/opensearch-project/security-dashboards-plugin/pull/897))
* Add tests for account-nav-button when multitenancy is disabled ([#1020](https://github.com/opensearch-project/security-dashboards-plugin/pull/1020))
* Increment version to 2.2.0.0 ([#1032](https://github.com/opensearch-project/security-dashboards-plugin/pull/1032))
* Add release notes for 2.2.0.0 release ([#1050](https://github.com/opensearch-project/security-dashboards-plugin/pull/1050))


### OpenSearch SQL
* Change version bump under maintenance ([#679](https://github.com/opensearch-project/sql/pull/679))
* Bump version to 2.2.0 ([#729](https://github.com/opensearch-project/sql/pull/729))


## REFACTORING

### OpenSearch Security
* Abstract waitForInit to minimize duplication and improve test reliability ([#1935](https://github.com/opensearch-project/security/pull/1935))

### OpenSearch k-NN
* Move engine and lib components into separate files([#438](https://github.com/opensearch-project/k-NN/pull/438))
* Refactor knn type and codecs([#439](https://github.com/opensearch-project/k-NN/pull/439))
* Move mappers to separate files([#448](https://github.com/opensearch-project/k-NN/pull/448))

