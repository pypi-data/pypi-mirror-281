# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RdsDbInstanceArgs', 'RdsDbInstance']

@pulumi.input_type
class RdsDbInstanceArgs:
    def __init__(__self__, *,
                 db_password: pulumi.Input[str],
                 db_user: pulumi.Input[str],
                 rds_db_instance_arn: pulumi.Input[str],
                 stack_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a RdsDbInstance resource.
        :param pulumi.Input[str] db_password: A db password
        :param pulumi.Input[str] db_user: A db username
        :param pulumi.Input[str] rds_db_instance_arn: The db instance to register for this stack. Changing this will force a new resource.
        :param pulumi.Input[str] stack_id: The stack to register a db instance for. Changing this will force a new resource.
        """
        pulumi.set(__self__, "db_password", db_password)
        pulumi.set(__self__, "db_user", db_user)
        pulumi.set(__self__, "rds_db_instance_arn", rds_db_instance_arn)
        pulumi.set(__self__, "stack_id", stack_id)

    @property
    @pulumi.getter(name="dbPassword")
    def db_password(self) -> pulumi.Input[str]:
        """
        A db password
        """
        return pulumi.get(self, "db_password")

    @db_password.setter
    def db_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_password", value)

    @property
    @pulumi.getter(name="dbUser")
    def db_user(self) -> pulumi.Input[str]:
        """
        A db username
        """
        return pulumi.get(self, "db_user")

    @db_user.setter
    def db_user(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_user", value)

    @property
    @pulumi.getter(name="rdsDbInstanceArn")
    def rds_db_instance_arn(self) -> pulumi.Input[str]:
        """
        The db instance to register for this stack. Changing this will force a new resource.
        """
        return pulumi.get(self, "rds_db_instance_arn")

    @rds_db_instance_arn.setter
    def rds_db_instance_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "rds_db_instance_arn", value)

    @property
    @pulumi.getter(name="stackId")
    def stack_id(self) -> pulumi.Input[str]:
        """
        The stack to register a db instance for. Changing this will force a new resource.
        """
        return pulumi.get(self, "stack_id")

    @stack_id.setter
    def stack_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "stack_id", value)


@pulumi.input_type
class _RdsDbInstanceState:
    def __init__(__self__, *,
                 db_password: Optional[pulumi.Input[str]] = None,
                 db_user: Optional[pulumi.Input[str]] = None,
                 rds_db_instance_arn: Optional[pulumi.Input[str]] = None,
                 stack_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RdsDbInstance resources.
        :param pulumi.Input[str] db_password: A db password
        :param pulumi.Input[str] db_user: A db username
        :param pulumi.Input[str] rds_db_instance_arn: The db instance to register for this stack. Changing this will force a new resource.
        :param pulumi.Input[str] stack_id: The stack to register a db instance for. Changing this will force a new resource.
        """
        if db_password is not None:
            pulumi.set(__self__, "db_password", db_password)
        if db_user is not None:
            pulumi.set(__self__, "db_user", db_user)
        if rds_db_instance_arn is not None:
            pulumi.set(__self__, "rds_db_instance_arn", rds_db_instance_arn)
        if stack_id is not None:
            pulumi.set(__self__, "stack_id", stack_id)

    @property
    @pulumi.getter(name="dbPassword")
    def db_password(self) -> Optional[pulumi.Input[str]]:
        """
        A db password
        """
        return pulumi.get(self, "db_password")

    @db_password.setter
    def db_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_password", value)

    @property
    @pulumi.getter(name="dbUser")
    def db_user(self) -> Optional[pulumi.Input[str]]:
        """
        A db username
        """
        return pulumi.get(self, "db_user")

    @db_user.setter
    def db_user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_user", value)

    @property
    @pulumi.getter(name="rdsDbInstanceArn")
    def rds_db_instance_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The db instance to register for this stack. Changing this will force a new resource.
        """
        return pulumi.get(self, "rds_db_instance_arn")

    @rds_db_instance_arn.setter
    def rds_db_instance_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rds_db_instance_arn", value)

    @property
    @pulumi.getter(name="stackId")
    def stack_id(self) -> Optional[pulumi.Input[str]]:
        """
        The stack to register a db instance for. Changing this will force a new resource.
        """
        return pulumi.get(self, "stack_id")

    @stack_id.setter
    def stack_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stack_id", value)


class RdsDbInstance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_password: Optional[pulumi.Input[str]] = None,
                 db_user: Optional[pulumi.Input[str]] = None,
                 rds_db_instance_arn: Optional[pulumi.Input[str]] = None,
                 stack_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an OpsWorks RDS DB Instance resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        my_instance = aws.opsworks.RdsDbInstance("my_instance",
            stack_id=my_stack["id"],
            rds_db_instance_arn=my_instance_aws_db_instance["arn"],
            db_user="someUser",
            db_password="somePass")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_password: A db password
        :param pulumi.Input[str] db_user: A db username
        :param pulumi.Input[str] rds_db_instance_arn: The db instance to register for this stack. Changing this will force a new resource.
        :param pulumi.Input[str] stack_id: The stack to register a db instance for. Changing this will force a new resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RdsDbInstanceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an OpsWorks RDS DB Instance resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        my_instance = aws.opsworks.RdsDbInstance("my_instance",
            stack_id=my_stack["id"],
            rds_db_instance_arn=my_instance_aws_db_instance["arn"],
            db_user="someUser",
            db_password="somePass")
        ```

        :param str resource_name: The name of the resource.
        :param RdsDbInstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RdsDbInstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_password: Optional[pulumi.Input[str]] = None,
                 db_user: Optional[pulumi.Input[str]] = None,
                 rds_db_instance_arn: Optional[pulumi.Input[str]] = None,
                 stack_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RdsDbInstanceArgs.__new__(RdsDbInstanceArgs)

            if db_password is None and not opts.urn:
                raise TypeError("Missing required property 'db_password'")
            __props__.__dict__["db_password"] = None if db_password is None else pulumi.Output.secret(db_password)
            if db_user is None and not opts.urn:
                raise TypeError("Missing required property 'db_user'")
            __props__.__dict__["db_user"] = db_user
            if rds_db_instance_arn is None and not opts.urn:
                raise TypeError("Missing required property 'rds_db_instance_arn'")
            __props__.__dict__["rds_db_instance_arn"] = rds_db_instance_arn
            if stack_id is None and not opts.urn:
                raise TypeError("Missing required property 'stack_id'")
            __props__.__dict__["stack_id"] = stack_id
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["dbPassword"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(RdsDbInstance, __self__).__init__(
            'aws:opsworks/rdsDbInstance:RdsDbInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            db_password: Optional[pulumi.Input[str]] = None,
            db_user: Optional[pulumi.Input[str]] = None,
            rds_db_instance_arn: Optional[pulumi.Input[str]] = None,
            stack_id: Optional[pulumi.Input[str]] = None) -> 'RdsDbInstance':
        """
        Get an existing RdsDbInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_password: A db password
        :param pulumi.Input[str] db_user: A db username
        :param pulumi.Input[str] rds_db_instance_arn: The db instance to register for this stack. Changing this will force a new resource.
        :param pulumi.Input[str] stack_id: The stack to register a db instance for. Changing this will force a new resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RdsDbInstanceState.__new__(_RdsDbInstanceState)

        __props__.__dict__["db_password"] = db_password
        __props__.__dict__["db_user"] = db_user
        __props__.__dict__["rds_db_instance_arn"] = rds_db_instance_arn
        __props__.__dict__["stack_id"] = stack_id
        return RdsDbInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dbPassword")
    def db_password(self) -> pulumi.Output[str]:
        """
        A db password
        """
        return pulumi.get(self, "db_password")

    @property
    @pulumi.getter(name="dbUser")
    def db_user(self) -> pulumi.Output[str]:
        """
        A db username
        """
        return pulumi.get(self, "db_user")

    @property
    @pulumi.getter(name="rdsDbInstanceArn")
    def rds_db_instance_arn(self) -> pulumi.Output[str]:
        """
        The db instance to register for this stack. Changing this will force a new resource.
        """
        return pulumi.get(self, "rds_db_instance_arn")

    @property
    @pulumi.getter(name="stackId")
    def stack_id(self) -> pulumi.Output[str]:
        """
        The stack to register a db instance for. Changing this will force a new resource.
        """
        return pulumi.get(self, "stack_id")

