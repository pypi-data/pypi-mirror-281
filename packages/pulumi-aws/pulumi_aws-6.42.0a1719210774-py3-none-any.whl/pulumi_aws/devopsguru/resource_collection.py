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

__all__ = ['ResourceCollectionArgs', 'ResourceCollection']

@pulumi.input_type
class ResourceCollectionArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 cloudformation: Optional[pulumi.Input['ResourceCollectionCloudformationArgs']] = None,
                 tags: Optional[pulumi.Input['ResourceCollectionTagsArgs']] = None):
        """
        The set of arguments for constructing a ResourceCollection resource.
        :param pulumi.Input[str] type: Type of AWS resource collection to create. Valid values are `AWS_CLOUD_FORMATION`, `AWS_SERVICE`, and `AWS_TAGS`.
               
               The following arguments are optional:
        :param pulumi.Input['ResourceCollectionCloudformationArgs'] cloudformation: A collection of AWS CloudFormation stacks. See `cloudformation` below for additional details.
        :param pulumi.Input['ResourceCollectionTagsArgs'] tags: AWS tags used to filter the resources in the resource collection. See `tags` below for additional details.
        """
        pulumi.set(__self__, "type", type)
        if cloudformation is not None:
            pulumi.set(__self__, "cloudformation", cloudformation)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type of AWS resource collection to create. Valid values are `AWS_CLOUD_FORMATION`, `AWS_SERVICE`, and `AWS_TAGS`.

        The following arguments are optional:
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def cloudformation(self) -> Optional[pulumi.Input['ResourceCollectionCloudformationArgs']]:
        """
        A collection of AWS CloudFormation stacks. See `cloudformation` below for additional details.
        """
        return pulumi.get(self, "cloudformation")

    @cloudformation.setter
    def cloudformation(self, value: Optional[pulumi.Input['ResourceCollectionCloudformationArgs']]):
        pulumi.set(self, "cloudformation", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input['ResourceCollectionTagsArgs']]:
        """
        AWS tags used to filter the resources in the resource collection. See `tags` below for additional details.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input['ResourceCollectionTagsArgs']]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ResourceCollectionState:
    def __init__(__self__, *,
                 cloudformation: Optional[pulumi.Input['ResourceCollectionCloudformationArgs']] = None,
                 tags: Optional[pulumi.Input['ResourceCollectionTagsArgs']] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ResourceCollection resources.
        :param pulumi.Input['ResourceCollectionCloudformationArgs'] cloudformation: A collection of AWS CloudFormation stacks. See `cloudformation` below for additional details.
        :param pulumi.Input['ResourceCollectionTagsArgs'] tags: AWS tags used to filter the resources in the resource collection. See `tags` below for additional details.
        :param pulumi.Input[str] type: Type of AWS resource collection to create. Valid values are `AWS_CLOUD_FORMATION`, `AWS_SERVICE`, and `AWS_TAGS`.
               
               The following arguments are optional:
        """
        if cloudformation is not None:
            pulumi.set(__self__, "cloudformation", cloudformation)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def cloudformation(self) -> Optional[pulumi.Input['ResourceCollectionCloudformationArgs']]:
        """
        A collection of AWS CloudFormation stacks. See `cloudformation` below for additional details.
        """
        return pulumi.get(self, "cloudformation")

    @cloudformation.setter
    def cloudformation(self, value: Optional[pulumi.Input['ResourceCollectionCloudformationArgs']]):
        pulumi.set(self, "cloudformation", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input['ResourceCollectionTagsArgs']]:
        """
        AWS tags used to filter the resources in the resource collection. See `tags` below for additional details.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input['ResourceCollectionTagsArgs']]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of AWS resource collection to create. Valid values are `AWS_CLOUD_FORMATION`, `AWS_SERVICE`, and `AWS_TAGS`.

        The following arguments are optional:
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class ResourceCollection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloudformation: Optional[pulumi.Input[pulumi.InputType['ResourceCollectionCloudformationArgs']]] = None,
                 tags: Optional[pulumi.Input[pulumi.InputType['ResourceCollectionTagsArgs']]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS DevOps Guru Resource Collection.

        > Only one type of resource collection (All Account Resources, CloudFormation, or Tags) can be enabled in an account at a time. To avoid persistent differences, this resource should be defined only once.

        ## Example Usage

        ### All Account Resources

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.devopsguru.ResourceCollection("example",
            type="AWS_SERVICE",
            cloudformation=aws.devopsguru.ResourceCollectionCloudformationArgs(
                stack_names=["*"],
            ))
        ```

        ### CloudFormation Stacks

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.devopsguru.ResourceCollection("example",
            type="AWS_CLOUD_FORMATION",
            cloudformation=aws.devopsguru.ResourceCollectionCloudformationArgs(
                stack_names=["ExampleStack"],
            ))
        ```

        ### Tags

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.devopsguru.ResourceCollection("example",
            type="AWS_TAGS",
            tags=aws.devopsguru.ResourceCollectionTagsArgs(
                app_boundary_key="DevOps-Guru-Example",
                tag_values=["Example-Value"],
            ))
        ```

        ### Tags All Resources

        To analyze all resources with the `app_boundary_key` regardless of the corresponding tag value, set `tag_values` to `["*"]`.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.devopsguru.ResourceCollection("example",
            type="AWS_TAGS",
            tags=aws.devopsguru.ResourceCollectionTagsArgs(
                app_boundary_key="DevOps-Guru-Example",
                tag_values=["*"],
            ))
        ```

        ## Import

        Using `pulumi import`, import DevOps Guru Resource Collection using the `id`. For example:

        ```sh
        $ pulumi import aws:devopsguru/resourceCollection:ResourceCollection example AWS_CLOUD_FORMATION
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ResourceCollectionCloudformationArgs']] cloudformation: A collection of AWS CloudFormation stacks. See `cloudformation` below for additional details.
        :param pulumi.Input[pulumi.InputType['ResourceCollectionTagsArgs']] tags: AWS tags used to filter the resources in the resource collection. See `tags` below for additional details.
        :param pulumi.Input[str] type: Type of AWS resource collection to create. Valid values are `AWS_CLOUD_FORMATION`, `AWS_SERVICE`, and `AWS_TAGS`.
               
               The following arguments are optional:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceCollectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS DevOps Guru Resource Collection.

        > Only one type of resource collection (All Account Resources, CloudFormation, or Tags) can be enabled in an account at a time. To avoid persistent differences, this resource should be defined only once.

        ## Example Usage

        ### All Account Resources

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.devopsguru.ResourceCollection("example",
            type="AWS_SERVICE",
            cloudformation=aws.devopsguru.ResourceCollectionCloudformationArgs(
                stack_names=["*"],
            ))
        ```

        ### CloudFormation Stacks

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.devopsguru.ResourceCollection("example",
            type="AWS_CLOUD_FORMATION",
            cloudformation=aws.devopsguru.ResourceCollectionCloudformationArgs(
                stack_names=["ExampleStack"],
            ))
        ```

        ### Tags

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.devopsguru.ResourceCollection("example",
            type="AWS_TAGS",
            tags=aws.devopsguru.ResourceCollectionTagsArgs(
                app_boundary_key="DevOps-Guru-Example",
                tag_values=["Example-Value"],
            ))
        ```

        ### Tags All Resources

        To analyze all resources with the `app_boundary_key` regardless of the corresponding tag value, set `tag_values` to `["*"]`.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.devopsguru.ResourceCollection("example",
            type="AWS_TAGS",
            tags=aws.devopsguru.ResourceCollectionTagsArgs(
                app_boundary_key="DevOps-Guru-Example",
                tag_values=["*"],
            ))
        ```

        ## Import

        Using `pulumi import`, import DevOps Guru Resource Collection using the `id`. For example:

        ```sh
        $ pulumi import aws:devopsguru/resourceCollection:ResourceCollection example AWS_CLOUD_FORMATION
        ```

        :param str resource_name: The name of the resource.
        :param ResourceCollectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceCollectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloudformation: Optional[pulumi.Input[pulumi.InputType['ResourceCollectionCloudformationArgs']]] = None,
                 tags: Optional[pulumi.Input[pulumi.InputType['ResourceCollectionTagsArgs']]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceCollectionArgs.__new__(ResourceCollectionArgs)

            __props__.__dict__["cloudformation"] = cloudformation
            __props__.__dict__["tags"] = tags
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
        super(ResourceCollection, __self__).__init__(
            'aws:devopsguru/resourceCollection:ResourceCollection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cloudformation: Optional[pulumi.Input[pulumi.InputType['ResourceCollectionCloudformationArgs']]] = None,
            tags: Optional[pulumi.Input[pulumi.InputType['ResourceCollectionTagsArgs']]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'ResourceCollection':
        """
        Get an existing ResourceCollection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ResourceCollectionCloudformationArgs']] cloudformation: A collection of AWS CloudFormation stacks. See `cloudformation` below for additional details.
        :param pulumi.Input[pulumi.InputType['ResourceCollectionTagsArgs']] tags: AWS tags used to filter the resources in the resource collection. See `tags` below for additional details.
        :param pulumi.Input[str] type: Type of AWS resource collection to create. Valid values are `AWS_CLOUD_FORMATION`, `AWS_SERVICE`, and `AWS_TAGS`.
               
               The following arguments are optional:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceCollectionState.__new__(_ResourceCollectionState)

        __props__.__dict__["cloudformation"] = cloudformation
        __props__.__dict__["tags"] = tags
        __props__.__dict__["type"] = type
        return ResourceCollection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def cloudformation(self) -> pulumi.Output[Optional['outputs.ResourceCollectionCloudformation']]:
        """
        A collection of AWS CloudFormation stacks. See `cloudformation` below for additional details.
        """
        return pulumi.get(self, "cloudformation")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional['outputs.ResourceCollectionTags']]:
        """
        AWS tags used to filter the resources in the resource collection. See `tags` below for additional details.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of AWS resource collection to create. Valid values are `AWS_CLOUD_FORMATION`, `AWS_SERVICE`, and `AWS_TAGS`.

        The following arguments are optional:
        """
        return pulumi.get(self, "type")

