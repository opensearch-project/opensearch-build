# CDK for deploying single-node and multi-node OpenSearch cluster with dashboards

This project enables uses to deploy either a single-node or a multi-node OpenSearch cluster.
There are two stacks that get deployed:
1. OpenSearch-Network-Stack: Use this stack to either use an existing Vpc or create a new Vpc. This stack also creates a new security group to manage access.
2. OpenSearch-Infra-Stack: Sets up EC2 ASG (installs opensearch and opensearch-dashboards using userdata), cloudwatch logging, load balancer. Check your cluster log in the log group created from your stack in the cloudwatch.

## Getting Started

- Requires [NPM](https://docs.npmjs.com/cli/v7/configuring-npm/install) to be installed
- Install project dependencies using `npm install` from this project directory
- Configure [aws credentials](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_prerequisites)

## Deployment

### Required context parameters

In order to deploy both the stacks the user needs to provide a set of mandatory and optional parameters listed below:

| Name                                                   | Type     | Description                                                                              |
|--------------------------------------------------------|:---------|:-----------------------------------------------------------------------------------------|
| distVersion (mandatory)                                | string   | The OpenSearch distribution version (released/un-released) the user wants to deploy      |
| securityDisabled (mandatory)                           | boolean  | Enable or disable security plugin                                                        |
| minDistribution (mandatory)                            | boolean  | Is it an un-released OpenSearch distribution with no plugins                             |
| distributionUrl (mandatory)                            | string   | OpenSearch tar distribution url                                                          |
| dashboardsUrl (mandatory)                              | string   | OpenSearch Dashboards tar distribution url                                               |
| cpuArch (mandatory)                                    | string   | CPU platform for EC2, could be either `x64` or `arm64`                                   |
| singleNodeCluster (mandatory)                          | boolean  | Set `true` for single-node cluster else `false` for multi-node                           |
| vpcId (Optional)                                       | string   | Re-use existing vpc, provide vpc id                                                      |
| securityGroupId (Optional)                             | boolean  | Re-use existing security group, provide security group id                                |
| cidr (Optional)                                        | string   | User provided CIDR block for new Vpc, default is `10.0.0.0/16`                           |
| managerNodeCount (Optional)                            | number   | Number of cluster manager nodes, default is 3                                            |
| dateNodeCount (Optional)                               | number   | Number of data nodes, default is 2                                                       |
| clientNodeCount (Optional)                             | number   | Number of dedicated client nodes, default is 0                                           |
| ingestNodeCount (Optional)                             | number   | Number of dedicated ingest nodes, default is 0                                           |

#### Sample command to setup multi-node cluster with security disabled on x64 AL2 machine

```
cdk deploy "*" --context securityDisabled=true \
--context minDistribution=false --context distributionUrl='https://artifacts.opensearch.org/releases/bundle/opensearch/2.3.0/opensearch-2.3.0-linux-x64.tar.gz' \
--context cpuArch='x64' --context singleNodeCluster=false --context dataNodeCount=3 \
--context dashboardsUrl='https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/2.3.0/opensearch-dashboards-2.3.0-linux-x64.tar.gz' \
--context distVersion=2.3.0
```

### Interacting with OpenSearch cluster

After CDK Stack deployment the user will be returned a load-balancer url which they can use to interact with the cluster.

#### Sample commands
`curl -X GET "http://<load-balancer-url>/_cluster/health?pretty"` for OpenSearch

To interact with dashboards use port `8443`. Type `http://<load-balancer-url>:8443` in your browser.

For security enabled cluster run `curl -X GET https://<load-balancer-url> -u 'admin:admin' --insecure`
The security enabled dashboard is accessible using `http` on port `8443`

#### Please note the load-balancer url is internet facing and can be accessed by anyone.
To restrict access please refer [Client IP Preservation](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#client-ip-preservation) to restrict access on internet-facing network load balancer.
You need to add the ip/prefix-list rule in the security group created in network stack.

### Check logs

The opensearch logs are available in cloudwatch logs log-group `opensearchLogGroup/opensearch.log` in the same region your stack is deployed.
Each ec2 instance will create its own log-stream and the log-stream will be named after each instance-id.
