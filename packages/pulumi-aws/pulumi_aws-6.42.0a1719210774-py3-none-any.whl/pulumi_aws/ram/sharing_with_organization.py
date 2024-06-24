# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SharingWithOrganizationArgs', 'SharingWithOrganization']

@pulumi.input_type
class SharingWithOrganizationArgs:
    def __init__(__self__):
        """
        The set of arguments for constructing a SharingWithOrganization resource.
        """
        pass


class SharingWithOrganization(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 __props__=None):
        """
        Manages Resource Access Manager (RAM) Resource Sharing with AWS Organizations. If you enable sharing with your organization, you can share resources without using invitations. Refer to the [AWS RAM user guide](https://docs.aws.amazon.com/ram/latest/userguide/getting-started-sharing.html#getting-started-sharing-orgs) for more details.

        > **NOTE:** Use this resource to manage resource sharing within your organization, **not** the `organizations.Organization` resource with `ram.amazonaws.com` configured in `aws_service_access_principals`.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ram.SharingWithOrganization("example")
        ```

        ## Import

        Using `pulumi import`, import the resource using the current AWS account ID. For example:

        ```sh
        $ pulumi import aws:ram/sharingWithOrganization:SharingWithOrganization example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[SharingWithOrganizationArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages Resource Access Manager (RAM) Resource Sharing with AWS Organizations. If you enable sharing with your organization, you can share resources without using invitations. Refer to the [AWS RAM user guide](https://docs.aws.amazon.com/ram/latest/userguide/getting-started-sharing.html#getting-started-sharing-orgs) for more details.

        > **NOTE:** Use this resource to manage resource sharing within your organization, **not** the `organizations.Organization` resource with `ram.amazonaws.com` configured in `aws_service_access_principals`.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ram.SharingWithOrganization("example")
        ```

        ## Import

        Using `pulumi import`, import the resource using the current AWS account ID. For example:

        ```sh
        $ pulumi import aws:ram/sharingWithOrganization:SharingWithOrganization example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param SharingWithOrganizationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SharingWithOrganizationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SharingWithOrganizationArgs.__new__(SharingWithOrganizationArgs)

        super(SharingWithOrganization, __self__).__init__(
            'aws:ram/sharingWithOrganization:SharingWithOrganization',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SharingWithOrganization':
        """
        Get an existing SharingWithOrganization resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SharingWithOrganizationArgs.__new__(SharingWithOrganizationArgs)

        return SharingWithOrganization(resource_name, opts=opts, __props__=__props__)

