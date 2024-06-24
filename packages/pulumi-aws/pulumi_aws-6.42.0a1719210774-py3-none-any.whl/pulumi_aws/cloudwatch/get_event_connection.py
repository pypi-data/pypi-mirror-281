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
    'GetEventConnectionResult',
    'AwaitableGetEventConnectionResult',
    'get_event_connection',
    'get_event_connection_output',
]

@pulumi.output_type
class GetEventConnectionResult:
    """
    A collection of values returned by getEventConnection.
    """
    def __init__(__self__, arn=None, authorization_type=None, id=None, name=None, secret_arn=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if authorization_type and not isinstance(authorization_type, str):
            raise TypeError("Expected argument 'authorization_type' to be a str")
        pulumi.set(__self__, "authorization_type", authorization_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if secret_arn and not isinstance(secret_arn, str):
            raise TypeError("Expected argument 'secret_arn' to be a str")
        pulumi.set(__self__, "secret_arn", secret_arn)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN (Amazon Resource Name) for the connection.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="authorizationType")
    def authorization_type(self) -> str:
        """
        Type of authorization to use to connect. One of `API_KEY`,`BASIC`,`OAUTH_CLIENT_CREDENTIALS`.
        """
        return pulumi.get(self, "authorization_type")

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
        """
        Name of the connection.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="secretArn")
    def secret_arn(self) -> str:
        """
        ARN (Amazon Resource Name) for the secret created from the authorization parameters specified for the connection.
        """
        return pulumi.get(self, "secret_arn")


class AwaitableGetEventConnectionResult(GetEventConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventConnectionResult(
            arn=self.arn,
            authorization_type=self.authorization_type,
            id=self.id,
            name=self.name,
            secret_arn=self.secret_arn)


def get_event_connection(name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventConnectionResult:
    """
    Use this data source to retrieve information about an EventBridge connection.

    > **Note:** EventBridge was formerly known as CloudWatch Events. The functionality is identical.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.cloudwatch.get_event_connection(name="test")
    ```


    :param str name: Name of the connection.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cloudwatch/getEventConnection:getEventConnection', __args__, opts=opts, typ=GetEventConnectionResult).value

    return AwaitableGetEventConnectionResult(
        arn=pulumi.get(__ret__, 'arn'),
        authorization_type=pulumi.get(__ret__, 'authorization_type'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        secret_arn=pulumi.get(__ret__, 'secret_arn'))


@_utilities.lift_output_func(get_event_connection)
def get_event_connection_output(name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventConnectionResult]:
    """
    Use this data source to retrieve information about an EventBridge connection.

    > **Note:** EventBridge was formerly known as CloudWatch Events. The functionality is identical.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.cloudwatch.get_event_connection(name="test")
    ```


    :param str name: Name of the connection.
    """
    ...
