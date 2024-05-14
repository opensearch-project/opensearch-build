# OpenSearch and OpenSearch Dashboards 2.14.0 Release Notes

## Release Highlights

OpenSearch 2.14.0 introduces a host of new and updated features designed to increase performance, improve usability, expand access to data sources, and help users build better search and machine learning (ML) applications.


### New Features

* Updates to OpenSearch’s hybrid search functionality, which combines neural search with lexical search to provide higher-quality results than when using either technique alone, offer performance increases of up to 4x.
* Multi-range traversal adds performance improvements for date histogram queries without sub-aggregations. Improvements should be significant for time-series data analysis use cases, where date histograms are critical. This optimization also addresses a performance regression noted in the PMC benchmark for these queries.
* Expanded multiple data sources functionality is extended to nine external Dashboards plugins: Index Management, ML Commons, Search Relevance, Anomaly Detection, Maps, Security, Notifications, Trace Analytics, and Query Workbench. Multiple data sources are also enabled for two core plugins: Region Map and the time series visual builder, delivering further progress toward a unified user experience for OpenSearch Dashboards.
* API-native ingest joins the OpenSearch machine learning (ML) toolkit. This allows you to integrate any ML model and use models to enrich data streams through the Ingest API, so you can easily transition between model providers and build applications more quickly. A new ML inference processor allows you to perform inferences on any integrated ML model to enrich your pipeline.
* A new semantic cache for LangChain applications lets you use k-NN indexes to cache large language model (LLM) requests and responses. This semantic cache functionality can reduce the number of calls made to LLMs for similar requests and responses.
* A new lower-level vector query interface expands neural sparse functionality, allowing you to run a neural sparse query by providing a sparse vector, a list of weighted tokens, as inputs. This adds an optional interface for building semantic search applications when using semantic sparse encoders.
* An update to the k-NN query interface lets you retrieve only results within a certain maximum distance or vector score threshold. This is particularly well suited for uses cases in which the goal is to retrieve all the results that are highly or sufficiently similar; for example, >= 0.95.
* A search pipelines enhancement allows you to use a single search pipeline as a default for multiple indexes and aliases. This gives you the option to use search pipelines with the benefits of index aliases for improved reusability.
* A new k-NN Clear Cache API lets you clear k-NN indexes from the cache without the need to delete the index or manually set the k-NN cluster settings knn.cache.item.expiry.enabled and knn.cache.item.expiry.minutes.
* An update to the OpenSearch RPM package expands the scope of the configuration files to include all files within the /etc/opensearch directory, helping ensure that plugin-specific configurations are preserved during upgrades.
* Please note that a new PGP public key is available for artifact verification. OpenSearch’s current PGP public key is scheduled to expire on May 12, 2024. Please visit https://opensearch.org/verify-signatures.html to download the new public key, which is scheduled to expire on May 12, 2025.


### Experimental Features

OpenSearch 2.14.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.

* This release introduces experimental support for tiered caching within the request cache. This enables caching of much larger datasets, helping to avoid cache evictions and misses due to limited available memory on a node. The tiered cache framework consists of multiple levels, each with its own size and performance characteristics. Evicted items from upper, faster tiers, such as the on-heap cache, are moved to lower, slower tiers, like the disk cache, which affords greater storage capacity but higher latency.
* This release includes an experimental update to OpenSearch’s remote storage and document replication capabilities. This functionality will allow you to migrate existing indexes with document replication enabled to remote-backed storage clusters.
* Experimental support for cluster-level dynamic application configuration offers users a secure and flexible set of tools for controlling more cluster settings, such as Content Security Policy (CSP) rules, to help assure a good user experience while maintaining security standards.


