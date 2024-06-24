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

__all__ = [
    'GetPlanResult',
    'AwaitableGetPlanResult',
    'get_plan',
    'get_plan_output',
]

@pulumi.output_type
class GetPlanResult:
    """
    A collection of values returned by getPlan.
    """
    def __init__(__self__, contact_id=None, id=None, stages=None):
        if contact_id and not isinstance(contact_id, str):
            raise TypeError("Expected argument 'contact_id' to be a str")
        pulumi.set(__self__, "contact_id", contact_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if stages and not isinstance(stages, list):
            raise TypeError("Expected argument 'stages' to be a list")
        pulumi.set(__self__, "stages", stages)

    @property
    @pulumi.getter(name="contactId")
    def contact_id(self) -> str:
        return pulumi.get(self, "contact_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def stages(self) -> Sequence['outputs.GetPlanStageResult']:
        """
        List of stages. A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.
        """
        return pulumi.get(self, "stages")


class AwaitableGetPlanResult(GetPlanResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPlanResult(
            contact_id=self.contact_id,
            id=self.id,
            stages=self.stages)


def get_plan(contact_id: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPlanResult:
    """
    Data source for managing a Plan of an AWS SSM Contact.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.ssmcontacts.get_plan(contact_id="arn:aws:ssm-contacts:us-west-2:123456789012:contact/contactalias")
    ```


    :param str contact_id: The Amazon Resource Name (ARN) of the contact or escalation plan.
    """
    __args__ = dict()
    __args__['contactId'] = contact_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ssmcontacts/getPlan:getPlan', __args__, opts=opts, typ=GetPlanResult).value

    return AwaitableGetPlanResult(
        contact_id=pulumi.get(__ret__, 'contact_id'),
        id=pulumi.get(__ret__, 'id'),
        stages=pulumi.get(__ret__, 'stages'))


@_utilities.lift_output_func(get_plan)
def get_plan_output(contact_id: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPlanResult]:
    """
    Data source for managing a Plan of an AWS SSM Contact.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.ssmcontacts.get_plan(contact_id="arn:aws:ssm-contacts:us-west-2:123456789012:contact/contactalias")
    ```


    :param str contact_id: The Amazon Resource Name (ARN) of the contact or escalation plan.
    """
    ...
