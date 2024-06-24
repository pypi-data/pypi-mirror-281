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

__all__ = ['InstanceStorageConfigArgs', 'InstanceStorageConfig']

@pulumi.input_type
class InstanceStorageConfigArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[str],
                 resource_type: pulumi.Input[str],
                 storage_config: pulumi.Input['InstanceStorageConfigStorageConfigArgs']):
        """
        The set of arguments for constructing a InstanceStorageConfig resource.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] resource_type: A valid resource type. Valid Values: `AGENT_EVENTS` | `ATTACHMENTS` | `CALL_RECORDINGS` | `CHAT_TRANSCRIPTS` | `CONTACT_EVALUATIONS` | `CONTACT_TRACE_RECORDS` | `MEDIA_STREAMS` | `REAL_TIME_CONTACT_ANALYSIS_SEGMENTS` | `SCHEDULED_REPORTS` | `SCREEN_RECORDINGS`.
        :param pulumi.Input['InstanceStorageConfigStorageConfigArgs'] storage_config: Specifies the storage configuration options for the Connect Instance. Documented below.
        """
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "resource_type", resource_type)
        pulumi.set(__self__, "storage_config", storage_config)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        Specifies the identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Input[str]:
        """
        A valid resource type. Valid Values: `AGENT_EVENTS` | `ATTACHMENTS` | `CALL_RECORDINGS` | `CHAT_TRANSCRIPTS` | `CONTACT_EVALUATIONS` | `CONTACT_TRACE_RECORDS` | `MEDIA_STREAMS` | `REAL_TIME_CONTACT_ANALYSIS_SEGMENTS` | `SCHEDULED_REPORTS` | `SCREEN_RECORDINGS`.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter(name="storageConfig")
    def storage_config(self) -> pulumi.Input['InstanceStorageConfigStorageConfigArgs']:
        """
        Specifies the storage configuration options for the Connect Instance. Documented below.
        """
        return pulumi.get(self, "storage_config")

    @storage_config.setter
    def storage_config(self, value: pulumi.Input['InstanceStorageConfigStorageConfigArgs']):
        pulumi.set(self, "storage_config", value)


@pulumi.input_type
class _InstanceStorageConfigState:
    def __init__(__self__, *,
                 association_id: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 storage_config: Optional[pulumi.Input['InstanceStorageConfigStorageConfigArgs']] = None):
        """
        Input properties used for looking up and filtering InstanceStorageConfig resources.
        :param pulumi.Input[str] association_id: The existing association identifier that uniquely identifies the resource type and storage config for the given instance ID.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] resource_type: A valid resource type. Valid Values: `AGENT_EVENTS` | `ATTACHMENTS` | `CALL_RECORDINGS` | `CHAT_TRANSCRIPTS` | `CONTACT_EVALUATIONS` | `CONTACT_TRACE_RECORDS` | `MEDIA_STREAMS` | `REAL_TIME_CONTACT_ANALYSIS_SEGMENTS` | `SCHEDULED_REPORTS` | `SCREEN_RECORDINGS`.
        :param pulumi.Input['InstanceStorageConfigStorageConfigArgs'] storage_config: Specifies the storage configuration options for the Connect Instance. Documented below.
        """
        if association_id is not None:
            pulumi.set(__self__, "association_id", association_id)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)
        if storage_config is not None:
            pulumi.set(__self__, "storage_config", storage_config)

    @property
    @pulumi.getter(name="associationId")
    def association_id(self) -> Optional[pulumi.Input[str]]:
        """
        The existing association identifier that uniquely identifies the resource type and storage config for the given instance ID.
        """
        return pulumi.get(self, "association_id")

    @association_id.setter
    def association_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "association_id", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        A valid resource type. Valid Values: `AGENT_EVENTS` | `ATTACHMENTS` | `CALL_RECORDINGS` | `CHAT_TRANSCRIPTS` | `CONTACT_EVALUATIONS` | `CONTACT_TRACE_RECORDS` | `MEDIA_STREAMS` | `REAL_TIME_CONTACT_ANALYSIS_SEGMENTS` | `SCHEDULED_REPORTS` | `SCREEN_RECORDINGS`.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter(name="storageConfig")
    def storage_config(self) -> Optional[pulumi.Input['InstanceStorageConfigStorageConfigArgs']]:
        """
        Specifies the storage configuration options for the Connect Instance. Documented below.
        """
        return pulumi.get(self, "storage_config")

    @storage_config.setter
    def storage_config(self, value: Optional[pulumi.Input['InstanceStorageConfigStorageConfigArgs']]):
        pulumi.set(self, "storage_config", value)


class InstanceStorageConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 storage_config: Optional[pulumi.Input[pulumi.InputType['InstanceStorageConfigStorageConfigArgs']]] = None,
                 __props__=None):
        """
        Provides an Amazon Connect Instance Storage Config resource. For more information see
        [Amazon Connect: Getting Started](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-get-started.html)

        ## Example Usage

        ### Storage Config Kinesis Firehose Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="CONTACT_TRACE_RECORDS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                kinesis_firehose_config=aws.connect.InstanceStorageConfigStorageConfigKinesisFirehoseConfigArgs(
                    firehose_arn=example_aws_kinesis_firehose_delivery_stream["arn"],
                ),
                storage_type="KINESIS_FIREHOSE",
            ))
        ```

        ### Storage Config Kinesis Stream Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="CONTACT_TRACE_RECORDS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                kinesis_stream_config=aws.connect.InstanceStorageConfigStorageConfigKinesisStreamConfigArgs(
                    stream_arn=example_aws_kinesis_stream["arn"],
                ),
                storage_type="KINESIS_STREAM",
            ))
        ```

        ### Storage Config Kinesis Video Stream Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="MEDIA_STREAMS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                kinesis_video_stream_config=aws.connect.InstanceStorageConfigStorageConfigKinesisVideoStreamConfigArgs(
                    prefix="example",
                    retention_period_hours=3,
                    encryption_config=aws.connect.InstanceStorageConfigStorageConfigKinesisVideoStreamConfigEncryptionConfigArgs(
                        encryption_type="KMS",
                        key_id=example_aws_kms_key["arn"],
                    ),
                ),
                storage_type="KINESIS_VIDEO_STREAM",
            ))
        ```

        ### Storage Config S3 Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="CHAT_TRANSCRIPTS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                s3_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigArgs(
                    bucket_name=example_aws_s3_bucket["id"],
                    bucket_prefix="example",
                ),
                storage_type="S3",
            ))
        ```

        ### Storage Config S3 Config with Encryption Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="CHAT_TRANSCRIPTS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                s3_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigArgs(
                    bucket_name=example_aws_s3_bucket["id"],
                    bucket_prefix="example",
                    encryption_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigEncryptionConfigArgs(
                        encryption_type="KMS",
                        key_id=example_aws_kms_key["arn"],
                    ),
                ),
                storage_type="S3",
            ))
        ```

        ## Import

        Using `pulumi import`, import Amazon Connect Instance Storage Configs using the `instance_id`, `association_id`, and `resource_type` separated by a colon (`:`). For example:

        ```sh
        $ pulumi import aws:connect/instanceStorageConfig:InstanceStorageConfig example f1288a1f-6193-445a-b47e-af739b2:c1d4e5f6-1b3c-1b3c-1b3c-c1d4e5f6c1d4e5:CHAT_TRANSCRIPTS
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] resource_type: A valid resource type. Valid Values: `AGENT_EVENTS` | `ATTACHMENTS` | `CALL_RECORDINGS` | `CHAT_TRANSCRIPTS` | `CONTACT_EVALUATIONS` | `CONTACT_TRACE_RECORDS` | `MEDIA_STREAMS` | `REAL_TIME_CONTACT_ANALYSIS_SEGMENTS` | `SCHEDULED_REPORTS` | `SCREEN_RECORDINGS`.
        :param pulumi.Input[pulumi.InputType['InstanceStorageConfigStorageConfigArgs']] storage_config: Specifies the storage configuration options for the Connect Instance. Documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InstanceStorageConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Amazon Connect Instance Storage Config resource. For more information see
        [Amazon Connect: Getting Started](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-get-started.html)

        ## Example Usage

        ### Storage Config Kinesis Firehose Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="CONTACT_TRACE_RECORDS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                kinesis_firehose_config=aws.connect.InstanceStorageConfigStorageConfigKinesisFirehoseConfigArgs(
                    firehose_arn=example_aws_kinesis_firehose_delivery_stream["arn"],
                ),
                storage_type="KINESIS_FIREHOSE",
            ))
        ```

        ### Storage Config Kinesis Stream Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="CONTACT_TRACE_RECORDS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                kinesis_stream_config=aws.connect.InstanceStorageConfigStorageConfigKinesisStreamConfigArgs(
                    stream_arn=example_aws_kinesis_stream["arn"],
                ),
                storage_type="KINESIS_STREAM",
            ))
        ```

        ### Storage Config Kinesis Video Stream Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="MEDIA_STREAMS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                kinesis_video_stream_config=aws.connect.InstanceStorageConfigStorageConfigKinesisVideoStreamConfigArgs(
                    prefix="example",
                    retention_period_hours=3,
                    encryption_config=aws.connect.InstanceStorageConfigStorageConfigKinesisVideoStreamConfigEncryptionConfigArgs(
                        encryption_type="KMS",
                        key_id=example_aws_kms_key["arn"],
                    ),
                ),
                storage_type="KINESIS_VIDEO_STREAM",
            ))
        ```

        ### Storage Config S3 Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="CHAT_TRANSCRIPTS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                s3_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigArgs(
                    bucket_name=example_aws_s3_bucket["id"],
                    bucket_prefix="example",
                ),
                storage_type="S3",
            ))
        ```

        ### Storage Config S3 Config with Encryption Config

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.InstanceStorageConfig("example",
            instance_id=example_aws_connect_instance["id"],
            resource_type="CHAT_TRANSCRIPTS",
            storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
                s3_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigArgs(
                    bucket_name=example_aws_s3_bucket["id"],
                    bucket_prefix="example",
                    encryption_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigEncryptionConfigArgs(
                        encryption_type="KMS",
                        key_id=example_aws_kms_key["arn"],
                    ),
                ),
                storage_type="S3",
            ))
        ```

        ## Import

        Using `pulumi import`, import Amazon Connect Instance Storage Configs using the `instance_id`, `association_id`, and `resource_type` separated by a colon (`:`). For example:

        ```sh
        $ pulumi import aws:connect/instanceStorageConfig:InstanceStorageConfig example f1288a1f-6193-445a-b47e-af739b2:c1d4e5f6-1b3c-1b3c-1b3c-c1d4e5f6c1d4e5:CHAT_TRANSCRIPTS
        ```

        :param str resource_name: The name of the resource.
        :param InstanceStorageConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceStorageConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 storage_config: Optional[pulumi.Input[pulumi.InputType['InstanceStorageConfigStorageConfigArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstanceStorageConfigArgs.__new__(InstanceStorageConfigArgs)

            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            if resource_type is None and not opts.urn:
                raise TypeError("Missing required property 'resource_type'")
            __props__.__dict__["resource_type"] = resource_type
            if storage_config is None and not opts.urn:
                raise TypeError("Missing required property 'storage_config'")
            __props__.__dict__["storage_config"] = storage_config
            __props__.__dict__["association_id"] = None
        super(InstanceStorageConfig, __self__).__init__(
            'aws:connect/instanceStorageConfig:InstanceStorageConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            association_id: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            resource_type: Optional[pulumi.Input[str]] = None,
            storage_config: Optional[pulumi.Input[pulumi.InputType['InstanceStorageConfigStorageConfigArgs']]] = None) -> 'InstanceStorageConfig':
        """
        Get an existing InstanceStorageConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] association_id: The existing association identifier that uniquely identifies the resource type and storage config for the given instance ID.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] resource_type: A valid resource type. Valid Values: `AGENT_EVENTS` | `ATTACHMENTS` | `CALL_RECORDINGS` | `CHAT_TRANSCRIPTS` | `CONTACT_EVALUATIONS` | `CONTACT_TRACE_RECORDS` | `MEDIA_STREAMS` | `REAL_TIME_CONTACT_ANALYSIS_SEGMENTS` | `SCHEDULED_REPORTS` | `SCREEN_RECORDINGS`.
        :param pulumi.Input[pulumi.InputType['InstanceStorageConfigStorageConfigArgs']] storage_config: Specifies the storage configuration options for the Connect Instance. Documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InstanceStorageConfigState.__new__(_InstanceStorageConfigState)

        __props__.__dict__["association_id"] = association_id
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["resource_type"] = resource_type
        __props__.__dict__["storage_config"] = storage_config
        return InstanceStorageConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="associationId")
    def association_id(self) -> pulumi.Output[str]:
        """
        The existing association identifier that uniquely identifies the resource type and storage config for the given instance ID.
        """
        return pulumi.get(self, "association_id")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        Specifies the identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Output[str]:
        """
        A valid resource type. Valid Values: `AGENT_EVENTS` | `ATTACHMENTS` | `CALL_RECORDINGS` | `CHAT_TRANSCRIPTS` | `CONTACT_EVALUATIONS` | `CONTACT_TRACE_RECORDS` | `MEDIA_STREAMS` | `REAL_TIME_CONTACT_ANALYSIS_SEGMENTS` | `SCHEDULED_REPORTS` | `SCREEN_RECORDINGS`.
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter(name="storageConfig")
    def storage_config(self) -> pulumi.Output['outputs.InstanceStorageConfigStorageConfig']:
        """
        Specifies the storage configuration options for the Connect Instance. Documented below.
        """
        return pulumi.get(self, "storage_config")

