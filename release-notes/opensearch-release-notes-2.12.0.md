<h1>OpenSearch and OpenSearch Dashboards 2.12.0 Release Notes</h1>
<h2>RELEASE HIGHLIGHTS</h2>
<ul>
OpenSearch 2.12.0 includes a number of features designed to increase performance for search and analytics applications as well as user experience enhancements and several new and enhanced machine learning tools. Experimental functionality includes the OpenSearch Assistant Toolkit for building interactive user experiences and new cross-cluster monitors. OpenSearch upgrades to Apache Lucene 9.9.2 with this release. 
</ul>

<h2>NEW FEATURES</h2>
<ul>
<li>Integration with Apache Spark lets you analyze all of your operational data in a single place using OpenSearch in combination with Apache Spark. </li>
<li>Conversational search is generally available, providing comprehensive functionality to build conversational experiences using OpenSearch’s lexical, vector, and hybrid search features.</li>
<li>New default processors for Amazon Bedrock text embedding connectors can reduce the effort required to build AI connectors.</li>
<li>You can now represent long documents as multiple vectors in a nested field with built-in chunking, eliminating the need to build custom processing logic in order to query documents represented as vector chunks.</li>
<li>Concurrent segment search is now generally available, giving you the option to query index segments in parallel at the shard level. This can deliver improved latency for many types of search queries.</li>
<li>Date histogram aggregations without sub-aggregations can now be transformed into and executed as range filters, offering a significant boost to search performance.</li>
<li>Multi-terms aggregations are now significantly faster for high-cardinality search terms, which offers improved performance for many prefix and wildcard queries.</li>
<li>A new match-only text field type, a variant of the text field, can help reduce storage costs while maintaining term and multi-term query performance.</li>
<li>The keyword, numeric, and IP field types can now be searched with doc_values queries. This type of query can decrease storage requirements for rarely accessed fields.</li>
<li>A new top N queries feature lets you track high-latency queries with an API.</li>
<li>Updates to the Discover tool in OpenSearch Dashboards include improvements to density, column order, sorting controls, and more. Users can now choose between the previously implemented Discover experience and the updated experience.</li>
</ul>

<h2>EXPERIMENTAL FEATURES</h2>
<ul>
<li>OpenSearch 2.12.0 includes the following experimental features. Experimental features are disabled by default. For instructions on how to enable them, refer to the documentation for the feature.</li>
<li>The OpenSearch Assistant Toolkit helps developers build generative AI experiences inside of OpenSearch Dashboards. With integrated natural language processing and context-aware features, developers can use this toolkit to apply generative AI to create interactive user experiences and extract insights from OpenSearch data.</li>
<li>A new agent framework added to ML Commons uses remote large language learning models (LLMs) for step-by-step problem-solving and can coordinate machine learning tools using LLMs. The framework includes a flow agent and a conversational agent in this release.</li>
<li>Users can now query multiple clusters with cross-cluster monitors through the Alerting plugin.</li>
<li>A new workflow engine lets you automate configurations for ML Commons resources, allowing you to set up machine learning resources to support AI use cases without the need to manually create resources or write custom scripts.</li>
</ul>

<h2>DEPRECATION NOTICE</h2>

