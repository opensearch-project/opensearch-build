# OpenSearch and OpenSearch Dashboards 2.19.2 Release Notes


## ENHANCEMENTS


### Opensearch Query Insights


* Use ClusterStateRequest with index pattern when searching for expired local indices ([#262](https://github.com/opensearch-project/query-insights/pull/262))
* Add strict hash check on top queries indices ([#266](https://github.com/opensearch-project/query-insights/pull/266))
* Add default index template for query insights local index ([#255](https://github.com/opensearch-project/query-insights/pull/255))
* Fix local index deletion timing ([#297](https://github.com/opensearch-project/query-insights/pull/297))
* Skip profile queries ([#298](https://github.com/opensearch-project/query-insights/pull/298))
* Add top\_queries API verbose param ([#300](https://github.com/opensearch-project/query-insights/pull/300))


## BUG FIXES


### Opensearch Flow Framework


* Fix Config parser does not handle tenant\_id field ([#1096](https://github.com/opensearch-project/flow-framework/pull/1096))


### Opensearch Query Insights


* Fix unit test SearchQueryCategorizerTests.testFunctionScoreQuery ([#270](https://github.com/opensearch-project/query-insights/pull/270))
* Fix bugs in top\_queries, including a wrong illegal argument exception and size limit ([#293](https://github.com/opensearch-project/query-insights/pull/293))


## INFRASTRUCTURE


### Opensearch Query Insights


* Add more integ tests for exporter n reader ([#267](https://github.com/opensearch-project/query-insights/pull/267))


## DOCUMENTATION


### Opensearch Query Insights


* 2.19.2 Release Notes ([#323](https://github.com/opensearch-project/query-insights/pull/323))


## MAINTENANCE


### Opensearch Anomaly Detection Dashboards


* bumping babel and axios versions ([#1023](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1023))


### Opensearch Query Insights


* Reduce LocalIndexReader size to 50 ([#281](https://github.com/opensearch-project/query-insights/pull/281))


