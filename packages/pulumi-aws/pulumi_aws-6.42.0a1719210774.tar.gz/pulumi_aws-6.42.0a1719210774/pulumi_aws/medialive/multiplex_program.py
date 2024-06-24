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

__all__ = ['MultiplexProgramArgs', 'MultiplexProgram']

@pulumi.input_type
class MultiplexProgramArgs:
    def __init__(__self__, *,
                 multiplex_id: pulumi.Input[str],
                 program_name: pulumi.Input[str],
                 multiplex_program_settings: Optional[pulumi.Input['MultiplexProgramMultiplexProgramSettingsArgs']] = None):
        """
        The set of arguments for constructing a MultiplexProgram resource.
        :param pulumi.Input[str] multiplex_id: Multiplex ID.
        :param pulumi.Input[str] program_name: Unique program name.
        :param pulumi.Input['MultiplexProgramMultiplexProgramSettingsArgs'] multiplex_program_settings: MultiplexProgram settings. See Multiplex Program Settings for more details.
               
               The following arguments are optional:
        """
        pulumi.set(__self__, "multiplex_id", multiplex_id)
        pulumi.set(__self__, "program_name", program_name)
        if multiplex_program_settings is not None:
            pulumi.set(__self__, "multiplex_program_settings", multiplex_program_settings)

    @property
    @pulumi.getter(name="multiplexId")
    def multiplex_id(self) -> pulumi.Input[str]:
        """
        Multiplex ID.
        """
        return pulumi.get(self, "multiplex_id")

    @multiplex_id.setter
    def multiplex_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "multiplex_id", value)

    @property
    @pulumi.getter(name="programName")
    def program_name(self) -> pulumi.Input[str]:
        """
        Unique program name.
        """
        return pulumi.get(self, "program_name")

    @program_name.setter
    def program_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "program_name", value)

    @property
    @pulumi.getter(name="multiplexProgramSettings")
    def multiplex_program_settings(self) -> Optional[pulumi.Input['MultiplexProgramMultiplexProgramSettingsArgs']]:
        """
        MultiplexProgram settings. See Multiplex Program Settings for more details.

        The following arguments are optional:
        """
        return pulumi.get(self, "multiplex_program_settings")

    @multiplex_program_settings.setter
    def multiplex_program_settings(self, value: Optional[pulumi.Input['MultiplexProgramMultiplexProgramSettingsArgs']]):
        pulumi.set(self, "multiplex_program_settings", value)


@pulumi.input_type
class _MultiplexProgramState:
    def __init__(__self__, *,
                 multiplex_id: Optional[pulumi.Input[str]] = None,
                 multiplex_program_settings: Optional[pulumi.Input['MultiplexProgramMultiplexProgramSettingsArgs']] = None,
                 program_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MultiplexProgram resources.
        :param pulumi.Input[str] multiplex_id: Multiplex ID.
        :param pulumi.Input['MultiplexProgramMultiplexProgramSettingsArgs'] multiplex_program_settings: MultiplexProgram settings. See Multiplex Program Settings for more details.
               
               The following arguments are optional:
        :param pulumi.Input[str] program_name: Unique program name.
        """
        if multiplex_id is not None:
            pulumi.set(__self__, "multiplex_id", multiplex_id)
        if multiplex_program_settings is not None:
            pulumi.set(__self__, "multiplex_program_settings", multiplex_program_settings)
        if program_name is not None:
            pulumi.set(__self__, "program_name", program_name)

    @property
    @pulumi.getter(name="multiplexId")
    def multiplex_id(self) -> Optional[pulumi.Input[str]]:
        """
        Multiplex ID.
        """
        return pulumi.get(self, "multiplex_id")

    @multiplex_id.setter
    def multiplex_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "multiplex_id", value)

    @property
    @pulumi.getter(name="multiplexProgramSettings")
    def multiplex_program_settings(self) -> Optional[pulumi.Input['MultiplexProgramMultiplexProgramSettingsArgs']]:
        """
        MultiplexProgram settings. See Multiplex Program Settings for more details.

        The following arguments are optional:
        """
        return pulumi.get(self, "multiplex_program_settings")

    @multiplex_program_settings.setter
    def multiplex_program_settings(self, value: Optional[pulumi.Input['MultiplexProgramMultiplexProgramSettingsArgs']]):
        pulumi.set(self, "multiplex_program_settings", value)

    @property
    @pulumi.getter(name="programName")
    def program_name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique program name.
        """
        return pulumi.get(self, "program_name")

    @program_name.setter
    def program_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "program_name", value)


