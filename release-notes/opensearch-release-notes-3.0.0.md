# OpenSearch and OpenSearch Dashboards 3.0.0 Release Notes

## Release Highlights

OpenSearch 3.0 delivers significant upgrades for performance, data management, security, vector database functionality, and more to help you build and deploy powerful, flexible solutions for search, analytics, observability, and other use cases.

### New and Updated Features

* Among the significant performance improvements included in OpenSearch 3.0 is an update to range queries. Applying smarter strategies for numeric and date fields, OpenSearch can now answer range filters with far fewer I/O operations to deliver 25% faster performance in Big5 benchmarks.
* New optimization features for high-cardinality queries introduce execution hints for cardinality aggregation, enabling users to better balance precision and performance. This enhancement achieves a 75% reduction in p90 latency in benchmark testing compared to the previous release.
* Concurrent segment search is now enabled by default for k-NN, delivering up to 2.5x faster query performance. Additionally, improvements to the floor segment size setting help improve tail latencies by up to 20%.
* Date histogram aggregations now benefit from enhanced filter rewrite optimization that supports sub-aggregations, offering significant performance gains for real-world use cases requiring multi-level aggregations.
* Derived source for k-NN vectors is production ready in this release, optimizing vector search performance with up to 30x improvement in cold start query latencies. This feature can also reduce storage requirements by 3x across the Faiss, Lucene, and NMSLIB libraries.
* Semantic sentence highlighting introduces context-aware highlighting to identify and highlight relevant sentences based on meaning, not just keyword matches, working seamlessly with traditional search as well as neural and hybrid search. This feature includes a pre-trained model for basic semantic highlighting use cases.
* Concurrent Segment Search is now enabled by default for k-NN, delivering up to 2.5x faster query performance. Additionally, improvements to the floor segment size setting help improve tail latencies by up to 20%.
* The new explain parameter for Faiss engine queries provides detailed insights into k-NN query scoring processes. This enhancement helps users understand and optimize their query results by providing a comprehensive view into search result scores.
* This release changes the default BM25 scoring function from LegacyBM25Similarity to BM25Similarity. This provides better compatibility with the latest Apache Lucene optimizations and removes unnecessary legacy code, leading to cleaner, more maintainable implementations while preserving search result quality.
* Piped Processing Language (PPL) receives powerful new capabilities with lookup, join, and subsearch commands, improving log correlation and filtering capabilities. These enhancements, backed by Apache Calcite, enable better query planning and execution for interactive data exploration.
* Query insights see major improvements with a new live queries API for real-time monitoring and a verbose parameter for optimized dashboard performance. Dynamic columns in the query insights dashboard support efficient query analysis.
* The observability experience is enhanced with contextual launch for anomaly detection, allow you to launch an anomaly detector from the main dashboard and automatically populating relevant logs in the Discover view. This streamlined workflow can significantly accelerate the task of investigating anomalies.
* Z-score normalization introduces a new statistical approach for hybrid search score normalization that better handles outliers compared to the default score-based normalization method. This supports more consistent and reliable hybrid search results.
* The addition of lower bound min-max normalization helps prevent over-amplification of low scores in hybrid search results by establishing minimum thresholds during normalization, supporting  more relevant and proportionate search results.
* Inner hits support for hybrid queries provides detailed visibility into results that are hidden by default when searching nested or parent-join fields.
* Star-tree indexing capabilities have been expanded to support metric aggregations and filtered terms queries, delivering up to 100x reduction in query work. This enhancement particularly benefits high-cardinality group-by operations and multi-level aggregations.
* New functionality lets you separates indexing and search traffic in remote store-enabled clusters to support failure isolation, enable independent scaling, and improve performance and efficiency.  For use cases that write-once and read-many, a new _scale API allows you to turn of all writers and make an index search only.  
* A new security framework replaces the Java Security Manager with a Java agent that enables OpenSearch to intercept privileged calls and ensure that the caller performing the privileged action has permissions. The replacement is configured in the same manner as the JSM, with policy files that give grants to individual codebases which specify the privileged actions they are allowed to perform.
* The Security plugin receives significant performance improvements through optimized privilege evaluation. These enhancements reduce internal serialization overhead and improve cluster performance for deployments using advanced security features.
* A new PGP public key has been implemented for version 3.0.0 and above, updating the artifact verification process, valid through March 6, 2027. The previous key will continue to be used for 2.x releases only.
* You can now configure node-level circuit breakers in OpenSearch k-NN, introducing the possibility of heterogenous circuit breaker limits, offering benefits for scenarios in which clusters live in mixed-hardware environments with different memory constraints.

### Experimental Features

* OpenSearch 3.0 includes the following experimental functionality. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.
* New experimental GPU acceleration for vector search operations offers substantial performance gains, delivering up to 9.3x faster indexing speeds while reducing operational costs by 3.75x compared to CPU-based solutions.
* This release introduces experimental high-performance data transport using protocol buffers (protobuf) over gRPC, enabling concurrent requests over single TCP connections. This can significantly reduces serialization overhead compared to JSON and provides an efficient path for integrating OpenSearch into existing gRPC ecosystems.
* Pull-based ingestion allows OpenSearch to fetch data directly from streaming sources like Apache Kafka and Amazon Kinesis. This experimental feature supports improved data pipeline stability, natively handling backpressure and offering a more resilient approach to ingestion.
* Experimental native Model Context Protocol (MCP) support enables seamless integration with AI agents, standardizing communications across LLM applications, data sources, and tools. This makes it easier to integrate OpenSearch with external AI agents such as Anthropic, LangChain, and OpenAI and build AI-powered applications. 
* A new plan-execute-reflect agent introduces autonomous problem-solving capabilities that break complex tasks into manageable steps. This intelligent agent supports iterative improvement through reflection, making it particularly effective for complex troubleshooting scenarios.


