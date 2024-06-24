# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RolePolicyAttachmentArgs', 'RolePolicyAttachment']

@pulumi.input_type
class RolePolicyAttachmentArgs:
    def __init__(__self__, *,
                 policy_arn: pulumi.Input[str],
                 role: pulumi.Input[str]):
        """
        The set of arguments for constructing a RolePolicyAttachment resource.
        :param pulumi.Input[str] policy_arn: The ARN of the policy you want to apply
        :param pulumi.Input[str] role: The name of the IAM role to which the policy should be applied
        """
        pulumi.set(__self__, "policy_arn", policy_arn)
        pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter(name="policyArn")
    def policy_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the policy you want to apply
        """
        return pulumi.get(self, "policy_arn")

    @policy_arn.setter
    def policy_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_arn", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        The name of the IAM role to which the policy should be applied
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)


@pulumi.input_type
class _RolePolicyAttachmentState:
    def __init__(__self__, *,
                 policy_arn: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RolePolicyAttachment resources.
        :param pulumi.Input[str] policy_arn: The ARN of the policy you want to apply
        :param pulumi.Input[str] role: The name of the IAM role to which the policy should be applied
        """
        if policy_arn is not None:
            pulumi.set(__self__, "policy_arn", policy_arn)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter(name="policyArn")
    def policy_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the policy you want to apply
        """
        return pulumi.get(self, "policy_arn")

    @policy_arn.setter
    def policy_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_arn", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the IAM role to which the policy should be applied
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


class RolePolicyAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_arn: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Attaches a Managed IAM Policy to an IAM role

        > **NOTE:** The usage of this resource conflicts with the `iam.PolicyAttachment` resource and will permanently show a difference if both are defined.

        > **NOTE:** For a given role, this resource is incompatible with using the `iam.Role` resource `managed_policy_arns` argument. When using that argument and this resource, both will attempt to manage the role's managed policy attachments and Pulumi will show a permanent difference.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["ec2.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        role = aws.iam.Role("role",
            name="test-role",
            assume_role_policy=assume_role.json)
        policy = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            actions=["ec2:Describe*"],
            resources=["*"],
        )])
        policy_policy = aws.iam.Policy("policy",
            name="test-policy",
            description="A test policy",
            policy=policy.json)
        test_attach = aws.iam.RolePolicyAttachment("test-attach",
            role=role.name,
            policy_arn=policy_policy.arn)
        ```

        ## Import

        Using `pulumi import`, import IAM role policy attachments using the role name and policy arn separated by `/`. For example:

        ```sh
        $ pulumi import aws:iam/rolePolicyAttachment:RolePolicyAttachment test-attach test-role/arn:aws:iam::xxxxxxxxxxxx:policy/test-policy
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_arn: The ARN of the policy you want to apply
        :param pulumi.Input[str] role: The name of the IAM role to which the policy should be applied
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RolePolicyAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attaches a Managed IAM Policy to an IAM role

        > **NOTE:** The usage of this resource conflicts with the `iam.PolicyAttachment` resource and will permanently show a difference if both are defined.

        > **NOTE:** For a given role, this resource is incompatible with using the `iam.Role` resource `managed_policy_arns` argument. When using that argument and this resource, both will attempt to manage the role's managed policy attachments and Pulumi will show a permanent difference.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["ec2.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        role = aws.iam.Role("role",
            name="test-role",
            assume_role_policy=assume_role.json)
        policy = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            actions=["ec2:Describe*"],
            resources=["*"],
        )])
        policy_policy = aws.iam.Policy("policy",
            name="test-policy",
            description="A test policy",
            policy=policy.json)
        test_attach = aws.iam.RolePolicyAttachment("test-attach",
            role=role.name,
            policy_arn=policy_policy.arn)
        ```

        ## Import

        Using `pulumi import`, import IAM role policy attachments using the role name and policy arn separated by `/`. For example:

        ```sh
        $ pulumi import aws:iam/rolePolicyAttachment:RolePolicyAttachment test-attach test-role/arn:aws:iam::xxxxxxxxxxxx:policy/test-policy
        ```

        :param str resource_name: The name of the resource.
        :param RolePolicyAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RolePolicyAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_arn: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RolePolicyAttachmentArgs.__new__(RolePolicyAttachmentArgs)

            if policy_arn is None and not opts.urn:
                raise TypeError("Missing required property 'policy_arn'")
            __props__.__dict__["policy_arn"] = policy_arn
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
        super(RolePolicyAttachment, __self__).__init__(
            'aws:iam/rolePolicyAttachment:RolePolicyAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            policy_arn: Optional[pulumi.Input[str]] = None,
            role: Optional[pulumi.Input[str]] = None) -> 'RolePolicyAttachment':
        """
        Get an existing RolePolicyAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_arn: The ARN of the policy you want to apply
        :param pulumi.Input[str] role: The name of the IAM role to which the policy should be applied
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RolePolicyAttachmentState.__new__(_RolePolicyAttachmentState)

        __props__.__dict__["policy_arn"] = policy_arn
        __props__.__dict__["role"] = role
        return RolePolicyAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="policyArn")
    def policy_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the policy you want to apply
        """
        return pulumi.get(self, "policy_arn")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The name of the IAM role to which the policy should be applied
        """
        return pulumi.get(self, "role")

