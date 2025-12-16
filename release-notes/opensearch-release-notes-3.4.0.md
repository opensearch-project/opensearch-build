# OpenSearch and OpenSearch Dashboards 3.4.0 Release Notes


## Release Highlights

### New and Updated Features
OpenSearch 3.4 delivers new features designed to help your search and observability applications along with performance enhancements. Highlights include

* **New agentic search user experience**
A redesigned, no-code user experience simplifies the work of building agents and running agentic searches, with support for the latest agentic capabilities, including external Model Context Protocol (MCP) integration, search template integration, conversational memory, and single model support. 

* **Enhanced search relevance tools**
New tools and UX enhancements for the Search Relevance Workbench include the ability to schedule experiments from the user interface, support for agentic search in the single query comparison tool, and support for GUID filtering.

* **Expanded PPL functions and commands**
Explore your data with new chart, streamstats, multisearch, replace, and appendpipe commands, as well as new mvindex and mvdedup functions.

* **Faster aggregation workloads**
This release integrates Lucene’s new bulk collection API to realize performance gains of 5% to 40% across several key analytical operations including cardinality, histogram, and series of statistical aggregations.

* **Better latencies for percentiles and matrix stats aggregations**
This release replaces the previous AVLTreeDigest implementation with the MergingDigest implementation for percentiles aggregations, delivering significant improvements in performance, particularly for low-cardinality fields. An improvement in the matrix_stats aggregation implementation delivers as much as a 5x performance increase.

* **Enhanced gRPC functionality**
gRPC gains functionality with support for new query types ConstantScoreQuery, FuzzyQuery, MatchBoolPrefixQuery, MatchPhrasePrefix, PrefixQuery, and MatchQuery, as well as improvements for gRPC bulk requests with support for CBOR/SMILE/YAML document formats.

* **Scroll Query performance improvement**
This release integrates cached StoredFieldsReader optimization in the query fetch phase, achieving approximately 19% improvement on scroll queries.


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


### OpenSearch Alerting Dashboards Plugin


