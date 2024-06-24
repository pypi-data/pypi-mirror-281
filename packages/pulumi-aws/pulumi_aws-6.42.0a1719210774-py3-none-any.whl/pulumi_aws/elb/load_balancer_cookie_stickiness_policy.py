# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['LoadBalancerCookieStickinessPolicyArgs', 'LoadBalancerCookieStickinessPolicy']

@pulumi.input_type
class LoadBalancerCookieStickinessPolicyArgs:
    def __init__(__self__, *,
                 lb_port: pulumi.Input[int],
                 load_balancer: pulumi.Input[str],
                 cookie_expiration_period: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a LoadBalancerCookieStickinessPolicy resource.
        :param pulumi.Input[int] lb_port: The load balancer port to which the policy
               should be applied. This must be an active listener on the load
               balancer.
        :param pulumi.Input[str] load_balancer: The load balancer to which the policy
               should be attached.
        :param pulumi.Input[int] cookie_expiration_period: The time period after which
               the session cookie should be considered stale, expressed in seconds.
        :param pulumi.Input[str] name: The name of the stickiness policy.
        """
        pulumi.set(__self__, "lb_port", lb_port)
        pulumi.set(__self__, "load_balancer", load_balancer)
        if cookie_expiration_period is not None:
            pulumi.set(__self__, "cookie_expiration_period", cookie_expiration_period)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="lbPort")
    def lb_port(self) -> pulumi.Input[int]:
        """
        The load balancer port to which the policy
        should be applied. This must be an active listener on the load
        balancer.
        """
        return pulumi.get(self, "lb_port")

    @lb_port.setter
    def lb_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "lb_port", value)

    @property
    @pulumi.getter(name="loadBalancer")
    def load_balancer(self) -> pulumi.Input[str]:
        """
        The load balancer to which the policy
        should be attached.
        """
        return pulumi.get(self, "load_balancer")

    @load_balancer.setter
    def load_balancer(self, value: pulumi.Input[str]):
        pulumi.set(self, "load_balancer", value)

    @property
    @pulumi.getter(name="cookieExpirationPeriod")
    def cookie_expiration_period(self) -> Optional[pulumi.Input[int]]:
        """
        The time period after which
        the session cookie should be considered stale, expressed in seconds.
        """
        return pulumi.get(self, "cookie_expiration_period")

    @cookie_expiration_period.setter
    def cookie_expiration_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cookie_expiration_period", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the stickiness policy.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _LoadBalancerCookieStickinessPolicyState:
    def __init__(__self__, *,
                 cookie_expiration_period: Optional[pulumi.Input[int]] = None,
                 lb_port: Optional[pulumi.Input[int]] = None,
                 load_balancer: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LoadBalancerCookieStickinessPolicy resources.
        :param pulumi.Input[int] cookie_expiration_period: The time period after which
               the session cookie should be considered stale, expressed in seconds.
        :param pulumi.Input[int] lb_port: The load balancer port to which the policy
               should be applied. This must be an active listener on the load
               balancer.
        :param pulumi.Input[str] load_balancer: The load balancer to which the policy
               should be attached.
        :param pulumi.Input[str] name: The name of the stickiness policy.
        """
        if cookie_expiration_period is not None:
            pulumi.set(__self__, "cookie_expiration_period", cookie_expiration_period)
        if lb_port is not None:
            pulumi.set(__self__, "lb_port", lb_port)
        if load_balancer is not None:
            pulumi.set(__self__, "load_balancer", load_balancer)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="cookieExpirationPeriod")
    def cookie_expiration_period(self) -> Optional[pulumi.Input[int]]:
        """
        The time period after which
        the session cookie should be considered stale, expressed in seconds.
        """
        return pulumi.get(self, "cookie_expiration_period")

    @cookie_expiration_period.setter
    def cookie_expiration_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cookie_expiration_period", value)

    @property
    @pulumi.getter(name="lbPort")
    def lb_port(self) -> Optional[pulumi.Input[int]]:
        """
        The load balancer port to which the policy
        should be applied. This must be an active listener on the load
        balancer.
        """
        return pulumi.get(self, "lb_port")

    @lb_port.setter
    def lb_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "lb_port", value)

    @property
    @pulumi.getter(name="loadBalancer")
    def load_balancer(self) -> Optional[pulumi.Input[str]]:
        """
        The load balancer to which the policy
        should be attached.
        """
        return pulumi.get(self, "load_balancer")

    @load_balancer.setter
    def load_balancer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "load_balancer", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the stickiness policy.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class LoadBalancerCookieStickinessPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cookie_expiration_period: Optional[pulumi.Input[int]] = None,
                 lb_port: Optional[pulumi.Input[int]] = None,
                 load_balancer: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a load balancer cookie stickiness policy, which allows an ELB to control the sticky session lifetime of the browser.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        lb = aws.elb.LoadBalancer("lb",
            name="test-lb",
            availability_zones=["us-east-1a"],
            listeners=[aws.elb.LoadBalancerListenerArgs(
                instance_port=8000,
                instance_protocol="http",
                lb_port=80,
                lb_protocol="http",
            )])
        foo = aws.elb.LoadBalancerCookieStickinessPolicy("foo",
            name="foo-policy",
            load_balancer=lb.id,
            lb_port=80,
            cookie_expiration_period=600)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] cookie_expiration_period: The time period after which
               the session cookie should be considered stale, expressed in seconds.
        :param pulumi.Input[int] lb_port: The load balancer port to which the policy
               should be applied. This must be an active listener on the load
               balancer.
        :param pulumi.Input[str] load_balancer: The load balancer to which the policy
               should be attached.
        :param pulumi.Input[str] name: The name of the stickiness policy.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LoadBalancerCookieStickinessPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a load balancer cookie stickiness policy, which allows an ELB to control the sticky session lifetime of the browser.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        lb = aws.elb.LoadBalancer("lb",
            name="test-lb",
            availability_zones=["us-east-1a"],
            listeners=[aws.elb.LoadBalancerListenerArgs(
                instance_port=8000,
                instance_protocol="http",
                lb_port=80,
                lb_protocol="http",
            )])
        foo = aws.elb.LoadBalancerCookieStickinessPolicy("foo",
            name="foo-policy",
            load_balancer=lb.id,
            lb_port=80,
            cookie_expiration_period=600)
        ```

        :param str resource_name: The name of the resource.
        :param LoadBalancerCookieStickinessPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LoadBalancerCookieStickinessPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cookie_expiration_period: Optional[pulumi.Input[int]] = None,
                 lb_port: Optional[pulumi.Input[int]] = None,
                 load_balancer: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LoadBalancerCookieStickinessPolicyArgs.__new__(LoadBalancerCookieStickinessPolicyArgs)

            __props__.__dict__["cookie_expiration_period"] = cookie_expiration_period
            if lb_port is None and not opts.urn:
                raise TypeError("Missing required property 'lb_port'")
            __props__.__dict__["lb_port"] = lb_port
            if load_balancer is None and not opts.urn:
                raise TypeError("Missing required property 'load_balancer'")
            __props__.__dict__["load_balancer"] = load_balancer
            __props__.__dict__["name"] = name
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="aws:elasticloadbalancing/loadBalancerCookieStickinessPolicy:LoadBalancerCookieStickinessPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(LoadBalancerCookieStickinessPolicy, __self__).__init__(
            'aws:elb/loadBalancerCookieStickinessPolicy:LoadBalancerCookieStickinessPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cookie_expiration_period: Optional[pulumi.Input[int]] = None,
            lb_port: Optional[pulumi.Input[int]] = None,
            load_balancer: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'LoadBalancerCookieStickinessPolicy':
        """
        Get an existing LoadBalancerCookieStickinessPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] cookie_expiration_period: The time period after which
               the session cookie should be considered stale, expressed in seconds.
        :param pulumi.Input[int] lb_port: The load balancer port to which the policy
               should be applied. This must be an active listener on the load
               balancer.
        :param pulumi.Input[str] load_balancer: The load balancer to which the policy
               should be attached.
        :param pulumi.Input[str] name: The name of the stickiness policy.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LoadBalancerCookieStickinessPolicyState.__new__(_LoadBalancerCookieStickinessPolicyState)

        __props__.__dict__["cookie_expiration_period"] = cookie_expiration_period
        __props__.__dict__["lb_port"] = lb_port
        __props__.__dict__["load_balancer"] = load_balancer
        __props__.__dict__["name"] = name
        return LoadBalancerCookieStickinessPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cookieExpirationPeriod")
    def cookie_expiration_period(self) -> pulumi.Output[Optional[int]]:
        """
        The time period after which
        the session cookie should be considered stale, expressed in seconds.
        """
        return pulumi.get(self, "cookie_expiration_period")

    @property
    @pulumi.getter(name="lbPort")
    def lb_port(self) -> pulumi.Output[int]:
        """
        The load balancer port to which the policy
        should be applied. This must be an active listener on the load
        balancer.
        """
        return pulumi.get(self, "lb_port")

    @property
    @pulumi.getter(name="loadBalancer")
    def load_balancer(self) -> pulumi.Output[str]:
        """
        The load balancer to which the policy
        should be attached.
        """
        return pulumi.get(self, "load_balancer")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the stickiness policy.
        """
        return pulumi.get(self, "name")

