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
    'PolicyDefinition',
    'PolicyDefinitionStatic',
    'PolicyDefinitionTemplateLinked',
    'PolicyDefinitionTemplateLinkedPrincipal',
    'PolicyDefinitionTemplateLinkedResource',
    'PolicyStoreValidationSettings',
    'SchemaDefinition',
    'GetPolicyStoreValidationSettingResult',
]

@pulumi.output_type
class PolicyDefinition(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "templateLinked":
            suggest = "template_linked"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyDefinition. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyDefinition.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyDefinition.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 static: Optional['outputs.PolicyDefinitionStatic'] = None,
                 template_linked: Optional['outputs.PolicyDefinitionTemplateLinked'] = None):
        """
        :param 'PolicyDefinitionStaticArgs' static: The static policy statement. See Static below.
        :param 'PolicyDefinitionTemplateLinkedArgs' template_linked: The template linked policy. See Template Linked below.
        """
        if static is not None:
            pulumi.set(__self__, "static", static)
        if template_linked is not None:
            pulumi.set(__self__, "template_linked", template_linked)

    @property
    @pulumi.getter
    def static(self) -> Optional['outputs.PolicyDefinitionStatic']:
        """
        The static policy statement. See Static below.
        """
        return pulumi.get(self, "static")

    @property
    @pulumi.getter(name="templateLinked")
    def template_linked(self) -> Optional['outputs.PolicyDefinitionTemplateLinked']:
        """
        The template linked policy. See Template Linked below.
        """
        return pulumi.get(self, "template_linked")


@pulumi.output_type
class PolicyDefinitionStatic(dict):
    def __init__(__self__, *,
                 statement: str,
                 description: Optional[str] = None):
        """
        :param str statement: The statement of the static policy.
        :param str description: The description of the static policy.
        """
        pulumi.set(__self__, "statement", statement)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def statement(self) -> str:
        """
        The statement of the static policy.
        """
        return pulumi.get(self, "statement")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the static policy.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class PolicyDefinitionTemplateLinked(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "policyTemplateId":
            suggest = "policy_template_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyDefinitionTemplateLinked. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyDefinitionTemplateLinked.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyDefinitionTemplateLinked.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 policy_template_id: str,
                 principal: Optional['outputs.PolicyDefinitionTemplateLinkedPrincipal'] = None,
                 resource: Optional['outputs.PolicyDefinitionTemplateLinkedResource'] = None):
        """
        :param str policy_template_id: The ID of the template.
        :param 'PolicyDefinitionTemplateLinkedPrincipalArgs' principal: The principal of the template linked policy.
        :param 'PolicyDefinitionTemplateLinkedResourceArgs' resource: The resource of the template linked policy.
        """
        pulumi.set(__self__, "policy_template_id", policy_template_id)
        if principal is not None:
            pulumi.set(__self__, "principal", principal)
        if resource is not None:
            pulumi.set(__self__, "resource", resource)

    @property
    @pulumi.getter(name="policyTemplateId")
    def policy_template_id(self) -> str:
        """
        The ID of the template.
        """
        return pulumi.get(self, "policy_template_id")

    @property
    @pulumi.getter
    def principal(self) -> Optional['outputs.PolicyDefinitionTemplateLinkedPrincipal']:
        """
        The principal of the template linked policy.
        """
        return pulumi.get(self, "principal")

    @property
    @pulumi.getter
    def resource(self) -> Optional['outputs.PolicyDefinitionTemplateLinkedResource']:
        """
        The resource of the template linked policy.
        """
        return pulumi.get(self, "resource")


@pulumi.output_type
class PolicyDefinitionTemplateLinkedPrincipal(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "entityId":
            suggest = "entity_id"
        elif key == "entityType":
            suggest = "entity_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyDefinitionTemplateLinkedPrincipal. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyDefinitionTemplateLinkedPrincipal.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyDefinitionTemplateLinkedPrincipal.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 entity_id: str,
                 entity_type: str):
        """
        :param str entity_id: The entity ID of the principal.
        :param str entity_type: The entity type of the principal.
        """
        pulumi.set(__self__, "entity_id", entity_id)
        pulumi.set(__self__, "entity_type", entity_type)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> str:
        """
        The entity ID of the principal.
        """
        return pulumi.get(self, "entity_id")

    @property
    @pulumi.getter(name="entityType")
    def entity_type(self) -> str:
        """
        The entity type of the principal.
        """
        return pulumi.get(self, "entity_type")


@pulumi.output_type
class PolicyDefinitionTemplateLinkedResource(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "entityId":
            suggest = "entity_id"
        elif key == "entityType":
            suggest = "entity_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PolicyDefinitionTemplateLinkedResource. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PolicyDefinitionTemplateLinkedResource.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PolicyDefinitionTemplateLinkedResource.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 entity_id: str,
                 entity_type: str):
        """
        :param str entity_id: The entity ID of the resource.
        :param str entity_type: The entity type of the resource.
        """
        pulumi.set(__self__, "entity_id", entity_id)
        pulumi.set(__self__, "entity_type", entity_type)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> str:
        """
        The entity ID of the resource.
        """
        return pulumi.get(self, "entity_id")

    @property
    @pulumi.getter(name="entityType")
    def entity_type(self) -> str:
        """
        The entity type of the resource.
        """
        return pulumi.get(self, "entity_type")


@pulumi.output_type
class PolicyStoreValidationSettings(dict):
    def __init__(__self__, *,
                 mode: str):
        """
        :param str mode: The mode for the validation settings. Valid values: `OFF`, `STRICT`.
               
               The following arguments are optional:
        """
        pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter
    def mode(self) -> str:
        """
        The mode for the validation settings. Valid values: `OFF`, `STRICT`.

        The following arguments are optional:
        """
        return pulumi.get(self, "mode")


@pulumi.output_type
class SchemaDefinition(dict):
    def __init__(__self__, *,
                 value: str):
        """
        :param str value: A JSON string representation of the schema.
        """
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        A JSON string representation of the schema.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class GetPolicyStoreValidationSettingResult(dict):
    def __init__(__self__, *,
                 mode: str):
        pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter
    def mode(self) -> str:
        return pulumi.get(self, "mode")


