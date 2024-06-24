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

__all__ = [
    'GetInstancesResult',
    'AwaitableGetInstancesResult',
    'get_instances',
    'get_instances_output',
]

@pulumi.output_type
class GetInstancesResult:
    """
    A collection of values returned by getInstances.
    """
    def __init__(__self__, filters=None, id=None, instance_arns=None, instance_identifiers=None, tags=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_arns and not isinstance(instance_arns, list):
            raise TypeError("Expected argument 'instance_arns' to be a list")
        pulumi.set(__self__, "instance_arns", instance_arns)
        if instance_identifiers and not isinstance(instance_identifiers, list):
            raise TypeError("Expected argument 'instance_identifiers' to be a list")
        pulumi.set(__self__, "instance_identifiers", instance_identifiers)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetInstancesFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceArns")
    def instance_arns(self) -> Sequence[str]:
        """
        ARNs of the matched RDS instances.
        """
        return pulumi.get(self, "instance_arns")

    @property
    @pulumi.getter(name="instanceIdentifiers")
    def instance_identifiers(self) -> Sequence[str]:
        """
        Identifiers of the matched RDS instances.
        """
        return pulumi.get(self, "instance_identifiers")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetInstancesResult(GetInstancesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstancesResult(
            filters=self.filters,
            id=self.id,
            instance_arns=self.instance_arns,
            instance_identifiers=self.instance_identifiers,
            tags=self.tags)


def get_instances(filters: Optional[Sequence[pulumi.InputType['GetInstancesFilterArgs']]] = None,
                  tags: Optional[Mapping[str, str]] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstancesResult:
    """
    Data source for listing RDS Database Instances.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.rds.get_instances(filters=[aws.rds.GetInstancesFilterArgs(
        name="db-instance-id",
        values=["my-database-id"],
    )])
    ```

    ### Using tags

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.rds.get_instances(tags={
        "Env": "test",
    })
    ```


    :param Sequence[pulumi.InputType['GetInstancesFilterArgs']] filters: Configuration block(s) used to filter instances with AWS supported attributes, such as `engine`, `db-cluster-id` or `db-instance-id` for example. Detailed below.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match a pair on the desired instances.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:rds/getInstances:getInstances', __args__, opts=opts, typ=GetInstancesResult).value

    return AwaitableGetInstancesResult(
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        instance_arns=pulumi.get(__ret__, 'instance_arns'),
        instance_identifiers=pulumi.get(__ret__, 'instance_identifiers'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_instances)
def get_instances_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetInstancesFilterArgs']]]]] = None,
                         tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstancesResult]:
    """
    Data source for listing RDS Database Instances.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.rds.get_instances(filters=[aws.rds.GetInstancesFilterArgs(
        name="db-instance-id",
        values=["my-database-id"],
    )])
    ```

    ### Using tags

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.rds.get_instances(tags={
        "Env": "test",
    })
    ```


    :param Sequence[pulumi.InputType['GetInstancesFilterArgs']] filters: Configuration block(s) used to filter instances with AWS supported attributes, such as `engine`, `db-cluster-id` or `db-instance-id` for example. Detailed below.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match a pair on the desired instances.
    """
    ...