* Allow keyword filter to be attached to bucket level monitor trigger ([#1325](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1325))
* Onboarded opensearch apis to use MDS client when MDS is enabled ([#1313](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1313))


### OpenSearch Anomaly Detection Dashboards Plugin


* Adding Indices management and selection for daily insights ([#1119](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1119))
* Introduce Daily Insights Page ([#1118](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1118))
* Adding data selector for index management ([#1120](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1120))


### OpenSearch Dashboards Assistant


* Disable dashboards assistant chatbot if investigation feature flag enabled ([#626](https://github.com/opensearch-project/dashboards-assistant/pull/626))


### OpenSearch Dashboards Flow Framework


* Add agent summary ([#801](https://github.com/opensearch-project/dashboards-flow-framework/pull/801))
* [Agentic Search] Add MCP server support ([#802](https://github.com/opensearch-project/dashboards-flow-framework/pull/802))
* [Agentic Search] Improve Test Flow UX ([#812](https://github.com/opensearch-project/dashboards-flow-framework/pull/812))


### OpenSearch Dashboards Search Relevance


* Add scheduling and descheduling experiments in the UI ([#636](https://github.com/opensearch-project/dashboards-search-relevance/pull/636))


* Add support for agent search in pariwise comparison ([#693](https://github.com/opensearch-project/dashboards-search-relevance/pull/693))


### OpenSearch Flow Framework


* Onboards flow-framework plugin to resource-sharing and access control framework ([#1251](https://github.com/opensearch-project/flow-framework/pull/1251))


### OpenSearch Index Management


* Supporting Exclusion pattern in index pattern in ISM ([#1509](https://github.com/opensearch-project/index-management/pull/1509))


### OpenSearch Query Insights Dashboards


* Add version-aware settings support ([#407](https://github.com/opensearch-project/query-insights-dashboards/pull/407))
* Security attribute feature for WLM dashboard ([#392](https://github.com/opensearch-project/query-insights-dashboards/pull/392))


### OpenSearch Search Relevance


* Added APIs and components to implement running scheduled experiments ([#220](https://github.com/opensearch-project/search-relevance/pull/220))


### OpenSearch k-NN


* Memory optimized search warmup ([#2954](https://github.com/opensearch-project/k-NN/pull/2954))


### SQL


* Support `chart` command in PPL ([#4579](https://github.com/opensearch-project/sql/pull/4579))
* Support `Streamstats` command with calcite ([#4297](https://github.com/opensearch-project/sql/pull/4297))
* Support `multisearch` command in calcite ([#4332](https://github.com/opensearch-project/sql/pull/4332))
* Support `replace` command in Calcite ([#4451](https://github.com/opensearch-project/sql/pull/4451))
* Support `mvdedup` eval function ([#4828](https://github.com/opensearch-project/sql/pull/4828))
* Support `mvindex` eval function ([#4794](https://github.com/opensearch-project/sql/pull/4794))
* Support `mvappend` function ([#4438](https://github.com/opensearch-project/sql/pull/4438))
* Support `per_second` function for `timechart` command ([#4464](https://github.com/opensearch-project/sql/pull/4464))
* Support `per_minute`, `per_hour`, `per_day` function ([#4531](https://github.com/opensearch-project/sql/pull/4531))
* Support `appendpipe` command in PPL ([#4602](https://github.com/opensearch-project/sql/pull/4602))
* Support `tostring()` eval function ([#4497](https://github.com/opensearch-project/sql/pull/4497))


## ENHANCEMENTS


### OpenSearch Anomaly Detection


* Adds capability to automatically switch to old access-control if model-group is excluded from protected resources setting ([#1569](https://github.com/opensearch-project/anomaly-detection/pull/1569))
* Adding suggest and validate transport actions to node client ([#1605](https://github.com/opensearch-project/anomaly-detection/pull/1605))
* Adding auto create as an optional field on detectors ([#1602](https://github.com/opensearch-project/anomaly-detection/pull/1602))


### OpenSearch Dashboards Assistant


* Support log pattern in discover summary ([#550](https://github.com/opensearch-project/dashboards-assistant/pull/550))


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


### OpenSearch Dashboards Notifications


* Avoid refetching channel config on every keystroke for name update ([#393](https://github.com/opensearch-project/dashboards-notifications/pull/393))


### OpenSearch Dashboards Observability


* Clean up interface for integrations static serving ([#2530](https://github.com/opensearch-project/dashboards-observability/pull/2530))


### OpenSearch Dashboards Search Relevance


* Added client-side filtering in experiment list by `type` and `status`, in addition to `id` (GUID). ([#686](https://github.com/opensearch-project/dashboards-search-relevance/pull/686))
* Added GUID search support to the Search Configuration listing to allow filtering by configuration ID in addition to name. ([#685](https://github.com/opensearch-project/dashboards-search-relevance/pull/685))
* Added support for filtering Query Sets by GUID and aligned QuerySetItem typing with existing structure ([#687](https://github.com/opensearch-project/dashboards-search-relevance/pull/687))
* Added support for filtering Judgment Lists by GUID (`id`) in the search bar, improving discoverability and navigation when working with judgment identifiers. ([#687](https://github.com/opensearch-project/dashboards-search-relevance/pull/687))
* Use appropriate title on the Experiment Detail page. ([#670](https://github.com/opensearch-project/dashboards-search-relevance/pull/670))


### OpenSearch ML Commons


* Declare credential and \*.Authorization as sensitive param in create connector API ([#4308](https://github.com/opensearch-project/ml-commons/pull/4308))
* Pass resourceType instead of resourceIndex to resourceSharingClient ([#4333](https://github.com/opensearch-project/ml-commons/pull/4333))
* allow higher maximum number of batch inference job tasks ([#4474](https://github.com/opensearch-project/ml-commons/pull/4474))


### OpenSearch Neural Search


* [Agentic Search] Preserve source parameter for the query ([#1669](https://github.com/opensearch-project/neural-search/pull/1669))


* [SEISMIC Nested Field]: Sparse ANN ingestion and query handle nested fields ([#1678](https://github.com/opensearch-project/neural-search/pull/1678))


### OpenSearch Learning To Rank Base


* Allow warnings about directly accessing the .plugins-ml-config index ([#256](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/256))
* Feature/ltr system origin avoid warnings ([#259](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/259))


### OpenSearch Remote Metadata Sdk


* Add CMK support to accept CMK to encrypt/decrypt customer data. ([#271](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/271))
* Add assume role for CMK. ([#295](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/295))


### OpenSearch Performance Analyzer


* Restore java min compatible to 21 and remove 24 ([#902](https://github.com/opensearch-project/performance-analyzer/pull/902))


### OpenSearch Query Insights Dashboards


* MDS support for live queries page ([#403](https://github.com/opensearch-project/query-insights-dashboards/pull/403))


### OpenSearch Search Relevance


* Add data integrity support for deleting experiments ([#324](https://github.com/opensearch-project/search-relevance/pull/324))


### OpenSearch Security


* Moved configuration reloading to dedicated thread to improve node stability ([#5479](https://github.com/opensearch-project/security/pull/5479))
* Makes resource settings dynamic ([#5677](https://github.com/opensearch-project/security/pull/5677))
* [Resource Sharing] Allow multiple sharable resource types in single resource index ([#5713](https://github.com/opensearch-project/security/pull/5713))
* Adding Alerting V2 roles to roles.yml ([#5747](https://github.com/opensearch-project/security/pull/5747))
* Add suggest api to ad read access role ([#5754](https://github.com/opensearch-project/security/pull/5754))
* Get list of headersToCopy from core and use getHeader(String headerName) instead of getHeaders() ([#5769](https://github.com/opensearch-project/security/pull/5769))
* [Resource Sharing] Keep track of resource\_type on resource sharing document ([#5772](https://github.com/opensearch-project/security/pull/5772))
* Add support for X509 v3 extensions (SAN) for authentication ([#5701](https://github.com/opensearch-project/security/pull/5701))
* [Resource Sharing] Requires default\_owner for resource/migrate API ([#5789](https://github.com/opensearch-project/security/pull/5789))
* Add --timeout (-to) as an option to securityadmin.sh ([#5787](https://github.com/opensearch-project/security/pull/5787))


### OpenSearch Skills


* Increase max\_sample\_count to 5 for log insight ([#678](https://github.com/opensearch-project/skills/pull/678))


### OpenSearch k-NN


* Removed VectorSearchHolders map from NativeEngines990KnnVectorsReader ([#2948](https://github.com/opensearch-project/k-NN/pull/2948))
* Native scoring for FP16 ([#2922](https://github.com/opensearch-project/k-NN/pull/2922))


### SQL


* Add `bucket_nullable` argument for `Streamstats` command ([#4831](https://github.com/opensearch-project/sql/pull/4831))
* Add `regexp_replace()` function as alias of `replace()` ([#4765](https://github.com/opensearch-project/sql/pull/4765))
* Convert `dedup` pushdown to composite + top\_hits ([#4844](https://github.com/opensearch-project/sql/pull/4844))
* Merge group fields for aggregate if having dependent group fields ([#4703](https://github.com/opensearch-project/sql/pull/4703))
* Merge the implementation of `timechart` and `chart` ([#4755](https://github.com/opensearch-project/sql/pull/4755))
* Perform RexNode expression standardization for script push down ([#4795](https://github.com/opensearch-project/sql/pull/4795))
* Pushdown sort by complex expressions to scan ([#4750](https://github.com/opensearch-project/sql/pull/4750))
* Pushdown the `top` `rare` commands to nested aggregation ([#4707](https://github.com/opensearch-project/sql/pull/4707))
* Refactor alias type field by adding another project with alias ([#4881](https://github.com/opensearch-project/sql/pull/4881))
* Remove count aggregation for sort on aggregate measure ([#4867](https://github.com/opensearch-project/sql/pull/4867))
* Remove redundant push-down-filters derived for bucket-non-null agg ([#4843](https://github.com/opensearch-project/sql/pull/4843))
* Remove unnecessary filter for DateHistogram aggregation ([#4877](https://github.com/opensearch-project/sql/pull/4877))
* Specify timestamp field with `timefield` in timechart command ([#4784](https://github.com/opensearch-project/sql/pull/4784))
* Support push down sort on aggregation measure for more than one agg call ([#4759](https://github.com/opensearch-project/sql/pull/4759))
* Support wildcard for replace command ([#4698](https://github.com/opensearch-project/sql/pull/4698))
* Add `bucket_nullable` argument for `Eventstats` ([#4817](https://github.com/opensearch-project/sql/pull/4817))
* Bin command error message enhancement ([#4690](https://github.com/opensearch-project/sql/pull/4690))
* Update clickbench queries with parameter bucket\_nullable=false ([#4732](https://github.com/opensearch-project/sql/pull/4732))
* Support 'usenull' option in PPL `top` and `rare` commands ([#4696](https://github.com/opensearch-project/sql/pull/4696))
* Support millisecond span ([#4672](https://github.com/opensearch-project/sql/pull/4672))
* Enhance dynamic source clause to support only metadata filters ([#4554](https://github.com/opensearch-project/sql/pull/4554))
* Support push down sort after limit ([#4657](https://github.com/opensearch-project/sql/pull/4657))
* Pushdown sort aggregate metrics ([#4603](https://github.com/opensearch-project/sql/pull/4603))
* Allow renaming group-by fields to existing field names ([#4586](https://github.com/opensearch-project/sql/pull/4586))
* Support Automatic Type Conversion for REX/SPATH/PARSE Command Extractions ([#4599](https://github.com/opensearch-project/sql/pull/4599))
* Pushdown case function in aggregations as range queries ([#4400](https://github.com/opensearch-project/sql/pull/4400))
* Update GEOIP function to support IP types as input ([#4613](https://github.com/opensearch-project/sql/pull/4613))
* Pushdown distinct count approx ([#4614](https://github.com/opensearch-project/sql/pull/4614))
* Optimize pushdown script size with necessary fields per expression ([#4615](https://github.com/opensearch-project/sql/pull/4615))
* Support referring to implicit `@timestamp` field in span ([#4138](https://github.com/opensearch-project/sql/pull/4138))
* Make composite bucket size configurable ([#4544](https://github.com/opensearch-project/sql/pull/4544))
* Add internal MAP\_REMOVE function for Calcite PPL ([#4511](https://github.com/opensearch-project/sql/pull/4511))
* Add MAP\_APPEND internal function to Calcite PPL ([#4515](https://github.com/opensearch-project/sql/pull/4515))
* Use `_doc` + `_shard_doc` as sort tiebreaker to get better performance ([#4569](https://github.com/opensearch-project/sql/pull/4569))
* [Enhancement] Error handling for illegal character usage in java regex named capture group ([#4434](https://github.com/opensearch-project/sql/pull/4434))
* Add JSON\_EXTRACT\_ALL internal function for Calcite PPL ([#4489](https://github.com/opensearch-project/sql/pull/4489))
* Set 0 and negative value of subsearch.maxout as unlimited ([#4534](https://github.com/opensearch-project/sql/pull/4534))
* Add configurable system limitations for `subsearch` and `join` command ([#4501](https://github.com/opensearch-project/sql/pull/4501))
* Add MAP\_CONCAT internal function ([#4477](https://github.com/opensearch-project/sql/pull/4477))
* Support Regex for replace eval function ([#4456](https://github.com/opensearch-project/sql/pull/4456))
* Add data anonymizer for spath command ([#4479](https://github.com/opensearch-project/sql/pull/4479))
* Support eval returns decimal division result instead of integer ([#4440](https://github.com/opensearch-project/sql/pull/4440))
* PPL `fillnull` command enhancement ([#4421](https://github.com/opensearch-project/sql/pull/4421))
* Support format=yaml in Explain API ([#4446](https://github.com/opensearch-project/sql/pull/4446))


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


### OpenSearch Dashboards Assistant


* Detect serverless data source ([#627](https://github.com/opensearch-project/dashboards-assistant/pull/627))
* Fix capability services access settings before login and show dialog ([#628](https://github.com/opensearch-project/dashboards-assistant/pull/628))


### OpenSearch Dashboards Flow Framework


* Gracefully handle workflows with no provisioned resources ([#821](https://github.com/opensearch-project/dashboards-flow-framework/pull/821))


### OpenSearch Dashboards Reporting


* Bump jspdf to fix CVE-2025-57810 ([#650](https://github.com/opensearch-project/dashboards-reporting/pull/650))
* Undefined and null check for date time values ([#649](https://github.com/opensearch-project/dashboards-reporting/pull/649))


### OpenSearch Flow Framework


* Incorrect field map output dimensions in default values for semantic search with local model use case template ([#1270](https://github.com/opensearch-project/flow-framework/pull/1270))


### OpenSearch Index Management


* Fix race condition in rollup start/stop tests ([#1529](https://github.com/opensearch-project/index-management/pull/1529))
* After remove policy from index, coordinator sweep will bind again ([#1525](https://github.com/opensearch-project/index-management/pull/1525))
* Fix snapshot pattern parsing in SM deletion workflow to handle comma-separated values ([#1503](https://github.com/opensearch-project/index-management/pull/1503))


### OpenSearch ML Commons


* Fix agent type update ([#4341](https://github.com/opensearch-project/ml-commons/pull/4341))
* Handle edge case of empty values of tool configs ([#4479](https://github.com/opensearch-project/ml-commons/pull/4479))
* Fix OpenAI RAG integration tests: Replace Wikimedia image URL with Unsplash ([#4472](https://github.com/opensearch-project/ml-commons/pull/4472))
* Remove the error log on request body ([#4450](https://github.com/opensearch-project/ml-commons/pull/4450))
* [Agentic Search] Fix model id parsing for QueryPlanningTool ([#4458](https://github.com/opensearch-project/ml-commons/pull/4458))
* Fix several bugs on agentic memory ([#4476](https://github.com/opensearch-project/ml-commons/pull/4476))
* Fix tool used error message not proper escaped in MLChatAgentRunner ([#4410](https://github.com/opensearch-project/ml-commons/pull/4410))


### OpenSearch Neural Search


* [SEISMIC IT]: Fix some failed IT cases ([#1655](https://github.com/opensearch-project/neural-search/pull/1655))


* [SEISMIC Query]: Sparse ANN query handle non-specified method\_parameters ([#1674](https://github.com/opensearch-project/neural-search/pull/1674))
* Revert change in ([#1086](https://github.com/opensearch-project/neural-search/pull/1086)) to add support for empty string ([#1668](https://github.com/opensearch-project/neural-search/pull/1668))
* [SEISMIC]: Fix the disk free space recovery problem with Sparse ANN ([#1683](https://github.com/opensearch-project/neural-search/pull/1683))
* Code bug fix - Unable to get ACTIONS\_ID\_TOKEN\_REQUEST\_URL env variable ([#1693](https://github.com/opensearch-project/neural-search/pull/1693))


### OpenSearch Notifications


* CVE fix upgrade jackson-core and Security fix related to hostDenyList ([#1006](https://github.com/opensearch-project/notifications/pull/1006))


### OpenSearch Learning To Rank Base


* Use OpenSearch Version.computeID for legacy version IDs ([#264](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/264))
* Bug/ml index warning ([#269](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/269))
* Use implicit wait\_for instead of explicit refresh to avoid warnings about touching system indexes ([#271](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/271))
* Fix rescore-only feature SLTR logging ([#266](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/266))


### OpenSearch Remote Metadata Sdk


* Fix error when updating model status ([#291](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/291))


### OpenSearch Query Insights


* Exclude internal `top_queries-*` indices ([#481](https://github.com/opensearch-project/query-insights/pull/481))


### OpenSearch Query Insights Dashboards


* Fix MDS Selector for Workload Management Dashboards ([#421](https://github.com/opensearch-project/query-insights-dashboards/pull/421))
* Fix for mds in server/wlmRoutes ([#411](https://github.com/opensearch-project/query-insights-dashboards/pull/411))
* Remove "Open in search comparison" button from Query Details & Query Group Details ([#396](https://github.com/opensearch-project/query-insights-dashboards/pull/396))
* [Fix] Jest test failures due to Monaco editor ES module imports ([#435](https://github.com/opensearch-project/query-insights-dashboards/pull/435))


### OpenSearch Search Relevance


* Fixed floating-point precision issues in Hybrid Optimizer weight generation by switching to step-based iteration and rounding, ensuring clean and consistent weight pairs. ([#308](https://github.com/opensearch-project/search-relevance/pull/308))
* Fixed hybrid optimizer experiments stuck in `PROCESSING` after judgment deletion by correcting failure handling. [#292](https://github.com/opensearch-project/search-relevance/pull/292)
* Fix query serialization for plugins (e.g., Learning to Rank) that extend OpenSearch's DSL. ([#260](https://github.com/opensearch-project/search-relevance/pull/260))


### OpenSearch Security


* Create a WildcardMatcher.NONE when creating a WildcardMatcher with an empty string ([#5694](https://github.com/opensearch-project/security/pull/5694))
* Improve array validator to also check for blank string in addition to null ([#5714](https://github.com/opensearch-project/security/pull/5714))
* Use RestRequestFilter.getFilteredRequest to declare sensitive API params ([#5710](https://github.com/opensearch-project/security/pull/5710))
* Fix deprecated SSL transport settings in demo certificates ([#5723](https://github.com/opensearch-project/security/pull/5723))
* Updates DlsFlsValveImpl condition to return true if request is internal and not a protected resource request ([#5721](https://github.com/opensearch-project/security/pull/5721))
* [Performance] Call AdminDns.isAdmin once per request ([#5752](https://github.com/opensearch-project/security/pull/5752))
* Update operations on `.kibana` system index now work correctly with Dashboards multi tenancy enabled. ([#5778](https://github.com/opensearch-project/security/pull/5778))


### OpenSearch Security Analytics Dashboards Plugin


* Bug fixes: add null checks to prevent undefined property access ([#1342](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1342))
* Correlation table rendering fixed ([#1360](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1360))
* Backport 1360 to 3.3 ([#1361](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1361))


### OpenSearch Security Dashboards Plugin


* Filter blank backend role before creating internal user ([#2330](https://github.com/opensearch-project/security-dashboards-plugin/pull/2330))


### OpenSearch User Behavior Insights


* Adapt ActionFilter interface to core change ([#142](https://github.com/opensearch-project/user-behavior-insights/pull/142))
* export CI env var as true to skip git diff on depth=1 checkout ([#146](https://github.com/opensearch-project/user-behavior-insights/pull/146))
* Fix the plugin publish zip errors ([#151](https://github.com/opensearch-project/user-behavior-insights/pull/151))


### OpenSearch k-NN


* Fix blocking old indices created before 2.18 to use memory optimized search. ([#2918](https://github.com/opensearch-project/k-NN/pull/2918))
* Fix NativeEngineKnnQuery to return all part results for valid totalHits in response ([#2965](https://github.com/opensearch-project/k-NN/pull/2965))
* Fix unsafe concurrent update query vector in KNNQueryBuilder ([#2974](https://github.com/opensearch-project/k-NN/pull/2974))
* Fix score to distance calculation for inner product in faiss [#2992](https://github.com/opensearch-project/k-NN/pull/2992)
* Fix Backwards Compatability on Segment Merge for Disk-Based vector search ([#2994](https://github.com/opensearch-project/k-NN/pull/2994))


### SQL


* Add hashCode() and equals() to the value class of ExprJavaType ([#4885](https://github.com/opensearch-project/sql/pull/4885))
* BucketAggretationParser should handle more non-composite bucket types ([#4706](https://github.com/opensearch-project/sql/pull/4706))
* Do not remove nested fields in resolving AllFieldsExcludeMeta ([#4708](https://github.com/opensearch-project/sql/pull/4708))
* Fix binning udf resolution / Add type coercion support for binning UDFs ([#4742](https://github.com/opensearch-project/sql/pull/4742))
* Fix bug that `Streamstats` command incorrectly treats null as a valid group ([#4777](https://github.com/opensearch-project/sql/pull/4777))
* Fix filter push down producing redundant filter queries ([#4744](https://github.com/opensearch-project/sql/pull/4744))
* Fix function identify problem in converting to sql dialect ([#4793](https://github.com/opensearch-project/sql/pull/4793))
* Fix search anonymizer only ([#4783](https://github.com/opensearch-project/sql/pull/4783))
* Fix sub-fields accessing of generated structs ([#4683](https://github.com/opensearch-project/sql/pull/4683))
* Fix wrong parameter and return result logic for LogPatternAggFunction ([#4868](https://github.com/opensearch-project/sql/pull/4868))
* Grouping key field type can only be overwritten when the `ExprCoreType`s are different ([#4850](https://github.com/opensearch-project/sql/pull/4850))
* Fix eval on grouped fields after timechart ([#4758](https://github.com/opensearch-project/sql/pull/4758))
* Support access to nested field of struct after fields command ([#4719](https://github.com/opensearch-project/sql/pull/4719))
* Support escaped field names in SPath parsing ([#4813](https://github.com/opensearch-project/sql/pull/4813))
* Support script pushdown in sort-on-measure pushdown rewriting ([#4749](https://github.com/opensearch-project/sql/pull/4749))
* Support serializing external OpenSearch UDFs at pushdown time ([#4618](https://github.com/opensearch-project/sql/pull/4618))
* Support using decimal as span literals ([#4717](https://github.com/opensearch-project/sql/pull/4717))
* Translate `SAFE_CAST` to `TRY_CAST` in Spark SQL ([#4788](https://github.com/opensearch-project/sql/pull/4788))
* Update syntax: like(string, PATTERN[, case\_sensitive]) ([#4837](https://github.com/opensearch-project/sql/pull/4837))
* [BugFix] Fix Memory Exhaustion for Multiple Filtering Operations in PPL ([#4841](https://github.com/opensearch-project/sql/pull/4841))
* Fix CVE-2025-48924 ([#4665](https://github.com/opensearch-project/sql/pull/4665))
* [BugFix] Fix unexpected shift of extraction for `rex` with nested capture groups in named groups ([#4641](https://github.com/opensearch-project/sql/pull/4641))
* Fix asc/desc keyword behavior for sort command ([#4651](https://github.com/opensearch-project/sql/pull/4651))
* Fixes for `Multisearch` and `Append` command ([#4512](https://github.com/opensearch-project/sql/pull/4512))
* Make nested alias type support referring to outer context ([#4673](https://github.com/opensearch-project/sql/pull/4673))
* Use table scan rowType in filter pushdown to fix rename issue ([#4670](https://github.com/opensearch-project/sql/pull/4670))
* Fix: Support Alias Fields in MIN, MAX, FIRST, LAST, and TAKE Aggregations ([#4621](https://github.com/opensearch-project/sql/pull/4621))
* Fix bin nested fields issue ([#4606](https://github.com/opensearch-project/sql/pull/4606))
* Change ComparableLinkedHashMap to compare Key than Value ([#4648](https://github.com/opensearch-project/sql/pull/4648))
* Replace all dots in fields of table scan's PhysType ([#4633](https://github.com/opensearch-project/sql/pull/4633))
* Return comparable LinkedHashMap in `valueForCalcite()` of ExprTupleValue ([#4629](https://github.com/opensearch-project/sql/pull/4629))
* Fix filter parsing failure on date fields with non-default format ([#4616](https://github.com/opensearch-project/sql/pull/4616))
* Fix compile issue in main ([#4608](https://github.com/opensearch-project/sql/pull/4608))
* Fix push down failure for min/max on derived field ([#4572](https://github.com/opensearch-project/sql/pull/4572))
* Add value type hint for derived aggregate group by field ([#4583](https://github.com/opensearch-project/sql/pull/4583))
* Fix sort push down into agg after project already pushed ([#4546](https://github.com/opensearch-project/sql/pull/4546))
* Update request builder after pushdown sort into agg buckets ([#4541](https://github.com/opensearch-project/sql/pull/4541))
* Including metadata fields type when doing agg/filter script push down ([#4522](https://github.com/opensearch-project/sql/pull/4522))
* Fix percentile bug ([#4539](https://github.com/opensearch-project/sql/pull/4539))
* Fix mapping after aggregation push down ([#4500](https://github.com/opensearch-project/sql/pull/4500))
* Throw an error when the conditions of case are not boolean values ([#4520](https://github.com/opensearch-project/sql/pull/4520))
* Fallback to sub-aggregation if composite aggregation doesn't support ([#4413](https://github.com/opensearch-project/sql/pull/4413))
* Fix the bug of explicit makeNullLiteral for UDT fields ([#4475](https://github.com/opensearch-project/sql/pull/4475))
* Fix missing keywordsCanBeId ([#4491](https://github.com/opensearch-project/sql/pull/4491))
* Fix issue 4441 ([#4449](https://github.com/opensearch-project/sql/pull/4449))
* Fix join type ambiguous issue when specify the join type with sql-like join criteria ([#4474](https://github.com/opensearch-project/sql/pull/4474))
* Remove shared mutable optimizer field that caused race condition ([#4454](https://github.com/opensearch-project/sql/pull/4454))
* Reverting to \_doc + \_id ([#4435](https://github.com/opensearch-project/sql/pull/4435))


## INFRASTRUCTURE


### OpenSearch Alerting


* Kotlin version upgrade ([#1993](https://github.com/opensearch-project/alerting/pull/1993))
* JDK upgrade to 25 and gradle upgrade to 9.2 ([#1995](https://github.com/opensearch-project/alerting/pull/1995))


### OpenSearch Anomaly Detection


* Test: Prevent oversized bulk requests in synthetic data test ([#1603](https://github.com/opensearch-project/anomaly-detection/pull/1603))
* Update CI to JDK 25 and gradle to 9.2 ([#1623](https://github.com/opensearch-project/anomaly-detection/pull/1623))


### OpenSearch Asynchronous Search


* Update to Gradle 9.2 and use JDK 25 for GHA ([#792](https://github.com/opensearch-project/asynchronous-search/pull/792))


### OpenSearch Cross Cluster Replication


* Update Gradle to 9.2.1 and CI to test on JDK 25 ([#1605](https://github.com/opensearch-project/cross-cluster-replication/pull/1605))


### OpenSearch Custom Codecs


* Update to Gradle 9.2 and test with JDK 25 ([#294](https://github.com/opensearch-project/custom-codecs/pull/294))


### OpenSearch Index Management


* Upgrade gradle to 9.2.0 and github actions JDK 25 ([#1534](https://github.com/opensearch-project/index-management/pull/1534))
* Dependabot: bump actions/github-script from 7 to 8 ([#1485](https://github.com/opensearch-project/index-management/pull/1485))


### OpenSearch Job Scheduler


* Dependabot: bump actions/checkout from 5 to 6 ([#863](https://github.com/opensearch-project/job-scheduler/pull/863))


### OpenSearch ML Commons


* Update JDK to 25 and Gradle to 9.2 ([#4465](https://github.com/opensearch-project/ml-commons/pull/4465))
* Fix dependency conflict and jar hell ([#4405](https://github.com/opensearch-project/ml-commons/pull/4405))
* Decrease Disk Circuit Breaker Free Space Threshold to unblock CI ([#4413](https://github.com/opensearch-project/ml-commons/pull/4413))
* Revert #4487 #4489 as it is resolved in build get image scripts ([#4498](https://github.com/opensearch-project/ml-commons/pull/4498))


### OpenSearch Neural Search


* Onboard to s3 snapshots ([#1618](https://github.com/opensearch-project/neural-search/pull/1618))


* Add BWC tests for Sparse ANN Seismic feature ([#1657](https://github.com/opensearch-project/neural-search/pull/1657))
* Add role assignment multi-node integ testing in CI ([#1663](https://github.com/opensearch-project/neural-search/pull/1663))
* Upgrade codecov-action version to v5 and fix codecov rate limit issue ([#1676](https://github.com/opensearch-project/neural-search/pull/1676))


### OpenSearch Notifications


* Upgrade Gradle to 9.2 and github actions to support java 25 ([#1101](https://github.com/opensearch-project/notifications/pull/1101))


### OpenSearch Learning To Rank Base


* Reduce the required coverage until we can improve it ([#258](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/258))
* Upgrade Gradle to 9.2.0 ([#263](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/263))


### OpenSearch System Templates


* Update Gradle to 9.2.0 and CI JDK to 25 ([#111](https://github.com/opensearch-project/opensearch-system-templates/pull/111))


### OpenSearch Query Insights


* Add multi-node, healthstats integration tests and fix flaky tests ([#482](https://github.com/opensearch-project/query-insights/pull/482))


### OpenSearch Search Relevance


* Use a system property to control run integ test with security plugin. [#287](https://github.com/opensearch-project/search-relevance/pull/287)


### OpenSearch Security Analytics


* Only use alerting SNAPSHOTS in SNAPSHOT build, otherwise use release artifacts ([#1608](https://github.com/opensearch-project/security-analytics/pull/1608))
* Jdk upgrade to 25 and gradle upgrade to 9.2 ([#1618](https://github.com/opensearch-project/security-analytics/pull/1618))


### OpenSearch Skills


* Gradle 9.2.0 and GitHub Actions JDK 25 Upgrade ([#675](https://github.com/opensearch-project/skills/pull/675))


### OpenSearch k-NN


* Include opensearchknn\_simd in build configurations ([#3025](https://github.com/opensearch-project/k-NN/pull/3025))


### SQL


* Add config for CodeRabbit review ([#4890](https://github.com/opensearch-project/sql/pull/4890))
* Split bwc-tests to bwc-rolling-upgrade and bwc-full-restart ([#4716](https://github.com/opensearch-project/sql/pull/4716))
* Update github workflows to move from macos-13 to 14 ([#4779](https://github.com/opensearch-project/sql/pull/4779))
* Fix the flaky CalcitePPLTcphIT ([#4846](https://github.com/opensearch-project/sql/pull/4846))
* Fix UT failure and Linkchecker failure ([#4809](https://github.com/opensearch-project/sql/pull/4809))
* Adding IT suite for PPL-based dashboards in Neo for CloudWatch Lake ([#4695](https://github.com/opensearch-project/sql/pull/4695))
* Add allowed\_warnings in yaml restful tests ([#4731](https://github.com/opensearch-project/sql/pull/4731))
* Mitigate the CI failure caused by 500 Internal Server Error ([#4646](https://github.com/opensearch-project/sql/pull/4646))
* Publish internal modules separately for downstream reuse ([#4484](https://github.com/opensearch-project/sql/pull/4484))
* Refactor JsonExtractAllFunctionIT and MapConcatFunctionIT ([#4623](https://github.com/opensearch-project/sql/pull/4623))
* Onboarding async query core and grammar files to maven snapshots ([#4598](https://github.com/opensearch-project/sql/pull/4598))
* Onboarding new maven snapshots publishing to s3 (sql) ([#4588](https://github.com/opensearch-project/sql/pull/4588))
* Fix JsonExtractAllFunctionIT failure ([#4556](https://github.com/opensearch-project/sql/pull/4556))
* Check server status before starting Prometheus ([#4537](https://github.com/opensearch-project/sql/pull/4537))
* Update stalled action ([#4485](https://github.com/opensearch-project/sql/pull/4485))
* Switch to Guice#createInjector and add concurrent SQL/PPL regression ITs ([#4462](https://github.com/opensearch-project/sql/pull/4462))
* Update delete\_backport\_branch workflow to include release-chores branches ([#4025](https://github.com/opensearch-project/sql/pull/4025))
* Add ignorePrometheus Flag for integTest and docTest ([#4442](https://github.com/opensearch-project/sql/pull/4442))


## DOCUMENTATION


### OpenSearch Search Relevance


* Updated Developer Guide with instructions for debugging unit tests via Gradle. ([#300](https://github.com/opensearch-project/search-relevance/pull/300))


### SQL


* Update PPL Command Documentation ([#4562](https://github.com/opensearch-project/sql/pull/4562))
* Doc update for `json_valid` ([#4803](https://github.com/opensearch-project/sql/pull/4803))
* Enhance tests and doc for eval isnull/isnotnull functions ([#4724](https://github.com/opensearch-project/sql/pull/4724))
* Update search.rst documentation ([#4686](https://github.com/opensearch-project/sql/pull/4686))
* Add more examples to the `where` command doc ([#4457](https://github.com/opensearch-project/sql/pull/4457))
* Update eventstats.rst ([#4447](https://github.com/opensearch-project/sql/pull/4447))


## MAINTENANCE


### OpenSearch Anomaly Detection Dashboards Plugin


* Bump js-yaml from 3.14.1 to 3.14.2 ([#1121](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1121))


### OpenSearch Common Utils


* Update logback dependencies to version 1.5.19 ([#893](https://github.com/opensearch-project/common-utils/pull/893))
* Upgrade to Gradle 9.2 ([#892](https://github.com/opensearch-project/common-utils/pull/892))


### OpenSearch Cross Cluster Replication


* Update Gradle to 9.2.1 and CI to test on JDK 25 ([#1605](https://github.com/opensearch-project/cross-cluster-replication/pull/1605))


### OpenSearch Dashboards Maps


* Increment version to 3.4.0.0 ([#769](https://github.com/opensearch-project/dashboards-maps/pull/769))
* update unit test workflow to include 3.\* branch ([#780](https://github.com/opensearch-project/dashboards-maps/pull/780))


### OpenSearch Dashboards Notifications


* Increment version to 3.4.0 ([#405](https://github.com/opensearch-project/dashboards-notifications/pull/405))


### OpenSearch Dashboards Observability


* Fix typo in checkout step name ([#2501](https://github.com/opensearch-project/dashboards-observability/pull/2501))
* [maintenance] Update snapshots and unit tests ([#2526](https://github.com/opensearch-project/dashboards-observability/pull/2526))
* Update CI workflows for Integ tests ([#2528](https://github.com/opensearch-project/dashboards-observability/pull/2528))


### OpenSearch Geospatial


* Update to Gradle 9.2 and run CI checks with JDK 25 ([#816](https://github.com/opensearch-project/geospatial/issues/816))


### OpenSearch Index Management


* Increments version to 3.4.0 and adds ActionFilter interface ([#1536](https://github.com/opensearch-project/index-management/pull/1536))
* Update logback dependencies to version 1.5.19 ([#1537](https://github.com/opensearch-project/index-management/pull/1537))
* Use optionalField for creation in ExplainSMPolicy serialization ([#1507](https://github.com/opensearch-project/index-management/pull/1507))


### OpenSearch Job Scheduler


* Upgrade to gradle 9.2 ([#864](https://github.com/opensearch-project/job-scheduler/pull/864))


### OpenSearch Neural Search


* Update to Gradle 9.2 and run CI checks with JDK 25 ([#1667](https://github.com/opensearch-project/neural-search/pull/1667))


### OpenSearch Observability


* Upgrade gradle to version 9.2 and Java to version 25 ([#1959](https://github.com/opensearch-project/observability/pull/1959))
* Bump logback core to 1.15.20 ([#1960](https://github.com/opensearch-project/observability/pull/1960))


### OpenSearch Performance Analyzer


* Upgrade to JDK25 and gradle 9.2.0 ([#896](https://github.com/opensearch-project/performance-analyzer/pull/896))


### OpenSearch Query Insights


* Gradle 9.2.0 and JDK 25 upgrade ([#486](https://github.com/opensearch-project/query-insights/pull/486))


### OpenSearch Reporting


* Upgrade gradle to version 9.2 and Java to version 25 ([#1139](https://github.com/opensearch-project/reporting/pull/1139))
* Bump logback core to 1.15.20 ([#1143](https://github.com/opensearch-project/reporting/pull/1143))


### OpenSearch Search Relevance


* Fixed dependency of `CalculateJudgmentsIT.java` on UBI plugin and created a strategy to handle when plugin does not exist. ([#311](https://github.com/opensearch-project/search-relevance/pull/311))
* Added JDWP debug support for the `test` Gradle task to allow debugging unit tests using `-Dtest.debug=1`. ([#300](https://github.com/opensearch-project/search-relevance/pull/300))
* Fixed duplicate JDWP configuration in the `integTest` Gradle task that caused `Cannot load this JVM TI agent twice` errors when running with `-Dtest.debug=1`. ([#296](https://github.com/opensearch-project/search-relevance/pull/296))
* Removed deprecated `AccessController.doPrivileged()` usage in `JsonUtils` to prevent warnings and ensure compatibility with newer Java versions. ([#307](https://github.com/opensearch-project/search-relevance/pull/307))
* Small cleans up to test classes. ([#288](https://github.com/opensearch-project/search-relevance/pull/288))
* Update to Gradle 9.2 and run CI checks with JDK 25 ([#319](https://github.com/opensearch-project/search-relevance/pull/319))


### OpenSearch Security


* Bump `org.junit.jupiter:junit-jupiter` from 5.13.4 to 5.14.1 ([#5678](https://github.com/opensearch-project/security/pull/5678), [#5764](https://github.com/opensearch-project/security/pull/5764))
* Bump `ch.qos.logback:logback-classic` from 1.5.18 to 1.5.20 ([#5680](https://github.com/opensearch-project/security/pull/5680), [#5724](https://github.com/opensearch-project/security/pull/5724))
* Bump `org.scala-lang:scala-library` from 2.13.16 to 2.13.18 ([#5682](https://github.com/opensearch-project/security/pull/5682), [#5809](https://github.com/opensearch-project/security/pull/5809))
* Bump `kafka_version` from 4.0.0 to 4.1.1 ([#5613](https://github.com/opensearch-project/security/pull/5613), [#5806](https://github.com/opensearch-project/security/pull/5806))
* Bump `org.gradle.test-retry` from 1.6.2 to 1.6.4 ([#5706](https://github.com/opensearch-project/security/pull/5706))
* Bump `org.checkerframework:checker-qual` from 3.51.0 to 3.52.0 ([#5705](https://github.com/opensearch-project/security/pull/5705), [#5821](https://github.com/opensearch-project/security/pull/5821))
* Bump `org.ow2.asm:asm` from 9.8 to 9.9 ([#5707](https://github.com/opensearch-project/security/pull/5707))
* Bump `stefanzweifel/git-auto-commit-action` from 6 to 7 ([#5704](https://github.com/opensearch-project/security/pull/5704))
* Bump `net.bytebuddy:byte-buddy` from 1.17.7 to 1.18.2 ([#5703](https://github.com/opensearch-project/security/pull/5703), [#5822](https://github.com/opensearch-project/security/pull/5822))
* Bump `derek-ho/start-opensearch` from 7 to 9 ([#5630](https://github.com/opensearch-project/security/pull/5630), [#5679](https://github.com/opensearch-project/security/pull/5679))
* Bump `github/codeql-action` from 3 to 4 ([#5702](https://github.com/opensearch-project/security/pull/5702))
* Bump `com.github.spotbugs` from 6.4.2 to 6.4.4 ([#5727](https://github.com/opensearch-project/security/pull/5727))
* Bump `com.autonomousapps.build-health` from 3.0.4 to 3.5.1 ([#5726](https://github.com/opensearch-project/security/pull/5726), [#5744](https://github.com/opensearch-project/security/pull/5744), [#5819](https://github.com/opensearch-project/security/pull/5819))
* Bump `spring_version` from 6.2.11 to 6.2.14 ([#5725](https://github.com/opensearch-project/security/pull/5725), [#5808](https://github.com/opensearch-project/security/pull/5808))
* Bump `org.springframework.kafka:spring-kafka-test` from 4.0.0-M5 to 4.0.0-RC1 ([#5742](https://github.com/opensearch-project/security/pull/5742))
* Bump `com.google.errorprone:error_prone_annotations` from 2.42.0 to 2.44.0 ([#5743](https://github.com/opensearch-project/security/pull/5743), [#5779](https://github.com/opensearch-project/security/pull/5779))
* Bump `actions/upload-artifact` from 4 to 5 ([#5740](https://github.com/opensearch-project/security/pull/5740))
* Bump `actions/download-artifact` from 5 to 6 ([#5739](https://github.com/opensearch-project/security/pull/5739))
* Bump `com.google.googlejavaformat:google-java-format` from 1.28.0 to 1.32.0 ([#5741](https://github.com/opensearch-project/security/pull/5741), [#5765](https://github.com/opensearch-project/security/pull/5765), [#5811](https://github.com/opensearch-project/security/pull/5811))
* Bump `com.jayway.jsonpath:json-path` from 2.9.0 to 2.10.0 ([#5767](https://github.com/opensearch-project/security/pull/5767))
* Bump `org.apache.ws.xmlschema:xmlschema-core` from 2.3.1 to 2.3.2 ([#5781](https://github.com/opensearch-project/security/pull/5781))
* Bump `commons-io:commons-io` from 2.20.0 to 2.21.0 ([#5780](https://github.com/opensearch-project/security/pull/5780))
* Bump `com.nimbusds:nimbus-jose-jwt` from 10.5 to 10.6 ([#5782](https://github.com/opensearch-project/security/pull/5782))
* Upgrade to gradle 9.2 and run CI with JDK 25 ([#5786](https://github.com/opensearch-project/security/pull/5786))
* Bump `commons-validator:commons-validator` from 1.10.0 to 1.10.1 ([#5807](https://github.com/opensearch-project/security/pull/5807))
* Bump `actions/checkout` from 5 to 6 ([#5810](https://github.com/opensearch-project/security/pull/5810))
* Bump `org.bouncycastle:bcpkix-jdk18on` from 1.82 to 1.83 ([#5825](https://github.com/opensearch-project/security/pull/5825))
* Bump `commons-codec:commons-codec` from 1.19.0 to 1.20.0 ([#5823](https://github.com/opensearch-project/security/pull/5823))
* Upgrade springframework to 7.0.1 and zookeeper to 3.9.4 ([#5829](https://github.com/opensearch-project/security/pull/5829))


### OpenSearch Security Dashboards Plugin


* Bump `Wandalen/wretry.action` from 3.3.0 to 3.8.0 ([#2322](https://github.com/opensearch-project/security-dashboards-plugin/pull/2322))
* Bump `stefanzweifel/git-auto-commit-action` from 6 to 7 ([#2329](https://github.com/opensearch-project/security-dashboards-plugin/pull/2329))
* Bump `derek-ho/setup-opensearch-dashboards` from 1 to 3 ([#2321](https://github.com/opensearch-project/security-dashboards-plugin/pull/2321))
* Bump `actions/setup-java` from 4 to 5 ([#2323](https://github.com/opensearch-project/security-dashboards-plugin/pull/2323))
* Bump `actions/checkout` from 5 to 6 ([#2339](https://github.com/opensearch-project/security-dashboards-plugin/pull/2339))


### OpenSearch User Behavior Insights


* Onboarding new maven snapshots publishing to s3 ([#140](https://github.com/opensearch-project/user-behavior-insights/pull/140))
* Update Documentation from OS 3.1 to 3.3 ([#127](https://github.com/opensearch-project/user-behavior-insights/pull/131))
* Bump jdk25 ([#148](https://github.com/opensearch-project/user-behavior-insights/pull/148))


### OpenSearch k-NN


* Onboard to s3 snapshots ([#2943](https://github.com/opensearch-project/k-NN/pull/2943))
* Gradle 9.2.0 and GitHub Actions JDK 25 Upgrade ([#2984](https://github.com/opensearch-project/k-NN/pull/2984))


### SQL


* Bump Calcite to 1.41.0 ([#4714](https://github.com/opensearch-project/sql/pull/4714))
* Execute yamlRestTest in integration job ([#4838](https://github.com/opensearch-project/sql/pull/4838))
* Fix test failures due to version in mapping ([#4748](https://github.com/opensearch-project/sql/pull/4748))
* Support timeouts for Calcite queries ([#4857](https://github.com/opensearch-project/sql/pull/4857))
* [Maintenance] Enforce PR label of 'bugFix' instead of 'bug' ([#4773](https://github.com/opensearch-project/sql/pull/4773))
* [3.4.0] Bump Gradle to 9.2.0 and GitHub Action JDK to 25 ([#4824](https://github.com/opensearch-project/sql/pull/4824))
* Fix clickbench query 43 ([#4861](https://github.com/opensearch-project/sql/pull/4861))
* Update big5 ppl queries and check plans ([#4668](https://github.com/opensearch-project/sql/pull/4668))
* Revert "Update grammar files and developer guide (#4301)" ([#4643](https://github.com/opensearch-project/sql/pull/4643))
* Increment version to 3.4.0-SNAPSHOT ([#4452](https://github.com/opensearch-project/sql/pull/4452))
* Revert partial of #4401 ([#4503](https://github.com/opensearch-project/sql/pull/4503))
* Implement one-batch lookahead for index enumerators ([#4345](https://github.com/opensearch-project/sql/pull/4345))
* Refactor name resolution in Calcite PPL ([#4393](https://github.com/opensearch-project/sql/pull/4393))


## REFACTORING


### OpenSearch Security


* [Resource Sharing] Make migrate api require default access level to be supplied and updates documentations + tests ([#5717](https://github.com/opensearch-project/security/pull/5717))
* [Resource Sharing] Removes share and revoke java APIs ([#5718](https://github.com/opensearch-project/security/pull/5718))
* Fix build failure in SecurityFilterTests ([#5736](https://github.com/opensearch-project/security/pull/5736))
* [Resource Sharing]Refactor ResourceProvider to an interface and other ResourceSharing refactors ([#5755](https://github.com/opensearch-project/security/pull/5755))
* Replace AccessController and remove restriction on word Extension ([#5750](https://github.com/opensearch-project/security/pull/5750))
* Add security provider earlier in bootstrap process ([#5749](https://github.com/opensearch-project/security/pull/5749))
* [GRPC] Fix compilation errors from core protobuf version bump to 0.23.0 ([#5763](https://github.com/opensearch-project/security/pull/5763))
* Modularized PrivilegesEvaluator ([#5791](https://github.com/opensearch-project/security/pull/5791))
* [Resource Sharing] Adds post support for update sharing info API ([#5799](https://github.com/opensearch-project/security/pull/5799))
* Cleaned up use of PrivilegesEvaluatorResponse ([#5804](https://github.com/opensearch-project/security/pull/5804))
* Remove reflective call to getInnerChannel ([#5816](https://github.com/opensearch-project/security/pull/5816))


### OpenSearch Security Dashboards Plugin


* [Resource Sharing] Changes patch update sharing API to post ([#2338](https://github.com/opensearch-project/security-dashboards-plugin/pull/2338))


### OpenSearch k-NN


* Refactor to not use parallel for MMR rerank. ([#2968](https://github.com/opensearch-project/k-NN/pull/2968))


## NON-COMPLIANT


## ADDED


### OpenSearch Security


* Add support for Basic Authentication in webhook audit log sink using `plugins.security.audit.config.username` and `plugins.security.audit.config.password` ([#5792](https://github.com/opensearch-project/security/pull/5792))


## CHANGED


### OpenSearch Security


* Ensure all restHeaders from ActionPlugin.getRestHeaders are carried to threadContext for tracing ([#5396](https://github.com/opensearch-project/security/pull/5396))
* Deprecate plugins.security.system\_indices.indices ([#5775](https://github.com/opensearch-project/security/pull/5775))
* Allow overlap of static and custom security configs, but prefer static ([#5805](https://github.com/opensearch-project/security/pull/5805))
* Update read access to specific search-relevance indices ([#5590](https://github.com/opensearch-project/security/pull/5590))


