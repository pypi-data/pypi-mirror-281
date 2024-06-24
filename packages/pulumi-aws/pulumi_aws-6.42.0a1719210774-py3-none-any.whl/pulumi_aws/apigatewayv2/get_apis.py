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
    'GetApisResult',
    'AwaitableGetApisResult',
    'get_apis',
    'get_apis_output',
]

@pulumi.output_type
class GetApisResult:
    """
    A collection of values returned by getApis.
    """
    def __init__(__self__, id=None, ids=None, name=None, protocol_type=None, tags=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if protocol_type and not isinstance(protocol_type, str):
            raise TypeError("Expected argument 'protocol_type' to be a str")
        pulumi.set(__self__, "protocol_type", protocol_type)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        Set of API identifiers.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="protocolType")
    def protocol_type(self) -> Optional[str]:
        return pulumi.get(self, "protocol_type")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "tags")


class AwaitableGetApisResult(GetApisResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApisResult(
            id=self.id,
            ids=self.ids,
            name=self.name,
            protocol_type=self.protocol_type,
            tags=self.tags)


def get_apis(name: Optional[str] = None,
             protocol_type: Optional[str] = None,
             tags: Optional[Mapping[str, str]] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApisResult:
    """
    Provides details about multiple Amazon API Gateway Version 2 APIs.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.apigatewayv2.get_apis(protocol_type="HTTP")
    ```


    :param str name: API name.
    :param str protocol_type: API protocol.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired APIs.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['protocolType'] = protocol_type
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:apigatewayv2/getApis:getApis', __args__, opts=opts, typ=GetApisResult).value

    return AwaitableGetApisResult(
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name=pulumi.get(__ret__, 'name'),
        protocol_type=pulumi.get(__ret__, 'protocol_type'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_apis)
def get_apis_output(name: Optional[pulumi.Input[Optional[str]]] = None,
                    protocol_type: Optional[pulumi.Input[Optional[str]]] = None,
                    tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApisResult]:
    """
    Provides details about multiple Amazon API Gateway Version 2 APIs.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.apigatewayv2.get_apis(protocol_type="HTTP")
    ```


    :param str name: API name.
    :param str protocol_type: API protocol.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired APIs.
    """
    ...
