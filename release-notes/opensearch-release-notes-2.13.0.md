<h1>OpenSearch and OpenSearch Dashboards 2.13.0 Release Notes</h1>
<h2>RELEASE HIGHLIGHTS</h2>

OpenSearch 2.13 includes several new features designed to help you build AI-powered applications, along with upgrades to help you access and analyze your operational data, and new ways to support resiliency for your OpenSearch clusters.

<h2>NEW FEATURES</h2>
<ul>
<li>The OpenSearch flow framework is generally available, allowing you to automate the configuration of search and ingest pipeline resources required by advanced search features like semantic, multimodal, and conversational search.</li>

<li>AI connectors receive several enhancements, including predefined templates that let you automate setup for machine learning models that are integrated through OpenSearch connectors to APIs such as those from OpenAI, Amazon Bedrock, and Cohere. New settings for AI connectors allow users to configure timeouts and automatically deploy models.</li>

<li>The OpenSearch Assistant Toolkit is now generally available, allowing developers to build interactive, AI-powered assistant experiences in OpenSearch that let users query their operational and security log data using natural language.</li> 

<li>The agent framework is now generally available, allowing you to automate machine learning  tasks using agents and tools.</li> 

<li>OpenSearch now supports guardrails for large language models (LLMs). The agent framework adds support for user-defined regex rules that can be used to filter inappropriate text generation that could be produced by integrated LLMs.</li>

<li>You can now index quantized vectors with FAISS engine based k-NN indexes. Instead of storing vectors that require 4 bytes per dimension, you can compress the dimensions down to 2 bytes, which can reduce memory requirements and improve query latency.</li>

<li>You can now post-filter hybrid search results, allowing you to apply aggregations to the results to support use cases such as faceting.</li>

<li>By default, OpenSearch executes upsert and get operations by executing a term query on document id to determine if the document is present in the index. With this release, users can now control whether fuzzy_set should be enabled to optimize document ID lookups in index or search calls using the Bloom filter data structure, with potential for throughput improvements of up to 30%.</li> 

<li>This release adds I/O-based admission control, a proactive mechanism designed to support cluster resiliency by protecting against spikes or increases in capacity if a cluster’s I/O usage breaches a defined threshold.</li>

<li>New cross-cluster monitors are added to the alerting plugin, allowing you to manage alerts across clusters. This release also introduces the option to set up a cluster that is dedicated to alerting, separating alerting resources from indexing and querying workloads.</li>
</ul>

