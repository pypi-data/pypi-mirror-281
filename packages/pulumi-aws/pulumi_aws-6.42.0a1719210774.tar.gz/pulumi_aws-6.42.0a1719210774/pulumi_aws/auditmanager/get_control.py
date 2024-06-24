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
    'GetControlResult',
    'AwaitableGetControlResult',
    'get_control',
    'get_control_output',
]

@pulumi.output_type
class GetControlResult:
    """
    A collection of values returned by getControl.
    """
    def __init__(__self__, action_plan_instructions=None, action_plan_title=None, arn=None, control_mapping_sources=None, description=None, id=None, name=None, tags=None, testing_information=None, type=None):
        if action_plan_instructions and not isinstance(action_plan_instructions, str):
            raise TypeError("Expected argument 'action_plan_instructions' to be a str")
        pulumi.set(__self__, "action_plan_instructions", action_plan_instructions)
        if action_plan_title and not isinstance(action_plan_title, str):
            raise TypeError("Expected argument 'action_plan_title' to be a str")
        pulumi.set(__self__, "action_plan_title", action_plan_title)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if control_mapping_sources and not isinstance(control_mapping_sources, list):
            raise TypeError("Expected argument 'control_mapping_sources' to be a list")
        pulumi.set(__self__, "control_mapping_sources", control_mapping_sources)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if testing_information and not isinstance(testing_information, str):
            raise TypeError("Expected argument 'testing_information' to be a str")
        pulumi.set(__self__, "testing_information", testing_information)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="actionPlanInstructions")
    def action_plan_instructions(self) -> str:
        return pulumi.get(self, "action_plan_instructions")

    @property
    @pulumi.getter(name="actionPlanTitle")
    def action_plan_title(self) -> str:
        return pulumi.get(self, "action_plan_title")

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="controlMappingSources")
    def control_mapping_sources(self) -> Optional[Sequence['outputs.GetControlControlMappingSourceResult']]:
        return pulumi.get(self, "control_mapping_sources")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="testingInformation")
    def testing_information(self) -> str:
        return pulumi.get(self, "testing_information")

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")


class AwaitableGetControlResult(GetControlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetControlResult(
            action_plan_instructions=self.action_plan_instructions,
            action_plan_title=self.action_plan_title,
            arn=self.arn,
            control_mapping_sources=self.control_mapping_sources,
            description=self.description,
            id=self.id,
            name=self.name,
            tags=self.tags,
            testing_information=self.testing_information,
            type=self.type)


def get_control(control_mapping_sources: Optional[Sequence[pulumi.InputType['GetControlControlMappingSourceArgs']]] = None,
                name: Optional[str] = None,
                type: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetControlResult:
    """
    Data source for managing an AWS Audit Manager Control.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.auditmanager.get_control(name="1. Risk Management",
        type="Standard")
    ```

    ### With Framework Resource

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.auditmanager.get_control(name="1. Risk Management",
        type="Standard")
    example2 = aws.auditmanager.get_control(name="2. Personnel",
        type="Standard")
    example_framework = aws.auditmanager.Framework("example",
        name="example",
        control_sets=[
            aws.auditmanager.FrameworkControlSetArgs(
                name="example",
                controls=[aws.auditmanager.FrameworkControlSetControlArgs(
                    id=example.id,
                )],
            ),
            aws.auditmanager.FrameworkControlSetArgs(
                name="example2",
                controls=[aws.auditmanager.FrameworkControlSetControlArgs(
                    id=example2.id,
                )],
            ),
        ])
    ```


    :param str name: Name of the control.
    :param str type: Type of control. Valid values are `Custom` and `Standard`.
    """
    __args__ = dict()
    __args__['controlMappingSources'] = control_mapping_sources
    __args__['name'] = name
    __args__['type'] = type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:auditmanager/getControl:getControl', __args__, opts=opts, typ=GetControlResult).value

    return AwaitableGetControlResult(
        action_plan_instructions=pulumi.get(__ret__, 'action_plan_instructions'),
        action_plan_title=pulumi.get(__ret__, 'action_plan_title'),
        arn=pulumi.get(__ret__, 'arn'),
        control_mapping_sources=pulumi.get(__ret__, 'control_mapping_sources'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'),
        testing_information=pulumi.get(__ret__, 'testing_information'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_control)
def get_control_output(control_mapping_sources: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetControlControlMappingSourceArgs']]]]] = None,
                       name: Optional[pulumi.Input[str]] = None,
                       type: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetControlResult]:
    """
    Data source for managing an AWS Audit Manager Control.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.auditmanager.get_control(name="1. Risk Management",
        type="Standard")
    ```

    ### With Framework Resource

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.auditmanager.get_control(name="1. Risk Management",
        type="Standard")
    example2 = aws.auditmanager.get_control(name="2. Personnel",
        type="Standard")
    example_framework = aws.auditmanager.Framework("example",
        name="example",
        control_sets=[
            aws.auditmanager.FrameworkControlSetArgs(
                name="example",
                controls=[aws.auditmanager.FrameworkControlSetControlArgs(
                    id=example.id,
                )],
            ),
            aws.auditmanager.FrameworkControlSetArgs(
                name="example2",
                controls=[aws.auditmanager.FrameworkControlSetControlArgs(
                    id=example2.id,
                )],
            ),
        ])
    ```


    :param str name: Name of the control.
    :param str type: Type of control. Valid values are `Custom` and `Standard`.
    """
    ...
