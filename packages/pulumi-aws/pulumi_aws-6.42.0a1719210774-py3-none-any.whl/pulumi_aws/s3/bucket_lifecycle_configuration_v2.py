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

__all__ = ['BucketLifecycleConfigurationV2Args', 'BucketLifecycleConfigurationV2']

@pulumi.input_type
class BucketLifecycleConfigurationV2Args:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 rules: pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]],
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BucketLifecycleConfigurationV2 resource.
        :param pulumi.Input[str] bucket: Name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]] rules: List of configuration blocks describing the rules managing the replication. See below.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        """
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "rules", rules)
        if expected_bucket_owner is not None:
            pulumi.set(__self__, "expected_bucket_owner", expected_bucket_owner)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        Name of the source S3 bucket you want Amazon S3 to monitor.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]:
        """
        List of configuration blocks describing the rules managing the replication. See below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> Optional[pulumi.Input[str]]:
        """
        Account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expected_bucket_owner", value)


@pulumi.input_type
class _BucketLifecycleConfigurationV2State:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]] = None):
        """
        Input properties used for looking up and filtering BucketLifecycleConfigurationV2 resources.
        :param pulumi.Input[str] bucket: Name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        :param pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]] rules: List of configuration blocks describing the rules managing the replication. See below.
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if expected_bucket_owner is not None:
            pulumi.set(__self__, "expected_bucket_owner", expected_bucket_owner)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the source S3 bucket you want Amazon S3 to monitor.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> Optional[pulumi.Input[str]]:
        """
        Account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expected_bucket_owner", value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]]:
        """
        List of configuration blocks describing the rules managing the replication. See below.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BucketLifecycleConfigurationV2RuleArgs']]]]):
        pulumi.set(self, "rules", value)


