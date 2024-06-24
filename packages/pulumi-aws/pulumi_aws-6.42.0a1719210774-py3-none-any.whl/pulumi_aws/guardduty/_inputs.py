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
    'DetectorDatasourcesArgs',
    'DetectorDatasourcesKubernetesArgs',
    'DetectorDatasourcesKubernetesAuditLogsArgs',
    'DetectorDatasourcesMalwareProtectionArgs',
    'DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs',
    'DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs',
    'DetectorDatasourcesS3LogsArgs',
    'DetectorFeatureAdditionalConfigurationArgs',
    'FilterFindingCriteriaArgs',
    'FilterFindingCriteriaCriterionArgs',
    'MalwareProtectionPlanActionArgs',
    'MalwareProtectionPlanProtectedResourceArgs',
    'MalwareProtectionPlanProtectedResourceS3BucketArgs',
    'OrganizationConfigurationDatasourcesArgs',
    'OrganizationConfigurationDatasourcesKubernetesArgs',
    'OrganizationConfigurationDatasourcesKubernetesAuditLogsArgs',
    'OrganizationConfigurationDatasourcesMalwareProtectionArgs',
    'OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs',
    'OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs',
    'OrganizationConfigurationDatasourcesS3LogsArgs',
    'OrganizationConfigurationFeatureAdditionalConfigurationArgs',
]

@pulumi.input_type
class DetectorDatasourcesArgs:
    def __init__(__self__, *,
                 kubernetes: Optional[pulumi.Input['DetectorDatasourcesKubernetesArgs']] = None,
                 malware_protection: Optional[pulumi.Input['DetectorDatasourcesMalwareProtectionArgs']] = None,
                 s3_logs: Optional[pulumi.Input['DetectorDatasourcesS3LogsArgs']] = None):
        """
        :param pulumi.Input['DetectorDatasourcesKubernetesArgs'] kubernetes: Configures [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               See Kubernetes and Kubernetes Audit Logs below for more details.
        :param pulumi.Input['DetectorDatasourcesMalwareProtectionArgs'] malware_protection: Configures [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html).
               See Malware Protection, Scan EC2 instance with findings and EBS volumes below for more details.
        :param pulumi.Input['DetectorDatasourcesS3LogsArgs'] s3_logs: Configures [S3 protection](https://docs.aws.amazon.com/guardduty/latest/ug/s3-protection.html).
               See S3 Logs below for more details.
        """
        if kubernetes is not None:
            pulumi.set(__self__, "kubernetes", kubernetes)
        if malware_protection is not None:
            pulumi.set(__self__, "malware_protection", malware_protection)
        if s3_logs is not None:
            pulumi.set(__self__, "s3_logs", s3_logs)

    @property
    @pulumi.getter
    def kubernetes(self) -> Optional[pulumi.Input['DetectorDatasourcesKubernetesArgs']]:
        """
        Configures [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        See Kubernetes and Kubernetes Audit Logs below for more details.
        """
        return pulumi.get(self, "kubernetes")

    @kubernetes.setter
    def kubernetes(self, value: Optional[pulumi.Input['DetectorDatasourcesKubernetesArgs']]):
        pulumi.set(self, "kubernetes", value)

    @property
    @pulumi.getter(name="malwareProtection")
    def malware_protection(self) -> Optional[pulumi.Input['DetectorDatasourcesMalwareProtectionArgs']]:
        """
        Configures [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html).
        See Malware Protection, Scan EC2 instance with findings and EBS volumes below for more details.
        """
        return pulumi.get(self, "malware_protection")

    @malware_protection.setter
    def malware_protection(self, value: Optional[pulumi.Input['DetectorDatasourcesMalwareProtectionArgs']]):
        pulumi.set(self, "malware_protection", value)

    @property
    @pulumi.getter(name="s3Logs")
    def s3_logs(self) -> Optional[pulumi.Input['DetectorDatasourcesS3LogsArgs']]:
        """
        Configures [S3 protection](https://docs.aws.amazon.com/guardduty/latest/ug/s3-protection.html).
        See S3 Logs below for more details.
        """
        return pulumi.get(self, "s3_logs")

    @s3_logs.setter
    def s3_logs(self, value: Optional[pulumi.Input['DetectorDatasourcesS3LogsArgs']]):
        pulumi.set(self, "s3_logs", value)


