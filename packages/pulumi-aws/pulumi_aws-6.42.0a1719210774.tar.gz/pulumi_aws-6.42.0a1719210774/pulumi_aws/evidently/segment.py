# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SegmentArgs', 'Segment']

@pulumi.input_type
class SegmentArgs:
    def __init__(__self__, *,
                 pattern: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Segment resource.
        :param pulumi.Input[str] pattern: The pattern to use for the segment. For more information about pattern syntax, see [Segment rule pattern syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax.html).
        :param pulumi.Input[str] description: Specifies the description of the segment.
        :param pulumi.Input[str] name: A name for the segment.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the segment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "pattern", pattern)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def pattern(self) -> pulumi.Input[str]:
        """
        The pattern to use for the segment. For more information about pattern syntax, see [Segment rule pattern syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax.html).
        """
        return pulumi.get(self, "pattern")

    @pattern.setter
    def pattern(self, value: pulumi.Input[str]):
        pulumi.set(self, "pattern", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the description of the segment.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the segment.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags to apply to the segment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _SegmentState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 created_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 experiment_count: Optional[pulumi.Input[int]] = None,
                 last_updated_time: Optional[pulumi.Input[str]] = None,
                 launch_count: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pattern: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Segment resources.
        :param pulumi.Input[str] arn: The ARN of the segment.
        :param pulumi.Input[str] created_time: The date and time that the segment is created.
        :param pulumi.Input[str] description: Specifies the description of the segment.
        :param pulumi.Input[int] experiment_count: The number of experiments that this segment is used in. This count includes all current experiments, not just those that are currently running.
        :param pulumi.Input[str] last_updated_time: The date and time that this segment was most recently updated.
        :param pulumi.Input[int] launch_count: The number of launches that this segment is used in. This count includes all current launches, not just those that are currently running.
        :param pulumi.Input[str] name: A name for the segment.
        :param pulumi.Input[str] pattern: The pattern to use for the segment. For more information about pattern syntax, see [Segment rule pattern syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax.html).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the segment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if created_time is not None:
            pulumi.set(__self__, "created_time", created_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if experiment_count is not None:
            pulumi.set(__self__, "experiment_count", experiment_count)
        if last_updated_time is not None:
            pulumi.set(__self__, "last_updated_time", last_updated_time)
        if launch_count is not None:
            pulumi.set(__self__, "launch_count", launch_count)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if pattern is not None:
            pulumi.set(__self__, "pattern", pattern)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the segment.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time that the segment is created.
        """
        return pulumi.get(self, "created_time")

    @created_time.setter
    def created_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the description of the segment.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="experimentCount")
    def experiment_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of experiments that this segment is used in. This count includes all current experiments, not just those that are currently running.
        """
        return pulumi.get(self, "experiment_count")

    @experiment_count.setter
    def experiment_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "experiment_count", value)

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time that this segment was most recently updated.
        """
        return pulumi.get(self, "last_updated_time")

    @last_updated_time.setter
    def last_updated_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_updated_time", value)

    @property
    @pulumi.getter(name="launchCount")
    def launch_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of launches that this segment is used in. This count includes all current launches, not just those that are currently running.
        """
        return pulumi.get(self, "launch_count")

    @launch_count.setter
    def launch_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "launch_count", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the segment.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def pattern(self) -> Optional[pulumi.Input[str]]:
        """
        The pattern to use for the segment. For more information about pattern syntax, see [Segment rule pattern syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax.html).
        """
        return pulumi.get(self, "pattern")

    @pattern.setter
    def pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pattern", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags to apply to the segment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class Segment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pattern: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a CloudWatch Evidently Segment resource.

        ## Example Usage

        ### Basic

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.evidently.Segment("example",
            name="example",
            pattern="{\\"Price\\":[{\\"numeric\\":[\\">\\",10,\\"<=\\",20]}]}",
            tags={
                "Key1": "example Segment",
            })
        ```

        ### With JSON object in pattern

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.evidently.Segment("example",
            name="example",
            pattern=\"\"\"  {
            "Price": [
              {
                "numeric": [">",10,"<=",20]
              }
            ]
          }
        \"\"\",
            tags={
                "Key1": "example Segment",
            })
        ```

        ### With Description

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.evidently.Segment("example",
            name="example",
            pattern="{\\"Price\\":[{\\"numeric\\":[\\">\\",10,\\"<=\\",20]}]}",
            description="example")
        ```

        ## Import

        Using `pulumi import`, import CloudWatch Evidently Segment using the `arn`. For example:

        ```sh
        $ pulumi import aws:evidently/segment:Segment example arn:aws:evidently:us-west-2:123456789012:segment/example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Specifies the description of the segment.
        :param pulumi.Input[str] name: A name for the segment.
        :param pulumi.Input[str] pattern: The pattern to use for the segment. For more information about pattern syntax, see [Segment rule pattern syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax.html).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the segment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SegmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CloudWatch Evidently Segment resource.

        ## Example Usage

        ### Basic

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.evidently.Segment("example",
            name="example",
            pattern="{\\"Price\\":[{\\"numeric\\":[\\">\\",10,\\"<=\\",20]}]}",
            tags={
                "Key1": "example Segment",
            })
        ```

        ### With JSON object in pattern

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.evidently.Segment("example",
            name="example",
            pattern=\"\"\"  {
            "Price": [
              {
                "numeric": [">",10,"<=",20]
              }
            ]
          }
        \"\"\",
            tags={
                "Key1": "example Segment",
            })
        ```

        ### With Description

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.evidently.Segment("example",
            name="example",
            pattern="{\\"Price\\":[{\\"numeric\\":[\\">\\",10,\\"<=\\",20]}]}",
            description="example")
        ```

        ## Import

        Using `pulumi import`, import CloudWatch Evidently Segment using the `arn`. For example:

        ```sh
        $ pulumi import aws:evidently/segment:Segment example arn:aws:evidently:us-west-2:123456789012:segment/example
        ```

        :param str resource_name: The name of the resource.
        :param SegmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SegmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pattern: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SegmentArgs.__new__(SegmentArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            if pattern is None and not opts.urn:
                raise TypeError("Missing required property 'pattern'")
            __props__.__dict__["pattern"] = pattern
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["created_time"] = None
            __props__.__dict__["experiment_count"] = None
            __props__.__dict__["last_updated_time"] = None
            __props__.__dict__["launch_count"] = None
            __props__.__dict__["tags_all"] = None
        super(Segment, __self__).__init__(
            'aws:evidently/segment:Segment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            created_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            experiment_count: Optional[pulumi.Input[int]] = None,
            last_updated_time: Optional[pulumi.Input[str]] = None,
            launch_count: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            pattern: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Segment':
        """
        Get an existing Segment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the segment.
        :param pulumi.Input[str] created_time: The date and time that the segment is created.
        :param pulumi.Input[str] description: Specifies the description of the segment.
        :param pulumi.Input[int] experiment_count: The number of experiments that this segment is used in. This count includes all current experiments, not just those that are currently running.
        :param pulumi.Input[str] last_updated_time: The date and time that this segment was most recently updated.
        :param pulumi.Input[int] launch_count: The number of launches that this segment is used in. This count includes all current launches, not just those that are currently running.
        :param pulumi.Input[str] name: A name for the segment.
        :param pulumi.Input[str] pattern: The pattern to use for the segment. For more information about pattern syntax, see [Segment rule pattern syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax.html).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the segment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SegmentState.__new__(_SegmentState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["created_time"] = created_time
        __props__.__dict__["description"] = description
        __props__.__dict__["experiment_count"] = experiment_count
        __props__.__dict__["last_updated_time"] = last_updated_time
        __props__.__dict__["launch_count"] = launch_count
        __props__.__dict__["name"] = name
        __props__.__dict__["pattern"] = pattern
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return Segment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the segment.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> pulumi.Output[str]:
        """
        The date and time that the segment is created.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the description of the segment.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="experimentCount")
    def experiment_count(self) -> pulumi.Output[int]:
        """
        The number of experiments that this segment is used in. This count includes all current experiments, not just those that are currently running.
        """
        return pulumi.get(self, "experiment_count")

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> pulumi.Output[str]:
        """
        The date and time that this segment was most recently updated.
        """
        return pulumi.get(self, "last_updated_time")

    @property
    @pulumi.getter(name="launchCount")
    def launch_count(self) -> pulumi.Output[int]:
        """
        The number of launches that this segment is used in. This count includes all current launches, not just those that are currently running.
        """
        return pulumi.get(self, "launch_count")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A name for the segment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def pattern(self) -> pulumi.Output[str]:
        """
        The pattern to use for the segment. For more information about pattern syntax, see [Segment rule pattern syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Evidently-segments.html#CloudWatch-Evidently-segments-syntax.html).
        """
        return pulumi.get(self, "pattern")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags to apply to the segment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

