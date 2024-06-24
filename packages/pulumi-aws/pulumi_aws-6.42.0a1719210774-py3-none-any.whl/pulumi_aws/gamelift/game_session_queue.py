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

__all__ = ['GameSessionQueueArgs', 'GameSessionQueue']

@pulumi.input_type
class GameSessionQueueArgs:
    def __init__(__self__, *,
                 custom_event_data: Optional[pulumi.Input[str]] = None,
                 destinations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notification_target: Optional[pulumi.Input[str]] = None,
                 player_latency_policies: Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a GameSessionQueue resource.
        :param pulumi.Input[str] custom_event_data: Information to be added to all events that are related to this game session queue.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] destinations: List of fleet/alias ARNs used by session queue for placing game sessions.
        :param pulumi.Input[str] name: Name of the session queue.
        :param pulumi.Input[str] notification_target: An SNS topic ARN that is set up to receive game session placement notifications.
        :param pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]] player_latency_policies: One or more policies used to choose fleet based on player latency. See below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[int] timeout_in_seconds: Maximum time a game session request can remain in the queue.
        """
        if custom_event_data is not None:
            pulumi.set(__self__, "custom_event_data", custom_event_data)
        if destinations is not None:
            pulumi.set(__self__, "destinations", destinations)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if notification_target is not None:
            pulumi.set(__self__, "notification_target", notification_target)
        if player_latency_policies is not None:
            pulumi.set(__self__, "player_latency_policies", player_latency_policies)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)

    @property
    @pulumi.getter(name="customEventData")
    def custom_event_data(self) -> Optional[pulumi.Input[str]]:
        """
        Information to be added to all events that are related to this game session queue.
        """
        return pulumi.get(self, "custom_event_data")

    @custom_event_data.setter
    def custom_event_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_event_data", value)

    @property
    @pulumi.getter
    def destinations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of fleet/alias ARNs used by session queue for placing game sessions.
        """
        return pulumi.get(self, "destinations")

    @destinations.setter
    def destinations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "destinations", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the session queue.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notificationTarget")
    def notification_target(self) -> Optional[pulumi.Input[str]]:
        """
        An SNS topic ARN that is set up to receive game session placement notifications.
        """
        return pulumi.get(self, "notification_target")

    @notification_target.setter
    def notification_target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notification_target", value)

    @property
    @pulumi.getter(name="playerLatencyPolicies")
    def player_latency_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]]]:
        """
        One or more policies used to choose fleet based on player latency. See below.
        """
        return pulumi.get(self, "player_latency_policies")

    @player_latency_policies.setter
    def player_latency_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]]]):
        pulumi.set(self, "player_latency_policies", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum time a game session request can remain in the queue.
        """
        return pulumi.get(self, "timeout_in_seconds")

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout_in_seconds", value)


@pulumi.input_type
class _GameSessionQueueState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 custom_event_data: Optional[pulumi.Input[str]] = None,
                 destinations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notification_target: Optional[pulumi.Input[str]] = None,
                 player_latency_policies: Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering GameSessionQueue resources.
        :param pulumi.Input[str] arn: Game Session Queue ARN.
        :param pulumi.Input[str] custom_event_data: Information to be added to all events that are related to this game session queue.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] destinations: List of fleet/alias ARNs used by session queue for placing game sessions.
        :param pulumi.Input[str] name: Name of the session queue.
        :param pulumi.Input[str] notification_target: An SNS topic ARN that is set up to receive game session placement notifications.
        :param pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]] player_latency_policies: One or more policies used to choose fleet based on player latency. See below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[int] timeout_in_seconds: Maximum time a game session request can remain in the queue.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if custom_event_data is not None:
            pulumi.set(__self__, "custom_event_data", custom_event_data)
        if destinations is not None:
            pulumi.set(__self__, "destinations", destinations)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if notification_target is not None:
            pulumi.set(__self__, "notification_target", notification_target)
        if player_latency_policies is not None:
            pulumi.set(__self__, "player_latency_policies", player_latency_policies)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Game Session Queue ARN.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="customEventData")
    def custom_event_data(self) -> Optional[pulumi.Input[str]]:
        """
        Information to be added to all events that are related to this game session queue.
        """
        return pulumi.get(self, "custom_event_data")

    @custom_event_data.setter
    def custom_event_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_event_data", value)

    @property
    @pulumi.getter
    def destinations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of fleet/alias ARNs used by session queue for placing game sessions.
        """
        return pulumi.get(self, "destinations")

    @destinations.setter
    def destinations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "destinations", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the session queue.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notificationTarget")
    def notification_target(self) -> Optional[pulumi.Input[str]]:
        """
        An SNS topic ARN that is set up to receive game session placement notifications.
        """
        return pulumi.get(self, "notification_target")

    @notification_target.setter
    def notification_target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notification_target", value)

    @property
    @pulumi.getter(name="playerLatencyPolicies")
    def player_latency_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]]]:
        """
        One or more policies used to choose fleet based on player latency. See below.
        """
        return pulumi.get(self, "player_latency_policies")

    @player_latency_policies.setter
    def player_latency_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]]]):
        pulumi.set(self, "player_latency_policies", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum time a game session request can remain in the queue.
        """
        return pulumi.get(self, "timeout_in_seconds")

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout_in_seconds", value)


class GameSessionQueue(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_event_data: Optional[pulumi.Input[str]] = None,
                 destinations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notification_target: Optional[pulumi.Input[str]] = None,
                 player_latency_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GameSessionQueuePlayerLatencyPolicyArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides an GameLift Game Session Queue resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.gamelift.GameSessionQueue("test",
            name="example-session-queue",
            destinations=[
                us_west2_fleet["arn"],
                eu_central1_fleet["arn"],
            ],
            notification_target=game_session_queue_notifications["arn"],
            player_latency_policies=[
                aws.gamelift.GameSessionQueuePlayerLatencyPolicyArgs(
                    maximum_individual_player_latency_milliseconds=100,
                    policy_duration_seconds=5,
                ),
                aws.gamelift.GameSessionQueuePlayerLatencyPolicyArgs(
                    maximum_individual_player_latency_milliseconds=200,
                ),
            ],
            timeout_in_seconds=60)
        ```

        ## Import

        Using `pulumi import`, import GameLift Game Session Queues using their `name`. For example:

        ```sh
        $ pulumi import aws:gamelift/gameSessionQueue:GameSessionQueue example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] custom_event_data: Information to be added to all events that are related to this game session queue.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] destinations: List of fleet/alias ARNs used by session queue for placing game sessions.
        :param pulumi.Input[str] name: Name of the session queue.
        :param pulumi.Input[str] notification_target: An SNS topic ARN that is set up to receive game session placement notifications.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GameSessionQueuePlayerLatencyPolicyArgs']]]] player_latency_policies: One or more policies used to choose fleet based on player latency. See below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[int] timeout_in_seconds: Maximum time a game session request can remain in the queue.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[GameSessionQueueArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an GameLift Game Session Queue resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.gamelift.GameSessionQueue("test",
            name="example-session-queue",
            destinations=[
                us_west2_fleet["arn"],
                eu_central1_fleet["arn"],
            ],
            notification_target=game_session_queue_notifications["arn"],
            player_latency_policies=[
                aws.gamelift.GameSessionQueuePlayerLatencyPolicyArgs(
                    maximum_individual_player_latency_milliseconds=100,
                    policy_duration_seconds=5,
                ),
                aws.gamelift.GameSessionQueuePlayerLatencyPolicyArgs(
                    maximum_individual_player_latency_milliseconds=200,
                ),
            ],
            timeout_in_seconds=60)
        ```

        ## Import

        Using `pulumi import`, import GameLift Game Session Queues using their `name`. For example:

        ```sh
        $ pulumi import aws:gamelift/gameSessionQueue:GameSessionQueue example example
        ```

        :param str resource_name: The name of the resource.
        :param GameSessionQueueArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GameSessionQueueArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_event_data: Optional[pulumi.Input[str]] = None,
                 destinations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notification_target: Optional[pulumi.Input[str]] = None,
                 player_latency_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GameSessionQueuePlayerLatencyPolicyArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GameSessionQueueArgs.__new__(GameSessionQueueArgs)

            __props__.__dict__["custom_event_data"] = custom_event_data
            __props__.__dict__["destinations"] = destinations
            __props__.__dict__["name"] = name
            __props__.__dict__["notification_target"] = notification_target
            __props__.__dict__["player_latency_policies"] = player_latency_policies
            __props__.__dict__["tags"] = tags
            __props__.__dict__["timeout_in_seconds"] = timeout_in_seconds
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(GameSessionQueue, __self__).__init__(
            'aws:gamelift/gameSessionQueue:GameSessionQueue',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            custom_event_data: Optional[pulumi.Input[str]] = None,
            destinations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            notification_target: Optional[pulumi.Input[str]] = None,
            player_latency_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GameSessionQueuePlayerLatencyPolicyArgs']]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            timeout_in_seconds: Optional[pulumi.Input[int]] = None) -> 'GameSessionQueue':
        """
        Get an existing GameSessionQueue resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Game Session Queue ARN.
        :param pulumi.Input[str] custom_event_data: Information to be added to all events that are related to this game session queue.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] destinations: List of fleet/alias ARNs used by session queue for placing game sessions.
        :param pulumi.Input[str] name: Name of the session queue.
        :param pulumi.Input[str] notification_target: An SNS topic ARN that is set up to receive game session placement notifications.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GameSessionQueuePlayerLatencyPolicyArgs']]]] player_latency_policies: One or more policies used to choose fleet based on player latency. See below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[int] timeout_in_seconds: Maximum time a game session request can remain in the queue.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GameSessionQueueState.__new__(_GameSessionQueueState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["custom_event_data"] = custom_event_data
        __props__.__dict__["destinations"] = destinations
        __props__.__dict__["name"] = name
        __props__.__dict__["notification_target"] = notification_target
        __props__.__dict__["player_latency_policies"] = player_latency_policies
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["timeout_in_seconds"] = timeout_in_seconds
        return GameSessionQueue(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Game Session Queue ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="customEventData")
    def custom_event_data(self) -> pulumi.Output[Optional[str]]:
        """
        Information to be added to all events that are related to this game session queue.
        """
        return pulumi.get(self, "custom_event_data")

    @property
    @pulumi.getter
    def destinations(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of fleet/alias ARNs used by session queue for placing game sessions.
        """
        return pulumi.get(self, "destinations")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the session queue.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notificationTarget")
    def notification_target(self) -> pulumi.Output[Optional[str]]:
        """
        An SNS topic ARN that is set up to receive game session placement notifications.
        """
        return pulumi.get(self, "notification_target")

    @property
    @pulumi.getter(name="playerLatencyPolicies")
    def player_latency_policies(self) -> pulumi.Output[Optional[Sequence['outputs.GameSessionQueuePlayerLatencyPolicy']]]:
        """
        One or more policies used to choose fleet based on player latency. See below.
        """
        return pulumi.get(self, "player_latency_policies")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum time a game session request can remain in the queue.
        """
        return pulumi.get(self, "timeout_in_seconds")

