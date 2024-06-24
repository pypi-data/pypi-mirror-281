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
    'GetNetworkInsightsAnalysisResult',
    'AwaitableGetNetworkInsightsAnalysisResult',
    'get_network_insights_analysis',
    'get_network_insights_analysis_output',
]

@pulumi.output_type
class GetNetworkInsightsAnalysisResult:
    """
    A collection of values returned by getNetworkInsightsAnalysis.
    """
    def __init__(__self__, alternate_path_hints=None, arn=None, explanations=None, filter_in_arns=None, filters=None, forward_path_components=None, id=None, network_insights_analysis_id=None, network_insights_path_id=None, path_found=None, return_path_components=None, start_date=None, status=None, status_message=None, tags=None, warning_message=None):
        if alternate_path_hints and not isinstance(alternate_path_hints, list):
            raise TypeError("Expected argument 'alternate_path_hints' to be a list")
        pulumi.set(__self__, "alternate_path_hints", alternate_path_hints)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if explanations and not isinstance(explanations, list):
            raise TypeError("Expected argument 'explanations' to be a list")
        pulumi.set(__self__, "explanations", explanations)
        if filter_in_arns and not isinstance(filter_in_arns, list):
            raise TypeError("Expected argument 'filter_in_arns' to be a list")
        pulumi.set(__self__, "filter_in_arns", filter_in_arns)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if forward_path_components and not isinstance(forward_path_components, list):
            raise TypeError("Expected argument 'forward_path_components' to be a list")
        pulumi.set(__self__, "forward_path_components", forward_path_components)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if network_insights_analysis_id and not isinstance(network_insights_analysis_id, str):
            raise TypeError("Expected argument 'network_insights_analysis_id' to be a str")
        pulumi.set(__self__, "network_insights_analysis_id", network_insights_analysis_id)
        if network_insights_path_id and not isinstance(network_insights_path_id, str):
            raise TypeError("Expected argument 'network_insights_path_id' to be a str")
        pulumi.set(__self__, "network_insights_path_id", network_insights_path_id)
        if path_found and not isinstance(path_found, bool):
            raise TypeError("Expected argument 'path_found' to be a bool")
        pulumi.set(__self__, "path_found", path_found)
        if return_path_components and not isinstance(return_path_components, list):
            raise TypeError("Expected argument 'return_path_components' to be a list")
        pulumi.set(__self__, "return_path_components", return_path_components)
        if start_date and not isinstance(start_date, str):
            raise TypeError("Expected argument 'start_date' to be a str")
        pulumi.set(__self__, "start_date", start_date)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if status_message and not isinstance(status_message, str):
            raise TypeError("Expected argument 'status_message' to be a str")
        pulumi.set(__self__, "status_message", status_message)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if warning_message and not isinstance(warning_message, str):
            raise TypeError("Expected argument 'warning_message' to be a str")
        pulumi.set(__self__, "warning_message", warning_message)

    @property
    @pulumi.getter(name="alternatePathHints")
    def alternate_path_hints(self) -> Sequence['outputs.GetNetworkInsightsAnalysisAlternatePathHintResult']:
        """
        Potential intermediate components of a feasible path.
        """
        return pulumi.get(self, "alternate_path_hints")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the selected Network Insights Analysis.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def explanations(self) -> Sequence['outputs.GetNetworkInsightsAnalysisExplanationResult']:
        """
        Explanation codes for an unreachable path.
        """
        return pulumi.get(self, "explanations")

    @property
    @pulumi.getter(name="filterInArns")
    def filter_in_arns(self) -> Sequence[str]:
        """
        ARNs of the AWS resources that the path must traverse.
        """
        return pulumi.get(self, "filter_in_arns")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetNetworkInsightsAnalysisFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter(name="forwardPathComponents")
    def forward_path_components(self) -> Sequence['outputs.GetNetworkInsightsAnalysisForwardPathComponentResult']:
        """
        The components in the path from source to destination.
        """
        return pulumi.get(self, "forward_path_components")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="networkInsightsAnalysisId")
    def network_insights_analysis_id(self) -> str:
        return pulumi.get(self, "network_insights_analysis_id")

    @property
    @pulumi.getter(name="networkInsightsPathId")
    def network_insights_path_id(self) -> str:
        """
        The ID of the path.
        """
        return pulumi.get(self, "network_insights_path_id")

    @property
    @pulumi.getter(name="pathFound")
    def path_found(self) -> bool:
        """
        Set to `true` if the destination was reachable.
        """
        return pulumi.get(self, "path_found")

    @property
    @pulumi.getter(name="returnPathComponents")
    def return_path_components(self) -> Sequence['outputs.GetNetworkInsightsAnalysisReturnPathComponentResult']:
        """
        The components in the path from destination to source.
        """
        return pulumi.get(self, "return_path_components")

    @property
    @pulumi.getter(name="startDate")
    def start_date(self) -> str:
        """
        Date/time the analysis was started.
        """
        return pulumi.get(self, "start_date")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the analysis. `succeeded` means the analysis was completed, not that a path was found, for that see `path_found`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusMessage")
    def status_message(self) -> str:
        """
        Message to provide more context when the `status` is `failed`.
        """
        return pulumi.get(self, "status_message")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="warningMessage")
    def warning_message(self) -> str:
        """
        Warning message.
        """
        return pulumi.get(self, "warning_message")


