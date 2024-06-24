# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ResourceArgs', 'Resource']

@pulumi.input_type
class ResourceArgs:
    def __init__(__self__, *,
                 arn: pulumi.Input[str],
                 hybrid_access_enabled: Optional[pulumi.Input[bool]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 use_service_linked_role: Optional[pulumi.Input[bool]] = None,
                 with_federation: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Resource resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the resource.
               
               The following arguments are optional:
        :param pulumi.Input[bool] hybrid_access_enabled: Flag to enable AWS LakeFormation hybrid access permission mode.
               
               > **NOTE:** AWS does not support registering an S3 location with an IAM role and subsequently updating the S3 location registration to a service-linked role.
        :param pulumi.Input[str] role_arn: Role that has read/write access to the resource.
        :param pulumi.Input[bool] use_service_linked_role: Designates an AWS Identity and Access Management (IAM) service-linked role by registering this role with the Data Catalog.
        """
        pulumi.set(__self__, "arn", arn)
        if hybrid_access_enabled is not None:
            pulumi.set(__self__, "hybrid_access_enabled", hybrid_access_enabled)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if use_service_linked_role is not None:
            pulumi.set(__self__, "use_service_linked_role", use_service_linked_role)
        if with_federation is not None:
            pulumi.set(__self__, "with_federation", with_federation)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of the resource.

        The following arguments are optional:
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="hybridAccessEnabled")
    def hybrid_access_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to enable AWS LakeFormation hybrid access permission mode.

        > **NOTE:** AWS does not support registering an S3 location with an IAM role and subsequently updating the S3 location registration to a service-linked role.
        """
        return pulumi.get(self, "hybrid_access_enabled")

    @hybrid_access_enabled.setter
    def hybrid_access_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "hybrid_access_enabled", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Role that has read/write access to the resource.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="useServiceLinkedRole")
    def use_service_linked_role(self) -> Optional[pulumi.Input[bool]]:
        """
        Designates an AWS Identity and Access Management (IAM) service-linked role by registering this role with the Data Catalog.
        """
        return pulumi.get(self, "use_service_linked_role")

    @use_service_linked_role.setter
    def use_service_linked_role(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_service_linked_role", value)

    @property
    @pulumi.getter(name="withFederation")
    def with_federation(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "with_federation")

    @with_federation.setter
    def with_federation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "with_federation", value)


@pulumi.input_type
class _ResourceState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 hybrid_access_enabled: Optional[pulumi.Input[bool]] = None,
                 last_modified: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 use_service_linked_role: Optional[pulumi.Input[bool]] = None,
                 with_federation: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering Resource resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the resource.
               
               The following arguments are optional:
        :param pulumi.Input[bool] hybrid_access_enabled: Flag to enable AWS LakeFormation hybrid access permission mode.
               
               > **NOTE:** AWS does not support registering an S3 location with an IAM role and subsequently updating the S3 location registration to a service-linked role.
        :param pulumi.Input[str] last_modified: Date and time the resource was last modified in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param pulumi.Input[str] role_arn: Role that has read/write access to the resource.
        :param pulumi.Input[bool] use_service_linked_role: Designates an AWS Identity and Access Management (IAM) service-linked role by registering this role with the Data Catalog.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if hybrid_access_enabled is not None:
            pulumi.set(__self__, "hybrid_access_enabled", hybrid_access_enabled)
        if last_modified is not None:
            pulumi.set(__self__, "last_modified", last_modified)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if use_service_linked_role is not None:
            pulumi.set(__self__, "use_service_linked_role", use_service_linked_role)
        if with_federation is not None:
            pulumi.set(__self__, "with_federation", with_federation)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the resource.

        The following arguments are optional:
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="hybridAccessEnabled")
    def hybrid_access_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to enable AWS LakeFormation hybrid access permission mode.

        > **NOTE:** AWS does not support registering an S3 location with an IAM role and subsequently updating the S3 location registration to a service-linked role.
        """
        return pulumi.get(self, "hybrid_access_enabled")

    @hybrid_access_enabled.setter
    def hybrid_access_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "hybrid_access_enabled", value)

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> Optional[pulumi.Input[str]]:
        """
        Date and time the resource was last modified in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "last_modified")

    @last_modified.setter
    def last_modified(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_modified", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Role that has read/write access to the resource.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="useServiceLinkedRole")
    def use_service_linked_role(self) -> Optional[pulumi.Input[bool]]:
        """
        Designates an AWS Identity and Access Management (IAM) service-linked role by registering this role with the Data Catalog.
        """
        return pulumi.get(self, "use_service_linked_role")

    @use_service_linked_role.setter
    def use_service_linked_role(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_service_linked_role", value)

    @property
    @pulumi.getter(name="withFederation")
    def with_federation(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "with_federation")

    @with_federation.setter
    def with_federation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "with_federation", value)


class Resource(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 hybrid_access_enabled: Optional[pulumi.Input[bool]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 use_service_linked_role: Optional[pulumi.Input[bool]] = None,
                 with_federation: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Registers a Lake Formation resource (e.g., S3 bucket) as managed by the Data Catalog. In other words, the S3 path is added to the data lake.

        Choose a role that has read/write access to the chosen Amazon S3 path or use the service-linked role.
        When you register the S3 path, the service-linked role and a new inline policy are created on your behalf.
        Lake Formation adds the first path to the inline policy and attaches it to the service-linked role.
        When you register subsequent paths, Lake Formation adds the path to the existing policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.get_bucket(bucket="an-example-bucket")
        example_resource = aws.lakeformation.Resource("example", arn=example.arn)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the resource.
               
               The following arguments are optional:
        :param pulumi.Input[bool] hybrid_access_enabled: Flag to enable AWS LakeFormation hybrid access permission mode.
               
               > **NOTE:** AWS does not support registering an S3 location with an IAM role and subsequently updating the S3 location registration to a service-linked role.
        :param pulumi.Input[str] role_arn: Role that has read/write access to the resource.
        :param pulumi.Input[bool] use_service_linked_role: Designates an AWS Identity and Access Management (IAM) service-linked role by registering this role with the Data Catalog.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Registers a Lake Formation resource (e.g., S3 bucket) as managed by the Data Catalog. In other words, the S3 path is added to the data lake.

        Choose a role that has read/write access to the chosen Amazon S3 path or use the service-linked role.
        When you register the S3 path, the service-linked role and a new inline policy are created on your behalf.
        Lake Formation adds the first path to the inline policy and attaches it to the service-linked role.
        When you register subsequent paths, Lake Formation adds the path to the existing policy.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.get_bucket(bucket="an-example-bucket")
        example_resource = aws.lakeformation.Resource("example", arn=example.arn)
        ```

        :param str resource_name: The name of the resource.
        :param ResourceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 hybrid_access_enabled: Optional[pulumi.Input[bool]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 use_service_linked_role: Optional[pulumi.Input[bool]] = None,
                 with_federation: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceArgs.__new__(ResourceArgs)

            if arn is None and not opts.urn:
                raise TypeError("Missing required property 'arn'")
            __props__.__dict__["arn"] = arn
            __props__.__dict__["hybrid_access_enabled"] = hybrid_access_enabled
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["use_service_linked_role"] = use_service_linked_role
            __props__.__dict__["with_federation"] = with_federation
            __props__.__dict__["last_modified"] = None
        super(Resource, __self__).__init__(
            'aws:lakeformation/resource:Resource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            hybrid_access_enabled: Optional[pulumi.Input[bool]] = None,
            last_modified: Optional[pulumi.Input[str]] = None,
            role_arn: Optional[pulumi.Input[str]] = None,
            use_service_linked_role: Optional[pulumi.Input[bool]] = None,
            with_federation: Optional[pulumi.Input[bool]] = None) -> 'Resource':
        """
        Get an existing Resource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the resource.
               
               The following arguments are optional:
        :param pulumi.Input[bool] hybrid_access_enabled: Flag to enable AWS LakeFormation hybrid access permission mode.
               
               > **NOTE:** AWS does not support registering an S3 location with an IAM role and subsequently updating the S3 location registration to a service-linked role.
        :param pulumi.Input[str] last_modified: Date and time the resource was last modified in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param pulumi.Input[str] role_arn: Role that has read/write access to the resource.
        :param pulumi.Input[bool] use_service_linked_role: Designates an AWS Identity and Access Management (IAM) service-linked role by registering this role with the Data Catalog.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceState.__new__(_ResourceState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["hybrid_access_enabled"] = hybrid_access_enabled
        __props__.__dict__["last_modified"] = last_modified
        __props__.__dict__["role_arn"] = role_arn
        __props__.__dict__["use_service_linked_role"] = use_service_linked_role
        __props__.__dict__["with_federation"] = with_federation
        return Resource(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the resource.

        The following arguments are optional:
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="hybridAccessEnabled")
    def hybrid_access_enabled(self) -> pulumi.Output[bool]:
        """
        Flag to enable AWS LakeFormation hybrid access permission mode.

        > **NOTE:** AWS does not support registering an S3 location with an IAM role and subsequently updating the S3 location registration to a service-linked role.
        """
        return pulumi.get(self, "hybrid_access_enabled")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> pulumi.Output[str]:
        """
        Date and time the resource was last modified in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        Role that has read/write access to the resource.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="useServiceLinkedRole")
    def use_service_linked_role(self) -> pulumi.Output[Optional[bool]]:
        """
        Designates an AWS Identity and Access Management (IAM) service-linked role by registering this role with the Data Catalog.
        """
        return pulumi.get(self, "use_service_linked_role")

    @property
    @pulumi.getter(name="withFederation")
    def with_federation(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "with_federation")

