# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['LogGroupArgs', 'LogGroup']

@pulumi.input_type
class LogGroupArgs:
    def __init__(__self__, *,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_group_class: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 retention_in_days: Optional[pulumi.Input[int]] = None,
                 skip_destroy: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a LogGroup resource.
        :param pulumi.Input[str] kms_key_id: The ARN of the KMS Key to use when encrypting log data. Please note, after the AWS KMS CMK is disassociated from the log group,
               AWS CloudWatch Logs stops encrypting newly ingested data for the log group. All previously ingested data remains encrypted, and AWS CloudWatch Logs requires
               permissions for the CMK whenever the encrypted data is requested.
        :param pulumi.Input[str] log_group_class: Specified the log class of the log group. Possible values are: `STANDARD` or `INFREQUENT_ACCESS`.
        :param pulumi.Input[str] name: The name of the log group. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[int] retention_in_days: Specifies the number of days
               you want to retain log events in the specified log group.  Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653, and 0.
               If you select 0, the events in the log group are always retained and never expire.
        :param pulumi.Input[bool] skip_destroy: Set to true if you do not wish the log group (and any logs it may contain) to be deleted at destroy time, and instead just remove the log group from the state.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if log_group_class is not None:
            pulumi.set(__self__, "log_group_class", log_group_class)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if name_prefix is not None:
            pulumi.set(__self__, "name_prefix", name_prefix)
        if retention_in_days is not None:
            pulumi.set(__self__, "retention_in_days", retention_in_days)
        if skip_destroy is not None:
            pulumi.set(__self__, "skip_destroy", skip_destroy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the KMS Key to use when encrypting log data. Please note, after the AWS KMS CMK is disassociated from the log group,
        AWS CloudWatch Logs stops encrypting newly ingested data for the log group. All previously ingested data remains encrypted, and AWS CloudWatch Logs requires
        permissions for the CMK whenever the encrypted data is requested.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter(name="logGroupClass")
    def log_group_class(self) -> Optional[pulumi.Input[str]]:
        """
        Specified the log class of the log group. Possible values are: `STANDARD` or `INFREQUENT_ACCESS`.
        """
        return pulumi.get(self, "log_group_class")

    @log_group_class.setter
    def log_group_class(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_group_class", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the log group. If omitted, this provider will assign a random, unique name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @name_prefix.setter
    def name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_prefix", value)

    @property
    @pulumi.getter(name="retentionInDays")
    def retention_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of days
        you want to retain log events in the specified log group.  Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653, and 0.
        If you select 0, the events in the log group are always retained and never expire.
        """
        return pulumi.get(self, "retention_in_days")

    @retention_in_days.setter
    def retention_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retention_in_days", value)

    @property
    @pulumi.getter(name="skipDestroy")
    def skip_destroy(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to true if you do not wish the log group (and any logs it may contain) to be deleted at destroy time, and instead just remove the log group from the state.
        """
        return pulumi.get(self, "skip_destroy")

    @skip_destroy.setter
    def skip_destroy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_destroy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _LogGroupState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_group_class: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 retention_in_days: Optional[pulumi.Input[int]] = None,
                 skip_destroy: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering LogGroup resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) specifying the log group. Any `:*` suffix added by the API, denoting all CloudWatch Log Streams under the CloudWatch Log Group, is removed for greater compatibility with other AWS services that do not accept the suffix.
        :param pulumi.Input[str] kms_key_id: The ARN of the KMS Key to use when encrypting log data. Please note, after the AWS KMS CMK is disassociated from the log group,
               AWS CloudWatch Logs stops encrypting newly ingested data for the log group. All previously ingested data remains encrypted, and AWS CloudWatch Logs requires
               permissions for the CMK whenever the encrypted data is requested.
        :param pulumi.Input[str] log_group_class: Specified the log class of the log group. Possible values are: `STANDARD` or `INFREQUENT_ACCESS`.
        :param pulumi.Input[str] name: The name of the log group. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[int] retention_in_days: Specifies the number of days
               you want to retain log events in the specified log group.  Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653, and 0.
               If you select 0, the events in the log group are always retained and never expire.
        :param pulumi.Input[bool] skip_destroy: Set to true if you do not wish the log group (and any logs it may contain) to be deleted at destroy time, and instead just remove the log group from the state.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if log_group_class is not None:
            pulumi.set(__self__, "log_group_class", log_group_class)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if name_prefix is not None:
            pulumi.set(__self__, "name_prefix", name_prefix)
        if retention_in_days is not None:
            pulumi.set(__self__, "retention_in_days", retention_in_days)
        if skip_destroy is not None:
            pulumi.set(__self__, "skip_destroy", skip_destroy)
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
        The Amazon Resource Name (ARN) specifying the log group. Any `:*` suffix added by the API, denoting all CloudWatch Log Streams under the CloudWatch Log Group, is removed for greater compatibility with other AWS services that do not accept the suffix.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the KMS Key to use when encrypting log data. Please note, after the AWS KMS CMK is disassociated from the log group,
        AWS CloudWatch Logs stops encrypting newly ingested data for the log group. All previously ingested data remains encrypted, and AWS CloudWatch Logs requires
        permissions for the CMK whenever the encrypted data is requested.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter(name="logGroupClass")
    def log_group_class(self) -> Optional[pulumi.Input[str]]:
        """
        Specified the log class of the log group. Possible values are: `STANDARD` or `INFREQUENT_ACCESS`.
        """
        return pulumi.get(self, "log_group_class")

    @log_group_class.setter
    def log_group_class(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_group_class", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the log group. If omitted, this provider will assign a random, unique name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @name_prefix.setter
    def name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_prefix", value)

    @property
    @pulumi.getter(name="retentionInDays")
    def retention_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of days
        you want to retain log events in the specified log group.  Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653, and 0.
        If you select 0, the events in the log group are always retained and never expire.
        """
        return pulumi.get(self, "retention_in_days")

    @retention_in_days.setter
    def retention_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retention_in_days", value)

    @property
    @pulumi.getter(name="skipDestroy")
    def skip_destroy(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to true if you do not wish the log group (and any logs it may contain) to be deleted at destroy time, and instead just remove the log group from the state.
        """
        return pulumi.get(self, "skip_destroy")

    @skip_destroy.setter
    def skip_destroy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_destroy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class LogGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_group_class: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 retention_in_days: Optional[pulumi.Input[int]] = None,
                 skip_destroy: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a CloudWatch Log Group resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        yada = aws.cloudwatch.LogGroup("yada",
            name="Yada",
            tags={
                "Environment": "production",
                "Application": "serviceA",
            })
        ```

        ## Import

        Using `pulumi import`, import Cloudwatch Log Groups using the `name`. For example:

        ```sh
        $ pulumi import aws:cloudwatch/logGroup:LogGroup test_group yada
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] kms_key_id: The ARN of the KMS Key to use when encrypting log data. Please note, after the AWS KMS CMK is disassociated from the log group,
               AWS CloudWatch Logs stops encrypting newly ingested data for the log group. All previously ingested data remains encrypted, and AWS CloudWatch Logs requires
               permissions for the CMK whenever the encrypted data is requested.
        :param pulumi.Input[str] log_group_class: Specified the log class of the log group. Possible values are: `STANDARD` or `INFREQUENT_ACCESS`.
        :param pulumi.Input[str] name: The name of the log group. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[int] retention_in_days: Specifies the number of days
               you want to retain log events in the specified log group.  Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653, and 0.
               If you select 0, the events in the log group are always retained and never expire.
        :param pulumi.Input[bool] skip_destroy: Set to true if you do not wish the log group (and any logs it may contain) to be deleted at destroy time, and instead just remove the log group from the state.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[LogGroupArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CloudWatch Log Group resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        yada = aws.cloudwatch.LogGroup("yada",
            name="Yada",
            tags={
                "Environment": "production",
                "Application": "serviceA",
            })
        ```

        ## Import

        Using `pulumi import`, import Cloudwatch Log Groups using the `name`. For example:

        ```sh
        $ pulumi import aws:cloudwatch/logGroup:LogGroup test_group yada
        ```

        :param str resource_name: The name of the resource.
        :param LogGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LogGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 log_group_class: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 retention_in_days: Optional[pulumi.Input[int]] = None,
                 skip_destroy: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LogGroupArgs.__new__(LogGroupArgs)

            __props__.__dict__["kms_key_id"] = kms_key_id
            __props__.__dict__["log_group_class"] = log_group_class
            __props__.__dict__["name"] = name
            __props__.__dict__["name_prefix"] = name_prefix
            __props__.__dict__["retention_in_days"] = retention_in_days
            __props__.__dict__["skip_destroy"] = skip_destroy
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(LogGroup, __self__).__init__(
            'aws:cloudwatch/logGroup:LogGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            kms_key_id: Optional[pulumi.Input[str]] = None,
            log_group_class: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            name_prefix: Optional[pulumi.Input[str]] = None,
            retention_in_days: Optional[pulumi.Input[int]] = None,
            skip_destroy: Optional[pulumi.Input[bool]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'LogGroup':
        """
        Get an existing LogGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) specifying the log group. Any `:*` suffix added by the API, denoting all CloudWatch Log Streams under the CloudWatch Log Group, is removed for greater compatibility with other AWS services that do not accept the suffix.
        :param pulumi.Input[str] kms_key_id: The ARN of the KMS Key to use when encrypting log data. Please note, after the AWS KMS CMK is disassociated from the log group,
               AWS CloudWatch Logs stops encrypting newly ingested data for the log group. All previously ingested data remains encrypted, and AWS CloudWatch Logs requires
               permissions for the CMK whenever the encrypted data is requested.
        :param pulumi.Input[str] log_group_class: Specified the log class of the log group. Possible values are: `STANDARD` or `INFREQUENT_ACCESS`.
        :param pulumi.Input[str] name: The name of the log group. If omitted, this provider will assign a random, unique name.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[int] retention_in_days: Specifies the number of days
               you want to retain log events in the specified log group.  Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653, and 0.
               If you select 0, the events in the log group are always retained and never expire.
        :param pulumi.Input[bool] skip_destroy: Set to true if you do not wish the log group (and any logs it may contain) to be deleted at destroy time, and instead just remove the log group from the state.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LogGroupState.__new__(_LogGroupState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["kms_key_id"] = kms_key_id
        __props__.__dict__["log_group_class"] = log_group_class
        __props__.__dict__["name"] = name
        __props__.__dict__["name_prefix"] = name_prefix
        __props__.__dict__["retention_in_days"] = retention_in_days
        __props__.__dict__["skip_destroy"] = skip_destroy
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return LogGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) specifying the log group. Any `:*` suffix added by the API, denoting all CloudWatch Log Streams under the CloudWatch Log Group, is removed for greater compatibility with other AWS services that do not accept the suffix.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ARN of the KMS Key to use when encrypting log data. Please note, after the AWS KMS CMK is disassociated from the log group,
        AWS CloudWatch Logs stops encrypting newly ingested data for the log group. All previously ingested data remains encrypted, and AWS CloudWatch Logs requires
        permissions for the CMK whenever the encrypted data is requested.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="logGroupClass")
    def log_group_class(self) -> pulumi.Output[str]:
        """
        Specified the log class of the log group. Possible values are: `STANDARD` or `INFREQUENT_ACCESS`.
        """
        return pulumi.get(self, "log_group_class")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the log group. If omitted, this provider will assign a random, unique name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> pulumi.Output[str]:
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @property
    @pulumi.getter(name="retentionInDays")
    def retention_in_days(self) -> pulumi.Output[Optional[int]]:
        """
        Specifies the number of days
        you want to retain log events in the specified log group.  Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653, and 0.
        If you select 0, the events in the log group are always retained and never expire.
        """
        return pulumi.get(self, "retention_in_days")

    @property
    @pulumi.getter(name="skipDestroy")
    def skip_destroy(self) -> pulumi.Output[Optional[bool]]:
        """
        Set to true if you do not wish the log group (and any logs it may contain) to be deleted at destroy time, and instead just remove the log group from the state.
        """
        return pulumi.get(self, "skip_destroy")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

