# OpenSearch and OpenSearch Dashboards 3.4.0 Release Notes


## Release Details
[OpenSearch and OpenSearch Dashboards 3.4.0](https://opensearch.org/artifacts/by-version/#release-3-4-0) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.4.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.4.0.md).


## FEATURES


### OpenSearch Alerting


* PPL Alerting: Execute Monitor and Monitor Stats ([#1960](https://github.com/opensearch-project/alerting/pull/1960))
* PPL Alerting: Get and Search Monitors ([#1966](https://github.com/opensearch-project/alerting/pull/1966))
* PPL Alerting: Delete Monitor, More V1/V2 Separation ([#1968](https://github.com/opensearch-project/alerting/pull/1968))
* PPL Alerting: Get Alerts and Alert Lifecycle ([#1972](https://github.com/opensearch-project/alerting/pull/1972))


### OpenSearch Anomaly Detection Dashboards Plugin


* Adding Indices management and selection for daily insights ([#1119](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1119))
* Introduce Daily Insights Page ([#1118](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1118))
* Adding data selector for index management ([#1120](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1120))


### OpenSearch Dashboards Flow Framework


* Add agent summary ([#801](https://github.com/opensearch-project/dashboards-flow-framework/pull/801))
* [Agentic Search] Add MCP server support ([#802](https://github.com/opensearch-project/dashboards-flow-framework/pull/802))
* [Agentic Search] Improve Test Flow UX ([#812](https://github.com/opensearch-project/dashboards-flow-framework/pull/812))


### OpenSearch Flow Framework


* Onboards flow-framework plugin to resource-sharing and access control framework ([#1251](https://github.com/opensearch-project/flow-framework/pull/1251))


### OpenSearch Index Management


* Supporting Exclusion pattern in index pattern in ISM ([#1509](https://github.com/opensearch-project/index-management/pull/1509))


### OpenSearch k-NN


* Memory optimized search warmup ([#2954](https://github.com/opensearch-project/k-NN/pull/2954))


## ENHANCEMENTS


### OpenSearch Anomaly Detection


* Adds capability to automatically switch to old access-control if model-group is excluded from protected resources setting ([#1569](https://github.com/opensearch-project/anomaly-detection/pull/1569))
* Adding suggest and validate transport actions to node client ([#1605](https://github.com/opensearch-project/anomaly-detection/pull/1605))
* Adding auto create as an optional field on detectors ([#1602](https://github.com/opensearch-project/anomaly-detection/pull/1602))


### OpenSearch Dashboards Flow Framework


* Clean up / hide complex fields on agent configuration ([#796](https://github.com/opensearch-project/dashboards-flow-framework/pull/796))
* Clean up agent summary formatting ([#803](https://github.com/opensearch-project/dashboards-flow-framework/pull/803))
* [Agentic Search] Improve export / next steps UX ([#805](https://github.com/opensearch-project/dashboards-flow-framework/pull/805))
* [Agentic Search] Simplify form inputs ([#807](https://github.com/opensearch-project/dashboards-flow-framework/pull/807))
* [Agentic Search] Simplify form inputs II ([#808](https://github.com/opensearch-project/dashboards-flow-framework/pull/808))
* Integrate with memory ([#809](https://github.com/opensearch-project/dashboards-flow-framework/pull/809))
* Add version filtering on agentic search usecase ([#813](https://github.com/opensearch-project/dashboards-flow-framework/pull/813))
* Improve 'Visualized Hits' values ([#814](https://github.com/opensearch-project/dashboards-flow-framework/pull/814))
* Automatically add response filters to flow agents when possible ([#817](https://github.com/opensearch-project/dashboards-flow-framework/pull/817))
* Remove default empty tool field values; fix EuiSelect values in Firefox ([#820](https://github.com/opensearch-project/dashboards-flow-framework/pull/820))


### OpenSearch Learning To Rank Base


* Allow warnings about directly accessing the .plugins-ml-config index ([#256](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/256))
* Feature/ltr system origin avoid warnings ([#259](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/259))


### OpenSearch OpenSearch Remote Metadata Sdk


* Add CMK support to accept CMK to encrypt/decrypt customer data. ([#271](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/271))
* Add assume role for CMK. ([#295](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/295))


### OpenSearch k-NN


* Removed VectorSearchHolders map from NativeEngines990KnnVectorsReader ([#2948](https://github.com/opensearch-project/k-NN/pull/2948))
* Native scoring for FP16 ([#2922](https://github.com/opensearch-project/k-NN/pull/2922))


## BUG FIXES


### OpenSearch Alerting


* Fix CI check with security failing due to empty string in payload body ([#1994](https://github.com/opensearch-project/alerting/pull/1994))


### OpenSearch Anomaly Detection


* Fix(forecast): auto-expand replicas for default results index on 3AZ domains ([#1615](https://github.com/opensearch-project/anomaly-detection/pull/1615))


### OpenSearch Anomaly Detection Dashboards Plugin


* Honor detector frequency when flagging missing feature data ([#1116](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1116))
* Address the issue where an error toast appears when the page opens ([#1126](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1126))


### OpenSearch Cross Cluster Replication


* Fix the requirement of empty request body in pause replication ([#1603](https://github.com/opensearch-project/cross-cluster-replication/pull/1603))


### OpenSearch Dashboards Flow Framework


* Gracefully handle workflows with no provisioned resources ([#821](https://github.com/opensearch-project/dashboards-flow-framework/pull/821))


### OpenSearch Flow Framework


* Incorrect field map output dimensions in default values for semantic search with local model use case template ([#1270](https://github.com/opensearch-project/flow-framework/pull/1270))


### OpenSearch Index Management


* Fix race condition in rollup start/stop tests ([#1529](https://github.com/opensearch-project/index-management/pull/1529))
* After remove policy from index, coordinator sweep will bind again ([#1525](https://github.com/opensearch-project/index-management/pull/1525))
* Fix snapshot pattern parsing in SM deletion workflow to handle comma-separated values ([#1503](https://github.com/opensearch-project/index-management/pull/1503))


### OpenSearch OpenSearch Learning To Rank Base


* Use OpenSearch Version.computeID for legacy version IDs ([#264](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/264))


### OpenSearch OpenSearch Remote Metadata Sdk


* Fix error when updating model status ([#291](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/291))


### OpenSearch Query Insights


* Exclude internal `top_queries-*` indices ([#481](https://github.com/opensearch-project/query-insights/pull/481))


### OpenSearch Security Dashboards Plugin


* Filter blank backend role before creating internal user ([#2330](https://github.com/opensearch-project/security-dashboards-plugin/pull/2330))


### OpenSearch k-NN


* Fix blocking old indices created before 2.18 to use memory optimized search. ([#2918](https://github.com/opensearch-project/k-NN/pull/2918))
* Fix NativeEngineKnnQuery to return all part results for valid totalHits in response ([#2965](https://github.com/opensearch-project/k-NN/pull/2965))
* Fix unsafe concurrent update query vector in KNNQueryBuilder ([#2974](https://github.com/opensearch-project/k-NN/pull/2974))
* Fix score to distance calculation for inner product in faiss [#2992](https://github.com/opensearch-project/k-NN/pull/2992)
* Fix Backwards Compatability on Segment Merge for Disk-Based vector search ([#2994](https://github.com/opensearch-project/k-NN/pull/2994))


## INFRASTRUCTURE


### OpenSearch Alerting


* Kotlin version upgrade ([#1993](https://github.com/opensearch-project/alerting/pull/1993))
* JDK upgrade to 25 and gradle upgrade to 9.2 ([#1995](https://github.com/opensearch-project/alerting/pull/1995))


### OpenSearch Anomaly Detection


* Test: Prevent oversized bulk requests in synthetic data test ([#1603](https://github.com/opensearch-project/anomaly-detection/pull/1603))
* Update CI to JDK 25 and gradle to 9.2 ([#1623](https://github.com/opensearch-project/anomaly-detection/pull/1623))


### OpenSearch Cross Cluster Replication


* Update Gradle to 9.2.1 and CI to test on JDK 25 ([#1605](https://github.com/opensearch-project/cross-cluster-replication/pull/1605))


### OpenSearch Custom Codecs


* Update to Gradle 9.2 and test with JDK 25 ([#294](https://github.com/opensearch-project/custom-codecs/pull/294))


### OpenSearch Index Management


* Upgrade gradle to 9.2.0 and github actions JDK 25 ([#1534](https://github.com/opensearch-project/index-management/pull/1534))
* Dependabot: bump actions/github-script from 7 to 8 ([#1485](https://github.com/opensearch-project/index-management/pull/1485))


### OpenSearch OpenSearch Learning To Rank Base


* Reduce the required coverage until we can improve it ([#258](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/258))
* Upgrade Gradle to 9.2.0 ([#263](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/263))


### OpenSearch Query Insights


* Add multi-node, healthstats integration tests and fix flaky tests ([#482](https://github.com/opensearch-project/query-insights/pull/482))


### OpenSearch Security Analytics


* Only use alerting SNAPSHOTS in SNAPSHOT build, otherwise use release artifacts ([#1608](https://github.com/opensearch-project/security-analytics/pull/1608))
* Jdk upgrade to 25 and gradle upgrade to 9.2 ([#1618](https://github.com/opensearch-project/security-analytics/pull/1618))


### OpenSearch k-NN


* Include opensearchknn\_simd in build configurations ([#3025](https://github.com/opensearch-project/k-NN/pull/3025))


## MAINTENANCE


### OpenSearch Anomaly Detection Dashboards Plugin


* Bump js-yaml from 3.14.1 to 3.14.2 ([#1121](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1121))


### OpenSearch Cross Cluster Replication


* Update Gradle to 9.2.1 and CI to test on JDK 25 ([#1605](https://github.com/opensearch-project/cross-cluster-replication/pull/1605))


### OpenSearch Index Management


* Increments version to 3.4.0 and adds ActionFilter interface ([#1536](https://github.com/opensearch-project/index-management/pull/1536))
* Update logback dependencies to version 1.5.19 ([#1537](https://github.com/opensearch-project/index-management/pull/1537))
* Use optionalField for creation in ExplainSMPolicy serialization ([#1507](https://github.com/opensearch-project/index-management/pull/1507))


### OpenSearch Query Insights


* Gradle 9.2.0 and JDK 25 upgrade ([#486](https://github.com/opensearch-project/query-insights/pull/486))


### OpenSearch Security Dashboards Plugin


* Bump `Wandalen/wretry.action` from 3.3.0 to 3.8.0 ([#2322](https://github.com/opensearch-project/security-dashboards-plugin/pull/2322))
* Bump `stefanzweifel/git-auto-commit-action` from 6 to 7 ([#2329](https://github.com/opensearch-project/security-dashboards-plugin/pull/2329))
* Bump `derek-ho/setup-opensearch-dashboards` from 1 to 3 ([#2321](https://github.com/opensearch-project/security-dashboards-plugin/pull/2321))
* Bump `actions/setup-java` from 4 to 5 ([#2323](https://github.com/opensearch-project/security-dashboards-plugin/pull/2323))
* Bump `actions/checkout` from 5 to 6 ([#2339](https://github.com/opensearch-project/security-dashboards-plugin/pull/2339))


### OpenSearch k-NN


* Onboard to s3 snapshots ([#2943](https://github.com/opensearch-project/k-NN/pull/2943))
* Gradle 9.2.0 and GitHub Actions JDK 25 Upgrade ([#2984](https://github.com/opensearch-project/k-NN/pull/2984))


## REFACTORING


### OpenSearch Security Dashboards Plugin


* [Resource Sharing] Changes patch update sharing API to post ([#2338](https://github.com/opensearch-project/security-dashboards-plugin/pull/2338))


### OpenSearch k-NN


* Refactor to not use parallel for MMR rerank. ([#2968](https://github.com/opensearch-project/k-NN/pull/2968))