@pulumi.input_type
class DetectorDatasourcesKubernetesArgs:
    def __init__(__self__, *,
                 audit_logs: pulumi.Input['DetectorDatasourcesKubernetesAuditLogsArgs']):
        """
        :param pulumi.Input['DetectorDatasourcesKubernetesAuditLogsArgs'] audit_logs: Configures Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               See Kubernetes Audit Logs below for more details.
        """
        pulumi.set(__self__, "audit_logs", audit_logs)

    @property
    @pulumi.getter(name="auditLogs")
    def audit_logs(self) -> pulumi.Input['DetectorDatasourcesKubernetesAuditLogsArgs']:
        """
        Configures Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        See Kubernetes Audit Logs below for more details.
        """
        return pulumi.get(self, "audit_logs")

    @audit_logs.setter
    def audit_logs(self, value: pulumi.Input['DetectorDatasourcesKubernetesAuditLogsArgs']):
        pulumi.set(self, "audit_logs", value)


@pulumi.input_type
class DetectorDatasourcesKubernetesAuditLogsArgs:
    def __init__(__self__, *,
                 enable: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] enable: If true, enables Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               Defaults to `true`.
        """
        pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> pulumi.Input[bool]:
        """
        If true, enables Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        Defaults to `true`.
        """
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enable", value)


@pulumi.input_type
class DetectorDatasourcesMalwareProtectionArgs:
    def __init__(__self__, *,
                 scan_ec2_instance_with_findings: pulumi.Input['DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs']):
        """
        :param pulumi.Input['DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs'] scan_ec2_instance_with_findings: Configure whether [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) is enabled as data source for EC2 instances with findings for the detector.
               See Scan EC2 instance with findings below for more details.
        """
        pulumi.set(__self__, "scan_ec2_instance_with_findings", scan_ec2_instance_with_findings)

    @property
    @pulumi.getter(name="scanEc2InstanceWithFindings")
    def scan_ec2_instance_with_findings(self) -> pulumi.Input['DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs']:
        """
        Configure whether [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) is enabled as data source for EC2 instances with findings for the detector.
        See Scan EC2 instance with findings below for more details.
        """
        return pulumi.get(self, "scan_ec2_instance_with_findings")

    @scan_ec2_instance_with_findings.setter
    def scan_ec2_instance_with_findings(self, value: pulumi.Input['DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs']):
        pulumi.set(self, "scan_ec2_instance_with_findings", value)


@pulumi.input_type
class DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs:
    def __init__(__self__, *,
                 ebs_volumes: pulumi.Input['DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs']):
        """
        :param pulumi.Input['DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs'] ebs_volumes: Configure whether scanning EBS volumes is enabled as data source for the detector for instances with findings.
               See EBS volumes below for more details.
        """
        pulumi.set(__self__, "ebs_volumes", ebs_volumes)

    @property
    @pulumi.getter(name="ebsVolumes")
    def ebs_volumes(self) -> pulumi.Input['DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs']:
        """
        Configure whether scanning EBS volumes is enabled as data source for the detector for instances with findings.
        See EBS volumes below for more details.
        """
        return pulumi.get(self, "ebs_volumes")

    @ebs_volumes.setter
    def ebs_volumes(self, value: pulumi.Input['DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs']):
        pulumi.set(self, "ebs_volumes", value)


@pulumi.input_type
class DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs:
    def __init__(__self__, *,
                 enable: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] enable: If true, enables [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) as data source for the detector.
               Defaults to `true`.
        """
        pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> pulumi.Input[bool]:
        """
        If true, enables [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) as data source for the detector.
        Defaults to `true`.
        """
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enable", value)


