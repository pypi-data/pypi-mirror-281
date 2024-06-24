# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VoiceConnectorLoggingArgs', 'VoiceConnectorLogging']

@pulumi.input_type
class VoiceConnectorLoggingArgs:
    def __init__(__self__, *,
                 voice_connector_id: pulumi.Input[str],
                 enable_media_metric_logs: Optional[pulumi.Input[bool]] = None,
                 enable_sip_logs: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a VoiceConnectorLogging resource.
        :param pulumi.Input[str] voice_connector_id: The Amazon Chime Voice Connector ID.
        :param pulumi.Input[bool] enable_media_metric_logs: When true, enables logging of detailed media metrics for Voice Connectors to Amazon CloudWatch logs.
        :param pulumi.Input[bool] enable_sip_logs: When true, enables SIP message logs for sending to Amazon CloudWatch Logs.
        """
        pulumi.set(__self__, "voice_connector_id", voice_connector_id)
        if enable_media_metric_logs is not None:
            pulumi.set(__self__, "enable_media_metric_logs", enable_media_metric_logs)
        if enable_sip_logs is not None:
            pulumi.set(__self__, "enable_sip_logs", enable_sip_logs)

    @property
    @pulumi.getter(name="voiceConnectorId")
    def voice_connector_id(self) -> pulumi.Input[str]:
        """
        The Amazon Chime Voice Connector ID.
        """
        return pulumi.get(self, "voice_connector_id")

    @voice_connector_id.setter
    def voice_connector_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "voice_connector_id", value)

    @property
    @pulumi.getter(name="enableMediaMetricLogs")
    def enable_media_metric_logs(self) -> Optional[pulumi.Input[bool]]:
        """
        When true, enables logging of detailed media metrics for Voice Connectors to Amazon CloudWatch logs.
        """
        return pulumi.get(self, "enable_media_metric_logs")

    @enable_media_metric_logs.setter
    def enable_media_metric_logs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_media_metric_logs", value)

    @property
    @pulumi.getter(name="enableSipLogs")
    def enable_sip_logs(self) -> Optional[pulumi.Input[bool]]:
        """
        When true, enables SIP message logs for sending to Amazon CloudWatch Logs.
        """
        return pulumi.get(self, "enable_sip_logs")

    @enable_sip_logs.setter
    def enable_sip_logs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_sip_logs", value)


@pulumi.input_type
class _VoiceConnectorLoggingState:
    def __init__(__self__, *,
                 enable_media_metric_logs: Optional[pulumi.Input[bool]] = None,
                 enable_sip_logs: Optional[pulumi.Input[bool]] = None,
                 voice_connector_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering VoiceConnectorLogging resources.
        :param pulumi.Input[bool] enable_media_metric_logs: When true, enables logging of detailed media metrics for Voice Connectors to Amazon CloudWatch logs.
        :param pulumi.Input[bool] enable_sip_logs: When true, enables SIP message logs for sending to Amazon CloudWatch Logs.
        :param pulumi.Input[str] voice_connector_id: The Amazon Chime Voice Connector ID.
        """
        if enable_media_metric_logs is not None:
            pulumi.set(__self__, "enable_media_metric_logs", enable_media_metric_logs)
        if enable_sip_logs is not None:
            pulumi.set(__self__, "enable_sip_logs", enable_sip_logs)
        if voice_connector_id is not None:
            pulumi.set(__self__, "voice_connector_id", voice_connector_id)

    @property
    @pulumi.getter(name="enableMediaMetricLogs")
    def enable_media_metric_logs(self) -> Optional[pulumi.Input[bool]]:
        """
        When true, enables logging of detailed media metrics for Voice Connectors to Amazon CloudWatch logs.
        """
        return pulumi.get(self, "enable_media_metric_logs")

    @enable_media_metric_logs.setter
    def enable_media_metric_logs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_media_metric_logs", value)

    @property
    @pulumi.getter(name="enableSipLogs")
    def enable_sip_logs(self) -> Optional[pulumi.Input[bool]]:
        """
        When true, enables SIP message logs for sending to Amazon CloudWatch Logs.
        """
        return pulumi.get(self, "enable_sip_logs")

    @enable_sip_logs.setter
    def enable_sip_logs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_sip_logs", value)

    @property
    @pulumi.getter(name="voiceConnectorId")
    def voice_connector_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Chime Voice Connector ID.
        """
        return pulumi.get(self, "voice_connector_id")

    @voice_connector_id.setter
    def voice_connector_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "voice_connector_id", value)


class VoiceConnectorLogging(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable_media_metric_logs: Optional[pulumi.Input[bool]] = None,
                 enable_sip_logs: Optional[pulumi.Input[bool]] = None,
                 voice_connector_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Adds a logging configuration for the specified Amazon Chime Voice Connector. The logging configuration specifies whether SIP message logs are enabled for sending to Amazon CloudWatch Logs.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default = aws.chime.VoiceConnector("default",
            name="vc-name-test",
            require_encryption=True)
        default_voice_connector_logging = aws.chime.VoiceConnectorLogging("default",
            enable_sip_logs=True,
            enable_media_metric_logs=True,
            voice_connector_id=default.id)
        ```

        ## Import

        Using `pulumi import`, import Chime Voice Connector Logging using the `voice_connector_id`. For example:

        ```sh
        $ pulumi import aws:chime/voiceConnectorLogging:VoiceConnectorLogging default abcdef1ghij2klmno3pqr4
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enable_media_metric_logs: When true, enables logging of detailed media metrics for Voice Connectors to Amazon CloudWatch logs.
        :param pulumi.Input[bool] enable_sip_logs: When true, enables SIP message logs for sending to Amazon CloudWatch Logs.
        :param pulumi.Input[str] voice_connector_id: The Amazon Chime Voice Connector ID.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VoiceConnectorLoggingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Adds a logging configuration for the specified Amazon Chime Voice Connector. The logging configuration specifies whether SIP message logs are enabled for sending to Amazon CloudWatch Logs.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        default = aws.chime.VoiceConnector("default",
            name="vc-name-test",
            require_encryption=True)
        default_voice_connector_logging = aws.chime.VoiceConnectorLogging("default",
            enable_sip_logs=True,
            enable_media_metric_logs=True,
            voice_connector_id=default.id)
        ```

        ## Import

        Using `pulumi import`, import Chime Voice Connector Logging using the `voice_connector_id`. For example:

        ```sh
        $ pulumi import aws:chime/voiceConnectorLogging:VoiceConnectorLogging default abcdef1ghij2klmno3pqr4
        ```

        :param str resource_name: The name of the resource.
        :param VoiceConnectorLoggingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VoiceConnectorLoggingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable_media_metric_logs: Optional[pulumi.Input[bool]] = None,
                 enable_sip_logs: Optional[pulumi.Input[bool]] = None,
                 voice_connector_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VoiceConnectorLoggingArgs.__new__(VoiceConnectorLoggingArgs)

            __props__.__dict__["enable_media_metric_logs"] = enable_media_metric_logs
            __props__.__dict__["enable_sip_logs"] = enable_sip_logs
            if voice_connector_id is None and not opts.urn:
                raise TypeError("Missing required property 'voice_connector_id'")
            __props__.__dict__["voice_connector_id"] = voice_connector_id
        super(VoiceConnectorLogging, __self__).__init__(
            'aws:chime/voiceConnectorLogging:VoiceConnectorLogging',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            enable_media_metric_logs: Optional[pulumi.Input[bool]] = None,
            enable_sip_logs: Optional[pulumi.Input[bool]] = None,
            voice_connector_id: Optional[pulumi.Input[str]] = None) -> 'VoiceConnectorLogging':
        """
        Get an existing VoiceConnectorLogging resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enable_media_metric_logs: When true, enables logging of detailed media metrics for Voice Connectors to Amazon CloudWatch logs.
        :param pulumi.Input[bool] enable_sip_logs: When true, enables SIP message logs for sending to Amazon CloudWatch Logs.
        :param pulumi.Input[str] voice_connector_id: The Amazon Chime Voice Connector ID.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VoiceConnectorLoggingState.__new__(_VoiceConnectorLoggingState)

        __props__.__dict__["enable_media_metric_logs"] = enable_media_metric_logs
        __props__.__dict__["enable_sip_logs"] = enable_sip_logs
        __props__.__dict__["voice_connector_id"] = voice_connector_id
        return VoiceConnectorLogging(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="enableMediaMetricLogs")
    def enable_media_metric_logs(self) -> pulumi.Output[Optional[bool]]:
        """
        When true, enables logging of detailed media metrics for Voice Connectors to Amazon CloudWatch logs.
        """
        return pulumi.get(self, "enable_media_metric_logs")

    @property
    @pulumi.getter(name="enableSipLogs")
    def enable_sip_logs(self) -> pulumi.Output[Optional[bool]]:
        """
        When true, enables SIP message logs for sending to Amazon CloudWatch Logs.
        """
        return pulumi.get(self, "enable_sip_logs")

    @property
    @pulumi.getter(name="voiceConnectorId")
    def voice_connector_id(self) -> pulumi.Output[str]:
        """
        The Amazon Chime Voice Connector ID.
        """
        return pulumi.get(self, "voice_connector_id")

