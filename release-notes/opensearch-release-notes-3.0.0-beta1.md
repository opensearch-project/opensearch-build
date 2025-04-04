# OpenSearch and OpenSearch Dashboards 3.0.0 Release Notes


## FEATURES


### Opensearch Neural Search


* Lower bound for min-max normalization technique in hybrid query ([#1195](https://github.com/opensearch-project/neural-search/pull/1195))


* Support filter function for HybridQueryBuilder and NeuralQueryBuilder ([#1206](https://github.com/opensearch-project/neural-search/pull/1206))
* Add Z Score normalization technique ([#1224](https://github.com/opensearch-project/neural-search/pull/1224))
* Support semantic sentence highlighter ([#1193](https://github.com/opensearch-project/neural-search/pull/1193))
* Optimize embedding generation in Text Embedding Processor ([#1191](https://github.com/opensearch-project/neural-search/pull/1191))
* Optimize embedding generation in Sparse Encoding Processor ([#1246](https://github.com/opensearch-project/neural-search/pull/1246))
* Optimize embedding generation in Text/Image Embedding Processor ([#1249](https://github.com/opensearch-project/neural-search/pull/1249))
* Inner hits support with hybrid query ([#1253](https://github.com/opensearch-project/neural-search/pull/1253))
* Support custom tags in semantic highlighter ([#1254](https://github.com/opensearch-project/neural-search/pull/1254))
* Add stats API ([#1256](https://github.com/opensearch-project/neural-search/pull/1256))


## ENHANCEMENTS


### Opensearch Flow Framework Dashboards


* Add new RAG + hybrid search preset ([#665](https://github.com/opensearch-project/dashboards-flow-framework/pull/665))


* Update new index mappings if selecting from existing index ([#670](https://github.com/opensearch-project/dashboards-flow-framework/pull/670))
* Persist state across Inspector tab switches; add presets dropdown ([#671](https://github.com/opensearch-project/dashboards-flow-framework/pull/671))
* Simplify ML processor form when interface is defined ([#676](https://github.com/opensearch-project/dashboards-flow-framework/pull/676))
* Cache form across ML transform types ([#678](https://github.com/opensearch-project/dashboards-flow-framework/pull/678))


### Opensearch ML Common


* Add parser for ModelTensorOutput and ModelTensors (#3658)[https://github.com/opensearch-project/ml-commons/pull/3658]


## BUG FIXES


### Opensearch Common Utils


* Escape/Unescape pipe UserInfo in ThreadContext ([#801](https://github.com/opensearch-project/common-utils/pull/801))


### Opensearch Flow Framework Dashboards


* Fix missed UI autofilling after JSON Lines change ([#672](https://github.com/opensearch-project/dashboards-flow-framework/pull/672))


### Opensearch ML Common


* fixing the circuit breaker issue for remote model (#3652)[https://github.com/opensearch-project/ml-commons/pull/3652]
* fix compilation error (#3667)[https://github.com/opensearch-project/ml-commons/pull/3667]
* revert CI workflow changes (#3674)[https://github.com/opensearch-project/ml-commons/pull/3674]


### Opensearch Neural Search


* Remove validations for unmapped fields (text and image) in TextImageEmbeddingProcessor ([#1230](https://github.com/opensearch-project/neural-search/pull/1230))


### Opensearch Opensearch Learning To Rank Base


* Add a model parser for xgboost (for the correct serialization format) ((#151)[https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/151])


### Opensearch Security Analytics


* Remove overrides of preserveIndicesUponCompletion ([#1498](https://github.com/opensearch-project/security-analytics/pull/1498))


## INFRASTRUCTURE


### Opensearch Neural Search


* [3.0] Update neural-search for OpenSearch 3.0 beta compatibility ([#1245](https://github.com/opensearch-project/neural-search/pull/1245))


## DOCUMENTATION


### Opensearch ML Common


* Add standard blueprint for vector search (#3659)[https://github.com/opensearch-project/ml-commons/pull/3659]


## MAINTENANCE


### Opensearch Alerting


* Update version qualifier to beta1. ([#1816](https://github.com/opensearch-project/alerting/pull/1816))


### Opensearch Alerting Dashboards Plugin


* Update version qualifier to beta1. ([#1227](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1227))


### Opensearch Common Utils


* Change 3.0.0 qualifier from alpha1 to beta1 ( ([#808](https://github.com/opensearch-project/common-utils/pull/808))


### Opensearch Cross Cluster Replication


* Version bump to opensearch-3.0.0-beta1 and replaced usage of deprecated classes


### Opensearch Dashboards Notifications


* Update version qualifier to beta1. ([#336](https://github.com/opensearch-project/dashboards-notifications/pull/336))


### Opensearch Dashboards Search Relevance


* Increment version to 3.0.0.0-beta1 ([#491](https://github.com/opensearch-project/dashboards-search-relevance/pull/491))


### Opensearch Geospatial


* Persist necessary license and developer information in maven pom ([#732](https://github.com/opensearch-project/geospatial/pull/732))


### Opensearch ML Common


* Remove forcing log4j version to 2.24.2 (#3647)[https://github.com/opensearch-project/ml-commons/pull/3647]
* Improve test coverage for MLHttpClientFactory.java (#3644)[https://github.com/opensearch-project/ml-commons/pull/3644]
* Improve test coverage for MLEngineClassLoader class (#3679)[https://github.com/opensearch-project/ml-commons/pull/3679]


### Opensearch Notifications


* [Release 3.0] Update version qualifier to beta1. ([#1011](https://github.com/opensearch-project/notifications/pull/1011))


### Opensearch Opensearch Learning To Rank Base


* Update 3.0.0 qualifier from alpha1 to beta1 ((#154)[https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/154])


### Opensearch Performance Analyzer


* Bumps plugin version to 3.0.0.0-beta1 in PA ([#794](https://github.com/opensearch-project/performance-analyzer/pull/794))


### Opensearch Security Analytics


* Update version qualifier to beta1. ([#1500](https://github.com/opensearch-project/security-analytics/pull/1500))


### Opensearch Security Analytics Dashboards


* Update version qualifier to beta1. ([#1275](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1275))
* Fix CVE 2025 27789. ([#1276](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1276))


