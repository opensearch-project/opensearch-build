# OpenSearch and OpenSearch Dashboards 2.19.2 Release Notes

## Release Details

[OpenSearch and OpenSearch Dashboards 2.19.2](https://opensearch.org/versions/opensearch-2-19-2.html) includes the following enhancements, bug fixes, infrastructure, documentation and maintenance updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.2.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.2.md).


### PGP Key Update (opensearch@amazon.com):


Please note that a new PGP public key is available for verification on 2.x artifacts. OpenSearch’s current PGP public key with opensearch@amazon.com email is scheduled to expire on May 12, 2025. Please visit https://opensearch.org/verify-signatures.html to download the new public key, which is scheduled to expire on March 6, 2027.


## ENHANCEMENTS


### OpenSearch Dashboards Query Insights


* Update Default Time Range from 1 Day to 1 Hour in TopNQueries Component ([#148](https://github.com/opensearch-project/query-insights-dashboards/pull/148))


### OpenSearch Query Insights


* Use ClusterStateRequest with index pattern when searching for expired local indices ([#262](https://github.com/opensearch-project/query-insights/pull/262))
* Add strict hash check on top queries indices ([#266](https://github.com/opensearch-project/query-insights/pull/266))
* Add default index template for query insights local index ([#255](https://github.com/opensearch-project/query-insights/pull/255))
* Fix local index deletion timing ([#297](https://github.com/opensearch-project/query-insights/pull/297))
* Skip profile queries ([#298](https://github.com/opensearch-project/query-insights/pull/298))
* Add top\_queries API verbose param ([#300](https://github.com/opensearch-project/query-insights/pull/300))


## BUG FIXES


### OpenSearch Dashboards Observability


* [Bug] Traces/Services remove toast message on empty data ([#2346](https://github.com/opensearch-project/dashboards-observability/pull/2346))


### OpenSearch Dashboards Query Insights


* Fix Placeholder metric Not Replaced with Actual Metric Type ([#140](https://github.com/opensearch-project/query-insights-dashboards/pull/140))
* Fix duplicated requests on refreshing the overview ([#138](https://github.com/opensearch-project/query-insights-dashboards/pull/138))


### OpenSearch Flow Framework


* Fix Config parser does not handle tenant\_id field ([#1096](https://github.com/opensearch-project/flow-framework/pull/1096))


### OpenSearch Query Insights


* Fix unit test SearchQueryCategorizerTests.testFunctionScoreQuery ([#270](https://github.com/opensearch-project/query-insights/pull/270))
* Fix bugs in top\_queries, including a wrong illegal argument exception and size limit ([#293](https://github.com/opensearch-project/query-insights/pull/293))


## INFRASTRUCTURE


### OpenSearch Query Insights


* Add more integ tests for exporter n reader ([#267](https://github.com/opensearch-project/query-insights/pull/267))


## DOCUMENTATION


### OpenSearch Dashboards Query Insights


* 2.19.2 Release Notes ([#187](https://github.com/opensearch-project/query-insights-dashboards/pull/187))


### OpenSearch Dashboards Security Analytics


* Added 2.19.2 release notes. ([#1291](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1291))


### OpenSearch Query Insights


* 2.19.2 Release Notes ([#323](https://github.com/opensearch-project/query-insights/pull/323))


## MAINTENANCE


### OpenSearch Anomaly Detection Dashboards


* Bumping babel and axios versions ([#1023](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1023))


### OpenSearch Dashboards Observability


* [AUTO] Increment version to 2.19.2.0 ([#2414](https://github.com/opensearch-project/dashboards-observability/pull/2414))
* [AUTO] Increment version to 2.19.1.0 ([#2356](https://github.com/opensearch-project/dashboards-observability/pull/2356))
* CVE Fix for CVE-2025-27789 and CVE-2024-53382 ([#2428](https://github.com/opensearch-project/dashboards-observability/pull/2428))


### OpenSearch Dashboards Query Insights


* Delete package-lock.json as it is duplicate with yarn.lock ([#133](https://github.com/opensearch-project/query-insights-dashboards/pull/133))
* Fix CVE-2025-27789 ([#181](https://github.com/opensearch-project/query-insights-dashboards/pull/181))


### OpenSearch Dashboards Reporting


* CVE Fix for CVE-2025-27789 ([#568](https://github.com/opensearch-project/dashboards-reporting/pull/568))
* Bump jspdf to 3.0.1 ([#555](https://github.com/opensearch-project/dashboards-reporting/pull/555))


### OpenSearch Dashboards Security


* Bump babel to address: CVE-2025-27789 ([#2224](https://github.com/opensearch-project/security-dashboards-plugin/pull/2224))


### OpenSearch Dashboards Security Analytics


* Increment version to 2.19.2.0 ([#1283](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1283))
* Fix CVEs ([#1290](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1290))


### OpenSearch ML Commons


* Fixing security integ test ([#3646](https://github.com/opensearch-project/ml-commons/pull/3646))


### OpenSearch Query Insights


* Reduce LocalIndexReader size to 50 ([#281](https://github.com/opensearch-project/query-insights/pull/281))


