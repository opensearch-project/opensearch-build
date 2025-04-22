# OpenSearch and OpenSearch Dashboards 3.0.0-beta1 Release Notes

## Release Highlights
* Lucene 10 is now used in OpenSearch 3.0.0-beta1.
* This is an early-stage preview of the 3.0.0 version, so expect potential bugs and unfinished features. This release is for testing purposes only, and we highly encourage users to try it out and report any issues or feedback. Please refer to the [release schedule](https://opensearch.org/releases.html) for GA release information.

### DEPRECATION NOTICES

**Deprecating support for Ubuntu Linux 20.04**
Please note that OpenSearch and OpenSearch Dashboards will deprecate support for Ubuntu Linux 20.04 as a continuous integration build image and supported operating system in an upcoming version, as Ubuntu Linux 20.04 will reach end-of-life with standard support as of April 2025 (refer to [this notice](https://ubuntu.com/blog/ubuntu-20-04-lts-end-of-life-standard-support-is-coming-to-an-end-heres-how-to-prepare) from Canonical Ubuntu). For a list of the compatible operating systems, [visit here](https://opensearch.org/docs/latest/install-and-configure/os-comp/).

**Deprecating support for Amazon Linux 2 on OpenSearch Dashboards**
Please note that OpenSearch Dashboards will deprecate support for Amazon Linux 2 as a continuous integration build image and supported operating system in an upcoming version, as Node.js 18 will reach end-of-life with support as of April 2025 (refer to [this notice](https://nodejs.org/en/blog/announcements/v18-release-announce) from nodejs.org) and newer version of Node.js LTS version (20+) will not support runtime on Amazon Linux 2. For a list of the compatible operating systems, [visit here](https://opensearch.org/docs/latest/install-and-configure/os-comp/).

## Breaking Changes

* For a full list of breaking changes and deprecated/removed features in version 3.0.0, please see details in the [meta issues](https://github.com/opensearch-project/opensearch-build/issues/5243).
  * See OpenSearch [breaking changes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.0.0-beta1.md#breaking-changes).
  * See OpenSearch Dashboards [breaking changes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.0.0-beta1.md#breaking-changes).

### OpenSearch SQL

* Unified OpenSearch PPL Data Type ([#3345](https://github.com/opensearch-project/sql/pull/3345))
* Add datetime functions ([#3473](https://github.com/opensearch-project/sql/pull/3473))
* Support CAST function with Calcite ([#3439](https://github.com/opensearch-project/sql/pull/3439))

### OpenSearch ML Commons

* Deprecate the restful API of batch ingestion (#3688)[https://github.com/opensearch-project/ml-commons/pull/3688]

### OpenSearch Dashboards Observability

* Remove support for legacy notebooks ([#2406](https://github.com/opensearch-project/dashboards-observability/pull/2406))

### OpenSearch Security

* Fix Blake2b hash implementation ([#5089](https://github.com/opensearch-project/security/pull/5089))
* Remove OpenSSL provider ([#5220](https://github.com/opensearch-project/security/pull/5220))
* Remove whitelist settings in favor of allowlist ([#5224](https://github.com/opensearch-project/security/pull/5224))


## Release Details
[OpenSearch and OpenSearch Dashboards 3.0.0-beta1](https://opensearch.org/artifacts/by-version/#release-3-0-0-alpha1) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.0.0-beta1.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.0.0-beta1.md).

## FEATURES


### OpenSearch Dashboards Anomaly Detection

* Implmentation of contextual launch ([#1005](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1005))

### OpenSearch Custom Codecs

* Bump ZTD lib version to 1.5.6-1 ([#232](https://github.com/opensearch-project/custom-codecs/pull/232))


### OpenSearch Flow Framework


* Add per-tenant provisioning throttling ([#1074](https://github.com/opensearch-project/flow-framework/pull/1074))


### OpenSearch Neural Search


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


### OpenSearch Skills


* Add web search tool ([#547](https://github.com/opensearch-project/skills/pull/547))


### OpenSearch k-NN


* [Remote Vector Index Build] Client polling mechanism, encoder check, method parameter retrieval [#2576](https://github.com/opensearch-project/k-NN/pull/2576)
* [Remote Vector Index Build] Move client to separate module [#2603](https://github.com/opensearch-project/k-NN/pull/2603)
* Add filter function to KNNQueryBuilder with unit tests and integration tests [#2599](https://github.com/opensearch-project/k-NN/pull/2599)
* [Lucene On Faiss] Add a new mode, memory-optimized-search enable user to run vector search on FAISS index under memory constrained environment. [#2630](https://github.com/opensearch-project/k-NN/pull/2630)
* [Remote Vector Index Build] Add metric collection for remote build process [#2615](https://github.com/opensearch-project/k-NN/pull/2615)
* [Explain API Support] Added Explain API support for Exact/ANN/Radial/Disk based KNN search on Faiss Engine [#2403] (https://github.com/opensearch-project/k-NN/pull/2403)


### OpenSearch SQL

* Framework of Calcite Engine: Parser, Catalog Binding and Plan Converter ([#3249](https://github.com/opensearch-project/sql/pull/3249))
* Enable Calcite by default and refactor all related ITs ([#3468](https://github.com/opensearch-project/sql/pull/3468))
* Make PPL execute successfully on Calcite engine ([#3258](https://github.com/opensearch-project/sql/pull/3258))
* Implement ppl join command with Calcite ([#3364](https://github.com/opensearch-project/sql/pull/3364))
* Implement ppl `IN` subquery command with Calcite ([#3371](https://github.com/opensearch-project/sql/pull/3371))
* Implement ppl relation subquery command with Calcite ([#3378](https://github.com/opensearch-project/sql/pull/3378))
* Implement ppl `exists` subquery command with Calcite ([#3388](https://github.com/opensearch-project/sql/pull/3388))
* Implement ppl scalar subquery command with Calcite ([#3392](https://github.com/opensearch-project/sql/pull/3392))
* Implement lookup command ([#3419](https://github.com/opensearch-project/sql/pull/3419))
* Support In expression in Calcite Engine ([#3429](https://github.com/opensearch-project/sql/pull/3429))
* Support ppl BETWEEN operator within Calcite ([#3433](https://github.com/opensearch-project/sql/pull/3433))
* Implement ppl `dedup` command with Calcite ([#3416](https://github.com/opensearch-project/sql/pull/3416))
* Support `parse` command with Calcite ([#3474](https://github.com/opensearch-project/sql/pull/3474))
* Support `TYPEOF` function with Calcite ([#3446](https://github.com/opensearch-project/sql/pull/3446))
* New output for explain endpoint with Calcite engine ([#3521](https://github.com/opensearch-project/sql/pull/3521))
* Make basic aggregation working ([#3318](https://github.com/opensearch-project/sql/pull/3318), [#3355](https://github.com/opensearch-project/sql/pull/3355))
* Push down project and filter operator into index scan ([#3327](https://github.com/opensearch-project/sql/pull/3327))
* Enable push down optimization by default ([#3366](https://github.com/opensearch-project/sql/pull/3366))
* Calcite enable pushdown aggregation ([#3389](https://github.com/opensearch-project/sql/pull/3389))
* Support multiple table and index pattern ([#3409](https://github.com/opensearch-project/sql/pull/3409))
* Support group by span over time based column with Span UDF ([#3421](https://github.com/opensearch-project/sql/pull/3421))
* Support nested field ([#3476](https://github.com/opensearch-project/sql/pull/3476))
* Execute Calcite PPL query in thread pool ([#3508](https://github.com/opensearch-project/sql/pull/3508))
* Support UDT for date, time, timestamp ([#3483](https://github.com/opensearch-project/sql/pull/3483))
* Support UDT for IP ([#3504](https://github.com/opensearch-project/sql/pull/3504))
* Support GEO\_POINT type ([#3511](https://github.com/opensearch-project/sql/pull/3511))
* Add UDF interface ([#3374](https://github.com/opensearch-project/sql/pull/3374))
* Add missing text function ([#3471](https://github.com/opensearch-project/sql/pull/3471))
* Add string builtin functions ([#3393](https://github.com/opensearch-project/sql/pull/3393))
* Add math UDF ([#3390](https://github.com/opensearch-project/sql/pull/3390))
* Add condition UDFs ([#3412](https://github.com/opensearch-project/sql/pull/3412))
* Register OpenSearchTypeSystem to OpenSearchTypeFactory ([#3349](https://github.com/opensearch-project/sql/pull/3349))
* Enable update calcite setting through \_plugins/\_query/settings API ([#3531](https://github.com/opensearch-project/sql/pull/3531))


## ENHANCEMENTS


### OpenSearch Dashboards Assistant


* Remove redundant error toast ([#515](https://github.com/opensearch-project/dashboards-assistant/pull/515))
* Add auto suggested aggregation for text2Viz ([#514](https://github.com/opensearch-project/dashboards-assistant/pull/514))
* Remove experimental badge for natural language vis ([#516](https://github.com/opensearch-project/dashboards-assistant/pull/516))
* Revert "Add http error instruction for t2ppl task" ([#519](https://github.com/opensearch-project/dashboards-assistant/pull/519))
* t2viz remove fields clause from generated PPL query ([#525](https://github.com/opensearch-project/dashboards-assistant/pull/525))
* Render Icon based on the chat status ([#523](https://github.com/opensearch-project/dashboards-assistant/pull/523))
* Add scroll load conversations ([#530](https://github.com/opensearch-project/dashboards-assistant/pull/530))
* Refactor InContext style, add white logo and remove outdated code ([#529](https://github.com/opensearch-project/dashboards-assistant/pull/529))
* Change chatbot entry point to a single button ([#540](https://github.com/opensearch-project/dashboards-assistant/pull/540))
* Support streaming output ([#493](https://github.com/opensearch-project/dashboards-assistant/pull/493))
* Update event names for t2v and feedback ([#543](https://github.com/opensearch-project/dashboards-assistant/pull/543))


### OpenSearch Anomaly Detection


* Use testclusters when testing with security ([#1414](https://github.com/opensearch-project/anomaly-detection/pull/1414))


### OpenSearch Flow Framework Dashboards


* Add new RAG + hybrid search preset ([#665](https://github.com/opensearch-project/dashboards-flow-framework/pull/665))
* Update new index mappings if selecting from existing index ([#670](https://github.com/opensearch-project/dashboards-flow-framework/pull/670))
* Persist state across Inspector tab switches; add presets dropdown ([#671](https://github.com/opensearch-project/dashboards-flow-framework/pull/671))
* Simplify ML processor form when interface is defined ([#676](https://github.com/opensearch-project/dashboards-flow-framework/pull/676))
* Cache form across ML transform types ([#678](https://github.com/opensearch-project/dashboards-flow-framework/pull/678))


### OpenSearch ML Commons

* Add parser for ModelTensorOutput and ModelTensors (#3658)[https://github.com/opensearch-project/ml-commons/pull/3658]
* Function calling for openai v1, bedrock claude and deepseek (#3712)[https://github.com/opensearch-project/ml-commons/pull/3712]
* Update highlighting model translator to adapt new model (#3699)[https://github.com/opensearch-project/ml-commons/pull/3699]
* Plan, Execute and Reflect Agent Type (#3716)[https://github.com/opensearch-project/ml-commons/pull/3716]
* Implement async mode in agent execution (#3714)[https://github.com/opensearch-project/ml-commons/pull/3714]


### OpenSearch Dashboards Observability


* Traces - Update custom source display, add toast ([#2403](https://github.com/opensearch-project/dashboards-observability/pull/2403))
* Trace to logs correlation, action icon updates ([#2398](https://github.com/opensearch-project/dashboards-observability/pull/2398))
* Traces - Custom source switch to data grid ([#2390](https://github.com/opensearch-project/dashboards-observability/pull/2390))
* Service Content/View Optimizationsc ([#2383](https://github.com/opensearch-project/dashboards-observability/pull/2383))
* Database selector in "Set Up Integration" page ([#2380](https://github.com/opensearch-project/dashboards-observability/pull/2380))
* Support custom logs correlation ([#2375] (https://github.com/opensearch-project/dashboards-observability/pull/2375))


### OpenSearch Query Insights


* Reduce LocalIndexReader size to 50 ([#281](https://github.com/opensearch-project/query-insights/pull/281))


### OpenSearch Dashboards Query Insights


* Update Default Time Range from 1 Day to 1 Hour in TopNQueries Component ([#148](https://github.com/opensearch-project/query-insights-dashboards/pull/148))
* Feat: dynamically display columns ([#103](https://github.com/opensearch-project/query-insights-dashboards/pull/103))


### OpenSearch SQL


* Support line comment and block comment in PPL ([#2806](https://github.com/opensearch-project/sql/pull/2806))
* [Calcite Engine] Function framework refactoring ([#3522](https://github.com/opensearch-project/sql/pull/3522))



### OpenSearch Security


* Optimized Privilege Evaluation ([#4380](https://github.com/opensearch-project/security/pull/4380))
* Add support for CIDR ranges in `ignore_hosts` setting ([#5099](https://github.com/opensearch-project/security/pull/5099))
* Add 'good' as a valid value for `plugins.security.restapi.password_score_based_validation_strength` ([#5119](https://github.com/opensearch-project/security/pull/5119))
* Adding stop-replication permission to `index_management_full_access` ([#5160](https://github.com/opensearch-project/security/pull/5160))
* Replace password generator step with a secure password generator action ([#5153](https://github.com/opensearch-project/security/pull/5153))
* Run Security build on image from opensearch-build ([#4966](https://github.com/opensearch-project/security/pull/4966))


## BUG FIXES


### OpenSearch Dashboards Assistant


* Remove experimental badge for vis-nlp ([#528](https://github.com/opensearch-project/dashboards-assistant/pull/528))
* Fix vertically alignment of alert insights popover title ([#526](https://github.com/opensearch-project/dashboards-assistant/pull/526))
* Change alert summary icon color to white ([#533](https://github.com/opensearch-project/dashboards-assistant/pull/533))
* Fix query assistant menu disappear due to upstream method signature change([#541]https://github.com/opensearch-project/dashboards-assistant/pull/541)
* Fix .plugins-ml-memory-meta not found when get conversations ([#542](https://github.com/opensearch-project/dashboards-assistant/pull/542))


### OpenSearch Anomaly Detection


* Distinguish local cluster when local name is same as remote ([#1446](https://github.com/opensearch-project/anomaly-detection/pull/1446))


### OpenSearch Dashboards Anomaly Detection


* Switching fieldcaps api to utilize js client ([#984](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/984))
* Update namespace for alerting plugin to avoid conflict with alerting ([#1003](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1003))
* Fix remote cluster bug when remote and local have same name ([#1007](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1007))
* Display selected clusters correctly on edit page ([#1011](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1011))


### OpenSearch Common Utils


* Escape/Unescape pipe UserInfo in ThreadContext ([#801](https://github.com/opensearch-project/common-utils/pull/801))


### OpenSearch Dashboards Reporting


* Updated the optional parameters for timefrom and timeto to resolve incorrect report generation scenarios ([#554](https://github.com/opensearch-project/dashboards-reporting/pull/554))


### OpenSearch Flow Framework


* Change REST status codes for RBAC and provisioning ([#1083](https://github.com/opensearch-project/flow-framework/pull/1083))
* Fix Config parser does not handle tenant\_id field ([#1096](https://github.com/opensearch-project/flow-framework/pull/1096))
* Complete action listener on failed synchronous workflow provisioning ([#1098](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/1098))


### OpenSearch Dashboards Flow Framework


* Fix missed UI autofilling after JSON Lines change ([#672](https://github.com/opensearch-project/dashboards-flow-framework/pull/672))


### OpenSearch Index Management


* Fix issue in Docker Security Tests where qualifier is not being parsed correctly ([#1401](https://github.com/opensearch-project/index-management/pull/1401))


### OpenSearch Index Management Dashboards Plugin


* Fixed CVE: Updated elliptic dependency resolution ([#1290](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1290))


### OpenSearch ML Commons


* Fixing the circuit breaker issue for remote model (#3652)[https://github.com/opensearch-project/ml-commons/pull/3652]
* Fix compilation error (#3667)[https://github.com/opensearch-project/ml-commons/pull/3667]
* Revert CI workflow changes (#3674)[https://github.com/opensearch-project/ml-commons/pull/3674]
* Fix config index masterkey pull up for multi-tenancy (#3700)[https://github.com/opensearch-project/ml-commons/pull/3700]


### OpenSearch Dashboards ML Commons


* Fix data source not compatible with prerelease ([#411](https://github.com/opensearch-project/ml-commons-dashboards/pull/411))


### OpenSearch Neural Search


* Remove validations for unmapped fields (text and image) in TextImageEmbeddingProcessor ([#1230](https://github.com/opensearch-project/neural-search/pull/1230))


### OpenSearch Dashboards Observability


* Application Analytics - Flaky cypress fix ([#2402](https://github.com/opensearch-project/dashboards-observability/pull/2402))
* Traces table fix for invalid date ([#2399](https://github.com/opensearch-project/dashboards-observability/pull/2399))
* Custom Traces- Sorting/Toast ([#2397](https://github.com/opensearch-project/dashboards-observability/pull/2397))
* Event Analytics - Cypress flaky fix ([#2395](https://github.com/opensearch-project/dashboards-observability/pull/2395))
* Services to Traces - Flyout redirection ([#2392](https://github.com/opensearch-project/dashboards-observability/pull/2392))


### OpenSearch Learning To Rank Base


* Add a model parser for xgboost (for the correct serialization format) ((#151)[https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/151])


### OpenSearch Remote Metadata Sdk


* Fix version conflict check for update ([#114](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/114))
* Use SdkClientDelegate's classloader for ServiceLoader ([#121](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/121))
* Ensure consistent reads on DynamoDB getItem calls ([#128](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/128))
* Return 404 for Index not found on Local Cluster search ([#130](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/130))


### OpenSearch Security Analytics


* Remove overrides of preserveIndicesUponCompletion ([#1498](https://github.com/opensearch-project/security-analytics/pull/1498))


### OpenSearch Skills


* Fix list bug of PPLTool when pass empty list ([#541](https://github.com/opensearch-project/skills/pull/541))



### OpenSearch Security


* Fix version matcher string in demo config installer ([#5157](https://github.com/opensearch-project/security/pull/5157)
* Escape pipe character for injected users ([#5175](https://github.com/opensearch-project/security/pull/5175))
* Assume default of v7 models if \_meta portion is not present ([#5193](https://github.com/opensearch-project/security/pull/5193))
* Fixed IllegalArgumentException when building stateful index privileges ([#5217](https://github.com/opensearch-project/security/pull/5217)
* DlsFlsFilterLeafReader::termVectors implementation causes assertion errors for users with FLS/FM active ([#5243](https://github.com/opensearch-project/security/pull/5243)


### OpenSearch k-NN


* Fixing bug to prevent NullPointerException while doing PUT mappings ([#2556](https://github.com/opensearch-project/k-NN/issues/2556))
* Add index operation listener to update translog source ([#2629](https://github.com/opensearch-project/k-NN/pull/2629))
* Add parent join support for faiss hnsw cagra ([#2647](https://github.com/opensearch-project/k-NN/pull/2647))
* [Remote Vector Index Build] Fix bug to support `COSINESIMIL` space type ([#2627](https://github.com/opensearch-project/k-NN/pull/2627))
* Disable doc value storage for vector field storage ([#2646](https://github.com/opensearch-project/k-NN/pull/2646))


### OpenSearch SQL


* Fix execution errors caused by plan gap ([#3350](https://github.com/opensearch-project/sql/pull/3350))
* Support push down text field correctly ([#3376](https://github.com/opensearch-project/sql/pull/3376))
* Fix the join condition resolving bug introduced by IN subquery implementation ([#3377](https://github.com/opensearch-project/sql/pull/3377))
* Fix flaky tests ([#3456](https://github.com/opensearch-project/sql/pull/3456))
* Fix antlr4 parser issues ([#3492](https://github.com/opensearch-project/sql/pull/3492))
* Fix CSV handling of embedded crlf ([#3515](https://github.com/opensearch-project/sql/pull/3515))
* Fix return types of MOD and DIVIDE UDFs ([#3513](https://github.com/opensearch-project/sql/pull/3513))
* Fix varchar bug ([#3518](https://github.com/opensearch-project/sql/pull/3518))
* Fix text function IT for locate and strcmp ([#3482](https://github.com/opensearch-project/sql/pull/3482))
* Fix IT and CI, revert alias change ([#3423](https://github.com/opensearch-project/sql/pull/3423))
* Fix CalcitePPLJoinIT ([#3369](https://github.com/opensearch-project/sql/pull/3369))
* Keep aggregation in Calcite consistent with current PPL behavior ([#3405](https://github.com/opensearch-project/sql/pull/3405))
* Revert result ordering of `stats-by` ([#3427](https://github.com/opensearch-project/sql/pull/3427))
* Correct the precedence for logical operators ([#3435](https://github.com/opensearch-project/sql/pull/3435))
* Use correct timezone name ([#3517](https://github.com/opensearch-project/sql/pull/3517))


## INFRASTRUCTURE


### OpenSearch Dashboards Assistant


* Fix failed UTs with OSD 3.0 ([#527](https://github.com/opensearch-project/dashboards-assistant/pull/527))
* Fix empty codecov report in CI([#547](https://github.com/opensearch-project/dashboards-assistant/pull/547))


### OpenSearch Anomaly Detection


* Adding dual cluster arg to gradle run ([#1441](https://github.com/opensearch-project/anomaly-detection/pull/1441))


### OpenSearch Dashboards Anomaly Detection


* Change gradle run to dualcluster is true ([#998](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/998))


### OpenSearch Neural Search


* [3.0] Update neural-search for OpenSearch 3.0 beta compatibility ([#1245](https://github.com/opensearch-project/neural-search/pull/1245))


### OpenSearch Dashboards Observability


* Improve error handling when setting up and reading a new integration ([#2387](https://github.com/opensearch-project/dashboards-observability/pull/2387))


### OpenSearch Dashboards Query Insights

* Update 3.0.0 qualifier from alpha1 to beta1 ([#154](https://github.com/opensearch-project/query-insights-dashboards/pull/154))


### OpenSearch k-NN


* Add github action to run ITs against remote index builder ([2620](https://github.com/opensearch-project/k-NN/pull/2620))


### OpenSearch SQL


* Build integration test framework ([#3342](https://github.com/opensearch-project/sql/pull/3342))
* Set bouncycastle version inline ([#3469](https://github.com/opensearch-project/sql/pull/3469))
* Use entire shadow jar to fix IT ([#3447](https://github.com/opensearch-project/sql/pull/3447))
* Separate with/without pushdown ITs ([#3413](https://github.com/opensearch-project/sql/pull/3413))


## DOCUMENTATION


### OpenSearch ML Commons


* Add standard blueprint for vector search (#3659)[https://github.com/opensearch-project/ml-commons/pull/3659]
* Add blueprint for Claude 3.7 on Bedrock (#3584)[https://github.com/opensearch-project/ml-commons/pull/3584]


### OpenSearch Query Insights


* 3.0.0.0-beta1 Release Notes ([#294](https://github.com/opensearch-project/query-insights/pull/294))


### OpenSearch Dashboards Query Insights


* 3.0.0.0-beta1 Release Notes ([#157](https://github.com/opensearch-project/query-insights-dashboards/pull/157))


### OpenSearch Remote Metadata Sdk


* Add a developer guide ([#124](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/124))


### OpenSearch SQL


* Documentation for PPL new engine (V3) and limitations of 3.0.0 Beta ([#3488](https://github.com/opensearch-project/sql/pull/3488))


## MAINTENANCE


### OpenSearch Dashboards Assistant


* Bump version to 3.0.0.0-beta1 ([#521](https://github.com/opensearch-project/dashboards-assistant/pull/521))


### OpenSearch Alerting


* Update version qualifier to beta1. ([#1816](https://github.com/opensearch-project/alerting/pull/1816))


### OpenSearch Dashboards Alerting


* Update version qualifier to beta1. ([#1227](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1227))


### OpenSearch Anomaly Detection


* Increment version to 3.0.0.0-beta1 ([#1444](https://github.com/opensearch-project/anomaly-detection/pull/1444))


### OpenSearch Dashboards Anomaly Detection


* Fix(security): Upgrade axios to 1.8.2 to fix SSRF ([#991](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/991))
* Update @babel/runtime to >=7.26.10 ([#993](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/993))
* Increment version to 3.0.0.0-beta1 ([#1004](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1004))


### OpenSearch Asynchronous Search


* Update main branch for 3.0.0.0-beta1 ([#716](https://github.com/opensearch-project/asynchronous-search/pull/716))


### OpenSearch Common Utils


* Change 3.0.0 qualifier from alpha1 to beta1 ( ([#808](https://github.com/opensearch-project/common-utils/pull/808))


### OpenSearch Cross Cluster Replication


* Version bump to opensearch-3.0.0-beta1 and replaced usage of deprecated classes


### OpenSearch Dashboards Maps


* Bump up version to 3.0.0-beta1 [#716](https://github.com/opensearch-project/dashboards-maps/pull/716)


### OpenSearch Dashboards Notifications


* Update version qualifier to beta1. ([#336](https://github.com/opensearch-project/dashboards-notifications/pull/336))


### OpenSearch Dashboards Reporting


* Remove cypress and babel jest from project dependency list ([#559](https://github.com/opensearch-project/dashboards-reporting/pull/559))
* CVE fix for babel/helpers and babel/runtime ([#558](https://github.com/opensearch-project/dashboards-reporting/pull/558))
* Bump dashboards reporting to version 3.0.0.0-beta1 ([#557](https://github.com/opensearch-project/dashboards-reporting/pull/557))
* Bump jspdf to version 3.0.1 ([#555](https://github.com/opensearch-project/dashboards-reporting/pull/555))
* CVE fix for elliptic dependency and update to release notes to reflect changes ([#550](https://github.com/opensearch-project/dashboards-reporting/pull/550))
* Minor CI updates and workflow fixes ([#548](https://github.com/opensearch-project/dashboards-reporting/pull/548))


### OpenSearch Dashboards Search Relevance


* Increment version to 3.0.0.0-beta1 ([#491](https://github.com/opensearch-project/dashboards-search-relevance/pull/491))


### OpenSearch Flow Framework


* Migrate from BC to BCFIPS libraries ([#1087](https://github.com/opensearch-project/flow-framework/pull/1087))


### OpenSearch Geospatial


* Persist necessary license and developer information in maven pom ([#732](https://github.com/opensearch-project/geospatial/pull/732))


### OpenSearch Index Management


* Update 3.0.0 qualifier from alpha1 to beta1 ([#1398](https://github.com/opensearch-project/index-management/pull/1398))


### OpenSearch Dashboards Index Management


* Updated 3.0.0 qualifier from alpha1 to beta1 ([#1293](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1293))


### OpenSearch Job Scheduler


* Increment version to 3.0.0-beta1 [#752](https://github.com/opensearch-project/job-scheduler/pull/752).
* Dependabot: bump com.google.guava:failureaccess from 1.0.2 to 1.0.3 [#750](https://github.com/opensearch-project/job-scheduler/pull/750).
* Dependabot: bump com.google.googlejavaformat:google-java-format [#753](https://github.com/opensearch-project/job-scheduler/pull/753).
* Dependabot: bump com.netflix.nebula.ospackage from 11.11.1 to 11.11.2 [#754](https://github.com/opensearch-project/job-scheduler/pull/754).


### OpenSearch ML Commons


* Remove forcing log4j version to 2.24.2 (#3647)[https://github.com/opensearch-project/ml-commons/pull/3647]
* Improve test coverage for MLHttpClientFactory.java (#3644)[https://github.com/opensearch-project/ml-commons/pull/3644]
* Improve test coverage for MLEngineClassLoader class (#3679)[https://github.com/opensearch-project/ml-commons/pull/3679]
* Typo: MLTaskDispatcher \_cluster/settings api (#3694)[https://github.com/opensearch-project/ml-commons/pull/3694]
* Add more logs to toubleshot flaky test (#3543)[https://github.com/opensearch-project/ml-commons/pull/3543]
* Add package for security test (#3698)[https://github.com/opensearch-project/ml-commons/pull/3698]
* Add sdk implementation to the connector search (#3704)[https://github.com/opensearch-project/ml-commons/pull/3704]
* Sdk client implementation for search connector, model group and task (#3707)[https://github.com/opensearch-project/ml-commons/pull/3707]


### OpenSearch ML Commons Dashboards


* Bump version to 3.0.0.0-beta1 ([#409](https://github.com/opensearch-project/ml-commons-dashboards/pull/409))


### OpenSearch Notifications


* [Release 3.0] Update version qualifier to beta1. ([#1011](https://github.com/opensearch-project/notifications/pull/1011))


### OpenSearch Observability


* Bump version 3.0.0-beta1-SNAPSHOT ([#1914] (https://github.com/opensearch-project/observability/pull/1914))


### OpenSearch Dashboards Observability


* Adding husky .only check hook to test files ([#2400](https://github.com/opensearch-project/dashboards-observability/pull/2400))
* Remove cypress to make it refer to the version used in OpenSearch Dashboard to fix build failure ([#2405](https://github.com/opensearch-project/dashboards-observability/pull/2405))
* Fix CVE issue for dependency prismjs ([#2404](https://github.com/opensearch-project/dashboards-observability/pull/2404))
* Bump dashboards observability to version 3.0.0.0-beta1 ([#2401](https://github.com/opensearch-project/dashboards-observability/pull/2401))
* Update README.md for unblocking PRs to be merged ([#2394](https://github.com/opensearch-project/dashboards-observability/pull/2394))
* Bump dep serialize-javascript version to 6.0.2 and @babel/runtime to 7.26.10 ([#2389](https://github.com/opensearch-project/dashboards-observability/pull/2389))
* Minor CI updates and workflow fixes ([#2388](https://github.com/opensearch-project/dashboards-observability/pull/2388))


### OpenSearch Learning To Rank Base


* Update 3.0.0 qualifier from alpha1 to beta1 ((#154)[https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/154])


### OpenSearch Performance Analyzer


* Bumps plugin version to 3.0.0.0-beta1 in PA ([#794](https://github.com/opensearch-project/performance-analyzer/pull/794))


### OpenSearch Query Insights


* Update 3.0.0 qualifier from alpha1 to beta1 ([#290](https://github.com/opensearch-project/query-insights/pull/290))


### OpenSearch Dashboards Query Insights


* Update babel/runtime version ([#156](https://github.com/opensearch-project/query-insights-dashboards/pull/156))


### OpenSearch Query Workbench


* Remove cypress version to make it uses the version in OpenSearch Dashboards ([#463] (https://github.com/opensearch-project/dashboards-query-workbench/pull/463))
* Bump dashboards query workbench to version 3.0.0.0-beta1 ([#462] (https://github.com/opensearch-project/dashboards-query-workbench/pull/462))
* Remove download JSON feature ([#460](https://github.com/opensearch-project/dashboards-query-workbench/pull/460))
* Minor CI updates and workflow fixes ([#459](https://github.com/opensearch-project/dashboards-query-workbench/pull/459))


### OpenSearch Reporting


* Bump version 3.0.0-beta1-SNAPSHOT ([#1083] (https://github.com/opensearch-project/reporting/pull/1083))


### OpenSearch Security Analytics


* Update version qualifier to beta1. ([#1500](https://github.com/opensearch-project/security-analytics/pull/1500))


### OpenSearch Dashboards Security Analytics


* Update version qualifier to beta1. ([#1275](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1275))
* Fix CVE 2025 27789. ([#1276](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1276))


### OpenSearch Dashboards Security


* Remove typescript dependency ([#2198](https://github.com/opensearch-project/security-dashboards-plugin/pull/2198))
* Bump babel ([#2200](https://github.com/opensearch-project/security-dashboards-plugin/pull/2200))
* Fix integration tests by removing sample flight data download ([#2202](https://github.com/opensearch-project/security-dashboards-plugin/pull/2202))


### OpenSearch k-NN


* Update minimum required CMAKE version in NMSLIB ([#2635](https://github.com/opensearch-project/k-NN/pull/2635))
* Revert CMake version bump, instead add CMake policy version flag to build task to support modern CMake builds ([#2645](https://github.com/opensearch-project/k-NN/pull/2645/files))


### OpenSearch SQL


* CVE-2024-57699 High: Fix json-smart vulnerability ([#3484](https://github.com/opensearch-project/sql/pull/3484))
* Adding new maintainer @qianheng-aws ([#3509](https://github.com/opensearch-project/sql/pull/3509))
* Bump SQL main to version 3.0.0.0-beta1 ([#3489](https://github.com/opensearch-project/sql/pull/3489))
* Merge feature/calcite-engine to main ([#3448](https://github.com/opensearch-project/sql/pull/3448))
* Merge main for OpenSearch 3.0 release ([#3434](https://github.com/opensearch-project/sql/pull/3434))


### OpenSearch Security


* Update AuditConfig.DEPRECATED\_KEYS deprecation message to match 4.0 ([#5155](https://github.com/opensearch-project/security/pull/5155))
* Update deprecation message for `_opendistro/_security/kibanainfo` API ([#5156](https://github.com/opensearch-project/security/pull/5156))
* Update DlsFlsFilterLeafReader to reflect Apache Lucene 10 API changes ([#5123](https://github.com/opensearch-project/security/pull/5123))
* Adapt to core changes in `SecureTransportParameters` ([#5122](https://github.com/opensearch-project/security/pull/5122))
* Format SSLConfigConstants.java and fix typos ([#5145](https://github.com/opensearch-project/security/pull/5145))
* Remove typo in `AbstractAuditlogUnitTest` ([#5130](https://github.com/opensearch-project/security/pull/5130))
* Update Andriy Redko's affiliation ([#5133](https://github.com/opensearch-project/security/pull/5133))
* Upgrade common-utils version to `3.0.0.0-alpha1-SNAPSHOT` ([#5137](https://github.com/opensearch-project/security/pull/5137))
* Bump Spring version ([#5173](https://github.com/opensearch-project/security/pull/5173))
* Bump org.checkerframework:checker-qual from 3.49.0 to 3.49.2 ([#5162](https://github.com/opensearch-project/security/pull/5162)) ([#5247](https://github.com/opensearch-project/security/pull/5247))
* Bump org.mockito:mockito-core from 5.15.2 to 5.17.0 ([#5161](https://github.com/opensearch-project/security/pull/5161)) ([#5248](https://github.com/opensearch-project/security/pull/5248))
* Bump org.apache.camel:camel-xmlsecurity from 3.22.3 to 3.22.4 ([#5163](https://github.com/opensearch-project/security/pull/5163))
* Bump ch.qos.logback:logback-classic from 1.5.16 to 1.5.17 ([#5149](https://github.com/opensearch-project/security/pull/5149))
* Bump org.awaitility:awaitility from 4.2.2 to 4.3.0 ([#5126](https://github.com/opensearch-project/security/pull/5126))
* Bump org.springframework.kafka:spring-kafka-test from 3.3.2 to 3.3.4 ([#5125](https://github.com/opensearch-project/security/pull/5125)) ([#5201](https://github.com/opensearch-project/security/pull/5201))
* Bump org.junit.jupiter:junit-jupiter from 5.11.4 to 5.12.0 ([#5127](https://github.com/opensearch-project/security/pull/5127))
* Bump Gradle to 8.13 ([#5148](https://github.com/opensearch-project/security/pull/5148))
* Bump Spring version to fix CVE-2024-38827 ([#5173](https://github.com/opensearch-project/security/pull/5173))
* Bump com.google.guava:guava from 33.4.0-jre to 33.4.6-jre ([#5205](https://github.com/opensearch-project/security/pull/5205)) ([#5228](https://github.com/opensearch-project/security/pull/5228))
* Bump ch.qos.logback:logback-classic from 1.5.17 to 1.5.18 ([#5204](https://github.com/opensearch-project/security/pull/5204))
* Bump spring\_version from 6.2.4 to 6.2.5 ([#5203](https://github.com/opensearch-project/security/pull/5203))
* Bump bouncycastle\_version from 1.78 to 1.80 ([#5202](https://github.com/opensearch-project/security/pull/5202))
* Remove java version check for reflection args in build.gradle ([#5218](https://github.com/opensearch-project/security/pull/5218))
* Improve coverage: Adding tests for ConfigurationRepository class ([#5206](https://github.com/opensearch-project/security/pull/5206))
* Refactor InternalAuditLogTest to use Awaitility ([#5214](https://github.com/opensearch-project/security/pull/5214))
* Bump com.google.googlejavaformat:google-java-format from 1.25.2 to 1.26.0 ([#5231](https://github.com/opensearch-project/security/pull/5231))
* Bump open\_saml\_shib\_version from 9.1.3 to 9.1.4 ([#5230](https://github.com/opensearch-project/security/pull/5230))
* Bump com.carrotsearch.randomizedtesting:randomizedtesting-runner from 2.8.2 to 2.8.3 ([#5229](https://github.com/opensearch-project/security/pull/5229))
* Bump open\_saml\_version from 5.1.3 to 5.1.4 ([#5227](https://github.com/opensearch-project/security/pull/5227))
* Bump org.ow2.asm:asm from 9.7.1 to 9.8 ([#5244](https://github.com/opensearch-project/security/pull/5244))
* Bump com.netflix.nebula.ospackage from 11.11.1 to 11.11.2 ([#5246](https://github.com/opensearch-project/security/pull/5246))
* Bump com.google.errorprone:error\_prone\_annotations from 2.36.0 to 2.37.0 ([#5245](https://github.com/opensearch-project/security/pull/5245))
* More tests for FLS and field masking ([#5237](https://github.com/opensearch-project/security/pull/5237))
* Migrate from com.amazon.dlic to org.opensearch.security package ([#5223](https://github.com/opensearch-project/security/pull/5223))



### OpenSearch Skills


* Remove `space_type` in integ test to adapt to the change of k-NN plugin ([#535](https://github.com/opensearch-project/skills/pull/535))
* Bump version to 3.0.0.0-beta1 ([#543](https://github.com/opensearch-project/skills/pull/543))
* Fix jar hell for sql jar ([#545](https://github.com/opensearch-project/skills/pull/545))
* Add attributes to tools to adapt the upstream changes ([#549](https://github.com/opensearch-project/skills/pull/549))


## REFACTORING


### OpenSearch Remote Metadata Sdk


* Update o.o.client imports to o.o.transport.client ([#73](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/73))


### OpenSearch k-NN


* Switch derived source from field attributes to segment attribute [#2606](https://github.com/opensearch-project/k-NN/pull/2606)
* Migrate derived source from filter to mask [#2612](https://github.com/opensearch-project/k-NN/pull/2612)
* Consolidate MethodFieldMapper and LuceneFieldMapper into EngineFieldMapper [#2646](https://github.com/opensearch-project/k-NN/pull/2646)