class MultiplexProgram(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 multiplex_id: Optional[pulumi.Input[str]] = None,
                 multiplex_program_settings: Optional[pulumi.Input[pulumi.InputType['MultiplexProgramMultiplexProgramSettingsArgs']]] = None,
                 program_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS MediaLive MultiplexProgram.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        available = aws.get_availability_zones(state="available")
        example = aws.medialive.Multiplex("example",
            name="example-multiplex-changed",
            availability_zones=[
                available.names[0],
                available.names[1],
            ],
            multiplex_settings=aws.medialive.MultiplexMultiplexSettingsArgs(
                transport_stream_bitrate=1000000,
                transport_stream_id=1,
                transport_stream_reserved_bitrate=1,
                maximum_video_buffer_delay_milliseconds=1000,
            ),
            start_multiplex=True,
            tags={
                "tag1": "value1",
            })
        example_multiplex_program = aws.medialive.MultiplexProgram("example",
            program_name="example_program",
            multiplex_id=example.id,
            multiplex_program_settings=aws.medialive.MultiplexProgramMultiplexProgramSettingsArgs(
                program_number=1,
                preferred_channel_pipeline="CURRENTLY_ACTIVE",
                video_settings=aws.medialive.MultiplexProgramMultiplexProgramSettingsVideoSettingsArgs(
                    constant_bitrate=100000,
                ),
            ))
        ```

        ## Import

        Using `pulumi import`, import MediaLive MultiplexProgram using the `id`, or a combination of "`program_name`/`multiplex_id`". For example:

        ```sh
        $ pulumi import aws:medialive/multiplexProgram:MultiplexProgram example example_program/1234567
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] multiplex_id: Multiplex ID.
        :param pulumi.Input[pulumi.InputType['MultiplexProgramMultiplexProgramSettingsArgs']] multiplex_program_settings: MultiplexProgram settings. See Multiplex Program Settings for more details.
               
               The following arguments are optional:
        :param pulumi.Input[str] program_name: Unique program name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MultiplexProgramArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS MediaLive MultiplexProgram.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        available = aws.get_availability_zones(state="available")
        example = aws.medialive.Multiplex("example",
            name="example-multiplex-changed",
            availability_zones=[
                available.names[0],
                available.names[1],
            ],
            multiplex_settings=aws.medialive.MultiplexMultiplexSettingsArgs(
                transport_stream_bitrate=1000000,
                transport_stream_id=1,
                transport_stream_reserved_bitrate=1,
                maximum_video_buffer_delay_milliseconds=1000,
            ),
            start_multiplex=True,
            tags={
                "tag1": "value1",
            })
        example_multiplex_program = aws.medialive.MultiplexProgram("example",
            program_name="example_program",
            multiplex_id=example.id,
            multiplex_program_settings=aws.medialive.MultiplexProgramMultiplexProgramSettingsArgs(
                program_number=1,
                preferred_channel_pipeline="CURRENTLY_ACTIVE",
                video_settings=aws.medialive.MultiplexProgramMultiplexProgramSettingsVideoSettingsArgs(
                    constant_bitrate=100000,
                ),
            ))
        ```

        ## Import

        Using `pulumi import`, import MediaLive MultiplexProgram using the `id`, or a combination of "`program_name`/`multiplex_id`". For example:

        ```sh
        $ pulumi import aws:medialive/multiplexProgram:MultiplexProgram example example_program/1234567
        ```

        :param str resource_name: The name of the resource.
        :param MultiplexProgramArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MultiplexProgramArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 multiplex_id: Optional[pulumi.Input[str]] = None,
                 multiplex_program_settings: Optional[pulumi.Input[pulumi.InputType['MultiplexProgramMultiplexProgramSettingsArgs']]] = None,
                 program_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MultiplexProgramArgs.__new__(MultiplexProgramArgs)

            if multiplex_id is None and not opts.urn:
                raise TypeError("Missing required property 'multiplex_id'")
            __props__.__dict__["multiplex_id"] = multiplex_id
            __props__.__dict__["multiplex_program_settings"] = multiplex_program_settings
            if program_name is None and not opts.urn:
                raise TypeError("Missing required property 'program_name'")
            __props__.__dict__["program_name"] = program_name
        super(MultiplexProgram, __self__).__init__(
            'aws:medialive/multiplexProgram:MultiplexProgram',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            multiplex_id: Optional[pulumi.Input[str]] = None,
            multiplex_program_settings: Optional[pulumi.Input[pulumi.InputType['MultiplexProgramMultiplexProgramSettingsArgs']]] = None,
            program_name: Optional[pulumi.Input[str]] = None) -> 'MultiplexProgram':
        """
        Get an existing MultiplexProgram resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] multiplex_id: Multiplex ID.
        :param pulumi.Input[pulumi.InputType['MultiplexProgramMultiplexProgramSettingsArgs']] multiplex_program_settings: MultiplexProgram settings. See Multiplex Program Settings for more details.
               
               The following arguments are optional:
        :param pulumi.Input[str] program_name: Unique program name.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MultiplexProgramState.__new__(_MultiplexProgramState)

        __props__.__dict__["multiplex_id"] = multiplex_id
        __props__.__dict__["multiplex_program_settings"] = multiplex_program_settings
        __props__.__dict__["program_name"] = program_name
        return MultiplexProgram(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="multiplexId")
    def multiplex_id(self) -> pulumi.Output[str]:
        """
        Multiplex ID.
        """
        return pulumi.get(self, "multiplex_id")

    @property
    @pulumi.getter(name="multiplexProgramSettings")
    def multiplex_program_settings(self) -> pulumi.Output[Optional['outputs.MultiplexProgramMultiplexProgramSettings']]:
        """
        MultiplexProgram settings. See Multiplex Program Settings for more details.

        The following arguments are optional:
        """
        return pulumi.get(self, "multiplex_program_settings")

    @property
    @pulumi.getter(name="programName")
    def program_name(self) -> pulumi.Output[str]:
        """
        Unique program name.
        """
        return pulumi.get(self, "program_name")

