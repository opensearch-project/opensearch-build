<h1>OpenSearch and OpenSearch Dashboards 2.10.0 Release Notes</h1>
<h2>FEATURES</h2>

<h3>Opensearch KNN</h3>

<ul>
<li>Add Clear Cache API (<a href="https://github.com/opensearch-project/k-NN/pull/740">#740</a>)</li>
</ul>

<h3>Opensearch Custom Codecs</h3>

<ul>
<li>Initial release with ZSTD codec support</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>IP2Geo processor implementation (<a href="https://github.com/opensearch-project/geospatial/pull/362">#362</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Support copy alias in rollover. (<a href="https://github.com/opensearch-project/index-management/pull/892">#892</a>)</li>
<li>make control center index as system index. (<a href="https://github.com/opensearch-project/index-management/pull/919">#919</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>common utils to support Microsoft teams in notifications (<a href="https://github.com/opensearch-project/common-utils/pull/428">#428</a>)</li>
<li>support list of monitor ids in Chained Monitor Findings (<a href="https://github.com/opensearch-project/common-utils/pull/514">#514</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Conversations and Generative AI in OpenSearch (<a href="https://github.com/opensearch-project/ml-commons/issues/1150">#1150</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Custom log type implementation (<a href="https://github.com/opensearch-project/security-analytics/pull/500">#500</a>)</li>
<li>add mitre attack based auto-correlations support in correlation engine (<a href="https://github.com/opensearch-project/security-analytics/pull/532">#532</a>)</li>
<li>Using alerting workflows in detectors (<a href="https://github.com/opensearch-project/security-analytics/pull/541">#541</a>)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Improved Hybrid Search relevancy by Score Normalization and Combination (<a href="https://github.com/opensearch-project/neural-search/pull/241/">#241</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Add workflowIds field in getAlerts API  (<a href="https://github.com/opensearch-project/alerting/pull/1014">#1014</a>)</li>
<li>add alertId parameter in get chained alert API and paginate associated alerts if alertId param is mentioned (<a href="https://github.com/opensearch-project/alerting/pull/1071">#1071</a>)</li>
<li>Chained Alert Behaviour Changes (<a href="https://github.com/opensearch-project/alerting/pull/1079">#1079</a>)</li>
</ul>

<h2>ENHANCEMENTS</h2>

<h3>Opensearch KNN</h3>

<ul>
<li>Enabled the IVF algorithm to work with Filters of K-NN Query. (<a href="https://github.com/opensearch-project/k-NN/pull/1013">#1013</a>)</li>
<li>Improved the logic to switch to exact search for restrictive filters search for better recall. (<a href="https://github.com/opensearch-project/k-NN/pull/1059">#1059</a>)</li>
<li>Added max distance computation logic to enhance the switch to exact search in filtered Nearest Neighbor Search. (<a href="https://github.com/opensearch-project/k-NN/pull/1066">#1066</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Add Search Back Pressure Autotune Pipeline <a href="https://github.com/opensearch-project/performance-analyzer/pull/517">#517</a></li>
<li>SearchBackPressure Service Node/Cluster RCA <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/437">#437</a></li>
<li>SearchBackPressure Policy/Decider Generic Framework Added <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/461">#461</a></li>
<li>Handle Reader thread termination gracefully <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/476">#476</a></li>
</ul>

<h3>Opensearch SQL</h3>

<ul>
<li>[Backport 2.x] Added support of timestamp/date/time using curly brackets by @matthewryanwells in https://github.com/opensearch-project/sql/pull/1908</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Add feature flags for remote inference (<a href="https://github.com/opensearch-project/ml-commons/pull/1223">#1223</a>)</li>
<li>Add eligible node role settings (<a href="https://github.com/opensearch-project/ml-commons/pull/1197">#1197</a>)</li>
<li>Add more stats: connector count, connector/config index status (<a href="https://github.com/opensearch-project/ml-commons/pull/1180">#1180</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Add .plugins-ml-config to the demo configuration system indices (<a href="https://github.com/opensearch-project/security/pull/2993">#2993</a>)</li>
<li>Add workflow cluster permissions to alerting roles (<a href="https://github.com/opensearch-project/security/pull/2994">#2994</a>)</li>
<li>Include password regex for Dashboardsinfo to display to users (<a href="https://github.com/opensearch-project/security/pull/2999">#2999</a>)</li>
<li>Add geospatial ip2geo to the demo configuration system indices and roles (<a href="https://github.com/opensearch-project/security/pull/3051">#3051</a>)</li>
<li>Make invalid password message clearer (<a href="https://github.com/opensearch-project/security/pull/3057">#3057</a>)</li>
<li>Service Accounts password is randomly generated (<a href="https://github.com/opensearch-project/security/pull/3077">#3077</a>)</li>
<li>Exclude sensitive info from the jackson serialization stacktraces (<a href="https://github.com/opensearch-project/security/pull/3195">#3195</a>)</li>
<li>Prevent raw request body as output in serialization error messages (<a href="https://github.com/opensearch-project/security/pull/3205">#3205</a>)</li>
<li>Command cat/indices will filter results per the Do Not Fail On Forbidden setting (<a href="https://github.com/opensearch-project/security/pull/3236">#3236</a>)</li>
<li>Generate new demo certs with IPv6 loopback added to SAN in node certificate (<a href="https://github.com/opensearch-project/security/pull/3268">#3268</a>)</li>
<li>System index permissions (<a href="https://github.com/opensearch-project/security/pull/2887">#2887</a>)</li>
</ul>

<h3>Opensearch Neural Search</h3>

<ul>
<li>Changed format for hybrid query results to a single list of scores with delimiter (<a href="https://github.com/opensearch-project/neural-search/pull/259">#259</a>)</li>
<li>Added validations for score combination weights in Hybrid Search (<a href="https://github.com/opensearch-project/neural-search/pull/265">#265</a>)</li>
<li>Made hybrid search active by default (<a href="https://github.com/opensearch-project/neural-search/pull/274">#274</a>)</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Defaults anomaly grade to 0 if negative. (<a href="https://github.com/opensearch-project/anomaly-detection/pull/977">#977</a>)</li>
<li>Update RCF to v3.8 and Enable Auto AD with 'Alert Once' Option (<a href="https://github.com/opensearch-project/anomaly-detection/pull/979">#979</a>)</li>
<li>Revert &quot;Enforce DOCUMENT Replication for AD Indices&quot; (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1006">#1006</a>)</li>
</ul>

<h2>BUG FIXES</h2>

<h3>Opensearch KNN</h3>

<ul>
<li>Update Faiss parameter construction to allow HNSW+PQ to work (<a href="https://github.com/opensearch-project/k-NN/pull/1074">#1074</a>)</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Revert datasource state when delete fails(<a href="https://github.com/opensearch-project/geospatial/pull/382">#382</a>)</li>
<li>Update ip2geo test data url(<a href="https://github.com/opensearch-project/geospatial/pull/389">#389</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Fix debug log for missing ISM config index. (<a href="https://github.com/opensearch-project/index-management/pull/846">#846</a>)</li>
<li>Handle NPE in isRollupIndex. (<a href="https://github.com/opensearch-project/index-management/pull/855">#855</a>)</li>
<li>fix for max &amp; min aggregations when no metric property exist. (<a href="https://github.com/opensearch-project/index-management/pull/870">#870</a>)</li>
<li>fix intelliJ IDEA gradle sync error (<a href="https://github.com/opensearch-project/index-management/pull/916">#916</a>)</li>
</ul>

<h3>Opensearch SQL</h3>

<ul>
<li>[2.x] bump okhttp to 4.10.0 (#2043) by @joshuali925 in https://github.com/opensearch-project/sql/pull/2044</li>
<li>[Backport 2.x] Okio upgrade to 3.5.0 by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1963</li>
<li>[Backport 2.x] Fixed response codes For Requests With security exception. by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/2029</li>
<li>[Backport 2.x] Backport breaking changes by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1920</li>
<li>[Manual Backport #1943] Fixing string format change #1943 by @MitchellGale in https://github.com/opensearch-project/sql/pull/1946</li>
<li>[Backport 2.x] Fix CVE by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1944</li>
<li>[Backport 2.x] Breaking change OpenSearch main project - Action movement (#1958) by @MitchellGale in https://github.com/opensearch-project/sql/pull/1965</li>
<li>[Backport 2.x] Update backport CI, add PR merged condition by @ps48 in https://github.com/opensearch-project/sql/pull/1970</li>
<li>[Backport 2.x] Fixed exception when datasource is updated with existing configuration. by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/2008</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Fixing metrics (<a href="https://github.com/opensearch-project/ml-commons/pull/1194">#1194</a>)</li>
<li>Fix null pointer exception when input parameter is null. (<a href="https://github.com/opensearch-project/ml-commons/pull/1192">#1192</a>)</li>
<li>Fix admin with no backend role on AOS unable to create restricted model group (<a href="https://github.com/opensearch-project/ml-commons/pull/1188">#1188</a>)</li>
<li>Fix parameter parsing bug for create connector input (<a href="https://github.com/opensearch-project/ml-commons/pull/1185">#1185</a>)</li>
<li>Handle escaping string parameters explicitly (<a href="https://github.com/opensearch-project/ml-commons/pull/1174">#1174</a>)</li>
<li>Fix model count bug (<a href="https://github.com/opensearch-project/ml-commons/pull/1180">#1180</a>)</li>
<li>Fix core package name to address compilation errors (<a href="https://github.com/opensearch-project/ml-commons/pull/1157">#1157</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Fix for mappings of custom log types &amp; other bug fixes (<a href="https://github.com/opensearch-project/security-analytics/pull/505">#505</a>)</li>
<li>Fixes detectorType incompatibility with detector rules (<a href="https://github.com/opensearch-project/security-analytics/pull/524">#524</a>)</li>
</ul>

<h3>Opensearch Cross Cluster Replication</h3>

<ul>
<li>Settings are synced before syncing mapping (<a href="https://github.com/opensearch-project/cross-cluster-replication/pull/994">#994</a>)</li>
<li>Handled OpenSearchRejectExecuteException, introduced new setting <code>plugins.replication.follower.concurrent_writers_per_shard</code>. (<a href="https://github.com/opensearch-project/cross-cluster-replication/pull/1004">#1004</a>)</li>
<li>Fixed tests relying on wait_for_active_shards, fixed test for single Node and consume numNodes (<a href="https://github.com/opensearch-project/cross-cluster-replication/pull/1091">#1091</a>)</li>
<li>Excessive logging avoided during certain exception types such as OpensearchTimeoutException (<a href="https://github.com/opensearch-project/cross-cluster-replication/pull/1114">#1114</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>Prevent raw request body as output in serialization error messages (<a href="https://github.com/opensearch-project/security/pull/3205">#3205</a>)</li>
<li>Prevent flaky behavior when determining if an request will be executed on the current node. (<a href="https://github.com/opensearch-project/security/pull/3066">#3066</a>)</li>
<li>Resolve a class of ConcurrentModificationException from during bulk requests (<a href="https://github.com/opensearch-project/security/pull/3094">#3094</a>)</li>
<li>Fix Document GET with DLS terms query (<a href="https://github.com/opensearch-project/security/pull/3136">#3136</a>)</li>
<li>Send log messages to log4j systems instead of system out / error (<a href="https://github.com/opensearch-project/security/pull/3231">#3231</a>)</li>
<li>Fix roles verification for roles mapping and internal users (<a href="https://github.com/opensearch-project/security/pull/3278">#3278</a>)</li>
<li>Prevent raw request body as output in serialization error messages (<a href="https://github.com/opensearch-project/security/pull/3205">#3205</a>)</li>
<li>Fix permissions issues while reading keys in PKCS#1 format (<a href="https://github.com/opensearch-project/security/pull/3289">#3289</a>)</li>
</ul>

<h3>Opensearch Reporting</h3>

<ul>
<li>Update import from upstream breaking changes (<a href="https://github.com/opensearch-project/reporting/pull/739">#739</a>)</li>
<li>Fix from upstream import changes (<a href="https://github.com/opensearch-project/reporting/pull/748">#748</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>fix get alerts alertState query filter (<a href="https://github.com/opensearch-project/alerting/pull/1064">#1064</a>)</li>
</ul>

<h2>INFRASTRUCTURE</h2>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Make jacoco report to be generated faster in local (<a href="https://github.com/opensearch-project/geospatial/pull/267">#267</a>)</li>
<li>Exclude lombok generated code from jacoco coverage report (<a href="https://github.com/opensearch-project/geospatial/pull/268">#268</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Update BWC version to 2.9.0 <a href="https://github.com/opensearch-project/performance-analyzer/pull/529">#529</a></li>
<li>Update performance-analyzer-commons library version <a href="https://github.com/opensearch-project/performance-analyzer/pull/446">#537</a></li>
<li>Upgrade gRPC protobug to mitigate connection termination issue <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/471">#471</a></li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Add auto github release workflow. (<a href="https://github.com/opensearch-project/index-management/pull/691">#691</a>)</li>
<li>Fixed the publish maven workflow to execute after pushes to release branches. (<a href="https://github.com/opensearch-project/index-management/pull/837">#837</a>)</li>
<li>Upgrade the backport workflow. (<a href="https://github.com/opensearch-project/index-management/pull/862">#862</a>)</li>
<li>Updates demo certs used in integ tests. (<a href="https://github.com/opensearch-project/index-management/pull/921">#921</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Fix core refactor: StreamIO from common to core.common(<a href="https://github.com/opensearch-project/notifications/pull/707">#707</a>)</li>
<li>Fix core XcontentFactory refactor(<a href="https://github.com/opensearch-project/notifications/pull/732">#732</a>)</li>
<li>Fix actions components after core(<a href="https://github.com/opensearch-project/notifications/pull/739">#739</a>)</li>
<li>Add auto release workflow(<a href="https://github.com/opensearch-project/notifications/pull/731">#731</a>)</li>
<li>Onboarding system and hidden index(<a href="https://github.com/opensearch-project/notifications/pull/742">#742</a>)</li>
<li>Updates demo certs used in integ tests(<a href="https://github.com/opensearch-project/notifications/pull/756">#756</a>)</li>
</ul>

<h3>Opensearch SQL</h3>

<ul>
<li>[Backport 2.x] Add _primary preference only for segment replication enabled indices by @opensearch-trigger-bot in
https://github.com/opensearch-project/sql/pull/2036</li>
<li>[Backport 2.x] Revert &quot;Guarantee datasource read api is strong consistent read (#1815)&quot; by @opensearch-trigger-bot in</li>
<li>[Backport 2.x] [Spotless] Adds new line at end of java files by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1925</li>
<li>(#1506) Remove reservedSymbolTable and replace with HIDDEN_FIELD_NAME… by @acarbonetto in https://github.com/opensearch-project/sql/pull/1964</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Updates demo certs used in integ tests (<a href="https://github.com/opensearch-project/ml-commons/pull/1291">#1291</a>)</li>
<li>Add Auto Release Workflow (<a href="https://github.com/opensearch-project/ml-commons/pull/1306">#1306</a>)</li>
</ul>

<h3>Opensearch Asynchronous Search</h3>

<ul>
<li>Updates demo certs used in rest tests (<a href="https://github.com/opensearch-project/asynchronous-search/pull/341">#341</a>)</li>
<li>Adding release workflow for the asynchronous search (<a href="https://github.com/opensearch-project/asynchronous-search/pull/330">#330</a>)</li>
<li>Refactoring changes in main (<a href="https://github.com/opensearch-project/asynchronous-search/pull/328">#328</a>)</li>
</ul>

<h3>Opensearch Observability</h3>

<ul>
<li>Update backport CI, add PR merged condition in https://github.com/opensearch-project/observability/pull/1587</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Adds auto release workflow (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1003">#1003</a>)</li>
<li>upgrading commons-lang3 version to fix conflict issue (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1014">#1014</a>)</li>
<li>Updates demo certs for integ tests (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1021">#1021</a>)</li>
<li>Upgrade AD's bwc baseline version to 1.3.2 to resolve cluster join issue (<a href="https://github.com/opensearch-project/anomaly-detection/pull/1029">#1029</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Upgrade the backport workflow (<a href="https://github.com/opensearch-project/alerting/pull/1029">#1028</a>)</li>
<li>Updates demo certs used in integ tests (<a href="https://github.com/opensearch-project/alerting/pull/1115">#1115</a>)</li>
</ul>

<h2>DOCUMENTATION</h2>

<h3>Opensearch Index Management</h3>

<ul>
<li>Added 2.10 release notes. (<a href="https://github.com/opensearch-project/index-management/pull/925">#925</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Added 2.10.0.0 release notes (<a href="https://github.com/opensearch-project/common-utils/pull/531">#531</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>Add 2.10.0 release notes (<a href="https://github.com/opensearch-project/notifications/pull/755">#755</a>)</li>
</ul>

<h3>Opensearch SQL</h3>

<ul>
<li>[Backport 2.x] Fix doctest data by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1998</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Updating cohere blueprint doc (<a href="https://github.com/opensearch-project/ml-commons/pull/1213">#1213</a>)</li>
<li>Fixing docs (<a href="https://github.com/opensearch-project/ml-commons/pull/1193">#1193</a>)</li>
<li>Add model auto redeploy tutorial (<a href="https://github.com/opensearch-project/ml-commons/pull/1175">#1175</a>)</li>
<li>Add remote inference tutorial (<a href="https://github.com/opensearch-project/ml-commons/pull/1158">#1158</a>)</li>
<li>Adding blueprint examples for remote inference (<a href="https://github.com/opensearch-project/ml-commons/pull/1155">#1155</a>)</li>
<li>Updating developer guide for CCI contributors (<a href="https://github.com/opensearch-project/ml-commons/pull/1049">#1049</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Added 2.10.0 release notes. (<a href="https://github.com/opensearch-project/security-analytics/pull/555">#555</a>)</li>
</ul>

<h3>Opensearch Asynchronous Search</h3>

<ul>
<li>Add 2.10.0 release notes (<a href="https://github.com/opensearch-project/asynchronous-search/pull/353">#353</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Added 2.10 release notes (<a href="https://github.com/opensearch-project/alerting/pull/1117">#1117</a>)</li>
</ul>

<h2>MAINTENANCE</h2>

<h3>Opensearch KNN</h3>

<ul>
<li>Update Guava Version to 32.0.1 (<a href="https://github.com/opensearch-project/k-NN/pull/1019">#1019</a>)</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Change package for Strings.hasText (<a href="https://github.com/opensearch-project/geospatial/pull/314">#314</a>)</li>
<li>Fixed compilation errors after refactoring in core foundation classes (<a href="https://github.com/opensearch-project/geospatial/pull/380">#380</a>)</li>
<li>Version bump for spotlss and apache commons(<a href="https://github.com/opensearch-project/geospatial/pull/400">#400</a>)</li>
</ul>

<h3>Opensearch Performance Analyzer</h3>

<ul>
<li>Address core refactor changes for Task foundation classes and StreamIO <a href="https://github.com/opensearch-project/performance-analyzer/pull/522">#522</a></li>
<li>Address xcontent changes in core <a href="https://github.com/opensearch-project/performance-analyzer/pull/526">#526</a></li>
<li>Remove usage of deprecated &quot;master&quot; APIs <a href="https://github.com/opensearch-project/performance-analyzer/pull/513">#513</a></li>
<li>Update docker-compose.yml <a href="https://github.com/opensearch-project/performance-analyzer-rca/pull/465">#465</a></li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>Increment version to 2.10.0-SNAPSHOT. (<a href="https://github.com/opensearch-project/index-management/pull/852">#852</a>)</li>
</ul>

<h3>Opensearch Common Utils</h3>

<ul>
<li>Upgrade the backport workflow (<a href="https://github.com/opensearch-project/common-utils/pull/487">#487</a>)</li>
<li>Updates demo certs used in rest tests (<a href="https://github.com/opensearch-project/common-utils/pull/518">#518</a>)</li>
</ul>

<h3>Opensearch Notifications</h3>

<ul>
<li>[AUTO] Increment version to 2.10.0-SNAPSHOT(<a href="https://github.com/opensearch-project/notifications/pull/706">#706</a>)</li>
</ul>

<h3>Opensearch ML Common</h3>

<ul>
<li>Bump checkstyle version for CVE fix (<a href="https://github.com/opensearch-project/ml-commons/pull/1216">#1216</a>)</li>
<li>Correct imports for new location with regard to core refactoring (<a href="https://github.com/opensearch-project/ml-commons/pull/1206">#1206</a>)</li>
<li>Fix breaking change caused by opensearch core (<a href="https://github.com/opensearch-project/ml-commons/pull/1187">#1187</a>)</li>
<li>Bump OpenSearch snapshot version to 2.10 (<a href="https://github.com/opensearch-project/ml-commons/pull/1157">#1157</a>)</li>
<li>Bump aws-encryption-sdk-java to fix CVE-2023-33201 (<a href="https://github.com/opensearch-project/ml-commons/pull/1309">#1309</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Bump version to 2.10 and resolve compile issues (<a href="https://github.com/opensearch-project/security-analytics/pull/521">#521</a>)</li>
</ul>

<h3>Opensearch Security</h3>

<ul>
<li>[Build Break] Update imports for files refactored in core PR #8157 (<a href="https://github.com/opensearch-project/security/pull/3003">#3003</a>)</li>
<li>[Build Break] Fix build after Lucene upgrade and breaking XContentFactory changes (<a href="https://github.com/opensearch-project/security/pull/3069">#3069</a>)</li>
<li>[Build Break] Update CircuitBreakerService and LifecycleComponent after core refactor in #9006 (<a href="https://github.com/opensearch-project/security/pull/3082">#3082</a>)</li>
<li>[Build Break] React to changes in ActionListener and ActionResponse from #9082 (<a href="https://github.com/opensearch-project/security/pull/3153">#3153</a>)</li>
<li>[Build Break] Disable gradlew build cache to ensure most up-to-date dependencies (<a href="https://github.com/opensearch-project/security/pull/3186">#3186</a>)</li>
<li>Bump com.carrotsearch.randomizedtesting:randomizedtesting-runner from 2.7.1 to 2.8.1 (<a href="https://github.com/opensearch-project/security/pull/3109">#3109</a>)</li>
<li>Bump com.diffplug.spotless from 6.19.0 to 6.21.0 (<a href="https://github.com/opensearch-project/security/pull/3108">#3108</a>)</li>
<li>Bump com.fasterxml.woodstox:woodstox-core from 6.4.0 to 6.5.1 (<a href="https://github.com/opensearch-project/security/pull/3148">#3148</a>)</li>
<li>Bump com.github.spotbugs from 5.0.14 to 5.1.3 (<a href="https://github.com/opensearch-project/security/pull/3251">#3251</a>)</li>
<li>Bump com.github.wnameless.json:json-base from 2.4.0 to 2.4.2 (<a href="https://github.com/opensearch-project/security/pull/3062">#3062</a>)</li>
<li>Bump com.github.wnameless.json:json-flattener from 0.16.4 to 0.16.5 (<a href="https://github.com/opensearch-project/security/pull/3296">#3296</a>)</li>
<li>Bump com.google.errorprone:error_prone_annotations from 2.3.4 to 2.20.0 (<a href="https://github.com/opensearch-project/security/pull/3023">#3023</a>)</li>
<li>Bump com.google.guava:guava from 32.1.1-jre to 32.1.2-jre (<a href="https://github.com/opensearch-project/security/pull/3149">#3149</a>)</li>
<li>Bump commons-io:commons-io from 2.11.0 to 2.13.0 (<a href="https://github.com/opensearch-project/security/pull/3074">#3074</a>)</li>
<li>Bump com.netflix.nebula.ospackage from 11.1.0 to 11.3.0 (<a href="https://github.com/opensearch-project/security/pull/3023">#3023</a>)</li>
<li>Bump com.nulab-inc:zxcvbn from 1.7.0 to 1.8.0 (<a href="https://github.com/opensearch-project/security/pull/3023">#3023</a>)</li>
<li>Bump com.unboundid:unboundid-ldapsdk from 4.0.9 to 4.0.14 (<a href="https://github.com/opensearch-project/security/pull/3143">#3143</a>)</li>
<li>Bump io.dropwizard.metrics:metrics-core from 3.1.2 to 4.2.19 (<a href="https://github.com/opensearch-project/security/pull/3073">#3073</a>)</li>
<li>Bump kafka_version from 3.5.0 to 3.5.1 (<a href="https://github.com/opensearch-project/security/pull/3041">#3041</a>)</li>
<li>Bump net.minidev:json-smart from 2.4.11 to 2.5.0 (<a href="https://github.com/opensearch-project/security/pull/3120">#3120</a>)</li>
<li>Bump org.apache.camel:camel-xmlsecurity from 3.14.2 to 3.21.0 (<a href="https://github.com/opensearch-project/security/pull/3023">#3023</a>)</li>
<li>Bump org.apache.santuario:xmlsec from 2.2.3 to 2.3.3 (<a href="https://github.com/opensearch-project/security/pull/3210">#3210</a>)</li>
<li>Bump org.checkerframework:checker-qual from 3.5.0 to 3.36.0 (<a href="https://github.com/opensearch-project/security/pull/3023">#3023</a>)</li>
<li>Bump org.cryptacular:cryptacular from 1.2.4 to 1.2.5 (<a href="https://github.com/opensearch-project/security/pull/3071">#3071</a>)</li>
<li>Bump org.gradle.test-retry from 1.5.2 to 1.5.4 (<a href="https://github.com/opensearch-project/security/pull/3072">#3072</a>)</li>
<li>Bump org.junit.jupiter:junit-jupiter from 5.8.2 to 5.10.0 (<a href="https://github.com/opensearch-project/security/pull/3146">#3146</a>)</li>
<li>Bump org.ow2.asm:asm from 9.1 to 9.5 (<a href="https://github.com/opensearch-project/security/pull/3121">#3121</a>)</li>
<li>Bump org.scala-lang:scala-library from 2.13.9 to 2.13.11 (<a href="https://github.com/opensearch-project/security/pull/3119">#3119</a>)</li>
<li>Bump org.slf4j:slf4j-api from 1.7.30 to 1.7.36 (<a href="https://github.com/opensearch-project/security/pull/3249">#3249</a>)</li>
<li>Bump org.xerial.snappy:snappy-java from 1.1.10.1 to 1.1.10.3 (<a href="https://github.com/opensearch-project/security/pull/3106">#3106</a>)</li>
<li>Bump actions/create-release from 1.0.0 to 1.1.4 (<a href="https://github.com/opensearch-project/security/pull/3141">#3141</a>)</li>
<li>Bump actions/setup-java from 1 to 3 (<a href="https://github.com/opensearch-project/security/pull/3142">#3142</a>)</li>
<li>Bump actions/upload-release-asset from 1.0.1 to 1.0.2 (<a href="https://github.com/opensearch-project/security/pull/3144">#3144</a>)</li>
<li>Bump fernandrone/linelint from 0.0.4 to 0.0.6 (<a href="https://github.com/opensearch-project/security/pull/3211">#3211</a>)</li>
<li>Bump tibdex/github-app-token from 1.5.0 to 1.8.0 (<a href="https://github.com/opensearch-project/security/pull/3147">#3147</a>)</li>
<li>Remove log spam for files that are cleaned up (<a href="https://github.com/opensearch-project/security/pull/3118">#3118</a>)</li>
<li>Updates integTestRemote task to dynamically fetch common-utils version from build.gradle (<a href="https://github.com/opensearch-project/security/pull/3122">#3122</a>)</li>
<li>Switch CodeQL to assemble artifacts using the same build as the rest of CI (<a href="https://github.com/opensearch-project/security/pull/3132">#3132</a>)</li>
<li>Only run the backport job on merged pull requests (<a href="https://github.com/opensearch-project/security/pull/3134">#3134</a>)</li>
<li>Add code coverage exclusions on false positives (<a href="https://github.com/opensearch-project/security/pull/3196">#3196</a>)</li>
<li>Enable jarhell check (<a href="https://github.com/opensearch-project/security/pull/3227">#3227</a>)</li>
<li>Retry code coverage upload on failure (<a href="https://github.com/opensearch-project/security/pull/3242">#3242</a>)</li>
<li>[Refactor] Adopt request builder patterns for SecurityRestApiActions for consistency and clarity (<a href="https://github.com/opensearch-project/security/pull/3123">#3123</a>)</li>
<li>[Refactor] Remove json-path from deps and use JsonPointer instead (<a href="https://github.com/opensearch-project/security/pull/3262">#3262</a>)</li>
<li>Use version of org.apache.commons:commons-lang3 defined in core (<a href="https://github.com/opensearch-project/security/pull/3306">#3306</a>)</li>
<li>Fix checkstyle #3283</li>
<li>Demo Configuration changes (<a href="https://github.com/opensearch-project/security/pull/3330">#3330</a>)</li>
</ul>

<h3>Opensearch Reporting</h3>

<ul>
<li>Fix CI (<a href="https://github.com/opensearch-project/reporting/pull/738">#738</a>)</li>
<li>Update backport CI, add PR merged condition (<a href="https://github.com/opensearch-project/reporting/pull/745">#745</a>)</li>
</ul>

<h3>Opensearch Asynchronous Search</h3>

<ul>
<li>Upgrade Guava version to 32.0.1 (<a href="https://github.com/opensearch-project/asynchronous-search/pull/347">#347</a>)</li>
<li>Increment version to 2.10.0 (<a href="https://github.com/opensearch-project/asynchronous-search/pull/321">#321</a>)</li>
</ul>

<h3>Opensearch Job Scheduler</h3>

<ul>
<li>Update packages according to a change in OpenSearch core (<a href="https://github.com/opensearch-project/job-scheduler/pull/422">#422</a>) (<a href="https://github.com/opensearch-project/job-scheduler/pull/431">#431</a>)</li>
<li>Xcontent changes to ODFERestTestCase (<a href="https://github.com/opensearch-project/job-scheduler/pull/440">#440</a>)</li>
<li>Update LifecycleListener import (<a href="https://github.com/opensearch-project/job-scheduler/pull/445">#445</a>)</li>
<li>Bump slf4j-api to 2.0.7, ospackage to 11.4.0, google-java-format to 1.17.0, guava to 32.1.2-jre and spotless to 6.20.0 (<a href="https://github.com/opensearch-project/job-scheduler/pull/453">#453</a>)</li>
<li>Fixing Strings import (<a href="https://github.com/opensearch-project/job-scheduler/pull/459">#459</a>)</li>
<li>bump com.cronutils:cron-utils from 9.2.0 to 9.2.1 (<a href="https://github.com/opensearch-project/job-scheduler/pull/458">#458</a>)</li>
<li>React to changes in ActionListener and ActionFuture (<a href="https://github.com/opensearch-project/job-scheduler/pull/467">#467</a>)</li>
<li>bump com.diffplug.spotless from 6.20.0 to 6.21.0 (<a href="https://github.com/opensearch-project/job-scheduler/pull/484">#484</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Increment version to 2.10.0-SNAPSHOT. (<a href="https://github.com/opensearch-project/alerting/pull/1018">#1018</a>)</li>
<li>exclude &lt;v32 version of google guava dependency from google java format and add google guava 32.0.1 to resolve CVE CVE-2023-2976 (<a href="https://github.com/opensearch-project/alerting/pull/1094">#1094</a>)</li>
</ul>

<h2>REFACTORING</h2>

<h3>Opensearch KNN</h3>

<ul>
<li>Fix TransportAddress Refactoring Changes in Core (<a href="https://github.com/opensearch-project/k-NN/pull/1020">#1020</a>)</li>
</ul>

<h3>Opensearch Geospatial</h3>

<ul>
<li>Refactor LifecycleComponent package path (<a href="https://github.com/opensearch-project/geospatial/pull/377">#377</a>)</li>
<li>Refactor Strings utility methods to core library (<a href="https://github.com/opensearch-project/geospatial/pull/379">#379</a>)</li>
</ul>

<h3>Opensearch Index Management</h3>

<ul>
<li>[Backport 2.x] Fix after core #8157. (<a href="https://github.com/opensearch-project/index-management/pull/886">#886</a>)</li>
<li>Fix breaking change by core refactor. (<a href="https://github.com/opensearch-project/index-management/pull/888">#888</a>)</li>
<li>Handle core breaking change. (<a href="https://github.com/opensearch-project/index-management/pull/895">#895</a>)</li>
<li>Set preference to _primary when searching control-center index. (<a href="https://github.com/opensearch-project/index-management/pull/911">#911</a>)</li>
<li>Add primary first preference to all search requests. (<a href="https://github.com/opensearch-project/index-management/pull/912">#912</a>)</li>
</ul>

<h3>Opensearch SQL</h3>

<ul>
<li>[Backport 2.x] Applied formatting improvements to Antlr files based on spotless changes (#2017) by @MitchellGale in</li>
<li>[Backport 2.x] Statically init <code>typeActionMap</code> in <code>OpenSearchExprValueFactory</code>. by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1901</li>
<li>[Backport 2.x] (#1536) Refactor OpenSearchQueryRequest and move includes to builder by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/1948</li>
<li>[Backport 2.x] [Spotless] Applying Google Code Format for core/src/main files #3 (#1932) by @MitchellGale in https://github.com/opensearch-project/sql/pull/1994</li>
<li>[Backport 2.x] Developer guide update with Spotless details by @opensearch-trigger-bot in https://github.com/opensearch-project/sql/pull/2004</li>
<li>[Backport 2.x] [Spotless] Applying Google Code Format for core/src/main files #4 #1933 by @MitchellGale in https://github.com/opensearch-project/sql/pull/1995</li>
<li>[Backport 2.x] [Spotless] Applying Google Code Format for core/src/main files #2 #1931 by @MitchellGale in https://github.com/opensearch-project/sql/pull/1993</li>
<li>[Backport 2.x] [Spotless] Applying Google Code Format for core/src/main files #1 #1930 by @MitchellGale in https://github.com/opensearch-project/sql/pull/1992</li>
<li>[Backport 2.x] [Spotless] Applying Google Code Format for core #5 (#1951) by @MitchellGale in https://github.com/opensearch-project/sql/pull/1996</li>
<li>[Backport 2.x] [spotless] Removes Checkstyle in favor of spotless by @MitchellGale in https://github.com/opensearch-project/sql/pull/2018</li>
<li>[Backport 2.x] [Spotless] Entire project running spotless by @MitchellGale in https://github.com/opensearch-project/sql/pull/2016</li>
</ul>
<hr />
<p><strong>Full Changelog</strong>: https://github.com/opensearch-project/sql/compare/2.3.0.0...v.2.10.0.0</p>

<h3>Opensearch ML Common</h3>

<ul>
<li>Renaming metrics (<a href="https://github.com/opensearch-project/ml-commons/pull/1224">#1224</a>)</li>
<li>Changing messaging for IllegalArgumentException on duplicate model groups (<a href="https://github.com/opensearch-project/ml-commons/pull/1294">#1294</a>)</li>
<li>Fixing some error message handeling (<a href="https://github.com/opensearch-project/ml-commons/pull/1222">#1222</a>)</li>
</ul>

<h3>Opensearch Security Analytics</h3>

<ul>
<li>Fix google-java-format-1.17.0.jar: 1 vulnerabilities (<a href="https://github.com/opensearch-project/security-analytics/pull/526">#526</a>)</li>
<li>segment replication changes (<a href="https://github.com/opensearch-project/security-analytics/pull/529">#529</a>)</li>
<li>Use core OpenSearch version of commons-lang3 (<a href="https://github.com/opensearch-project/security-analytics/pull/535">#535</a>)</li>
<li>Force google guava to 32.0.1 (<a href="https://github.com/opensearch-project/security-analytics/pull/536">#536</a>)</li>
<li>Updates demo certs used in integ tests (<a href="https://github.com/opensearch-project/security-analytics/pull/543">#543</a>)</li>
</ul>

<h3>Opensearch Observability</h3>

<ul>
<li>Fix from upstream core.action changes in https://github.com/opensearch-project/observability/pull/1590</li>
<li>Pull jackson,mockito versions from upstream in https://github.com/opensearch-project/observability/pull/1598</li>
<li>Updates demo certs used in integ tests in https://github.com/opensearch-project/observability/pull/1600</li>
</ul>

<h3>Opensearch Anomaly Detection</h3>

<ul>
<li>Refactor due to core updates: Replace and modify classes and methods. (<a href="https://github.com/opensearch-project/anomaly-detection/pull/974">#974</a>)</li>
</ul>

<h3>Opensearch Alerting</h3>

<ul>
<li>Update actionGet to SuspendUntil for ClusterMetrics (<a href="https://github.com/opensearch-project/alerting/pull/1067">#1067</a>)</li>
<li>Resolve compile issues from core changes and update CIs (<a href="https://github.com/opensearch-project/alerting/pull/1100">#1100</a>)</li>
</ul>

<h2>NON-COMPLIANT</h2>
<h2>FEATURES/ENHANCEMENTS</h2>
<h3>Opensearch Notifications</h3>
<ul>
<li>Support SNS FIFO queues(<a href="https://github.com/opensearch-project/notifications/pull/716">#716</a>)</li>
<li>Supuport Microsoft teams(<a href="https://github.com/opensearch-project/notifications/pull/676">#676</a>,<a href="https://github.com/opensearch-project/notifications/pull/746">#746</a>)</li>
<li>Support auto upgrade mapping logic(<a href="https://github.com/opensearch-project/notifications/pull/699">#699</a>)</li>
</ul>
<h2>ADDED</h2>
<h3>Opensearch Job Scheduler</h3>
<ul>
<li>Setting JobSweeper search preference against primary shard (<a href="https://github.com/opensearch-project/job-scheduler/pull/483">#483</a>) (<a href="https://github.com/opensearch-project/job-scheduler/pull/485">#485</a>)</li>
<li>Converts .opendistro-job-scheduler-lock index into a system index (<a href="https://github.com/opensearch-project/job-scheduler/pull/478">#478</a>)</li>
<li>Public snapshots on all release branches (<a href="https://github.com/opensearch-project/job-scheduler/pull/475">#475</a>) (<a href="https://github.com/opensearch-project/job-scheduler/pull/476">#476</a>)</li>
</ul>
<h2>FIXED</h2>
<h3>Opensearch Job Scheduler</h3>
<ul>
<li>Call listner.onFailure when lock creation failed (<a href="https://github.com/opensearch-project/job-scheduler/pull/435">#435</a>) (<a href="https://github.com/opensearch-project/job-scheduler/pull/443">#443</a>)</li>
</ul>
