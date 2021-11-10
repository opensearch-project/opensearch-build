import { ArnPrincipal, IRole, Role } from '@aws-cdk/aws-iam';
import { IBucket } from '@aws-cdk/aws-s3';
import { Arn, Stack } from '@aws-cdk/core';

export interface IdentitiesProps {
  readonly buildBucket: IBucket;
  readonly useExistingRoles: boolean;
  readonly buildAgentPrinciple: ArnPrincipal;
}

export class Identities {
  private static readonly BUILD_ROLE_NAME = 'opensearch-build';

  private static readonly BUNDLE_ROLE_NAME = 'opensearch-bundle';

  private static readonly TEST_ROLE_NAME = 'opensearch-test';

  constructor(stack: Stack, props: IdentitiesProps) {
    const buildRole = props.useExistingRoles
      ? Identities.roleFromName(stack, Identities.BUILD_ROLE_NAME)
      : new Role(stack, Identities.BUILD_ROLE_NAME, {
        roleName: Identities.BUILD_ROLE_NAME,
        assumedBy: props.buildAgentPrinciple,
      });

    const bundleRole = props.useExistingRoles
      ? Identities.roleFromName(stack, Identities.BUNDLE_ROLE_NAME)
      : new Role(stack, Identities.BUNDLE_ROLE_NAME, {
        roleName: Identities.BUNDLE_ROLE_NAME,
        assumedBy: props.buildAgentPrinciple,
      });

    const testRole = props.useExistingRoles
      ? Identities.roleFromName(stack, Identities.TEST_ROLE_NAME)
      : new Role(stack, Identities.TEST_ROLE_NAME, {
        roleName: Identities.TEST_ROLE_NAME,
        assumedBy: props.buildAgentPrinciple,
      });

    props.buildBucket.grantPut(buildRole, '*/builds/*');

    props.buildBucket.grantRead(bundleRole, '*/builds/*');
    props.buildBucket.grantPut(bundleRole, '*/builds/*');
    props.buildBucket.grantPut(bundleRole, '*/dist/*');

    props.buildBucket.grantRead(testRole, '*/dist/*');
    props.buildBucket.grantPut(testRole, '*/dist/*/tests/*');
    props.buildBucket.grantPut(testRole, '*/test-results/*');
  }

  private static roleFromName(stack: Stack, roleName: string): IRole {
    const roleArn = Arn.format({
      service: 'iam',
      account: stack.account,
      resource: 'role',
      resourceName: roleName,
    }, stack);
    return Role.fromRoleArn(stack, roleName, roleArn);
  }
}
