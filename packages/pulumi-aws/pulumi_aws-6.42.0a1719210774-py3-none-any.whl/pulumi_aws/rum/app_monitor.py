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

__all__ = ['AppMonitorArgs', 'AppMonitor']

@pulumi.input_type
class AppMonitorArgs:
    def __init__(__self__, *,
                 domain: pulumi.Input[str],
                 app_monitor_configuration: Optional[pulumi.Input['AppMonitorAppMonitorConfigurationArgs']] = None,
                 custom_events: Optional[pulumi.Input['AppMonitorCustomEventsArgs']] = None,
                 cw_log_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AppMonitor resource.
        :param pulumi.Input[str] domain: The top-level internet domain name for which your application has administrative authority.
        :param pulumi.Input['AppMonitorAppMonitorConfigurationArgs'] app_monitor_configuration: configuration data for the app monitor. See app_monitor_configuration below.
        :param pulumi.Input['AppMonitorCustomEventsArgs'] custom_events: Specifies whether this app monitor allows the web client to define and send custom events. If you omit this parameter, custom events are `DISABLED`. See custom_events below.
        :param pulumi.Input[bool] cw_log_enabled: Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter  specifies whether RUM sends a copy of this telemetry data to Amazon CloudWatch Logs in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur Amazon CloudWatch Logs charges. Default value is `false`.
        :param pulumi.Input[str] name: The name of the log stream.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "domain", domain)
        if app_monitor_configuration is not None:
            pulumi.set(__self__, "app_monitor_configuration", app_monitor_configuration)
        if custom_events is not None:
            pulumi.set(__self__, "custom_events", custom_events)
        if cw_log_enabled is not None:
            pulumi.set(__self__, "cw_log_enabled", cw_log_enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Input[str]:
        """
        The top-level internet domain name for which your application has administrative authority.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter(name="appMonitorConfiguration")
    def app_monitor_configuration(self) -> Optional[pulumi.Input['AppMonitorAppMonitorConfigurationArgs']]:
        """
        configuration data for the app monitor. See app_monitor_configuration below.
        """
        return pulumi.get(self, "app_monitor_configuration")

    @app_monitor_configuration.setter
    def app_monitor_configuration(self, value: Optional[pulumi.Input['AppMonitorAppMonitorConfigurationArgs']]):
        pulumi.set(self, "app_monitor_configuration", value)

    @property
    @pulumi.getter(name="customEvents")
    def custom_events(self) -> Optional[pulumi.Input['AppMonitorCustomEventsArgs']]:
        """
        Specifies whether this app monitor allows the web client to define and send custom events. If you omit this parameter, custom events are `DISABLED`. See custom_events below.
        """
        return pulumi.get(self, "custom_events")

    @custom_events.setter
    def custom_events(self, value: Optional[pulumi.Input['AppMonitorCustomEventsArgs']]):
        pulumi.set(self, "custom_events", value)

    @property
    @pulumi.getter(name="cwLogEnabled")
    def cw_log_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter  specifies whether RUM sends a copy of this telemetry data to Amazon CloudWatch Logs in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur Amazon CloudWatch Logs charges. Default value is `false`.
        """
        return pulumi.get(self, "cw_log_enabled")

    @cw_log_enabled.setter
    def cw_log_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cw_log_enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the log stream.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _AppMonitorState:
    def __init__(__self__, *,
                 app_monitor_configuration: Optional[pulumi.Input['AppMonitorAppMonitorConfigurationArgs']] = None,
                 app_monitor_id: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 custom_events: Optional[pulumi.Input['AppMonitorCustomEventsArgs']] = None,
                 cw_log_enabled: Optional[pulumi.Input[bool]] = None,
                 cw_log_group: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering AppMonitor resources.
        :param pulumi.Input['AppMonitorAppMonitorConfigurationArgs'] app_monitor_configuration: configuration data for the app monitor. See app_monitor_configuration below.
        :param pulumi.Input[str] app_monitor_id: The unique ID of the app monitor. Useful for JS templates.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) specifying the app monitor.
        :param pulumi.Input['AppMonitorCustomEventsArgs'] custom_events: Specifies whether this app monitor allows the web client to define and send custom events. If you omit this parameter, custom events are `DISABLED`. See custom_events below.
        :param pulumi.Input[bool] cw_log_enabled: Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter  specifies whether RUM sends a copy of this telemetry data to Amazon CloudWatch Logs in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur Amazon CloudWatch Logs charges. Default value is `false`.
        :param pulumi.Input[str] cw_log_group: The name of the log group where the copies are stored.
        :param pulumi.Input[str] domain: The top-level internet domain name for which your application has administrative authority.
        :param pulumi.Input[str] name: The name of the log stream.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if app_monitor_configuration is not None:
            pulumi.set(__self__, "app_monitor_configuration", app_monitor_configuration)
        if app_monitor_id is not None:
            pulumi.set(__self__, "app_monitor_id", app_monitor_id)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if custom_events is not None:
            pulumi.set(__self__, "custom_events", custom_events)
        if cw_log_enabled is not None:
            pulumi.set(__self__, "cw_log_enabled", cw_log_enabled)
        if cw_log_group is not None:
            pulumi.set(__self__, "cw_log_group", cw_log_group)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter(name="appMonitorConfiguration")
    def app_monitor_configuration(self) -> Optional[pulumi.Input['AppMonitorAppMonitorConfigurationArgs']]:
        """
        configuration data for the app monitor. See app_monitor_configuration below.
        """
        return pulumi.get(self, "app_monitor_configuration")

    @app_monitor_configuration.setter
    def app_monitor_configuration(self, value: Optional[pulumi.Input['AppMonitorAppMonitorConfigurationArgs']]):
        pulumi.set(self, "app_monitor_configuration", value)

    @property
    @pulumi.getter(name="appMonitorId")
    def app_monitor_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique ID of the app monitor. Useful for JS templates.
        """
        return pulumi.get(self, "app_monitor_id")

    @app_monitor_id.setter
    def app_monitor_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_monitor_id", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) specifying the app monitor.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="customEvents")
    def custom_events(self) -> Optional[pulumi.Input['AppMonitorCustomEventsArgs']]:
        """
        Specifies whether this app monitor allows the web client to define and send custom events. If you omit this parameter, custom events are `DISABLED`. See custom_events below.
        """
        return pulumi.get(self, "custom_events")

    @custom_events.setter
    def custom_events(self, value: Optional[pulumi.Input['AppMonitorCustomEventsArgs']]):
        pulumi.set(self, "custom_events", value)

    @property
    @pulumi.getter(name="cwLogEnabled")
    def cw_log_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter  specifies whether RUM sends a copy of this telemetry data to Amazon CloudWatch Logs in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur Amazon CloudWatch Logs charges. Default value is `false`.
        """
        return pulumi.get(self, "cw_log_enabled")

    @cw_log_enabled.setter
    def cw_log_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cw_log_enabled", value)

    @property
    @pulumi.getter(name="cwLogGroup")
    def cw_log_group(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the log group where the copies are stored.
        """
        return pulumi.get(self, "cw_log_group")

    @cw_log_group.setter
    def cw_log_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cw_log_group", value)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        """
        The top-level internet domain name for which your application has administrative authority.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the log stream.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class AppMonitor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_monitor_configuration: Optional[pulumi.Input[pulumi.InputType['AppMonitorAppMonitorConfigurationArgs']]] = None,
                 custom_events: Optional[pulumi.Input[pulumi.InputType['AppMonitorCustomEventsArgs']]] = None,
                 cw_log_enabled: Optional[pulumi.Input[bool]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a CloudWatch RUM App Monitor resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.rum.AppMonitor("example",
            name="example",
            domain="localhost")
        ```

        ## Import

        Using `pulumi import`, import Cloudwatch RUM App Monitor using the `name`. For example:

        ```sh
        $ pulumi import aws:rum/appMonitor:AppMonitor example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AppMonitorAppMonitorConfigurationArgs']] app_monitor_configuration: configuration data for the app monitor. See app_monitor_configuration below.
        :param pulumi.Input[pulumi.InputType['AppMonitorCustomEventsArgs']] custom_events: Specifies whether this app monitor allows the web client to define and send custom events. If you omit this parameter, custom events are `DISABLED`. See custom_events below.
        :param pulumi.Input[bool] cw_log_enabled: Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter  specifies whether RUM sends a copy of this telemetry data to Amazon CloudWatch Logs in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur Amazon CloudWatch Logs charges. Default value is `false`.
        :param pulumi.Input[str] domain: The top-level internet domain name for which your application has administrative authority.
        :param pulumi.Input[str] name: The name of the log stream.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AppMonitorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CloudWatch RUM App Monitor resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.rum.AppMonitor("example",
            name="example",
            domain="localhost")
        ```

        ## Import

        Using `pulumi import`, import Cloudwatch RUM App Monitor using the `name`. For example:

        ```sh
        $ pulumi import aws:rum/appMonitor:AppMonitor example example
        ```

        :param str resource_name: The name of the resource.
        :param AppMonitorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppMonitorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_monitor_configuration: Optional[pulumi.Input[pulumi.InputType['AppMonitorAppMonitorConfigurationArgs']]] = None,
                 custom_events: Optional[pulumi.Input[pulumi.InputType['AppMonitorCustomEventsArgs']]] = None,
                 cw_log_enabled: Optional[pulumi.Input[bool]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AppMonitorArgs.__new__(AppMonitorArgs)

            __props__.__dict__["app_monitor_configuration"] = app_monitor_configuration
            __props__.__dict__["custom_events"] = custom_events
            __props__.__dict__["cw_log_enabled"] = cw_log_enabled
            if domain is None and not opts.urn:
                raise TypeError("Missing required property 'domain'")
            __props__.__dict__["domain"] = domain
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["app_monitor_id"] = None
            __props__.__dict__["arn"] = None
            __props__.__dict__["cw_log_group"] = None
            __props__.__dict__["tags_all"] = None
        super(AppMonitor, __self__).__init__(
            'aws:rum/appMonitor:AppMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            app_monitor_configuration: Optional[pulumi.Input[pulumi.InputType['AppMonitorAppMonitorConfigurationArgs']]] = None,
            app_monitor_id: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            custom_events: Optional[pulumi.Input[pulumi.InputType['AppMonitorCustomEventsArgs']]] = None,
            cw_log_enabled: Optional[pulumi.Input[bool]] = None,
            cw_log_group: Optional[pulumi.Input[str]] = None,
            domain: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'AppMonitor':
        """
        Get an existing AppMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AppMonitorAppMonitorConfigurationArgs']] app_monitor_configuration: configuration data for the app monitor. See app_monitor_configuration below.
        :param pulumi.Input[str] app_monitor_id: The unique ID of the app monitor. Useful for JS templates.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) specifying the app monitor.
        :param pulumi.Input[pulumi.InputType['AppMonitorCustomEventsArgs']] custom_events: Specifies whether this app monitor allows the web client to define and send custom events. If you omit this parameter, custom events are `DISABLED`. See custom_events below.
        :param pulumi.Input[bool] cw_log_enabled: Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter  specifies whether RUM sends a copy of this telemetry data to Amazon CloudWatch Logs in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur Amazon CloudWatch Logs charges. Default value is `false`.
        :param pulumi.Input[str] cw_log_group: The name of the log group where the copies are stored.
        :param pulumi.Input[str] domain: The top-level internet domain name for which your application has administrative authority.
        :param pulumi.Input[str] name: The name of the log stream.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AppMonitorState.__new__(_AppMonitorState)

        __props__.__dict__["app_monitor_configuration"] = app_monitor_configuration
        __props__.__dict__["app_monitor_id"] = app_monitor_id
        __props__.__dict__["arn"] = arn
        __props__.__dict__["custom_events"] = custom_events
        __props__.__dict__["cw_log_enabled"] = cw_log_enabled
        __props__.__dict__["cw_log_group"] = cw_log_group
        __props__.__dict__["domain"] = domain
        __props__.__dict__["name"] = name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return AppMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appMonitorConfiguration")
    def app_monitor_configuration(self) -> pulumi.Output['outputs.AppMonitorAppMonitorConfiguration']:
        """
        configuration data for the app monitor. See app_monitor_configuration below.
        """
        return pulumi.get(self, "app_monitor_configuration")

    @property
    @pulumi.getter(name="appMonitorId")
    def app_monitor_id(self) -> pulumi.Output[str]:
        """
        The unique ID of the app monitor. Useful for JS templates.
        """
        return pulumi.get(self, "app_monitor_id")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) specifying the app monitor.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="customEvents")
    def custom_events(self) -> pulumi.Output['outputs.AppMonitorCustomEvents']:
        """
        Specifies whether this app monitor allows the web client to define and send custom events. If you omit this parameter, custom events are `DISABLED`. See custom_events below.
        """
        return pulumi.get(self, "custom_events")

    @property
    @pulumi.getter(name="cwLogEnabled")
    def cw_log_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter  specifies whether RUM sends a copy of this telemetry data to Amazon CloudWatch Logs in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur Amazon CloudWatch Logs charges. Default value is `false`.
        """
        return pulumi.get(self, "cw_log_enabled")

    @property
    @pulumi.getter(name="cwLogGroup")
    def cw_log_group(self) -> pulumi.Output[str]:
        """
        The name of the log group where the copies are stored.
        """
        return pulumi.get(self, "cw_log_group")

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Output[str]:
        """
        The top-level internet domain name for which your application has administrative authority.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the log stream.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

