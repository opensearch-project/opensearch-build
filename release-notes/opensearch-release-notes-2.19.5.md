# OpenSearch and OpenSearch Dashboards 2.19.5 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 2.19.5 includes the following bug fixes, infrastructure, documentation and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.5.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.5.md).


## BUG FIXES


### OpenSearch Alerting


* Preserve user when stashing thread context when sending alert notification messages. ([#2027](https://github.com/opensearch-project/alerting/pull/2027))


### OpenSearch Alerting Dashboards Plugin


* Onboarded opensearch apis to use MDS client when MDS is enabled ([#1313](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1313))


### OpenSearch Cross Cluster Replication


* [Backport 2.19] Upgrade filelock to 3.20.3 (CVE-2025-68146 and CVE-2026-22701) ([#1643](https://github.com/opensearch-project/cross-cluster-replication/pull/1643))


### OpenSearch Dashboards Assistant


* CVE-2025-64718 ([#635](https://github.com/opensearch-project/dashboards-assistant/pull/635))
* Fix CVE-2025-5889 ([#602](https://github.com/opensearch-project/dashboards-assistant/pull/602))


### OpenSearch Dashboards Notifications


* Bumped qs version for CVE-2025-15284. ([#428](https://github.com/opensearch-project/dashboards-notifications/pull/428))


### OpenSearch Dashboards Observability


* [backport] Upgrade cypress-parallel for js-yaml CVE-2025-64718 fix #2577 ([#2606](https://github.com/opensearch-project/dashboards-observability/pull/2606))


### OpenSearch Dashboards Reporting


* CVE-2025-68428 CVE-2025-15284 CVE-2025-64718 fixes ([#696](https://github.com/opensearch-project/dashboards-reporting/pull/696))


### OpenSearch Flow Framework


* Fixing connector name in default use case ([#1207](https://github.com/opensearch-project/flow-framework/pull/1207))


### OpenSearch Index Management Dashboards Plugin


* Fixing CVE-2025-15284 and CVE-2025-64718 ([#1402](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1402))


### OpenSearch ML Commons


* Fix CVE 2.19 ([#4694](https://github.com/opensearch-project/ml-commons/pull/4694))


### OpenSearch Notifications


* CVE Fix upgrade jackson-core and Security fix related to hostDenyList ([#1006](https://github.com/opensearch-project/notifications/pull/1006))


### OpenSearch Learning To Rank Base


* [Backport 2.19] Fix bad inclusion of log4j in this jar when bundled ([#297](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/297))


### OpenSearch System Templates


* Upgrade 2.19.5, fix cgroup detection ([#121](https://github.com/opensearch-project/opensearch-system-templates/pull/121))


### OpenSearch Query Insights Dashboards


* Fix CVE-2025-15284 and CVE-2025-64718 ([#481](https://github.com/opensearch-project/query-insights-dashboards/pull/481))


### OpenSearch Security


* [2.19] Fix issue serializing user to threadcontext when userRequestedTenant is null ([#5925](https://github.com/opensearch-project/security/pull/5925))
* Fix ConcurrentModificationException for SecurityRoles for 2.x ([#5860](https://github.com/opensearch-project/security/pull/5860))


### OpenSearch Security Analytics


* Fix bug when deleting detector with 0 rules. ([#1648](https://github.com/opensearch-project/security-analytics/pull/1648))


### OpenSearch k-NN


* [Backport 2.19] Fix indexing for 16x and 8x compression ([#3123](https://github.com/opensearch-project/k-NN/pull/3123))


### OpenSearch SQL


* Fix 2.19.5 Build Failures ([#5195](https://github.com/opensearch-project/sql/pull/5195))


## INFRASTRUCTURE


### OpenSearch Alerting


* Adjust shadowJar name. ([#2031](https://github.com/opensearch-project/alerting/pull/2031))
* Update logback dependencies to version 1.5.19 ([#1996](https://github.com/opensearch-project/alerting/pull/1996))


### OpenSearch Alerting Dashboards Plugin


* Updated package structure and configs for cypress 12.17.4 version bump. ([#1381](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1381))


### OpenSearch Anomaly Detection


* [2.19] Update urllib3 to 2.6.3 to resolve CVEs ([#1676](https://github.com/opensearch-project/anomaly-detection/pull/1676))
* [Backport 2.19] Update macOS GitHub runners to macos-15-intel ([#1640](https://github.com/opensearch-project/anomaly-detection/pull/1640))


### OpenSearch Common Utils


* Adjust shadowJar name. ([#909](https://github.com/opensearch-project/common-utils/pull/909))


### OpenSearch Custom Codecs


* Fix Github Actions MacOS checks ([#298](https://github.com/opensearch-project/custom-codecs/pull/298))


### OpenSearch Dashboards Notifications


* Updated package structure and configs for cypress 12.17.4 version bump. ([#429](https://github.com/opensearch-project/dashboards-notifications/pull/429))


### OpenSearch Job Scheduler


* [2.19] Change com.github.johnrengelman.shadow to com.gradleup.shadow ([#888](https://github.com/opensearch-project/job-scheduler/pull/888))


### OpenSearch Security


* [Backport 2.19] Enable mend remediate to create PRs ([#5784](https://github.com/opensearch-project/security/pull/5784))


### OpenSearch Security Analytics Dashboards Plugin


* Updated package structure and configs for cypress 12.17.4 version bump. ([#1386](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1386))


### OpenSearch SQL


* Adjust shadowJar name ([#5203](https://github.com/opensearch-project/sql/pull/5203))


## MAINTENANCE


### OpenSearch Alerting


* Remove PPL alerting feature. ([#2019](https://github.com/opensearch-project/alerting/pull/2019))


### OpenSearch Alerting Dashboards Plugin


* Bumped qs version for CVE-2025-15284. ([#1380](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1380))


### OpenSearch Anomaly Detection Dashboards Plugin


* Bump lodash from 4.17.21 to 4.17.23 ([#1135](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1135))
* [2.19] Force js-yaml to 3.14.2 to resolve CVE-2025-64718 ([#1155](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1155))


### OpenSearch Common Utils


* [Backport 2.19] Bump logback from 1.5.19 to 1.5.32 ([#905](https://github.com/opensearch-project/common-utils/pull/905))


### OpenSearch Dashboards Flow Framework


* Bump lodash from 4.17.21 to 4.17.23 ([#840](https://github.com/opensearch-project/dashboards-flow-framework/pull/840))
* Change `jsonpath` dep to `jsonpath-plus` ([#756](https://github.com/opensearch-project/dashboards-flow-framework/pull/756))


### OpenSearch Dashboards Observability


* Pin glob to ^10.5.0 to fix yarn build failure on Node 18 ([#2610](https://github.com/opensearch-project/dashboards-observability/pull/2610))
* Remove unused @cypress/request ([#2614](https://github.com/opensearch-project/dashboards-observability/pull/2614))


### OpenSearch Dashboards Query Workbench


* Bump js-yaml ([#527](https://github.com/opensearch-project/dashboards-query-workbench/pull/527))
* Update a dep ([#530](https://github.com/opensearch-project/dashboards-query-workbench/pull/530))


### OpenSearch Notifications


* Update logback dependencies to version 1.5.19 ([#1103](https://github.com/opensearch-project/notifications/pull/1103))


### OpenSearch Observability


* Bump logback core to 1.15.20 ([#1960](https://github.com/opensearch-project/observability/pull/1960))


### OpenSearch Learning To Rank Base


* Force error\_prone\_annotations to 2.41.0 to resolve dependency conflict ([#299](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/299))


### OpenSearch Reporting


* Bump logback core to 1.15.20 ([#1143](https://github.com/opensearch-project/reporting/pull/1143))


### OpenSearch Security


* [2.19] Bump commons-text to 1.15.0 and log4j-core to 2.25.3 ([#5974](https://github.com/opensearch-project/security/pull/5974))
* [Backport 2.19] Bump org.lz4:lz4-java from 1.8.0 to 1.10.1 ([#5970](https://github.com/opensearch-project/security/pull/5970))


### OpenSearch Security Analytics Dashboards Plugin


* Bumped qs version for CVE-2025-15284. ([#1384](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1384))
* Bumped ys-yaml for CVE-2025-64718. ([#1385](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1385))


### OpenSearch Security Dashboards Plugin


* [2.19] Run yarn upgrade and checkin latest yarn.lock ([#2378](https://github.com/opensearch-project/security-dashboards-plugin/pull/2378))
* [Backport 2.19] Force resolution of basic-ftp to 5.2.0 ([#2377](https://github.com/opensearch-project/security-dashboards-plugin/pull/2377))


## REFACTORING


### OpenSearch Security


* Use RestRequestFilter.getFilteredRequest to declare sensitive API params ([#5710](https://github.com/opensearch-project/security/pull/5710))


