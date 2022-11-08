/* Copyright OpenSearch Contributors
SPDX-License-Identifier: Apache-2.0

The OpenSearch Contributors require contributions made to
this file be licensed under the Apache-2.0 license or a
compatible open source license. */

import { Construct } from 'constructs';
import { Stack, StackProps } from 'aws-cdk-lib';
import {
  AmazonLinuxCpuType, IVpc, SecurityGroup, Vpc,
} from 'aws-cdk-lib/aws-ec2';
import { NetworkStack } from './networking/vpc-stack';
import { InfraStack } from './infra/infra-stack';

enum cpuArchEnum{
    X64='x64',
    ARM64='arm64'
}

export class OsClusterEntrypoint {
    public stacks: Stack[] = [];

    public vpc: IVpc;

    public securityGroup = SecurityGroup;

    constructor(scope: Construct, props: StackProps) {
      let instanceCpuType: AmazonLinuxCpuType;
      let managerCount: number;
      let dataCount: number;
      let clientCount: number;
      let ingestCount: number;

      const vpcId: string = scope.node.tryGetContext('vpcId');
      const securityGroupId = scope.node.tryGetContext('securityGroupId');
      const cidrRange = scope.node.tryGetContext('cidr');

      const distVersion = `${scope.node.tryGetContext('distVersion')}`;
      if (distVersion.toString() === 'undefined') {
        throw new Error('Please provide the OS distribution version');
      }

      const securityDisabled = `${scope.node.tryGetContext('securityDisabled')}`;
      if (securityDisabled !== 'true' && securityDisabled !== 'false') {
        throw new Error('securityEnabled parameter is required to be set as - true or false');
      }
      const security = securityDisabled === 'true';

      const minDistribution = `${scope.node.tryGetContext('minDistribution')}`;
      if (minDistribution !== 'true' && minDistribution !== 'false') {
        throw new Error('minDistribution parameter is required to be set as - true or false');
      }
      const minDist = minDistribution === 'true';

      const distributionUrl = `${scope.node.tryGetContext('distributionUrl')}`;
      if (distributionUrl.toString() === 'undefined') {
        throw new Error('distributionUrl parameter is required. Please provide the artifact url to download');
      }

      const dashboardUrl = `${scope.node.tryGetContext('dashboardsUrl')}`;
      if (dashboardUrl.toString() === 'undefined') {
        throw new Error('dashboardsUrl parameter is required. Please provide the artifact url to download');
      }

      const cpuArch = `${scope.node.tryGetContext('cpuArch')}`;
      if (cpuArch.toString() === 'undefined') {
        throw new Error('cpuArch parameter is required. The provided value should be either x64 or arm64, any other value is invalid');
        // @ts-ignore
      } else if (Object.values(cpuArchEnum).includes(cpuArch.toString())) {
        if (cpuArch.toString() === cpuArchEnum.X64) {
          instanceCpuType = AmazonLinuxCpuType.X86_64;
        } else {
          instanceCpuType = AmazonLinuxCpuType.ARM_64;
        }
      } else {
        throw new Error('Please provide a valid cpu architecture. The valid value can be either x64 or arm64');
      }

      const singleNodeCluster = `${scope.node.tryGetContext('singleNodeCluster')}`;
      const isSingleNode = singleNodeCluster === 'true';

      const managerNodeCount = `${scope.node.tryGetContext('managerNodeCount')}`;
      if (managerNodeCount.toString() === 'undefined') {
        managerCount = 3;
      } else {
        managerCount = parseInt(managerNodeCount, 10);
      }

      const dataNodeCount = `${scope.node.tryGetContext('dataNodeCount')}`;
      if (dataNodeCount.toString() === 'undefined') {
        dataCount = 2;
      } else {
        dataCount = parseInt(dataNodeCount, 10);
      }

      const clientNodeCount = `${scope.node.tryGetContext('clientNodeCount')}`;
      if (clientNodeCount.toString() === 'undefined') {
        clientCount = 0;
      } else {
        clientCount = parseInt(clientNodeCount, 10);
      }

      const ingestNodeCount = `${scope.node.tryGetContext('ingestNodeCount')}`;
      if (ingestNodeCount.toString() === 'undefined') {
        ingestCount = 0;
      } else {
        ingestCount = parseInt(clientNodeCount, 10);
      }

      const network = new NetworkStack(scope, 'OpenSearch-Network-Stack', {
        cidrBlock: cidrRange,
        maxAzs: 3,
        vpcId,
        securityGroupId,
        ...props,
      });

      this.vpc = network.vpc;
      // @ts-ignore
      this.securityGroup = network.osSecurityGroup;

      this.stacks.push(network);

      // @ts-ignore
      const infraStack = new InfraStack(scope, 'OpenSearch-Infra-Stack', {
        vpc: this.vpc,
        securityDisabled: security,
        opensearchVersion: distVersion,
        clientNodeCount: clientCount,
        cpuArch,
        cpuType: instanceCpuType,
        dashboardsUrl: dashboardUrl,
        dataNodeCount: dataCount,
        distributionUrl,
        ingestNodeCount: ingestCount,
        managerNodeCount: managerCount,
        minDistribution: minDist,
        // @ts-ignore
        securityGroup: this.securityGroup,
        singleNodeCluster: isSingleNode,
        ...props,
      });

      infraStack.addDependency(network);

      this.stacks.push(infraStack);
    }
}
