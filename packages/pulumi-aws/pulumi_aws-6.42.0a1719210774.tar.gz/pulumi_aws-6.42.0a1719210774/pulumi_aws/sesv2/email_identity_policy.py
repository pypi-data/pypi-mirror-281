# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EmailIdentityPolicyArgs', 'EmailIdentityPolicy']

@pulumi.input_type
class EmailIdentityPolicyArgs:
    def __init__(__self__, *,
                 email_identity: pulumi.Input[str],
                 policy: pulumi.Input[str],
                 policy_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a EmailIdentityPolicy resource.
        :param pulumi.Input[str] email_identity: The email identity.
        :param pulumi.Input[str] policy: The text of the policy in JSON format.
        :param pulumi.Input[str] policy_name: The name of the policy.
        """
        pulumi.set(__self__, "email_identity", email_identity)
        pulumi.set(__self__, "policy", policy)
        pulumi.set(__self__, "policy_name", policy_name)

    @property
    @pulumi.getter(name="emailIdentity")
    def email_identity(self) -> pulumi.Input[str]:
        """
        The email identity.
        """
        return pulumi.get(self, "email_identity")

    @email_identity.setter
    def email_identity(self, value: pulumi.Input[str]):
        pulumi.set(self, "email_identity", value)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        The text of the policy in JSON format.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Input[str]:
        """
        The name of the policy.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_name", value)


@pulumi.input_type
class _EmailIdentityPolicyState:
    def __init__(__self__, *,
                 email_identity: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EmailIdentityPolicy resources.
        :param pulumi.Input[str] email_identity: The email identity.
        :param pulumi.Input[str] policy: The text of the policy in JSON format.
        :param pulumi.Input[str] policy_name: The name of the policy.
        """
        if email_identity is not None:
            pulumi.set(__self__, "email_identity", email_identity)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if policy_name is not None:
            pulumi.set(__self__, "policy_name", policy_name)

    @property
    @pulumi.getter(name="emailIdentity")
    def email_identity(self) -> Optional[pulumi.Input[str]]:
        """
        The email identity.
        """
        return pulumi.get(self, "email_identity")

    @email_identity.setter
    def email_identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_identity", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        The text of the policy in JSON format.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the policy.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_name", value)


class EmailIdentityPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 email_identity: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS SESv2 (Simple Email V2) Email Identity Policy.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sesv2.EmailIdentity("example", email_identity="testing@example.com")
        example_email_identity_policy = aws.sesv2.EmailIdentityPolicy("example",
            email_identity=example.email_identity,
            policy_name="example",
            policy=example.arn.apply(lambda arn: f\"\"\"{{
          "Id":"ExampleAuthorizationPolicy",
          "Version":"2012-10-17",
          "Statement":[
            {{
              "Sid":"AuthorizeIAMUser",
              "Effect":"Allow",
              "Resource":"{arn}",
              "Principal":{{
                "AWS":[
                  "arn:aws:iam::123456789012:user/John",
                  "arn:aws:iam::123456789012:user/Jane"
                ]
              }},
              "Action":[
                "ses:DeleteEmailIdentity",
                "ses:PutEmailIdentityDkimSigningAttributes"
              ]
            }}
          ]
        }}
        \"\"\"))
        ```

        ## Import

        Using `pulumi import`, import SESv2 (Simple Email V2) Email Identity Policy using the `example_id_arg`. For example:

        ```sh
        $ pulumi import aws:sesv2/emailIdentityPolicy:EmailIdentityPolicy example example_email_identity|example_policy_name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] email_identity: The email identity.
        :param pulumi.Input[str] policy: The text of the policy in JSON format.
        :param pulumi.Input[str] policy_name: The name of the policy.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EmailIdentityPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS SESv2 (Simple Email V2) Email Identity Policy.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sesv2.EmailIdentity("example", email_identity="testing@example.com")
        example_email_identity_policy = aws.sesv2.EmailIdentityPolicy("example",
            email_identity=example.email_identity,
            policy_name="example",
            policy=example.arn.apply(lambda arn: f\"\"\"{{
          "Id":"ExampleAuthorizationPolicy",
          "Version":"2012-10-17",
          "Statement":[
            {{
              "Sid":"AuthorizeIAMUser",
              "Effect":"Allow",
              "Resource":"{arn}",
              "Principal":{{
                "AWS":[
                  "arn:aws:iam::123456789012:user/John",
                  "arn:aws:iam::123456789012:user/Jane"
                ]
              }},
              "Action":[
                "ses:DeleteEmailIdentity",
                "ses:PutEmailIdentityDkimSigningAttributes"
              ]
            }}
          ]
        }}
        \"\"\"))
        ```

        ## Import

        Using `pulumi import`, import SESv2 (Simple Email V2) Email Identity Policy using the `example_id_arg`. For example:

        ```sh
        $ pulumi import aws:sesv2/emailIdentityPolicy:EmailIdentityPolicy example example_email_identity|example_policy_name
        ```

        :param str resource_name: The name of the resource.
        :param EmailIdentityPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EmailIdentityPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 email_identity: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EmailIdentityPolicyArgs.__new__(EmailIdentityPolicyArgs)

            if email_identity is None and not opts.urn:
                raise TypeError("Missing required property 'email_identity'")
            __props__.__dict__["email_identity"] = email_identity
            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
            if policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'policy_name'")
            __props__.__dict__["policy_name"] = policy_name
        super(EmailIdentityPolicy, __self__).__init__(
            'aws:sesv2/emailIdentityPolicy:EmailIdentityPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            email_identity: Optional[pulumi.Input[str]] = None,
            policy: Optional[pulumi.Input[str]] = None,
            policy_name: Optional[pulumi.Input[str]] = None) -> 'EmailIdentityPolicy':
        """
        Get an existing EmailIdentityPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] email_identity: The email identity.
        :param pulumi.Input[str] policy: The text of the policy in JSON format.
        :param pulumi.Input[str] policy_name: The name of the policy.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EmailIdentityPolicyState.__new__(_EmailIdentityPolicyState)

        __props__.__dict__["email_identity"] = email_identity
        __props__.__dict__["policy"] = policy
        __props__.__dict__["policy_name"] = policy_name
        return EmailIdentityPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="emailIdentity")
    def email_identity(self) -> pulumi.Output[str]:
        """
        The email identity.
        """
        return pulumi.get(self, "email_identity")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The text of the policy in JSON format.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Output[str]:
        """
        The name of the policy.
        """
        return pulumi.get(self, "policy_name")

