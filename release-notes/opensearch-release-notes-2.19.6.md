# OpenSearch and OpenSearch Dashboards 2.19.6 Release Notes

## Release Details

OpenSearch and OpenSearch Dashboards 2.19.6 includes the following bug fixes, infrastructure and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.6.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.6.md).



## BUG FIXES


### OpenSearch Alerting


* Fix NullPointerException when nested field type has no properties in doc-level monitor ([#2051](https://github.com/opensearch-project/alerting/pull/2051))


### OpenSearch Alerting Dashboards Plugin


* Fixed monitor schedule edit workflow when there is no ui\_metadata for the monitor ([#1421](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1421))


### OpenSearch Common Utils


* Validate api\_type matches path in ClusterMetricsInput to prevent creating monitors with mismatched fields that cannot be deleted ([#914](https://github.com/opensearch-project/common-utils/pull/914))
* Normalize cluster metrics input URI path during validation to fix exception when path is not prepended with `/` ([#922](https://github.com/opensearch-project/common-utils/pull/922))


### OpenSearch Dashboards Assistant


* Bump dependency versions to address 19 CVEs/GHSAs including XSS, prototype pollution, and DoS vulnerabilities ([#698](https://github.com/opensearch-project/dashboards-assistant/pull/698))


### OpenSearch Dashboards Notifications


* Regenerate yarn.lock to resolve lodash to 4.18.1 (CVE-2025-13465, CVE-2026-2950, CVE-2026-4800) ([#463](https://github.com/opensearch-project/dashboards-notifications/pull/463))


### OpenSearch Dashboards Reporting


* Resolve critical, high, and moderate CVEs by upgrading jspdf, updating dependency resolutions, and pinning GitHub Actions to commit SHAs ([#770](https://github.com/opensearch-project/dashboards-reporting/pull/770))
* Replace showdown with marked to resolve CVE-2024-1899 ReDoS vulnerability in markdown-to-HTML conversion ([#776](https://github.com/opensearch-project/dashboards-reporting/pull/776))
* Restore uuid package and revert crypto.randomUUID changes to fix webpack compatibility issues in non-secure HTTP contexts ([#775](https://github.com/opensearch-project/dashboards-reporting/pull/775))


### OpenSearch Learning To Rank Base


* Fix float comparison flakiness with ULP precision and hybrid comparison, cache size integration test fix, rescore-only feature SLTR logging fix, and LoggingSearchExtBuilder.toXContent missing field name fix ([#355](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/355))


### OpenSearch Performance Analyzer


* Upgrade vulnerable dependencies to resolve CVEs (Bouncy Castle, plexus-utils, Netty, Jackson) ([#953](https://github.com/opensearch-project/performance-analyzer/pull/953))


### OpenSearch Reporting


* Bump assertj-core to 3.27.7 to fix CVE-2026-24400 (HIGH) XXE vulnerability ([#1195](https://github.com/opensearch-project/reporting/pull/1195))


### OpenSearch Security Analytics Dashboards Plugin


* Fix webpack build failure on Node 18 by removing uuid resolution that used incompatible optional chaining syntax ([#1543](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1543))


### OpenSearch Security Dashboards Plugin


* Remove serialize-javascript dependency to fix node compatibility issue ([#2455](https://github.com/opensearch-project/security-dashboards-plugin/pull/2455))


### OpenSearch Skills


* Upgrade Apache Spark to 3.5.8 to address CVE-2025-54920 ([#751](https://github.com/opensearch-project/skills/pull/751))


### SQL


* Add ObjectInputFilter allowlist for deserialization in PlanSerializer, DefaultExpressionSerializer, and RelJsonSerializer ([#5469](https://github.com/opensearch-project/sql/pull/5469))

* Validate materialized view subqueries against SQL grammar deny list ([#5490](https://github.com/opensearch-project/sql/pull/5490))



## INFRASTRUCTURE


### OpenSearch ML Commons


* Fix snapshot publishing by pinning GitHub Actions to commit SHAs and removing unreachable Spotless p2 mirror ([#4865](https://github.com/opensearch-project/ml-commons/pull/4865))


### OpenSearch Learning To Rank Base


* Fix Windows CI build failure caused by Spotless P2 mirror timeout by removing withP2Mirrors() configuration ([#303](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/303))


### OpenSearch Query Insights


* Fix 2.19 CI matrix, security integration tests, and Eclipse formatter configuration ([#565](https://github.com/opensearch-project/query-insights/pull/565))
* Disable validatePluginZipPom to fix preexisting JDK 11 build failure on 2.19 ([#631](https://github.com/opensearch-project/query-insights/pull/631))


### OpenSearch Query Insights Dashboards


* Address CVEs in transitive dependencies (lodash, serialize-javascript, minimatch, picomatch, brace-expansion, yaml) ([#541](https://github.com/opensearch-project/query-insights-dashboards/pull/541))
* Onboard new backport-pr reusable GitHub workflow ([#547](https://github.com/opensearch-project/query-insights-dashboards/pull/547))


### OpenSearch Reporting


* Fix maven snapshot publication on 2.19 branch ([#1161](https://github.com/opensearch-project/reporting/pull/1161))



## MAINTENANCE


### OpenSearch Alerting Dashboards Plugin


* Resolved CVE-2026-2739, CVE-2025-69873, and GHSA-5c6j-r48x-rmvq ([#1469](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1469))
* Resolved CVE-2026-27903, CVE-2026-27904, CVE-2026-33671, CVE-2026-33750, and CVE-2026-33532 by adding yarn resolutions for minimatch, picomatch, brace-expansion, and yaml ([#1440](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1440))
* Resolved CVE-2026-8723 by bumping qs to 6.15.2 ([#1458](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1458))
* Removed direct lodash dependency to address CVE-2025-13465, CVE-2026-2950, and CVE-2026-4800 ([#1475](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1475))


### OpenSearch Anomaly Detection Dashboards Plugin


* Fix dependency CVEs for lodash, picomatch, minimatch, bn.js, and brace-expansion ([#1214](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1214))


### OpenSearch Custom Codecs


* Bump opensearch\_version in bwc-test to 2.19.6-SNAPSHOT to resolve log4j-core CVEs ([#350](https://github.com/opensearch-project/custom-codecs/pull/350))


### OpenSearch Dashboards Observability


* Resolve ajv version conflict from OSD ([#2759](https://github.com/opensearch-project/dashboards-observability/pull/2759))
* Remediate dependency vulnerabilities including lodash, picomatch, minimatch, brace-expansion, yaml, ajv, and flatted ([#2750](https://github.com/opensearch-project/dashboards-observability/pull/2750))


### OpenSearch Dashboards Query Workbench


* Patch dependency versions to resolve CVE security vulnerabilities ([#564](https://github.com/opensearch-project/dashboards-query-workbench/pull/564))


### OpenSearch Dashboards Reporting


* Bump lodash from 4.17.21 to 4.17.23 ([#672](https://github.com/opensearch-project/dashboards-reporting/pull/672))


### OpenSearch Index Management Dashboards Plugin


* Bump lodash and picomatch to fix CVEs ([#1446](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1446))


### OpenSearch ML Commons Dashboards


* Fix CVE-2026-33671, CVE-2026-33672, and CVE-2026-33532 by updating picomatch and yaml dependencies ([#499](https://github.com/opensearch-project/ml-commons-dashboards/pull/499))


### OpenSearch Observability


* Bump assertj-core from 3.16.1 to 3.27.7 to remediate CVE-2026-24400 (XXE vulnerability) ([#2008](https://github.com/opensearch-project/observability/pull/2008))


### OpenSearch Learning To Rank Base


* Fix CVE-2026-34478 by upgrading log4j dependencies to 2.25.4 ([#330](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/330))
* Upgrade RankyMcRankFace 0.1.1 to 0.3.0 to fix XXE/DTD vulnerability and add issues:write permission to untriaged-label workflow ([#355](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/355))


### OpenSearch Security


* Update Kafka to 3.9.2 to resolve CVE-2026-35554 and other security issues ([#6089](https://github.com/opensearch-project/security/pull/6089))
* Resolve CVEs by bumping dependencies ([#6242](https://github.com/opensearch-project/security/pull/6242))


### OpenSearch Security Analytics Dashboards Plugin


* Resolve CVE-2026-33750 by bumping brace-expansion to ^5.0.5 to prevent infinite loop on zero-step brace patterns ([#1421](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1421))
* Resolve CVE-2026-4800, CVE-2026-27904, CVE-2026-33532, and CVE-2026-33672 by bumping lodash and lodash-es to ^4.18.0 ([#1514](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1514))
* Resolve CVE-2026-8723 by bumping qs to ^6.15.2 to fix TypeError with arrayFormat comma and null array entries ([#1532](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1532))
* Resolve CVE-2026-2739, CVE-2025-69873, and GHSA-5c6j-r48x-rmvq ([#1538](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1538))


### OpenSearch Security Dashboards Plugin


* Resolve 22 CVEs by adding package resolutions, regenerating yarn.lock, and pinning GitHub Actions to commit SHAs ([#2452](https://github.com/opensearch-project/security-dashboards-plugin/pull/2452))


### SQL


* Bump assertj-core from 3.9.1 to 3.27.7 to address CVE-2026-24400 ([#5294](https://github.com/opensearch-project/sql/pull/5294))

