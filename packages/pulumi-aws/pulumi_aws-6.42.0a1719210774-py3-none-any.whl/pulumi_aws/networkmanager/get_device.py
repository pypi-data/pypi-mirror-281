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
    'GetDeviceResult',
    'AwaitableGetDeviceResult',
    'get_device',
    'get_device_output',
]

@pulumi.output_type
class GetDeviceResult:
    """
    A collection of values returned by getDevice.
    """
    def __init__(__self__, arn=None, aws_locations=None, description=None, device_id=None, global_network_id=None, id=None, locations=None, model=None, serial_number=None, site_id=None, tags=None, type=None, vendor=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if aws_locations and not isinstance(aws_locations, list):
            raise TypeError("Expected argument 'aws_locations' to be a list")
        pulumi.set(__self__, "aws_locations", aws_locations)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if device_id and not isinstance(device_id, str):
            raise TypeError("Expected argument 'device_id' to be a str")
        pulumi.set(__self__, "device_id", device_id)
        if global_network_id and not isinstance(global_network_id, str):
            raise TypeError("Expected argument 'global_network_id' to be a str")
        pulumi.set(__self__, "global_network_id", global_network_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if locations and not isinstance(locations, list):
            raise TypeError("Expected argument 'locations' to be a list")
        pulumi.set(__self__, "locations", locations)
        if model and not isinstance(model, str):
            raise TypeError("Expected argument 'model' to be a str")
        pulumi.set(__self__, "model", model)
        if serial_number and not isinstance(serial_number, str):
            raise TypeError("Expected argument 'serial_number' to be a str")
        pulumi.set(__self__, "serial_number", serial_number)
        if site_id and not isinstance(site_id, str):
            raise TypeError("Expected argument 'site_id' to be a str")
        pulumi.set(__self__, "site_id", site_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vendor and not isinstance(vendor, str):
            raise TypeError("Expected argument 'vendor' to be a str")
        pulumi.set(__self__, "vendor", vendor)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the device.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsLocations")
    def aws_locations(self) -> Sequence['outputs.GetDeviceAwsLocationResult']:
        """
        AWS location of the device. Documented below.
        """
        return pulumi.get(self, "aws_locations")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the device.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="deviceId")
    def device_id(self) -> str:
        return pulumi.get(self, "device_id")

    @property
    @pulumi.getter(name="globalNetworkId")
    def global_network_id(self) -> str:
        return pulumi.get(self, "global_network_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def locations(self) -> Sequence['outputs.GetDeviceLocationResult']:
        """
        Location of the device. Documented below.
        """
        return pulumi.get(self, "locations")

    @property
    @pulumi.getter
    def model(self) -> str:
        """
        Model of device.
        """
        return pulumi.get(self, "model")

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> str:
        """
        Serial number of the device.
        """
        return pulumi.get(self, "serial_number")

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> str:
        """
        ID of the site.
        """
        return pulumi.get(self, "site_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Key-value tags for the device.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of device.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def vendor(self) -> str:
        """
        Vendor of the device.
        """
        return pulumi.get(self, "vendor")


class AwaitableGetDeviceResult(GetDeviceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDeviceResult(
            arn=self.arn,
            aws_locations=self.aws_locations,
            description=self.description,
            device_id=self.device_id,
            global_network_id=self.global_network_id,
            id=self.id,
            locations=self.locations,
            model=self.model,
            serial_number=self.serial_number,
            site_id=self.site_id,
            tags=self.tags,
            type=self.type,
            vendor=self.vendor)


def get_device(device_id: Optional[str] = None,
               global_network_id: Optional[str] = None,
               tags: Optional[Mapping[str, str]] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDeviceResult:
    """
    Retrieve information about a device.


    :param str device_id: ID of the device.
    :param str global_network_id: ID of the global network.
    :param Mapping[str, str] tags: Key-value tags for the device.
    """
    __args__ = dict()
    __args__['deviceId'] = device_id
    __args__['globalNetworkId'] = global_network_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:networkmanager/getDevice:getDevice', __args__, opts=opts, typ=GetDeviceResult).value

    return AwaitableGetDeviceResult(
        arn=pulumi.get(__ret__, 'arn'),
        aws_locations=pulumi.get(__ret__, 'aws_locations'),
        description=pulumi.get(__ret__, 'description'),
        device_id=pulumi.get(__ret__, 'device_id'),
        global_network_id=pulumi.get(__ret__, 'global_network_id'),
        id=pulumi.get(__ret__, 'id'),
        locations=pulumi.get(__ret__, 'locations'),
        model=pulumi.get(__ret__, 'model'),
        serial_number=pulumi.get(__ret__, 'serial_number'),
        site_id=pulumi.get(__ret__, 'site_id'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'),
        vendor=pulumi.get(__ret__, 'vendor'))


@_utilities.lift_output_func(get_device)
def get_device_output(device_id: Optional[pulumi.Input[str]] = None,
                      global_network_id: Optional[pulumi.Input[str]] = None,
                      tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDeviceResult]:
    """
    Retrieve information about a device.


    :param str device_id: ID of the device.
    :param str global_network_id: ID of the global network.
    :param Mapping[str, str] tags: Key-value tags for the device.
    """
    ...
