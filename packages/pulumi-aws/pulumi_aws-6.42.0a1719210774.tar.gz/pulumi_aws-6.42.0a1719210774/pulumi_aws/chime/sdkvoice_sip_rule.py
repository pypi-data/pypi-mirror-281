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

__all__ = ['SdkvoiceSipRuleArgs', 'SdkvoiceSipRule']

@pulumi.input_type
class SdkvoiceSipRuleArgs:
    def __init__(__self__, *,
                 target_applications: pulumi.Input[Sequence[pulumi.Input['SdkvoiceSipRuleTargetApplicationArgs']]],
                 trigger_type: pulumi.Input[str],
                 trigger_value: pulumi.Input[str],
                 disabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SdkvoiceSipRule resource.
        :param pulumi.Input[Sequence[pulumi.Input['SdkvoiceSipRuleTargetApplicationArgs']]] target_applications: List of SIP media applications with priority and AWS Region. Only one SIP application per AWS Region can be used. See `target_applications`.
        :param pulumi.Input[str] trigger_type: The type of trigger assigned to the SIP rule in `trigger_value`. Valid values are `RequestUriHostname` or `ToPhoneNumber`.
        :param pulumi.Input[str] trigger_value: If `trigger_type` is `RequestUriHostname`, the value can be the outbound host name of an Amazon Chime Voice Connector. If `trigger_type` is `ToPhoneNumber`, the value can be a customer-owned phone number in the E164 format. The Sip Media Application specified in the Sip Rule is triggered if the request URI in an incoming SIP request matches the `RequestUriHostname`, or if the "To" header in the incoming SIP request matches the `ToPhoneNumber` value.
               
               The following arguments are optional:
        :param pulumi.Input[bool] disabled: Enables or disables a rule. You must disable rules before you can delete them.
        :param pulumi.Input[str] name: The name of the SIP rule.
        """
        pulumi.set(__self__, "target_applications", target_applications)
        pulumi.set(__self__, "trigger_type", trigger_type)
        pulumi.set(__self__, "trigger_value", trigger_value)
        if disabled is not None:
            pulumi.set(__self__, "disabled", disabled)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="targetApplications")
    def target_applications(self) -> pulumi.Input[Sequence[pulumi.Input['SdkvoiceSipRuleTargetApplicationArgs']]]:
        """
        List of SIP media applications with priority and AWS Region. Only one SIP application per AWS Region can be used. See `target_applications`.
        """
        return pulumi.get(self, "target_applications")

    @target_applications.setter
    def target_applications(self, value: pulumi.Input[Sequence[pulumi.Input['SdkvoiceSipRuleTargetApplicationArgs']]]):
        pulumi.set(self, "target_applications", value)

    @property
    @pulumi.getter(name="triggerType")
    def trigger_type(self) -> pulumi.Input[str]:
        """
        The type of trigger assigned to the SIP rule in `trigger_value`. Valid values are `RequestUriHostname` or `ToPhoneNumber`.
        """
        return pulumi.get(self, "trigger_type")

    @trigger_type.setter
    def trigger_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "trigger_type", value)

    @property
    @pulumi.getter(name="triggerValue")
    def trigger_value(self) -> pulumi.Input[str]:
        """
        If `trigger_type` is `RequestUriHostname`, the value can be the outbound host name of an Amazon Chime Voice Connector. If `trigger_type` is `ToPhoneNumber`, the value can be a customer-owned phone number in the E164 format. The Sip Media Application specified in the Sip Rule is triggered if the request URI in an incoming SIP request matches the `RequestUriHostname`, or if the "To" header in the incoming SIP request matches the `ToPhoneNumber` value.

        The following arguments are optional:
        """
        return pulumi.get(self, "trigger_value")

    @trigger_value.setter
    def trigger_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "trigger_value", value)

    @property
    @pulumi.getter
    def disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables or disables a rule. You must disable rules before you can delete them.
        """
        return pulumi.get(self, "disabled")

    @disabled.setter
    def disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the SIP rule.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _SdkvoiceSipRuleState:
    def __init__(__self__, *,
                 disabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 target_applications: Optional[pulumi.Input[Sequence[pulumi.Input['SdkvoiceSipRuleTargetApplicationArgs']]]] = None,
                 trigger_type: Optional[pulumi.Input[str]] = None,
                 trigger_value: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SdkvoiceSipRule resources.
        :param pulumi.Input[bool] disabled: Enables or disables a rule. You must disable rules before you can delete them.
        :param pulumi.Input[str] name: The name of the SIP rule.
        :param pulumi.Input[Sequence[pulumi.Input['SdkvoiceSipRuleTargetApplicationArgs']]] target_applications: List of SIP media applications with priority and AWS Region. Only one SIP application per AWS Region can be used. See `target_applications`.
        :param pulumi.Input[str] trigger_type: The type of trigger assigned to the SIP rule in `trigger_value`. Valid values are `RequestUriHostname` or `ToPhoneNumber`.
        :param pulumi.Input[str] trigger_value: If `trigger_type` is `RequestUriHostname`, the value can be the outbound host name of an Amazon Chime Voice Connector. If `trigger_type` is `ToPhoneNumber`, the value can be a customer-owned phone number in the E164 format. The Sip Media Application specified in the Sip Rule is triggered if the request URI in an incoming SIP request matches the `RequestUriHostname`, or if the "To" header in the incoming SIP request matches the `ToPhoneNumber` value.
               
               The following arguments are optional:
        """
        if disabled is not None:
            pulumi.set(__self__, "disabled", disabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if target_applications is not None:
            pulumi.set(__self__, "target_applications", target_applications)
        if trigger_type is not None:
            pulumi.set(__self__, "trigger_type", trigger_type)
        if trigger_value is not None:
            pulumi.set(__self__, "trigger_value", trigger_value)

    @property
    @pulumi.getter
    def disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables or disables a rule. You must disable rules before you can delete them.
        """
        return pulumi.get(self, "disabled")

    @disabled.setter
    def disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the SIP rule.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="targetApplications")
    def target_applications(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SdkvoiceSipRuleTargetApplicationArgs']]]]:
        """
        List of SIP media applications with priority and AWS Region. Only one SIP application per AWS Region can be used. See `target_applications`.
        """
        return pulumi.get(self, "target_applications")

    @target_applications.setter
    def target_applications(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SdkvoiceSipRuleTargetApplicationArgs']]]]):
        pulumi.set(self, "target_applications", value)

    @property
    @pulumi.getter(name="triggerType")
    def trigger_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of trigger assigned to the SIP rule in `trigger_value`. Valid values are `RequestUriHostname` or `ToPhoneNumber`.
        """
        return pulumi.get(self, "trigger_type")

    @trigger_type.setter
    def trigger_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trigger_type", value)

    @property
    @pulumi.getter(name="triggerValue")
    def trigger_value(self) -> Optional[pulumi.Input[str]]:
        """
        If `trigger_type` is `RequestUriHostname`, the value can be the outbound host name of an Amazon Chime Voice Connector. If `trigger_type` is `ToPhoneNumber`, the value can be a customer-owned phone number in the E164 format. The Sip Media Application specified in the Sip Rule is triggered if the request URI in an incoming SIP request matches the `RequestUriHostname`, or if the "To" header in the incoming SIP request matches the `ToPhoneNumber` value.

        The following arguments are optional:
        """
        return pulumi.get(self, "trigger_value")

    @trigger_value.setter
    def trigger_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trigger_value", value)


class SdkvoiceSipRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 disabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 target_applications: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SdkvoiceSipRuleTargetApplicationArgs']]]]] = None,
                 trigger_type: Optional[pulumi.Input[str]] = None,
                 trigger_value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A SIP rule associates your SIP media application with a phone number or a Request URI hostname. You can associate a SIP rule with more than one SIP media application. Each application then runs only that rule.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.chime.SdkvoiceSipRule("example",
            name="example-sip-rule",
            trigger_type="RequestUriHostname",
            trigger_value=example_voice_connector["outboundHostName"],
            target_applications=[aws.chime.SdkvoiceSipRuleTargetApplicationArgs(
                priority=1,
                sip_media_application_id=example_sma["id"],
                aws_region="us-east-1",
            )])
        ```

        ## Import

        Using `pulumi import`, import a ChimeSDKVoice SIP Rule using the `id`. For example:

        ```sh
        $ pulumi import aws:chime/sdkvoiceSipRule:SdkvoiceSipRule example abcdef123456
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] disabled: Enables or disables a rule. You must disable rules before you can delete them.
        :param pulumi.Input[str] name: The name of the SIP rule.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SdkvoiceSipRuleTargetApplicationArgs']]]] target_applications: List of SIP media applications with priority and AWS Region. Only one SIP application per AWS Region can be used. See `target_applications`.
        :param pulumi.Input[str] trigger_type: The type of trigger assigned to the SIP rule in `trigger_value`. Valid values are `RequestUriHostname` or `ToPhoneNumber`.
        :param pulumi.Input[str] trigger_value: If `trigger_type` is `RequestUriHostname`, the value can be the outbound host name of an Amazon Chime Voice Connector. If `trigger_type` is `ToPhoneNumber`, the value can be a customer-owned phone number in the E164 format. The Sip Media Application specified in the Sip Rule is triggered if the request URI in an incoming SIP request matches the `RequestUriHostname`, or if the "To" header in the incoming SIP request matches the `ToPhoneNumber` value.
               
               The following arguments are optional:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SdkvoiceSipRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A SIP rule associates your SIP media application with a phone number or a Request URI hostname. You can associate a SIP rule with more than one SIP media application. Each application then runs only that rule.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.chime.SdkvoiceSipRule("example",
            name="example-sip-rule",
            trigger_type="RequestUriHostname",
            trigger_value=example_voice_connector["outboundHostName"],
            target_applications=[aws.chime.SdkvoiceSipRuleTargetApplicationArgs(
                priority=1,
                sip_media_application_id=example_sma["id"],
                aws_region="us-east-1",
            )])
        ```

        ## Import

        Using `pulumi import`, import a ChimeSDKVoice SIP Rule using the `id`. For example:

        ```sh
        $ pulumi import aws:chime/sdkvoiceSipRule:SdkvoiceSipRule example abcdef123456
        ```

        :param str resource_name: The name of the resource.
        :param SdkvoiceSipRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SdkvoiceSipRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 disabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 target_applications: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SdkvoiceSipRuleTargetApplicationArgs']]]]] = None,
                 trigger_type: Optional[pulumi.Input[str]] = None,
                 trigger_value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SdkvoiceSipRuleArgs.__new__(SdkvoiceSipRuleArgs)

            __props__.__dict__["disabled"] = disabled
            __props__.__dict__["name"] = name
            if target_applications is None and not opts.urn:
                raise TypeError("Missing required property 'target_applications'")
            __props__.__dict__["target_applications"] = target_applications
            if trigger_type is None and not opts.urn:
                raise TypeError("Missing required property 'trigger_type'")
            __props__.__dict__["trigger_type"] = trigger_type
            if trigger_value is None and not opts.urn:
                raise TypeError("Missing required property 'trigger_value'")
            __props__.__dict__["trigger_value"] = trigger_value
        super(SdkvoiceSipRule, __self__).__init__(
            'aws:chime/sdkvoiceSipRule:SdkvoiceSipRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            disabled: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            target_applications: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SdkvoiceSipRuleTargetApplicationArgs']]]]] = None,
            trigger_type: Optional[pulumi.Input[str]] = None,
            trigger_value: Optional[pulumi.Input[str]] = None) -> 'SdkvoiceSipRule':
        """
        Get an existing SdkvoiceSipRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] disabled: Enables or disables a rule. You must disable rules before you can delete them.
        :param pulumi.Input[str] name: The name of the SIP rule.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SdkvoiceSipRuleTargetApplicationArgs']]]] target_applications: List of SIP media applications with priority and AWS Region. Only one SIP application per AWS Region can be used. See `target_applications`.
        :param pulumi.Input[str] trigger_type: The type of trigger assigned to the SIP rule in `trigger_value`. Valid values are `RequestUriHostname` or `ToPhoneNumber`.
        :param pulumi.Input[str] trigger_value: If `trigger_type` is `RequestUriHostname`, the value can be the outbound host name of an Amazon Chime Voice Connector. If `trigger_type` is `ToPhoneNumber`, the value can be a customer-owned phone number in the E164 format. The Sip Media Application specified in the Sip Rule is triggered if the request URI in an incoming SIP request matches the `RequestUriHostname`, or if the "To" header in the incoming SIP request matches the `ToPhoneNumber` value.
               
               The following arguments are optional:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SdkvoiceSipRuleState.__new__(_SdkvoiceSipRuleState)

        __props__.__dict__["disabled"] = disabled
        __props__.__dict__["name"] = name
        __props__.__dict__["target_applications"] = target_applications
        __props__.__dict__["trigger_type"] = trigger_type
        __props__.__dict__["trigger_value"] = trigger_value
        return SdkvoiceSipRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def disabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables or disables a rule. You must disable rules before you can delete them.
        """
        return pulumi.get(self, "disabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the SIP rule.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="targetApplications")
    def target_applications(self) -> pulumi.Output[Sequence['outputs.SdkvoiceSipRuleTargetApplication']]:
        """
        List of SIP media applications with priority and AWS Region. Only one SIP application per AWS Region can be used. See `target_applications`.
        """
        return pulumi.get(self, "target_applications")

    @property
    @pulumi.getter(name="triggerType")
    def trigger_type(self) -> pulumi.Output[str]:
        """
        The type of trigger assigned to the SIP rule in `trigger_value`. Valid values are `RequestUriHostname` or `ToPhoneNumber`.
        """
        return pulumi.get(self, "trigger_type")

    @property
    @pulumi.getter(name="triggerValue")
    def trigger_value(self) -> pulumi.Output[str]:
        """
        If `trigger_type` is `RequestUriHostname`, the value can be the outbound host name of an Amazon Chime Voice Connector. If `trigger_type` is `ToPhoneNumber`, the value can be a customer-owned phone number in the E164 format. The Sip Media Application specified in the Sip Rule is triggered if the request URI in an incoming SIP request matches the `RequestUriHostname`, or if the "To" header in the incoming SIP request matches the `ToPhoneNumber` value.

        The following arguments are optional:
        """
        return pulumi.get(self, "trigger_value")

