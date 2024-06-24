# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ModelPackageGroupPolicyArgs', 'ModelPackageGroupPolicy']

@pulumi.input_type
class ModelPackageGroupPolicyArgs:
    def __init__(__self__, *,
                 model_package_group_name: pulumi.Input[str],
                 resource_policy: pulumi.Input[str]):
        """
        The set of arguments for constructing a ModelPackageGroupPolicy resource.
        :param pulumi.Input[str] model_package_group_name: The name of the model package group.
        """
        pulumi.set(__self__, "model_package_group_name", model_package_group_name)
        pulumi.set(__self__, "resource_policy", resource_policy)

    @property
    @pulumi.getter(name="modelPackageGroupName")
    def model_package_group_name(self) -> pulumi.Input[str]:
        """
        The name of the model package group.
        """
        return pulumi.get(self, "model_package_group_name")

    @model_package_group_name.setter
    def model_package_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "model_package_group_name", value)

    @property
    @pulumi.getter(name="resourcePolicy")
    def resource_policy(self) -> pulumi.Input[str]:
        return pulumi.get(self, "resource_policy")

    @resource_policy.setter
    def resource_policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_policy", value)


@pulumi.input_type
class _ModelPackageGroupPolicyState:
    def __init__(__self__, *,
                 model_package_group_name: Optional[pulumi.Input[str]] = None,
                 resource_policy: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ModelPackageGroupPolicy resources.
        :param pulumi.Input[str] model_package_group_name: The name of the model package group.
        """
        if model_package_group_name is not None:
            pulumi.set(__self__, "model_package_group_name", model_package_group_name)
        if resource_policy is not None:
            pulumi.set(__self__, "resource_policy", resource_policy)

    @property
    @pulumi.getter(name="modelPackageGroupName")
    def model_package_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the model package group.
        """
        return pulumi.get(self, "model_package_group_name")

    @model_package_group_name.setter
    def model_package_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "model_package_group_name", value)

    @property
    @pulumi.getter(name="resourcePolicy")
    def resource_policy(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "resource_policy")

    @resource_policy.setter
    def resource_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_policy", value)


class ModelPackageGroupPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 model_package_group_name: Optional[pulumi.Input[str]] = None,
                 resource_policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a SageMaker Model Package Group Policy resource.

        ## Example Usage

        ## Import

        Using `pulumi import`, import SageMaker Model Package Groups using the `name`. For example:

        ```sh
        $ pulumi import aws:sagemaker/modelPackageGroupPolicy:ModelPackageGroupPolicy example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] model_package_group_name: The name of the model package group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ModelPackageGroupPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a SageMaker Model Package Group Policy resource.

        ## Example Usage

        ## Import

        Using `pulumi import`, import SageMaker Model Package Groups using the `name`. For example:

        ```sh
        $ pulumi import aws:sagemaker/modelPackageGroupPolicy:ModelPackageGroupPolicy example example
        ```

        :param str resource_name: The name of the resource.
        :param ModelPackageGroupPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ModelPackageGroupPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 model_package_group_name: Optional[pulumi.Input[str]] = None,
                 resource_policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ModelPackageGroupPolicyArgs.__new__(ModelPackageGroupPolicyArgs)

            if model_package_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'model_package_group_name'")
            __props__.__dict__["model_package_group_name"] = model_package_group_name
            if resource_policy is None and not opts.urn:
                raise TypeError("Missing required property 'resource_policy'")
            __props__.__dict__["resource_policy"] = resource_policy
        super(ModelPackageGroupPolicy, __self__).__init__(
            'aws:sagemaker/modelPackageGroupPolicy:ModelPackageGroupPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            model_package_group_name: Optional[pulumi.Input[str]] = None,
            resource_policy: Optional[pulumi.Input[str]] = None) -> 'ModelPackageGroupPolicy':
        """
        Get an existing ModelPackageGroupPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] model_package_group_name: The name of the model package group.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ModelPackageGroupPolicyState.__new__(_ModelPackageGroupPolicyState)

        __props__.__dict__["model_package_group_name"] = model_package_group_name
        __props__.__dict__["resource_policy"] = resource_policy
        return ModelPackageGroupPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="modelPackageGroupName")
    def model_package_group_name(self) -> pulumi.Output[str]:
        """
        The name of the model package group.
        """
        return pulumi.get(self, "model_package_group_name")

    @property
    @pulumi.getter(name="resourcePolicy")
    def resource_policy(self) -> pulumi.Output[str]:
        return pulumi.get(self, "resource_policy")