<h3>CentOS7</h3>
<ul>
Please note that OpenSearch will deprecate support for CentOS Linux 7 as a continuous integration build image and supported operating system in an upcoming release, as CentOS Linux 7 will reach end-of-life on June 30, 2024 (see <a href="https://blog.centos.org/2023/04/end-dates-are-coming-for-centos-stream-8-and-centos-linux-7/">#notice</a>). To view OpenSearch's compatible operating systems, visit <a href="https://opensearch.org/docs/latest/install-and-configure/install-opensearch/index/#operating-system-compatibility">#operating-system-compatibility</a>.

</ul>

<h2>RELEASE DETAILS</h2>
<ul>
<li>[OpenSearch and OpenSearch Dashboards 2.12.0](https://opensearch.org/versions/opensearch-2-12-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.
</li>
<li>
OpenSearch <a href="https://github.com/opensearch-project/OpenSearch/blob/2.12/release-notes/opensearch.release-notes-2.12.0.md">Release Notes</a>.

OpenSearch Dashboards <a href="https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.12/release-notes/opensearch-dashboards.release-notes-2.12.0.md">Release Notes</a>.

</li>
</ul>

<h2>FEATURES</h2>

<h3>Opensearch Custom Codecs</h3>

<ul>
<li>Accessors for custom compression modes (<a href="https://github.com/opensearch-project/custom-codecs/pull/90">#90</a>)</li>
<li>Lucene 9.9.2 Upgrade (<a href="https://github.com/opensearch-project/OpenSearch/pull/12069">#12069</a>)</li>
</ul>

<h3>Opensearch Flow Framework</h3>

<ul>
<li>Initial release of Flow Framework</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Add denylist ip config for datasource endpoint (<a href="https://github.com/opensearch-project/geospatial/pull/573">#573</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Add cross encoder support (#1739)</li>
<li>Enable conversation memory feature flags (#2095)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Add rerank processor interface and ml-commons reranker (<a href="https://github.com/opensearch-project/neural-search/pull/494">#494</a>)</li>
</ul>

<h3>Opensearch Observability</h3>

<ul>
<li>Add metric type (<a href="https://github.com/opensearch-project/observability/pull/1775">#1775</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Integrate threat intel feeds (<a href="https://github.com/opensearch-project/security-analytics/pull/669">#669</a>)</li>
</ul>

<h3>Opensearch k-NN</h3>

<ul>
<li>Add parent join support for lucene knn <a href="https://github.com/opensearch-project/k-NN/pull/1182">#1182</a></li>
<li>Add parent join support for faiss hnsw <a href="https://github.com/opensearch-project/k-NN/pull/1398">#1398</a></li>
</ul>

<h3>Skills</h3>

<ul>
<li>Initial release of Skills</li>
</ul>

<h3>Dashboards Assistant</h3>

<ul>
<li><h3>Feature</h3>
</li>
</ul>
<ul>
<li>Set verbose to false (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/131">#131</a>)</li>
</ul>

<h3>Dashboards Observability</h3>

<ul>
<li>Add redirect with error message if integrations template not found (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1418">#1418</a>)</li>
<li>Enable data grid in Chatbot (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1383">#1383</a>)</li>
<li>Support Query assist (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1369">#1369</a>)</li>
<li>Allow patch on allowedRoles (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1144">#1144</a>)</li>
<li>Enable ppl visualization in Chatbot (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1374">#1374</a>)</li>
<li>Added HAProxy Integration (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1277">#1277</a>)</li>
</ul>

<h3>Opensearch Alerting Dashboards Plugin</h3>

<ul>
<li>Implemented UI to support cross-cluster monitors configuration - experimental. (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/871">#871</a>)</li>
</ul>

<h3>Opensearch Dashboards Reporting</h3>

<ul>
<li>Feature Use Timezone in Reports (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/238">#238</a>)</li>
</ul>

<h3>Opensearch Dashboards Search Relevance</h3>

<ul>
<li>Add Ability to Select a Search Pipeline in Comparison Tool (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/352">#352</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/362">#362</a>)</li>
</ul>

<h3>Opensearch Query Workbench</h3>

<ul>
<li>Add materlized views, manual refresh option (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/159">#159</a>)</li>
</ul>
<ul>
<li>Added changes for making tree view persistent (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/153">#153</a>)</li>
<li>Support dark mode and session for sql (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/165">#165</a>)</li>
<li>Update ppl editor readonly property (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/248">#248</a>)</li>
<li>Support for multiple datasource sessions (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/251">#251</a>)</li>
</ul>

<h3>Opensearch Security Analytics Dashboards</h3>

<ul>
<li>Cache date time filter in local storage (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/848">#848</a>)</li>
<li>Show aliases in data source options for detector and correlation rule creation (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/864">#864</a>)</li>
<li>Correlations page improvements (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/855">#855</a>)</li>
</ul>

<h2>ENHANCEMENTS</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Optimize doc-level monitor execution workflow for datastreams (<a href="https://github.com/opensearch-project/alerting/pull/1302">#1302</a>)</li>
<li>Inject namedWriteableRegistry during ser/deser of SearchMonitorAction (<a href="https://github.com/opensearch-project/alerting/pull/1382">#1382</a>)</li>
<li>Bulk index findings and sequentially invoke auto-correlations (<a href="https://github.com/opensearch-project/alerting/pull/1355">#1355</a>)</li>
<li>Implemented cross-cluster monitor support (<a href="https://github.com/opensearch-project/alerting/pull/1404">#1404</a>)</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Add an AD transport client (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1111">#1111</a>)</li>
<li>Add profile transport action to AD client (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1123">#1123</a>)</li>
<li>Refactor client's getDetectorProfile to use GetAnomalyDetectorTransportAction (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1124">#1124</a>)</li>
<li>Add ser/deser to get AD transport action request (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1150">#1150</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>add 'fields' parameter in doc level query object. (<a href="https://github.com/opensearch-project/common-utils/pull/546">#546</a>)</li>
<li>add fields param in toxcontent() for doc level query (<a href="https://github.com/opensearch-project/common-utils/pull/549">#549</a>)</li>
<li>Add User.isAdminDn to User class (<a href="https://github.com/opensearch-project/common-utils/pull/547">#547</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Implemented filtering on the ISM eplain API (<a href="https://github.com/opensearch-project/index-management/pull/1067">#1067</a>)</li>
<li>Add more error notification at fail points (<a href="https://github.com/opensearch-project/index-management/pull/1000">#1000</a>)</li>
<li>[Feature] Support Transform as an ISM action (<a href="https://github.com/opensearch-project/index-management/pull/760">#760</a>)</li>
<li>Set the rollover action to idempotent (<a href="https://github.com/opensearch-project/index-management/pull/986">#986</a>)</li>
<li>Support switch aliases in shrink action. (<a href="https://github.com/opensearch-project/index-management/pull/987">#987</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Add register and deploy api in client (#1502)</li>
<li>Added create connector API for MLClient (#1506)</li>
<li>Added register model group API for MLClient (#1519)</li>
<li>Expose execute api for MLClient (#1541)</li>
<li>Add prefix to show the error is from remote service (#1515)</li>
<li>Fine tune predict API: read model from index directly (#1559)</li>
<li>Removed empty host check, inherently within httpHost object generation (#1599)</li>
<li>Cluster restart model auto redeploy (#1627)</li>
<li>Add new data fields in the memory layer and update tests (#1753)</li>
<li>Check if model id is null when undeploy (#2015)</li>
<li>Adds inputs validation for create memory (#2040)</li>
<li>Make response_field customizable in MLModelTool (#2043)</li>
<li>Add memory id and interation id for non-verbose (#2005)</li>
<li>Issue #1965: Remove logging of sensitive chat history (#2012)</li>
<li>Update memory if tool output needs to be included in response (#2018)</li>
<li>Disable dynamic mapping for config index (#2027)</li>
<li>Move allow model setting from rest to transport (#1977)</li>
<li>Fine tune connector process function (#1963)</li>
<li>Change model auto redeploy enabled to true (#1809)</li>
<li>Add auto expand replica settings to memories (#1824)</li>
<li>Add interaction id into execute response (#1825)</li>
<li>Add more methods to client (#1782)</li>
<li>Support charset input params and change default charset as utf8 (#1828)</li>
<li>Fine tune log message based on error type (#1842)</li>
<li>Stash thread context before running forward action (#1906)</li>
<li>Refine the error message on cluster status not ready scenario (#1931)</li>
<li>Add Request-Source header (#1892)</li>
<li>Add process function for bedrock (#1554)</li>
<li>send agent execution response after saving memory (#2066)</li>
<li>add conversational flow agent (#2069)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Improve security plugin enabling check (<a href="https://github.com/opensearch-project/notifications/pull/792">#792</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Add separate metric for cluster manager service events and metrics <a href="https://github.com/opensearch-project/performance-analyzer/pull/579">#579</a></li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Add additional sendRequestDecorate cases (<a href="https://github.com/opensearch-project/security/pull/4007">#4007</a>)</li>
<li>[BUG-2556] Add new DLS filtering test (<a href="https://github.com/opensearch-project/security/pull/4001">#4001</a>)</li>
<li>[Enhancement-3191] <code>transport_enabled</code> setting on an auth domain and authorizer may be unnecessary after transport client removal  (<a href="https://github.com/opensearch-project/security/pull/3966">#3966</a>)</li>
<li>Update roles.yml with new API for experimental alerting plugin feature <a href="https://github.com/opensearch-project/security/pull/4027">#4027</a> (<a href="https://github.com/opensearch-project/security/pull/4029">#4029</a>)</li>
<li>Admin role for Query insights plugin (<a href="https://github.com/opensearch-project/security/pull/4022">#4022</a>)</li>
<li>Validate 409s occur when multiple config updates happen simultaneously (<a href="https://github.com/opensearch-project/security/pull/3962">#3962</a>)</li>
<li>Protect config object from concurrent modification issues (<a href="https://github.com/opensearch-project/security/pull/3956">#3956</a>)</li>
<li>Add test coverage for ComplianceConfig (<a href="https://github.com/opensearch-project/security/pull/3957">#3957</a>)</li>
<li>Update security analytics roles to include custom log type cluster permissions (<a href="https://github.com/opensearch-project/security/pull/3954">#3954</a>)</li>
<li>Add logging for test LdapServer actions (<a href="https://github.com/opensearch-project/security/pull/3942">#3942</a>)</li>
<li>HeapBasedRateTracker uses time provider to allow simluating of time in unit tests (<a href="https://github.com/opensearch-project/security/pull/3941">#3941</a>)</li>
<li>Add additional logging around <code>testShouldSearchAll</code> tests (<a href="https://github.com/opensearch-project/security/pull/3943">#3943</a>)</li>
<li>Add permission for get workflow step (<a href="https://github.com/opensearch-project/security/pull/3940">#3940</a>)</li>
<li>Add additional ignore_headers audit configuration setting (<a href="https://github.com/opensearch-project/security/pull/3926">#3926</a>)</li>
<li>Update to Gradle 8.5 (<a href="https://github.com/opensearch-project/security/pull/3919">#3919</a>) (<a href="https://github.com/opensearch-project/security/pull/3923">#3923</a>)</li>
<li>Refactor SSL handler retrieval to use HttpChannel / TranportChannel APIs instead of typecasting (<a href="https://github.com/opensearch-project/security/pull/3917">#3917</a>) (<a href="https://github.com/opensearch-project/security/pull/3922">#3922</a>)</li>
<li>Improve messaging on how to set initial admin password (<a href="https://github.com/opensearch-project/security/pull/3918">#3918</a>)</li>
<li>Re-enable disabled PIT integration tests (<a href="https://github.com/opensearch-project/security/pull/3914">#3914</a>)</li>
<li>Switched to more reliable OpenSearch Lucene snapshot location (<a href="https://github.com/opensearch-project/security/pull/3913">#3913</a>)</li>
<li>Add deprecation check for <code>jwt_header</code> setting (<a href="https://github.com/opensearch-project/security/pull/3896">#3896</a>)</li>
<li>Add render search template as a cluster permission (<a href="https://github.com/opensearch-project/security/pull/3689">#3689</a>) (<a href="https://github.com/opensearch-project/security/pull/3872">#3872</a>)</li>
<li>Add flow framework system indices and roles (<a href="https://github.com/opensearch-project/security/pull/3851">#3851</a>) (<a href="https://github.com/opensearch-project/security/pull/3880">#3880</a>)</li>
<li>Search operation test flakiness fix (<a href="https://github.com/opensearch-project/security/pull/3862">#3862</a>)</li>
<li>Extracts demo configuration setup into a java tool, adds support for Bundled JDK for this tool and updates DEVELOPER_GUIDE.md (<a href="https://github.com/opensearch-project/security/pull/3845">#3845</a>)</li>
<li>SAML permissions changes in DynamicConfigModelV7 (<a href="https://github.com/opensearch-project/security/pull/3853">#3853</a>)</li>
<li>Add do not fail on forbidden test cases around the stats API (<a href="https://github.com/opensearch-project/security/pull/3825">#3825</a>) (<a href="https://github.com/opensearch-project/security/pull/3828">#3828</a>)</li>
<li>Switch jwt library from org.apache.cxf.rs.security.jose to com.nimbusds.jose.jwk (<a href="https://github.com/opensearch-project/security/pull/3595">#3595</a>)</li>
</ul>

<h3>Opensearch k-NN</h3>

<ul>
<li>Increase Lucene max dimension limit to 16,000 <a href="https://github.com/opensearch-project/k-NN/pull/1346">#1346</a></li>
<li>Tuned default values for ef_search and ef_construction for better indexing and search performance for vector search <a href="https://github.com/opensearch-project/k-NN/pull/1353">#1353</a></li>
<li>Enabled Filtering on Nested Vector fields with top level filters <a href="https://github.com/opensearch-project/k-NN/pull/1372">#1372</a></li>
<li>Throw proper exception to invalid k-NN query <a href="https://github.com/opensearch-project/k-NN/pull/1380">#1380</a></li>
</ul>

<h3>SQL</h3>

<ul>
<li>add InteractiveSession and SessionManager by @penghuo in https://github.com/opensearch-project/sql/pull/2290</li>
<li>Add Statement by @penghuo in https://github.com/opensearch-project/sql/pull/2294</li>
<li>Add sessionId parameters for create async query API by @penghuo in https://github.com/opensearch-project/sql/pull/2312</li>
<li>Implement patch API for datasources by @derek-ho in https://github.com/opensearch-project/sql/pull/2273</li>
<li>Integration with REPL Spark job by @penghuo in https://github.com/opensearch-project/sql/pull/2327</li>
<li>Add missing tags and MV support by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2336</li>
<li>Bug Fix, support cancel query in running state by @penghuo in https://github.com/opensearch-project/sql/pull/2351</li>
<li>Add Session limitation by @penghuo in https://github.com/opensearch-project/sql/pull/2354</li>
<li>Handle Describe,Refresh and Show Queries Properly by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2357</li>
<li>Add where clause support in create statement by @dai-chen in https://github.com/opensearch-project/sql/pull/2366</li>
<li>Add Flint Index Purging Logic by @kaituo in https://github.com/opensearch-project/sql/pull/2372</li>
<li>add concurrent limit on datasource and sessions by @penghuo in https://github.com/opensearch-project/sql/pull/2390</li>
<li>Redefine Drop Index as logical delete by @penghuo in https://github.com/opensearch-project/sql/pull/2386</li>
<li>Added session, statement, emrjob metrics to sql stats api by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2398</li>
<li>Add more metrics and handle emr exception message by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2422</li>
<li>Add cluster name in spark submit params by @noCharger in https://github.com/opensearch-project/sql/pull/2467</li>
<li>Add setting plugins.query.executionengine.async_query.enabled by @penghuo in https://github.com/opensearch-project/sql/pull/2510</li>
</ul>

<h3>Dashboards Observability</h3>

<ul>
<li>Updating app analytics jest and cypress tests (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1417">#1417</a>)</li>
<li>Hide dot indices for query assist (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1413">#1413</a>)</li>
<li>Optimize searches for integration data (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1406">#1406</a>)</li>
<li>Add Index-based adaptor for integrations (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1399">#1399</a>)</li>
<li>Optimize images in integrations repository (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1395">#1395</a>)</li>
<li>JSON Catalog Reader for Integrations (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1392">#1392</a>)</li>
<li>Improve lint workflow to avoid fast fail (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1384">#1384</a>)</li>
<li>Stop filtering stats by for data grid (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1385">#1385</a>)</li>
<li>Update notebooks snapshots and cypress (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1375">#1375</a>)</li>
<li>Revise and edit PPL in-product documentation (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1368">#1368</a>)</li>
<li>Refactor data sources cypress tests (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1351">#1351</a>)</li>
<li>Separate linting rules for cypress (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1348">#1348</a>)</li>
<li>Remove manual refresh for S3 integrations (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1227">#1227</a>)</li>
<li>Notebook jest updates (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1346">#1346</a>)</li>
<li>Sync dependencies with latest versions (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1345">#1345</a>)</li>
<li>Removes Zeppelin code and docs (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1340">#1340</a>)</li>
<li>Metrics explore updated with PromQL (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1303">#1303</a>)</li>
<li>Updated naming convention for HAProxy Integration (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1284">#1284</a>)</li>
<li>Style changes for rendering fullscreen data grid (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1279">#1279</a>)</li>
</ul>

<h3>Opensearch Dashboards Search Relevance</h3>

<ul>
<li>Utilize EuiEmptyPrompt to represent empty state (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/320">#320</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/333">#333</a>)</li>
<li>Update results to display non-source fields in search comparison tool (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/340">#340</a> )(<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/354">#354</a>)</li>
</ul>

<h3>Opensearch Index Management Dashboards Plugin</h3>

<ul>
<li>sort by managed policy feature (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/950">#950</a>)</li>
<li>Update background color in &quot;state&quot; block (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/903">#903</a>)</li>
<li>Rename indices to indexes (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/926">#926</a>)</li>
<li>adding cancel button to change policy (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/919">#919</a>)</li>
</ul>

<h3>Opensearch Security Dashboards Plugin</h3>

<ul>
<li>Run SAML Multi Auth integration tests in Cypress (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1729">#1729</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1749">#1749</a>)</li>
<li>Add step to install dependencies prior to building (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1743">#1743</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1747">#1747</a>)</li>
<li>Add indices:data/read/search/template/render to cluster permissions dropdown (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1725">#1725</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1732">#1732</a>)</li>
<li>Run Security dashboards plugin from binary  (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1734">#1734</a>)</li>
<li>Run <code>cypress-tests</code> and <code>cypress-tests-tenancy-disabled</code> on Chrome (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1728">#1728</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1733">#1733</a>)</li>
<li>Cookie compression and splitting for JWT (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1651">#1651</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1723">#1723</a>)</li>
<li>Adds system index permission as allowed action under static drop down list (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1720">#1720</a>)</li>
<li>Handle other permission group types (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1715">#1715</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1718">#1718</a>)</li>
<li>Implement nextUrl for OpenID Authentication (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1563">#1563</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1701">#1701</a>)</li>
<li>Cypress13 testing frame work for OIDC and SAML (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1691">#1691</a>)</li>
<li>Added client certificate options to support mutual TLS for OpenID endpoint (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1650">#1650</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1683">#1683</a>)</li>
<li>Adds openid parameters (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1637">#1637</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1677">#1677</a>)</li>
<li>Show controls as read only based on tenant permissions (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1472">#1472</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1670">#1670</a>)</li>
<li>Add search pipeline action permissions (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1661">#1661</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1663">#1663</a>)</li>
<li>Add permissions for async query and patch datasource API (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1626">#1626</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1630">#1630</a>)</li>
</ul>

<h2>BUG FIXES</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Don't attempt to parse workflow if it doesn't exist (<a href="https://github.com/opensearch-project/alerting/pull/1346">#1346</a>)</li>
<li>Set docData to empty string if actual is null (<a href="https://github.com/opensearch-project/alerting/pull/1325">#1325</a>)</li>
</ul>

<h3>Opensearch Custom Codecs</h3>

<ul>
<li>GA updates and minor BWC test cleanups (<a href="https://github.com/opensearch-project/custom-codecs/pull/105">#105</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>GET SM policies return empty list when ism config index does not exist (<a href="https://github.com/opensearch-project/index-management/pull/1072">#1072</a>)</li>
<li>Added minimum timeout for transforms search of 10 minutes (<a href="https://github.com/opensearch-project/index-management/pull/1033">#1033</a>)</li>
<li>Interval schedule should take start time from the request, should not… (<a href="https://github.com/opensearch-project/index-management/pull/1040">#1040</a>)</li>
<li>Added minimum for search.cancel_after_time_interval setting for rollups (<a href="https://github.com/opensearch-project/index-management/pull/1026">#1026</a>)</li>
<li>Interval schedule should take start time from the request, should not set it to the current time of request execution. (<a href="https://github.com/opensearch-project/index-management/pull/1036">#1036</a>)</li>
<li>added type check for pipeline aggregator types in Transform initialization (<a href="https://github.com/opensearch-project/index-management/pull/1014">#1014</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Fix missing lombok version compilation failure issue (#1278)</li>
<li>Fix update connector API (#1484)</li>
<li>Fixes bugs in the Cohere Blueprint (#1505)</li>
<li>Fix register client API (#1561)</li>
<li>Fixing MachineLearningNodeClient create connector, deploy model, register model group actions (#1584)</li>
<li>Fix model/connector update API to address security concern (#1595)</li>
<li>Fixing class casting exception for MachineLearningNodeClient GetMLTask API (#1618)</li>
<li>Fix for controller error stack trace and tokenbucket (#1985)</li>
<li>Fix internal connector (#1992)</li>
<li>Fix argument pass (#1993)</li>
<li>Fix error code when failed to delete model (#2037)</li>
<li>Fix edge case for validate json method (#2045)</li>
<li>Fix long pending issue when deleting model (#2046)</li>
<li>Add escape method for process function (#2055)</li>
<li>Fix bug in delete empty memory (#1966)</li>
<li>Fix dup last trace (#1975)</li>
<li>Add a version filter to enable bwc in 2.12 (#1944)</li>
<li>Fix error message (#1976)</li>
<li>Fix string.format wrong parameter position (#1960)</li>
<li>Fix null taskId causing model undeploy issue (#1945)</li>
<li>Fix updating plugins.ml_commons.jvm_heap_memory_threshold takes no effect (#1946)</li>
<li>Fix compilation when backport (#1798)</li>
<li>Fix duplicate node if node has both data and ml role (#1830)</li>
<li>Fix partially response issue in profile API result (#1775)</li>
<li>Fix: RestStatus 500 returned ml validation (#1811)</li>
<li>Fix the hardcode password in IT (#1856)</li>
<li>Fix model not deploy issue under intensive prediction tasks (#1930)</li>
<li>Fix bug - not found agent index (#1867)</li>
<li>Issue #1787: Fixing connector endpoint returns index not found (#1885)</li>
<li>Issue #1878/#1879/#1880: Fixing index not found for model group/model/tasks (#1895)</li>
<li>Change searchResponse method to fix breaking change in managed service (#1917)</li>
<li>Adjust ListTool response format (#1912)</li>
<li>Issue #844: Add accessUserInformation to the plugin security policy (#1959)</li>
<li>Escape input data (#1974)</li>
<li>flow agent suggestions missing (#2064)</li>
<li>bug fix - tool parameters missing (#2065)</li>
<li>fix empty tool parameter issue (#2067)</li>
<li>tool uses original input (#2068)</li>
<li>update Unthrotized error code to 401 (#2076)</li>
<li>handle null value exceptions when arguments are missing or Null in caling RAG pipeline (#2079)</li>
<li>changing error message and error code (#2073) (#2086)</li>
<li>Fix bwc issue in remote prediction (#2085)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Fixed exception for case when Hybrid query being wrapped into bool query (<a href="https://github.com/opensearch-project/neural-search/pull/490">#490</a>)</li>
</ul>
<ul>
<li>Hybrid query and nested type fields (<a href="https://github.com/opensearch-project/neural-search/pull/498">#498</a>)</li>
<li>Fixing multiple issues reported in #497 (<a href="https://github.com/opensearch-project/neural-search/pull/524">#524</a>)</li>
<li>Fix Flaky test reported in #433 (<a href="https://github.com/opensearch-project/neural-search/pull/533">#533</a>)</li>
<li>Enable support for default model id on HybridQueryBuilder (<a href="https://github.com/opensearch-project/neural-search/pull/541">#541</a>)</li>
<li>Fix Flaky test reported in #384 (<a href="https://github.com/opensearch-project/neural-search/pull/559">#559</a>)</li>
<li>Add validations for reranker requests per #555 (<a href="https://github.com/opensearch-project/neural-search/pull/562">#562</a>)</li>
</ul>

<h3>Opensearch Observability</h3>

<ul>
<li>Upgrade JSON to 20231013 to fix CVE-2023-5072 (<a href="https://github.com/opensearch-project/observability/pull/1750">#1750</a>)</li>
</ul>
<ul>
<li>Bumping ktlint and resolving conflicts (<a href="https://github.com/opensearch-project/observability/pull/1792">#1792</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Fix Bug with Install demo configuration running in cluster mode with -y (<a href="https://github.com/opensearch-project/security/pull/3936">#3936</a>)</li>
<li>Allow TransportConfigUpdateAction when security config initialization has completed (<a href="https://github.com/opensearch-project/security/pull/3810">#3810</a>) (<a href="https://github.com/opensearch-project/security/pull/3927">#3927</a>)</li>
<li>Fix the CI / report-coverage check by switching to corresponding actions/upload-artifact@v4 (<a href="https://github.com/opensearch-project/security/pull/3893">#3893</a>) (<a href="https://github.com/opensearch-project/security/pull/3895">#3895</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Fix for doc level query constructor change (<a href="https://github.com/opensearch-project/security-analytics/pull/651">#651</a>)</li>
<li>Make threat intel async (<a href="https://github.com/opensearch-project/security-analytics/pull/703">#703</a>)</li>
<li>Return empty response for empty mappings and no applied aliases (<a href="https://github.com/opensearch-project/security-analytics/pull/724">#724</a>)</li>
<li>Fix threat intel plugin integ test (<a href="https://github.com/opensearch-project/security-analytics/pull/774">#774</a>)</li>
<li>Use a common constant to specify the version for log type mappings (<a href="https://github.com/opensearch-project/security-analytics/pull/734">#708</a>)</li>
<li>Sigma keywords field not handled correctly (<a href="https://github.com/opensearch-project/security-analytics/pull/725">#725</a>)</li>
<li>Allow updation/deletion of custom log type if custom rule index is missing (<a href="https://github.com/opensearch-project/security-analytics/pull/767">#767</a>)</li>
<li>Delete detector successfully if workflow is missing (<a href="https://github.com/opensearch-project/security-analytics/pull/790">#790</a>)</li>
<li>fix null query filter conversion from sigma to query string query (<a href="https://github.com/opensearch-project/security-analytics/pull/722">#722</a>)</li>
<li>add field based rules support in correlation engine (<a href="https://github.com/opensearch-project/security-analytics/pull/737">#737</a>)</li>
<li>Reduce log level for informative message (<a href="https://github.com/opensearch-project/security-analytics/pull/203">#203</a>)</li>
</ul>

<h3>Opensearch k-NN</h3>

<ul>
<li>Fix use-after-free case on nmslib search path <a href="https://github.com/opensearch-project/k-NN/pull/1305">#1305</a></li>
<li>Allow nested knn field mapping when train model <a href="https://github.com/opensearch-project/k-NN/pull/1318">#1318</a></li>
<li>Properly designate model state for actively training models when nodes crash or leave cluster <a href="https://github.com/opensearch-project/k-NN/pull/1317">#1317</a></li>
<li>Fix script score queries not getting cached <a href="https://github.com/opensearch-project/k-NN/pull/1367">#1367</a></li>
<li>Fix KNNScorer to apply boost <a href="https://github.com/opensearch-project/k-NN/pull/1403">#1403</a></li>
<li>Fix equals and hashCode methods for KNNQuery and KNNQueryBuilder <a href="https://github.com/opensearch-project/k-NN/pull/1397">#1397</a></li>
<li>Pass correct value on IDSelectorBitmap initialization <a href="https://github.com/opensearch-project/k-NN/pull/1444">#1444</a></li>
</ul>

<h3>SQL</h3>

<ul>
<li>Fix bug, using basic instead of basicauth by @penghuo in https://github.com/opensearch-project/sql/pull/2342</li>
<li>create new session if current session not ready by @penghuo in https://github.com/opensearch-project/sql/pull/2363</li>
<li>Create new session if client provided session is invalid by @penghuo in https://github.com/opensearch-project/sql/pull/2368</li>
<li>Enable session by default by @penghuo in https://github.com/opensearch-project/sql/pull/2373</li>
<li>Return 429 for ConcurrencyLimitExceededException by @penghuo in https://github.com/opensearch-project/sql/pull/2428</li>
<li>Async query get result bug fix by @dai-chen in https://github.com/opensearch-project/sql/pull/2443</li>
<li>Validate session with flint datasource passed in async job request by @kaituo in https://github.com/opensearch-project/sql/pull/2448</li>
<li>Temporary fixes for build errors by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2476</li>
<li>Add SparkDataType as wrapper for unmapped spark data type by @penghuo in https://github.com/opensearch-project/sql/pull/2492</li>
<li>Fix wrong 503 error response code by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2493</li>
</ul>

<h3>Dashboards Assistant</h3>

<ul>
<li>Fix: comply with the field change of agent framework (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/137">#137</a>)</li>
</ul>

<h3>Dashboards Observability</h3>

<ul>
<li>Change class name to decouple styling from discover (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1427">#1427</a>)</li>
<li>Add modal for DQL language (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1422">#1422</a>)</li>
<li>fixing panel PPL filters not being added (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1419">#1419</a>)</li>
<li>Hide query assist UI if PPL agent is not created (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1400">#1400</a>)</li>
<li>Fix trace link in event viewer (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1396">#1396</a>)</li>
<li>Fix command syntax error for ppl_docs (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1372">#1372</a>)</li>
<li>Update snapshots for upstream changes (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1353">#1353</a>)</li>
<li>Fix for explorer data grid not paginating (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1140">#1140</a>)</li>
<li>Update URL of create datasources, fix spacing(<a href="https://github.com/opensearch-project/dashboards-observability/pull/1153">#1153</a>)</li>
<li>Disable integration set up button if invalid (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1160">#1160</a>)</li>
<li>Switch from toast to callout for integration set up failures (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1158">#1158</a>)</li>
<li>Fix integration labeling to identify S3 integrations (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1165">#1165</a>)</li>
<li>Correct date pass-through on Notebook Visualizations (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1327">#1327</a>)</li>
<li>Fix for Notebook Observability Visualization loading (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1312">#1312</a>)</li>
<li>Fix metrics loading loop (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1309">#1309</a>)</li>
<li>Fix explorer stats function typing crash (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1429">#1429</a>)</li>
</ul>

<h3>Opensearch Alerting Dashboards Plugin</h3>

<ul>
<li>Do not create Message component on every text change (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/854">#854</a>)</li>
</ul>

<h3>Opensearch Dashboards Maps</h3>

<ul>
<li>Fixed maps tooltip display at dark mode<a href="https://github.com/opensearch-project/dashboards-maps/pull/564">#564</a></li>
</ul>

<h3>Opensearch Dashboards Notifications</h3>

<ul>
<li>Replaced wrongly formatted mock Slack URLs with properly formatted mock Slack URLs. (<a href="https://github.com/opensearch-project/dashboards-notifications/pull/139">#139</a>)</li>
<li>Replace all wrong Chime urls with correct ones (<a href="https://github.com/opensearch-project/dashboards-notifications/pull/144">#144</a>)</li>
<li>Fix: CI flow on windows main (<a href="https://github.com/opensearch-project/dashboards-notifications/pull/145">#145</a>)</li>
</ul>

<h3>Opensearch Dashboards Reporting</h3>

<ul>
<li>Update the dependencies in .babelrc (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/260">#260</a>)
Fix the bootstrap failure on the fresh run (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/270">#270</a>)</li>
</ul>

<h3>Opensearch Dashboards Search Relevance</h3>

<ul>
<li>Updating snapshots (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/363">#363</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/364">#364</a>)</li>
</ul>

<h3>Opensearch Query Workbench</h3>

<ul>
<li>fixed create table async query bug (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/158">#158</a>)</li>
</ul>
<ul>
<li>design changes for loading, changed the banner: (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/170">#170</a>)</li>
<li>Make checkpoint mandatory, add watermark delay, minor UI fixes (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/173">#173</a>)</li>
<li>UI fixes for loading state, empty tree, added toast for error, fixed no indicies error (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/176">#176</a>)</li>
<li>Session update, minor fixes for acceleration flyout (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/179">#179</a>)</li>
<li>Add backticks and remove ckpt for manual refresh in acceleration flyout (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/183">#183</a>)</li>
<li>UI-bug fixes, added create query for MV (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/182">#182</a>)</li>
<li>added fix for loading spinner issue for other database (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/189">#189</a>)</li>
<li>Fix error handling for user w/o proper permissions (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/195">#195</a>)</li>
<li>Add minutes option to acceleration (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/249">#249</a>)</li>
<li>added changes for cancel query not being able to cancel (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/256">#256</a>)</li>
</ul>

<h3>Opensearch Security Analytics Dashboards</h3>

<ul>
<li>Ask for mapping of threat intel feeds related fields only when threat intel is enabled (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/849">#849</a>)</li>
<li>Add check for mappings view API call during create detector (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/862">#862</a>)</li>
</ul>

<h3>Opensearch Security Dashboards Plugin</h3>

<ul>
<li>Fixes Short URL redirection for SAML login (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1744">#1744</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1767">#1767</a>)</li>
<li>Disable tenancy pop-ups when disabled or default tenant set (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1759">#1759</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1763">#1763</a>)</li>
<li>Fix cannot find module when import ResourceType in server from public folder (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1705">#1705</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1716">#1716</a>)</li>
<li>Fix copy link issue in Safari (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1633">#1633</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1672">#1672</a>)</li>
<li>Fix bug where custom permission groups are missing (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1636">#1636</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1639">#1639</a>)</li>
</ul>

<h2>INFRASTRUCTURE</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Fix workflow security tests. (<a href="https://github.com/opensearch-project/alerting/pull/1310">#1310</a>)</li>
<li>Upgrade to Gradle 8.5 (<a href="https://github.com/opensearch-project/alerting/pull/1369">#1369</a>)</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Update to Gradle 8.5 (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1131">#1131</a>)</li>
<li>Remove default admin credentials (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1134">#1134</a>)</li>
<li>Require JDK version for java spotless check (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1129">#1129</a>)</li>
<li>Updated lucene snapshot url (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1146">#1146</a>)</li>
<li>Fix build, update CVE-affected versions (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1102">#1102</a>)</li>
</ul>

<h3>Opensearch Asynchronous Search</h3>

<ul>
<li>Updates admin credentials used in github workflow and upgrade to Gradle 8.5 (<a href="https://github.com/opensearch-project/asynchronous-search/pull/522">#522</a>)</li>
</ul>

<h3>Opensearch Custom Codecs</h3>

<ul>
<li>Onboard jenkins prod docker images to github actions (<a href="https://github.com/opensearch-project/custom-codecs/pull/77">#77</a>)</li>
<li>Switch to ci-runner user for the checks (<a href="https://github.com/opensearch-project/custom-codecs/pull/82">#82</a>)</li>
<li>Add updateVersion gradle task from plugin template (<a href="https://github.com/opensearch-project/custom-codecs/pull/87">#87</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Update admin credential in integration test (<a href="https://github.com/opensearch-project/index-management/pull/1084">#1084</a>)</li>
<li>Onboard jenkins prod docker images to github actions (<a href="https://github.com/opensearch-project/index-management/pull/1025">#1025</a>)</li>
<li>Improve security plugin enabling check (<a href="https://github.com/opensearch-project/index-management/pull/1017">#1017</a>)</li>
<li>Fixes password assignment for integTest when using remote cluster (<a href="https://github.com/opensearch-project/index-management/pull/1091">#1091</a>)</li>
<li>Accepts https as a property to set securityEnabled flag (<a href="https://github.com/opensearch-project/index-management/pull/1100">#1100</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Onboarding Jenkins prod docker images to github ci check (#1566)</li>
<li>Add code coverage report for commons and memory modules (#1585)</li>
<li>Adding UT coverage for in-cache update and fine-tuning throttling feature (#1913)</li>
<li>Add tests for MLAgent Get and Delete (#1794)</li>
<li>Fix race confition in index initialization and RestUpdateConnector UT (#1857)</li>
<li>Fix failing flaky tests due to pytorch library not available for dependency plugins (#1886)</li>
<li>Adding tests for all the agent runners (#1792)</li>
<li>Update deprecated openAI mode in integration test and fix flaky tests (#1858)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>BWC tests for Neural Search (<a href="https://github.com/opensearch-project/neural-search/pull/515">#515</a>)</li>
</ul>
<ul>
<li>Github action to run integ tests in secure opensearch cluster (<a href="https://github.com/opensearch-project/neural-search/pull/535">#535</a>)</li>
<li>BWC tests for Multimodal search, Hybrid Search and Neural Sparse Search (<a href="https://github.com/opensearch-project/neural-search/pull/533">#533</a>)</li>
<li>Distribution bundle bwc tests ([#579])(https://github.com/opensearch-project/neural-search/pull/579)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Fix integration test failure by allowing direct access to system index warning (<a href="https://github.com/opensearch-project/notifications/pull/784">#784</a>)</li>
<li>Add github workflow to auto bump bwc version (<a href="https://github.com/opensearch-project/notifications/pull/799">#799</a>)</li>
<li>Onboard prod jenkins docker image to github actions (<a href="https://github.com/opensearch-project/notifications/pull/809">#809</a>)</li>
<li>Update Gradle to 8.5 (<a href="https://github.com/opensearch-project/notifications/pull/824">#824</a>)</li>
</ul>

<h3>Opensearch Observability</h3>

<ul>
<li>Onboard jenkins prod docker images on github actions (<a href="https://github.com/opensearch-project/observability/pull/1763">#1763</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Update to Gradle 8.5 and Fixing CVE-2023-33202 <a href="https://github.com/opensearch-project/performance-analyzer/pull/617">#617</a></li>
</ul>

<h3>Opensearch Reporting</h3>

<ul>
<li>Bumping ktlint to 0.47.1 (<a href="https://github.com/opensearch-project/reporting/pull/960">#960</a>)</li>
<li>upgrade gradle to 8.5 (<a href="https://github.com/opensearch-project/reporting/pull/941">#941</a>)</li>
</ul>

<h3>Opensearch k-NN</h3>

<ul>
<li>Upgrade gradle to 8.4 <a href="https://github.com/opensearch-project/k-NN/pull/1289">1289</a></li>
<li>Refactor security testing to install from individual components <a href="https://github.com/opensearch-project/k-NN/pull/1307">#1307</a></li>
<li>Refactor integ tests that access model index <a href="https://github.com/opensearch-project/k-NN/pull/1423">#1423</a></li>
<li>Fix flaky model tests <a href="https://github.com/opensearch-project/k-NN/pull/1429">#1429</a></li>
</ul>

<h3>SQL</h3>

<ul>
<li>Onboard jenkins prod docker images in github actions by @peterzhuamazon in https://github.com/opensearch-project/sql/pull/2404</li>
<li>Add publishToMavenLocal to publish plugins in this script by @zane-neo in https://github.com/opensearch-project/sql/pull/2461</li>
<li>Update to Gradle 8.4 by @reta in https://github.com/opensearch-project/sql/pull/2433</li>
<li>Add JDK-21 to GA worklflows by @reta in https://github.com/opensearch-project/sql/pull/2481</li>
</ul>

<h3>Dashboards Observability</h3>

<ul>
<li>Add FTR workflow for dashboards observability (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1334">#1334</a>)</li>
<li>Fix no matching issue corner case for lint CI (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1326">#1326</a>)</li>
<li>Add enforce-labels action (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1330">#1330</a>)</li>
<li>Linter CI (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1313">#1313</a>)</li>
<li>Refactor Cypress Workflow (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1299">#1299</a>)</li>
</ul>

<h3>Opensearch Anomaly Detection Dashboards</h3>

<ul>
<li>Updating maintainers and code owners (<a href="https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/625">#625</a>)</li>
<li>Support github actions to run yarn build on build docker images (<a href="https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/620">#620</a>)</li>
<li>fix build error due to missing babel plugins (<a href="https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/661">#661</a>)</li>
<li>fix multiple CVEs (<a href="https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/675">#675</a>)</li>
</ul>

<h3>Opensearch Dashboards Reporting</h3>

<ul>
<li>Add E2E Cypress workflow for Dashboards Reporting (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/262">#262</a>)</li>
</ul>

<h3>Opensearch Dashboards Search Relevance</h3>

<ul>
<li>Onboard jenkins prod docker images to github actions (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/345">#345</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/346">#346</a>)</li>
<li>Remove babel-proposal plugins (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/355">#355</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/357">#357</a>)</li>
</ul>

<h3>Opensearch Dashboards Visualizations</h3>

<ul>
<li>Onboard jenkins prod docker images to github actions (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/287">#287</a>)</li>
</ul>
<ul>
<li>[CI/CD] Add Cypress e2e workflow for gantt chart (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/298">#298</a>)</li>
<li>[CI/CD] Add FTR workflow for gantt chart plugin test (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/306">#306</a>)</li>
<li>[CI/CD] Add eslint workflow (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/316">#316</a>)</li>
</ul>

<h3>Opensearch Index Management Dashboards Plugin</h3>

<ul>
<li>Onboard jenkins prod docker images to github actions (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/907">#907</a>)</li>
</ul>

<h3>Opensearch Query Workbench</h3>

<ul>
<li>Fix jest tests (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/255">#255</a>)</li>
</ul>

<h3>Opensearch Security Analytics Dashboards</h3>

<ul>
<li>Add missing modules common and types (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/875">#875</a>)</li>
<li>[Detector creation] UI workflow metrics (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/865">#865</a>)</li>
</ul>

<h2>DOCUMENTATION</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Added 2.12 release notes (<a href="https://github.com/opensearch-project/alerting/pull/1408">#1408</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Added 2.12.0.0 release notes (<a href="https://github.com/opensearch-project/common-utils/pull/585">#585</a>)</li>
</ul>

<h3>Opensearch Custom Codecs</h3>

<ul>
<li>Version 2.12 Release Notes (<a href="https://github.com/opensearch-project/custom-codecs/pull/110">#110</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Version 2.12 Release Notes Draft (<a href="https://github.com/opensearch-project/index-management/pull/1092">#1092</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Updated developer guide to include links for getting started with git (#1409)</li>
<li>Add triaging doc (#1250)</li>
<li>Add bedrock blueprint doc (#1501)</li>
<li>Add bedrock titan embedding model blueprint (#1527)</li>
<li>Fix bedrock embedding model blueprint (#1563)</li>
<li>Add openai embedding model blueprint (#1602)</li>
<li>Added Connector Blueprint for AI21 Labs Jurassic-2 Mid (#1617)</li>
<li>Update default model_access_mode for model group (#1677)</li>
<li>Add cohere version 3 embedding model (#1721)</li>
<li>Blueprint for multi-model titan model (#1729)</li>
<li>AI connector blueprint for the Aleph Alpha Luminous-Base Embedding Model (#2003)</li>
<li>Add tutorial doc for semantic search on amazon opensearch (#1928)</li>
<li>Add tutorial doc for semantic search with OpenAI embedding model (#1936)</li>
<li>Add connector blueprint for Azure OpenAI Embedding and Chat model (#2062)</li>
<li>Add updated Cohere Embedding blueprint (#2063)</li>
<li>add tutorial for conversational search (#2075)</li>
<li>Add Cohere Chat blueprint with RAG (#1991)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Add 2.12.0 release notes (<a href="https://github.com/opensearch-project/notifications/issues/851">#851</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Added 2.12.0 release notes. (<a href="https://github.com/opensearch-project/security-analytics/pull/834">#834</a>)</li>
<li>Add developer guide (<a href="https://github.com/opensearch-project/security-analytics/pull/791">#791</a>)</li>
</ul>

<h3>SQL</h3>

<ul>
<li>[DOC] Configure the Spark metrics properties while creating a s3 Glue Connector by @noCharger in https://github.com/opensearch-project/sql/pull/2504</li>
</ul>

<h3>Dashboards Observability</h3>

<ul>
<li>Use approved svg from UX in (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1066">#1066</a>)</li>
<li>add docker-compose.yml testing and readme for integration to 2.9 in (<a href="https://github.com/opensearch-project/dashboards-observability/pull/923">#923</a>)</li>
<li>Correct doc link (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1336">#1336</a>)</li>
<li>Integrations integration test fixes (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1331">#1331</a>)</li>
</ul>

<h3>Opensearch Alerting Dashboards Plugin</h3>

<ul>
<li>Drafted 2.12 release notes. (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/876">#876</a>)</li>
</ul>

<h3>Opensearch Dashboards Notifications</h3>

<ul>
<li>Drafted release notes. (<a href="https://github.com/opensearch-project/dashboards-notifications/pull/156">#156</a>)</li>
</ul>

<h3>Opensearch Dashboards Search Relevance</h3>

<ul>
<li>Updating CONTRIBUTING.md by adding DCO section (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/337">#337</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/341">#341</a>)</li>
<li>Update CONTRIBUTING.md by adding command for running tests to PR directions (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/335">#335</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/347">#347</a>)</li>
</ul>

<h3>Opensearch Index Management Dashboards Plugin</h3>

<ul>
<li>Version 2.12 Release Notes Draft (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/971">#971</a>)</li>
</ul>

<h3>Opensearch Security Analytics Dashboards</h3>

<ul>
<li>Added release notes for 2.12.0 (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/879">#879</a>)</li>
</ul>

<h2>MAINTENANCE</h2>

<h3>Opensearch Observability</h3>
<ul>
<li>Upgrade gradle to 8.5 (<a href="https://github.com/opensearch-project/observability/pull/1777">#1777</a>)</li>
</ul>
<ul>
<li>Remove integration content (<a href="https://github.com/opensearch-project/observability/pull/1738">#1738</a>)</li>
<li>Manually Force Secure logback Dependencies (<a href="https://github.com/opensearch-project/observability/pull/1795">#1795</a>)</li>
</ul>
<h2>SECURITY</h2>
<h3>SQL</h3>
<ul>
<li>Upgrade JSON to 20231013 to fix CVE-2023-5072 by @derek-ho in https://github.com/opensearch-project/sql/pull/2307</li>
<li>Block execution engine settings in sql query settings API and add more unit tests by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2407</li>
<li>upgrade okhttp to 4.12.0 by @joshuali925 in https://github.com/opensearch-project/sql/pull/2405</li>
<li>Bump aws-java-sdk-core version to 1.12.651 by @penghuo in https://github.com/opensearch-project/sql/pull/2503</li>
</ul>
<h2>New Contributors</h2>
<ul>
<li>@dreamer-89 made their first contribution in https://github.com/opensearch-project/sql/pull/2013</li>
<li>@kaituo made their first contribution in https://github.com/opensearch-project/sql/pull/2212</li>
<li>@zane-neo made their first contribution in https://github.com/opensearch-project/sql/pull/2452</li>
<li>@noCharger made their first contribution in https://github.com/opensearch-project/sql/pull/2467</li>
</ul>
<hr />
<p><strong>Full Changelog</strong>: https://github.com/opensearch-project/sql/compare/2.11.0.0...2.12.0.0</p>

<h3>Opensearch Alerting</h3>

<ul>
<li>Increment version to 2.12.0-SNAPSHOT. (<a href="https://github.com/opensearch-project/alerting/pull/1239">#1239</a>)</li>
<li>Removed default admin credentials for alerting (<a href="https://github.com/opensearch-project/alerting/pull/1399">#1399</a>)</li>
<li>ipaddress lib upgrade as part of cve fix (<a href="https://github.com/opensearch-project/alerting/pull/1397">#1397</a>)</li>
</ul>

<h3>Opensearch Asynchronous Search</h3>

<ul>
<li>Increment version to 2.12.0 (<a href="https://github.com/opensearch-project/asynchronous-search/pull/466">#466</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Increment version to 2.12.0-SNAPSHOT (<a href="https://github.com/opensearch-project/common-utils/pull/545">#545</a>)</li>
<li>Onboard prod jenkins docker image to github actions (<a href="https://github.com/opensearch-project/common-utils/pull/557">#557</a>)</li>
<li>Update Gradle to 8.4 (<a href="https://github.com/opensearch-project/common-utils/pull/560">#560</a>)</li>
<li>Add Java 11/17/21 matrix for build, test and integration checks (<a href="https://github.com/opensearch-project/common-utils/pull/561">#561</a>)</li>
<li>changed all usages of 'admin' as a password to something different (<a href="https://github.com/opensearch-project/common-utils/pull/581">#581</a>)</li>
<li>Update dependency com.pinterest:ktlint to 0.47.1 and fix CVE-2023-6378 (<a href="https://github.com/opensearch-project/common-utils/pull/585">#585</a>)</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Upgrade gradle to 8.4 (<a href="https://github.com/opensearch-project/geospatial/pull/596">#596</a>)</li>
<li>Update spotless and eclipse dependencies (<a href="https://github.com/opensearch-project/geospatial/pull/620">#620</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Increment version to 2.12.0-SNAPSHOT (<a href="https://github.com/opensearch-project/index-management/pull/996">#996</a>)</li>
<li>Update to Gradle 8.5 (<a href="https://github.com/opensearch-project/index-management/pull/1069">#1069</a>)</li>
<li>Upgrade ktlint to mitigate CVE-2023-6378 (<a href="https://github.com/opensearch-project/index-management/pull/1095">#1095</a>)</li>
</ul>

<h3>Opensearch Job Scheduler</h3>

<ul>
<li>Fix flaky tests (<a href="https://github.com/opensearch-project/job-scheduler/pull/556">#556</a>).</li>
<li>Use the build CI image in the Build and Test workflow (<a href="https://github.com/opensearch-project/job-scheduler/pull/534">#534</a>).</li>
<li>Upgrade gradle to 8.5 (<a href="https://github.com/opensearch-project/job-scheduler/pull/545">#545</a>).</li>
<li>Update release-drafter/release-drafter from 5 to 6 (<a href="https://github.com/opensearch-project/job-scheduler/pull/567">#567</a>).</li>
<li>Update  peter-evans/create-issue-from-file from 4 to 5 (<a href="https://github.com/opensearch-project/job-scheduler/pull/566">#566</a>).</li>
<li>Update <code>org.slf4j:slf4j-api</code> from 2.0.7 to 2.0.11 (<a href="https://github.com/opensearch-project/job-scheduler/pull/570">#570</a>).</li>
<li>Update <code>com.google.googlejavaformat:google-java-format</code> from 1.17.0 to 1.19.2 (<a href="https://github.com/opensearch-project/job-scheduler/pull/555">#555</a>).</li>
<li>Update <code>com.google.guava:guava</code> from 32.1.2-jre to 32.1.3-jre (<a href="https://github.com/opensearch-project/job-scheduler/pull/530">#530</a>).</li>
<li>Update <code>com.google.guava:failureacces</code>s from 1.0.1 to 1.0.2 (<a href="https://github.com/opensearch-project/job-scheduler/pull/532">#532</a>).</li>
<li>Update <code>com.netflix.nebula.ospackage</code> from 11.5.0 to 11.6.0 (<a href="https://github.com/opensearch-project/job-scheduler/pull/551">#551</a>).</li>
<li>Update <code>com.diffplug.spotless</code> from 6.22.0 to 6.25.0 (<a href="https://github.com/opensearch-project/job-scheduler/pull/558">#558</a>).</li>
<li>Fix backport workflow (<a href="https://github.com/opensearch-project/job-scheduler/pull/533">#533</a>).</li>
<li>Enable <code>publishPluginZipPublicationToMavenLocal</code> gradle task to publish job-scheduler plugin zip to maven local (<a href="https://github.com/opensearch-project/job-scheduler/pull/584">#584</a>).</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Add Austin and Henry as maintainer (#1579)</li>
<li>Updated version of awssdk (#1607)</li>
<li>Update Gradle to 8.4 (#1697)</li>
<li>Address CVE-2023-42503 (#1727)</li>
<li>Fix CVE-2023-2976 and upgrade guava to be consistent (#2013)</li>
<li>Fix CVE-2023-42503 due to djl models (#2016)</li>
<li>Add maintainer (#1952)</li>
<li>Updating maintainers list (#1938)</li>
<li>Bump Mockito dependencies (#1868)</li>
<li>Updated OpenSearch Lucene snapshot location (#1834)</li>
<li>Add kotlin stblib dependency for SearchAlertTool (#1861)</li>
<li>Update dependency com.jayway.jsonpath:json-path to v2.9.0 (#1956)</li>
<li>Update http package import for 2.x (#1957)</li>
<li>Update the lucene snapshot url (#2082)</li>
<li>removing skills first (#2089)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Added support for jdk-21 (<a href="https://github.com/opensearch-project/neural-search/pull/500">#500</a>))</li>
</ul>
<ul>
<li>Update spotless and eclipse dependencies (<a href="https://github.com/opensearch-project/neural-search/pull/589">#589</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Increment version to 2.12.0-SNAPSHOT (<a href="https://github.com/opensearch-project/notifications/pull/780">#780</a>)</li>
<li>Update dependency org.json:json to v20231013 (<a href="https://github.com/opensearch-project/notifications/pull/795">#795</a>)</li>
<li>Replace the TestMailServer to GreenMail server (<a href="https://github.com/opensearch-project/notifications/pull/807">#807</a>)</li>
<li>Re-enable detekt (<a href="https://github.com/opensearch-project/notifications/pull/796">#796</a>)</li>
<li>Removed default admin credentials. (<a href="https://github.com/opensearch-project/notifications/pull/837">#837</a>)</li>
<li>Force logback to use 1.3.14 (<a href="https://github.com/opensearch-project/notifications/pull/849">#849</a>)</li>
<li>Bump ktlint version to fix CVE (<a href="https://github.com/opensearch-project/notifications/pull/850">#850</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Remove redundant ClusterManagerThrottlingMetricsCollector <a href="https://github.com/opensearch-project/performance-analyzer/pull/582">#582</a></li>
<li>Update spotless to meet JDK-21 baseline <a href="https://github.com/opensearch-project/performance-analyzer/pull/618">#618</a></li>
</ul>

<h3>Opensearch Reporting</h3>

<ul>
<li>Onboard jenkins prod docker images to github actions (<a href="https://github.com/opensearch-project/reporting/pull/924">#924</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Bump org.apache.camel:camel-xmlsecurity from 3.22.0 to 3.22.1 (<a href="https://github.com/opensearch-project/security/pull/4018">#4018</a>)</li>
<li>Bump release-drafter/release-drafter from 5 to 6 (<a href="https://github.com/opensearch-project/security/pull/4021">#4021</a>)</li>
<li>Bump com.netflix.nebula.ospackage from 11.6.0 to 11.7.0 (<a href="https://github.com/opensearch-project/security/pull/4019">#4019</a>)</li>
<li>Bump org.junit.jupiter:junit-jupiter from 5.10.1 to 5.10.2 (<a href="https://github.com/opensearch-project/security/pull/4020">#4020</a>)</li>
<li>Bump jjwt_version from 0.12.4 to 0.12.5 (<a href="https://github.com/opensearch-project/security/pull/4017">#4017</a>)</li>
<li>Bump io.dropwizard.metrics:metrics-core from 4.2.24 to 4.2.25 (<a href="https://github.com/opensearch-project/security/pull/3998">#3998</a>)</li>
<li>Bump gradle/gradle-build-action from 2 to 3 (<a href="https://github.com/opensearch-project/security/pull/4000">#4000</a>)</li>
<li>Bump jjwt_version from 0.12.3 to 0.12.4 (<a href="https://github.com/opensearch-project/security/pull/3999">#3999</a>)</li>
<li>Bump spotless (6.24.0 -&gt; 6.25.0) to bump eclipse resources (3.18 -&gt; 3.19)  (<a href="https://github.com/opensearch-project/security/pull/3993">#3993</a>)</li>
<li>Fix: remove unnecessary trailing slashes in APIs. (<a href="https://github.com/opensearch-project/security/pull/3978">#3978</a>)</li>
<li>Adds new ml-commons system indices to the list (<a href="https://github.com/opensearch-project/security/pull/3974">#3974</a>)</li>
<li>Bump io.dropwizard.metrics:metrics-core from 4.2.23 to 4.2.24 (<a href="https://github.com/opensearch-project/security/pull/3970">#3970</a>)</li>
<li>Bump com.fasterxml.woodstox:woodstox-core from 6.5.1 to 6.6.0 (<a href="https://github.com/opensearch-project/security/pull/3969">#3969</a>)</li>
<li>Bump com.diffplug.spotless from 6.23.3 to 6.24.0 (<a href="https://github.com/opensearch-project/security/pull/3947">#3947</a>)</li>
<li>Bump org.apache.camel:camel-xmlsecurity from 3.21.3 to 3.22.0 (<a href="https://github.com/opensearch-project/security/pull/3906">#3906</a>)</li>
<li>Bump com.google.errorprone:error_prone_annotations from 2.23.0 to 2.24.0 (<a href="https://github.com/opensearch-project/security/pull/3897">#3897</a>) (<a href="https://github.com/opensearch-project/security/pull/3902">#3902</a>)</li>
<li>Bump io.dropwizard.metrics:metrics-core from 4.2.22 to 4.2.23 (<a href="https://github.com/opensearch-project/security/pull/3900">#3900</a>)</li>
<li>Bump com.google.googlejavaformat:google-java-format from 1.18.1 to 1.19.1 (<a href="https://github.com/opensearch-project/security/pull/3901">#3901</a>)</li>
<li>Bump github/codeql-action from 2 to 3 (<a href="https://github.com/opensearch-project/security/pull/3859">#3859</a>) (<a href="https://github.com/opensearch-project/security/pull/3867">#3867</a>)</li>
<li>Bump org.apache.camel:camel-xmlsecurity from 3.21.2 to 3.21.3 (<a href="https://github.com/opensearch-project/security/pull/3864">#3864</a>)</li>
<li>Bump org.checkerframework:checker-qual from 3.40.0 to 3.42.0 (<a href="https://github.com/opensearch-project/security/pull/3857">#3857</a>) (<a href="https://github.com/opensearch-project/security/pull/3866">#3866</a>)</li>
<li>Bump com.flipkart.zjsonpatch:zjsonpatch from 0.4.14 to 0.4.16 (<a href="https://github.com/opensearch-project/security/pull/3865">#3865</a>)</li>
<li>Bump com.netflix.nebula.ospackage from 11.5.0 to 11.6.0 (<a href="https://github.com/opensearch-project/security/pull/3863">#3863</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Increment to 2.12. (<a href="https://github.com/opensearch-project/security-analytics/pull/771">#771</a>)</li>
<li>Onboard prod jenkins docker images to github actions (<a href="https://github.com/opensearch-project/security-analytics/pull/710">#710</a>)</li>
<li>Match maintainer account username (<a href="https://github.com/opensearch-project/security-analytics/pull/438">#438</a>)</li>
<li>Add to Codeowners (<a href="https://github.com/opensearch-project/security-analytics/pull/726">#726</a>)</li>
<li>Fix codeowners to match maintainers (<a href="https://github.com/opensearch-project/security-analytics/pull/783">#783</a>)</li>
<li>updated lucene MAX_DIMENSIONS path (<a href="https://github.com/opensearch-project/security-analytics/pull/607">#607</a>)</li>
<li>Addresses changes related to default admin credentials (<a href="https://github.com/opensearch-project/security-analytics/pull/832">#832</a>)</li>
<li>Upgrade Lucene Codec to Lucene99 + Upgrade to Gradle 8.5 (<a href="https://github.com/opensearch-project/security-analytics/pull/800">#800</a>)</li>
<li>fix CVE-2023-2976 (<a href="https://github.com/opensearch-project/security-analytics/pull/835">#835</a>)</li>
</ul>

<h3>Opensearch k-NN</h3>

<ul>
<li>Update developer guide to include M1 Setup <a href="https://github.com/opensearch-project/k-NN/pull/1222">#1222</a></li>
<li>Upgrade urllib to 1.26.17 <a href="https://github.com/opensearch-project/k-NN/pull/1278">#1278</a></li>
<li>Upgrade urllib to 1.26.18 <a href="https://github.com/opensearch-project/k-NN/pull/1319">#1319</a></li>
<li>Upgrade guava to 32.1.3 <a href="https://github.com/opensearch-project/k-NN/pull/1319">#1319</a></li>
<li>Bump lucene codec to 99 <a href="https://github.com/opensearch-project/k-NN/pull/1383">#1383</a></li>
<li>Update spotless and eclipse dependencies <a href="https://github.com/opensearch-project/k-NN/pull/1450">#1450</a></li>
</ul>

<h3>Opensearch Alerting Dashboards Plugin</h3>

<ul>
<li>Remove integtest.sh since it is not being used. (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/849">#849</a>)</li>
<li>[AUTO] Increment version to 2.12.0.0 (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/772">#772</a>)</li>
</ul>

<h3>Opensearch Dashboards Maps</h3>

<ul>
<li>Fix broken build and failing tests <a href="https://github.com/opensearch-project/dashboards-maps/pull/572">#572</a></li>
<li>Update dependencies to align with other plugins <a href="https://github.com/opensearch-project/dashboards-maps/pull/575">#575</a></li>
</ul>

<h3>Opensearch Dashboards Notifications</h3>

<ul>
<li>Increment version to 2.12.0.0 (<a href="https://github.com/opensearch-project/dashboards-notifications/pull/130">#130</a>)</li>
<li>Increase OSD start timeout for windows platform (<a href="https://github.com/opensearch-project/dashboards-notifications/pull/135">#118</a>)</li>
<li>Update to latest babel package name (<a href="https://github.com/opensearch-project/dashboards-notifications/pull/142">#142</a>)</li>
</ul>

<h3>Opensearch Dashboards Reporting</h3>

<ul>
<li>Add eslint workflow (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/273">#273</a>)
Sync dependencies with latest versions (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/268">#268</a>)
Onboard jenkins prod docker images to github actions (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/243">243</a>)</li>
</ul>

<h3>Opensearch Dashboards Visualizations</h3>

<ul>
<li>Increment Version to 2.11.0 (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/253">#253</a>)</li>
</ul>
<ul>
<li>Onboard Stylelint (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/229">#229</a>)</li>
<li>Increment version to 2.12.0.0 (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/272">#272</a>)</li>
<li>Rename the .babelrc file (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/294">#294</a>)</li>
<li>Bump Cypress version from 5.0.0 to 12.8.1 (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/296">#296</a>)</li>
<li>Sync dependencies with latest versions (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/310">#310</a>)</li>
<li>Update jest snapshots &amp; cypress tests (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/314">#314</a>)</li>
<li>Move gantt-chart out from subdirectory (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/321">#321</a>)</li>
</ul>

<h3>Opensearch Index Management Dashboards Plugin</h3>

<ul>
<li>Remove unused integtest.sh file (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/954">#954</a>)</li>
<li>Increment version to 2.12.0.0 (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/928">#928</a>)</li>
<li>Update the babel require (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/935">#935</a>)</li>
<li>Update browserify-sign to fix cve-2023-46234 (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/978">#978</a>)</li>
</ul>

<h3>Opensearch ML Commons Dashboards</h3>

<ul>
<li>Increment version to 2.12.0.0 (<a href="https://github.com/opensearch-project/ml-commons-dashboards/pull/279">#279</a>)</li>
</ul>

<h3>Opensearch Query Workbench</h3>

<ul>
<li>Increment version to 2.12.0.0 (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/164">#164</a>)</li>
</ul>
<ul>
<li>Onboard Jenkins prod docker images to github actions (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/198">#198</a>)</li>
<li>Bump Cypress to version 12 (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/234">#234</a>)</li>
<li>Add E2E Cypress workflow for sql workbench (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/235">#235</a>)</li>
<li>Add FTR workflow for sql workbench (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/239">#239</a>)</li>
<li>Add eslint workflow (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/245">#245</a>)</li>
<li>babel config change: (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/229">#1229</a>)</li>
</ul>

<h3>Opensearch Security Analytics Dashboards</h3>

<ul>
<li>[AUTO] Increment version to 2.12.0.0 (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/761">#761</a>)</li>
</ul>

<h3>Opensearch Security Dashboards Plugin</h3>

<ul>
<li>Removing Prerequisite Checks Workflow (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1757">#1757</a>)</li>
<li>Addressing spelling mistakes in server code. (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1753">#1753</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1754">#1754</a>)</li>
<li>Moves eslint to devDependency and save yarn.lock file (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1746">#1746</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1748">#1748</a>)</li>
<li>Update cypress E2E workflow to reflect changes to default admin password (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1714">#1714</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1719">#1719</a>)</li>
<li>Pass in env variable and -t flag to set &quot;admin&quot; as the initial admin password (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1708">#1708</a>)</li>
<li>Increment version to 2.12.0.0 (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1686">#1686</a>)</li>
<li>Upgrade glob-parent to 5.1.2 and debug to 4.3.4 (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1685">#1685</a>)</li>
<li>Check in yarn.lock for 2.x branch (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1671">#1671</a>)</li>
<li>Different Values Pointing to Basic Auth, Need to Unify (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1619">#1619</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1649">#1649</a>)</li>
<li>Stabilize SAML integration test cases for security dashboard CIs (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1641">#1641</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1654">#1654</a>)</li>
<li>Update babel imports (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1652">#1652</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1653">#1653</a>)</li>
</ul>


<h2>REFACTORING</h2>

<h3>Opensearch Alerting</h3>

<ul>
<li>Reference get monitor and search monitor action / request / responses from common-utils (<a href="https://github.com/opensearch-project/alerting/pull/1315">#1315</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Move get monitor and search monitor action / request / responses to common-utils (<a href="https://github.com/opensearch-project/common-utils/pull/566">#566</a>)</li>
</ul>
<h1>Features</h1>
<ul>
<li>Implemented cross-cluster monitor support (<a href="https://github.com/opensearch-project/common-utils/pull/584">#584</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Rename memory field names in responses (#2020)</li>
<li>Refactor memory layer APIs (#1890)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Deprecate the <code>max_token_score</code> field in <code>neural_sparse</code> query clause (<a href="https://github.com/opensearch-project/neural-search/pull/478">#478</a>)</li>
</ul>
<ul>
<li>Added spotless check in the build (<a href="https://github.com/opensearch-project/neural-search/pull/515">#515</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Refactored alert tests (<a href="https://github.com/opensearch-project/security-analytics/pull/837">#837</a>)</li>
</ul>

<h3>SQL</h3>

<ul>
<li>Refactoring in Unit Tests by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2308</li>
<li>deprecated job-metadata-index by @penghuo in https://github.com/opensearch-project/sql/pull/2339</li>
<li>Refactoring for tags usage in test files. by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2383</li>
<li>Add seder to TransportPPLQueryResponse by @zane-neo in https://github.com/opensearch-project/sql/pull/2452</li>
<li>Move pplenabled to transport by @zane-neo in https://github.com/opensearch-project/sql/pull/2451</li>
<li>Async Executor Service Depedencies Refactor by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2488</li>
</ul>

<h3>Opensearch Dashboards Search Relevance</h3>

<ul>
<li>Add id attribute to search bar (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/338">#338</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/353">#353</a>)</li>
</ul>
<h2>New Contributors</h2>
<ul>
<li>@nung22 made their first contribution in <a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/300">#300</a></li>
</ul>

<h3>Opensearch Security Dashboards Plugin</h3>

<ul>
<li>Refactor cypress OIDC tests to use Run Cypress Tests action (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1755">#1755</a>) (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1756">#1756</a>)</li>
</ul>

<h2>EXPERIMENTAL</h2>
<h3>Opensearch ML Common</h3>
<ul>
<li>Update Model API (#1350)</li>
<li>Hidden model implementation (#1755)</li>
<li>Model &amp; user level throttling (#1814)</li>
<li>Search agent api (#1826)</li>
<li>Add GetTool API and ListTools API (#1850)</li>
<li>Enable in-place update model (#1796)</li>
<li>Memory Manager and Update Memory Actions/APIs (#1776)</li>
<li>Add CatIndexTool (#1770)</li>
<li>Add search and singular APIs to conversation memory (#1720)</li>
<li>Memory interface in spi (#1771)</li>
<li>Tool interface (#1772)</li>
<li>Add get config api to retrieve root agent id (#1995)</li>
<li>Register agent rest and transport actions (#1801)</li>
<li>IndicesHandler and conversationIndexMemory (#1777)</li>
<li>Adding mlmodeltool and agent tool with tests (#1778)</li>
<li>Get and delete agent APIs (#1779)</li>
<li>Add register action request/response (#1780)</li>
<li>Add execute agent api; add load extension (#1810)</li>
<li>Add IndexMapping Tool (#1934)</li>
<li>Agent meta classes in common (#1759)</li>
<li>Agent framework disable/enable flag (#1994)</li>
<li>Do not allow non super admin users to undeploy hidden models (#1981)</li>
<li>System error handling (#2051)</li>
<li>Handling tool errors (#1881)</li>
<li>Changes to hidden model code to use OPENDISTRO_SECURITY_USER instad of ssl principal (#1897) (#1900)</li>
<li>Support regenerate for chatbot (#1823)</li>
<li>Update IndexMappingTool Description (#1998)</li>
<li>Add more user based permission check in Memory (#1935)</li>
<li>Update memory index name and add updated_time (#1793)</li>
<li>fine tune prompt;refactor conversational agent code (#2094)</li>
</ul>

<h3>Dashboards Assistant</h3>

<ul>
<li>Features</li>
</ul>
<ul>
<li>Integrate chatbot with agent framework (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/2">#2</a>)(<a href="https://github.com/opensearch-project/dashboards-assistant/commit/88eb43e">88eb43e</a>)</li>
<li>Add conversation management (<a href="https://github.com/opensearch-project/dashboards-assistant/commit/7ceee22">7ceee22</a>)(<a href="https://github.com/opensearch-project/dashboards-assistant/commit/d941234">d941234</a>)</li>
<li>Implement how was it generated function with agent framework API (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/25">#25</a>)(<a href="https://github.com/opensearch-project/dashboards-assistant/commit/94fed43">94fed43</a>)</li>
<li>Add regenerating interaction (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/58">#58</a>)(<a href="https://github.com/opensearch-project/dashboards-assistant/commit/11e5779">11e5779</a>)</li>
<li>Support give feedback on interaction (<a href="https://github.com/opensearch-project/dashboards-assistant/commit/9c6cb29">9c6cb29</a>)(<a href="https://github.com/opensearch-project/dashboards-assistant/commit/4ff6726">4ff6726</a>)</li>
<li>Support save conversation to notebook (<a href="https://github.com/opensearch-project/dashboards-assistant/commit/3010362">3010362</a>)(<a href="https://github.com/opensearch-project/dashboards-assistant/pull/93">#93</a>)</li>
</ul>


