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
    'HostVpcConfigurationArgs',
]

@pulumi.input_type
class HostVpcConfigurationArgs:
    def __init__(__self__, *,
                 security_group_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 subnet_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 vpc_id: pulumi.Input[str],
                 tls_certificate: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_ids: ID of the security group or security groups associated with the Amazon VPC connected to the infrastructure where your provider type is installed.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: The ID of the subnet or subnets associated with the Amazon VPC connected to the infrastructure where your provider type is installed.
        :param pulumi.Input[str] vpc_id: The ID of the Amazon VPC connected to the infrastructure where your provider type is installed.
        :param pulumi.Input[str] tls_certificate: The value of the Transport Layer Security (TLS) certificate associated with the infrastructure where your provider type is installed.
        """
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        pulumi.set(__self__, "vpc_id", vpc_id)
        if tls_certificate is not None:
            pulumi.set(__self__, "tls_certificate", tls_certificate)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        ID of the security group or security groups associated with the Amazon VPC connected to the infrastructure where your provider type is installed.
        """
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The ID of the subnet or subnets associated with the Amazon VPC connected to the infrastructure where your provider type is installed.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The ID of the Amazon VPC connected to the infrastructure where your provider type is installed.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter(name="tlsCertificate")
    def tls_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The value of the Transport Layer Security (TLS) certificate associated with the infrastructure where your provider type is installed.
        """
        return pulumi.get(self, "tls_certificate")

    @tls_certificate.setter
    def tls_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tls_certificate", value)


