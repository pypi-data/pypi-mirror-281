# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TrustStoreRevocationArgs', 'TrustStoreRevocation']

@pulumi.input_type
class TrustStoreRevocationArgs:
    def __init__(__self__, *,
                 revocations_s3_bucket: pulumi.Input[str],
                 revocations_s3_key: pulumi.Input[str],
                 trust_store_arn: pulumi.Input[str],
                 revocations_s3_object_version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TrustStoreRevocation resource.
        :param pulumi.Input[str] revocations_s3_bucket: S3 Bucket name holding the client certificate CA bundle.
        :param pulumi.Input[str] revocations_s3_key: S3 object key holding the client certificate CA bundle.
        :param pulumi.Input[str] trust_store_arn: Trust Store ARN.
        :param pulumi.Input[str] revocations_s3_object_version: Version Id of CA bundle S3 bucket object, if versioned, defaults to latest if omitted.
        """
        pulumi.set(__self__, "revocations_s3_bucket", revocations_s3_bucket)
        pulumi.set(__self__, "revocations_s3_key", revocations_s3_key)
        pulumi.set(__self__, "trust_store_arn", trust_store_arn)
        if revocations_s3_object_version is not None:
            pulumi.set(__self__, "revocations_s3_object_version", revocations_s3_object_version)

    @property
    @pulumi.getter(name="revocationsS3Bucket")
    def revocations_s3_bucket(self) -> pulumi.Input[str]:
        """
        S3 Bucket name holding the client certificate CA bundle.
        """
        return pulumi.get(self, "revocations_s3_bucket")

    @revocations_s3_bucket.setter
    def revocations_s3_bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "revocations_s3_bucket", value)

    @property
    @pulumi.getter(name="revocationsS3Key")
    def revocations_s3_key(self) -> pulumi.Input[str]:
        """
        S3 object key holding the client certificate CA bundle.
        """
        return pulumi.get(self, "revocations_s3_key")

    @revocations_s3_key.setter
    def revocations_s3_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "revocations_s3_key", value)

    @property
    @pulumi.getter(name="trustStoreArn")
    def trust_store_arn(self) -> pulumi.Input[str]:
        """
        Trust Store ARN.
        """
        return pulumi.get(self, "trust_store_arn")

    @trust_store_arn.setter
    def trust_store_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "trust_store_arn", value)

    @property
    @pulumi.getter(name="revocationsS3ObjectVersion")
    def revocations_s3_object_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version Id of CA bundle S3 bucket object, if versioned, defaults to latest if omitted.
        """
        return pulumi.get(self, "revocations_s3_object_version")

    @revocations_s3_object_version.setter
    def revocations_s3_object_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "revocations_s3_object_version", value)