class AwaitableGetNetworkInsightsAnalysisResult(GetNetworkInsightsAnalysisResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkInsightsAnalysisResult(
            alternate_path_hints=self.alternate_path_hints,
            arn=self.arn,
            explanations=self.explanations,
            filter_in_arns=self.filter_in_arns,
            filters=self.filters,
            forward_path_components=self.forward_path_components,
            id=self.id,
            network_insights_analysis_id=self.network_insights_analysis_id,
            network_insights_path_id=self.network_insights_path_id,
            path_found=self.path_found,
            return_path_components=self.return_path_components,
            start_date=self.start_date,
            status=self.status,
            status_message=self.status_message,
            tags=self.tags,
            warning_message=self.warning_message)


def get_network_insights_analysis(filters: Optional[Sequence[pulumi.InputType['GetNetworkInsightsAnalysisFilterArgs']]] = None,
                                  network_insights_analysis_id: Optional[str] = None,
                                  tags: Optional[Mapping[str, str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkInsightsAnalysisResult:
    """
    `ec2.NetworkInsightsAnalysis` provides details about a specific Network Insights Analysis.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_network_insights_analysis(network_insights_analysis_id=example_aws_ec2_network_insights_analysis["id"])
    ```


    :param Sequence[pulumi.InputType['GetNetworkInsightsAnalysisFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    :param str network_insights_analysis_id: ID of the Network Insights Analysis to select.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['networkInsightsAnalysisId'] = network_insights_analysis_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getNetworkInsightsAnalysis:getNetworkInsightsAnalysis', __args__, opts=opts, typ=GetNetworkInsightsAnalysisResult).value

    return AwaitableGetNetworkInsightsAnalysisResult(
        alternate_path_hints=pulumi.get(__ret__, 'alternate_path_hints'),
        arn=pulumi.get(__ret__, 'arn'),
        explanations=pulumi.get(__ret__, 'explanations'),
        filter_in_arns=pulumi.get(__ret__, 'filter_in_arns'),
        filters=pulumi.get(__ret__, 'filters'),
        forward_path_components=pulumi.get(__ret__, 'forward_path_components'),
        id=pulumi.get(__ret__, 'id'),
        network_insights_analysis_id=pulumi.get(__ret__, 'network_insights_analysis_id'),
        network_insights_path_id=pulumi.get(__ret__, 'network_insights_path_id'),
        path_found=pulumi.get(__ret__, 'path_found'),
        return_path_components=pulumi.get(__ret__, 'return_path_components'),
        start_date=pulumi.get(__ret__, 'start_date'),
        status=pulumi.get(__ret__, 'status'),
        status_message=pulumi.get(__ret__, 'status_message'),
        tags=pulumi.get(__ret__, 'tags'),
        warning_message=pulumi.get(__ret__, 'warning_message'))


@_utilities.lift_output_func(get_network_insights_analysis)
def get_network_insights_analysis_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetNetworkInsightsAnalysisFilterArgs']]]]] = None,
                                         network_insights_analysis_id: Optional[pulumi.Input[Optional[str]]] = None,
                                         tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNetworkInsightsAnalysisResult]:
    """
    `ec2.NetworkInsightsAnalysis` provides details about a specific Network Insights Analysis.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_network_insights_analysis(network_insights_analysis_id=example_aws_ec2_network_insights_analysis["id"])
    ```


    :param Sequence[pulumi.InputType['GetNetworkInsightsAnalysisFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    :param str network_insights_analysis_id: ID of the Network Insights Analysis to select.
    """
    ...
