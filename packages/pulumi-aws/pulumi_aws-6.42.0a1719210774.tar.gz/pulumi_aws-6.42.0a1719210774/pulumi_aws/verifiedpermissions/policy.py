# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['PolicyArgs', 'Policy']

@pulumi.input_type
class PolicyArgs:
    def __init__(__self__, *,
                 policy_store_id: pulumi.Input[str],
                 definition: Optional[pulumi.Input['PolicyDefinitionArgs']] = None):
        """
        The set of arguments for constructing a Policy resource.
        :param pulumi.Input[str] policy_store_id: The Policy Store ID of the policy store.
        :param pulumi.Input['PolicyDefinitionArgs'] definition: The definition of the policy. See Definition below.
        """
        pulumi.set(__self__, "policy_store_id", policy_store_id)
        if definition is not None:
            pulumi.set(__self__, "definition", definition)

    @property
    @pulumi.getter(name="policyStoreId")
    def policy_store_id(self) -> pulumi.Input[str]:
        """
        The Policy Store ID of the policy store.
        """
        return pulumi.get(self, "policy_store_id")

    @policy_store_id.setter
    def policy_store_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_store_id", value)

    @property
    @pulumi.getter
    def definition(self) -> Optional[pulumi.Input['PolicyDefinitionArgs']]:
        """
        The definition of the policy. See Definition below.
        """
        return pulumi.get(self, "definition")

    @definition.setter
    def definition(self, value: Optional[pulumi.Input['PolicyDefinitionArgs']]):
        pulumi.set(self, "definition", value)


@pulumi.input_type
class _PolicyState:
    def __init__(__self__, *,
                 created_date: Optional[pulumi.Input[str]] = None,
                 definition: Optional[pulumi.Input['PolicyDefinitionArgs']] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 policy_store_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Policy resources.
        :param pulumi.Input[str] created_date: The date the policy was created.
        :param pulumi.Input['PolicyDefinitionArgs'] definition: The definition of the policy. See Definition below.
        :param pulumi.Input[str] policy_id: The Policy ID of the policy.
        :param pulumi.Input[str] policy_store_id: The Policy Store ID of the policy store.
        """
        if created_date is not None:
            pulumi.set(__self__, "created_date", created_date)
        if definition is not None:
            pulumi.set(__self__, "definition", definition)
        if policy_id is not None:
            pulumi.set(__self__, "policy_id", policy_id)
        if policy_store_id is not None:
            pulumi.set(__self__, "policy_store_id", policy_store_id)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> Optional[pulumi.Input[str]]:
        """
        The date the policy was created.
        """
        return pulumi.get(self, "created_date")

    @created_date.setter
    def created_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_date", value)

    @property
    @pulumi.getter
    def definition(self) -> Optional[pulumi.Input['PolicyDefinitionArgs']]:
        """
        The definition of the policy. See Definition below.
        """
        return pulumi.get(self, "definition")

    @definition.setter
    def definition(self, value: Optional[pulumi.Input['PolicyDefinitionArgs']]):
        pulumi.set(self, "definition", value)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Policy ID of the policy.
        """
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter(name="policyStoreId")
    def policy_store_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Policy Store ID of the policy store.
        """
        return pulumi.get(self, "policy_store_id")

    @policy_store_id.setter
    def policy_store_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_store_id", value)


class Policy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 definition: Optional[pulumi.Input[pulumi.InputType['PolicyDefinitionArgs']]] = None,
                 policy_store_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS Verified Permissions Policy.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.verifiedpermissions.Policy("test",
            policy_store_id=test_aws_verifiedpermissions_policy_store["id"],
            definition=aws.verifiedpermissions.PolicyDefinitionArgs(
                static=aws.verifiedpermissions.PolicyDefinitionStaticArgs(
                    statement="permit (principal, action == Action::\\"view\\", resource in Album:: \\"test_album\\");",
                ),
            ))
        ```

        ## Import

        Using `pulumi import`, import Verified Permissions Policy using the `policy_id,policy_store_id`. For example:

        ```sh
        $ pulumi import aws:verifiedpermissions/policy:Policy example policy-id-12345678,policy-store-id-12345678
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PolicyDefinitionArgs']] definition: The definition of the policy. See Definition below.
        :param pulumi.Input[str] policy_store_id: The Policy Store ID of the policy store.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS Verified Permissions Policy.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.verifiedpermissions.Policy("test",
            policy_store_id=test_aws_verifiedpermissions_policy_store["id"],
            definition=aws.verifiedpermissions.PolicyDefinitionArgs(
                static=aws.verifiedpermissions.PolicyDefinitionStaticArgs(
                    statement="permit (principal, action == Action::\\"view\\", resource in Album:: \\"test_album\\");",
                ),
            ))
        ```

        ## Import

        Using `pulumi import`, import Verified Permissions Policy using the `policy_id,policy_store_id`. For example:

        ```sh
        $ pulumi import aws:verifiedpermissions/policy:Policy example policy-id-12345678,policy-store-id-12345678
        ```

        :param str resource_name: The name of the resource.
        :param PolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 definition: Optional[pulumi.Input[pulumi.InputType['PolicyDefinitionArgs']]] = None,
                 policy_store_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PolicyArgs.__new__(PolicyArgs)

            __props__.__dict__["definition"] = definition
            if policy_store_id is None and not opts.urn:
                raise TypeError("Missing required property 'policy_store_id'")
            __props__.__dict__["policy_store_id"] = policy_store_id
            __props__.__dict__["created_date"] = None
            __props__.__dict__["policy_id"] = None
        super(Policy, __self__).__init__(
            'aws:verifiedpermissions/policy:Policy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            created_date: Optional[pulumi.Input[str]] = None,
            definition: Optional[pulumi.Input[pulumi.InputType['PolicyDefinitionArgs']]] = None,
            policy_id: Optional[pulumi.Input[str]] = None,
            policy_store_id: Optional[pulumi.Input[str]] = None) -> 'Policy':
        """
        Get an existing Policy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_date: The date the policy was created.
        :param pulumi.Input[pulumi.InputType['PolicyDefinitionArgs']] definition: The definition of the policy. See Definition below.
        :param pulumi.Input[str] policy_id: The Policy ID of the policy.
        :param pulumi.Input[str] policy_store_id: The Policy Store ID of the policy store.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PolicyState.__new__(_PolicyState)

        __props__.__dict__["created_date"] = created_date
        __props__.__dict__["definition"] = definition
        __props__.__dict__["policy_id"] = policy_id
        __props__.__dict__["policy_store_id"] = policy_store_id
        return Policy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> pulumi.Output[str]:
        """
        The date the policy was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter
    def definition(self) -> pulumi.Output[Optional['outputs.PolicyDefinition']]:
        """
        The definition of the policy. See Definition below.
        """
        return pulumi.get(self, "definition")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> pulumi.Output[str]:
        """
        The Policy ID of the policy.
        """
        return pulumi.get(self, "policy_id")

    @property
    @pulumi.getter(name="policyStoreId")
    def policy_store_id(self) -> pulumi.Output[str]:
        """
        The Policy Store ID of the policy store.
        """
        return pulumi.get(self, "policy_store_id")