@pulumi.input_type
class DetectorDatasourcesS3LogsArgs:
    def __init__(__self__, *,
                 enable: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] enable: If true, enables [S3 protection](https://docs.aws.amazon.com/guardduty/latest/ug/s3-protection.html).
               Defaults to `true`.
        """
        pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> pulumi.Input[bool]:
        """
        If true, enables [S3 protection](https://docs.aws.amazon.com/guardduty/latest/ug/s3-protection.html).
        Defaults to `true`.
        """
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enable", value)


@pulumi.input_type
class DetectorFeatureAdditionalConfigurationArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 status: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The name of the additional configuration for a feature. Valid values: `EKS_ADDON_MANAGEMENT`, `ECS_FARGATE_AGENT_MANAGEMENT`, `EC2_AGENT_MANAGEMENT`. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorAdditionalConfiguration.html) for the current list of supported values.
        :param pulumi.Input[str] status: The status of the additional configuration. Valid values: `ENABLED`, `DISABLED`.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the additional configuration for a feature. Valid values: `EKS_ADDON_MANAGEMENT`, `ECS_FARGATE_AGENT_MANAGEMENT`, `EC2_AGENT_MANAGEMENT`. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorAdditionalConfiguration.html) for the current list of supported values.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> pulumi.Input[str]:
        """
        The status of the additional configuration. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: pulumi.Input[str]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class FilterFindingCriteriaArgs:
    def __init__(__self__, *,
                 criterions: pulumi.Input[Sequence[pulumi.Input['FilterFindingCriteriaCriterionArgs']]]):
        pulumi.set(__self__, "criterions", criterions)

    @property
    @pulumi.getter
    def criterions(self) -> pulumi.Input[Sequence[pulumi.Input['FilterFindingCriteriaCriterionArgs']]]:
        return pulumi.get(self, "criterions")

    @criterions.setter
    def criterions(self, value: pulumi.Input[Sequence[pulumi.Input['FilterFindingCriteriaCriterionArgs']]]):
        pulumi.set(self, "criterions", value)


@pulumi.input_type
class FilterFindingCriteriaCriterionArgs:
    def __init__(__self__, *,
                 field: pulumi.Input[str],
                 equals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 greater_than: Optional[pulumi.Input[str]] = None,
                 greater_than_or_equal: Optional[pulumi.Input[str]] = None,
                 less_than: Optional[pulumi.Input[str]] = None,
                 less_than_or_equal: Optional[pulumi.Input[str]] = None,
                 not_equals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] field: The name of the field to be evaluated. The full list of field names can be found in [AWS documentation](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_filter-findings.html#filter_criteria).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] equals: List of string values to be evaluated.
        :param pulumi.Input[str] greater_than: A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param pulumi.Input[str] greater_than_or_equal: A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param pulumi.Input[str] less_than: A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param pulumi.Input[str] less_than_or_equal: A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_equals: List of string values to be evaluated.
        """
        pulumi.set(__self__, "field", field)
        if equals is not None:
            pulumi.set(__self__, "equals", equals)
        if greater_than is not None:
            pulumi.set(__self__, "greater_than", greater_than)
        if greater_than_or_equal is not None:
            pulumi.set(__self__, "greater_than_or_equal", greater_than_or_equal)
        if less_than is not None:
            pulumi.set(__self__, "less_than", less_than)
        if less_than_or_equal is not None:
            pulumi.set(__self__, "less_than_or_equal", less_than_or_equal)
        if not_equals is not None:
            pulumi.set(__self__, "not_equals", not_equals)

    @property
    @pulumi.getter
    def field(self) -> pulumi.Input[str]:
        """
        The name of the field to be evaluated. The full list of field names can be found in [AWS documentation](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_filter-findings.html#filter_criteria).
        """
        return pulumi.get(self, "field")

    @field.setter
    def field(self, value: pulumi.Input[str]):
        pulumi.set(self, "field", value)

    @property
    @pulumi.getter
    def equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of string values to be evaluated.
        """
        return pulumi.get(self, "equals")

    @equals.setter
    def equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "equals", value)

    @property
    @pulumi.getter(name="greaterThan")
    def greater_than(self) -> Optional[pulumi.Input[str]]:
        """
        A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "greater_than")

    @greater_than.setter
    def greater_than(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "greater_than", value)

    @property
    @pulumi.getter(name="greaterThanOrEqual")
    def greater_than_or_equal(self) -> Optional[pulumi.Input[str]]:
        """
        A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "greater_than_or_equal")

    @greater_than_or_equal.setter
    def greater_than_or_equal(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "greater_than_or_equal", value)

    @property
    @pulumi.getter(name="lessThan")
    def less_than(self) -> Optional[pulumi.Input[str]]:
        """
        A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "less_than")

    @less_than.setter
    def less_than(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "less_than", value)

    @property
    @pulumi.getter(name="lessThanOrEqual")
    def less_than_or_equal(self) -> Optional[pulumi.Input[str]]:
        """
        A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "less_than_or_equal")

    @less_than_or_equal.setter
    def less_than_or_equal(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "less_than_or_equal", value)

    @property
    @pulumi.getter(name="notEquals")
    def not_equals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of string values to be evaluated.
        """
        return pulumi.get(self, "not_equals")

    @not_equals.setter
    def not_equals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_equals", value)


@pulumi.input_type
class MalwareProtectionPlanActionArgs:
    def __init__(__self__, *,
                 taggings: pulumi.Input[Sequence[Any]]):
        """
        :param pulumi.Input[Sequence[Any]] taggings: Indicates whether the scanned S3 object will have tags about the scan result. See `tagging` below.
        """
        pulumi.set(__self__, "taggings", taggings)

    @property
    @pulumi.getter
    def taggings(self) -> pulumi.Input[Sequence[Any]]:
        """
        Indicates whether the scanned S3 object will have tags about the scan result. See `tagging` below.
        """
        return pulumi.get(self, "taggings")

    @taggings.setter
    def taggings(self, value: pulumi.Input[Sequence[Any]]):
        pulumi.set(self, "taggings", value)


@pulumi.input_type
class MalwareProtectionPlanProtectedResourceArgs:
    def __init__(__self__, *,
                 s3_bucket: Optional[pulumi.Input['MalwareProtectionPlanProtectedResourceS3BucketArgs']] = None):
        """
        :param pulumi.Input['MalwareProtectionPlanProtectedResourceS3BucketArgs'] s3_bucket: Information about the protected S3 bucket resource. See `s3_bucket` below.
        """
        if s3_bucket is not None:
            pulumi.set(__self__, "s3_bucket", s3_bucket)

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> Optional[pulumi.Input['MalwareProtectionPlanProtectedResourceS3BucketArgs']]:
        """
        Information about the protected S3 bucket resource. See `s3_bucket` below.
        """
        return pulumi.get(self, "s3_bucket")

    @s3_bucket.setter
    def s3_bucket(self, value: Optional[pulumi.Input['MalwareProtectionPlanProtectedResourceS3BucketArgs']]):
        pulumi.set(self, "s3_bucket", value)


@pulumi.input_type
class MalwareProtectionPlanProtectedResourceS3BucketArgs:
    def __init__(__self__, *,
                 bucket_name: pulumi.Input[str],
                 object_prefixes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] bucket_name: Name of the S3 bucket.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] object_prefixes: The list of object prefixes that specify the S3 objects that will be scanned.
        """
        pulumi.set(__self__, "bucket_name", bucket_name)
        if object_prefixes is not None:
            pulumi.set(__self__, "object_prefixes", object_prefixes)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Input[str]:
        """
        Name of the S3 bucket.
        """
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter(name="objectPrefixes")
    def object_prefixes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of object prefixes that specify the S3 objects that will be scanned.
        """
        return pulumi.get(self, "object_prefixes")

    @object_prefixes.setter
    def object_prefixes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "object_prefixes", value)


@pulumi.input_type
class OrganizationConfigurationDatasourcesArgs:
    def __init__(__self__, *,
                 kubernetes: Optional[pulumi.Input['OrganizationConfigurationDatasourcesKubernetesArgs']] = None,
                 malware_protection: Optional[pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionArgs']] = None,
                 s3_logs: Optional[pulumi.Input['OrganizationConfigurationDatasourcesS3LogsArgs']] = None):
        """
        :param pulumi.Input['OrganizationConfigurationDatasourcesKubernetesArgs'] kubernetes: Enable Kubernetes Audit Logs Monitoring automatically for new member accounts.
        :param pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionArgs'] malware_protection: Enable Malware Protection automatically for new member accounts.
        :param pulumi.Input['OrganizationConfigurationDatasourcesS3LogsArgs'] s3_logs: Enable S3 Protection automatically for new member accounts.
        """
        if kubernetes is not None:
            pulumi.set(__self__, "kubernetes", kubernetes)
        if malware_protection is not None:
            pulumi.set(__self__, "malware_protection", malware_protection)
        if s3_logs is not None:
            pulumi.set(__self__, "s3_logs", s3_logs)

    @property
    @pulumi.getter
    def kubernetes(self) -> Optional[pulumi.Input['OrganizationConfigurationDatasourcesKubernetesArgs']]:
        """
        Enable Kubernetes Audit Logs Monitoring automatically for new member accounts.
        """
        return pulumi.get(self, "kubernetes")

    @kubernetes.setter
    def kubernetes(self, value: Optional[pulumi.Input['OrganizationConfigurationDatasourcesKubernetesArgs']]):
        pulumi.set(self, "kubernetes", value)

    @property
    @pulumi.getter(name="malwareProtection")
    def malware_protection(self) -> Optional[pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionArgs']]:
        """
        Enable Malware Protection automatically for new member accounts.
        """
        return pulumi.get(self, "malware_protection")

    @malware_protection.setter
    def malware_protection(self, value: Optional[pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionArgs']]):
        pulumi.set(self, "malware_protection", value)

    @property
    @pulumi.getter(name="s3Logs")
    def s3_logs(self) -> Optional[pulumi.Input['OrganizationConfigurationDatasourcesS3LogsArgs']]:
        """
        Enable S3 Protection automatically for new member accounts.
        """
        return pulumi.get(self, "s3_logs")

    @s3_logs.setter
    def s3_logs(self, value: Optional[pulumi.Input['OrganizationConfigurationDatasourcesS3LogsArgs']]):
        pulumi.set(self, "s3_logs", value)


@pulumi.input_type
class OrganizationConfigurationDatasourcesKubernetesArgs:
    def __init__(__self__, *,
                 audit_logs: pulumi.Input['OrganizationConfigurationDatasourcesKubernetesAuditLogsArgs']):
        """
        :param pulumi.Input['OrganizationConfigurationDatasourcesKubernetesAuditLogsArgs'] audit_logs: Enable Kubernetes Audit Logs Monitoring automatically for new member accounts. [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               See Kubernetes Audit Logs below for more details.
        """
        pulumi.set(__self__, "audit_logs", audit_logs)

    @property
    @pulumi.getter(name="auditLogs")
    def audit_logs(self) -> pulumi.Input['OrganizationConfigurationDatasourcesKubernetesAuditLogsArgs']:
        """
        Enable Kubernetes Audit Logs Monitoring automatically for new member accounts. [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        See Kubernetes Audit Logs below for more details.
        """
        return pulumi.get(self, "audit_logs")

    @audit_logs.setter
    def audit_logs(self, value: pulumi.Input['OrganizationConfigurationDatasourcesKubernetesAuditLogsArgs']):
        pulumi.set(self, "audit_logs", value)


@pulumi.input_type
class OrganizationConfigurationDatasourcesKubernetesAuditLogsArgs:
    def __init__(__self__, *,
                 enable: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] enable: If true, enables Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               Defaults to `true`.
        """
        pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> pulumi.Input[bool]:
        """
        If true, enables Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        Defaults to `true`.
        """
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enable", value)


@pulumi.input_type
class OrganizationConfigurationDatasourcesMalwareProtectionArgs:
    def __init__(__self__, *,
                 scan_ec2_instance_with_findings: pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs']):
        """
        :param pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs'] scan_ec2_instance_with_findings: Configure whether [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) for EC2 instances with findings should be auto-enabled for new members joining the organization.
               See Scan EC2 instance with findings below for more details.
        """
        pulumi.set(__self__, "scan_ec2_instance_with_findings", scan_ec2_instance_with_findings)

    @property
    @pulumi.getter(name="scanEc2InstanceWithFindings")
    def scan_ec2_instance_with_findings(self) -> pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs']:
        """
        Configure whether [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) for EC2 instances with findings should be auto-enabled for new members joining the organization.
        See Scan EC2 instance with findings below for more details.
        """
        return pulumi.get(self, "scan_ec2_instance_with_findings")

    @scan_ec2_instance_with_findings.setter
    def scan_ec2_instance_with_findings(self, value: pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs']):
        pulumi.set(self, "scan_ec2_instance_with_findings", value)


@pulumi.input_type
class OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs:
    def __init__(__self__, *,
                 ebs_volumes: pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs']):
        """
        :param pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs'] ebs_volumes: Configure whether scanning EBS volumes should be auto-enabled for new members joining the organization
               See EBS volumes below for more details.
        """
        pulumi.set(__self__, "ebs_volumes", ebs_volumes)

    @property
    @pulumi.getter(name="ebsVolumes")
    def ebs_volumes(self) -> pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs']:
        """
        Configure whether scanning EBS volumes should be auto-enabled for new members joining the organization
        See EBS volumes below for more details.
        """
        return pulumi.get(self, "ebs_volumes")

    @ebs_volumes.setter
    def ebs_volumes(self, value: pulumi.Input['OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs']):
        pulumi.set(self, "ebs_volumes", value)


@pulumi.input_type
class OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs:
    def __init__(__self__, *,
                 auto_enable: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] auto_enable: If true, enables [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) for all new accounts joining the organization.
               Defaults to `true`.
        """
        pulumi.set(__self__, "auto_enable", auto_enable)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> pulumi.Input[bool]:
        """
        If true, enables [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) for all new accounts joining the organization.
        Defaults to `true`.
        """
        return pulumi.get(self, "auto_enable")

    @auto_enable.setter
    def auto_enable(self, value: pulumi.Input[bool]):
        pulumi.set(self, "auto_enable", value)


@pulumi.input_type
class OrganizationConfigurationDatasourcesS3LogsArgs:
    def __init__(__self__, *,
                 auto_enable: pulumi.Input[bool]):
        """
        :param pulumi.Input[bool] auto_enable: Set to `true` if you want S3 data event logs to be automatically enabled for new members of the organization. Default: `false`
        """
        pulumi.set(__self__, "auto_enable", auto_enable)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> pulumi.Input[bool]:
        """
        Set to `true` if you want S3 data event logs to be automatically enabled for new members of the organization. Default: `false`
        """
        return pulumi.get(self, "auto_enable")

    @auto_enable.setter
    def auto_enable(self, value: pulumi.Input[bool]):
        pulumi.set(self, "auto_enable", value)


@pulumi.input_type
class OrganizationConfigurationFeatureAdditionalConfigurationArgs:
    def __init__(__self__, *,
                 auto_enable: pulumi.Input[str],
                 name: pulumi.Input[str]):
        """
        :param pulumi.Input[str] auto_enable: The status of the additional configuration that will be configured for the organization. Valid values: `NEW`, `ALL`, `NONE`.
        :param pulumi.Input[str] name: The name of the additional configuration for a feature that will be configured for the organization. Valid values: `EKS_ADDON_MANAGEMENT`, `ECS_FARGATE_AGENT_MANAGEMENT`, `EC2_AGENT_MANAGEMENT`. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorAdditionalConfiguration.html) for the current list of supported values.
        """
        pulumi.set(__self__, "auto_enable", auto_enable)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> pulumi.Input[str]:
        """
        The status of the additional configuration that will be configured for the organization. Valid values: `NEW`, `ALL`, `NONE`.
        """
        return pulumi.get(self, "auto_enable")

    @auto_enable.setter
    def auto_enable(self, value: pulumi.Input[str]):
        pulumi.set(self, "auto_enable", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the additional configuration for a feature that will be configured for the organization. Valid values: `EKS_ADDON_MANAGEMENT`, `ECS_FARGATE_AGENT_MANAGEMENT`, `EC2_AGENT_MANAGEMENT`. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorAdditionalConfiguration.html) for the current list of supported values.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


