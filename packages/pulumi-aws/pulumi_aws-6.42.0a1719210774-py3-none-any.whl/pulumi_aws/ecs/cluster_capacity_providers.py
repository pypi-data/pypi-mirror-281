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

__all__ = ['ClusterCapacityProvidersArgs', 'ClusterCapacityProviders']

@pulumi.input_type
class ClusterCapacityProvidersArgs:
    def __init__(__self__, *,
                 cluster_name: pulumi.Input[str],
                 capacity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 default_capacity_provider_strategies: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]] = None):
        """
        The set of arguments for constructing a ClusterCapacityProviders resource.
        :param pulumi.Input[str] cluster_name: Name of the ECS cluster to manage capacity providers for.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] capacity_providers: Set of names of one or more capacity providers to associate with the cluster. Valid values also include `FARGATE` and `FARGATE_SPOT`.
        :param pulumi.Input[Sequence[pulumi.Input['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]] default_capacity_provider_strategies: Set of capacity provider strategies to use by default for the cluster. Detailed below.
        """
        pulumi.set(__self__, "cluster_name", cluster_name)
        if capacity_providers is not None:
            pulumi.set(__self__, "capacity_providers", capacity_providers)
        if default_capacity_provider_strategies is not None:
            pulumi.set(__self__, "default_capacity_provider_strategies", default_capacity_provider_strategies)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Input[str]:
        """
        Name of the ECS cluster to manage capacity providers for.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter(name="capacityProviders")
    def capacity_providers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of names of one or more capacity providers to associate with the cluster. Valid values also include `FARGATE` and `FARGATE_SPOT`.
        """
        return pulumi.get(self, "capacity_providers")

    @capacity_providers.setter
    def capacity_providers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "capacity_providers", value)

    @property
    @pulumi.getter(name="defaultCapacityProviderStrategies")
    def default_capacity_provider_strategies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]]:
        """
        Set of capacity provider strategies to use by default for the cluster. Detailed below.
        """
        return pulumi.get(self, "default_capacity_provider_strategies")

    @default_capacity_provider_strategies.setter
    def default_capacity_provider_strategies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]]):
        pulumi.set(self, "default_capacity_provider_strategies", value)


