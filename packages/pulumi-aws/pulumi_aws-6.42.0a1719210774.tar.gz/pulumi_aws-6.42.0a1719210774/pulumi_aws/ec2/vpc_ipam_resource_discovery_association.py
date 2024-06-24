# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VpcIpamResourceDiscoveryAssociationArgs', 'VpcIpamResourceDiscoveryAssociation']

@pulumi.input_type
class VpcIpamResourceDiscoveryAssociationArgs:
    def __init__(__self__, *,
                 ipam_id: pulumi.Input[str],
                 ipam_resource_discovery_id: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a VpcIpamResourceDiscoveryAssociation resource.
        :param pulumi.Input[str] ipam_id: The ID of the IPAM to associate.
        :param pulumi.Input[str] ipam_resource_discovery_id: The ID of the Resource Discovery to associate.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to add to the IPAM resource discovery association resource.
        """
        pulumi.set(__self__, "ipam_id", ipam_id)
        pulumi.set(__self__, "ipam_resource_discovery_id", ipam_resource_discovery_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="ipamId")
    def ipam_id(self) -> pulumi.Input[str]:
        """
        The ID of the IPAM to associate.
        """
        return pulumi.get(self, "ipam_id")

    @ipam_id.setter
    def ipam_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "ipam_id", value)

    @property
    @pulumi.getter(name="ipamResourceDiscoveryId")
    def ipam_resource_discovery_id(self) -> pulumi.Input[str]:
        """
        The ID of the Resource Discovery to associate.
        """
        return pulumi.get(self, "ipam_resource_discovery_id")

    @ipam_resource_discovery_id.setter
    def ipam_resource_discovery_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "ipam_resource_discovery_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to add to the IPAM resource discovery association resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _VpcIpamResourceDiscoveryAssociationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 ipam_arn: Optional[pulumi.Input[str]] = None,
                 ipam_id: Optional[pulumi.Input[str]] = None,
                 ipam_region: Optional[pulumi.Input[str]] = None,
                 ipam_resource_discovery_id: Optional[pulumi.Input[str]] = None,
                 is_default: Optional[pulumi.Input[bool]] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering VpcIpamResourceDiscoveryAssociation resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of IPAM Resource Discovery Association.
        :param pulumi.Input[str] ipam_arn: The Amazon Resource Name (ARN) of the IPAM.
        :param pulumi.Input[str] ipam_id: The ID of the IPAM to associate.
        :param pulumi.Input[str] ipam_region: The home region of the IPAM.
        :param pulumi.Input[str] ipam_resource_discovery_id: The ID of the Resource Discovery to associate.
        :param pulumi.Input[bool] is_default: A boolean to identify if the Resource Discovery is the accounts default resource discovery.
        :param pulumi.Input[str] owner_id: The account ID for the account that manages the Resource Discovery
        :param pulumi.Input[str] state: The lifecycle state of the association when you associate or disassociate a resource discovery.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to add to the IPAM resource discovery association resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if ipam_arn is not None:
            pulumi.set(__self__, "ipam_arn", ipam_arn)
        if ipam_id is not None:
            pulumi.set(__self__, "ipam_id", ipam_id)
        if ipam_region is not None:
            pulumi.set(__self__, "ipam_region", ipam_region)
        if ipam_resource_discovery_id is not None:
            pulumi.set(__self__, "ipam_resource_discovery_id", ipam_resource_discovery_id)
        if is_default is not None:
            pulumi.set(__self__, "is_default", is_default)
        if owner_id is not None:
            pulumi.set(__self__, "owner_id", owner_id)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of IPAM Resource Discovery Association.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="ipamArn")
    def ipam_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the IPAM.
        """
        return pulumi.get(self, "ipam_arn")

    @ipam_arn.setter
    def ipam_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipam_arn", value)

    @property
    @pulumi.getter(name="ipamId")
    def ipam_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the IPAM to associate.
        """
        return pulumi.get(self, "ipam_id")

    @ipam_id.setter
    def ipam_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipam_id", value)

    @property
    @pulumi.getter(name="ipamRegion")
    def ipam_region(self) -> Optional[pulumi.Input[str]]:
        """
        The home region of the IPAM.
        """
        return pulumi.get(self, "ipam_region")

    @ipam_region.setter
    def ipam_region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipam_region", value)

    @property
    @pulumi.getter(name="ipamResourceDiscoveryId")
    def ipam_resource_discovery_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Resource Discovery to associate.
        """
        return pulumi.get(self, "ipam_resource_discovery_id")

    @ipam_resource_discovery_id.setter
    def ipam_resource_discovery_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipam_resource_discovery_id", value)

    @property
    @pulumi.getter(name="isDefault")
    def is_default(self) -> Optional[pulumi.Input[bool]]:
        """
        A boolean to identify if the Resource Discovery is the accounts default resource discovery.
        """
        return pulumi.get(self, "is_default")

    @is_default.setter
    def is_default(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_default", value)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The account ID for the account that manages the Resource Discovery
        """
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_id", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The lifecycle state of the association when you associate or disassociate a resource discovery.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to add to the IPAM resource discovery association resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class VpcIpamResourceDiscoveryAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ipam_id: Optional[pulumi.Input[str]] = None,
                 ipam_resource_discovery_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides an association between an Amazon IP Address Manager (IPAM) and a IPAM Resource Discovery. IPAM Resource Discoveries are resources meant for multi-organization customers. If you wish to use a single IPAM across multiple orgs, a resource discovery can be created and shared from a subordinate organization to the management organizations IPAM delegated admin account.

        Once an association is created between two organizations via IPAM & a IPAM Resource Discovery, IPAM Pools can be shared via Resource Access Manager (RAM) to accounts in the subordinate organization; these RAM shares must be accepted by the end user account. Pools can then also discover and monitor IPAM resources in the subordinate organization.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ec2.VpcIpamResourceDiscoveryAssociation("test",
            ipam_id=test_aws_vpc_ipam["id"],
            ipam_resource_discovery_id=test_aws_vpc_ipam_resource_discovery["id"],
            tags={
                "Name": "test",
            })
        ```

        ## Import

        Using `pulumi import`, import IPAMs using the IPAM resource discovery association `id`. For example:

        ```sh
        $ pulumi import aws:ec2/vpcIpamResourceDiscoveryAssociation:VpcIpamResourceDiscoveryAssociation example ipam-res-disco-assoc-0178368ad2146a492
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ipam_id: The ID of the IPAM to associate.
        :param pulumi.Input[str] ipam_resource_discovery_id: The ID of the Resource Discovery to associate.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to add to the IPAM resource discovery association resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VpcIpamResourceDiscoveryAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an association between an Amazon IP Address Manager (IPAM) and a IPAM Resource Discovery. IPAM Resource Discoveries are resources meant for multi-organization customers. If you wish to use a single IPAM across multiple orgs, a resource discovery can be created and shared from a subordinate organization to the management organizations IPAM delegated admin account.

        Once an association is created between two organizations via IPAM & a IPAM Resource Discovery, IPAM Pools can be shared via Resource Access Manager (RAM) to accounts in the subordinate organization; these RAM shares must be accepted by the end user account. Pools can then also discover and monitor IPAM resources in the subordinate organization.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ec2.VpcIpamResourceDiscoveryAssociation("test",
            ipam_id=test_aws_vpc_ipam["id"],
            ipam_resource_discovery_id=test_aws_vpc_ipam_resource_discovery["id"],
            tags={
                "Name": "test",
            })
        ```

        ## Import

        Using `pulumi import`, import IPAMs using the IPAM resource discovery association `id`. For example:

        ```sh
        $ pulumi import aws:ec2/vpcIpamResourceDiscoveryAssociation:VpcIpamResourceDiscoveryAssociation example ipam-res-disco-assoc-0178368ad2146a492
        ```

        :param str resource_name: The name of the resource.
        :param VpcIpamResourceDiscoveryAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VpcIpamResourceDiscoveryAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ipam_id: Optional[pulumi.Input[str]] = None,
                 ipam_resource_discovery_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VpcIpamResourceDiscoveryAssociationArgs.__new__(VpcIpamResourceDiscoveryAssociationArgs)

            if ipam_id is None and not opts.urn:
                raise TypeError("Missing required property 'ipam_id'")
            __props__.__dict__["ipam_id"] = ipam_id
            if ipam_resource_discovery_id is None and not opts.urn:
                raise TypeError("Missing required property 'ipam_resource_discovery_id'")
            __props__.__dict__["ipam_resource_discovery_id"] = ipam_resource_discovery_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["ipam_arn"] = None
            __props__.__dict__["ipam_region"] = None
            __props__.__dict__["is_default"] = None
            __props__.__dict__["owner_id"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["tags_all"] = None
        super(VpcIpamResourceDiscoveryAssociation, __self__).__init__(
            'aws:ec2/vpcIpamResourceDiscoveryAssociation:VpcIpamResourceDiscoveryAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            ipam_arn: Optional[pulumi.Input[str]] = None,
            ipam_id: Optional[pulumi.Input[str]] = None,
            ipam_region: Optional[pulumi.Input[str]] = None,
            ipam_resource_discovery_id: Optional[pulumi.Input[str]] = None,
            is_default: Optional[pulumi.Input[bool]] = None,
            owner_id: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'VpcIpamResourceDiscoveryAssociation':
        """
        Get an existing VpcIpamResourceDiscoveryAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of IPAM Resource Discovery Association.
        :param pulumi.Input[str] ipam_arn: The Amazon Resource Name (ARN) of the IPAM.
        :param pulumi.Input[str] ipam_id: The ID of the IPAM to associate.
        :param pulumi.Input[str] ipam_region: The home region of the IPAM.
        :param pulumi.Input[str] ipam_resource_discovery_id: The ID of the Resource Discovery to associate.
        :param pulumi.Input[bool] is_default: A boolean to identify if the Resource Discovery is the accounts default resource discovery.
        :param pulumi.Input[str] owner_id: The account ID for the account that manages the Resource Discovery
        :param pulumi.Input[str] state: The lifecycle state of the association when you associate or disassociate a resource discovery.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to add to the IPAM resource discovery association resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VpcIpamResourceDiscoveryAssociationState.__new__(_VpcIpamResourceDiscoveryAssociationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["ipam_arn"] = ipam_arn
        __props__.__dict__["ipam_id"] = ipam_id
        __props__.__dict__["ipam_region"] = ipam_region
        __props__.__dict__["ipam_resource_discovery_id"] = ipam_resource_discovery_id
        __props__.__dict__["is_default"] = is_default
        __props__.__dict__["owner_id"] = owner_id
        __props__.__dict__["state"] = state
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return VpcIpamResourceDiscoveryAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of IPAM Resource Discovery Association.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="ipamArn")
    def ipam_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the IPAM.
        """
        return pulumi.get(self, "ipam_arn")

    @property
    @pulumi.getter(name="ipamId")
    def ipam_id(self) -> pulumi.Output[str]:
        """
        The ID of the IPAM to associate.
        """
        return pulumi.get(self, "ipam_id")

    @property
    @pulumi.getter(name="ipamRegion")
    def ipam_region(self) -> pulumi.Output[str]:
        """
        The home region of the IPAM.
        """
        return pulumi.get(self, "ipam_region")

    @property
    @pulumi.getter(name="ipamResourceDiscoveryId")
    def ipam_resource_discovery_id(self) -> pulumi.Output[str]:
        """
        The ID of the Resource Discovery to associate.
        """
        return pulumi.get(self, "ipam_resource_discovery_id")

    @property
    @pulumi.getter(name="isDefault")
    def is_default(self) -> pulumi.Output[bool]:
        """
        A boolean to identify if the Resource Discovery is the accounts default resource discovery.
        """
        return pulumi.get(self, "is_default")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        The account ID for the account that manages the Resource Discovery
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The lifecycle state of the association when you associate or disassociate a resource discovery.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to add to the IPAM resource discovery association resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