@pulumi.input_type
class _TrustStoreRevocationState:
    def __init__(__self__, *,
                 revocation_id: Optional[pulumi.Input[int]] = None,
                 revocations_s3_bucket: Optional[pulumi.Input[str]] = None,
                 revocations_s3_key: Optional[pulumi.Input[str]] = None,
                 revocations_s3_object_version: Optional[pulumi.Input[str]] = None,
                 trust_store_arn: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TrustStoreRevocation resources.
        :param pulumi.Input[int] revocation_id: AWS assigned RevocationId, (number).
        :param pulumi.Input[str] revocations_s3_bucket: S3 Bucket name holding the client certificate CA bundle.
        :param pulumi.Input[str] revocations_s3_key: S3 object key holding the client certificate CA bundle.
        :param pulumi.Input[str] revocations_s3_object_version: Version Id of CA bundle S3 bucket object, if versioned, defaults to latest if omitted.
        :param pulumi.Input[str] trust_store_arn: Trust Store ARN.
        """
        if revocation_id is not None:
            pulumi.set(__self__, "revocation_id", revocation_id)
        if revocations_s3_bucket is not None:
            pulumi.set(__self__, "revocations_s3_bucket", revocations_s3_bucket)
        if revocations_s3_key is not None:
            pulumi.set(__self__, "revocations_s3_key", revocations_s3_key)
        if revocations_s3_object_version is not None:
            pulumi.set(__self__, "revocations_s3_object_version", revocations_s3_object_version)
        if trust_store_arn is not None:
            pulumi.set(__self__, "trust_store_arn", trust_store_arn)

    @property
    @pulumi.getter(name="revocationId")
    def revocation_id(self) -> Optional[pulumi.Input[int]]:
        """
        AWS assigned RevocationId, (number).
        """
        return pulumi.get(self, "revocation_id")

    @revocation_id.setter
    def revocation_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "revocation_id", value)

    @property
    @pulumi.getter(name="revocationsS3Bucket")
    def revocations_s3_bucket(self) -> Optional[pulumi.Input[str]]:
        """
        S3 Bucket name holding the client certificate CA bundle.
        """
        return pulumi.get(self, "revocations_s3_bucket")

    @revocations_s3_bucket.setter
    def revocations_s3_bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "revocations_s3_bucket", value)

    @property
    @pulumi.getter(name="revocationsS3Key")
    def revocations_s3_key(self) -> Optional[pulumi.Input[str]]:
        """
        S3 object key holding the client certificate CA bundle.
        """
        return pulumi.get(self, "revocations_s3_key")

    @revocations_s3_key.setter
    def revocations_s3_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "revocations_s3_key", value)

    @property
    @pulumi.getter(name="revocationsS3ObjectVersion")
    def revocations_s3_object_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version Id of CA bundle S3 bucket object, if versioned, defaults to latest if omitted.
        """
        return pulumi.get(self, "revocations_s3_object_version")

    @revocations_s3_object_version.setter
    def revocations_s3_object_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "revocations_s3_object_version", value)

    @property
    @pulumi.getter(name="trustStoreArn")
    def trust_store_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Trust Store ARN.
        """
        return pulumi.get(self, "trust_store_arn")

    @trust_store_arn.setter
    def trust_store_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trust_store_arn", value)


class TrustStoreRevocation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 revocations_s3_bucket: Optional[pulumi.Input[str]] = None,
                 revocations_s3_key: Optional[pulumi.Input[str]] = None,
                 revocations_s3_object_version: Optional[pulumi.Input[str]] = None,
                 trust_store_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a ELBv2 Trust Store Revocation for use with Application Load Balancer Listener resources.

        ## Example Usage

        ### Trust Store With Revocations

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.lb.TrustStore("test",
            name="tf-example-lb-ts",
            ca_certificates_bundle_s3_bucket="...",
            ca_certificates_bundle_s3_key="...")
        test_trust_store_revocation = aws.lb.TrustStoreRevocation("test",
            trust_store_arn=test.arn,
            revocations_s3_bucket="...",
            revocations_s3_key="...")
        ```

        ## Import

        Using `pulumi import`, import Trust Store Revocations using their ARN. For example:

        ```sh
        $ pulumi import aws:lb/trustStoreRevocation:TrustStoreRevocation example arn:aws:elasticloadbalancing:us-west-2:187416307283:truststore/my-trust-store/20cfe21448b66314,6
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] revocations_s3_bucket: S3 Bucket name holding the client certificate CA bundle.
        :param pulumi.Input[str] revocations_s3_key: S3 object key holding the client certificate CA bundle.
        :param pulumi.Input[str] revocations_s3_object_version: Version Id of CA bundle S3 bucket object, if versioned, defaults to latest if omitted.
        :param pulumi.Input[str] trust_store_arn: Trust Store ARN.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TrustStoreRevocationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a ELBv2 Trust Store Revocation for use with Application Load Balancer Listener resources.

        ## Example Usage

        ### Trust Store With Revocations

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.lb.TrustStore("test",
            name="tf-example-lb-ts",
            ca_certificates_bundle_s3_bucket="...",
            ca_certificates_bundle_s3_key="...")
        test_trust_store_revocation = aws.lb.TrustStoreRevocation("test",
            trust_store_arn=test.arn,
            revocations_s3_bucket="...",
            revocations_s3_key="...")
        ```

        ## Import

        Using `pulumi import`, import Trust Store Revocations using their ARN. For example:

        ```sh
        $ pulumi import aws:lb/trustStoreRevocation:TrustStoreRevocation example arn:aws:elasticloadbalancing:us-west-2:187416307283:truststore/my-trust-store/20cfe21448b66314,6
        ```

        :param str resource_name: The name of the resource.
        :param TrustStoreRevocationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TrustStoreRevocationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 revocations_s3_bucket: Optional[pulumi.Input[str]] = None,
                 revocations_s3_key: Optional[pulumi.Input[str]] = None,
                 revocations_s3_object_version: Optional[pulumi.Input[str]] = None,
                 trust_store_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TrustStoreRevocationArgs.__new__(TrustStoreRevocationArgs)

            if revocations_s3_bucket is None and not opts.urn:
                raise TypeError("Missing required property 'revocations_s3_bucket'")
            __props__.__dict__["revocations_s3_bucket"] = revocations_s3_bucket
            if revocations_s3_key is None and not opts.urn:
                raise TypeError("Missing required property 'revocations_s3_key'")
            __props__.__dict__["revocations_s3_key"] = revocations_s3_key
            __props__.__dict__["revocations_s3_object_version"] = revocations_s3_object_version
            if trust_store_arn is None and not opts.urn:
                raise TypeError("Missing required property 'trust_store_arn'")
            __props__.__dict__["trust_store_arn"] = trust_store_arn
            __props__.__dict__["revocation_id"] = None
        super(TrustStoreRevocation, __self__).__init__(
            'aws:lb/trustStoreRevocation:TrustStoreRevocation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            revocation_id: Optional[pulumi.Input[int]] = None,
            revocations_s3_bucket: Optional[pulumi.Input[str]] = None,
            revocations_s3_key: Optional[pulumi.Input[str]] = None,
            revocations_s3_object_version: Optional[pulumi.Input[str]] = None,
            trust_store_arn: Optional[pulumi.Input[str]] = None) -> 'TrustStoreRevocation':
        """
        Get an existing TrustStoreRevocation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] revocation_id: AWS assigned RevocationId, (number).
        :param pulumi.Input[str] revocations_s3_bucket: S3 Bucket name holding the client certificate CA bundle.
        :param pulumi.Input[str] revocations_s3_key: S3 object key holding the client certificate CA bundle.
        :param pulumi.Input[str] revocations_s3_object_version: Version Id of CA bundle S3 bucket object, if versioned, defaults to latest if omitted.
        :param pulumi.Input[str] trust_store_arn: Trust Store ARN.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TrustStoreRevocationState.__new__(_TrustStoreRevocationState)

        __props__.__dict__["revocation_id"] = revocation_id
        __props__.__dict__["revocations_s3_bucket"] = revocations_s3_bucket
        __props__.__dict__["revocations_s3_key"] = revocations_s3_key
        __props__.__dict__["revocations_s3_object_version"] = revocations_s3_object_version
        __props__.__dict__["trust_store_arn"] = trust_store_arn
        return TrustStoreRevocation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="revocationId")
    def revocation_id(self) -> pulumi.Output[int]:
        """
        AWS assigned RevocationId, (number).
        """
        return pulumi.get(self, "revocation_id")

    @property
    @pulumi.getter(name="revocationsS3Bucket")
    def revocations_s3_bucket(self) -> pulumi.Output[str]:
        """
        S3 Bucket name holding the client certificate CA bundle.
        """
        return pulumi.get(self, "revocations_s3_bucket")

    @property
    @pulumi.getter(name="revocationsS3Key")
    def revocations_s3_key(self) -> pulumi.Output[str]:
        """
        S3 object key holding the client certificate CA bundle.
        """
        return pulumi.get(self, "revocations_s3_key")

    @property
    @pulumi.getter(name="revocationsS3ObjectVersion")
    def revocations_s3_object_version(self) -> pulumi.Output[Optional[str]]:
        """
        Version Id of CA bundle S3 bucket object, if versioned, defaults to latest if omitted.
        """
        return pulumi.get(self, "revocations_s3_object_version")

    @property
    @pulumi.getter(name="trustStoreArn")
    def trust_store_arn(self) -> pulumi.Output[str]:
        """
        Trust Store ARN.
        """
        return pulumi.get(self, "trust_store_arn")

