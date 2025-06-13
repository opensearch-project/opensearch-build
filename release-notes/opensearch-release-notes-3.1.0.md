# OpenSearch and OpenSearch Dashboards 3.1.0 Release Notes


## FEATURES


### Opensearch Dashboards Search Relevance


* Add search relevance workbench features ([#533](https://github.com/opensearch-project/dashboards-search-relevance/pull/533))


### Opensearch Flow Framework Dashboards


* Integrate preview panel into inspector panel ([#722](https://github.com/opensearch-project/dashboards-flow-framework/pull/722))


* Refactor form navigation to left panel ([#737](https://github.com/opensearch-project/dashboards-flow-framework/pull/737))
* Added workflow template for Semantic Search using Sparse Encoders ([#742](https://github.com/opensearch-project/dashboards-flow-framework/pull/742))


### Opensearch Neural Search


* Implement analyzer based neural sparse query ([#1088](https://github.com/opensearch-project/neural-search/pull/1088) [#1279](https://github.com/opensearch-project/neural-search/pull/1279))


* [Semantic Field] Add semantic mapping transformer. ([#1276](https://github.com/opensearch-project/neural-search/pull/1276))
* [Semantic Field] Add semantic ingest processor. ([#1309](https://github.com/opensearch-project/neural-search/pull/1309))
* [Semantic Field] Implement the query logic for the semantic field. ([#1315](https://github.com/opensearch-project/neural-search/pull/1315))
* [Semantic Field] Enhance semantic field to allow to enable/disable chunking. ([#1337](https://github.com/opensearch-project/neural-search/pull/1337))
* [Semantic Field] Implement the search analyzer support for semantic field at query time. ([#1341](https://github.com/opensearch-project/neural-search/pull/1341))
* Add `FixedCharLengthChunker` for character length-based chunking ([#1342](https://github.com/opensearch-project/neural-search/pull/1342))
* [Semantic Field] Implement the search analyzer support for semantic field at semantic field index creation time. ([#1367](https://github.com/opensearch-project/neural-search/pull/1367))
* [Hybrid] Add collapse functionality to hybrid query ([#1345](https://github.com/opensearch-project/neural-search/pull/1345))


### Opensearch k-NN


* Introduce memory optimized search for Faiss binary index types [#2735](https://github.com/opensearch-project/k-NN/pull/2735)


## ENHANCEMENTS


### Opensearch Anomaly Detection


* Use Centralized Resource Access Control framework provided by security plugin ([#1400](https://github.com/opensearch-project/anomaly-detection/pull/1400))


* Introduce state machine, separate config index, improve suggest/validate APIs, and persist cold-start results for run-once visualization ([#1479](https://github.com/opensearch-project/anomaly-detection/pull/1479))


### Opensearch Flow Framework Dashboards


* Misc improvements IV ([#743](https://github.com/opensearch-project/dashboards-flow-framework/pull/743))


* Update README.md ([#744](https://github.com/opensearch-project/dashboards-flow-framework/pull/744))


### Opensearch ML Common


* Support persisting MCP tools in system index (#3874)[https://github.com/opensearch-project/ml-commons/pull/3874]
* [Agent] PlanExecuteReflect: Return memory early to track progress (#3884)[https://github.com/opensearch-project/ml-commons/pull/3884]
* Add space type mapping for pre-trained embedding models, add new additional\_config field and BaseModelConfig class (#3786)[https://github.com/opensearch-project/ml-commons/pull/3786]
* support customized message endpoint and addressing comments (#3810)[https://github.com/opensearch-project/ml-commons/pull/3810]
* Add custom SSE endpoint for the MCP Client (#3891)[https://github.com/opensearch-project/ml-commons/pull/3891]
* Expose Update Agent API (#3820)[https://github.com/opensearch-project/ml-commons/pull/3902]
* Use function calling for existing LLM interfaces (#3888)[https://github.com/opensearch-project/ml-commons/pull/3888]
* Add error handling for plan&execute agent (#3845)[https://github.com/opensearch-project/ml-commons/pull/3845]
* Metrics framework integration with ml-commons (#3661)[https://github.com/opensearch-project/ml-commons/pull/3661]


### Opensearch Neural Search


* [Performance Improvement] Add custom bulk scorer for hybrid query (2-3x faster) ([#1289](https://github.com/opensearch-project/neural-search/pull/1289))


* [Stats] Add stats for text chunking processor algorithms ([#1308](https://github.com/opensearch-project/neural-search/pull/1308))
* Support custom weights in RRF normalization processor ([#1322](https://github.com/opensearch-project/neural-search/pull/1322))
* [Stats] Add stats tracking for semantic highlighting ([#1327](https://github.com/opensearch-project/neural-search/pull/1327))
* [Stats] Add stats for text embedding processor with different settings ([#1332](https://github.com/opensearch-project/neural-search/pull/1332))
* Validate model id and analyzer should not be provided at the same time for the neural sparse query ([#1359](https://github.com/opensearch-project/neural-search/pull/1359))
* [Stats] Add stats for score based and rank based normalization processors ([#1326](https://github.com/opensearch-project/neural-search/pull/1326))
* [Stats] Add stats tracking for semantic field ([#1362](https://github.com/opensearch-project/neural-search/pull/1362))
* [Stats] Add stats for neural query enricher, neural sparse encoding, two phase, and reranker processors ([#1343](https://github.com/opensearch-project/neural-search/pull/1343))
* [Stats] Add `include_individual_nodes`, `include_all_nodes`, `include_info` parameters to stats API ([#1360](https://github.com/opensearch-project/neural-search/pull/1360))
* [Stats] Add stats for custom flags set in ingest processors ([#1378](https://github.com/opensearch-project/neural-search/pull/1378))


### Opensearch Query Insights


* Add metric labels to historical data ([#326](https://github.com/opensearch-project/query-insights/pull/326))
* Consolidate grouping settings ([#336](https://github.com/opensearch-project/query-insights/pull/336))
* Add setting to exclude certain indices from insight query ([#308](https://github.com/opensearch-project/query-insights/pull/308))
* asynchronous search operations in reader ([#344](https://github.com/opensearch-project/query-insights/pull/344))
* Added isCancelled field in Live Queries API ([#355](https://github.com/opensearch-project/query-insights/pull/355))


### Opensearch Query Insights Dashboards


* Remove duplicate requests on overview page loading ([#179](https://github.com/opensearch-project/query-insights-dashboards/pull/179))
* New Live Queries Dashboard ([#199](https://github.com/opensearch-project/query-insights-dashboards/pull/199))
* New Workload Management dashboard ([#155](https://github.com/opensearch-project/query-insights-dashboards/pull/155))
* Add unit tests for wlm dashboard ([#209](https://github.com/opensearch-project/query-insights-dashboards/pull/209))


### Opensearch k-NN


* Removing redundant type conversions for script scoring for hamming space with binary vectors [#2351](https://github.com/opensearch-project/k-NN/pull/2351)
* Apply mask operation in preindex to optimize derived source [#2704](https://github.com/opensearch-project/k-NN/pull/2704)
* [Remote Vector Index Build] Add tuned repository upload/download configurations per benchmarking results [#2662](https://github.com/opensearch-project/k-NN/pull/2662)
* [Remote Vector Index Build] Add segment size upper bound setting and prepare other settings for GA [#2734](https://github.com/opensearch-project/k-NN/pull/2734)
* [Remote Vector Index Build] Make `index.knn.remote_index_build.enabled` default to true [#2743](https://github.com/opensearch-project/k-NN/pull/2743)


## BUG FIXES


### Opensearch ML Common


* Fix connector private IP validation when executing agent without remote model (#3862)[https://github.com/opensearch-project/ml-commons/pull/3862]
* for inline model connector name isn't required (#3882)[https://github.com/opensearch-project/ml-commons/pull/3882]
* fix the tutorial in AIConnectorHelper when fetching domain\_url (#3852)[https://github.com/opensearch-project/ml-commons/pull/3852]
* Adds Json Parsing to nested object during update Query step in ML Inference Request processor (#3856)[https://github.com/opensearch-project/ml-commons/pull/3856]
* adding / as a valid character (#3854)[https://github.com/opensearch-project/ml-commons/pull/3854]
* quick fix for guava noclass issue (#3844)[https://github.com/opensearch-project/ml-commons/pull/3844]
* Fix python client not able to connect to MCP server issue (#3822)[https://github.com/opensearch-project/ml-commons/pull/3822]
* excluding circuit breaker for Agent (#3814)[https://github.com/opensearch-project/ml-commons/pull/3814]
* adding tenantId to the connector executor when this is inline connector (#3837)[https://github.com/opensearch-project/ml-commons/pull/3837]
* add validation for name and description for model model group and connector resources (#3805)[https://github.com/opensearch-project/ml-commons/pull/3805]
* Don't convert schema-defined strings to other types during validation (#3761)[https://github.com/opensearch-project/ml-commons/pull/3761]


### Opensearch Neural Search


* Fix score value as null for single shard when sorting is not done on score field ([#1277](https://github.com/opensearch-project/neural-search/pull/1277))


* Return bad request for stats API calls with invalid stat names instead of ignoring them ([#1291](https://github.com/opensearch-project/neural-search/pull/1291))
* Add validation for invalid nested hybrid query ([#1305](https://github.com/opensearch-project/neural-search/pull/1305))
* Use stack to collect semantic fields to avoid stack overflow ([#1357](https://github.com/opensearch-project/neural-search/pull/1357))
* Filter requested stats based on minimum cluster version to fix BWC tests for stats API ([#1373](https://github.com/opensearch-project/neural-search/pull/1373))


### Opensearch Query Insights


* Fix a bug in creating node level top queries request ([#365](https://github.com/opensearch-project/query-insights/pull/365))


### Opensearch Query Insights Dashboards


* Fix failing cypress tests ([#206](https://github.com/opensearch-project/query-insights-dashboards/pull/206))
* Improved the proper query status with updated live query response ([#210](https://github.com/opensearch-project/query-insights-dashboards/pull/210))


### Opensearch k-NN


* [BUGFIX] Fix KNN Quantization state cache have an invalid weight threshold [#2666](https://github.com/opensearch-project/k-NN/pull/2666)
* [BUGFIX] Fix enable rescoring when dimensions > 1000. [#2671](https://github.com/opensearch-project/k-NN/pull/2671)
* [BUGFIX] Honors slice counts for non-quantization cases [#2692](https://github.com/opensearch-project/k-NN/pull/2692)
* [BUGFIX] Block derived source enable if index.knn is false [#2702](https://github.com/opensearch-project/k-NN/pull/2702)
* Block mode and compression for indices created before version 2.17.0 [#2722](https://github.com/opensearch-project/k-NN/pull/2722)
* [BUGFIX] Avoid opening of graph file if graph is already loaded in memory [#2719](https://github.com/opensearch-project/k-NN/pull/2719)
* [BUGFIX] [Remote Vector Index Build] End remote build metrics before falling back to CPU, exception logging [#2693](https://github.com/opensearch-project/k-NN/pull/2693)
* [BUGFIX] Fix RefCount and ClearCache in some race conditions [#2728](https://github.com/opensearch-project/k-NN/pull/2728)
* [BUGFIX] Fix nested vector query at efficient filter scenarios [#2641](https://github.com/opensearch-project/k-NN/pull/2641)
* [BUGFIX] Fix memory optimized searcher to use a sliced index input [#2739](https://github.com/opensearch-project/k-NN/pull/2739)


## INFRASTRUCTURE


### Opensearch ML Common


* change release note (#3811)[https://github.com/opensearch-project/ml-commons/pull/3811]


### Opensearch Neural Search


* [3.0] Update neural-search for OpenSearch 3.0 beta compatibility ([#1245](https://github.com/opensearch-project/neural-search/pull/1245))


### Opensearch Query Insights Dashboards


* Fix version mismatch between OpenSearch and Dashboards in CI binary installation workflow ([#205](https://github.com/opensearch-project/query-insights-dashboards/pull/205))


### Opensearch k-NN


* Add testing support to run all ITs with remote index builder [#2659](https://github.com/opensearch-project/k-NN/pull/2659)
* Fix KNNSettingsTests after change in MockNode constructor [#2700](https://github.com/opensearch-project/k-NN/pull/2700)


## DOCUMENTATION


### Opensearch ML Common


* Replace the usage of elasticsearch with OpenSearch in README (#3876)[https://github.com/opensearch-project/ml-commons/pull/3876]
* added blueprint for Bedrock Claude v4 (#3871)[https://github.com/opensearch-project/ml-commons/pull/3871]


## MAINTENANCE


### Opensearch Dashboards Maps


* Increment version to 3.1.0.0 [#735](https://github.com/opensearch-project/dashboards-maps/pull/735)


### Opensearch Dashboards Search Relevance


* Increment version to 3.1.0.0 ([#534](https://github.com/opensearch-project/dashboards-search-relevance/pull/534))


* Fix schema validation in POST Query Sets endpoint ([#542](https://github.com/opensearch-project/dashboards-search-relevance/pull/542))


### Opensearch Flow Framework Dashboards


* Remove legacy tutorial doc ([#747](https://github.com/opensearch-project/dashboards-flow-framework/pull/747))


### Opensearch Geospatial


* Fix a unit test and update github workflow to use actions/setup-java@v3.


### Opensearch ML Common


* [Code Quality] Adding test cases for PlanExecuteReflect Agent (#3778)[https://github.com/opensearch-project/ml-commons/pull/3778]
* Add Unit Tests for MCP feature (#3787)[https://github.com/opensearch-project/ml-commons/pull/3787]
* exclude trusted connector check for hidden model (#3838)[https://github.com/opensearch-project/ml-commons/pull/3838]
* add more logging to deploy/undeploy flows for better debugging (#3825)[https://github.com/opensearch-project/ml-commons/pull/3825]
* remove libs folder (#3824)[https://github.com/opensearch-project/ml-commons/pull/3824]
* Downgrade MCP version to 0.9 (#3821)[https://github.com/opensearch-project/ml-commons/pull/3821]
* upgrade http client to version align with core (#3809)[https://github.com/opensearch-project/ml-commons/pull/3809]
* Use stream optional enum set from core in MLStatsInput (#3648)[https://github.com/opensearch-project/ml-commons/pull/3648]
* change SearchIndexTool arguments parsing logic (#3883)[https://github.com/opensearch-project/ml-commons/pull/3883]


### Opensearch Neural Search


* Update Lucene dependencies ([#1336](https://github.com/opensearch-project/neural-search/pull/1336))


### Opensearch Opensearch Learning To Rank Base


* Lucene 10.2 upgrade changes ((#186)[https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/186])


### Opensearch Query Insights


* fix flaky integ tests ([#364](https://github.com/opensearch-project/query-insights/pull/364))


### Opensearch Query Insights Dashboards


* Increment version to 3.1.0.0 ([#194](https://github.com/opensearch-project/query-insights-dashboards/pull/194))


## REFACTORING


### Opensearch k-NN


* Refactor Knn Search Results to use TopDocs [#2727](https://github.com/opensearch-project/k-NN/pull/2727)


## NON-COMPLIANT


## ADDED


### Opensearch Search Relevance


* Added new experiment type for hybrid search ([#26](https://github.com/opensearch-project/search-relevance/pull/26))


* Added feature flag for search relevance workbench ([#34](https://github.com/opensearch-project/search-relevance/pull/34))
* [Enhancement] Extend data model to adopt different experiment options/parameters ([#29](https://github.com/opensearch-project/search-relevance/issues/29))
* Added validation for hybrid query structure ([#40](https://github.com/opensearch-project/search-relevance/pull/40))
* [Enhancement] Add support for importing judgments created externally from SRW. ([#42](https://github.com/opensearch-project/search-relevance/pull/42)
* Changing URL for plugin APIs to /\_plugin/\_search\_relevance [backend] ([#62](https://github.com/opensearch-project/search-relevance/pull/62)
* Added lazy index creation for all APIs ([#65](https://github.com/opensearch-project/search-relevance/pull/65)
* Realistic test data set based on ESCI (products, queries, judgements) ([#70](https://github.com/opensearch-project/search-relevance/pull/70)
* [Stats] Add stats API ([#63](https://github.com/opensearch-project/search-relevance/pull/63)))


## FIXED


### Opensearch Search Relevance


* Update demo setup to be include ubi and ecommerce data sets and run in OS 3.1 ([#10](https://github.com/opensearch-project/search-relevance/issues/10))


* Build search request with normal parsing and wrapper query ([#22](https://github.com/opensearch-project/search-relevance/pull/22))
* Change aggregation field from `action_name.keyword` to `action_name` to fix implicit judgments calculation ([#15](https://github.com/opensearch-project/search-relevance/issues/10)).
* Fix COEC calculation: introduce rank in ClickthroughRate class, fix bucket size for positional aggregation, correct COEC claculation ([#23](https://github.com/opensearch-project/search-relevance/issues/23)).
* LLM Judgment Processor Improvement ([#27](https://github.com/opensearch-project/search-relevance/pull/27))
* Deal with experiment processing when no experiment variants exist. ([#45](https://github.com/opensearch-project/search-relevance/pull/45))
* Extend the `src/test/demo.sh` script to support pointwise and hybrid experiments.
* Enable Search Relevance backend plugin as part of running demo scripts. ([#60](https://github.com/opensearch-project/search-relevance/pull/60))
* Move from Judgments being "scores" to Judgments being "ratings". ([#64](https://github.com/opensearch-project/search-relevance/pull/64))
* Extend hybrid search optimizer demo script to use models. ([#69](https://github.com/opensearch-project/search-relevance/pull/69))
* Set limit for number of fields programmatically during index creation ([#74](https://github.com/opensearch-project/search-relevance/pull/74)
* Change model for Judgment entity ([#77](https://github.com/opensearch-project/search-relevance/pull/77)
* Fix judgment handling for implicit judgments to be aligned with data model for Judgment again ([#93](https://github.com/opensearch-project/search-relevance/pull/93)
* Change model for Experiment and Evaluation Result entities: ([#99](https://github.com/opensearch-project/search-relevance/pull/99))
* Refactor and fix LLM judgment duplication issue ([#98](https://github.com/opensearch-project/search-relevance/pull/98)))


## ADDED


### Opensearch Security


* [Resource Permissions] Introduces Centralized Resource Access Control Framework ([#5281](https://github.com/opensearch-project/security/pull/5281))
* Github workflow for changelog verification ([#5318](https://github.com/opensearch-project/security/pull/5318))
* Register cluster settings listener for `plugins.security.cache.ttl_minutes` ([#5324](https://github.com/opensearch-project/security/pull/5324))
* Add flush cache endpoint for individual user ([#5337](https://github.com/opensearch-project/security/pull/5337))
* Handle roles in nested claim for JWT auth backends ([#5355](https://github.com/opensearch-project/security/pull/5355))
* Integrate search-relevance functionalities with security plugin ([#5376](https://github.com/opensearch-project/security/pull/5376))
* Add forecast roles and permissions ([#5386](https://github.com/opensearch-project/security/pull/5386))


## CHANGED


### Opensearch Security


* Use extendedPlugins in integrationTest framework for sample resource plugin testing ([#5322](https://github.com/opensearch-project/security/pull/5322))
* [Resource Sharing] Refactor ResourcePermissions to refer to action groups as access levels ([#5335](https://github.com/opensearch-project/security/pull/5335))
* Introduced new, performance-optimized implementation for tenant privileges ([#5339](https://github.com/opensearch-project/security/pull/5339))
* Performance improvements: Immutable user object ([#5212](https://github.com/opensearch-project/security/pull/5212))
* Include mapped roles when setting userInfo in ThreadContext ([#5369](https://github.com/opensearch-project/security/pull/5369))
* Adds details for debugging Security not initialized error([#5370](https://github.com/opensearch-project/security/pull/5370))
* [Resource Sharing] Store resource sharing info in indices that map 1-to-1 with resource index ([#5358](https://github.com/opensearch-project/security/pull/5358))


## REMOVED


### Opensearch Security


* Removed unused support for custom User object serialization ([#5339](https://github.com/opensearch-project/security/pull/5339))


## FIXED


### Opensearch Security


* Corrections in DlsFlsFilterLeafReader regarding PointVales and object valued attributes ([#5303](https://github.com/opensearch-project/security/pull/5303))
* Fix issue computing diffs in compliance audit log when writing to security index ([#5279](https://github.com/opensearch-project/security/pull/5279))
* Fixing dependabot broken pull\_request workflow for changelog update ([#5331](https://github.com/opensearch-project/security/pull/5331))
* Fixes assemble workflow failure during Jenkins build ([#5334](https://github.com/opensearch-project/security/pull/5334))
* Fixes security index stale cache issue post snapshot restore ([#5307](https://github.com/opensearch-project/security/pull/5307))
* Only log Invalid Authentication header when HTTP Basic auth challenge is called ([#5377](https://github.com/opensearch-project/security/pull/5377))


## DEPENDENCIES


### Opensearch Security


* Bump `guava_version` from 33.4.6-jre to 33.4.8-jre ([#5284](https://github.com/opensearch-project/security/pull/5284))
* Bump `spring_version` from 6.2.5 to 6.2.7 ([#5283](https://github.com/opensearch-project/security/pull/5283), [#5345](https://github.com/opensearch-project/security/pull/5345))
* Bump `com.google.errorprone:error_prone_annotations` from 2.37.0 to 2.38.0 ([#5285](https://github.com/opensearch-project/security/pull/5285))
* Bump `org.mockito:mockito-core` from 5.15.2 to 5.18.0 ([#5296](https://github.com/opensearch-project/security/pull/5296), [#5362](https://github.com/opensearch-project/security/pull/5362))
* Bump `com.carrotsearch.randomizedtesting:randomizedtesting-runner` from 2.8.2 to 2.8.3 ([#5294](https://github.com/opensearch-project/security/pull/5294))
* Bump `org.ow2.asm:asm` from 9.7.1 to 9.8 ([#5293](https://github.com/opensearch-project/security/pull/5293))
* Bump `commons-codec:commons-codec` from 1.16.1 to 1.18.0 ([#5295](https://github.com/opensearch-project/security/pull/5295))
* Bump `net.bytebuddy:byte-buddy` from 1.15.11 to 1.17.5 ([#5313](https://github.com/opensearch-project/security/pull/5313))
* Bump `org.awaitility:awaitility` from 4.2.2 to 4.3.0 ([#5314](https://github.com/opensearch-project/security/pull/5314))
* Bump `org.springframework.kafka:spring-kafka-test` from 3.3.4 to 3.3.5 ([#5315](https://github.com/opensearch-project/security/pull/5315))
* Bump `com.fasterxml.jackson.core:jackson-databind` from 2.18.2 to 2.19.0 ([#5292](https://github.com/opensearch-project/security/pull/5292))
* Bump `org.apache.commons:commons-collections4` from 4.4 to 4.5.0 ([#5316](https://github.com/opensearch-project/security/pull/5316))
* Bump `com.google.googlejavaformat:google-java-format` from 1.26.0 to 1.27.0 ([#5330](https://github.com/opensearch-project/security/pull/5330))
* Bump `io.github.goooler.shadow` from 8.1.7 to 8.1.8 ([#5329](https://github.com/opensearch-project/security/pull/5329))
* Bump `commons-io:commons-io` from 2.18.0 to 2.19.0 ([#5328](https://github.com/opensearch-project/security/pull/5328))
* Upgrade kafka\_version from 3.7.1 to 4.0.0 ([#5131](https://github.com/opensearch-project/security/pull/5131))
* Bump `io.dropwizard.metrics:metrics-core` from 4.2.30 to 4.2.32 ([#5361](https://github.com/opensearch-project/security/pull/5361))
* Bump `org.junit.jupiter:junit-jupiter` from 5.12.2 to 5.13.1 ([#5371](https://github.com/opensearch-project/security/pull/5371), [#5382](https://github.com/opensearch-project/security/pull/5382))
* Bump `bouncycastle_version` from 1.80 to 1.81 ([#5380](https://github.com/opensearch-project/security/pull/5380))
* Bump `org.junit.jupiter:junit-jupiter-api` from 5.13.0 to 5.13.1 ([#5383](https://github.com/opensearch-project/security/pull/5383))
* Bump `org.checkerframework:checker-qual` from 3.49.3 to 3.49.4 ([#5381](https://github.com/opensearch-project/security/pull/5381))


## ADDED


### Opensearch Security Dashboards Plugin


* Adds forecasting transport actions to the static dropdown list ([#2253](https://github.com/opensearch-project/security-dashboards-plugin/pull/2253))


## CHANGED


### Opensearch Security Dashboards Plugin


* Changes to prevent page reload on entering invalid current password and to disable reset button when current or new password is empty ([#2238](https://github.com/opensearch-project/security-dashboards-plugin/pull/2238))


## DEPENDENCIES


### Opensearch Security Dashboards Plugin


* Bump dev dependencies to resolve CVE-2024-52798 ([#2231](https://github.com/opensearch-project/security-dashboards-plugin/pull/2231))


