/* Copyright OpenSearch Contributors
SPDX-License-Identifier: Apache-2.0

The OpenSearch Contributors require contributions made to
this file be licensed under the Apache-2.0 license or a
compatible open source license. */

import { App } from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { OsClusterEntrypoint } from '../lib/os-cluster-entrypoint';

test('Test Resources with security disabled multi-node', () => {
  const app = new App({
    context: {
      securityDisabled: true,
      minDistribution: false,
      distributionUrl: 'www.example.com',
      cpuArch: 'x64',
      singleNodeCluster: false,
      dashboardsUrl: 'www.example.com',
      distVersion: '1.0.0',
    },
  });

  // WHEN
  const securityDisabledStack = new OsClusterEntrypoint(app, {
    env: { account: 'test-account', region: 'us-east-1' },
  });
  expect(securityDisabledStack.stacks).toHaveLength(2);
  const networkStack = securityDisabledStack.stacks.filter((s) => s.stackName === 'OpenSearch-Network-Stack')[0];
  const networkTemplate = Template.fromStack(networkStack);
  networkTemplate.resourceCountIs('AWS::EC2::VPC', 1);
  networkTemplate.resourceCountIs('AWS::EC2::SecurityGroup', 1);

  const infraStack = securityDisabledStack.stacks.filter((s) => s.stackName === 'OpenSearch-Infra-Stack')[0];
  const infraTemplate = Template.fromStack(infraStack);
  infraTemplate.resourceCountIs('AWS::Logs::LogGroup', 1);
  infraTemplate.resourceCountIs('AWS::IAM::Role', 1);
  infraTemplate.resourceCountIs('AWS::AutoScaling::AutoScalingGroup', 3);
  infraTemplate.resourceCountIs('AWS::ElasticLoadBalancingV2::LoadBalancer', 1);
  infraTemplate.resourceCountIs('AWS::ElasticLoadBalancingV2::Listener', 2);
  infraTemplate.resourceCountIs('AWS::ElasticLoadBalancingV2::TargetGroup', 2);
  infraTemplate.hasResourceProperties('AWS::ElasticLoadBalancingV2::Listener', {
    Port: 80,
    Protocol: 'TCP',
  });
  infraTemplate.hasResourceProperties('AWS::ElasticLoadBalancingV2::Listener', {
    Port: 8443,
    Protocol: 'TCP',
  });
});

test('Test Resources with security enabled multi-node with existing Vpc', () => {
  const app = new App({
    context: {
      securityDisabled: false,
      minDistribution: false,
      distributionUrl: 'www.example.com',
      cpuArch: 'x64',
      singleNodeCluster: false,
      dashboardsUrl: 'www.example.com',
      distVersion: '1.0.0',
      vpcId: 'vpc-12345',
    },
  });

  // WHEN
  const securityEnabledStack = new OsClusterEntrypoint(app, {
    env: { account: 'test-account', region: 'us-east-1' },
  });
  expect(securityEnabledStack.stacks).toHaveLength(2);
  const networkStack = securityEnabledStack.stacks.filter((s) => s.stackName === 'OpenSearch-Network-Stack')[0];
  const networkTemplate = Template.fromStack(networkStack);
  networkTemplate.resourceCountIs('AWS::EC2::VPC', 0);
  networkTemplate.resourceCountIs('AWS::EC2::SecurityGroup', 1);
  networkTemplate.hasResourceProperties('AWS::EC2::SecurityGroup', {
    VpcId: 'vpc-12345',
  });

  const infraStack = securityEnabledStack.stacks.filter((s) => s.stackName === 'OpenSearch-Infra-Stack')[0];
  const infraTemplate = Template.fromStack(infraStack);
  infraTemplate.hasResourceProperties('AWS::ElasticLoadBalancingV2::Listener', {
    Port: 443,
    Protocol: 'TCP',
  });
});

test('Test Resources with security enabled single-node cluster', () => {
  const app = new App({
    context: {
      securityDisabled: false,
      minDistribution: false,
      distributionUrl: 'www.example.com',
      cpuArch: 'x64',
      singleNodeCluster: true,
      dashboardsUrl: 'www.example.com',
      distVersion: '1.0.0',
    },
  });

  // WHEN
  const singleNodeStack = new OsClusterEntrypoint(app, {
    env: { account: 'test-account', region: 'us-east-1' },
  });
  expect(singleNodeStack.stacks).toHaveLength(2);
  const networkStack = singleNodeStack.stacks.filter((s) => s.stackName === 'OpenSearch-Network-Stack')[0];
  const networkTemplate = Template.fromStack(networkStack);
  networkTemplate.resourceCountIs('AWS::EC2::VPC', 1);
  networkTemplate.resourceCountIs('AWS::EC2::SecurityGroup', 1);

  const infraStack = singleNodeStack.stacks.filter((s) => s.stackName === 'OpenSearch-Infra-Stack')[0];
  const infraTemplate = Template.fromStack(infraStack);
  infraTemplate.hasResourceProperties('AWS::ElasticLoadBalancingV2::Listener', {
    Port: 443,
    Protocol: 'TCP',
  });
  infraTemplate.resourceCountIs('AWS::AutoScaling::AutoScalingGroup', 1);
  infraTemplate.resourceCountIs('AWS::ElasticLoadBalancingV2::LoadBalancer', 1);
  infraTemplate.resourceCountIs('AWS::ElasticLoadBalancingV2::Listener', 2);
  infraTemplate.resourceCountIs('AWS::ElasticLoadBalancingV2::TargetGroup', 2);
});