## Release Details
[OpenSearch and OpenSearch Dashboards 3.0.0](https://opensearch.org/artifacts/by-version/#release-3-0-0) includes the following breaking changes, features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.

OpenSearch [Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.0.0.md).

OpenSearch Dashboards [Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.0.0.md).

## Deprecation Notices

### Deprecating support for Ubuntu Linux 20.04
Please note that OpenSearch and OpenSearch Dashboards will deprecate support for Ubuntu Linux 20.04 as a continuous integration build image and supported operating system in an upcoming version, as Ubuntu Linux 20.04 will reach end-of-life with standard support as of April 2025 (refer to [this notice](https://ubuntu.com/blog/ubuntu-20-04-lts-end-of-life-standard-support-is-coming-to-an-end-heres-how-to-prepare) from Canonical Ubuntu). For a list of the compatible operating systems, [visit here](https://opensearch.org/docs/latest/install-and-configure/os-comp/).

### Deprecating support for Amazon Linux 2 on OpenSearch Dashboards
Please note that OpenSearch Dashboards will deprecate support for Amazon Linux 2 as a continuous integration build image and supported operating system in an upcoming version, as Node.js 18 will reach end-of-life with support as of April 2025 (refer to [this notice](https://nodejs.org/en/blog/announcements/v18-release-announce) from nodejs.org) and newer version of Node.js LTS version (20+) will not support runtime on Amazon Linux 2. For a list of the compatible operating systems, [visit here](https://opensearch.org/docs/latest/install-and-configure/os-comp/).

## PGP Key Update (release@opensearch.org):

Please note that a new PGP public key (with release@opensearch.org email) is available for artifact verification on OpenSearch version 3.0.0 and above. OpenSearch’s current PGP public key (with opensearch@amazon.com email) will be reserved for 2.x releases only. Please visit https://opensearch.org/verify-signatures.html to download the new public key, which is scheduled to expire on March 6, 2027.

## Breaking Changes

* For a full list of breaking changes and deprecated/removed features in version 3.0.0, please see details in the [meta issues](https://github.com/opensearch-project/opensearch-build/issues/5243).
  * See OpenSearch [breaking changes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.0.0.md#breaking-changes).
  * See OpenSearch Dashboards [breaking changes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.0.0.md#-breaking-changes).

### OpenSearch

* Upgrade to Lucene 10.1.0 - PR ([#16366](https://github.com/opensearch-project/OpenSearch/pull/16366))
* JDK21 as minimum supported Java runtime ([#10745](https://github.com/opensearch-project/OpenSearch/issues/10745))
* Remove deprecated terms from Java API ([#5214](https://github.com/opensearch-project/OpenSearch/issues/5214))
* JPMS Support (Eliminate top level split packages ) Phase-0 only ([#8110](https://github.com/opensearch-project/OpenSearch/issues/8110))
* Add ThreadContextPermission for stashAndMergeHeaders and stashWithOrigin ([#15039](https://github.com/opensearch-project/OpenSearch/pull/15039))
* Add ThreadContextPermission for markAsSystemContext and allow core to perform the method ([#15016](https://github.com/opensearch-project/OpenSearch/pull/15016))
* Migrate client transports to Apache HttpClient / Core 5.x ([#4459](https://github.com/opensearch-project/OpenSearch/pull/4459))
* Validation changes on the Bulk Index API like enforcing 512 byte _id size limit ([#6595](https://github.com/opensearch-project/OpenSearch/issues/6595))
* Ability to use the node as coordinating node by passing node.roles as empty array ([#3412](https://github.com/opensearch-project/OpenSearch/issues/3412))
* Treat Setting value with empty array string as empty array ([#10625](https://github.com/opensearch-project/OpenSearch/pull/10625))
* Ensure Jackson default maximums introduced in 2.16.0 do not conflict with OpenSearch settings ([#11811](https://github.com/opensearch-project/OpenSearch/pull/11811))
* Setting a maximum depth for nested queries ([#11670](https://github.com/opensearch-project/OpenSearch/pull/11670))
* Fix interchanged formats of total_indexing_buffer_in_bytes and total_indexing_buffer ([#17070](https://github.com/opensearch-project/OpenSearch/pull/17070))
* Cleanup deprecated thread pool settings ([#2595](https://github.com/opensearch-project/OpenSearch/issues/2595))
* Replace "blacklist/whitelist" terminology in Java APIs ([#1683](https://github.com/opensearch-project/OpenSearch/issues/1683))
* Remove deprecated methods from JodaCompatibleZonedDateTime which are called by scripts ([#3346](https://github.com/opensearch-project/OpenSearch/pull/3346))
* List of deprecated code removal in 3.0- partially done ([#2773](https://github.com/opensearch-project/OpenSearch/issues/2773))
* Remove mmap.extensions setting ([#9392](https://github.com/opensearch-project/OpenSearch/pull/9392))
* Remove COMPAT locale provider ([#13988](https://github.com/opensearch-project/OpenSearch/pull/13988))
* Remove transport-nio plugin ([#16887](https://github.com/opensearch-project/OpenSearch/issues/16887))
* Deprecate CamelCase PathHierarchy tokenizer name ([#10894](https://github.com/opensearch-project/OpenSearch/pull/10894))
* Rename Class ending with Plugin to Module under modules dir ([#4042](https://github.com/opensearch-project/OpenSearch/pull/4042))
* Remove deprecated `batch_size` parameter from `_bulk` ([#14283](https://github.com/opensearch-project/OpenSearch/issues/14283))
* Unset discovery nodes for every transport node actions request ([#17682](https://github.com/opensearch-project/OpenSearch/pull/17682))
* Added cluster:monitor/shards permission for _cat/shards action ([#13966](https://github.com/opensearch-project/OpenSearch/pull/13966))

### OpenSearch Dashboards

* Remove `CssDistFilename` ([#9446](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9446))
* Remove `withLongNumerals` in `HttpFetchOptions`. ([#9448](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9448))
* Remove `@elastic/filesaver` ([#9484](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9484))
* Bump `monaco-editor` from 0.17.0 to 0.30.1 ([#9497](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9497))
* Remove the deprecated "newExperience" table option in discover ([#9531](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9531))
* Bump monaco-editor from 0.30.1 to 0.52.0 ([#9618](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9618))

### OpenSearch ML Commons

* Use \_list/indices API instead of \_cat/index API in CatIndexTool ([#3243](https://github.com/opensearch-project/ml-commons/pull/3243))
* Deprecate the restful API of batch ingestion ([#3688](https://github.com/opensearch-project/ml-commons/pull/3688))

### OpenSearch Observability

* Remove support for legacy notebooks ([#2406](https://github.com/opensearch-project/dashboards-observability/pull/2406))

### OpenSearch Security

* Fix Blake2b hash implementation ([#5089](https://github.com/opensearch-project/security/pull/5089))
* Remove OpenSSL provider ([#5220](https://github.com/opensearch-project/security/pull/5220))
* Remove whitelist settings in favor of allowlist ([#5224](https://github.com/opensearch-project/security/pull/5224))

### OpenSearch k-NN

* Remove ef construction from Index Seeting ([#2564](https://github.com/opensearch-project/k-NN/pull/2564))
* Remove m from Index Setting ([#2564](https://github.com/opensearch-project/k-NN/pull/2564))
* Remove space type from index setting ([#2564](https://github.com/opensearch-project/k-NN/pull/2564))
* Remove Knn Plugin enabled setting ([#2564](https://github.com/opensearch-project/k-NN/pull/2564))

### OpenSearch SQL

* [v3.0.0] Bump gradle 8.10.2 / JDK23 on SQL plugin ([#3319](https://github.com/opensearch-project/sql/pull/3319))
* [v3.0.0] Remove SparkSQL support ([#3306](https://github.com/opensearch-project/sql/pull/3306))
* [v3.0.0] Remove opendistro settings and endpoints ([#3326](https://github.com/opensearch-project/sql/pull/3326))
* [v3.0.0] Deprecate SQL Delete statement ([#3337](https://github.com/opensearch-project/sql/pull/3337))
* [v3.0.0] Deprecate scroll API usage ([#3346](https://github.com/opensearch-project/sql/pull/3346))
* [v3.0.0] Deprecate OpenSearch DSL format ([#3367](https://github.com/opensearch-project/sql/pull/3367))
* [v3.0.0] Unified OpenSearch PPL Data Type ([#3345](https://github.com/opensearch-project/sql/pull/3345))
* [v3.0.0] Add datetime functions ([#3473](https://github.com/opensearch-project/sql/pull/3473))
* [v3.0.0] Support CAST function with Calcite ([#3439](https://github.com/opensearch-project/sql/pull/3439))


## FEATURES

### OpenSearch Dashboards Assistant

* Expose chatEnabled flag to capabilities ([#398](https://github.com/opensearch-project/dashboards-assistant/pull/398))
* Update chatbot UI to align with new look ([#435](https://github.com/opensearch-project/dashboards-assistant/pull/435))
* Add data to summary response post processing ([#436](https://github.com/opensearch-project/dashboards-assistant/pull/436))
* Add flag to control if display conversation list ([#438](https://github.com/opensearch-project/dashboards-assistant/pull/438))
* When open chatbot, load the last conversation automatically ([#439](https://github.com/opensearch-project/dashboards-assistant/pull/439))
* Add index type detection ([#454](https://github.com/opensearch-project/dashboards-assistant/pull/454))
* Add error handling when open chatbot and loading conversation ([#485](https://github.com/opensearch-project/dashboards-assistant/pull/485))
* Generate visualization on t2v page mount ([#505](https://github.com/opensearch-project/dashboards-assistant/pull/505))
* Update insight badge ([#507](https://github.com/opensearch-project/dashboards-assistant/pull/507))


### OpenSearch Dashboards Anomaly Detection

* Implmentation of contextual launch ([#1005](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1005))


### OpenSearch Common Utils

* Adding replication (CCR) plugin interface and classes to common-utils ([#667](https://github.com/opensearch-project/common-utils/pull/667))


### OpenSearch Custom Codecs

* Upgrade to Lucene 10.1.0 and Introduce new Codec implementation for the upgrade ([#228](https://github.com/opensearch-project/custom-codecs/pull/228))
* Bump ZTD lib version to 1.5.6-1 ([#232](https://github.com/opensearch-project/custom-codecs/pull/232))


### OpenSearch Dashboards Maps

* Introduce cluster layer in maps-dashboards ([#703](https://github.com/opensearch-project/dashboards-maps/pull/703))


### OpenSearch Dashboards Search Relevance

* Add cross cluster support ([#497](https://github.com/opensearch-project/dashboards-search-relevance/pull/497))


### OpenSearch Flow Framework

* Add per-tenant provisioning throttling ([#1074](https://github.com/opensearch-project/flow-framework/pull/1074))


### OpenSearch Dashboards Flow Framework

* Add fine-grained error handling ([#598](https://github.com/opensearch-project/dashboards-flow-framework/pull/598))
* Change ingestion input to JSON lines format ([#639](https://github.com/opensearch-project/dashboards-flow-framework/pull/639))


### OpenSearch Index Management

* Adding unfollow action in ism to invoke stop replication for ccr ([#1198](https://github.com/opensearch-project/index-management/pull/1198))


### OpenSearch ML Commons

* Onboard MCP ([#3721](https://github.com/opensearch-project/ml-commons/pull/3721))
* Plan, Execute and Reflect Agent Type ([#3716](https://github.com/opensearch-project/ml-commons/pull/3716))
* Support custom prompts from user ([#3731](https://github.com/opensearch-project/ml-commons/pull/3731))
* Support MCP server in OpenSearch ([#3781](https://github.com/opensearch-project/ml-commons/pull/3781))


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
* Implement analyzer based neural sparse query ([#1088](https://github.com/opensearch-project/neural-search/pull/1088))
* [Semantic Field] Add semantic field mapper. ([#1225](https://github.com/opensearch-project/neural-search/pull/1225))


### OpenSearch Security Analytics

* Adds support for uploading threat intelligence in Custom Format ([#1493](https://github.com/opensearch-project/security-analytics/pull/1493))


### OpenSearch Dashboards Security Analytics

* Add support for custom ioc schema in threat intel source ([#1266](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1266))


### OpenSearch Skills

* Add web search tool ([#547](https://github.com/opensearch-project/skills/pull/547))


### OpenSearch k-NN

* [Remote Vector Index Build] Client polling mechanism, encoder check, method parameter retrieval ([#2576](https://github.com/opensearch-project/k-NN/pull/2576))
* [Remote Vector Index Build] Move client to separate module ([#2603](https://github.com/opensearch-project/k-NN/pull/2603))
* Add filter function to KNNQueryBuilder with unit tests and integration tests ([#2599](https://github.com/opensearch-project/k-NN/pull/2599))
* [Lucene On Faiss] Add a new mode, memory-optimized-search enable user to run vector search on FAISS index under memory constrained environment. ([#2630](https://github.com/opensearch-project/k-NN/pull/2630))
* [Remote Vector Index Build] Add metric collection for remote build process ([#2615](https://github.com/opensearch-project/k-NN/pull/2615))
* [Explain API Support] Added Explain API support for Exact/ANN/Radial/Disk based KNN search on Faiss Engine ([#2403](https://github.com/opensearch-project/k-NN/pull/2403))
* Introduce Remote Native Index Build feature flag, settings, and initial skeleton ([#2525](https://github.com/opensearch-project/k-NN/pull/2525))
* Implement vector data upload and vector data size threshold setting ([#2550](https://github.com/opensearch-project/k-NN/pull/2550))
* Implement data download and IndexOutput write functionality ([#2554](https://github.com/opensearch-project/k-NN/pull/2554))
* Introduce Client Skeleton + basic Build Request implementation ([#2560](https://github.com/opensearch-project/k-NN/pull/2560))
* Add concurrency optimizations with native memory graph loading and force eviction ([#2345](https://github.com/opensearch-project/k-NN/pull/2345))


### OpenSearch SQL

* PPL: Add `json` function and `cast(x as json)` function ([#3243](https://github.com/opensearch-project/sql/pull/3243))
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
* Support alias type field ([#3538](https://github.com/opensearch-project/sql/pull/3538))
* Support UDT for BINARY ([#3549](https://github.com/opensearch-project/sql/pull/3549))
* Support metadata field ([#3445](https://github.com/opensearch-project/sql/pull/3445))
* Support CASE function ([#3558](https://github.com/opensearch-project/sql/pull/3558))


## ENHANCEMENTS


### OpenSearch Dashboards Assistant

* Remove os\_insight agent ([#452](https://github.com/opensearch-project/dashboards-assistant/pull/452))
* Hide the assistant entry when there isn't data2summary agent ([#417](https://github.com/opensearch-project/dashboards-assistant/pull/417))
* Adjust buttons' padding inside alert in-context insight popover ([#467](https://github.com/opensearch-project/dashboards-assistant/pull/467))
* Add a space to the left of the AI action menu button ([#486](https://github.com/opensearch-project/dashboards-assistant/pull/486))
* Add a tooltip for disabled assistant action button ([#490](https://github.com/opensearch-project/dashboards-assistant/pull/490))
* Improve the text to visualization error handling ([#491](https://github.com/opensearch-project/dashboards-assistant/pull/491))
* Optimize source selector width in t2v page ([#497](https://github.com/opensearch-project/dashboards-assistant/pull/497))
* Show error message if PPL query does not contain aggregation ([#499](https://github.com/opensearch-project/dashboards-assistant/pull/499))
* Adjust the overall style of alert summary popover ([#501](https://github.com/opensearch-project/dashboards-assistant/pull/501))
* Change the background color, button position and text for alert summary popover ([#506](https://github.com/opensearch-project/dashboards-assistant/pull/506))
* Collect metrics for when t2viz triggered([#510](https://github.com/opensearch-project/dashboards-assistant/pull/510))
* Chatbot dock bottom border top([#511](https://github.com/opensearch-project/dashboards-assistant/pull/511))
* Update the no aggregation PPL error message([#512](https://github.com/opensearch-project/dashboards-assistant/pull/512))
* Remove redundant error toast([#515](https://github.com/opensearch-project/dashboards-assistant/pull/515))
* Add auto suggested aggregation for text2Viz ([#514](https://github.com/opensearch-project/dashboards-assistant/pull/514))
* Remove experimental badge for natural language vis ([#516](https://github.com/opensearch-project/dashboards-assistant/pull/516))
* Revert "Add http error instruction for t2ppl task" ([#519](https://github.com/opensearch-project/dashboards-assistant/pull/519))
* t2viz remove fields clause from generated PPL query ([#525](https://github.com/opensearch-project/dashboards-assistant/pull/525))
* Render Icon based on the chat status ([#523](https://github.com/opensearch-project/dashboards-assistant/pull/523))
* Add scroll load conversations ([#530](https://github.com/opensearch-project/dashboards-assistant/pull/530))
* Refactor InContext style, add white logo and remove outdated code ([#529](https://github.com/opensearch-project/dashboards-assistant/pull/529))
* Change chatbot entry point to a single button ([#540](https://github.com/opensearch-project/dashboards-assistant/pull/540))
* Support streaming output([#493](https://github.com/opensearch-project/dashboards-assistant/pull/493))
* Update event names for t2v and feedback ([#543](https://github.com/opensearch-project/dashboards-assistant/pull/543))


### OpenSearch Anomaly Detection


* Use testclusters when testing with security ([#1414](https://github.com/opensearch-project/anomaly-detection/pull/1414))
* Add AWS SAM template for WAF log analysis and anomaly detection ([#1460](https://github.com/opensearch-project/anomaly-detection/pull/1460))


### OpenSearch Dashboards Flow Framework

* Integrate legacy presets with quick-configure fields ([#602](https://github.com/opensearch-project/dashboards-flow-framework/pull/602))
* Simplify RAG presets, add bulk API details ([#610](https://github.com/opensearch-project/dashboards-flow-framework/pull/610))
* Improve RAG preset experience ([#617](https://github.com/opensearch-project/dashboards-flow-framework/pull/617))
* Update model options and callout ([#622](https://github.com/opensearch-project/dashboards-flow-framework/pull/622))
* Added popover to display links to suggested models ([#625](https://github.com/opensearch-project/dashboards-flow-framework/pull/625))
* Implicitly update input maps defined on non-expanded queries (common cases) ([#632](https://github.com/opensearch-project/dashboards-flow-framework/pull/632))
* Show interim JSON provision flow even if provisioned ([#633](https://github.com/opensearch-project/dashboards-flow-framework/pull/633))
* Add functional buttons in form headers, fix query parse bug ([#649](https://github.com/opensearch-project/dashboards-flow-framework/pull/649))
* Block simulate API calls if datasource version is missing ([#657](https://github.com/opensearch-project/dashboards-flow-framework/pull/657))
* Update default queries, update quick config fields, misc updates ([#660](https://github.com/opensearch-project/dashboards-flow-framework/pull/660))
* Update visible plugin name to 'AI Search Flows' ([#662](https://github.com/opensearch-project/dashboards-flow-framework/pull/662))
* Update plugin name and rearrange Try AI Search Flows card ([#664](https://github.com/opensearch-project/dashboards-flow-framework/pull/664))
* Add new RAG + hybrid search preset ([#665](https://github.com/opensearch-project/dashboards-flow-framework/pull/665))
* Update new index mappings if selecting from existing index ([#670](https://github.com/opensearch-project/dashboards-flow-framework/pull/670))
* Persist state across Inspector tab switches; add presets dropdown ([#671](https://github.com/opensearch-project/dashboards-flow-framework/pull/671))
* Simplify ML processor form when interface is defined ([#676](https://github.com/opensearch-project/dashboards-flow-framework/pull/676))
* Cache form across ML transform types ([#678](https://github.com/opensearch-project/dashboards-flow-framework/pull/678))
* Add callout if knn query does not have knn index ([#688](https://github.com/opensearch-project/dashboards-flow-framework/pull/688))
* Adding icons to reorder processors up and down ([#690](https://github.com/opensearch-project/dashboards-flow-framework/pull/690))
* Support optional model inputs ([#701](https://github.com/opensearch-project/dashboards-flow-framework/pull/701))
* Support whitespace for string constant; support ext toggling on ML resp processors ([#702](https://github.com/opensearch-project/dashboards-flow-framework/pull/702))


### OpenSearch ML Commons

* Support sentence highlighting QA model ([#3600](https://github.com/opensearch-project/ml-commons/pull/3600))
* Add parser for ModelTensorOutput and ModelTensors ([#3658](https://github.com/opensearch-project/ml-commons/pull/3658))
* Function calling for openai v1, bedrock claude and deepseek ([#3712](https://github.com/opensearch-project/ml-commons/pull/3712))
* Update highlighting model translator to adapt new model ([#3699](https://github.com/opensearch-project/ml-commons/pull/3699))
* Implement async mode in agent execution ([#3714](https://github.com/opensearch-project/ml-commons/pull/3714))


### OpenSearch Neural Search

* Set neural-search plugin 3.0.0 baseline JDK version to JDK-21 ([#838](https://github.com/opensearch-project/neural-search/pull/838))
* Support different embedding types in model's response ([#1007](https://github.com/opensearch-project/neural-search/pull/1007))


### OpenSearch Observability


* Traces - Add "attributes" field ([#2432](https://github.com/opensearch-project/dashboards-observability/pull/2432))
* Traces - Update custom source toast/error/sorting ([#2407](https://github.com/opensearch-project/dashboards-observability/pull/2407))
* Adding Amazon Network Firewall Integration ([#2410](https://github.com/opensearch-project/dashboards-observability/pull/2410))
* Traces - Update custom source display, add toast ([#2403](https://github.com/opensearch-project/dashboards-observability/pull/2403))
* Trace to logs correlation, action icon updates ([#2398](https://github.com/opensearch-project/dashboards-observability/pull/2398))
* Traces - Custom source switch to data grid ([#2390](https://github.com/opensearch-project/dashboards-observability/pull/2390))
* Service Content/View Optimizationsc ([#2383](https://github.com/opensearch-project/dashboards-observability/pull/2383))
* Database selector in "Set Up Integration" page ([#2380](https://github.com/opensearch-project/dashboards-observability/pull/2380))
* Support custom logs correlation ([#2375](https://github.com/opensearch-project/dashboards-observability/pull/2375))


### OpenSearch Query Insights

* Add strict hash check on top queries indices ([#266](https://github.com/opensearch-project/query-insights/pull/266))
* Add default index template for query insights local index ([#254](https://github.com/opensearch-project/query-insights/pull/254))
* Skip profile queries ([#298](https://github.com/opensearch-project/query-insights/pull/298))
* Add top\_queries API verbose param ([#300](https://github.com/opensearch-project/query-insights/pull/300))
* Feat integ tests for exporter n reader ([#310](https://github.com/opensearch-project/query-insights/pull/310))
* Inflight Queries API ([#295](https://github.com/opensearch-project/query-insights/pull/295))


### OpenSearch Dashboards Query Insights

* Dynamically display columns ([#103](https:/github.com/opensearch-project/query-insights-dashboards/pull/103))
* Fetch top query with verbose=false on overview ([#164](https:/github.com/opensearch-project/query-insights-dashboards/pull/164))
* Fetch only once if the first call returns a valid query ([#182](https:/github.com/opensearch-project/query-insights-dashboards/pull/182))


### OpenSearch Dashboards Security Plugin

* Add cat shard api permission ([#2223](https://github.com/opensearch-project/security-dashboards-plugin/pull/2223))
* Changes to remove tenant panels from roles pages when multitenancy is disabled ([#2218](https://github.com/opensearch-project/security-dashboards-plugin/pull/2218))


### OpenSearch k-NN

* Introduce node level circuit breakers for k-NN ([#2509](https://github.com/opensearch-project/k-NN/pull/2509))
* Added more detailed error messages for KNN model training ([#2378](https://github.com/opensearch-project/k-NN/pull/2378))


### OpenSearch SQL

* Add other functions to SQL query validator ([#3304](https://github.com/opensearch-project/sql/pull/3304))
* Improved patterns command with new algorithm ([#3263](https://github.com/opensearch-project/sql/pull/3263))
* Clean up syntax error reporting ([#3278](https://github.com/opensearch-project/sql/pull/3278))
* Support line comment and block comment in PPL ([#2806](https://github.com/opensearch-project/sql/pull/2806))
* Function framework refactoring ([#3522](https://github.com/opensearch-project/sql/pull/3522))
* Add SQLQuery Utils support for Vaccum queries ([#3269](https://github.com/opensearch-project/sql/pull/3269))


### OpenSearch Security

* Optimized Privilege Evaluation ([#4380](https://github.com/opensearch-project/security/pull/4380))
* Add support for CIDR ranges in `ignore_hosts` setting ([#5099](https://github.com/opensearch-project/security/pull/5099))
* Add 'good' as a valid value for `plugins.security.restapi.password_score_based_validation_strength` ([#5119](https://github.com/opensearch-project/security/pull/5119))
* Adding stop-replication permission to `index_management_full_access` ([#5160](https://github.com/opensearch-project/security/pull/5160))
* Replace password generator step with a secure password generator action ([#5153](https://github.com/opensearch-project/security/pull/5153))
* Run Security build on image from opensearch-build ([#4966](https://github.com/opensearch-project/security/pull/4966))


## BUG FIXES


### OpenSearch Dashboards Assistant

* Fixed incorrect message id field used ([#378](https://github.com/opensearch-project/dashboards-assistant/pull/378))
* Improve alert summary with backend log pattern experience ([#389](https://github.com/opensearch-project/dashboards-assistant/pull/389))
* Fixed in context feature returning 500 error if workspace is invalid to returning 4XX ([#429](https://github.com/opensearch-project/dashboards-assistant/pull/429))([#458](https://github.com/opensearch-project/dashboards-assistant/pull/458))
* Fix incorrect insight API response ([#473](https://github.com/opensearch-project/dashboards-assistant/pull/473/files))
* Improve error handling for index type detection ([#472](https://github.com/opensearch-project/dashboards-assistant/pull/472))
* Fix header button input sending messages to active conversation ([#481](https://github.com/opensearch-project/dashboards-assistant/pull/481))
* Shrink source selector in t2v page ([#492](https://github.com/opensearch-project/dashboards-assistant/pull/492))
* Increase search selector width in t2v page ([#495](https://github.com/opensearch-project/dashboards-assistant/pull/495))
* Fix bottom spacing for chatbot flyout's input box ([#496](https://github.com/opensearch-project/dashboards-assistant/pull/496))
* Fix incontext insight popover close ([#498](https://github.com/opensearch-project/dashboards-assistant/pull/498))
* Fix error handling for data source connection errors ([#500](https://github.com/opensearch-project/dashboards-assistant/pull/500))
* Fix bug by hiding alert summary when clicking alert name ([#482](https://github.com/opensearch-project/dashboards-assistant/pull/482))
* Fix alert summary message action position when no discover button ([#504](https://github.com/opensearch-project/dashboards-assistant/pull/504))
* Remove text in badge to make it compatible with small screen ([#509](https://github.com/opensearch-project/dashboards-assistant/pull/509))
* remove experimental badge for vis-nlp ([#528](https://github.com/opensearch-project/dashboards-assistant/pull/528))
* Fix vertically alignment of alert insights popover title ([#526](https://github.com/opensearch-project/dashboards-assistant/pull/526))
* Change alert summary icon color to white ([#533](https://github.com/opensearch-project/dashboards-assistant/pull/533))
* Fix query assistant menu disappear due to upstream method signature change([#541](https://github.com/opensearch-project/dashboards-assistant/pull/541))
* Fix .plugins-ml-memory-meta not found when get conversations ([#542](https://github.com/opensearch-project/dashboards-assistant/pull/542))
* Fix save to notebook with MDS ([#554](https://github.com/opensearch-project/dashboards-assistant/pull/554))


### OpenSearch Alerting

* Correct release notes filename ([#1831](https://github.com/opensearch-project/alerting/pull/1831))
* Use java-agent Gradle plugin to support phasing off SecurityManager usage in favor of Java Agent ([#1824](https://github.com/opensearch-project/alerting/pull/1637))
* Fix build due to phasing off SecurityManager usage in favor of Java Agent ([#1823](https://github.com/opensearch-project/alerting/pull/1823))
* Fix bucket selector aggregation writeable name. ([#1780](https://github.com/opensearch-project/alerting/pull/1780))


### OpenSearch Alerting Dashboards Plugin

* Alerting Dashboard doesn't find sub-fields when building the list of fields by type. ([#1234](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1234))


### OpenSearch Anomaly Detection

* Distinguish local cluster when local name is same as remote ([#1446](https://github.com/opensearch-project/anomaly-detection/pull/1446))


### OpenSearch Dashboards Anomaly Detection

* Switching fieldcaps api to utilize js client ([#984](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/984))
* Update namespace for alerting plugin to avoid conflict with alerting ([#1003](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1003))
* Fix remote cluster bug when remote and local have same name ([#1007](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1007))
* Display selected clusters correctly on edit page ([#1011](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1011))


### OpenSearch Common Utils

* Fix imports related to split package of org.opensearch.transport ([#790](https://github.com/opensearch-project/common-utils/pull/790))
* Escape/Unescape pipe UserInfo in ThreadContext ([#801](https://github.com/opensearch-project/common-utils/pull/801))


### OpenSearch Cross Cluster Replication

* Disabling knn validation checks ([#1515](https://github.com/opensearch-project/cross-cluster-replication/pull/1515))


### OpenSearch Custom Codecs

* Fix build due to phasing off SecurityManager usage in favor of Java Agent ([#235](https://github.com/opensearch-project/custom-codecs/pull/235))
* Add java agent plugin ([#237](https://github.com/opensearch-project/custom-codecs/pull/237))


### OpenSearch Dashboards Maps

* Fix layer config panel background color inconsistency ([#704](https://github.com/opensearch-project/dashboards-maps/pull/704))
* Fix overlapping data labels on map layer ([#718](https://github.com/opensearch-project/dashboards-maps/pull/718))


### OpenSearch Dashboards Reporting

* [Bug] Support for date range in report generation ([#524](https://github.com/opensearch-project/dashboards-reporting/pull/524))
* Updated the optional parameters for timefrom and timeto to resolve incorrect report generation scenarios ([#554](https://github.com/opensearch-project/dashboards-reporting/pull/554))
* [Bug] Reporting Popover UI ([#570](https://github.com/opensearch-project/dashboards-reporting/pull/570))


### OpenSearch Flow Framework

* Change REST status codes for RBAC and provisioning ([#1083](https://github.com/opensearch-project/flow-framework/pull/1083))
* Fix Config parser does not handle tenant\_id field ([#1096](https://github.com/opensearch-project/flow-framework/pull/1096))
* Complete action listener on failed synchronous workflow provisioning ([#1098](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/1098))
* Add new attributes field to ToolStep ([#1113](https://github.com/opensearch-project/flow-framework/pull/1113))
* Fix bug handleReprovision missing wait\_for\_completion\_timeout response ([#1107](https://github.com/opensearch-project/flow-framework/pull/1107))


### OpenSearch Dashboards Flow Framework

* Fix error that local cluster cannot get version ([#606](https://github.com/opensearch-project/dashboards-flow-framework/pull/606))
* UX fit-n-finish updates XI ([#613](https://github.com/opensearch-project/dashboards-flow-framework/pull/613))
* UX fit-n-finish updates XII ([#618](https://github.com/opensearch-project/dashboards-flow-framework/pull/618))
* Bug fixes XIII ([#630](https://github.com/opensearch-project/dashboards-flow-framework/pull/630))
* Various bug fixes & improvements ([#644](https://github.com/opensearch-project/dashboards-flow-framework/pull/644))
* Fixed bug related to Search Index in Local Cluster scenario ([#654](https://github.com/opensearch-project/dashboards-flow-framework/pull/654))
* Fix missed UI autofilling after JSON Lines change ([#672](https://github.com/opensearch-project/dashboards-flow-framework/pull/672))


### OpenSearch Index Management

* Target Index Settings if create index during rollup ([#1377](https://github.com/opensearch-project/index-management/pull/1377))
* Fixed CVE upgrade logback-core to 1.5.13 ([#1388](https://github.com/opensearch-project/index-management/pull/1388))
* Fix issue in Docker Security Tests where qualifier is not being parsed correctly ([#1401](https://github.com/opensearch-project/index-management/pull/1401))
* Fix build due to phasing off SecurityManager usage in favor of Java Agent ([#1404](https://github.com/opensearch-project/index-management/pull/1404))


### OpenSearch Dashboards Index Management Plugin

* Fix wrong urls to documentation ([#1278](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1278))
* Fixed CVE in glob-parent and braces dependencies ([#1287](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1287))
* Fixed CVE: Updated elliptic dependency resolution ([#1290](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1290))
* Fix: Update @babel dependencies to address RegExp vulnerability ([#1296](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1296))
* Fixed CVE: Updated babel dependencies ([#1308](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1308))
* Fixed verify-binary-installation workflow file ([#1309](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1309))


### OpenSearch Job Scheduler

* Fix job-scheduler with OpenSearch Refactoring ([#730](https://github.com/opensearch-project/job-scheduler/pull/730))
* Fetch certs from security repo and remove locally checked in demo certs ([#713](https://github.com/opensearch-project/job-scheduler/pull/713))
* Only download demo certs when integTest run with `-Dsecurity.enabled=true` ([#737](https://github.com/opensearch-project/job-scheduler/pull/737))


### OpenSearch ML Commons

* Fix building error due to a breaking change from core ([#3617](https://github.com/opensearch-project/ml-commons/pull/3617))
* Fixing the circuit breaker issue for remote model ([#3652](https://github.com/opensearch-project/ml-commons/pull/3652))
* Fix compilation error ([#3667](https://github.com/opensearch-project/ml-commons/pull/3667))
* Revert CI workflow changes ([#3674](https://github.com/opensearch-project/ml-commons/pull/3674))
* Fix config index masterkey pull up for multi-tenancy ([#3700](vhttps://github.com/opensearch-project/ml-commons/pull/3700))
* Fix error message when input map and output map length not match ([#3730](https://github.com/opensearch-project/ml-commons/pull/3730))
* Agent Framework: Handle model response when toolUse is not accompanied by text ([#3755](https://github.com/opensearch-project/ml-commons/pull/3755))
* Allow user to control react agent max\_interations value to prevent empty response ([#3756](https://github.com/opensearch-project/ml-commons/pull/3756))
* Agent framework: Fix SearchIndexTool to parse special floating point values and NaN ([#3754](https://github.com/opensearch-project/ml-commons/pull/3754))
* Directly return Response objects from metadata client responses ([#3768](https://github.com/opensearch-project/ml-commons/pull/3768))
* Remove opensearch-ml-2.4.0.0.zip file that was added by random mistake ([#3763](https://github.com/opensearch-project/ml-commons/pull/3763))
* Replace null GetResponse with valid response and not exists ([#3759](https://github.com/opensearch-project/ml-commons/pull/3759))
* Fix ListIndexTool and SearchIndexTool ([#3720](https://github.com/opensearch-project/ml-commons/pull/3720))
* Support MCP session management ([#3803](https://github.com/opensearch-project/ml-commons/pull/3803))
* Support customized message endpoint and addressing comments ([#3810](https://github.com/opensearch-project/ml-commons/pull/3810))
* Excluding circuit breaker for Agent ([#3814](https://github.com/opensearch-project/ml-commons/pull/3814))


### OpenSearch Dashboards ML Commons

* Fix data source not compatible with prerelease ([#411](https://github.com/opensearch-project/ml-commons-dashboards/pull/411))
* Fix verify install binary workflow failed ([#421](https://github.com/opensearch-project/ml-commons-dashboards/pull/421))


### OpenSearch Neural Search

* Fix a bug to unflatten the doc with list of map with multiple entries correctly ([#1204](https://github.com/opensearch-project/neural-search/pull/1204))
* Remove validations for unmapped fields (text and image) in TextImageEmbeddingProcessor ([#1230](https://github.com/opensearch-project/neural-search/pull/1230))
* Add validations to prevent empty input\_text\_field and input\_image\_field in TextImageEmbeddingProcessor ([#1257](https://github.com/opensearch-project/neural-search/pull/1257))
* Fix score value as null for single shard when sorting is not done on score field ([#1277](https://github.com/opensearch-project/neural-search/pull/1277))


### OpenSearch Notifications

* Fix build due to phasing off SecurityManager usage in favor of Java Agent ([#1013](https://github.com/opensearch-project/notifications/pull/1013))


### OpenSearch Observability

* Traces - Custom Traces mode pagination reset ([#2437](https://github.com/opensearch-project/dashboards-observability/pull/2437))
* Fix(notebook): fix set\_paragraphs API ([#2417](https://github.com/opensearch-project/dashboards-observability/pull/2417))
* [Bug] Notebooks - Action popover ([#2418](https://github.com/opensearch-project/dashboards-observability/pull/2418))
* Fix link checker 404 and update the table of content in README ([#2413](https://github.com/opensearch-project/dashboards-observability/pull/2413))
* Cypress - Config fix ([#2408](https://github.com/opensearch-project/dashboards-observability/pull/2408))
* Application Analytics - Flaky cypress fix ([#2402](https://github.com/opensearch-project/dashboards-observability/pull/2402))
* Traces table fix for invalid date ([#2399](https://github.com/opensearch-project/dashboards-observability/pull/2399))
* Custom Traces- Sorting/Toast ([#2397](https://github.com/opensearch-project/dashboards-observability/pull/2397))
* Event Analytics - Cypress flaky fix ([#2395](https://github.com/opensearch-project/dashboards-observability/pull/2395))
* Services to Traces - Flyout redirection ([#2392](https://github.com/opensearch-project/dashboards-observability/pull/2392))
* [Bug] Traces/Services remove toast message on empty data ([#2346](https://github.com/opensearch-project/dashboards-observability/pull/2346))
* Restore spans limit to 3000 in trace view ([#2353](https://github.com/opensearch-project/dashboards-observability/pull/2353))
* [BUG] Updated cache for the sub tree in Workbench ([#2351](https://github.com/opensearch-project/dashboards-observability/pull/2351))
* Trace Groups Optimization - Remove duplicate filters ([#2368](https://github.com/opensearch-project/dashboards-observability/pull/2368))
* [Bug] Traces redirection while QA enabled ([#2369](https://github.com/opensearch-project/dashboards-observability/pull/2369))


### OpenSearch Observability

* Fix build due to phasing off SecurityManager usage in favor of Java Agent ([#1916](https://github.com/opensearch-project/observability/pull/1916))


### OpenSearch Learning To Rank Base

* Add a model parser for xgboost (for the correct serialization format) ([#151](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/151))
* Fix test to ApproximateScoreQuery ([#158](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/158))


### OpenSearch Query Insights

* Fix github upload artifact error ([#229](https://github.com/opensearch-project/query-insights/pull/229))
* Fix unit test SearchQueryCategorizerTests.testFunctionScoreQuery ([#270](https://github.com/opensearch-project/query-insights/pull/270))
* Fix pipeline on main branch ([#274](https://github.com/opensearch-project/query-insights/pull/274))
* Fix local index deletion timing ([#289](https://github.com/opensearch-project/query-insights/pull/289))
* Top queries api bugs ([#293](https://github.com/opensearch-project/query-insights/pull/293))
* Fix CVE-2025-27820 ([#317](https://github.com/opensearch-project/query-insights/pull/317))
* Fix flaky live queries tests ([#335](https://github.com/opensearch-project/query-insights/pull/335))


### OpenSearch Dashboards Query Insights

* Fix duplicated requests on refreshing the overview ([#138](https:/github.com/opensearch-project/query-insights-dashboards/pull/138))
* Bug Fix - Placeholder metric Not Replaced with Actual Metric Type ([#140](https:/github.com/opensearch-project/query-insights-dashboards/pull/140))
* Enable Correct Sorting for Metrics in Query Insights Dashboard ([#173](https:/github.com/opensearch-project/query-insights-dashboards/pull/173))
* Fix Window size changing unexpectedly ([#178](https:/github.com/opensearch-project/query-insights-dashboards/pull/178))


### OpenSearch Query Workbench

* [Bug] Side tree flyout fix in async operations ([#448](https://github.com/opensearch-project/dashboards-query-workbench/pull/448))


### OpenSearch Remote Metadata Sdk

* Fix version conflict check for update ([#114](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/114))
* Use SdkClientDelegate's classloader for ServiceLoader ([#121](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/121))
* Ensure consistent reads on DynamoDB getItem calls ([#128](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/128))
* Return 404 for Index not found on Local Cluster search ([#130](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/130))
* Directly return responses from Local Cluster client ([#141](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/141))
* Make generated responses robust to URL encoded id and index values ([#156](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/156))
* Validate request fields in DDB Put and Update implementations ([#157](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/157))
* Properly handle remote client search failures with status codes ([#158](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/158))


### OpenSearch Reporting

* Fix build due to phasing off SecurityManager usage in favor of Java Agent ([#1085](https://github.com/opensearch-project/reporting/pull/1085))


### OpenSearch Security Analytics

* Remove usage of deprecated batchSize() method ([#1503](https://github.com/opensearch-project/security-analytics/pull/1503))
* Refactored flaky test. ([#1467](https://github.com/opensearch-project/security-analytics/pull/1467))
* Remove overrides of preserveIndicesUponCompletion ([#1498](https://github.com/opensearch-project/security-analytics/pull/1498))


### OpenSearch Dashboards Security Analytics

* Fix custom rule creation. ([#1281](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1281))


### OpenSearch Skills

* Fix list bug of PPLTool when pass empty list ([#541](https://github.com/opensearch-project/skills/pull/541))


### OpenSearch k-NN

* Fixing bug to prevent NullPointerException while doing PUT mappings ([#2556](https://github.com/opensearch-project/k-NN/issues/2556))
* Add index operation listener to update translog source ([#2629](https://github.com/opensearch-project/k-NN/pull/2629))
* Add parent join support for faiss hnsw cagra ([#2647](https://github.com/opensearch-project/k-NN/pull/2647))
* [Remote Vector Index Build] Fix bug to support `COSINESIMIL` space type ([#2627](https://github.com/opensearch-project/k-NN/pull/2627))
* Disable doc value storage for vector field storage ([#2646](https://github.com/opensearch-project/k-NN/pull/2646))
* Fix KNN Quantization state cache have an invalid weight threshold ([#2666](https://github.com/opensearch-project/k-NN/pull/2666))
* Fix enable rescoring when dimensions > 1000. ([#2671](https://github.com/opensearch-project/k-NN/pull/2671))
* Fix derived source for binary and byte vectors ([#2533](https://github.com/opensearch-project/k-NN/pull/2533/))
* Fix the put mapping issue for already created index with flat mapper ([#2542](https://github.com/opensearch-project/k-NN/pull/2542))
* Fixing the bug to prevent index.knn setting from being modified or removed on restore snapshot ([#2445](https://github.com/opensearch-project/k-NN/pull/2445))


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
* Fix GET\_FORMAT UDF ([#3543](https://github.com/opensearch-project/sql/pull/3543))
* Fix timestamp bug ([#3542](https://github.com/opensearch-project/sql/pull/3542))
* Fix issue 2489 ([#3442](https://github.com/opensearch-project/sql/pull/3442))
* New added commands should throw exception when calcite disabled ([#3571](https://github.com/opensearch-project/sql/pull/3571))
* Support parsing documents with flattened value ([#3577](https://github.com/opensearch-project/sql/pull/3577))


### OpenSearch Security

* Fix version matcher string in demo config installer ([#5157](https://github.com/opensearch-project/security/pull/5157))
* Escape pipe character for injected users ([#5175](https://github.com/opensearch-project/security/pull/5175))
* Assume default of v7 models if \_meta portion is not present ([#5193](https://github.com/opensearch-project/security/pull/5193)))
* Fixed IllegalArgumentException when building stateful index privileges ([#5217](https://github.com/opensearch-project/security/pull/5217))
* DlsFlsFilterLeafReader::termVectors implementation causes assertion errors for users with FLS/FM active ([#5243](https://github.com/opensearch-project/security/pull/5243))
* Only check validity of certs in the chain of the node certificates ([#4979](https://github.com/opensearch-project/security/pull/4979))
* Corrections in DlsFlsFilterLeafReader regarding PointVales and object valued attributes ([#5304](https://github.com/opensearch-project/security/pull/5304))


## INFRASTRUCTURE


### OpenSearch Dashboards Assistant

* Fix failed UTs with OSD 3.0 ([#527](https://github.com/opensearch-project/dashboards-assistant/pull/527))
* Fix empty codecov report in CI([#547](https://github.com/opensearch-project/dashboards-assistant/pull/547))


### OpenSearch Anomaly Detection

* Adding dual cluster arg to gradle run ([#1441](https://github.com/opensearch-project/anomaly-detection/pull/1441))
* Fix build due to phasing off SecurityManager usage in favor of Java Agent ([#1450](https://github.com/opensearch-project/anomaly-detection/pull/1450))
* Using java-agent gradle plugin to phase off Security Manager in favor of Java-agent ([#1454](https://github.com/opensearch-project/anomaly-detection/pull/1454))
* Add integtest.sh to specifically run integTestRemote task ([#1456](https://github.com/opensearch-project/anomaly-detection/pull/1456))


### OpenSearch Dashboards Anomaly Detection

* Change gradle run to dualcluster is true ([#998](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/998))


### OpenSearch Dashboards Maps

* Increment version to 3.0.0-alpha1 ([#708](https://github.com/opensearch-project/dashboards-maps/pull/708))
* Bump up version to 3.0.0-beta1 [#716](https://github.com/opensearch-project/dashboards-maps/pull/716)


### OpenSearch Flow Framework

* Set Java target compatibility to JDK 21 ([#730](https://github.com/opensearch-project/flow-framework/pull/730))
* Use java-agent Gradle plugin to support phasing off SecurityManager usage in favor of Java Agent ([#1108](https://github.com/opensearch-project/flow-framework/pull/1108))


### OpenSearch Neural Search

* [3.0] Update neural-search for OpenSearch 3.0 compatibility ([#1141](https://github.com/opensearch-project/neural-search/pull/1141))
* [3.0] Update neural-search for OpenSearch 3.0 beta compatibility ([#1245](https://github.com/opensearch-project/neural-search/pull/1245))


### OpenSearch Observability

* Improve error handling when setting up and reading a new integration ([#2387](https://github.com/opensearch-project/dashboards-observability/pull/2387))
* Improve the test results for Integrations internals ([#2376](https://github.com/opensearch-project/dashboards-observability/pull/2376))


### OpenSearch Observability

* Using java-agent gradle plugin to phase off Security Manager in favor of Java-agent. ([#1917](https://github.com/opensearch-project/observability/pull/1917))


### OpenSearch Reporting

* Using java-agent gradle plugin to phase off Security Manager in favor of Java-agent. ([#1086](https://github.com/opensearch-project/reporting/pull/1086))


### OpenSearch Skills

* Replace `ml-common-client` build dependency to `ml-common-common` and `ml-common-spi` ([#529](https://github.com/opensearch-project/skills/pull/529))


### OpenSearch k-NN

* Add github action to run ITs against remote index builder ([2620](https://github.com/opensearch-project/k-NN/pull/2620))
* Removed JDK 11 and 17 version from CI runs ([#1921](https://github.com/opensearch-project/k-NN/pull/1921))
* Upgrade min JDK compatibility to JDK 21 ([#2422](https://github.com/opensearch-project/k-NN/pull/2422))


### OpenSearch SQL

* Build integration test framework ([#3342](https://github.com/opensearch-project/sql/pull/3342))
* Set bouncycastle version inline ([#3469](https://github.com/opensearch-project/sql/pull/3469))
* Use entire shadow jar to fix IT ([#3447](https://github.com/opensearch-project/sql/pull/3447))
* Separate with/without pushdown ITs ([#3413](https://github.com/opensearch-project/sql/pull/3413))
* Only enable fallback for tests that need to fall back ([#3544](https://github.com/opensearch-project/sql/pull/3544))
* Remove beta1 qualifier ([#3589](https://github.com/opensearch-project/sql/pull/3589))


## DOCUMENTATION


### OpenSearch Alerting

* Added 3.0 release notes. ([#1843](https://github.com/opensearch-project/alerting/pull/1843))


### OpenSearch Dashboards Alerting Plugin

* Added 3.0.0 release notes. ([#1246](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1246))


### OpenSearch Dashboards Notifications

* Added 3.0.0 release notes. ([#347](https://github.com/opensearch-project/dashboards-notifications/pull/347))


### OpenSearch Flow Framework

* Add text to visualization agent template ([#936](https://github.com/opensearch-project/flow-framework/pull/936))


### OpenSearch ML Commons

* Add tutorial for RAG of openai and bedrock ([#2975](https://github.com/opensearch-project/ml-commons/pull/2975))
* Fix template query link ([#3612](https://github.com/opensearch-project/ml-commons/pull/3612))
* Add standard blueprint for vector search ([#3659](https://github.com/opensearch-project/ml-commons/pull/3659))
* Add blueprint for Claude 3.7 on Bedrock ([#3584](https://github.com/opensearch-project/ml-commons/pull/3584))
* Add standard blueprint for azure embedding ada2 ([#3725](https://github.com/opensearch-project/ml-commons/pull/3725))


### OpenSearch Neural Search

* Adding code guidelines ([#502](https://github.com/opensearch-project/neural-search/pull/502))


### OpenSearch Notifications

* Add 3.0.0 release notes ([#1033](https://github.com/opensearch-project/notifications/pull/1033))


### OpenSearch Query Insights

* Release Notes 3.0.0.0-Alpha1 ([#278](https://github.com/opensearch-project/query-insights/pull/278))
* 3.0.0.0-beta1 Release Notes ([#294](https://github.com/opensearch-project/query-insights/pull/294))


### OpenSearch Dashboards Query Insights

* 3.0.0.0 Alpha1 Release Notes ([#147](https:/github.com/opensearch-project/query-insights-dashboards/pull/147))
* 3.0.0.0-beta1 Release Notes ([#157](https:/github.com/opensearch-project/query-insights-dashboards/pull/157))
* Update 3.0-beta1 release notes ([#160](https:/github.com/opensearch-project/query-insights-dashboards/pull/160))


### OpenSearch Remote Metadata Sdk

* Add a developer guide ([#124](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/124))


### OpenSearch Security Analytics

* Added 3.0.0 release notes. ([#1523](https://github.com/opensearch-project/security-analytics/pull/1523))


### OpenSearch Dashboards Security Analytics

* Added 3.0.0 release notes. ([#1283](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1283))


### OpenSearch Skills

* Add tutorial to build and test custom tool ([#521](https://github.com/opensearch-project/skills/pull/521))


### OpenSearch SQL

* Documentation for PPL new engine (V3) and limitations of 3.0.0 Beta ([#3488](https://github.com/opensearch-project/sql/pull/3488))


## MAINTENANCE


### OpenSearch Dashboards Assistant

* Bump version to 3.0.0.0-alpha1 ([#450](https://github.com/opensearch-project/dashboards-assistant/pull/450))
* Chore(deps): update dependency dompurify to v3.2.4 ([#461](https://github.com/opensearch-project/dashboards-assistant/pull/461))
* Chore(deps): update dependency dompurify to v3.2.3 ([#383](https://github.com/opensearch-project/dashboards-assistant/pull/383))
* Bump version to 3.0.0.0-beta1 ([#521](https://github.com/opensearch-project/dashboards-assistant/pull/521))
* Bump version to 3.0.0.0 ([#559](https://github.com/opensearch-project/dashboards-assistant/pull/559))
* Upgrade derek-ho/start-opensearch to v6 and set java version to 21 for OS 3.0 ([#563](https://github.com/opensearch-project/dashboards-assistant/pull/563))


### OpenSearch Alerting

* Increment version to 3.0.0-SNAPSHOT. ([#1837](https://github.com/opensearch-project/alerting/pull/1837))
* Disabled non-security tests from executing during security-enabled CI workflows. ([#1632](https://github.com/opensearch-project/alerting/pull/1632))
* Update version qualifier to beta1. ([#1816](https://github.com/opensearch-project/alerting/pull/1816))
* Increment version to 3.0.0.0-alpha1 ([#1786](https://github.com/opensearch-project/alerting/pull/1786))
* CVE fix for ktlint ([#1802](https://github.com/opensearch-project/alerting/pull/1802))
* Fix security-enabled test configurations for 3.0-alpha1. ([#1807](https://github.com/opensearch-project/alerting/pull/1807))


### OpenSearch Dashboards Alerting Plugin

* Increment version to 3.0.0.0. ([#1246](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1246))
* Fix CVE. ([#1223](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1223))


### OpenSearch Anomaly Detection

* Fix breaking changes for 3.0.0 release ([#1424](https://github.com/opensearch-project/anomaly-detection/pull/1424))


### OpenSearch Dashboards Anomaly Detection

* Fix(security): Upgrade axios to 1.8.2 to fix SSRF ([#991](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/991))
* Update @babel/runtime to >=7.26.10 ([#993](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/993))


### OpenSearch Asynchronous Search

* Phase out SecurityManager in favor of Java Agent ([#719](https://github.com/opensearch-project/asynchronous-search/pull/719))
* Update 3.0 branch for 3.0.0.0 GA release ([#724](https://github.com/opensearch-project/asynchronous-search/pull/724))


### OpenSearch Common Utils

* Update common-utils shadow plugin repo and bump to 3.0.0.0-alpha1 ([#775](https://github.com/opensearch-project/common-utils/pull/775))
* Change 3.0.0 qualifier from alpha1 to beta1 (([#808](https://github.com/opensearch-project/common-utils/pull/808))


### OpenSearch Cross Cluster Replication

* Update CCR with gradle 8.10.2 and support JDK23 ([#1496](https://github.com/opensearch-project/cross-cluster-replication/pull/1496))


### OpenSearch Dashboards Notifications

* Increment version to 3.0.0.0. ([#347](https://github.com/opensearch-project/dashboards-notifications/pull/347))
* Bump cypress versiont to ^13.6.0. ([#338](https://github.com/opensearch-project/dashboards-notifications/pull/338))


### OpenSearch Dashboards Reporting

* Change dompurify version to 3.0.11 to match OSD ([#516](https://github.com/opensearch-project/dashboards-reporting/pull/516))
* Bump jspdf to 3.0 to fix CVE-2025-26791 ([#529](https://github.com/opensearch-project/dashboards-reporting/pull/529))
* Bump dashboards reporting to version 3.0.0.0-alpha1 ([#536](https://github.com/opensearch-project/dashboards-reporting/pull/536))
* Minor CI updates and workflow fixes ([#548](https://github.com/opensearch-project/dashboards-reporting/pull/548))
* CVE fix for elliptic and update release notes ([#550](https://github.com/opensearch-project/dashboards-reporting/pull/550))
* Bump jspdf to version 3.0.1 ([#555](https://github.com/opensearch-project/dashboards-reporting/pull/555))
* Bump dashboards reporting to version 3.0.0.0-beta1 ([#557](https://github.com/opensearch-project/dashboards-reporting/pull/557))
* CVE fix for babel/helpers and babel/runtime ([#558](https://github.com/opensearch-project/dashboards-reporting/pull/558))
* Remove cypress and babel jest from project dependency list ([#559](https://github.com/opensearch-project/dashboards-reporting/pull/559))


### OpenSearch Dashboards Search Relevance

* Increment version to 3.0.0.0 ([#505](https://github.com/opensearch-project/dashboards-search-relevance/pull/505))
* Increment version to 3.0.0.0-beta1 ([#491](https://github.com/opensearch-project/dashboards-search-relevance/pull/491))
* Increment version to 3.0.0.0-alpha1 ([#486](https://github.com/opensearch-project/dashboards-search-relevance/pull/486))


### OpenSearch Flow Framework

* Fix breaking changes for 3.0.0 release ([#1026](https://github.com/opensearch-project/flow-framework/pull/1026))
* Migrate from BC to BCFIPS libraries ([#1087](https://github.com/opensearch-project/flow-framework/pull/1087))


### OpenSearch Dashboards Flow Framework

* Support 2.17 BWC with latest backend integrations ([#612](https://github.com/opensearch-project/dashboards-flow-framework/pull/612))


### OpenSearch Geospatial

* Set geospatial plugin 3.0.0 baseline JDK version to JDK-21 ([#695](https://github.com/opensearch-project/geospatial/pull/695))
* Bump gradle 8.10.2 / JDK 23 / 3.0.0.0-alpha1 support on geospatial ([#723](https://github.com/opensearch-project/geospatial/pull/723))
* Persist necessary license and developer information in maven pom ([#732](https://github.com/opensearch-project/geospatial/pull/732))


### OpenSearch Index Management

* Dependabot: bump com.netflix.nebula.ospackage from 11.10.1 to 11.11.1 ([#1374](https://github.com/opensearch-project/index-management/pull/1374))
* Dependabot: bump commons-beanutils:commons-beanutils ([#1375](https://github.com/opensearch-project/index-management/pull/1375))
* Dependabot: bump io.gitlab.arturbosch.detekt:detekt-gradle-plugin ([#1381](https://github.com/opensearch-project/index-management/pull/1381))
* [Release 3.0.0] Bump Version to 3.0.0-alpha1 and updated shadowPlugin ([#1384](https://github.com/opensearch-project/index-management/pull/1384))
* Update 3.0.0 qualifier from alpha1 to beta1 ([#1398](https://github.com/opensearch-project/index-management/pull/1398))
* Using java-agent gradle plugin to phase off Security Manager in favor of Java-agent ([#1406](https://github.com/opensearch-project/index-management/pull/1406))
* Increment version to 3.0.0-SNAPSHOT ([#1412](https://github.com/opensearch-project/index-management/pull/1412))


### OpenSearch Dashboards Index Management Plugin

* Index Management Dashboards plugin to version 3.0.0 ([#1265](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1265))
* Updated Micromatch new version ([#1273](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1273))
* Updated 3.0.0 qualifier from alpha1 to beta1 ([#1293](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1293))
* Increment version to 3.0.0.0 ([#1303](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1303))


### OpenSearch Job Scheduler

* Remove beta1 qualifier ([#767](https://github.com/opensearch-project/job-scheduler/pull/767) [#768](https://github.com/opensearch-project/job-scheduler/pull/768))
* Increment version to 3.0.0-alpha1 ([#722](https://github.com/opensearch-project/job-scheduler/pull/722))
* Increment version to 3.0.0-beta1 ([#752](https://github.com/opensearch-project/job-scheduler/pull/752))
* Update shadow plugin to `com.gradleup.shadow` ([#722](https://github.com/opensearch-project/job-scheduler/pull/722))
* Enable custom start commands and options to resolve GHA issues ([#702](https://github.com/opensearch-project/job-scheduler/pull/702))
* Fix delete merged branch workflow ([#693](https://github.com/opensearch-project/job-scheduler/pull/693))
* Update `PULL_REQUEST_TEMPLATE` to include an API spec change in the checklist ([#649](https://github.com/opensearch-project/job-scheduler/pull/649))
* Fix checkout action failure ([#650](https://github.com/opensearch-project/job-scheduler/pull/650))
* dependabot: bump com.google.guava:failureaccess from 1.0.2 to 1.0.3 ([#750](https://github.com/opensearch-project/job-scheduler/pull/750))
* dependabot: bump com.google.googlejavaformat:google-java-format ([#753](https://github.com/opensearch-project/job-scheduler/pull/753))
* dependabot: bump com.netflix.nebula.ospackage from 11.11.1 to 11.11.2 ([#754](https://github.com/opensearch-project/job-scheduler/pull/754))


### OpenSearch ML Commons

* Update CB setting to 100 to bypass memory check ([#3627](https://github.com/opensearch-project/ml-commons/pull/3627))
* Use model type to check local or remote model ([#3597](https://github.com/opensearch-project/ml-commons/pull/3597))
* Fixing security integ test ([#3646](https://github.com/opensearch-project/ml-commons/pull/3646))
* Remove forcing log4j version to 2.24.2 ([#3647](https://github.com/opensearch-project/ml-commons/pull/3647))
* Improve test coverage for MLHttpClientFactory.java ([#3644](https://github.com/opensearch-project/ml-commons/pull/3644))
* Improve test coverage for MLEngineClassLoader class ([#3679](https://github.com/opensearch-project/ml-commons/pull/3679))
* Typo: MLTaskDispatcher \_cluster/settings api ([#3694](https://github.com/opensearch-project/ml-commons/pull/3694))
* Add more logs to troubleshoot flaky test ([#3543](https://github.com/opensearch-project/ml-commons/pull/3543))
* Add package for security test ([#3698](https://github.com/opensearch-project/ml-commons/pull/3698))
* Add sdk implementation to the connector search ([#3704](https://github.com/opensearch-project/ml-commons/pull/3704))
* Sdk client implementation for search connector, model group and task ([#3707](https://github.com/opensearch-project/ml-commons/pull/3707))
* Add Feature Flag for MCP connectors Feature ([(#3738](https://github.com/opensearch-project/ml-commons/pull/3738))
* Support phasing off SecurityManager usage in favor of Java Agent ([#3729](https://github.com/opensearch-project/ml-commons/pull/3729))
* Add java-agent gradle plugin ([#3727](https://github.com/opensearch-project/ml-commons/pull/3727))


### OpenSearch Dashboards ML Commons

* Bump version to 3.0.0.0-alpha1 ([#400](https://github.com/opensearch-project/ml-commons-dashboards/pull/400))
* Bump version to 3.0.0.0-beta1 ([#409](https://github.com/opensearch-project/ml-commons-dashboards/pull/409))
* Bump version to 3.0.0.0 ([#419](https://github.com/opensearch-project/ml-commons-dashboards/pull/419))


### OpenSearch Notifications

* Increment version to 3.0.0-SNAPSHOT ([#1023](https://github.com/opensearch-project/notifications/pull/1023))
* Remove beta1 qualifier ([#1028](https://github.com/opensearch-project/notifications/pull/1028))
* Use java-agent Gradle plugin to support phasing off SecurityManager usage in favor of Java Agent ([#1032](https://github.com/opensearch-project/notifications/pull/1032))
* [Release 3.0] Add alpha1 qualifier. ([#1002](https://github.com/opensearch-project/notifications/pull/1002))
* Get bwc version dynamically ([#987](https://github.com/opensearch-project/notifications/pull/987))
* bump logback to 1.5.16 ([#1003](https://github.com/opensearch-project/notifications/pull/1003))
* Fix security-enabled test workflow. ([#1007](https://github.com/opensearch-project/notifications/pull/1007))
* [Release 3.0] Update version qualifier to beta1. ([#1011](https://github.com/opensearch-project/notifications/pull/1011))


### OpenSearch Observability

* [Doc] Update the integraiton SOP to reference to dashbaords observability only ([#2412](https://github.com/opensearch-project/dashboards-observability/pull/2412))
* Adding husky .only check hook to test files ([#2400](https://github.com/opensearch-project/dashboards-observability/pull/2400))
* Remove cypress to make it refer to the version used in OpenSearch Dashboard to fix build failure ([#2405](https://github.com/opensearch-project/dashboards-observability/pull/2405))
* Fix CVE issue for dependency prismjs ([#2404](https://github.com/opensearch-project/dashboards-observability/pull/2404))
* Bump dashboards observability to version 3.0.0.0-beta1 ([#2401](https://github.com/opensearch-project/dashboards-observability/pull/2401))
* Update README.md for unblocking PRs to be merged ([#2394](https://github.com/opensearch-project/dashboards-observability/pull/2394))
* Bump dep serialize-javascript version to 6.0.2 and @babel/runtime to 7.26.10 ([#2389](https://github.com/opensearch-project/dashboards-observability/pull/2389))
* Minor CI updates and workflow fixes ([#2388](https://github.com/opensearch-project/dashboards-observability/pull/2388))
* TraceView - Optimization of queries ([#2349](https://github.com/opensearch-project/dashboards-observability/pull/2349))
* [Integration] Remove maxFilesPerTrigger from all the integrations queries ([#2354](https://github.com/opensearch-project/dashboards-observability/pull/2354))
* Bump dashboards observability to version 3.0.0.0-alpha1 ([#2364](https://github.com/opensearch-project/dashboards-observability/pull/2364))
* ServiceMap Query Optimizations ([#2367](https://github.com/opensearch-project/dashboards-observability/pull/2367))
* Increase dashboards timeout & store logs on failure ([#2371](https://github.com/opensearch-project/dashboards-observability/pull/2371))
* Clear ADMINS.md. ([#2363](https://github.com/opensearch-project/dashboards-observability/pull/2363))


### OpenSearch Observability

* Bump version 3.0.0-alpha1-SNAPSHOT ([#1904](https://github.com/opensearch-project/observability/pull/1904))
* Bump jdk to 21 for maven snapshot build ([#1909](https://github.com/opensearch-project/observability/pull/1909))
* Bump version 3.0.0-beta1-SNAPSHOT ([#1914](https://github.com/opensearch-project/observability/pull/1914))
* [AUTO] Increment version to 3.1.0-SNAPSHOT ([#1922](https://github.com/opensearch-project/observability/pull/1922))


### OpenSearch Learning To Rank Base

* Update for Lucene 10 changes ([#144](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/144))
* Update 3.0.0 qualifier from alpha1 to beta1 ([#154](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/154))
* Support phasing off SecurityManager usage in favor of Java Agent ([#156](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/156))
* Using java-agent gradle plugin to phase off Security Manager in favor of Java-agent ([#157](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/157))
* [AUTO] Increment version to 3.0.0-SNAPSHOT 3.0 branch ([#166](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/166))
* Remove beta1 qualifier ([#169](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/169))
* [Backport 3.0] Address http5client CVE, use core's dependency ([#171](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/171)) ([#172](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/172))


### OpenSearch Performance Analyzer

* Bumps OS to 3.0.0-alpha1 and JDK 21 ([#791](https://github.com/opensearch-project/performance-analyzer/pull/791))
* Bumps plugin version to 3.0.0.0-beta1 in PA ([#794](https://github.com/opensearch-project/performance-analyzer/pull/794))


### OpenSearch Query Insights

* Bump version to 3.0.0-alpha1 & upgrade to gradle 8.10.2 ([#247](https://github.com/opensearch-project/query-insights/pull/247))
* Fix default exporter settings ([#234](https://github.com/opensearch-project/query-insights/pull/234))
* Change local index replica count to 0 ([#257](https://github.com/opensearch-project/query-insights/pull/257))
* Use ClusterStateRequest with index pattern when searching for expired local indi ces ([#262](https://github.com/opensearch-project/query-insights/pull/262))
* Reduce MAX\_TOP\_N\_INDEX\_READ\_SIZE to 50, sort by desc latency ([#281](https://github.com/opensearch-project/query-insights/pull/281))
* Update 3.0.0 qualifier from alpha1 to beta1 ([#290](https://github.com/opensearch-project/query-insights/pull/290))
* Support phasing off SecurityManager usage in favor of Java Agent ([#296](https://github.com/opensearch-project/query-insights/pull/296))
* Using java-agent gradle plugin to phase off Security Manager in favor of Java-ag ent. ([#303](https://github.com/opensearch-project/query-insights/pull/303))
* Integ tests for exporter n reader ([#267](https://github.com/opensearch-project/query-insights/pull/267))
* Remove beta1 qualifier ([#329](https://github.com/opensearch-project/query-insights/pull/329))
* Increment version to 3.1.0-SNAPSHOT ([#325](https://github.com/opensearch-project/query-insights/pull/325))


### OpenSearch Dashboards Query Insights

* Bump to 3.0.0-alpha1 ([#127](https:/github.com/opensearch-project/query-insights-dashboards/pull/127))
* Updated package.json ([#126](https:/github.com/opensearch-project/query-insights-dashboards/pull/126))
* Upgrade actions/cache to v4 ([#130](https:/github.com/opensearch-project/query-insights-dashboards/pull/130))
* Delete package-lock.json ([#133](https:/github.com/opensearch-project/query-insights-dashboards/pull/133))
* Updated-glob-parent-version ([#134](https:/github.com/opensearch-project/query-insights-dashboards/pull/134))
* Update @babel/helpers ([#139](https:/github.com/opensearch-project/query-insights-dashboards/pull/139))
* Update-default-time-range-1h ([#148](https:/github.com/opensearch-project/query-insights-dashboards/pull/148))
* Update 3.0.0 qualifier from alpha1 to beta1 ([#154](https:/github.com/opensearch-project/query-insights-dashboards/pull/154))
* Update babel/runtime version ([#156](https:/github.com/opensearch-project/query-insights-dashboards/pull/156))
* Improved Cypress test that validates the dynamic column ([#168](https:/github.com/opensearch-project/query-insights-dashboards/pull/168))


### OpenSearch Query Workbench

* Remove cypress version to make it uses the version in OpenSearch Dashboards ([#463](https://github.com/opensearch-project/dashboards-query-workbench/pull/463))
* Bump dashboards query workbench to version 3.0.0.0-beta1 ([#462](https://github.com/opensearch-project/dashboards-query-workbench/pull/462))
* Remove download JSON feature ([#460](https://github.com/opensearch-project/dashboards-query-workbench/pull/460))
* Minor CI updates and workflow fixes ([#459](https://github.com/opensearch-project/dashboards-query-workbench/pull/459))
* Update yarn.lock for cross-spawn ([#441](https://github.com/opensearch-project/dashboards-query-workbench/pull/441))
* Bump dashboards query workbench to version 3.0.0.0-alpha1 ([#444](https://github.com/opensearch-project/dashboards-query-workbench/pull/444))
* Update CIs to install job-scheduler plugin ([#453](https://github.com/opensearch-project/dashboards-query-workbench/pull/453))


### OpenSearch Reporting

* Bump version 3.0.0-alpha1-SNAPSHOT ([#1073](https://github.com/opensearch-project/reporting/pull/1073))
* Update gradle version to 8.12.0 for JDK23 support ([#1077](https://github.com/opensearch-project/reporting/pull/1077))
* Bump version 3.0.0-beta1-SNAPSHOT ([#1083](https://github.com/opensearch-project/reporting/pull/1083))
* [AUTO] Increment version to 3.1.0-SNAPSHOT ([#1092](https://github.com/opensearch-project/reporting/pull/1092))


### OpenSearch Security Analytics

* Increment version to 3.1.0-SNAPSHOT ([#1517](https://github.com/opensearch-project/security-analytics/pull/1517))
* Remove beta1 qualifier ([#1519](https://github.com/opensearch-project/security-analytics/pull/1519))
* Using java-agent gradle plugin to phase off Security Manager in favor of Java-agent. ([#1505](https://github.com/opensearch-project/security-analytics/pull/1505))
* Fix build due to phasing off SecurityManager usage in favor of Java Agent ([#1504](https://github.com/opensearch-project/security-analytics/pull/1504))
* [Release 3.0] Add alpha1 qualifier. ([#1490](https://github.com/opensearch-project/security-analytics/pull/1490))
* Updated commons jar with CVE fixes. ([#1481](https://github.com/opensearch-project/security-analytics/pull/1481))
* Update gradle 8.10.2 and support jdk23 ([#1492](https://github.com/opensearch-project/security-analytics/pull/1492))
* Fix security-enabled test workflow for 3.0-alpha1. ([#1494](https://github.com/opensearch-project/security-analytics/pull/1494/))
* Update version qualifier to beta1. ([#1500](https://github.com/opensearch-project/security-analytics/pull/1500))


### OpenSearch Dashboards Security Analytics

* Increment version to 3.0.0.0. ([#1283](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1283))
* Fix CVE. ([#1270](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1270))
* Fix CVE 2025 27789. ([#1276](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1276))
* Fix CVE-2025 27789. ([#1278](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1278))
* Fix integration tests. ([#1280](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1280))


### OpenSearch Dashboards Security Plugin

* Fix alpha bump ([#2190](https://github.com/opensearch-project/security-dashboards-plugin/pull/2190))
* Bump xlm-crypto and elliptic ([#2196](https://github.com/opensearch-project/security-dashboards-plugin/pull/2196))
* Remove typescript dependency ([#2198](https://github.com/opensearch-project/security-dashboards-plugin/pull/2198))
* Bump babel to 7.27.0 ([#2200](https://github.com/opensearch-project/security-dashboards-plugin/pull/2200))
* Fix integration tests by removing sample flight data download ([#2202](https://github.com/opensearch-project/security-dashboards-plugin/pull/2202))
* Bump express to 5.1.0 ([#2232](https://github.com/opensearch-project/security-dashboards-plugin/pull/2232))


### OpenSearch System Templates

* Update gradle 8.10.2 JDK23 and support lucene10 ([#62](https://github.com/opensearch-project/opensearch-system-templates/pull/62))
* Using java-agent gradle plugin to phase off Security Manager in favor of Java-agent. ([#68](https://github.com/opensearch-project/opensearch-system-templates/pull/68))


### OpenSearch k-NN

* Update minimum required CMAKE version in NMSLIB ([#2635](https://github.com/opensearch-project/k-NN/pull/2635))
* Revert CMake version bump, instead add CMake policy version flag to build task to support modern CMake builds ([#2645](https://github.com/opensearch-project/k-NN/pull/2645/files))
* Update package name to fix compilation issue ([#2513](https://github.com/opensearch-project/k-NN/pull/2513))
* Update gradle to 8.13 to fix command exec on java 21 ([#2571](https://github.com/opensearch-project/k-NN/pull/2571))
* Add fix for nmslib pragma on arm ([#2574](https://github.com/opensearch-project/k-NN/pull/2574))
* Removes Array based vector serialization ([#2587](https://github.com/opensearch-project/k-NN/pull/2587))
* Enabled indices.breaker.total.use\_real\_memory setting via build.gradle for integTest Cluster to catch heap CB in local ITs and github CI actions ([#2395](https://github.com/opensearch-project/k-NN/pull/2395/))
* Fixing Lucene912Codec Issue with BWC for Lucene 10.0.1 upgrade ([#2429](https://github.com/opensearch-project/k-NN/pull/2429))
* Enabled idempotency of local builds when using `./gradlew clean` and nest `jni/release` directory under `jni/build` for easier cleanup ([#2516](https://github.com/opensearch-project/k-NN/pull/2516))


### OpenSearch SQL

* Build: Centralise dependencies version - Pt1 ([#3294](https://github.com/opensearch-project/sql/pull/3294))
* Remove dependency from async-query-core to datasources ([#2891](https://github.com/opensearch-project/sql/pull/2891))
* CVE-2024-57699 High: Fix json-smart vulnerability ([#3484](https://github.com/opensearch-project/sql/pull/3484))
* Adding new maintainer @qianheng-aws ([#3509](https://github.com/opensearch-project/sql/pull/3509))
* Bump SQL main to version 3.0.0.0-beta1 ([#3489](https://github.com/opensearch-project/sql/pull/3489))
* Merge feature/calcite-engine to main ([#3448](https://github.com/opensearch-project/sql/pull/3448))
* Merge main for OpenSearch 3.0 release ([#3434](https://github.com/opensearch-project/sql/pull/3434))
* Fix build due to phasing off SecurityManager usage in favor of Java Agent ([#3539](https://github.com/opensearch-project/sql/pull/3539))
* Using java-agent gradle plugin to phase off Security Manager in favor of Java-agent ([#3551](https://github.com/opensearch-project/sql/pull/3551))


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
* Bump org.junit.jupiter:junit-jupiter from 5.11.4 to 5.12.2 ([#5127](https://github.com/opensearch-project/security/pull/5127)) ([#5269](https://github.com/opensearch-project/security/pull/5269))
* Bump Gradle to 8.13 ([#5148](https://github.com/opensearch-project/security/pull/5148))
* Bump Spring version to fix CVE-2024-38827 ([#5173](https://github.com/opensearch-project/security/pull/5173))
* Bump com.google.guava:guava from 33.4.0-jre to 33.4.6-jre ([#5205](https://github.com/opensearch-project/security/pull/5205)) ([#5228](https://github.com/opensearch-project/security/pull/5228))
* Bump ch.qos.logback:logback-classic from 1.5.17 to 1.5.18 ([#5204](https://github.com/opensearch-project/security/pull/5204))
* Bump spring\_version from 6.2.4 to 6.2.5 ([#5203](https://github.com/opensearch-project/security/pull/5203))
* Bump bouncycastle\_version from 1.78 to 1.80 ([#5202](https://github.com/opensearch-project/security/pull/5202))
* remove java version check for reflection args in build.gradle ([#5218](https://github.com/opensearch-project/security/pull/5218))
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
* Fix compilation issue after Secure gRPC PR (#17796) merged into core ([#5263](https://github.com/opensearch-project/security/pull/5263))
* Bump commons-io:commons-io from 2.18.0 to 2.19.0 ([#5267](https://github.com/opensearch-project/security/pull/5267))
* Bump org.apache.commons:commons-text from 1.13.0 to 1.13.1 ([#5266](https://github.com/opensearch-project/security/pull/5266))
* Bump org.junit.jupiter:junit-jupiter-api from 5.12.1 to 5.12.2 ([#5268](https://github.com/opensearch-project/security/pull/5268))
* Bump com.google.guava:failureaccess from 1.0.2 to 1.0.3 ([#5265](https://github.com/opensearch-project/security/pull/5265))


### OpenSearch Skills

* Remove `space_type` in integ test to adapt to the change of k-NN plugin ([#535](https://github.com/opensearch-project/skills/pull/535))
* Fix jar hell for sql jar ([#545](https://github.com/opensearch-project/skills/pull/545))
* Add attributes to tools to adapt the upstream changes ([#549](https://github.com/opensearch-project/skills/pull/549))
* Support phasing off SecurityManager usage in favor of Java Agent ([#553](https://github.com/opensearch-project/skills/pull/553))



## REFACTORING


### OpenSearch Dashboards Alerting Plugin

* Only use latest active alert for alert summary context ([#1220](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1220))


### OpenSearch Dashboards Flow Framework

* Refactor quick configure components, improve processor error handling ([#604](https://github.com/opensearch-project/dashboards-flow-framework/pull/604))
* Hide search query section when version is less than 2.19 ([#605](https://github.com/opensearch-project/dashboards-flow-framework/pull/605))


### OpenSearch Neural Search

* Encapsulate KNNQueryBuilder creation within NeuralKNNQueryBuilder ([#1183](https://github.com/opensearch-project/neural-search/pull/1183))


### OpenSearch Remote Metadata Sdk

* Update o.o.client imports to o.o.transport.client ([#73](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/73))


### OpenSearch Dashboards Security Analytics

* Temporarily removed visualizations for 3.0-alpha1. ([#1272](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1272))


### OpenSearch k-NN

* Switch derived source from field attributes to segment attribute ([#2606](https://github.com/opensearch-project/k-NN/pull/2606))
* Migrate derived source from filter to mask ([#2612](https://github.com/opensearch-project/k-NN/pull/2612))
* Consolidate MethodFieldMapper and LuceneFieldMapper into EngineFieldMapper ([#2646](https://github.com/opensearch-project/k-NN/pull/2646))
* Small Refactor Post Lucene 10.0.1 upgrade ([#2541](https://github.com/opensearch-project/k-NN/pull/2541))
* Refactor codec to leverage backwards\_codecs ([#2546](https://github.com/opensearch-project/k-NN/pull/2546))
* Blocking Index Creation using NMSLIB ([#2573](https://github.com/opensearch-project/k-NN/pull/2573))
* Improve Streaming Compatibility Issue for MethodComponetContext and Remove OpenDistro URL ([#2575](https://github.com/opensearch-project/k-NN/pull/2575))
* 3.0.0 Breaking Changes For KNN ([#2564](https://github.com/opensearch-project/k-NN/pull/2564))
