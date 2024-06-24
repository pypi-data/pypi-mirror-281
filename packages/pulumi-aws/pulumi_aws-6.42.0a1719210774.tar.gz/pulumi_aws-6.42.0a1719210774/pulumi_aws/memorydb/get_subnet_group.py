# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetSubnetGroupResult',
    'AwaitableGetSubnetGroupResult',
    'get_subnet_group',
    'get_subnet_group_output',
]

@pulumi.output_type
class GetSubnetGroupResult:
    """
    A collection of values returned by getSubnetGroup.
    """
    def __init__(__self__, arn=None, description=None, id=None, name=None, subnet_ids=None, tags=None, vpc_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if subnet_ids and not isinstance(subnet_ids, list):
            raise TypeError("Expected argument 'subnet_ids' to be a list")
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the subnet group.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the subnet group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        Set of VPC Subnet ID-s of the subnet group.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags assigned to the subnet group.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        VPC in which the subnet group exists.
        """
        return pulumi.get(self, "vpc_id")


class AwaitableGetSubnetGroupResult(GetSubnetGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubnetGroupResult(
            arn=self.arn,
            description=self.description,
            id=self.id,
            name=self.name,
            subnet_ids=self.subnet_ids,
            tags=self.tags,
            vpc_id=self.vpc_id)


def get_subnet_group(name: Optional[str] = None,
                     tags: Optional[Mapping[str, str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubnetGroupResult:
    """
    Provides information about a MemoryDB Subnet Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.memorydb.get_subnet_group(name="my-subnet-group")
    ```


    :param str name: Name of the subnet group.
    :param Mapping[str, str] tags: Map of tags assigned to the subnet group.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:memorydb/getSubnetGroup:getSubnetGroup', __args__, opts=opts, typ=GetSubnetGroupResult).value

    return AwaitableGetSubnetGroupResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        subnet_ids=pulumi.get(__ret__, 'subnet_ids'),
        tags=pulumi.get(__ret__, 'tags'),
        vpc_id=pulumi.get(__ret__, 'vpc_id'))


@_utilities.lift_output_func(get_subnet_group)
def get_subnet_group_output(name: Optional[pulumi.Input[str]] = None,
                            tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSubnetGroupResult]:
    """
    Provides information about a MemoryDB Subnet Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.memorydb.get_subnet_group(name="my-subnet-group")
    ```


    :param str name: Name of the subnet group.
    :param Mapping[str, str] tags: Map of tags assigned to the subnet group.
    """
    ...
