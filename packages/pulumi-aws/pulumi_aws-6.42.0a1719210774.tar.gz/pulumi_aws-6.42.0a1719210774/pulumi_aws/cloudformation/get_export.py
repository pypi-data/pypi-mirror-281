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
    'GetExportResult',
    'AwaitableGetExportResult',
    'get_export',
    'get_export_output',
]

@pulumi.output_type
class GetExportResult:
    """
    A collection of values returned by getExport.
    """
    def __init__(__self__, exporting_stack_id=None, id=None, name=None, value=None):
        if exporting_stack_id and not isinstance(exporting_stack_id, str):
            raise TypeError("Expected argument 'exporting_stack_id' to be a str")
        pulumi.set(__self__, "exporting_stack_id", exporting_stack_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="exportingStackId")
    def exporting_stack_id(self) -> str:
        """
        ARN of stack that contains the exported output name and value.
        """
        return pulumi.get(self, "exporting_stack_id")

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
    @pulumi.getter
    def value(self) -> str:
        """
        Value from Cloudformation export identified by the export name found from [list-exports](http://docs.aws.amazon.com/cli/latest/reference/cloudformation/list-exports.html)
        """
        return pulumi.get(self, "value")


class AwaitableGetExportResult(GetExportResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetExportResult(
            exporting_stack_id=self.exporting_stack_id,
            id=self.id,
            name=self.name,
            value=self.value)


def get_export(name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetExportResult:
    """
    The CloudFormation Export data source allows access to stack
    exports specified in the [Output](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html) section of the Cloudformation Template using the optional Export Property.

     > Note: If you are trying to use a value from a Cloudformation Stack in the same deployment please use normal interpolation or Cloudformation Outputs.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    subnet_id = aws.cloudformation.get_export(name="mySubnetIdExportName")
    web = aws.ec2.Instance("web",
        ami="ami-abb07bcb",
        instance_type=aws.ec2.InstanceType.T2_MICRO,
        subnet_id=subnet_id.value)
    ```


    :param str name: Name of the export as it appears in the console or from [list-exports](http://docs.aws.amazon.com/cli/latest/reference/cloudformation/list-exports.html)
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cloudformation/getExport:getExport', __args__, opts=opts, typ=GetExportResult).value

    return AwaitableGetExportResult(
        exporting_stack_id=pulumi.get(__ret__, 'exporting_stack_id'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        value=pulumi.get(__ret__, 'value'))


@_utilities.lift_output_func(get_export)
def get_export_output(name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetExportResult]:
    """
    The CloudFormation Export data source allows access to stack
    exports specified in the [Output](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html) section of the Cloudformation Template using the optional Export Property.

     > Note: If you are trying to use a value from a Cloudformation Stack in the same deployment please use normal interpolation or Cloudformation Outputs.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    subnet_id = aws.cloudformation.get_export(name="mySubnetIdExportName")
    web = aws.ec2.Instance("web",
        ami="ami-abb07bcb",
        instance_type=aws.ec2.InstanceType.T2_MICRO,
        subnet_id=subnet_id.value)
    ```


    :param str name: Name of the export as it appears in the console or from [list-exports](http://docs.aws.amazon.com/cli/latest/reference/cloudformation/list-exports.html)
    """
    ...
