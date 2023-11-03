<h1>OpenSearch and OpenSearch Dashboards 2.9.0 Release Notes</h1>
<h2>FEATURES</h2>

<h3>Opensearch Knn</h3>

<ul>
<li>Added support for Efficient Pre-filtering for Faiss Engine (<a href="https://github.com/opensearch-project/k-NN/pull/936">#936</a>)</li>
<li>Add Support for Lucene Byte Sized Vector (<a href="https://github.com/opensearch-project/k-NN/pull/971">#971</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Adds Chained alerts triggers for workflows. (<a href="https://github.com/opensearch-project/common-utils/pull/456">#456</a>)</li>
<li>Acknowledge chained alert request for workflow. (<a href="https://github.com/opensearch-project/common-utils/pull/459">#459</a>)</li>
<li>Adds audit state in Alert. (<a href="https://github.com/opensearch-project/common-utils/pull/461">#461</a>)</li>
<li>Add workflowId field in alert. ((<a href="https://github.com/opensearch-project/common-utils/pull/463">#463</a>)</li>
<li>APIs for get workflow alerts and acknowledge chained alerts. (<a href="https://github.com/opensearch-project/common-utils/pull/472">#472</a>)</li>
<li>Add auditDelegateMonitorAlerts flag. (<a href="https://github.com/opensearch-project/common-utils/pull/476">#476</a>)</li>
<li>Implemented support for configuring a cluster metrics monitor to call cat/indices, and cat/shards. (<a href="https://github.com/opensearch-project/common-utils/pull/479">#479</a>)</li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Enable Table Function and PromQL function (<a href="https://github.com/opensearch-project/sql/pull/1719">#1719</a>)</li>
<li>Add spark connector (<a href="https://github.com/opensearch-project/sql/pull/1780">#1780</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Adds transport layer actions for CRUD workflows. (<a href="https://github.com/opensearch-project/alerting/pull/934">#934</a>)</li>
<li>Added rest layer for the workflow. (<a href="https://github.com/opensearch-project/alerting/pull/963">#963</a>)</li>
<li>[BucketLevelMonitor] Multi-term agg support. (<a href="https://github.com/opensearch-project/alerting/pull/964">#964</a>)</li>
<li>Check if AD backend role is enabled. (<a href="https://github.com/opensearch-project/alerting/pull/968">#968</a>)</li>
<li>Add workflow_id field in alert mapping json. (<a href="https://github.com/opensearch-project/alerting/pull/969">#969</a>)</li>
<li>Adds chained alerts. (<a href="https://github.com/opensearch-project/alerting/pull/976">#976</a>)</li>
<li>Implemented support for configuring a cluster metrics monitor to call cat/indices, and cat/shards. (<a href="https://github.com/opensearch-project/alerting/pull/992">#992</a>)</li>
</ul>

<h3>Opensearch Ml Common</h3>

<ul>
<li>remote inference: add connector; fine tune ML model and tensor class (<a href="https://github.com/opensearch-project/ml-commons/pull/1051">#1051</a>)</li>
<li>remote inference: add connector executor (<a href="https://github.com/opensearch-project/ml-commons/pull/1052">#1052</a>)</li>
<li>connector transport actions, requests and responses (<a href="https://github.com/opensearch-project/ml-commons/pull/1053">#1053</a>)</li>
<li>refactor predictable: add method to check if model is ready (<a href="https://github.com/opensearch-project/ml-commons/pull/1057">#1057</a>)</li>
<li>Add basic connector access control classes (<a href="https://github.com/opensearch-project/ml-commons/pull/1055">#1055</a>)</li>
<li>connector transport actions and disable native memory CB (<a href="https://github.com/opensearch-project/ml-commons/pull/1056">#1056</a>)</li>
<li>restful connector actions and UT (<a href="https://github.com/opensearch-project/ml-commons/pull/1065">#1065</a>)</li>
<li>Change connector access control creation allow empty list (<a href="https://github.com/opensearch-project/ml-commons/pull/1069">#1069</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>New Log Type JSON format. (<a href="https://github.com/opensearch-project/security-analytics/pull/465">#465</a>)</li>
<li>Correlation rule search, delete and edit API. (<a href="https://github.com/opensearch-project/security-analytics/pull/476">#476</a>)</li>
<li>Logtypes PR v2. (<a href="https://github.com/opensearch-project/security-analytics/pull/482">#482</a>)</li>
</ul>

<h2>ENHANCEMENTS</h2>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Remove heap allocation rate as the input metric to HotShardClusterRca <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/411">#411</a></li>
<li>Set ThreadMetricsRca evaluation period from 12 seconds to 5 seconds <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/410">#410</a></li>
<li>Add unit tests for the REST layer in RCA Agent <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/436">#436</a></li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Pagination: Support WHERE clause, column list in SELECT clause and for functions and expressions in the query (<a href="https://github.com/opensearch-project/sql/pull/1500">#1500</a>)</li>
<li>Pagination: Support ORDER BY clauses and queries without FROM clause (<a href="https://github.com/opensearch-project/sql/pull/1599">#1599</a>)</li>
<li>Remove backticks on by field in stats (<a href="https://github.com/opensearch-project/sql/pull/1728">#1728</a>)</li>
<li>Support Array and ExprValue Parsing With Inner Hits (<a href="https://github.com/opensearch-project/sql/pull/1737">#1737</a>)</li>
<li>Add Support for Nested Function in Order By Clause (<a href="https://github.com/opensearch-project/sql/pull/1789">#1789</a>)</li>
<li>Add Support for Field Star in Nested Function (<a href="https://github.com/opensearch-project/sql/pull/1773">#1773</a>)</li>
<li>Guarantee datasource read api is strong consistent read (compatibility with segment replication) (<a href="https://github.com/opensearch-project/sql/pull/1815">#1815</a>)</li>
<li>Added new datetime functions and aliases to PPL (<a href="https://github.com/opensearch-project/sql/pull/1807">#1807</a>)</li>
<li>Support user-defined and incomplete date formats (<a href="https://github.com/opensearch-project/sql/pull/1821">#1821</a>)</li>
<li>Add _routing to SQL includes list (<a href="https://github.com/opensearch-project/sql/pull/1771">#1771</a>)</li>
<li>Disable read of plugins.query.datasources.encryption.masterkey from cluster settings GET API (<a href="https://github.com/opensearch-project/sql/pull/1825">#1825</a>)</li>
<li>Add EMR client to spark connector (<a href="https://github.com/opensearch-project/sql/pull/1790">#1790</a>)</li>
<li>Improved error codes in case of data sourcde API security exception (<a href="https://github.com/opensearch-project/sql/pull/1753">#1753</a>)</li>
<li>Remove Default master encryption key from settings (<a href="https://github.com/opensearch-project/sql/pull/1851">#1851</a>)</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Enforce DOCUMENT Replication for AD Indices and Adjust Primary Shards (<a href="https://github.com/opensearch-project/anomaly-detection/pull/948">#948</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Use boucycastle PEM reader instead of reg expression (<a href="https://github.com/opensearch-project/security/pull/2877">#2877</a>)</li>
<li>Adding field level security test cases for FlatFields (<a href="https://github.com/opensearch-project/security/pull/2876">#2876</a>) (<a href="https://github.com/opensearch-project/security/pull/2893">#2893</a>)</li>
<li>Add password message to /dashboardsinfo endpoint (<a href="https://github.com/opensearch-project/security/pull/2949">#2949</a>) (<a href="https://github.com/opensearch-project/security/pull/2955">#2955</a>)</li>
<li>Add .plugins-ml-connector to system index (<a href="https://github.com/opensearch-project/security/pull/2947">#2947</a>) (<a href="https://github.com/opensearch-project/security/pull/2954">#2954</a>)</li>
<li>Parallel test jobs for CI (<a href="https://github.com/opensearch-project/security/pull/2861">#2861</a>) (<a href="https://github.com/opensearch-project/security/pull/2936">#2936</a>)</li>
<li>Adds a check to skip serialization-deserialization if request is for same node (<a href="https://github.com/opensearch-project/security/pull/2765">#2765</a>) (<a href="https://github.com/opensearch-project/security/pull/2973">#2973</a>)</li>
<li>Add workflow cluster permissions to alerting roles and add .plugins-ml-config in the system index (<a href="https://github.com/opensearch-project/security/pull/2996">#2996</a>)</li>
</ul>

<h3>Opensearch Ml Common</h3>

<ul>
<li>create model group automatically with first model version (<a href="https://github.com/opensearch-project/ml-commons/pull/1063">#1063</a>)</li>
<li>init master key automatically (<a href="https://github.com/opensearch-project/ml-commons/pull/1075">#1075</a>))</li>
</ul>

<h2>BUG FIXES</h2>

<h3>Opensearch Neural Search</h3>

<h3>Bug Fixes</h3>
<p>Fix update document with knnn_vector size not matching issue (<a href="https://github.com/opensearch-project/neural-search/pull/208">#208</a>)</p>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Fix NPE issue in ShardStateCollector, which was impacted by changes from upstream core <a href="https://github.com/opensearch-project/performance-analyzer/pull/489">#489</a></li>
<li>Fix Mockito initialization issue <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/443">#443</a></li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>OpenSearch commons strings library dependency import. (<a href="https://github.com/opensearch-project/common-utils/pull/474">#474</a>)</li>
</ul>

<h3>Opensearch Reporting</h3>

<ul>
<li>Removing guava dependency to fix jarhell (<a href="https://github.com/opensearch-project/reporting/pull/709">#709</a>)</li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Fixed bug of byte/short not handling 0 denominator in divide/modulus equations (<a href="https://github.com/opensearch-project/sql/pull/1716">#1716</a>)</li>
<li>Fix CSV/RAW output header being application/json rather than plain/text (<a href="https://github.com/opensearch-project/sql/pull/1779">#1779</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Fix schema version in tests and delegate monitor metadata construction in tests. (<a href="https://github.com/opensearch-project/alerting/pull/948">#948</a>)</li>
<li>Fixed search monitor API to return alert counts. (<a href="https://github.com/opensearch-project/alerting/pull/978">#978</a>)</li>
<li>Resolve string issues from core. (<a href="https://github.com/opensearch-project/alerting/pull/987">#987</a>)</li>
<li>Fix getAlerts RBAC problem. (<a href="https://github.com/opensearch-project/alerting/pull/991">#991</a>)</li>
<li>Fix alert constructor with noop trigger to use execution id and workflow id. (<a href="https://github.com/opensearch-project/alerting/pull/994">#994</a>)</li>
</ul>

<h3>Opensearch Ml Common</h3>

<ul>
<li>Add missing codes from pen test fix (<a href="https://github.com/opensearch-project/ml-commons/pull/1060">#1060</a>)</li>
<li>fix cannot specify model access control parameters error (<a href="https://github.com/opensearch-project/ml-commons/pull/1068">#1068</a>)</li>
<li>fix memory circuit breaker (<a href="https://github.com/opensearch-project/ml-commons/pull/1072">#1072</a>)</li>
<li>PenTest fixes: error codes and update model group fix (<a href="https://github.com/opensearch-project/ml-commons/pull/1074">#1074</a>)</li>
<li>Fix rare private ip address bypass SSRF issue (<a href="https://github.com/opensearch-project/ml-commons/pull/1070">#1070</a>)</li>
<li>leftover in the 404 Not Found return error (<a href="https://github.com/opensearch-project/ml-commons/pull/1079">#1079</a>)</li>
<li>modify error message when model group not unique is provided (<a href="https://github.com/opensearch-project/ml-commons/pull/1078">#1078</a>)</li>
<li>stash context before accessing ml config index (<a href="https://github.com/opensearch-project/ml-commons/pull/1092">#1092</a>)</li>
<li>fix init master key bug (<a href="https://github.com/opensearch-project/ml-commons/pull/1094">#1094</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Fixed compile issues related to latest OS core repo changes. (<a href="https://github.com/opensearch-project/security-analytics/pull/412">#412</a>)</li>
</ul>

<h2>INFRASTRUCTURE</h2>

<h3>Opensearch Notifications</h3>

<ul>
<li>Run publish maven snapshots on all branches matching pattern (<a href="https://github.com/opensearch-project/notifications/pull/698">#698</a>)</li>
<li>Strings compile fix due to core package change(<a href="https://github.com/opensearch-project/notifications/pull/680">#680</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Update the BWC version to 2.8.0 <a href="https://github.com/opensearch-project/performance-analyzer/pull/446">#446</a></li>
<li>Upgrade bcprov to bcprov-jdk15to18 in performance-analyzer <a href="https://github.com/opensearch-project/performance-analyzer/pull/493">#493</a></li>
<li>Upgrade bcprov to bcprov-jdk15to18 in performance-analyzer-rca <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/439">439</a></li>
<li>Upgrade bcpkix to bcpkix-jdk15to18 in performance-analyzer-rca <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/446">446</a></li>
<li>Upgrade checkstyle version from 9.3 to 10.3.3 <a href="https://github.com/opensearch-project/performance-analyzer/pull/495">#495</a></li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>stopPrometheus task in doctest build.gradle now runs upon project failure in startOpenSearch (<a href="https://github.com/opensearch-project/sql/pull/1747">#1747</a>)</li>
<li>Upgrade guava to 32.0.1</li>
<li>Disable CrossClusterSearchIT test (<a href="https://github.com/opensearch-project/sql/pull/1814">#1814</a>)</li>
<li>fix flakytest when tests.locale=tr (<a href="https://github.com/opensearch-project/sql/pull/1827">#1827</a>)</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Updated Maintainers and CODE_OWNERS list (<a href="https://github.com/opensearch-project/anomaly-detection/pull/926">#926</a>)</li>
<li>Bump guava version to 32.0.1 (<a href="https://github.com/opensearch-project/anomaly-detection/pull/933">#933</a>)</li>
<li>Bump scipy from 1.8.0 to 1.10.0 in /dataGeneration (<a href="https://github.com/opensearch-project/anomaly-detection/pull/943">#943</a>)</li>
<li>Fix main build - update import of Releasable and remove reference to BaseExceptionsHelper (<a href="https://github.com/opensearch-project/anomaly-detection/pull/930">#930</a>)</li>
</ul>

<h3>Opensearch Ml Common</h3>

<ul>
<li>Adding an integration test for redeploying a model (<a href="https://github.com/opensearch-project/ml-commons/pull/1016">#1016</a>)</li>
<li>add unit test for connector class in commons (<a href="https://github.com/opensearch-project/ml-commons/pull/1058">#1058</a>)</li>
<li>remote inference: add unit test for model and register model input (<a href="https://github.com/opensearch-project/ml-commons/pull/1059">#1059</a>)</li>
<li>remote inference: add unit test for StringUtils and remote inference input (<a href="https://github.com/opensearch-project/ml-commons/pull/1061">#1061</a>)</li>
<li>more UT for rest and trasport actions (<a href="https://github.com/opensearch-project/ml-commons/pull/1066">#1066</a>)</li>
<li>remote inference: add unit test for create connector request/response (<a href="https://github.com/opensearch-project/ml-commons/pull/1067">#1067</a>)</li>
<li>Add more UT for remote inference classes (<a href="https://github.com/opensearch-project/ml-commons/pull/1077">#1077</a>)</li>
<li>IT Security Tests for model access control (<a href="https://github.com/opensearch-project/ml-commons/pull/1095">#1095</a>)</li>
</ul>

<h2>DOCUMENTATION</h2>

<h3>Opensearch Notifications</h3>

<ul>
<li>Add 2.9.0 release notes (<a href="https://github.com/opensearch-project/notifications/pull/702">#702</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Added 2.9 release notes. (<a href="https://github.com/opensearch-project/common-utils/pull/482">#482</a>)</li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Updated documentation of round function return type (<a href="https://github.com/opensearch-project/sql/pull/1725">#1725</a>)</li>
<li>Updated <code>protocol.rst</code> with new wording for error message (<a href="https://github.com/opensearch-project/sql/pull/1662">#1662</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Added 2.9 release notes. (<a href="https://github.com/opensearch-project/alerting/pull/1010">#1010</a>)</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Updated Maintainers and CODE_OWNERS list (<a href="https://github.com/opensearch-project/anomaly-detection/pull/926">#926</a>)</li>
</ul>

<h3>Opensearch Ml Common</h3>

<ul>
<li>model access control documentation (<a href="https://github.com/opensearch-project/ml-commons/pull/966">#966</a>)</li>
<li>updating docs for model group id (<a href="https://github.com/opensearch-project/ml-commons/pull/980">#980</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Added 2.9.0 release notes. (<a href="https://github.com/opensearch-project/security-analytics/pull/486">#486</a>)</li>
</ul>

<h2>MAINTENANCE</h2>

<h3>Opensearch Neural Search</h3>

<h3>Maintenance</h3>
<p>Increment version to 2.9.0-SNAPSHOT (<a href="https://github.com/opensearch-project/neural-search/pull/191">#191</a>)</p>

<h3>Opensearch Notifications</h3>

<ul>
<li>[AUTO] Increment version to 2.9.0-SNAPSHOT (<a href="https://github.com/opensearch-project/notifications/pull/690">#690</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Update build.gradle and github workflow to support 2.9 version <a href="https://github.com/opensearch-project/performance-analyzer/pull/499">#499</a></li>
<li>Update licenses files for 2.9 <a href="https://github.com/opensearch-project/performance-analyzer/pull/501">#501</a></li>
<li>Swap jboss annotation dependency for jakarta annotations <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/407">#407</a></li>
<li>Ensures compatibility check readiness <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/438">#438</a></li>
</ul>

<h3>Opensearch Geospatial</h3>

<h3>Maintenance</h3>
<p>Increment version to 2.9.0-SNAPSHOT (<a href="https://github.com/opensearch-project/geospatial/pull/329">#329</a>)</p>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Increment version to 2.9.0-SNAPSHOT. (<a href="https://github.com/opensearch-project/common-utils/pull/444">#444</a>)</li>
<li>Modify triggers to push snapshots on all branches. (<a href="https://github.com/opensearch-project/common-utils/pull/454">#454</a>)</li>
</ul>

<h3>Opensearch Reporting</h3>

<ul>
<li>Increment version to 2.9.0-SNAPSHOT (<a href="https://github.com/opensearch-project/reporting/pull/712">#712</a>)</li>
</ul>

<h3>Opensearch Asynchronous Search</h3>

<ul>
<li>Increment version to 2.9.0 (<a href="https://github.com/opensearch-project/asynchronous-search/pull/300">300</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Increment version to 2.9.0-SNAPSHOT. (<a href="https://github.com/opensearch-project/alerting/pull/950">#950</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Match version of zstd-jni from core (<a href="https://github.com/opensearch-project/security/pull/2835">#2835</a>)</li>
<li>Add Andrey Pleskach (Willyborankin) to Maintainers (<a href="https://github.com/opensearch-project/security/pull/2843">#2843</a>)</li>
<li>Updates bwc versions to latest release (<a href="https://github.com/opensearch-project/security/pull/2849">#2849</a>)</li>
<li>Add search model group permission to ml_read_access role (<a href="https://github.com/opensearch-project/security/pull/2855">#2855</a>) (<a href="https://github.com/opensearch-project/security/pull/2858">#2858</a>)</li>
<li>Format 2.x (<a href="https://github.com/opensearch-project/security/pull/2878">#2878</a>)</li>
<li>Update snappy to 1.1.10.1 and guava to 32.0.1-jre (<a href="https://github.com/opensearch-project/security/pull/2886">#2886</a>) (<a href="https://github.com/opensearch-project/security/pull/2889">#2889</a>)</li>
<li>Resolve ImmutableOpenMap issue from core refactor (<a href="https://github.com/opensearch-project/security/pull/2908">#2908</a>)</li>
<li>Misc changes (<a href="https://github.com/opensearch-project/security/pull/2902">#2902</a>) (<a href="https://github.com/opensearch-project/security/pull/2904">#2904</a>)</li>
<li>Bump BouncyCastle from jdk15on to jdk15to18 (<a href="https://github.com/opensearch-project/security/pull/2901">#2901</a>) (<a href="https://github.com/opensearch-project/security/pull/2917">#2917</a>)</li>
<li>Fix the import org.opensearch.core.common.Strings; and import org.opensearch.core.common.logging.LoggerMessageFormat; (<a href="https://github.com/opensearch-project/security/pull/2953">#2953</a>)</li>
<li>Remove commons-collections 3.2.2 (<a href="https://github.com/opensearch-project/security/pull/2924">#2924</a>) (<a href="https://github.com/opensearch-project/security/pull/2957">#2957</a>)</li>
<li>Resolve CVE-2023-2976 by forcing use of Guava 32.0.1 (<a href="https://github.com/opensearch-project/security/pull/2937">#2937</a>) (<a href="https://github.com/opensearch-project/security/pull/2974">#2974</a>)</li>
<li>Bump jaxb to 2.3.8 (<a href="https://github.com/opensearch-project/security/pull/2977">#2977</a>) (<a href="https://github.com/opensearch-project/security/pull/2979">#2979</a>)</li>
<li>Update Gradle to 8.2.1 (<a href="https://github.com/opensearch-project/security/pull/2978">#2978</a>) (<a href="https://github.com/opensearch-project/security/pull/2981">#2981</a>)</li>
<li>Changed maven repo location for compatibility check (<a href="https://github.com/opensearch-project/security/pull/2988">#2988</a>)</li>
<li>Bump guava to 32.1.1-jre (<a href="https://github.com/opensearch-project/security/pull/2976">#2976</a>) (<a href="https://github.com/opensearch-project/security/pull/2990">#2990</a>)</li>
</ul>

<h3>Opensearch Ml Common</h3>

<ul>
<li>Increment version to 2.9.0-SNAPSHOT (<a href="https://github.com/opensearch-project/ml-commons/pull/955">#955</a>)</li>
<li>Manual CVE backport (<a href="https://github.com/opensearch-project/ml-commons/pull/1008">#1008</a>)</li>
<li>Fix build. (<a href="https://github.com/opensearch-project/ml-commons/pull/1018">#1018</a>)</li>
<li>Fix the refactor change brought by core backport (<a href="https://github.com/opensearch-project/ml-commons/pull/1047">#1047</a>)</li>
<li>change to compileOnly to avoid jarhell (<a href="https://github.com/opensearch-project/ml-commons/pull/1062">#1062</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Increment version to 2.9.0-SNAPSHOT. (<a href="https://github.com/opensearch-project/security-analytics/pull/466">#466</a>)</li>
<li>Gradle update. (<a href="https://github.com/opensearch-project/security-analytics/pull/437">#437</a>)</li>
</ul>

<h2>REFACTORING</h2>

<h3>Opensearch Observability</h3>

<h3>Refactoring</h3>
<ul>
<li>Add class for loading mapping templates in bulk (<a href="https://github.com/opensearch-project/observability/pull/1550">#1550</a>)</li>
</ul>

<h3>Opensearch Geospatial</h3>

<h3>Refactoring</h3>
<p>Change package for Strings.hasText (<a href="https://github.com/opensearch-project/geospatial/pull/314">#314</a>)</p>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Pass workflow id in alert constructors. (<a href="https://github.com/opensearch-project/common-utils/pull/465">#465</a>)</li>
</ul>

<h3>Opensearch Sql</h3>

<ul>
<li>Simplify OpenSearchIndexScanBuilder (<a href="https://github.com/opensearch-project/sql/pull/1738">#1738</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Use strong password in security test. (<a href="https://github.com/opensearch-project/alerting/pull/933">#933</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Use strong password in security test. (<a href="https://github.com/opensearch-project/security-analytics/pull/452">#452</a>)</li>
</ul>

