# OpenSearch and OpenSearch Dashboards 2.19.4 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 2.19.4 includes the following bug fixes, infrastructure, documentation and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.4.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.4.md).

## BUG FIXES


### OpenSearch Alerting


* Fix MGet bug, randomize fan out distribution ([#1907](https://github.com/opensearch-project/alerting/pull/1907))


### OpenSearch Dashboards Observability


* Fixed metrics viz not showing up ([#2490](https://github.com/opensearch-project/dashboards-observability/pull/2490))


### OpenSearch Flow Framework


* Always succeed hasIndex checks with multiTenancy enabled ([#1209](https://github.com/opensearch-project/flow-framework/pull/1209))
* Avoid race condition setting encryption key ([#1202](https://github.com/opensearch-project/flow-framework/pull/1202))


### OpenSearch ML Commons


* Fix CVE-2025-55163, CVE-2025-48924, CVE-2025-58057 ([#4339](https://github.com/opensearch-project/ml-commons/pull/4339))


### OpenSearch OpenSearch Learning To Rank Base


* Fix Version compatibility issues with legacy versions ([#216](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/216))


### OpenSearch OpenSearch Remote Metadata Sdk


* Avoid race condition putting the same document id in DDB Client ([#229](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/229))
* Throw exception on empty string for put request ID ([#237](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/237))


### OpenSearch Query Insights


* Fix missing check for time range validation that from timestamp is before to timestamp ([#419](https://github.com/opensearch-project/query-insights/pull/419))
* Fix-flaky-ReaderIT ([#402](https://github.com/opensearch-project/query-insights/pull/402))


### OpenSearch Query Insights Dashboards


* Fetch top query with verbose=false on overview ([#322](https://github.com/opensearch-project/query-insights-dashboards/pull/322))
* Remove duplicate requests on overview page loading ([#319](https://github.com/opensearch-project/query-insights-dashboards/pull/319))
* Fetch only once if the first call returns a valid response on Detail page ([#324](https://github.com/opensearch-project/query-insights-dashboards/pull/324))
* Bug fix for Top N table column filters and date picker ([#338](https://github.com/opensearch-project/query-insights-dashboards/pull/338))
* Fix failed cypress tests and fix table sort in 2.19 ([#320](https://github.com/opensearch-project/query-insights-dashboards/pull/320))
* CVE Fixes ([#420](https://github.com/opensearch-project/query-insights-dashboards/pull/420))


### OpenSearch Security


* Create a WildcardMatcher.NONE when creating a WildcardMatcher with an empty string ([#5694](https://github.com/opensearch-project/security/pull/5694))
* Optimize the Fls/Dls/FieldMasking data structure to only include the concrete indices from the current request ([#5482](https://github.com/opensearch-project/security/pull/5482))
* Ensure that IndexResolverReplacer resolves to indices for RolloverRequests ([#5522](https://github.com/opensearch-project/security/pull/5522))
* Add 'good' as a valid value for plugins.security.restapi.password\_score\_based\_validation\_strength ([#5523](https://github.com/opensearch-project/security/pull/5523))
* Use FilterLeafReader based DLS for parent/child queries ([#5538](https://github.com/opensearch-project/security/pull/5538))
* Fixed index resolution for rollover requests ([#5526](https://github.com/opensearch-project/security/pull/5526))
* Fixed TLS endpoint identification by SAN ([#5669](https://github.com/opensearch-project/security/pull/5669))
* Avoid ConcurrentModificationException for User class fields ([#5615](https://github.com/opensearch-project/security/pull/5615))


### OpenSearch Security Analytics


* Move rules to config directory from classpath resources ([#1584](https://github.com/opensearch-project/security-analytics/pull/1584))


### OpenSearch Security Analytics Dashboards Plugin


* Display alerts when a configured correlation rule is opened ([#1303](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1303))


### OpenSearch k-NN


* Fix @ collision in NativeMemoryCacheKeyHelper and add unit tests([#2813](https://github.com/opensearch-project/k-NN/pull/2813))


### SQL


* Bump commons-lang3 version to resolve CVE-2025-48924 ([#4693](https://github.com/opensearch-project/sql/pull/4693))


## INFRASTRUCTURE


### OpenSearch ML Commons


* Onboard to s3 snapshots ([#4320](https://github.com/opensearch-project/ml-commons/pull/4320))
* Pass isMultiTenancyEnabled across classes to early return index search ([#4113](https://github.com/opensearch-project/ml-commons/pull/4113))


### OpenSearch Query Insights Dashboards


* Unit test for QueryUtils, application, plugin ([#316](https://github.com/opensearch-project/query-insights-dashboards/pull/316))
* Updated the cypress workflow in 2.19 ([#321](https://github.com/opensearch-project/query-insights-dashboards/pull/321))


### OpenSearch Security Dashboards Plugin


* Specify cypress version in run-cypress-tests action to v13 for node compatibility ([#2314](https://github.com/opensearch-project/security-dashboards-plugin/pull/2314))
* Update sonatype repo ([#2312](https://github.com/opensearch-project/security-dashboards-plugin/pull/2312))


## MAINTENANCE


### OpenSearch Alerting Dashboards Plugin


* [Backport 2.19] Cherry pick CVE fixes ([#1303](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1303))


### OpenSearch Anomaly Detection


* [2.19] Bumping python dependencies to resolve CVEs ([#1597](https://github.com/opensearch-project/anomaly-detection/pull/1597))


### OpenSearch Anomaly Detection Dashboards Plugin


* [2.19] Updating several dependencies ([#1113](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1113))


### OpenSearch Cross Cluster Replication


* [CVE 2024 47081] Fix:Update dependency requests to v2.32.4 ([#1569](https://github.com/opensearch-project/cross-cluster-replication/pull/1569))
* [Backport 2.19] [CVE 2024 47081] Fix:Update dependency requests to v2.32.4 ([#1599](https://github.com/opensearch-project/cross-cluster-replication/pull/1599))


### OpenSearch Dashboards Assistant


* Bump formdata to 4.0.4 ([#619](https://github.com/opensearch-project/dashboards-assistant/pull/619))


### OpenSearch Dashboards Notifications


* Cve fix: bump form-data to 4.0.4 ([#390](https://github.com/opensearch-project/dashboards-notifications/pull/390))


### OpenSearch Dashboards Observability


* Added cve fix CVE-2025-7783 ([#2519](https://github.com/opensearch-project/dashboards-observability/pull/2519))
* Bump serialize to 6.0.2 ([#2521](https://github.com/opensearch-project/dashboards-observability/pull/2521))


### OpenSearch Dashboards Query Workbench


* Fixing CVE-2025-7783 ([#509](https://github.com/opensearch-project/dashboards-query-workbench/pull/509))


### OpenSearch Dashboards Reporting


* [Maintenance] CVE fixes ([#651](https://github.com/opensearch-project/dashboards-reporting/pull/651))


### OpenSearch Flow Framework


* Update spotless and checkstyle to run on JDK21 ([#1210](https://github.com/opensearch-project/flow-framework/pull/1210))


### OpenSearch Geospatial


* Bump up commons-lang3 version ([#808](https://github.com/opensearch-project/geospatial/pull/808))


### OpenSearch Index Management Dashboards Plugin


* Fixing CVE-2025-7783 CVE-2025-9287 CVE-2025-9288 CVE-2025-6547 CVE-2025-6545 ([#1370](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1370))


### OpenSearch Neural Search


* Remove commons-lang:commons-lang dependency and use gradle version catalog for commons-lang3 ([#1628](https://github.com/opensearch-project/neural-search/pull/1628))


### OpenSearch OpenSearch Remote Metadata Sdk


* Exclude commons-lang3 from checkstyle transitive dependencies ([#275](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/275)
* Resolve netty CVEs([#277](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/277))


### OpenSearch Performance Analyzer


* Bump bcpkix-jdk18on and commons-lang3 ([#877](https://github.com/opensearch-project/performance-analyzer/pull/877))
* Bump checkstyle and spotbug versions ([#861](https://github.com/opensearch-project/performance-analyzer/pull/861))
* Force io.netty:netty-codec-http2 version ([#879](https://github.com/opensearch-project/performance-analyzer/pull/879))
* Hardcode BWC to 2.19 to mitigate build failure ([#874](https://github.com/opensearch-project/performance-analyzer/pull/874))
* [2.19] run ./gradlew updateSHAs to fix dependency license check ([#859](https://github.com/opensearch-project/performance-analyzer/pull/859))


### OpenSearch Security


* Bump `com.nimbusds:nimbus-jose-jwt:9.48` from 9.48 to 10.0.2 ([#5480](https://github.com/opensearch-project/security/pull/5480))
* Bump `checkstyle` from 10.3.3 to 10.26.1 ([#5480](https://github.com/opensearch-project/security/pull/5480))
* Add tenancy access info to serialized user in threadcontext ([#5519](https://github.com/opensearch-project/security/pull/5519))
* Optimized wildcard matching runtime performance ([#5543](https://github.com/opensearch-project/security/pull/5543))
* Always install demo certs if configured with demo certs ([#5517](https://github.com/opensearch-project/security/pull/5517))
* Bump org.apache.zookeeper:zookeeper from 3.9.3 to 3.9.4 ([#5689](https://github.com/opensearch-project/security/pull/5689))


### OpenSearch Security Analytics


* Add updateVersion task ([#1605](https://github.com/opensearch-project/security-analytics/pull/1605))


### OpenSearch Security Analytics Dashboards Plugin


* Upgrade js-yaml to v4.1 ([#1333](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1333))
* Cherry pick CVE fixes #1322, #1340 ([#1348](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1348))


### OpenSearch Security Dashboards Plugin


* Forcibly resolve a few dependencies to resolve CVEs ([#2332](https://github.com/opensearch-project/security-dashboards-plugin/pull/2332))
* Bumps cypress to 13.6.0 ([#2335](https://github.com/opensearch-project/security-dashboards-plugin/pull/2335))


### OpenSearch Skills


* Bump org.apache.commons.commons-lang3 from 3.16.0 to 3.18.0 ([#661](https://github.com/opensearch-project/skills/pull/661))


### OpenSearch k-NN


* Replace commons-lang with org.apache.commons:commons-lang3 ([#2956](https://github.com/opensearch-project/k-NN/pull/2956)


## REFACTORING


### OpenSearch Dashboards Flow Framework


* Improve yaml parsing on import ([#771](https://github.com/opensearch-project/dashboards-flow-framework/pull/771))


### OpenSearch ML Commons


* Refactors undeploy models client with sdkClient bulk op ([#4077](https://github.com/opensearch-project/ml-commons/pull/4077))