@pulumi.input_type
class _ClusterCapacityProvidersState:
    def __init__(__self__, *,
                 capacity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 default_capacity_provider_strategies: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]] = None):
        """
        Input properties used for looking up and filtering ClusterCapacityProviders resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] capacity_providers: Set of names of one or more capacity providers to associate with the cluster. Valid values also include `FARGATE` and `FARGATE_SPOT`.
        :param pulumi.Input[str] cluster_name: Name of the ECS cluster to manage capacity providers for.
        :param pulumi.Input[Sequence[pulumi.Input['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]] default_capacity_provider_strategies: Set of capacity provider strategies to use by default for the cluster. Detailed below.
        """
        if capacity_providers is not None:
            pulumi.set(__self__, "capacity_providers", capacity_providers)
        if cluster_name is not None:
            pulumi.set(__self__, "cluster_name", cluster_name)
        if default_capacity_provider_strategies is not None:
            pulumi.set(__self__, "default_capacity_provider_strategies", default_capacity_provider_strategies)

    @property
    @pulumi.getter(name="capacityProviders")
    def capacity_providers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of names of one or more capacity providers to associate with the cluster. Valid values also include `FARGATE` and `FARGATE_SPOT`.
        """
        return pulumi.get(self, "capacity_providers")

    @capacity_providers.setter
    def capacity_providers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "capacity_providers", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the ECS cluster to manage capacity providers for.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter(name="defaultCapacityProviderStrategies")
    def default_capacity_provider_strategies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]]:
        """
        Set of capacity provider strategies to use by default for the cluster. Detailed below.
        """
        return pulumi.get(self, "default_capacity_provider_strategies")

    @default_capacity_provider_strategies.setter
    def default_capacity_provider_strategies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]]):
        pulumi.set(self, "default_capacity_provider_strategies", value)


class ClusterCapacityProviders(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 capacity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 default_capacity_provider_strategies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]]] = None,
                 __props__=None):
        """
        Manages the capacity providers of an ECS Cluster.

        More information about capacity providers can be found in the [ECS User Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-capacity-providers.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ecs.Cluster("example", name="my-cluster")
        example_cluster_capacity_providers = aws.ecs.ClusterCapacityProviders("example",
            cluster_name=example.name,
            capacity_providers=["FARGATE"],
            default_capacity_provider_strategies=[aws.ecs.ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs(
                base=1,
                weight=100,
                capacity_provider="FARGATE",
            )])
        ```

        ## Import

        Using `pulumi import`, import ECS cluster capacity providers using the `cluster_name` attribute. For example:

        ```sh
        $ pulumi import aws:ecs/clusterCapacityProviders:ClusterCapacityProviders example my-cluster
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] capacity_providers: Set of names of one or more capacity providers to associate with the cluster. Valid values also include `FARGATE` and `FARGATE_SPOT`.
        :param pulumi.Input[str] cluster_name: Name of the ECS cluster to manage capacity providers for.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]] default_capacity_provider_strategies: Set of capacity provider strategies to use by default for the cluster. Detailed below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterCapacityProvidersArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages the capacity providers of an ECS Cluster.

        More information about capacity providers can be found in the [ECS User Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-capacity-providers.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ecs.Cluster("example", name="my-cluster")
        example_cluster_capacity_providers = aws.ecs.ClusterCapacityProviders("example",
            cluster_name=example.name,
            capacity_providers=["FARGATE"],
            default_capacity_provider_strategies=[aws.ecs.ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs(
                base=1,
                weight=100,
                capacity_provider="FARGATE",
            )])
        ```

        ## Import

        Using `pulumi import`, import ECS cluster capacity providers using the `cluster_name` attribute. For example:

        ```sh
        $ pulumi import aws:ecs/clusterCapacityProviders:ClusterCapacityProviders example my-cluster
        ```

        :param str resource_name: The name of the resource.
        :param ClusterCapacityProvidersArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterCapacityProvidersArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 capacity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 default_capacity_provider_strategies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterCapacityProvidersArgs.__new__(ClusterCapacityProvidersArgs)

            __props__.__dict__["capacity_providers"] = capacity_providers
            if cluster_name is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_name'")
            __props__.__dict__["cluster_name"] = cluster_name
            __props__.__dict__["default_capacity_provider_strategies"] = default_capacity_provider_strategies
        super(ClusterCapacityProviders, __self__).__init__(
            'aws:ecs/clusterCapacityProviders:ClusterCapacityProviders',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            capacity_providers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            cluster_name: Optional[pulumi.Input[str]] = None,
            default_capacity_provider_strategies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]]] = None) -> 'ClusterCapacityProviders':
        """
        Get an existing ClusterCapacityProviders resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] capacity_providers: Set of names of one or more capacity providers to associate with the cluster. Valid values also include `FARGATE` and `FARGATE_SPOT`.
        :param pulumi.Input[str] cluster_name: Name of the ECS cluster to manage capacity providers for.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs']]]] default_capacity_provider_strategies: Set of capacity provider strategies to use by default for the cluster. Detailed below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ClusterCapacityProvidersState.__new__(_ClusterCapacityProvidersState)

        __props__.__dict__["capacity_providers"] = capacity_providers
        __props__.__dict__["cluster_name"] = cluster_name
        __props__.__dict__["default_capacity_provider_strategies"] = default_capacity_provider_strategies
        return ClusterCapacityProviders(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="capacityProviders")
    def capacity_providers(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Set of names of one or more capacity providers to associate with the cluster. Valid values also include `FARGATE` and `FARGATE_SPOT`.
        """
        return pulumi.get(self, "capacity_providers")

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Output[str]:
        """
        Name of the ECS cluster to manage capacity providers for.
        """
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter(name="defaultCapacityProviderStrategies")
    def default_capacity_provider_strategies(self) -> pulumi.Output[Optional[Sequence['outputs.ClusterCapacityProvidersDefaultCapacityProviderStrategy']]]:
        """
        Set of capacity provider strategies to use by default for the cluster. Detailed below.
        """
        return pulumi.get(self, "default_capacity_provider_strategies")