<h2>RELEASE DETAILS</h2>
[OpenSearch and OpenSearch Dashboards 2.13.0](https://opensearch.org/versions/opensearch-2-3-0.html) includes the following features, enhancements, bug fixes, infrastructure, documentation, maintenance and refactoring updates.
<ul>
<li>
OpenSearch <a href="https://github.com/opensearch-project/OpenSearch/blob/2.13/release-notes/opensearch.release-notes-2.13.0.md">Release Notes</a>.
</li>
<li>
OpenSearch Dashboards <a href="https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.13/release-notes/opensearch-dashboards.release-notes-2.13.0.md">Release Notes</a>.
</li>
</ul>

<h2>FEATURES</h2>

<h3>OpenSearch Flow Framework</h3>

<ul>
<li>Added create ingest pipeline step (<a href="https://github.com/opensearch-project/flow-framework/pull/558">#558</a>)</li>
<li>Added create search pipeline step (<a href="https://github.com/opensearch-project/flow-framework/pull/569">#569</a>)</li>
<li>Added create index step (<a href="https://github.com/opensearch-project/flow-framework/pull/574">#574</a>)</li>
<li>Added default use cases (<a href="https://github.com/opensearch-project/flow-framework/pull/583">#583</a>)</li>
</ul>

<h3>OpenSearch ML Commons</h3>

<ul>
<li>Hidden agent (<a href="https://github.com/opensearch-project/ml-commons/pull/2204">#2204</a>)</li>
<li>Auto deployment for remote models (<a href="https://github.com/opensearch-project/ml-commons/pull/2206">#2206</a>)</li>
<li>Support question answering model (<a href="https://github.com/opensearch-project/ml-commons/pull/2208">#2208</a>)</li>
<li>Guardrails for remote model input and output (<a href="https://github.com/opensearch-project/ml-commons/pull/2209">#2209</a>)</li>
</ul>

<h3>OpenSearch Neural Search</h3>

<ul>
<li>Implement document chunking processor with fixed token length and delimiter algorithm (<a href="https://github.com/opensearch-project/neural-search/pull/607/">#607</a>)</li>
</ul>
<ul>
<li>Enabled support for applying default modelId in neural sparse query (<a href="https://github.com/opensearch-project/neural-search/pull/614">#614</a></li>
</ul>

<h3>OpenSearch Reporting</h3>

<ul>
<li>xlsx support (<a href="https://github.com/opensearch-project/reporting/pull/940">#940</a>)</li>
</ul>

<h3>OpenSearch Security Analytics</h3>

<ul>
<li>Findings api enhancements (#<a href="https://github.com/opensearch-project/security-analytics/pull/914">914</a>) (#<a href="https://github.com/opensearch-project/security-analytics/issues/795">795</a>)</li>
<li>Get all findings as part of findings API enhancement (#<a href="https://github.com/opensearch-project/security-analytics/pull/803">803</a>)</li>
<li>Support object fields in aggregation based sigma rules (#<a href="https://github.com/opensearch-project/security-analytics/pull/789">789</a>)</li>
<li>Add latest sigma rules (#<a href="https://github.com/opensearch-project/security-analytics/pull/942">942</a>)</li>
</ul>

<h3>OpenSearch Skills</h3>

<ul>
<li>Fix SearchAnomalyDetectorsTool indices param bug</li>
<li>Fix detector state params in SearchAnomalyDetectorsTool</li>
<li>Update ppl tool claude model prompts to use &lt;ppl&gt; tags</li>
<li>Add parameter validation for PPL tool</li>
</ul>

<h3>Dashboards Observability</h3>

<ul>
<li>Add integration installation to data sources flyout (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1568">#1568</a>)</li>
<li>Integrations: Update delete modal to support custom verify prompt (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1567">#1567</a>)</li>
<li>Data sources bug fixes and UI improvements (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1565">#1565</a>)</li>
<li>Allow browsing integrations in Flyout from Data Sources page (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1562">#1562</a>)</li>
<li>Add auto-suggestions for skipping index definition and export types (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1552">#1552</a>)</li>
<li>Data Sources component Improvements and bug fixes (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1551">#1551</a>)</li>
<li>Adding datasource status and filter for hive tables (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1549">#1549</a>)</li>
<li>Implement redirection to explorer within data sources (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1548">#1548</a>)</li>
<li>Add actual integration queries to table (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1544">#1544</a>)</li>
<li>Remove modal for discover redirection (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1543">#1543</a>)</li>
<li>Acceleration Actions Implementation (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1540">#1540</a>)</li>
<li>Updating UI for create acceleration flyout (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1532">#1532</a>)</li>
<li>Add conditional installation for S3 integrations (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1528">#1528</a>)</li>
<li>Add datasource field in accelerations cache (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1525">#1525</a>)</li>
<li>Acceleration components' data implementation (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1521">#1521</a>)</li>
<li>Add Retrieval from Catalog Cache (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1517">#1517</a>)</li>
<li>Export observability start interface (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1515">#1515</a>)</li>
<li>Expose create acceleration flyout, update acceleration docs link (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1513">#1513</a>)</li>
<li>Bump plugin version to 2.13.0 (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1506">#1506</a>)</li>
<li>Catalog cache and Session update for async queries (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1500">#1500</a>)</li>
<li>Add flyout pages to associated objects table (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1496">#1496</a>)</li>
<li>Remove index store region and index store URI for data connection panel (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1490">#1490</a>)</li>
<li>Accelerations Tab and Flyout Skeletons (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1489">#1489</a>)</li>
<li>Associated objects searchbar filters (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1474">#1474</a>)</li>
<li>Data sources associated objects tab (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1470">#1470</a>)</li>
</ul>

<h3>OpenSearch Dashboards Reporting</h3>

<ul>
<li>Add xlsx support(<a href="https://github.com/opensearch-project/dashboards-reporting/pull/275">#275</a>)</li>
</ul>

<h3>OpenSearch Dashboards Search Relevance</h3>

<ul>
<li>Feature: Add Option to Expand Document Source (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/350">#350</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/378">#378</a>)</li>
</ul>

<h3>OpenSearch Query Workbench</h3>

<ul>
<li>Updates create accelerations flyout usage and side tree (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/285">#285</a>)</li>
</ul>

<h3>OpenSearch Security Analytics Dashboards</h3>

<ul>
<li>Added spinner to better indicate that rules are loading (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/905">#905</a>)</li>
<li>Rule editor enhancements (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/924">#924</a>)</li>
<li>Fetch all findings and alerts for the detectors when displaying in the tables (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/942">#942</a>)</li>
</ul>

<h2>ENHANCEMENTS</h2>

<h3>OpenSearch Alerting</h3>

<ul>
<li>Enhance per bucket, and per document monitor notification message ctx. (#<a href="https://github.com/opensearch-project/alerting/pull/1450">1450</a>) (#<a href="https://github.com/opensearch-project/alerting/pull/1477">1477</a>)</li>
<li>Findings API Enhancements changes and integ tests fix (#<a href="https://github.com/opensearch-project/alerting/pull/1464">1464</a>) (#<a href="https://github.com/opensearch-project/alerting/pull/1474">1474</a>)</li>
<li>Feature findings enhancement (#<a href="https://github.com/opensearch-project/alerting/pull/1427">1427</a>) (#<a href="https://github.com/opensearch-project/alerting/pull/1457">1457</a>)</li>
<li>Add distributed locking to jobs in alerting (#<a href="https://github.com/opensearch-project/alerting/pull/1403">1403</a>) (#<a href="https://github.com/opensearch-project/alerting/pull/1458">1458</a>)</li>
</ul>

<h3>OpenSearch Custom Codecs</h3>

<ul>
<li>Remove unneccessary ArrayUtil.grow in Zstd compression modes. (<a href="https://github.com/opensearch-project/custom-codecs/pull/121">#121</a>)</li>
</ul>

<h3>OpenSearch Common Utils</h3>

<ul>
<li>Add queryFieldNames field in Doc Level Queries (#<a href="https://github.com/opensearch-project/common-utils/pull/582">582</a>) (#<a href="https://github.com/opensearch-project/common-utils/pull/597">597</a>)</li>
</ul>
<h1>Features</h1>
<ul>
<li>Fix findings API enhancemnts (#<a href="https://github.com/opensearch-project/common-utils/pull/611">611</a>) (#<a href="https://github.com/opensearch-project/common-utils/pull/617">617</a>)</li>
<li>Feature findings enhancemnt (#<a href="https://github.com/opensearch-project/common-utils/pull/596">596</a>) (#<a href="https://github.com/opensearch-project/common-utils/pull/606">606</a>)</li>
</ul>

<h3>OpenSearch Flow Framework</h3>

<ul>
<li>Substitute REST path or body parameters in Workflow Steps (<a href="https://github.com/opensearch-project/flow-framework/pull/525">#525</a>)</li>
<li>Added an optional workflow_step param to the get workflow steps API (<a href="https://github.com/opensearch-project/flow-framework/pull/538">#538</a>)</li>
<li>Add created, updated, and provisioned timestamps to saved template (<a href="https://github.com/opensearch-project/flow-framework/pull/551">#551</a>)</li>
<li>Enable Flow Framework by default (<a href="https://github.com/opensearch-project/flow-framework/pull/553">#553</a>)</li>
<li>Adding new exception type for workflow step failures (<a href="https://github.com/opensearch-project/flow-framework/pull/577">#577</a>)</li>
</ul>

<h3>OpenSearch ML Commons</h3>

<ul>
<li>Adding connector http timeout in the connector level (<a href="https://github.com/opensearch-project/ml-commons/pull/1835">#1835</a>)</li>
<li>Enable auto redeploy for hidden model (<a href="https://github.com/opensearch-project/ml-commons/pull/2102">#2102</a>)</li>
<li>Add verification to rate limiter number field (<a href="https://github.com/opensearch-project/ml-commons/pull/2113">#2113</a>)</li>
<li>Asymmetric embeddings (<a href="https://github.com/opensearch-project/ml-commons/pull/2123">#2123</a>)</li>
<li>Set the number of ml system index primary shards to 1 (<a href="https://github.com/opensearch-project/ml-commons/pull/2137">#2137</a>)</li>
<li>Prevent exposing internal ip when an agent gets an internal OpenSearch exception (<a href="https://github.com/opensearch-project/ml-commons/pull/2154">#2154</a>)</li>
<li>Change the index update settings to make it only contain dynamic settings (<a href="https://github.com/opensearch-project/ml-commons/pull/2156">#2156</a>)</li>
<li>Add remote predict thread pool (<a href="https://github.com/opensearch-project/ml-commons/pull/2207">#2207</a>)</li>
<li>Add local inference enabling/disabling setting (<a href="https://github.com/opensearch-project/ml-commons/pull/2232">#2232</a>)</li>
<li>Add request level parameters for system_prompt and user_instructions (<a href="https://github.com/opensearch-project/ml-commons/pull/2236">#2236</a>)</li>
<li>Add support for Cohere and other chat model input/outputs in the RAG pipeline (<a href="https://github.com/opensearch-project/ml-commons/pull/2238">#2238</a>)</li>
</ul>

<h3>OpenSearch Neural Search</h3>

<ul>
<li>Adding aggregations in hybrid query (<a href="https://github.com/opensearch-project/neural-search/pull/630">#630</a>)</li>
</ul>
<ul>
<li>Support for post filter in hybrid query (<a href="https://github.com/opensearch-project/neural-search/pull/633">#633</a>)</li>
</ul>

<h3>OpenSearch Security</h3>

<ul>
<li>Admin role for Query insights plugin (<a href="https://github.com/opensearch-project/security/pull/4022">#4022</a>)</li>
<li>Add query assistant role and new ml system indices (<a href="https://github.com/opensearch-project/security/pull/4143">#4143</a>)</li>
<li>Redact sensitive configuration values when retrieving security configuration (<a href="https://github.com/opensearch-project/security/pull/4028">#4028</a>)</li>
<li>v2.12 update roles.yml with new API for experimental alerting plugin feature (<a href="https://github.com/opensearch-project/security/pull/4035">#4035</a>)</li>
<li>Add deprecate message that TLSv1 and TLSv1.1 support will be removed in the next major version (<a href="https://github.com/opensearch-project/security/pull/4083">#4083</a>)</li>
<li>Log password requirement details in demo environment (<a href="https://github.com/opensearch-project/security/pull/4082">#4082</a>)</li>
<li>Redact sensitive URL parameters from audit logging (<a href="https://github.com/opensearch-project/security/pull/4070">#4070</a>)</li>
<li>Fix unconsumed parameter exception when authenticating with jwtUrlParameter (<a href="https://github.com/opensearch-project/security/pull/4065">#4065</a>)</li>
<li>Regenerates root-ca, kirk and esnode certificates to address already expired root ca certificate (<a href="https://github.com/opensearch-project/security/pull/4066">#4066</a>)</li>
<li>Add exclude_roles configuration parameter to LDAP authorization backend (<a href="https://github.com/opensearch-project/security/pull/4043">#4043</a>)</li>
<li>Refactor and update existing ml roles (<a href="https://github.com/opensearch-project/security/pull/4157">#4157</a>)</li>
</ul>

<h3>OpenSearch k-NN</h3>

<ul>
<li>Optize Faiss Query With Filters: Reduce iteration and memory for id filter <a href="https://github.com/opensearch-project/k-NN/pull/1402">#1402</a></li>
<li>Detect AVX2 Dynamically on the System <a href="https://github.com/opensearch-project/k-NN/pull/1502">#1502</a></li>
<li>Validate zero vector when using cosine metric <a href="https://github.com/opensearch-project/k-NN/pull/1501">#1501</a></li>
<li>Persist model definition in model metadata [#1527] (https://github.com/opensearch-project/k-NN/pull/1527)</li>
<li>Added Inner Product Space type support for Lucene Engine <a href="https://github.com/opensearch-project/k-NN/pull/1551">#1551</a></li>
<li>Add Range Validation for Faiss SQFP16 <a href="https://github.com/opensearch-project/k-NN/pull/1493">#1493</a></li>
<li>SQFP16 Range Validation for Faiss IVF Models <a href="https://github.com/opensearch-project/k-NN/pull/1557">#1557</a></li>
</ul>

<h3>SQL</h3>

<ul>
<li>Datasource disable feature by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2539</li>
<li>Handle ALTER Index Queries. by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2554</li>
<li>Implement vacuum index operation by @dai-chen in https://github.com/opensearch-project/sql/pull/2557</li>
<li>Stop Streaming Jobs When datasource is disabled/deleted. by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2559</li>
</ul>

<h3>OpenSearch Security Dashboards Plugin</h3>

<ul>
<li>Clear the contents of opensearch_dashboards prior to putting settings (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1781">#1781</a>)</li>
<li>Add loose flag to OSD bootstrap (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1789">#1789</a>)</li>
<li>Hide tenant when disabled in the account nav button popover (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1792">#1792</a>)</li>
<li>Use start-opensearch and setup-opensearch-dashboards actions (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1808">#1808</a>)</li>
<li>Fix cookie expiry issues from IDP/JWT auth methods, disables keepalive for JWT/IDP (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1806">#1806</a>)</li>
<li>Copy tenant with Short URL (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1812">#1812</a>)</li>
<li>Add toast handling for purge cache action (<a href="https://github.com/opensearch-project/security-dashboards-plugin/pull/1827">#1827</a>)</li>
</ul>

<h2>BUG FIXES</h2>

<h3>OpenSearch Alerting</h3>

<ul>
<li>Add an <em>exists</em> check to document level monitor queries (#<a href="https://github.com/opensearch-project/alerting/pull/1425">1425</a>) (#<a href="https://github.com/opensearch-project/alerting/pull/1456">1456</a>)</li>
<li>Optimize sequence number calculation and reduce search requests in doc level monitor execution (#<a href="https://github.com/opensearch-project/alerting/pull/1455">1445</a>)</li>
<li>Clean up doc level queries on dry run (#<a href="https://github.com/opensearch-project/alerting/pull/1430">1430</a>)</li>
<li>Optimize to fetch only fields relevant to doc level queries in doc level monitor instead of entire _source for each doc #<a href="https://github.com/opensearch-project/alerting/pull/1441">1441</a></li>
<li>Add jvm aware setting and max num docs settings for batching docs for percolate queries #<a href="https://github.com/opensearch-project/alerting/pull/1435">1435</a></li>
<li>Fix for MapperException[the [enabled] parameter can't be updated for the object mapping [metadata.source_to_query_index_mapping] (#<a href="https://github.com/opensearch-project/alerting/pull/1432">1432</a>) (#<a href="https://github.com/opensearch-project/alerting/pull/1434">1434</a>)</li>
<li>Adding tracking_total_hits in search query for findings (#<a href="https://github.com/opensearch-project/alerting/pull/1487">1487</a>)</li>
</ul>

<h3>OpenSearch Flow Framework</h3>

<ul>
<li>Fixing create index and use case input parsing bugs (<a href="https://github.com/opensearch-project/flow-framework/pull/600">#600</a>)</li>
</ul>

<h3>OpenSearch Geospatial</h3>

<ul>
<li>Adjusted dependency versions to address CVEs (<a href="https://github.com/opensearch-project/geospatial/pull/635">#635</a>)</li>
</ul>

<h3>OpenSearch Index Management</h3>

<ul>
<li>Fix Typo in Alias Message (<a href="https://github.com/opensearch-project/index-management/pull/1137">#1137</a>)</li>
</ul>

<h3>OpenSearch ML Commons</h3>

<ul>
<li>Fix error code when executing agent (<a href="https://github.com/opensearch-project/ml-commons/pull/2120">#2120</a>)</li>
<li>Fix npe when executing agent with empty parameter (<a href="https://github.com/opensearch-project/ml-commons/pull/2145">#2145</a>)</li>
<li>Fix delete model cache on macOS causing model deploy fail with model (<a href="https://github.com/opensearch-project/ml-commons/pull/2180">#2180</a>)</li>
<li>Adding BWC for connector config field (<a href="https://github.com/opensearch-project/ml-commons/pull/2184">#2184</a>)</li>
<li>Fix onnx dep (<a href="https://github.com/opensearch-project/ml-commons/pull/2198">#2198</a>)</li>
<li>Update the response code to 404 when deleting a memory (<a href="https://github.com/opensearch-project/ml-commons/pull/2212">#2212</a>)</li>
<li>Fix model enable flag not loading (<a href="https://github.com/opensearch-project/ml-commons/pull/2221">#2221</a>)</li>
<li>Updating ml_connector schema version (<a href="https://github.com/opensearch-project/ml-commons/pull/2228">#2228</a>)</li>
<li>Fix json error (<a href="https://github.com/opensearch-project/ml-commons/pull/2234">#2234</a>)</li>
<li>Update remote model auto deploy tests in predict runner (<a href="https://github.com/opensearch-project/ml-commons/pull/2237">#2237</a>)</li>
</ul>

<h3>OpenSearch Neural Search</h3>

<ul>
<li>Fix typo for sparse encoding processor factory(<a href="https://github.com/opensearch-project/neural-search/pull/600">#600</a>)</li>
</ul>
<ul>
<li>Add non-null check for queryBuilder in NeuralQueryEnricherProcessor (<a href="https://github.com/opensearch-project/neural-search/pull/619">#619</a>)</li>
<li>Fix runtime exceptions in hybrid query for case when sub-query scorer return TwoPhase iterator that is incompatible with DISI iterator (<a href="https://github.com/opensearch-project/neural-search/pull/624">#624</a>)</li>
</ul>

<h3>OpenSearch Notifications</h3>

<ul>
<li>Adding hostname support for notifications deny list (#<a href="https://github.com/opensearch-project/notifications/pull/858">858</a>) (#<a href="https://github.com/opensearch-project/notifications/pull/860">860</a>)</li>
</ul>

<h3>OpenSearch Security Analytics</h3>

<ul>
<li>Fix get mappings view API incorrectly returning ecs path (#<a href="https://github.com/opensearch-project/security-analytics/pull/867">867</a>) (#<a href="https://github.com/opensearch-project/security-analytics/pull/905">905</a>) (#<a href="https://github.com/opensearch-project/security-analytics/issues/866">866</a>)</li>
<li>Add an &quot;exists&quot; check for &quot;not&quot; condition in sigma rules (#<a href="https://github.com/opensearch-project/security-analytics/pull/852">852</a>) (#<a href="https://github.com/opensearch-project/security-analytics/pull/897">897</a>)</li>
<li>Fix duplicate ecs mappings which returns incorrect log index field in mapping view API (#<a href="https://github.com/opensearch-project/security-analytics/pull/786">786</a>) (#<a href="https://github.com/opensearch-project/security-analytics/pull/788">788</a>) (#<a href="https://github.com/opensearch-project/security-analytics/pull/898">898</a>)</li>
<li>ArrayIndexOutOfBoundsException for inconsistent detector index behavior (#<a href="https://github.com/opensearch-project/security-analytics/pull/843">843</a>) (#<a href="https://github.com/opensearch-project/security-analytics/pull/852">858</a>)</li>
<li>Fail the flow when detector type is missing in the log types index (#<a href="https://github.com/opensearch-project/security-analytics/pull/845">845</a>) (#<a href="https://github.com/opensearch-project/security-analytics/pull/857">857</a>)</li>
<li>Remove blocking calls and change threat intel feed flow to event driven (#<a href="https://github.com/opensearch-project/security-analytics/pull/871">871</a>) (#<a href="https://github.com/opensearch-project/security-analytics/pull/876">876</a>)</li>
<li>Fixes OCSF integ test (#<a href="https://github.com/opensearch-project/security-analytics/pull/918">918</a>)</li>
<li>Pass rule field names in doc level queries during monitor/creation. Remove blocking actionGet() calls (#<a href="https://github.com/opensearch-project/security-analytics/pull/873">873</a>)</li>
<li>Add search request timeouts for correlations workflows (#<a href="https://github.com/opensearch-project/security-analytics/pull/893">893</a>) (#<a href="https://github.com/opensearch-project/security-analytics/pull/893">901</a>) (#<a href="https://github.com/opensearch-project/security-analytics/issues/879">879</a>])</li>
</ul>

<h3>OpenSearch k-NN</h3>

<ul>
<li>Disable sdc table for HNSWPQ read-only indices <a href="https://github.com/opensearch-project/k-NN/pull/1518">#1518</a></li>
<li>Switch SpaceType.INNERPRODUCT's vector similarity function to MAXIMUM_INNER_PRODUCT <a href="https://github.com/opensearch-project/k-NN/pull/1532">#1532</a></li>
<li>Add patch to fix arm segfault in nmslib during ingestion <a href="https://github.com/opensearch-project/k-NN/pull/1541">#1541</a></li>
<li>Share ivfpq-l2 table allocations across indices on load <a href="https://github.com/opensearch-project/k-NN/pull/1558">#1558</a></li>
</ul>

<h3>SQL</h3>

<ul>
<li>Fix issue in testSourceMetricCommandWithTimestamp integ test with different timezones and locales. by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2522</li>
<li>Refactor query param by @noCharger in https://github.com/opensearch-project/sql/pull/2519</li>
<li>Restrict the scope of cancel API by @penghuo in https://github.com/opensearch-project/sql/pull/2548</li>
<li>Change async query default setting by @penghuo in https://github.com/opensearch-project/sql/pull/2561</li>
<li>Percent encode opensearch index name by @seankao-az in https://github.com/opensearch-project/sql/pull/2564</li>
<li>[Bugfix] Wrap the query with double quotes by @noCharger in https://github.com/opensearch-project/sql/pull/2565</li>
<li>FlintStreamingJobCleanerTask missing event listener by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2574</li>
</ul>

<h3>Dashboards Observability</h3>

<ul>
<li>Update integrations to allow custom checkpoint locations (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1501">#1501</a>)</li>
<li>(query assist) show error toasts if summary is disabled (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1480">#1480</a>)</li>
<li>Fixing style overriding issue in dashboards core vizBuilder (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1451">#1451</a>)</li>
<li>Fix jaeger spans key names for filtering (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1428">#1428</a>)</li>
</ul>

<h3>Dashboards Assistant</h3>

<ul>
<li>Integrate chatbot with sidecar service. (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/164">#164</a>)</li>
<li>Update view trace button from suggestions to message action bar. (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/158">#158</a>)</li>
<li>Fetch root agent id before executing the agent. (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/165">#165</a>)</li>
<li>Encode id if it is used in request path. (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/174">#174</a>)</li>
</ul>

<h3>OpenSearch Alerting Dashboards Plugin</h3>

<ul>
<li>Fix fetching of channels for composite monitors (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/820">#820</a>)</li>
<li>Fix error to disblay monitors with disable/enable state (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/869">#869</a>)</li>
</ul>

<h3>OpenSearch Dashboards Reporting</h3>

<ul>
<li>Reporting is missing from the navigation menu (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/295">#295</a>)</li>
<li>Allow negative signs in duration(<a href="https://github.com/opensearch-project/dashboards-reporting/pull/284">#284</a>)</li>
<li>Fix condition to determine if the date field's value is an array (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/299">#299</a>)</li>
<li>Fix menu cut off (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/315">#315</a>)</li>
</ul>

<h3>OpenSearch Query Workbench</h3>

<ul>
<li>Refactor async calls and minor bug fixes (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/274">#274</a>)</li>
<li>Add empty tree state for SQL sidebar (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/292">#292</a>)</li>
<li>Catch no database found errors from cache manager (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/296">#296</a>)</li>
</ul>

<h3>OpenSearch Security Analytics Dashboards</h3>

<ul>
<li>Added more mime types for yaml file (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/909">#909</a>)</li>
<li>Load log type from log source if present (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/894">#894</a>)</li>
<li>Update actions menu after start/stop detector action for the selected detector (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/895">#895</a>)</li>
<li>Loading spinner added; fixed copied popup (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/904">#904</a>)</li>
<li>Fixed view surrounding logs for aliases (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/906">#906</a>)</li>
<li>Fetching channel types using API; updated type imports (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/919">#919</a>)</li>
<li>Fixed UI for setting alert severity (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/920">#920</a>)</li>
<li>Do not filter timestamp field from required mappings when at least one rule is selected (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/925">#925</a>)</li>
<li>Fixed create button staying in submit state on review config (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/926">#926</a>)</li>
<li>Don't show index-pattern creation form once created (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/927">#927</a>)</li>
<li>Fixed logic to get all alerts for a detector (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/965">#965</a>)</li>
</ul>

<h2>INFRASTRUCTURE</h2>

<h3>OpenSearch Anomaly Detection</h3>

<ul>
<li>Fixed lucene url (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1158">#1158</a>)</li>
</ul>

<h3>OpenSearch ML Commons</h3>

<ul>
<li>Add integration tests for the RAG pipeline covering OpenAI and Bedrock (<a href="https://github.com/opensearch-project/ml-commons/pull/2213">#2213</a>)</li>
</ul>

<h3>OpenSearch k-NN</h3>

<ul>
<li>Manually install zlib for win CI <a href="https://github.com/opensearch-project/k-NN/pull/1513">#1513</a></li>
<li>Update k-NN build artifact script to enable SIMD on ARM for Faiss <a href="https://github.com/opensearch-project/k-NN/pull/1543">#1543</a></li>
</ul>

<h3>SQL</h3>

<ul>
<li>Bump bwc version by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2546</li>
<li>[Backport main] Add release notes for 1.3.15 by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/2538</li>
<li>Upgrade opensearch-spark jars to 0.3.0 by @noCharger in https://github.com/opensearch-project/sql/pull/2568</li>
</ul>

<h3>Dashboards Assistant</h3>

<ul>
<li>Add new workflow to verify binary install. (<a href="https://github.com/opensearch-project/dashboards-assistant/pull/159">#159</a>)</li>
</ul>

<h3>Dashboards Observability</h3>

<ul>
<li>Add single version flag during bootstrap to fix version conflicts (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1460">#1460</a>)</li>
</ul>

<h3>OpenSearch Dashboards Reporting</h3>

<ul>
<li>Add single version flag during bootstrap to fix version conflicts(<a href="https://github.com/opensearch-project/dashboards-reporting/pull/303">#303</a>)</li>
<li>Add workflow to verify binary installation is successful  (<a href="https://github.com/opensearch-project/dashboards-reporting/pull/313">#313</a>)</li>
</ul>

<h3>OpenSearch Dashboards Search Relevance</h3>

<ul>
<li>Add workflow to verify binary installation (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/373">#373</a>) (<a href="https://github.com/opensearch-project/dashboards-search-relevance/pull/375">#375</a>)</li>
</ul>

<h3>OpenSearch Dashboards Visualizations</h3>

<ul>
<li>Add workflow to verify binary installation (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/347">#347</a>)</li>
</ul>
<ul>
<li>[CI/CD] Add single version flag during bootstrap to fix version conflicts (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/341">#341</a>)</li>
</ul>

<h3>OpenSearch ML Commonss Dashboards</h3>

<ul>
<li>Add new workflow to verify binary install. (<a href="https://github.com/opensearch-project/ml-commons-dashboards/pull/306">#306</a>)</li>
</ul>

<h3>OpenSearch Query Workbench</h3>

<ul>
<li>Add single version flag during bootstrap to fix version conflicts (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/269">#269</a>)</li>
</ul>
<ul>
<li>Add OSD react as required plugin (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/278">#278</a>)</li>
</ul>

<h3>OpenSearch Security Analytics Dashboards</h3>

<ul>
<li>Updated cypress version to match core OSD (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/907">#907</a>)</li>
</ul>

<h3> OpenSearch Build </h3>

<ul>
<li>Fix default config permissions for RPM and Debian Packages (<a href="https://github.com/opensearch-project/opensearch-build/issues/3815">#3815</a>)</li>
<li>Allow automatically restarting of OpenSearch and OpenSearch-Dashboards Service after upgrading the Debian package (<a href="https://github.com/opensearch-project/opensearch-build/pull/4530">#4530</a>)</li>
</ul>

<h2>DOCUMENTATION</h2>

<h3>OpenSearch Alerting</h3>

<ul>
<li>Added 2.13 release notes (#<a href="https://github.com/opensearch-project/alerting/pull/1483">1483</a>)</li>
</ul>

<h3>OpenSearch Common Utils</h3>

<ul>
<li>Added 2.13.0.0 release notes (<a href="https://github.com/opensearch-project/common-utils/pull/622">#622</a>)</li>
</ul>

<h3>OpenSearch Index Management</h3>

<ul>
<li>Version 2.13 Release Notes Draft (<a href="https://github.com/opensearch-project/index-management/pull/1142">#1142</a>)</li>
</ul>

<h3>OpenSearch ML Commons</h3>

<ul>
<li>Add Cohere Chat blueprint with RAG (<a href="https://github.com/opensearch-project/ml-commons/pull/1991">#1991</a>)</li>
<li>Add tutorial for semantic search with byte quantized vector and Cohere embedding model (<a href="https://github.com/opensearch-project/ml-commons/pull/2127">#2127</a>)</li>
<li>Add tutorial for rerank pipeline with Cohere rerank model (<a href="https://github.com/opensearch-project/ml-commons/pull/2134">#2134</a>)</li>
<li>Add tutorial for chatbot with rag (<a href="https://github.com/opensearch-project/ml-commons/pull/2141">#2141</a>)</li>
<li>Add tutorial for building your own chatbot (<a href="https://github.com/opensearch-project/ml-commons/pull/2144">#2144</a>)</li>
<li>Add tutorial for CFN template integration (<a href="https://github.com/opensearch-project/ml-commons/pull/2161">#2161</a>)</li>
<li>Fix cohere chat blueprint (<a href="https://github.com/opensearch-project/ml-commons/pull/2167">#2167</a>)</li>
<li>Add demo notebook for creating connector (<a href="https://github.com/opensearch-project/ml-commons/pull/2192">#2192</a>)</li>
<li>Enhance connector helper notebook to support 2.9 (<a href="https://github.com/opensearch-project/ml-commons/pull/2202">#2202</a>)</li>
</ul>

<h3>OpenSearch Notifications</h3>

<ul>
<li>Add 2.13.0 release notes (#<a href="https://github.com/opensearch-project/notifications/pull/878">878</a>)</li>
</ul>

<h3>OpenSearch Security Analytics</h3>

<ul>
<li>Added 2.13.0 release notes (#<a href="https://github.com/opensearch-project/security-analytics/pull/945">945</a>)</li>
</ul>

<h3>OpenSearch Alerting Dashboards Plugin</h3>

<ul>
<li>Added 2.13 release notes. (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/904">#904</a>)</li>
</ul>

<h3>OpenSearch Dashboards Maps</h3>

<ul>
<li>Update data layer source name <a href="https://github.com/opensearch-project/dashboards-maps/pull/588">#588</a></li>
</ul>

<h3>OpenSearch Dashboards Notifications</h3>

<ul>
<li>Added 2.13.0 release notes. (<a href="https://github.com/opensearch-project/dashboards-notifications/pull/173">#173</a>)</li>
</ul>

<h3>OpenSearch Index Management Dashboards Plugin</h3>

<ul>
<li>Version 2.13 Release Notes Draft (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1012">#1012</a>)</li>
</ul>

<h3>OpenSearch Security Analytics Dashboards</h3>

<ul>
<li>Added release notes for 2.13.0 (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/959">#959</a>)</li>
<li>Updated release notes for 2.13.0 (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/968">#968</a>)</li>
</ul>

<h2>MAINTENANCE</h2>

<h3>OpenSearch Alerting</h3>

<ul>
<li>Bump up the version to 2.13 (#<a href="https://github.com/opensearch-project/alerting/pull/1460">1460</a>)</li>
</ul>

<h3>OpenSearch Anomaly Detection</h3>

<ul>
<li>Increment version to 2.13.0-SNAPSHOT (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1156">#1156</a>)</li>
</ul>

<h3>OpenSearch Asynchronous Search</h3>

<ul>
<li>Increment version to 2.13.0 (<a href="https://github.com/opensearch-project/asynchronous-search/pull/544">#544</a>)</li>
</ul>

<h3>OpenSearch Common Utils</h3>

<ul>
<li>Increment version to 2.13.0-SNAPSHOT (<a href="https://github.com/opensearch-project/common-utils/pull/591">#591</a>)</li>
</ul>

<h3>OpenSearch Index Management</h3>

<ul>
<li>Increment version to 2.13.0-SNAPSHOT. (<a href="https://github.com/opensearch-project/index-management/pull/1096">#1096</a>)</li>
<li>Upgrade com.github.seancfoley:ipaddress to mitigate CVE-2023-50570  (<a href="https://github.com/opensearch-project/index-management/pull/1126">#1126</a>)</li>
<li>Updates demo certs and admin keystore (<a href="https://github.com/opensearch-project/index-management/pull/1116">#1116</a>)</li>
</ul>

<h3>OpenSearch Job Scheduler</h3>

<ul>
<li>Increment version to 2.13.0 (<a href="https://github.com/opensearch-project/job-scheduler/pull/575">#575</a>)</li>
<li>Spotless plugin remove apply false (<a href="https://github.com/opensearch-project/job-scheduler/pull/590">#590</a>) <a href="https://github.com/opensearch-project/job-scheduler/pull/591">(#591)</a></li>
<li>dependabot: bump com.google.googlejavaformat:google-java-format <a href="https://github.com/opensearch-project/job-scheduler/pull/596">(#596)</a> <a href="https://github.com/opensearch-project/job-scheduler/pull/597">(#597)</a></li>
<li>dependabot: bump com.netflix.nebula.ospackage from 11.8.0 to 11.8.1 <a href="https://github.com/opensearch-project/job-scheduler/pull/593">(#593)</a> <a href="https://github.com/opensearch-project/job-scheduler/pull/598">(#598)</a></li>
<li>dependabot: bump org.slf4j:slf4j-api from 2.0.11 to 2.0.12 <a href="https://github.com/opensearch-project/job-scheduler/pull/587">(#587)</a> <a href="https://github.com/opensearch-project/job-scheduler/pull/599">(#599)</a></li>
</ul>

<h3>OpenSearch ML Commons</h3>

<ul>
<li>Updates sample cert and admin keystore (<a href="https://github.com/opensearch-project/ml-commons/pull/2143">#2143</a>)</li>
<li>Bump common-compress package to fix CVE (<a href="https://github.com/opensearch-project/ml-commons/pull/2186">#2186</a>)</li>
<li>Suppress removal AccessController in java.security has been deprecated and marked for removal (<a href="https://github.com/opensearch-project/ml-commons/pull/2195">#2195</a>)</li>
</ul>

<h3>OpenSearch Notifications</h3>

<ul>
<li>Bump up the version to 2.13 (#<a href="https://github.com/opensearch-project/notifications/pull/873">873</a>)</li>
</ul>

<h3>OpenSearch Observability</h3>

<ul>
<li>Increment version to 2.13.0-SNAPSHOT (<a href="https://github.com/opensearch-project/observability/pull/1796">#1796</a>)</li>
</ul>

<h3>OpenSearch Security</h3>

<ul>
<li>Add exlusion for logback-core to resolve CVE-2023-6378 (<a href="https://github.com/opensearch-project/security/pull/4050">#4050</a>)</li>
<li>Bump com.netflix.nebula.ospackage from 11.7.0 to 11.8.1 (<a href="https://github.com/opensearch-project/security/pull/4041">#4041</a>, <a href="https://github.com/opensearch-project/security/pull/4075">#4075</a>)</li>
<li>Bump Wandalen/wretry.action from 1.3.0 to 1.4.10 (<a href="https://github.com/opensearch-project/security/pull/4042">#4042</a>, <a href="https://github.com/opensearch-project/security/pull/4092">#4092</a>, <a href="https://github.com/opensearch-project/security/pull/4108">#4108</a>, <a href="https://github.com/opensearch-project/security/pull/4135">#4135</a>)</li>
<li>Bump spring_version from 5.3.31 to 5.3.33 (<a href="https://github.com/opensearch-project/security/pull/4058">#4058</a>, <a href="https://github.com/opensearch-project/security/pull/4131">#4131</a>)</li>
<li>Bump org.scala-lang:scala-library from 2.13.12 to 2.13.13 (<a href="https://github.com/opensearch-project/security/pull/4076">#4076</a>)</li>
<li>Bump com.google.googlejavaformat:google-java-format from 1.19.1 to 1.21.0 (<a href="https://github.com/opensearch-project/security/pull/4078">#4078</a>, <a href="https://github.com/opensearch-project/security/pull/4110">#4110</a>)</li>
<li>Bump ch.qos.logback:logback-classic from 1.2.13 to 1.5.3 (<a href="https://github.com/opensearch-project/security/pull/4091">#4091</a>, <a href="https://github.com/opensearch-project/security/pull/4111">#4111</a>)</li>
<li>Bump com.fasterxml.woodstox:woodstox-core from 6.6.0 to 6.6.1 (<a href="https://github.com/opensearch-project/security/pull/4093">#4093</a>)</li>
<li>Bump kafka_version from 3.5.1 to 3.7.0 (<a href="https://github.com/opensearch-project/security/pull/4095">#4095</a>)</li>
<li>Bump jakarta.xml.bind:jakarta.xml.bind-api from 4.0.1 to 4.0.2 (<a href="https://github.com/opensearch-project/security/pull/4109">#4109</a>)</li>
<li>Bump org.apache.zookeeper:zookeeper from 3.9.1. to 3.9.2 (<a href="https://github.com/opensearch-project/security/pull/4130">#4130</a>)</li>
<li>Bump org.awaitility:awaitility from 4.2.0 to 4.2.1 (<a href="https://github.com/opensearch-project/security/pull/4133">#4133</a>)</li>
<li>Bump com.google.errorprone:error_prone_annotations from 2.25.0 to 2.26.1 (<a href="https://github.com/opensearch-project/security/pull/4132">#4132</a>)</li>
</ul>

<h3>OpenSearch Skills</h3>
<ul>
<li>Update mockito monorepo to v5.10.0 (#128) (#197)</li>
<li>Update dependency org.apache.commons:commons-lang3 to v3.14.0 (#47)</li>
<li>Update dependency org.apache.commons:commons-text to v1.11.0 (#62)</li>
<li>Update plugin io.freefair.lombok to v8.6 (#245) (#249)</li>
<li>Update plugin de.undercouch.download to v5.6.0 (#239) (#250)</li>
<li>Update plugin com.diffplug.spotless to v6.25.0 (#127) (#252)</li>
<li>Update dependency org.json:json to v20240205 (#246) (#251)</li>
</ul>

<h3>OpenSearch Security Analytics</h3>

<ul>
<li>Increment to 2.13. (<a href="https://github.com/opensearch-project/security-analytics/pull/913">#913</a>)</li>
<li>Add goyamegh as a maintainer (#<a href="https://github.com/opensearch-project/security-analytics/pull/868">868</a>) (#<a href="https://github.com/opensearch-project/security-analytics/pull/899">899</a>)</li>
</ul>

<h3>OpenSearch k-NN</h3>

<ul>
<li>Bump faiss lib commit to 32f0e8cf92cd2275b60364517bb1cce67aa29a55 <a href="https://github.com/opensearch-project/k-NN/pull/1443">#1443</a></li>
<li>Fix FieldInfo Parameters Mismatch <a href="https://github.com/opensearch-project/k-NN/pull/1490">#1490</a></li>
<li>Upgrade faiss to 12b92e9 <a href="https://github.com/opensearch-project/k-NN/pull/1509">#1509</a></li>
</ul>

<h3>SQL</h3>

<ul>
<li>Bump ipaddress to 5.4.2 by @joshuali925 in https://github.com/opensearch-project/sql/pull/2544</li>
</ul>
<hr />

<h3>Dashboards Observability</h3>

<ul>
<li>Copy Updates: Integration Flows -&gt; Integration Resources (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1555">#1555</a>)</li>
<li>Update UI styles for query assist (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1523">#1523</a>)</li>
<li>Move create acceleration flyout from workbench to datasources (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1508">#1508</a>)</li>
<li>Minor integration name updates (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1505">#1505</a>)</li>
<li>Update integration format for better handling of multiple asset types (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1502">#1502</a>)</li>
<li>Update names and descriptions for integrations (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1499">#1499</a>)</li>
<li>(query assist) get agent id through config API (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1482">#1482</a>)</li>
<li>Changed Explorer Data Grid useage of timestamp (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1479">#1479</a>)</li>
<li>Flint bug fix explorer failure (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1476">#1476</a>)</li>
<li>Fixing Flaky Panels Test (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1463">#1463</a>)</li>
<li>Remove hardcoded width for generate ppl button (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1447">#1447</a>)</li>
<li>Upgrade plotly to v2 (<a href="https://github.com/opensearch-project/dashboards-observability/pull/1432">#1432</a>)</li>
</ul>

<h3>OpenSearch Alerting Dashboards Plugin</h3>

<ul>
<li>Increment version to 2.13.0.0 (<a href="https://github.com/opensearch-project/alerting-dashboards-plugin/pull/892">#892</a>)</li>
</ul>

<h3>OpenSearch Anomaly Detection Dashboards</h3>

<ul>
<li>Increment version to 2.13.0.0 (<a href="https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/695">#695</a>)</li>
</ul>

<h3>OpenSearch Dashboards Notifications</h3>

<ul>
<li>Update snapshot. (<a href="https://github.com/opensearch-project/dashboards-notifications/pull/168">#168</a>)</li>
</ul>

<h3>OpenSearch Dashboards Visualizations</h3>

<ul>
<li>Upgrade plotly to v2 (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/336">#336</a>)</li>
</ul>
<ul>
<li>Increment version to 2.13.0.0 (<a href="https://github.com/opensearch-project/dashboards-visualizations/pull/348">#348</a>)</li>
</ul>

<h3>OpenSearch Index Management Dashboards Plugin</h3>

<ul>
<li>Increment version to 2.13.0.0. (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1000">#1000</a>)</li>
<li>CVE fixes for CVE-2022-38900, CVE-2021-3807, CVE-2021-43138, CVE-2022-25858, CVE-2022-37603, CVE-2023-26136, CVE-2022-37599, CVE-2022-37601 (<a href="https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1008">#1008</a>)</li>
</ul>

<h3>OpenSearch ML Commonss Dashboards</h3>

<ul>
<li>Increment version to 2.13.0.0 (<a href="https://github.com/opensearch-project/ml-commons-dashboards/pull/307">#307</a>)</li>
</ul>

<h3>OpenSearch Query Workbench</h3>

<ul>
<li>Add workflow to verify binary install (<a href="https://github.com/opensearch-project/dashboards-query-workbench/pull/272">#272</a>)</li>
</ul>

<h3>OpenSearch Security Analytics Dashboards</h3>

<ul>
<li>Added riysaxen-amzn as a maintainer (<a href="https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/898">#898</a>)</li>
</ul>

<h2>REFACTORING</h2>

<h3>OpenSearch Flow Framework</h3>

<ul>
<li>Moved workflow-steps.json to Enum (<a href="https://github.com/opensearch-project/flow-framework/pull/523">#523</a>)</li>
<li>Refactored logging for consistency (<a href="https://github.com/opensearch-project/flow-framework/pull/524">#524</a>)</li>
</ul>

<h3>OpenSearch ML Commons</h3>

<ul>
<li>Refactor memory logs (<a href="https://github.com/opensearch-project/ml-commons/pull/2121">#2121</a>)</li>
<li>Parse tool input to map (<a href="https://github.com/opensearch-project/ml-commons/pull/2131">#2131</a>)</li>
</ul>

<h3>OpenSearch Security Analytics</h3>

<ul>
<li>Refactor invocation of Action listeners in correlations (#<a href="https://github.com/opensearch-project/security-analytics/issues/879">880</a>) (#<a href="https://github.com/opensearch-project/security-analytics/issues/879">900</a>) (#<a href="https://github.com/opensearch-project/security-analytics/issues/879">879</a>])</li>
</ul>

<h3>SQL</h3>

<ul>
<li>Change emr job names based on the query type by @vamsi-amazon in https://github.com/opensearch-project/sql/pull/2543</li>
</ul>
