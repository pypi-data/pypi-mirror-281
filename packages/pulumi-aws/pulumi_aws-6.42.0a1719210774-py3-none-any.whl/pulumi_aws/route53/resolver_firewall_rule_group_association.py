# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ResolverFirewallRuleGroupAssociationArgs', 'ResolverFirewallRuleGroupAssociation']

@pulumi.input_type
class ResolverFirewallRuleGroupAssociationArgs:
    def __init__(__self__, *,
                 firewall_rule_group_id: pulumi.Input[str],
                 priority: pulumi.Input[int],
                 vpc_id: pulumi.Input[str],
                 mutation_protection: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ResolverFirewallRuleGroupAssociation resource.
        :param pulumi.Input[str] firewall_rule_group_id: The unique identifier of the firewall rule group.
        :param pulumi.Input[int] priority: The setting that determines the processing order of the rule group among the rule groups that you associate with the specified VPC. DNS Firewall filters VPC traffic starting from the rule group with the lowest numeric priority setting.
        :param pulumi.Input[str] vpc_id: The unique identifier of the VPC that you want to associate with the rule group.
        :param pulumi.Input[str] mutation_protection: If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Valid values: `ENABLED`, `DISABLED`.
        :param pulumi.Input[str] name: A name that lets you identify the rule group association, to manage and use it.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "firewall_rule_group_id", firewall_rule_group_id)
        pulumi.set(__self__, "priority", priority)
        pulumi.set(__self__, "vpc_id", vpc_id)
        if mutation_protection is not None:
            pulumi.set(__self__, "mutation_protection", mutation_protection)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> pulumi.Input[str]:
        """
        The unique identifier of the firewall rule group.
        """
        return pulumi.get(self, "firewall_rule_group_id")

    @firewall_rule_group_id.setter
    def firewall_rule_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "firewall_rule_group_id", value)

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Input[int]:
        """
        The setting that determines the processing order of the rule group among the rule groups that you associate with the specified VPC. DNS Firewall filters VPC traffic starting from the rule group with the lowest numeric priority setting.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: pulumi.Input[int]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The unique identifier of the VPC that you want to associate with the rule group.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter(name="mutationProtection")
    def mutation_protection(self) -> Optional[pulumi.Input[str]]:
        """
        If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "mutation_protection")

    @mutation_protection.setter
    def mutation_protection(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mutation_protection", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name that lets you identify the rule group association, to manage and use it.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ResolverFirewallRuleGroupAssociationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 firewall_rule_group_id: Optional[pulumi.Input[str]] = None,
                 mutation_protection: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ResolverFirewallRuleGroupAssociation resources.
        :param pulumi.Input[str] arn: The ARN (Amazon Resource Name) of the firewall rule group association.
        :param pulumi.Input[str] firewall_rule_group_id: The unique identifier of the firewall rule group.
        :param pulumi.Input[str] mutation_protection: If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Valid values: `ENABLED`, `DISABLED`.
        :param pulumi.Input[str] name: A name that lets you identify the rule group association, to manage and use it.
        :param pulumi.Input[int] priority: The setting that determines the processing order of the rule group among the rule groups that you associate with the specified VPC. DNS Firewall filters VPC traffic starting from the rule group with the lowest numeric priority setting.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] vpc_id: The unique identifier of the VPC that you want to associate with the rule group.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if firewall_rule_group_id is not None:
            pulumi.set(__self__, "firewall_rule_group_id", firewall_rule_group_id)
        if mutation_protection is not None:
            pulumi.set(__self__, "mutation_protection", mutation_protection)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN (Amazon Resource Name) of the firewall rule group association.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier of the firewall rule group.
        """
        return pulumi.get(self, "firewall_rule_group_id")

    @firewall_rule_group_id.setter
    def firewall_rule_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "firewall_rule_group_id", value)

    @property
    @pulumi.getter(name="mutationProtection")
    def mutation_protection(self) -> Optional[pulumi.Input[str]]:
        """
        If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "mutation_protection")

    @mutation_protection.setter
    def mutation_protection(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mutation_protection", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name that lets you identify the rule group association, to manage and use it.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        The setting that determines the processing order of the rule group among the rule groups that you associate with the specified VPC. DNS Firewall filters VPC traffic starting from the rule group with the lowest numeric priority setting.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier of the VPC that you want to associate with the rule group.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class ResolverFirewallRuleGroupAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 firewall_rule_group_id: Optional[pulumi.Input[str]] = None,
                 mutation_protection: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Route 53 Resolver DNS Firewall rule group association resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.route53.ResolverFirewallRuleGroup("example", name="example")
        example_resolver_firewall_rule_group_association = aws.route53.ResolverFirewallRuleGroupAssociation("example",
            name="example",
            firewall_rule_group_id=example.id,
            priority=100,
            vpc_id=example_aws_vpc["id"])
        ```

        ## Import

        Using `pulumi import`, import Route 53 Resolver DNS Firewall rule group associations using the Route 53 Resolver DNS Firewall rule group association ID. For example:

        ```sh
        $ pulumi import aws:route53/resolverFirewallRuleGroupAssociation:ResolverFirewallRuleGroupAssociation example rslvr-frgassoc-0123456789abcdef
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] firewall_rule_group_id: The unique identifier of the firewall rule group.
        :param pulumi.Input[str] mutation_protection: If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Valid values: `ENABLED`, `DISABLED`.
        :param pulumi.Input[str] name: A name that lets you identify the rule group association, to manage and use it.
        :param pulumi.Input[int] priority: The setting that determines the processing order of the rule group among the rule groups that you associate with the specified VPC. DNS Firewall filters VPC traffic starting from the rule group with the lowest numeric priority setting.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] vpc_id: The unique identifier of the VPC that you want to associate with the rule group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResolverFirewallRuleGroupAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Route 53 Resolver DNS Firewall rule group association resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.route53.ResolverFirewallRuleGroup("example", name="example")
        example_resolver_firewall_rule_group_association = aws.route53.ResolverFirewallRuleGroupAssociation("example",
            name="example",
            firewall_rule_group_id=example.id,
            priority=100,
            vpc_id=example_aws_vpc["id"])
        ```

        ## Import

        Using `pulumi import`, import Route 53 Resolver DNS Firewall rule group associations using the Route 53 Resolver DNS Firewall rule group association ID. For example:

        ```sh
        $ pulumi import aws:route53/resolverFirewallRuleGroupAssociation:ResolverFirewallRuleGroupAssociation example rslvr-frgassoc-0123456789abcdef
        ```

        :param str resource_name: The name of the resource.
        :param ResolverFirewallRuleGroupAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResolverFirewallRuleGroupAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 firewall_rule_group_id: Optional[pulumi.Input[str]] = None,
                 mutation_protection: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResolverFirewallRuleGroupAssociationArgs.__new__(ResolverFirewallRuleGroupAssociationArgs)

            if firewall_rule_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'firewall_rule_group_id'")
            __props__.__dict__["firewall_rule_group_id"] = firewall_rule_group_id
            __props__.__dict__["mutation_protection"] = mutation_protection
            __props__.__dict__["name"] = name
            if priority is None and not opts.urn:
                raise TypeError("Missing required property 'priority'")
            __props__.__dict__["priority"] = priority
            __props__.__dict__["tags"] = tags
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(ResolverFirewallRuleGroupAssociation, __self__).__init__(
            'aws:route53/resolverFirewallRuleGroupAssociation:ResolverFirewallRuleGroupAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            firewall_rule_group_id: Optional[pulumi.Input[str]] = None,
            mutation_protection: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            priority: Optional[pulumi.Input[int]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'ResolverFirewallRuleGroupAssociation':
        """
        Get an existing ResolverFirewallRuleGroupAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN (Amazon Resource Name) of the firewall rule group association.
        :param pulumi.Input[str] firewall_rule_group_id: The unique identifier of the firewall rule group.
        :param pulumi.Input[str] mutation_protection: If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Valid values: `ENABLED`, `DISABLED`.
        :param pulumi.Input[str] name: A name that lets you identify the rule group association, to manage and use it.
        :param pulumi.Input[int] priority: The setting that determines the processing order of the rule group among the rule groups that you associate with the specified VPC. DNS Firewall filters VPC traffic starting from the rule group with the lowest numeric priority setting.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] vpc_id: The unique identifier of the VPC that you want to associate with the rule group.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResolverFirewallRuleGroupAssociationState.__new__(_ResolverFirewallRuleGroupAssociationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["firewall_rule_group_id"] = firewall_rule_group_id
        __props__.__dict__["mutation_protection"] = mutation_protection
        __props__.__dict__["name"] = name
        __props__.__dict__["priority"] = priority
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["vpc_id"] = vpc_id
        return ResolverFirewallRuleGroupAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN (Amazon Resource Name) of the firewall rule group association.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> pulumi.Output[str]:
        """
        The unique identifier of the firewall rule group.
        """
        return pulumi.get(self, "firewall_rule_group_id")

    @property
    @pulumi.getter(name="mutationProtection")
    def mutation_protection(self) -> pulumi.Output[str]:
        """
        If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "mutation_protection")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A name that lets you identify the rule group association, to manage and use it.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[int]:
        """
        The setting that determines the processing order of the rule group among the rule groups that you associate with the specified VPC. DNS Firewall filters VPC traffic starting from the rule group with the lowest numeric priority setting.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The unique identifier of the VPC that you want to associate with the rule group.
        """
        return pulumi.get(self, "vpc_id")

