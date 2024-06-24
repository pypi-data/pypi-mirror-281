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

__all__ = ['GroupArgs', 'Group']

@pulumi.input_type
class GroupArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 identity_store_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Group resource.
        :param pulumi.Input[str] display_name: A string containing the name of the group. This value is commonly displayed when the group is referenced.
        :param pulumi.Input[str] identity_store_id: The globally unique identifier for the identity store.
               
               The following arguments are optional:
        :param pulumi.Input[str] description: A string containing the description of the group.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "identity_store_id", identity_store_id)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        A string containing the name of the group. This value is commonly displayed when the group is referenced.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="identityStoreId")
    def identity_store_id(self) -> pulumi.Input[str]:
        """
        The globally unique identifier for the identity store.

        The following arguments are optional:
        """
        return pulumi.get(self, "identity_store_id")

    @identity_store_id.setter
    def identity_store_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "identity_store_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A string containing the description of the group.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class _GroupState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 external_ids: Optional[pulumi.Input[Sequence[pulumi.Input['GroupExternalIdArgs']]]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 identity_store_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Group resources.
        :param pulumi.Input[str] description: A string containing the description of the group.
        :param pulumi.Input[str] display_name: A string containing the name of the group. This value is commonly displayed when the group is referenced.
        :param pulumi.Input[Sequence[pulumi.Input['GroupExternalIdArgs']]] external_ids: A list of external IDs that contains the identifiers issued to this resource by an external identity provider. See External IDs below.
        :param pulumi.Input[str] group_id: The identifier of the newly created group in the identity store.
        :param pulumi.Input[str] identity_store_id: The globally unique identifier for the identity store.
               
               The following arguments are optional:
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if external_ids is not None:
            pulumi.set(__self__, "external_ids", external_ids)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if identity_store_id is not None:
            pulumi.set(__self__, "identity_store_id", identity_store_id)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A string containing the description of the group.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        A string containing the name of the group. This value is commonly displayed when the group is referenced.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="externalIds")
    def external_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GroupExternalIdArgs']]]]:
        """
        A list of external IDs that contains the identifiers issued to this resource by an external identity provider. See External IDs below.
        """
        return pulumi.get(self, "external_ids")

    @external_ids.setter
    def external_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GroupExternalIdArgs']]]]):
        pulumi.set(self, "external_ids", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the newly created group in the identity store.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="identityStoreId")
    def identity_store_id(self) -> Optional[pulumi.Input[str]]:
        """
        The globally unique identifier for the identity store.

        The following arguments are optional:
        """
        return pulumi.get(self, "identity_store_id")

    @identity_store_id.setter
    def identity_store_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_store_id", value)


class Group(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 identity_store_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS IdentityStore Group.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        this = aws.identitystore.Group("this",
            display_name="Example group",
            description="Example description",
            identity_store_id=example["identityStoreIds"])
        ```

        ## Import

        Using `pulumi import`, import an Identity Store Group using the combination `identity_store_id/group_id`. For example:

        ```sh
        $ pulumi import aws:identitystore/group:Group example d-9c6705e95c/b8a1c340-8031-7071-a2fb-7dc540320c30
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A string containing the description of the group.
        :param pulumi.Input[str] display_name: A string containing the name of the group. This value is commonly displayed when the group is referenced.
        :param pulumi.Input[str] identity_store_id: The globally unique identifier for the identity store.
               
               The following arguments are optional:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS IdentityStore Group.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        this = aws.identitystore.Group("this",
            display_name="Example group",
            description="Example description",
            identity_store_id=example["identityStoreIds"])
        ```

        ## Import

        Using `pulumi import`, import an Identity Store Group using the combination `identity_store_id/group_id`. For example:

        ```sh
        $ pulumi import aws:identitystore/group:Group example d-9c6705e95c/b8a1c340-8031-7071-a2fb-7dc540320c30
        ```

        :param str resource_name: The name of the resource.
        :param GroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 identity_store_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GroupArgs.__new__(GroupArgs)

            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            if identity_store_id is None and not opts.urn:
                raise TypeError("Missing required property 'identity_store_id'")
            __props__.__dict__["identity_store_id"] = identity_store_id
            __props__.__dict__["external_ids"] = None
            __props__.__dict__["group_id"] = None
        super(Group, __self__).__init__(
            'aws:identitystore/group:Group',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            external_ids: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GroupExternalIdArgs']]]]] = None,
            group_id: Optional[pulumi.Input[str]] = None,
            identity_store_id: Optional[pulumi.Input[str]] = None) -> 'Group':
        """
        Get an existing Group resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A string containing the description of the group.
        :param pulumi.Input[str] display_name: A string containing the name of the group. This value is commonly displayed when the group is referenced.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GroupExternalIdArgs']]]] external_ids: A list of external IDs that contains the identifiers issued to this resource by an external identity provider. See External IDs below.
        :param pulumi.Input[str] group_id: The identifier of the newly created group in the identity store.
        :param pulumi.Input[str] identity_store_id: The globally unique identifier for the identity store.
               
               The following arguments are optional:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GroupState.__new__(_GroupState)

        __props__.__dict__["description"] = description
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["external_ids"] = external_ids
        __props__.__dict__["group_id"] = group_id
        __props__.__dict__["identity_store_id"] = identity_store_id
        return Group(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A string containing the description of the group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        A string containing the name of the group. This value is commonly displayed when the group is referenced.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="externalIds")
    def external_ids(self) -> pulumi.Output[Sequence['outputs.GroupExternalId']]:
        """
        A list of external IDs that contains the identifiers issued to this resource by an external identity provider. See External IDs below.
        """
        return pulumi.get(self, "external_ids")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[str]:
        """
        The identifier of the newly created group in the identity store.
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter(name="identityStoreId")
    def identity_store_id(self) -> pulumi.Output[str]:
        """
        The globally unique identifier for the identity store.

        The following arguments are optional:
        """
        return pulumi.get(self, "identity_store_id")

