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
    'KeyKeyAttributes',
    'KeyKeyAttributesKeyModesOfUse',
    'KeyTimeouts',
]

@pulumi.output_type
class KeyKeyAttributes(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyAlgorithm":
            suggest = "key_algorithm"
        elif key == "keyClass":
            suggest = "key_class"
        elif key == "keyUsage":
            suggest = "key_usage"
        elif key == "keyModesOfUse":
            suggest = "key_modes_of_use"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeyKeyAttributes. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeyKeyAttributes.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeyKeyAttributes.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_algorithm: str,
                 key_class: str,
                 key_usage: str,
                 key_modes_of_use: Optional['outputs.KeyKeyAttributesKeyModesOfUse'] = None):
        """
        :param str key_algorithm: Key algorithm to be use during creation of an AWS Payment Cryptography key.
        :param str key_class: Type of AWS Payment Cryptography key to create.
        :param str key_usage: Cryptographic usage of an AWS Payment Cryptography key as defined in section A.5.2 of the TR-31 spec.
        :param 'KeyKeyAttributesKeyModesOfUseArgs' key_modes_of_use: List of cryptographic operations that you can perform using the key.
        """
        pulumi.set(__self__, "key_algorithm", key_algorithm)
        pulumi.set(__self__, "key_class", key_class)
        pulumi.set(__self__, "key_usage", key_usage)
        if key_modes_of_use is not None:
            pulumi.set(__self__, "key_modes_of_use", key_modes_of_use)

    @property
    @pulumi.getter(name="keyAlgorithm")
    def key_algorithm(self) -> str:
        """
        Key algorithm to be use during creation of an AWS Payment Cryptography key.
        """
        return pulumi.get(self, "key_algorithm")

    @property
    @pulumi.getter(name="keyClass")
    def key_class(self) -> str:
        """
        Type of AWS Payment Cryptography key to create.
        """
        return pulumi.get(self, "key_class")

    @property
    @pulumi.getter(name="keyUsage")
    def key_usage(self) -> str:
        """
        Cryptographic usage of an AWS Payment Cryptography key as defined in section A.5.2 of the TR-31 spec.
        """
        return pulumi.get(self, "key_usage")

    @property
    @pulumi.getter(name="keyModesOfUse")
    def key_modes_of_use(self) -> Optional['outputs.KeyKeyAttributesKeyModesOfUse']:
        """
        List of cryptographic operations that you can perform using the key.
        """
        return pulumi.get(self, "key_modes_of_use")


@pulumi.output_type
class KeyKeyAttributesKeyModesOfUse(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "deriveKey":
            suggest = "derive_key"
        elif key == "noRestrictions":
            suggest = "no_restrictions"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeyKeyAttributesKeyModesOfUse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeyKeyAttributesKeyModesOfUse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeyKeyAttributesKeyModesOfUse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 decrypt: Optional[bool] = None,
                 derive_key: Optional[bool] = None,
                 encrypt: Optional[bool] = None,
                 generate: Optional[bool] = None,
                 no_restrictions: Optional[bool] = None,
                 sign: Optional[bool] = None,
                 unwrap: Optional[bool] = None,
                 verify: Optional[bool] = None,
                 wrap: Optional[bool] = None):
        """
        :param bool decrypt: Whether an AWS Payment Cryptography key can be used to decrypt data.
        :param bool derive_key: Whether an AWS Payment Cryptography key can be used to derive new keys.
        :param bool encrypt: Whether an AWS Payment Cryptography key can be used to encrypt data.
        :param bool generate: Whether an AWS Payment Cryptography key can be used to generate and verify other card and PIN verification keys.
        :param bool no_restrictions: Whether an AWS Payment Cryptography key has no special restrictions other than the restrictions implied by KeyUsage.
        :param bool sign: Whether an AWS Payment Cryptography key can be used for signing.
        :param bool unwrap: Whether an AWS Payment Cryptography key can be used to unwrap other keys.
        :param bool verify: Whether an AWS Payment Cryptography key can be used to verify signatures.
        :param bool wrap: Whether an AWS Payment Cryptography key can be used to wrap other keys.
        """
        if decrypt is not None:
            pulumi.set(__self__, "decrypt", decrypt)
        if derive_key is not None:
            pulumi.set(__self__, "derive_key", derive_key)
        if encrypt is not None:
            pulumi.set(__self__, "encrypt", encrypt)
        if generate is not None:
            pulumi.set(__self__, "generate", generate)
        if no_restrictions is not None:
            pulumi.set(__self__, "no_restrictions", no_restrictions)
        if sign is not None:
            pulumi.set(__self__, "sign", sign)
        if unwrap is not None:
            pulumi.set(__self__, "unwrap", unwrap)
        if verify is not None:
            pulumi.set(__self__, "verify", verify)
        if wrap is not None:
            pulumi.set(__self__, "wrap", wrap)

    @property
    @pulumi.getter
    def decrypt(self) -> Optional[bool]:
        """
        Whether an AWS Payment Cryptography key can be used to decrypt data.
        """
        return pulumi.get(self, "decrypt")

    @property
    @pulumi.getter(name="deriveKey")
    def derive_key(self) -> Optional[bool]:
        """
        Whether an AWS Payment Cryptography key can be used to derive new keys.
        """
        return pulumi.get(self, "derive_key")

    @property
    @pulumi.getter
    def encrypt(self) -> Optional[bool]:
        """
        Whether an AWS Payment Cryptography key can be used to encrypt data.
        """
        return pulumi.get(self, "encrypt")

    @property
    @pulumi.getter
    def generate(self) -> Optional[bool]:
        """
        Whether an AWS Payment Cryptography key can be used to generate and verify other card and PIN verification keys.
        """
        return pulumi.get(self, "generate")

    @property
    @pulumi.getter(name="noRestrictions")
    def no_restrictions(self) -> Optional[bool]:
        """
        Whether an AWS Payment Cryptography key has no special restrictions other than the restrictions implied by KeyUsage.
        """
        return pulumi.get(self, "no_restrictions")

    @property
    @pulumi.getter
    def sign(self) -> Optional[bool]:
        """
        Whether an AWS Payment Cryptography key can be used for signing.
        """
        return pulumi.get(self, "sign")

    @property
    @pulumi.getter
    def unwrap(self) -> Optional[bool]:
        """
        Whether an AWS Payment Cryptography key can be used to unwrap other keys.
        """
        return pulumi.get(self, "unwrap")

    @property
    @pulumi.getter
    def verify(self) -> Optional[bool]:
        """
        Whether an AWS Payment Cryptography key can be used to verify signatures.
        """
        return pulumi.get(self, "verify")

    @property
    @pulumi.getter
    def wrap(self) -> Optional[bool]:
        """
        Whether an AWS Payment Cryptography key can be used to wrap other keys.
        """
        return pulumi.get(self, "wrap")


@pulumi.output_type
class KeyTimeouts(dict):
    def __init__(__self__, *,
                 create: Optional[str] = None,
                 delete: Optional[str] = None,
                 update: Optional[str] = None):
        """
        :param str create: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        :param str delete: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.
        :param str update: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        if create is not None:
            pulumi.set(__self__, "create", create)
        if delete is not None:
            pulumi.set(__self__, "delete", delete)
        if update is not None:
            pulumi.set(__self__, "update", update)

    @property
    @pulumi.getter
    def create(self) -> Optional[str]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        return pulumi.get(self, "create")

    @property
    @pulumi.getter
    def delete(self) -> Optional[str]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.
        """
        return pulumi.get(self, "delete")

    @property
    @pulumi.getter
    def update(self) -> Optional[str]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        return pulumi.get(self, "update")