class BucketLifecycleConfigurationV2(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]]] = None,
                 __props__=None):
        """
        Provides an independent configuration resource for S3 bucket [lifecycle configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html).

        An S3 Lifecycle configuration consists of one or more Lifecycle rules. Each rule consists of the following:

        * Rule metadata (`id` and `status`)
        * Filter identifying objects to which the rule applies
        * One or more transition or expiration actions

        For more information see the Amazon S3 User Guide on [`Lifecycle Configuration Elements`](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html).

        > **NOTE:** S3 Buckets only support a single lifecycle configuration. Declaring multiple `s3.BucketLifecycleConfigurationV2` resources to the same S3 Bucket will cause a perpetual difference in configuration.

        > **NOTE:** Lifecycle configurations may take some time to fully propagate to all AWS S3 systems.
        Running Pulumi operations shortly after creating a lifecycle configuration may result in changes that affect configuration idempotence.
        See the Amazon S3 User Guide on [setting lifecycle configuration on a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html).

        > This resource cannot be used with S3 directory buckets.

        ## Example Usage

        ### With neither a filter nor prefix specified

        The Lifecycle rule applies to a subset of objects based on the key name prefix (`""`).

        This configuration is intended to replicate the default behavior of the `lifecycle_rule`
        parameter in the AWS Provider `s3.BucketV2` resource prior to `v4.0`.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                status="Enabled",
            )])
        ```

        ### Specifying an empty filter

        The Lifecycle rule applies to all objects in the bucket.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(),
                status="Enabled",
            )])
        ```

        ### Specifying a filter using key prefixes

        The Lifecycle rule applies to a subset of objects based on the key name prefix (`logs/`).

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    prefix="logs/",
                ),
                status="Enabled",
            )])
        ```

        If you want to apply a Lifecycle action to a subset of objects based on different key name prefixes, specify separate rules.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[
                aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                    id="rule-1",
                    filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                        prefix="logs/",
                    ),
                    status="Enabled",
                ),
                aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                    id="rule-2",
                    filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                        prefix="tmp/",
                    ),
                    status="Enabled",
                ),
            ])
        ```

        ### Specifying a filter based on an object tag

        The Lifecycle rule specifies a filter based on a tag key and value. The rule then applies only to a subset of objects with the specific tag.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    tag=aws.s3.BucketLifecycleConfigurationV2RuleFilterTagArgs(
                        key="Name",
                        value="Staging",
                    ),
                ),
                status="Enabled",
            )])
        ```

        ### Specifying a filter based on multiple tags

        The Lifecycle rule directs Amazon S3 to perform lifecycle actions on objects with two tags (with the specific tag keys and values). Notice `tags` is wrapped in the `and` configuration block.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    and_=aws.s3.BucketLifecycleConfigurationV2RuleFilterAndArgs(
                        tags={
                            "Key1": "Value1",
                            "Key2": "Value2",
                        },
                    ),
                ),
                status="Enabled",
            )])
        ```

        ### Specifying a filter based on both prefix and one or more tags

        The Lifecycle rule directs Amazon S3 to perform lifecycle actions on objects with the specified prefix and two tags (with the specific tag keys and values). Notice both `prefix` and `tags` are wrapped in the `and` configuration block.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    and_=aws.s3.BucketLifecycleConfigurationV2RuleFilterAndArgs(
                        prefix="logs/",
                        tags={
                            "Key1": "Value1",
                            "Key2": "Value2",
                        },
                    ),
                ),
                status="Enabled",
            )])
        ```

        ### Specifying a filter based on object size

        Object size values are in bytes. Maximum filter size is 5TB. Some storage classes have minimum object size limitations, for more information, see [Comparing the Amazon S3 storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html#sc-compare).

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    object_size_greater_than="500",
                ),
                status="Enabled",
            )])
        ```

        ### Specifying a filter based on object size range and prefix

        The `object_size_greater_than` must be less than the `object_size_less_than`. Notice both the object size range and prefix are wrapped in the `and` configuration block.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    and_=aws.s3.BucketLifecycleConfigurationV2RuleFilterAndArgs(
                        prefix="logs/",
                        object_size_greater_than=500,
                        object_size_less_than=64000,
                    ),
                ),
                status="Enabled",
            )])
        ```

        ### Creating a Lifecycle Configuration for a bucket with versioning

        ```python
        import pulumi
        import pulumi_aws as aws

        bucket = aws.s3.BucketV2("bucket", bucket="my-bucket")
        bucket_acl = aws.s3.BucketAclV2("bucket_acl",
            bucket=bucket.id,
            acl="private")
        bucket_config = aws.s3.BucketLifecycleConfigurationV2("bucket-config",
            bucket=bucket.id,
            rules=[
                aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                    id="log",
                    expiration=aws.s3.BucketLifecycleConfigurationV2RuleExpirationArgs(
                        days=90,
                    ),
                    filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                        and_=aws.s3.BucketLifecycleConfigurationV2RuleFilterAndArgs(
                            prefix="log/",
                            tags={
                                "rule": "log",
                                "autoclean": "true",
                            },
                        ),
                    ),
                    status="Enabled",
                    transitions=[
                        aws.s3.BucketLifecycleConfigurationV2RuleTransitionArgs(
                            days=30,
                            storage_class="STANDARD_IA",
                        ),
                        aws.s3.BucketLifecycleConfigurationV2RuleTransitionArgs(
                            days=60,
                            storage_class="GLACIER",
                        ),
                    ],
                ),
                aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                    id="tmp",
                    filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                        prefix="tmp/",
                    ),
                    expiration=aws.s3.BucketLifecycleConfigurationV2RuleExpirationArgs(
                        date="2023-01-13T00:00:00Z",
                    ),
                    status="Enabled",
                ),
            ])
        versioning_bucket = aws.s3.BucketV2("versioning_bucket", bucket="my-versioning-bucket")
        versioning_bucket_acl = aws.s3.BucketAclV2("versioning_bucket_acl",
            bucket=versioning_bucket.id,
            acl="private")
        versioning = aws.s3.BucketVersioningV2("versioning",
            bucket=versioning_bucket.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        versioning_bucket_config = aws.s3.BucketLifecycleConfigurationV2("versioning-bucket-config",
            bucket=versioning_bucket.id,
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="config",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    prefix="config/",
                ),
                noncurrent_version_expiration=aws.s3.BucketLifecycleConfigurationV2RuleNoncurrentVersionExpirationArgs(
                    noncurrent_days=90,
                ),
                noncurrent_version_transitions=[
                    aws.s3.BucketLifecycleConfigurationV2RuleNoncurrentVersionTransitionArgs(
                        noncurrent_days=30,
                        storage_class="STANDARD_IA",
                    ),
                    aws.s3.BucketLifecycleConfigurationV2RuleNoncurrentVersionTransitionArgs(
                        noncurrent_days=60,
                        storage_class="GLACIER",
                    ),
                ],
                status="Enabled",
            )],
            opts=pulumi.ResourceOptions(depends_on=[versioning]))
        ```

        ## Import

        If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, import using the `bucket` and `expected_bucket_owner` separated by a comma (`,`):

        __Using `pulumi import` to import__ S3 bucket lifecycle configuration using the `bucket` or using the `bucket` and `expected_bucket_owner` separated by a comma (`,`). For example:

        If the owner (account ID) of the source bucket is the same account used to configure the AWS Provider, import using the `bucket`:

        ```sh
        $ pulumi import aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2 example bucket-name
        ```
        If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, import using the `bucket` and `expected_bucket_owner` separated by a comma (`,`):

        ```sh
        $ pulumi import aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2 example bucket-name,123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]] rules: List of configuration blocks describing the rules managing the replication. See below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketLifecycleConfigurationV2Args,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an independent configuration resource for S3 bucket [lifecycle configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html).

        An S3 Lifecycle configuration consists of one or more Lifecycle rules. Each rule consists of the following:

        * Rule metadata (`id` and `status`)
        * Filter identifying objects to which the rule applies
        * One or more transition or expiration actions

        For more information see the Amazon S3 User Guide on [`Lifecycle Configuration Elements`](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html).

        > **NOTE:** S3 Buckets only support a single lifecycle configuration. Declaring multiple `s3.BucketLifecycleConfigurationV2` resources to the same S3 Bucket will cause a perpetual difference in configuration.

        > **NOTE:** Lifecycle configurations may take some time to fully propagate to all AWS S3 systems.
        Running Pulumi operations shortly after creating a lifecycle configuration may result in changes that affect configuration idempotence.
        See the Amazon S3 User Guide on [setting lifecycle configuration on a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html).

        > This resource cannot be used with S3 directory buckets.

        ## Example Usage

        ### With neither a filter nor prefix specified

        The Lifecycle rule applies to a subset of objects based on the key name prefix (`""`).

        This configuration is intended to replicate the default behavior of the `lifecycle_rule`
        parameter in the AWS Provider `s3.BucketV2` resource prior to `v4.0`.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                status="Enabled",
            )])
        ```

        ### Specifying an empty filter

        The Lifecycle rule applies to all objects in the bucket.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(),
                status="Enabled",
            )])
        ```

        ### Specifying a filter using key prefixes

        The Lifecycle rule applies to a subset of objects based on the key name prefix (`logs/`).

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    prefix="logs/",
                ),
                status="Enabled",
            )])
        ```

        If you want to apply a Lifecycle action to a subset of objects based on different key name prefixes, specify separate rules.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[
                aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                    id="rule-1",
                    filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                        prefix="logs/",
                    ),
                    status="Enabled",
                ),
                aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                    id="rule-2",
                    filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                        prefix="tmp/",
                    ),
                    status="Enabled",
                ),
            ])
        ```

        ### Specifying a filter based on an object tag

        The Lifecycle rule specifies a filter based on a tag key and value. The rule then applies only to a subset of objects with the specific tag.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    tag=aws.s3.BucketLifecycleConfigurationV2RuleFilterTagArgs(
                        key="Name",
                        value="Staging",
                    ),
                ),
                status="Enabled",
            )])
        ```

        ### Specifying a filter based on multiple tags

        The Lifecycle rule directs Amazon S3 to perform lifecycle actions on objects with two tags (with the specific tag keys and values). Notice `tags` is wrapped in the `and` configuration block.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    and_=aws.s3.BucketLifecycleConfigurationV2RuleFilterAndArgs(
                        tags={
                            "Key1": "Value1",
                            "Key2": "Value2",
                        },
                    ),
                ),
                status="Enabled",
            )])
        ```

        ### Specifying a filter based on both prefix and one or more tags

        The Lifecycle rule directs Amazon S3 to perform lifecycle actions on objects with the specified prefix and two tags (with the specific tag keys and values). Notice both `prefix` and `tags` are wrapped in the `and` configuration block.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    and_=aws.s3.BucketLifecycleConfigurationV2RuleFilterAndArgs(
                        prefix="logs/",
                        tags={
                            "Key1": "Value1",
                            "Key2": "Value2",
                        },
                    ),
                ),
                status="Enabled",
            )])
        ```

        ### Specifying a filter based on object size

        Object size values are in bytes. Maximum filter size is 5TB. Some storage classes have minimum object size limitations, for more information, see [Comparing the Amazon S3 storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html#sc-compare).

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    object_size_greater_than="500",
                ),
                status="Enabled",
            )])
        ```

        ### Specifying a filter based on object size range and prefix

        The `object_size_greater_than` must be less than the `object_size_less_than`. Notice both the object size range and prefix are wrapped in the `and` configuration block.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketLifecycleConfigurationV2("example",
            bucket=bucket["id"],
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="rule-1",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    and_=aws.s3.BucketLifecycleConfigurationV2RuleFilterAndArgs(
                        prefix="logs/",
                        object_size_greater_than=500,
                        object_size_less_than=64000,
                    ),
                ),
                status="Enabled",
            )])
        ```

        ### Creating a Lifecycle Configuration for a bucket with versioning

        ```python
        import pulumi
        import pulumi_aws as aws

        bucket = aws.s3.BucketV2("bucket", bucket="my-bucket")
        bucket_acl = aws.s3.BucketAclV2("bucket_acl",
            bucket=bucket.id,
            acl="private")
        bucket_config = aws.s3.BucketLifecycleConfigurationV2("bucket-config",
            bucket=bucket.id,
            rules=[
                aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                    id="log",
                    expiration=aws.s3.BucketLifecycleConfigurationV2RuleExpirationArgs(
                        days=90,
                    ),
                    filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                        and_=aws.s3.BucketLifecycleConfigurationV2RuleFilterAndArgs(
                            prefix="log/",
                            tags={
                                "rule": "log",
                                "autoclean": "true",
                            },
                        ),
                    ),
                    status="Enabled",
                    transitions=[
                        aws.s3.BucketLifecycleConfigurationV2RuleTransitionArgs(
                            days=30,
                            storage_class="STANDARD_IA",
                        ),
                        aws.s3.BucketLifecycleConfigurationV2RuleTransitionArgs(
                            days=60,
                            storage_class="GLACIER",
                        ),
                    ],
                ),
                aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                    id="tmp",
                    filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                        prefix="tmp/",
                    ),
                    expiration=aws.s3.BucketLifecycleConfigurationV2RuleExpirationArgs(
                        date="2023-01-13T00:00:00Z",
                    ),
                    status="Enabled",
                ),
            ])
        versioning_bucket = aws.s3.BucketV2("versioning_bucket", bucket="my-versioning-bucket")
        versioning_bucket_acl = aws.s3.BucketAclV2("versioning_bucket_acl",
            bucket=versioning_bucket.id,
            acl="private")
        versioning = aws.s3.BucketVersioningV2("versioning",
            bucket=versioning_bucket.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        versioning_bucket_config = aws.s3.BucketLifecycleConfigurationV2("versioning-bucket-config",
            bucket=versioning_bucket.id,
            rules=[aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="config",
                filter=aws.s3.BucketLifecycleConfigurationV2RuleFilterArgs(
                    prefix="config/",
                ),
                noncurrent_version_expiration=aws.s3.BucketLifecycleConfigurationV2RuleNoncurrentVersionExpirationArgs(
                    noncurrent_days=90,
                ),
                noncurrent_version_transitions=[
                    aws.s3.BucketLifecycleConfigurationV2RuleNoncurrentVersionTransitionArgs(
                        noncurrent_days=30,
                        storage_class="STANDARD_IA",
                    ),
                    aws.s3.BucketLifecycleConfigurationV2RuleNoncurrentVersionTransitionArgs(
                        noncurrent_days=60,
                        storage_class="GLACIER",
                    ),
                ],
                status="Enabled",
            )],
            opts=pulumi.ResourceOptions(depends_on=[versioning]))
        ```

        ## Import

        If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, import using the `bucket` and `expected_bucket_owner` separated by a comma (`,`):

        __Using `pulumi import` to import__ S3 bucket lifecycle configuration using the `bucket` or using the `bucket` and `expected_bucket_owner` separated by a comma (`,`). For example:

        If the owner (account ID) of the source bucket is the same account used to configure the AWS Provider, import using the `bucket`:

        ```sh
        $ pulumi import aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2 example bucket-name
        ```
        If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, import using the `bucket` and `expected_bucket_owner` separated by a comma (`,`):

        ```sh
        $ pulumi import aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2 example bucket-name,123456789012
        ```

        :param str resource_name: The name of the resource.
        :param BucketLifecycleConfigurationV2Args args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketLifecycleConfigurationV2Args, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketLifecycleConfigurationV2Args.__new__(BucketLifecycleConfigurationV2Args)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            __props__.__dict__["expected_bucket_owner"] = expected_bucket_owner
            if rules is None and not opts.urn:
                raise TypeError("Missing required property 'rules'")
            __props__.__dict__["rules"] = rules
        super(BucketLifecycleConfigurationV2, __self__).__init__(
            'aws:s3/bucketLifecycleConfigurationV2:BucketLifecycleConfigurationV2',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            expected_bucket_owner: Optional[pulumi.Input[str]] = None,
            rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]]] = None) -> 'BucketLifecycleConfigurationV2':
        """
        Get an existing BucketLifecycleConfigurationV2 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the source S3 bucket you want Amazon S3 to monitor.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BucketLifecycleConfigurationV2RuleArgs']]]] rules: List of configuration blocks describing the rules managing the replication. See below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BucketLifecycleConfigurationV2State.__new__(_BucketLifecycleConfigurationV2State)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["expected_bucket_owner"] = expected_bucket_owner
        __props__.__dict__["rules"] = rules
        return BucketLifecycleConfigurationV2(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        Name of the source S3 bucket you want Amazon S3 to monitor.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> pulumi.Output[Optional[str]]:
        """
        Account ID of the expected bucket owner. If the bucket is owned by a different account, the request will fail with an HTTP 403 (Access Denied) error.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output[Sequence['outputs.BucketLifecycleConfigurationV2Rule']]:
        """
        List of configuration blocks describing the rules managing the replication. See below.
        """
        return pulumi.get(self, "rules")