## Release Details
[OpenSearch and OpenSearch Dashboards 2.14.0](https://opensearch.org/versions/opensearch-2-14-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.14/release-notes/opensearch.release-notes-2.14.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.14/release-notes/opensearch-dashboards.release-notes-2.14.0.md).


## FEATURES


### Dashboards Observability


* Add skipping index and saved queries for WAF integration ([#1750](https://github.com/opensearch-project/dashboards-observability/pull/1750))
* Add multi-checkpoint support to integrations ([#1742](https://github.com/opensearch-project/dashboards-observability/pull/1742))
* Enhance Explorer to use describe command ([#1736](https://github.com/opensearch-project/dashboards-observability/pull/1736))
* Update vpc flow with flint-s3 based DDL assets and dashboard ([#1721](https://github.com/opensearch-project/dashboards-observability/pull/1721))
* Add default refresh interval for all the integrations and correct the version on `main` ([#1717](https://github.com/opensearch-project/dashboards-observability/pull/1717))
* More example queries for S3-based integrations ([#1714](https://github.com/opensearch-project/dashboards-observability/pull/1714))
* Implement saved query substitution for S3 integrations ([#1711](https://github.com/opensearch-project/dashboards-observability/pull/1711))
* Update cloud trail integration with flint-s3 based DDL assets and das… ([#1707](https://github.com/opensearch-project/dashboards-observability/pull/1707))
* [Integrations] Add integration of S3 Access log ([#1697](https://github.com/opensearch-project/dashboards-observability/pull/1697))
* Update pattern for multiple mview suffixes ([#1693](https://github.com/opensearch-project/dashboards-observability/pull/1693))
* HAProxy Flint Integration ([#1692](https://github.com/opensearch-project/dashboards-observability/pull/1692))
* Add CloudFront queries for integrations and integration table bug fix ([#1687](https://github.com/opensearch-project/dashboards-observability/pull/1687))
* Add integration of WAF log ([#1685](https://github.com/opensearch-project/dashboards-observability/pull/1685))
* Improve on ELB integration assets ([#1682](https://github.com/opensearch-project/dashboards-observability/pull/1682))
* Add Flint queries for Apache Access integration ([#1681](https://github.com/opensearch-project/dashboards-observability/pull/1681))
* Add observability-search link rendering for integrations ([#1642](https://github.com/opensearch-project/dashboards-observability/pull/1642))
* Flint Datasource Cypress testing for tables ([#1610](https://github.com/opensearch-project/dashboards-observability/pull/1610))
* Update loading state for tables fields in create acceleration flyout ([#1576](https://github.com/opensearch-project/dashboards-observability/pull/1576))
* Add info callout for s3 datasources ([#1575](https://github.com/opensearch-project/dashboards-observability/pull/1575))
* Flint datasource 2.13 bug bash fix ([#1574](https://github.com/opensearch-project/dashboards-observability/pull/1574))
* Fixed small bugs in explorer ([#1559](https://github.com/opensearch-project/dashboards-observability/pull/1559))


### Opensearch Dashboards Maps


* Support multi data source display in Maps app([#611](https://github.com/opensearch-project/dashboards-maps/pull/611))
* Support multi data source in Region map ([#614](https://github.com/opensearch-project/dashboards-maps/pull/614))


### Opensearch Dashboards Search Relevance


* Multi-datasource support for Search-relevance ([#383](https://github.com/opensearch-project/dashboards-search-relevance/pull/383)) ([#387](https://github.com/opensearch-project/dashboards-search-relevance/pull/387))


### Opensearch ML Commons


* Initiate MLInferencelngestProcessor ([#2205](https://github.com/opensearch-project/ml-commons/pull/2205))
* Add TTL to un-deploy model automatically ([#2365](https://github.com/opensearch-project/ml-commons/pull/2365))
* ML Model Interface ([#2357](https://github.com/opensearch-project/ml-commons/pull/2357))


### Opensearch ML Commons Dashboards


* Add multi data source support ([#315](https://github.com/opensearch-project/ml-commons-dashboards/pull/315))
* Add model id column to deployed models list ([#318](https://github.com/opensearch-project/ml-commons-dashboards/pull/318))


### Opensearch Neural Search


* Support k-NN radial search parameters in neural search ([#697](https://github.com/opensearch-project/neural-search/pull/697))


### Opensearch Query Workbench


* Multi datasource support ([#311](https://github.com/opensearch-project/dashboards-query-workbench/pull/311))


### Opensearch Reporting


* Tenancy access control ([#992](https://github.com/opensearch-project/reporting/pull/992))


### Opensearch Security Analytics


* Add latest sigma rules ([#942](https://github.com/opensearch-project/security-analytics/pull/942))


### Opensearch Skills


* Fix filter fields, adding geo point and date\_nanos ([#285](https://github.com/opensearch-project/skills/pull/285)) ([#286](https://github.com/opensearch-project/skills/pull/286))
* Change ad plugin jar dependency ([#288](https://github.com/opensearch-project/skills/pull/288))
* Remove logic about replace quota for finetuning model ([#289](https://github.com/opensearch-project/skills/pull/289)) ([#291](https://github.com/opensearch-project/skills/pull/291))
* Move search index tool to ml-commons repo ([#297](https://github.com/opensearch-project/skills/pull/297))
* Move visualization tool to ml-commons ([#296](https://github.com/opensearch-project/skills/pull/296)) ([#298](https://github.com/opensearch-project/skills/pull/298))


### Opensearch k-NN


* Add k-NN clear cache api ([#740](https://github.com/opensearch-project/k-NN/pull/740))
* Support radial search in k-NN plugin ([#1617](https://github.com/opensearch-project/k-NN/pull/1617))
* Support filter and nested field in faiss engine radial search ([#1652](https://github.com/opensearch-project/k-NN/pull/1652))


## ENHANCEMENTS


### Opensearch Alerting


* Adding tracking\_total\_hits in search query for findings. ([#1487](https://github.com/opensearch-project/alerting/pull/1487))


### Opensearch Anomaly Detection Dashboards


* Support MDS on List, Detail, Dashboard, Overview pages ([#722](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/722))


### Opensearch Cross Cluster Replication


* Support for fetching changes from Lucene store during remote store migration ([#1369](https://github.com/opensearch-project/cross-cluster-replication/pull/1369))


### Opensearch Dashboards Notifications

* Added Multidata Source Support ([#197](https://github.com/opensearch-project/dashboards-notifications/pull/197))
* Moved enrichment of server features to server side ([#181](https://github.com/opensearch-project/dashboards-notifications/pull/181)) ([#194](https://github.com/opensearch-project/dashboards-notifications/pull/194))


### Opensearch Flow Framework


* Add guardrails to default use case params ([#658](https://github.com/opensearch-project/flow-framework/pull/658))
* Allow strings for boolean workflow step parameters ([#671](https://github.com/opensearch-project/flow-framework/pull/671))
* Add optional delay parameter to no-op step ([#674](https://github.com/opensearch-project/flow-framework/pull/674))
* Add model interface support for remote and local custom models ([#701](https://github.com/opensearch-project/flow-framework/pull/701))


### Opensearch Index Management Dashboards Plugin


* Add MDS support for policies, policy managed indices, rollup jobs and transform jobs ([#1021](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1021))
* Interface change for MDS support and deprecating dataSourceLabel from the URL ([#1031](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1031))
* Mount MDS on the empty route ([#1039](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1039))


### Opensearch ML Commons


* Change httpclient to async ([#1958](https://github.com/opensearch-project/ml-commons/pull/1958))
* Migrate RAG pipeline to async processing. ([#2345](https://github.com/opensearch-project/ml-commons/pull/2345))
* Filtering hidden model info from model profiling for users other than superadmin ([#2332](https://github.com/opensearch-project/ml-commons/pull/2332))
* Check model auto deploy ([#2288](https://github.com/opensearch-project/ml-commons/pull/2288))
* Restrict stash context only for stop words system index ([#2283](https://github.com/opensearch-project/ml-commons/pull/2283))
* Add a flag to control auto-deploy behavior ([#2276](https://github.com/opensearch-project/ml-commons/pull/2276))


### Opensearch Neural Search


* BWC tests for text chunking processor ([#661](https://github.com/opensearch-project/neural-search/pull/661))
* Add support for request\_cache flag in hybrid query ([#663](https://github.com/opensearch-project/neural-search/pull/663))
* Allowing execution of hybrid query on index alias with filters ([#670](https://github.com/opensearch-project/neural-search/pull/670))
* Allowing query by raw tokens in neural\_sparse query ([#693](https://github.com/opensearch-project/neural-search/pull/693))
* Removed stream.findFirst implementation to use more native iteration implement to improve hybrid query latencies by 35% ([#706](https://github.com/opensearch-project/neural-search/pull/706))
* Removed map of subquery to subquery index in favor of storing index as part of disi wrapper to improve hybrid query latencies by 20% ([#711](https://github.com/opensearch-project/neural-search/pull/711))
* Avoid change max\_chunk\_limit exceed exception in text chunking processor ([#717](https://github.com/opensearch-project/neural-search/pull/717))


### Opensearch Observability


* Tenancy access control ([#1821](https://github.com/opensearch-project/observability/pull/1821))


### Opensearch Security


* Check for and perform upgrades on security configurations ([#4251](https://github.com/opensearch-project/security/pull/4251))
* Replace bouncy castle blake2b ([#4284](https://github.com/opensearch-project/security/pull/4284))
* Adds saml auth header to differentiate saml requests and prevents auto login as anonymous user when basic authentication fails ([#4228](https://github.com/opensearch-project/security/pull/4228))
* Dynamic sign in options ([#4137](https://github.com/opensearch-project/security/pull/4137))
* Add index permissions for query insights exporters ([#4231](https://github.com/opensearch-project/security/pull/4231))
* Add new stop words system index ([#4181](https://github.com/opensearch-project/security/pull/4181))
* Switch to built-in security transports from core ([#4119](https://github.com/opensearch-project/security/pull/4119)) ([#4174](https://github.com/opensearch-project/security/pull/4174)) ([#4187](https://github.com/opensearch-project/security/pull/4187))
* System index permission grants reading access to documents in the index ([#4291](https://github.com/opensearch-project/security/pull/4291))
* Improve cluster initialization reliability ([#4002](https://github.com/opensearch-project/security/pull/4002)) ([#4256](https://github.com/opensearch-project/security/pull/4256))


### Opensearch Security Dashboards Plugin


* Adds Multiple Datasources Support for Security Dashboards Plugin ([#1888](https://github.com/opensearch-project/security-dashboards-plugin/pull/1888))
* Adds flow-framework transport action permissions to the static dropdown list ([#1908](https://github.com/opensearch-project/security-dashboards-plugin/pull/1908))
* Update copy for tenancy tab ([#1881](https://github.com/opensearch-project/security-dashboards-plugin/pull/1881))
* Clear session storage on auto-logout & remove unused saml function ([#1872](https://github.com/opensearch-project/security-dashboards-plugin/pull/1872))
* Create a password strength UI for security dashboards plugin ([#1762](https://github.com/opensearch-project/security-dashboards-plugin/pull/1762))


### Opensearch k-NN


* Make the HitQueue size more appropriate for exact search ([#1549](https://github.com/opensearch-project/k-NN/pull/1549))
* Implement the Streaming Feature to stream vectors from Java to JNI layer to enable creation of larger segments for vector indices ([#1604](https://github.com/opensearch-project/k-NN/pull/1604))
* Remove unnecessary toString conversion of vector field and added some minor optimization in KNNCodec ([1613](https://github.com/opensearch-project/k-NN/pull/1613))
* Serialize all models into cluster metadata ([#1499](https://github.com/opensearch-project/k-NN/pull/1499))


### SQL


* Add iceberg support to EMR serverless jobs. ([#2602](https://github.com/opensearch-project/sql/pull/2602))
* Use EMR serverless bundled iceberg JAR. ([#2646](https://github.com/opensearch-project/sql/pull/2646))


## BUG FIXES


### Dashboards Observability


* Update live mv table name ([#1725](https://github.com/opensearch-project/dashboards-observability/pull/1725))
* Changes loading configuration for Explorer default ([#1720](https://github.com/opensearch-project/dashboards-observability/pull/1720))
* Remove auto refresh option in create acceleration flyout ([#1716](https://github.com/opensearch-project/dashboards-observability/pull/1716))
* Update mv name to include double "\_" ([#1712](https://github.com/opensearch-project/dashboards-observability/pull/1712))
* Bugfix: Use workflows option in selection ([#1704](https://github.com/opensearch-project/dashboards-observability/pull/1704))
* Fix small issues within explorer search bar and sample query ([#1683](https://github.com/opensearch-project/dashboards-observability/pull/1683))
* (query assist) Update styles for callout and combo box ([#1675](https://github.com/opensearch-project/dashboards-observability/pull/1675))
* Convert cache to session storage ([#1669](https://github.com/opensearch-project/dashboards-observability/pull/1669))
* Correctly Utilize Cache in Tables Flyout ([#1662](https://github.com/opensearch-project/dashboards-observability/pull/1662))
* Bug Fix for Undefined Association ([#1658](https://github.com/opensearch-project/dashboards-observability/pull/1658))
* Prevent logged out datasources call ([#1653](https://github.com/opensearch-project/dashboards-observability/pull/1653))
* Update intercept to check logout request ([#1650](https://github.com/opensearch-project/dashboards-observability/pull/1650))
* Fix integration flyout successes ([#1647](https://github.com/opensearch-project/dashboards-observability/pull/1647))
* Clear callout in query assist ([#1646](https://github.com/opensearch-project/dashboards-observability/pull/1646))
* [BUGFIX] Fix integration data reading double escape ([#1644](https://github.com/opensearch-project/dashboards-observability/pull/1644))
* Clear cache on any 401 response errors ([#1634](https://github.com/opensearch-project/dashboards-observability/pull/1634))
* Updating catch for guardrails ([#1631](https://github.com/opensearch-project/dashboards-observability/pull/1631))
* Updating snapshot to fix build ([#1627](https://github.com/opensearch-project/dashboards-observability/pull/1627))
* Bug fixes and UI updates for datasources ([#1618](https://github.com/opensearch-project/dashboards-observability/pull/1618))
* Create acceleration flyout bug fixes ([#1617](https://github.com/opensearch-project/dashboards-observability/pull/1617))
* Fix DSL router, update UI for query assist ([#1612](https://github.com/opensearch-project/dashboards-observability/pull/1612))
* Fixed bugs in explorer redirection ([#1609](https://github.com/opensearch-project/dashboards-observability/pull/1609))
* Sanitize create acceleration queries and direct queries ([#1605](https://github.com/opensearch-project/dashboards-observability/pull/1605))
* Fix create acceleration bugs ([#1599](https://github.com/opensearch-project/dashboards-observability/pull/1599))
* Updating usePolling to cleanup after unmount ([#1598](https://github.com/opensearch-project/dashboards-observability/pull/1598))
* Enable integration install flyout for other install buttons ([#1596](https://github.com/opensearch-project/dashboards-observability/pull/1596))
* Disable close button when integration is being installed ([#1591](https://github.com/opensearch-project/dashboards-observability/pull/1591))


### Opensearch Alerting


* Fix fieldLimit exception in docLevelMonitor. ([#1368](https://github.com/opensearch-project/alerting/pull/1368))


### Opensearch Alerting Dashboards Plugin


* Include server.basepath config in the manage notifications channel Url. ([#914](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/914))
* Removed cross cluster monitor experimental banner, and fixed bugs. ([#933](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/933))
* Fetching timezone from ui settings for Trigger context formatting ([#913](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/913))


### Opensearch Anomaly Detection Dashboards


* Populate selected indices from query params on initial load ([#713](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/713))
* Build query parameters using data\_end\_time ([#741](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/741))


### Opensearch Asynchronous Search


* Fix number of total shards in partial search response ([#565](https://github.com/opensearch-project/asynchronous-search/pull/565))


### Opensearch Cross Cluster Replication


* Handle response for deletion of non-existent autofollow replication rule ([#1371](https://github.com/opensearch-project/cross-cluster-replication/pull/1371))


### Opensearch Dashboards Maps


* Fix zoom level type error in custom layer ([#605](https://github.com/opensearch-project/dashboards-maps/pull/605))


### Opensearch Dashboards Notifications


* Handle error state when dataSource switches to invalid dataSource ([#199](https://github.com/opensearch-project/dashboards-notifications/pull/199))
* Fix broken osd functional test repo ([#189](https://github.com/opensearch-project/dashboards-notifications/pull/189))([#190](https://github.com/opensearch-project/dashboards-notifications/pull/190))


### Opensearch Dashboards Search Relevance


* Added flag for fix when mds is disabled ([#390](https://github.com/opensearch-project/dashboards-search-relevance/pull/390)) ([#392](https://github.com/opensearch-project/dashboards-search-relevance/pull/392))



### Opensearch Flow Framework


* Reset workflow state to initial state after successful deprovision ([#635](https://github.com/opensearch-project/flow-framework/pull/635))
* Silently ignore content on APIs that don't require it ([#639](https://github.com/opensearch-project/flow-framework/pull/639))
* Hide user and credential field from search response ([#680](https://github.com/opensearch-project/flow-framework/pull/680))
* Throw the correct error message in status API for WorkflowSteps ([#676](https://github.com/opensearch-project/flow-framework/pull/676))
* Delete workflow state when template is deleted and no resources exist ([#689](https://github.com/opensearch-project/flow-framework/pull/689))
* Fixing model group parsing and restoring context ([#695](https://github.com/opensearch-project/flow-framework/pull/695))


### Opensearch Index Management Dashboards Plugin


* Set ActiveOption prop to undefined on first load ([#1042](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1042))
* Readonly DataSourceMenu in create rollup and create transform workflow ([#1047](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1047))
* Fix Transform job create flow where indices won't reset after change of datasource ([#1053](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1053))


### Opensearch ML Commons


* Fix stopwords npe ([#2311](https://github.com/opensearch-project/ml-commons/pull/2311))
* Guardrails npe ([#2304](https://github.com/opensearch-project/ml-commons/pull/2304))
* Not sending failure message when model index isn't present ([#2351](https://github.com/opensearch-project/ml-commons/pull/2351))
* Fix guardrails mapping ([#2279](https://github.com/opensearch-project/ml-commons/pull/2279))
* Fix no model group index issue in connector helper notebook ([#2336](https://github.com/opensearch-project/ml-commons/pull/2336))
* Fixes #2317 predict api not working with asymmetric models ([#2318](https://github.com/opensearch-project/ml-commons/pull/2318))
* Fixing isHidden null issue ([#2337](https://github.com/opensearch-project/ml-commons/pull/2337))
* Fix remote register model / circuit breaker 500([#2264](https://github.com/opensearch-project/ml-commons/pull/2264))
* Guardrails bug fixes and IT for creating guardrails ([#2269](https://github.com/opensearch-project/ml-commons/pull/2269))
* Added missing result filter to inference ([#2367](https://github.com/opensearch-project/ml-commons/pull/2367))
* Making Boolean type for isHidden ([#2341](https://github.com/opensearch-project/ml-commons/pull/2341%EF%BC%89)
* Clear planningWorkerNodes when model auto-deploys again after undeploy ([#2396](https://github.com/opensearch-project/ml-commons/pull/2396))
* Avoid race condition in syncup model state refresh ([#2405](https://github.com/opensearch-project/ml-commons/pull/2405))
* Add a flag to distinguish remote model auto deploy and transport deploy ([#2410](https://github.com/opensearch-project/ml-commons/pull/2410))
* Add deploySetting in registering local models ([#2415](https://github.com/opensearch-project/ml-commons/pull/2415))


### Opensearch ML Commons Dashboards


* Reset current page after data source change ([#320](https://github.com/opensearch-project/ml-commons-dashboards/pull/320))
* Reset to max page when current page overflow ([#323](https://github.com/opensearch-project/ml-commons-dashboards/pull/323))


### Opensearch Neural Search


* Fix async actions are left in neural\_sparse query ([#438](https://github.com/opensearch-project/neural-search/pull/438))
* Fix typo for sparse encoding processor factory([#578](https://github.com/opensearch-project/neural-search/pull/578))
* Add non-null check for queryBuilder in NeuralQueryEnricherProcessor ([#615](https://github.com/opensearch-project/neural-search/pull/615))
* Add max\_token\_score field placeholder in NeuralSparseQueryBuilder to fix the rolling-upgrade from 2.x nodes bwc tests. ([#696](https://github.com/opensearch-project/neural-search/pull/696))
* Fix multi node "no such index" error in text chunking processor. ([#713](https://github.com/opensearch-project/neural-search/pull/713))


### Opensearch Notifications


* Adding max http response string length as a setting, and capping http response string based on that setting ([#876](https://github.com/opensearch-project/notifications/pull/876))
* Adding Max HTTP Response Size IT ([#901](https://github.com/opensearch-project/notifications/pull/901)) ([#909](https://github.com/opensearch-project/notifications/pull/909))
* Replacing spi.utils isHostInDenyList with core.utils isHostInDenyList ([#904](https://github.com/opensearch-project/notifications/pull/904)) ([#913](https://github.com/opensearch-project/notifications/pull/913))
* Upgrade AWS version for SDKs to 1.12.687 ([#884](https://github.com/opensearch-project/notifications/pull/884)) ([#887](https://github.com/opensearch-project/notifications/pull/887))


### Opensearch Query Workbench


* Fix initial load from cache for S3 tree ([#300](https://github.com/opensearch-project/dashboards-query-workbench/pull/300))


### Opensearch Security


* Ensure that challenge response contains body ([#4268](https://github.com/opensearch-project/security/pull/4268))
* Add logging for audit log that are unable to saving the request body ([#4272](https://github.com/opensearch-project/security/pull/4272))
* Use predictable serialization logic for transport headers ([#4288](https://github.com/opensearch-project/security/pull/4288))
* Update Log4JSink Default from sgaudit to audit and add test for default values ([#4155](https://github.com/opensearch-project/security/pull/4155))
* Remove Pom task dependencies rewrite ([#4178](https://github.com/opensearch-project/security/pull/4178)) ([#4186](https://github.com/opensearch-project/security/pull/4186))
* Misc changes for tests ([#4184](https://github.com/opensearch-project/security/pull/4184))
* Add simple roles mapping integ test to test mapping of backend role to role ([#4176](https://github.com/opensearch-project/security/pull/4176))


### Opensearch Security Analytics


* Fix integ tests after add latest sigma rules ([#950](https://github.com/opensearch-project/security-analytics/pull/950))
* Fix keywords bug and add comments ([#964](https://github.com/opensearch-project/security-analytics/pull/964))
* Changes doc level query name field from id to rule name and adds validation ([#972](https://github.com/opensearch-project/security-analytics/pull/972))
* Fix check for agg rules in detector trigger condition to create chained findings monitor ([#992](https://github.com/opensearch-project/security-analytics/pull/992))


### Opensearch Security Analytics Dashboards


* Wait longer for action button to become enabled ([#983](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/983))


### Opensearch Security Dashboards Plugin


* Fixes saml login flow to work with anonymous auth ([#1839](https://github.com/opensearch-project/security-dashboards-plugin/pull/1839))
* Fixes issue with multi-tenancy and default route to use corresponding default route for the selected tenant ([#1820](https://github.com/opensearch-project/security-dashboards-plugin/pull/1820))
* Fix oidc cypress test and remove doc link ([#1923](https://github.com/opensearch-project/security-dashboards-plugin/pull/1923))
* Add fix for data source disabled plugin should work ([#1916](https://github.com/opensearch-project/security-dashboards-plugin/pull/1916))


### Opensearch k-NN


* Add stored fields for knn\_vector type ([#1630](https://github.com/opensearch-project/k-NN/pull/1630))
* Enable script score to work with model based indices ([#1649](https://github.com/opensearch-project/k-NN/pull/1649))


### SQL


* Align vacuum statement semantics with Flint Spark ([#2606](https://github.com/opensearch-project/sql/pull/2606))
* Handle EMRS exception as 400 ([#2612](https://github.com/opensearch-project/sql/pull/2612))
* Fix pagination for many columns (#2440) ([#2441](https://github.com/opensearch-project/sql/pull/2441))
* Fix semicolon parsing for async query ([#2631](https://github.com/opensearch-project/sql/pull/2631))
* Throw OpensearchSecurityException in case of datasource authorization ([#2626](https://github.com/opensearch-project/sql/pull/2626))


## INFRASTRUCTURE


### Dashboards Observability


* Add workflow to build and install binary to catch run time issues ([#1467](https://github.com/opensearch-project/dashboards-observability/pull/1467))


### Opensearch Alerting


* Adjusted maven publish workflow to execute automatically when merging a PR. ([#1531](https://github.com/opensearch-project/alerting/pull/1531))


### Opensearch Anomaly Detection


* Update sample cert and admin keystore ([#1163](https://github.com/opensearch-project/anomaly-detection/pull/1163))


### Opensearch Anomaly Detection Dashboards


* Add workflow to verify binary installation works ([#693](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/693))


### Opensearch Flow Framework


* Switch macOS runner to macos-13 from macos-latest since macos-latest is now arm64 ([#686](https://github.com/opensearch-project/flow-framework/pull/686))


### Opensearch Job Scheduler


* Improve the repo Code Coverage percentage [(#616)](https://github.com/opensearch-project/job-scheduler/pull/616) [(#621)](https://github.com/opensearch-project/job-scheduler/pull/621)


### Opensearch ML Commons


* Remove checkstyle ([#2312](https://github.com/opensearch-project/ml-commons/pull/2312))
* Increase rounding delta from 0.005% to 0.5% on RestMLInferenceIngestProcessorIT ([#2372](https://github.com/opensearch-project/ml-commons/pull/2372))
* Add agent framework security it tests by ([#2266](https://github.com/opensearch-project/ml-commons/pull/2266))
* Add IT for interface ([#2394](https://github.com/opensearch-project/ml-commons/pull/2394))
* Fix local build failure for RestMLInferenceIngestProcessorIT ([#2402](https://github.com/opensearch-project/ml-commons/pull/2402))


### Opensearch Neural Search


* Adding integration tests for scenario of hybrid query with aggregations ([#632](https://github.com/opensearch-project/neural-search/pull/632))


### Opensearch k-NN


* Add micro-benchmark module in k-NN plugin for benchmark streaming vectors to JNI layer functionality. ([#1583](https://github.com/opensearch-project/k-NN/pull/1583))
* Add arm64 check when SIMD is disabled ([#1618](https://github.com/opensearch-project/k-NN/pull/1618))
* Skip rebuild from scratch after cmake is run ([#1636](https://github.com/opensearch-project/k-NN/pull/1636))


### SQL


* Increment version to 2.14.0-SNAPSHOT ([#2585](https://github.com/opensearch-project/sql/pull/2585))


## DOCUMENTATION


### Dashboards Observability


* Add basic developer docs for integration setup and config ([#1613](https://github.com/opensearch-project/dashboards-observability/pull/1613))
* Change query access messaging ([#1224](https://github.com/opensearch-project/dashboards-observability/pull/1224))


### Opensearch Alerting


* Dev guide update to include building/using local os-min distro. ([#757](https://github.com/opensearch-project/alerting/pull/757))
* Added 2.14 release notes. ([#1534](https://github.com/opensearch-project/alerting/pull/1534))


### Opensearch Alerting Dashboards Plugin


* Added 2.14 release notes. ([#945](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/945))


### Opensearch Common Utils


* Added 2.14.0.0 release notes. ([#648](https://github.com/opensearch-project/common-utils/pull/648))


### Opensearch Dashboards Notifications


* 2.14 release notes. ([#201](https://github.com/opensearch-project/dashboards-notifications/pull/201))


### Opensearch ML Commons


* Add connector blueprint for VertexAI Embedding endpoint ([#2268](https://github.com/opensearch-project/ml-commons/pull/2268))


### Opensearch Notifications


* Add 2.14.0 release notes ([#915](https://github.com/opensearch-project/notifications/pull/915))


### Opensearch Security Analytics


* Added 2.14.0 release notes. ([#1009](https://github.com/opensearch-project/security-analytics/pull/1009))


### Opensearch Security Analytics Dashboards


* Added release notes for 2.14.0 ([#997](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/997))


## MAINTENANCE


### Dashboards Assistant


* Increment version to 2.14.0.0 ([#183](https://github.com/opensearch-project/dashboards-assistant/pull/183))


### Dashboards Observability


* Refactor integrations setup for easier separation of different setup options ([#1741](https://github.com/opensearch-project/dashboards-observability/pull/1741))
* Reformatting integration queries ([#1726](https://github.com/opensearch-project/dashboards-observability/pull/1726))
* Increment version to 2.14.0.0 ([#1673](https://github.com/opensearch-project/dashboards-observability/pull/1673))
* Enable query assist by default ([#1640](https://github.com/opensearch-project/dashboards-observability/pull/1640))
* Update ag-grid dependency to 31 ([#1604](https://github.com/opensearch-project/dashboards-observability/pull/1604))
* Fix datagrid snapshots for 2.x ([#1590](https://github.com/opensearch-project/dashboards-observability/pull/1590))


### Opensearch Alerting


* Increment version to 2.14.0-SNAPSHOT. ([#1492](https://github.com/opensearch-project/alerting/pull/1492))


### Opensearch Alerting Dashboards Plugin


* Increment version to 2.14.0.0 ([#931](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/931))


### Opensearch Anomaly Detection Dashboards


* Remove legacy dependency ([#710](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/710))
* Increment version to 2.14.0.0 ([#695](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/695))


### Opensearch Asynchronous Search


* Increment version to 2.14.0 ([#549](https://github.com/opensearch-project/asynchronous-search/pull/549))


### Opensearch Common Utils


* Increment version to 2.14.0-SNAPSHOT ([#625](https://github.com/opensearch-project/common-utils/pull/625))


### Opensearch Dashboards Notifications


* Add workflow to verify installation of the plugin zip and dashboards ([#165](https://github.com/opensearch-project/dashboards-notifications/pull/165))
* Add AWSHurneyt as maintainer ([#177](https://github.com/opensearch-project/dashboards-notifications/pull/177))
* Increment version to 2.14.0.0 ([#182](https://github.com/opensearch-project/dashboards-notifications/pull/182))


### Opensearch Dashboards Reporting


* Increment version to 2.14.0.0 ([#338](https://github.com/opensearch-project/dashboards-reporting/pull/338))


### Opensearch Dashboards Visualizations


* Increment version to 2.14.0.0 ([#358](https://github.com/opensearch-project/dashboards-visualizations/pull/358))


* Adding 2.14.0 release notes ([#364](https://github.com/opensearch-project/dashboards-visualizations/pull/364))


### Opensearch Job Scheduler


* Increment version to 2.14.0 ([#605](https://github.com/opensearch-project/job-scheduler/pull/605))
* Dependabot: bump com.google.googlejavaformat:google-java-format ([#608](https://github.com/opensearch-project/job-scheduler/pull/608))
* Dependabot: bump org.slf4j:slf4j-api from 2.0.12 to 2.0.13 [(#611)](https://github.com/opensearch-project/job-scheduler/pull/611) [(#614)](https://github.com/opensearch-project/job-scheduler/pull/614)
* Dependabot: bump org.gradle.test-retry from 1.5.8 to 1.5.9 [(#618)](https://github.com/opensearch-project/job-scheduler/pull/618) [(#619)](https://github.com/opensearch-project/job-scheduler/pull/619)
* Dependabot: bump com.netflix.nebula.ospackage from 11.8.1 to 11.9.0 [(#617)](https://github.com/opensearch-project/job-scheduler/pull/617) [(#620)](https://github.com/opensearch-project/job-scheduler/pull/620)


### Opensearch ML Commons


* Fix CVE for org.eclipse.core.runtime ([#2378](https://github.com/opensearch-project/ml-commons/pull/2378))


### Opensearch ML Commons Dashboards


* Increment version to 2.14.0.0 ([#313](https://github.com/opensearch-project/ml-commons-dashboards/pull/313))


### Opensearch Neural Search


* Update bwc tests for neural\_query\_enricher neural\_sparse search ([#652](https://github.com/opensearch-project/neural-search/pull/652))


### Opensearch Notifications


* Increment version to 2.14.0-SNAPSHOT (#[882](https://github.com/opensearch-project/notifications/pull/882))
* Updates sample cert and admin keystore (#[862](https://github.com/opensearch-project/notifications/pull/862)) (#[885](https://github.com/opensearch-project/notifications/pull/885))
* Updates sample cert and trust-store (#[899](https://github.com/opensearch-project/notifications/pull/899)) (#[912](https://github.com/opensearch-project/notifications/pull/912))


### Opensearch Observability


* Increment version to 2.14.0-SNAPSHOT ([#1813](https://github.com/opensearch-project/observability/pull/1813))


### Opensearch Query Workbench


* Increment version to 2.14.0.0 ([#304](https://github.com/opensearch-project/dashboards-query-workbench/pull/304))


* Add release notes for 2.14 ([#312](https://github.com/opensearch-project/dashboards-query-workbench/pull/312))


### Opensearch Reporting


* Updates sample cert and admin keystore ([#970](https://github.com/opensearch-project/reporting/pull/970))
* Increment version to 2.14.0-SNAPSHOT ([#980](https://github.com/opensearch-project/reporting/pull/980))


### Opensearch Security


* Add getProperty.org.bouncycastle.ec.max\_f2m\_field\_size to plugin-security.policy ([#4270](https://github.com/opensearch-project/security/pull/4270))
* Add getProperty.org.bouncycastle.pkcs12.default to plugin-security.policy ([#4266](https://github.com/opensearch-project/security/pull/4266))
* Bump apache\_cxf\_version from 4.0.3 to 4.0.4 ([#4287](https://github.com/opensearch-project/security/pull/4287))
* Bump ch.qos.logback:logback-classic from 1.5.3 to 1.5.5 ([#4248](https://github.com/opensearch-project/security/pull/4248))
* Bump codecov/codecov-action from v3 to v4 ([#4237](https://github.com/opensearch-project/security/pull/4237))
* Bump com.fasterxml.woodstox:woodstox-core from 6.6.1 to 6.6.2 ([#4195](https://github.com/opensearch-project/security/pull/4195))
* Bump com.google.googlejavaformat:google-java-format from 1.21.0 to 1.22.0 ([#4220](https://github.com/opensearch-project/security/pull/4220))
* Bump commons-io:commons-io from 2.15.1 to 2.16.1 ([#4196](https://github.com/opensearch-project/security/pull/4196)) ([#4246](https://github.com/opensearch-project/security/pull/4246))
* Bump com.nulab-inc:zxcvbn from 1.8.2 to 1.9.0 ([#4219](https://github.com/opensearch-project/security/pull/4219))
* Bump io.dropwizard.metrics:metrics-core from 4.2.15 to 4.2.25 ([#4193](https://github.com/opensearch-project/security/pull/4193)) ([#4197](https://github.com/opensearch-project/security/pull/4197))
* Bump net.shibboleth.utilities:java-support from 8.4.1 to 8.4.2 ([#4245](https://github.com/opensearch-project/security/pull/4245))
* Bump spring\_version from 5.3.33 to 5.3.34 ([#4250](https://github.com/opensearch-project/security/pull/4250))
* Bump Wandalen/wretry.action from 1.4.10 to 3.3.0 ([#4167](https://github.com/opensearch-project/security/pull/4167)) ([#4198](https://github.com/opensearch-project/security/pull/4198)) ([#4221](https://github.com/opensearch-project/security/pull/4221)) ([#4247](https://github.com/opensearch-project/security/pull/4247))
* Bump open\_saml\_version from 4.3.0 to 4.3.2 ([#4303](https://github.com/opensearch-project/security/pull/4303)) ([#4239](https://github.com/opensearch-project/security/pull/4239))


### Opensearch Security Analytics


* Increment version to 2.14.0-SNAPSHOT. ([#1007](https://github.com/opensearch-project/security-analytics/pull/1007))
* Updates sample cert and admin keystore ([#864](https://github.com/opensearch-project/security-analytics/pull/864))


### Opensearch Security Analytics Dashboards


* [AUTO] Increment version to 2.14.0.0 ([#990](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/990))
* Updated dependencies ([#984](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/984))


### Opensearch Security Dashboards Plugin


* Add husky pre commit and lint files ([#1859](https://github.com/opensearch-project/security-dashboards-plugin/pull/1859))
* Remove implicit dependency to admin as password ([#1855](https://github.com/opensearch-project/security-dashboards-plugin/pull/1855))
* Bump jose from 4.11.2 to 5.2.4 ([#1902](https://github.com/opensearch-project/security-dashboards-plugin/pull/1902))


### Opensearch Skills


* Increment byte-buddy version to 1.14.9 ([#288](https://github.com/opensearch-project/skills/pull/288))


### SQL


* Refactoring of SparkQueryDispatcher ([#2615](https://github.com/opensearch-project/sql/pull/2615))


## REFACTORING


### Opensearch Alerting


* Removed log entry regarding destination migration. ([#1356](https://github.com/opensearch-project/alerting/pull/1356))
* Set the cancelAfterTimeInterval parameter on SearchRequest object in all MonitorRunners. ([#1366](https://github.com/opensearch-project/alerting/pull/1366))
* Add validation check for doc level query name during monitor creation. ([#1506](https://github.com/opensearch-project/alerting/pull/1506))
* Added input validation, and fixed bug for cross cluster monitors. ([#1510](https://github.com/opensearch-project/alerting/pull/1510))
* Doc-level monitor fan-out approach ([#1521](https://github.com/opensearch-project/alerting/pull/1521))


### Opensearch Common Utils


* Obfuscate ip addresses in alert error message ([#511](https://github.com/opensearch-project/common-utils/pull/511))
* Change doc level query name validation ([#630](https://github.com/opensearch-project/common-utils/pull/630))
* Added validation for the new clusters field. ([#633](https://github.com/opensearch-project/common-utils/pull/633))
* Wrapped URI syntax exception in IllegalArgument exception. ([#645](https://github.com/opensearch-project/common-utils/pull/645))


### Opensearch Flow Framework


* Improve error messages for workflow states other than NOT\_STARTED ([#642](https://github.com/opensearch-project/flow-framework/pull/642))


### Opensearch ML Commons


* Feat: Add search index tool ([#2356](https://github.com/opensearch-project/ml-commons/pull/2356))
* Move visualization tool to ml-commons ([#2363](https://github.com/opensearch-project/ml-commons/pull/2363))


### Opensearch Security Analytics


* Allow detectors to be stopped if underlying workflow is deleted. Don't allow them to then be started/edited ([#810](https://github.com/opensearch-project/security-analytics/pull/810))


### Opensearch Security Analytics Dashboards


* Update vega-lite specs with theme based colors ([#978](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/978))


