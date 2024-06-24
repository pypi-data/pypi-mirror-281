# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['MatchmakingRuleSetArgs', 'MatchmakingRuleSet']

@pulumi.input_type
class MatchmakingRuleSetArgs:
    def __init__(__self__, *,
                 rule_set_body: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a MatchmakingRuleSet resource.
        :param pulumi.Input[str] rule_set_body: JSON encoded string containing rule set data.
        :param pulumi.Input[str] name: Name of the matchmaking rule set.
        """
        pulumi.set(__self__, "rule_set_body", rule_set_body)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="ruleSetBody")
    def rule_set_body(self) -> pulumi.Input[str]:
        """
        JSON encoded string containing rule set data.
        """
        return pulumi.get(self, "rule_set_body")

    @rule_set_body.setter
    def rule_set_body(self, value: pulumi.Input[str]):
        pulumi.set(self, "rule_set_body", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the matchmaking rule set.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _MatchmakingRuleSetState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rule_set_body: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering MatchmakingRuleSet resources.
        :param pulumi.Input[str] arn: Rule Set ARN.
        :param pulumi.Input[str] name: Name of the matchmaking rule set.
        :param pulumi.Input[str] rule_set_body: JSON encoded string containing rule set data.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if rule_set_body is not None:
            pulumi.set(__self__, "rule_set_body", rule_set_body)
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
        Rule Set ARN.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the matchmaking rule set.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="ruleSetBody")
    def rule_set_body(self) -> Optional[pulumi.Input[str]]:
        """
        JSON encoded string containing rule set data.
        """
        return pulumi.get(self, "rule_set_body")

    @rule_set_body.setter
    def rule_set_body(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_set_body", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
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


class MatchmakingRuleSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rule_set_body: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a GameLift Matchmaking Rule Set resources.

        ## Import

        GameLift Matchmaking Rule Sets  can be imported using the ID, e.g.,

        ```sh
        $ pulumi import aws:gamelift/matchmakingRuleSet:MatchmakingRuleSet example <ruleset-id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the matchmaking rule set.
        :param pulumi.Input[str] rule_set_body: JSON encoded string containing rule set data.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MatchmakingRuleSetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a GameLift Matchmaking Rule Set resources.

        ## Import

        GameLift Matchmaking Rule Sets  can be imported using the ID, e.g.,

        ```sh
        $ pulumi import aws:gamelift/matchmakingRuleSet:MatchmakingRuleSet example <ruleset-id>
        ```

        :param str resource_name: The name of the resource.
        :param MatchmakingRuleSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MatchmakingRuleSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rule_set_body: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MatchmakingRuleSetArgs.__new__(MatchmakingRuleSetArgs)

            __props__.__dict__["name"] = name
            if rule_set_body is None and not opts.urn:
                raise TypeError("Missing required property 'rule_set_body'")
            __props__.__dict__["rule_set_body"] = rule_set_body
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(MatchmakingRuleSet, __self__).__init__(
            'aws:gamelift/matchmakingRuleSet:MatchmakingRuleSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            rule_set_body: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'MatchmakingRuleSet':
        """
        Get an existing MatchmakingRuleSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Rule Set ARN.
        :param pulumi.Input[str] name: Name of the matchmaking rule set.
        :param pulumi.Input[str] rule_set_body: JSON encoded string containing rule set data.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MatchmakingRuleSetState.__new__(_MatchmakingRuleSetState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["name"] = name
        __props__.__dict__["rule_set_body"] = rule_set_body
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return MatchmakingRuleSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Rule Set ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the matchmaking rule set.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ruleSetBody")
    def rule_set_body(self) -> pulumi.Output[str]:
        """
        JSON encoded string containing rule set data.
        """
        return pulumi.get(self, "rule_set_body")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
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

