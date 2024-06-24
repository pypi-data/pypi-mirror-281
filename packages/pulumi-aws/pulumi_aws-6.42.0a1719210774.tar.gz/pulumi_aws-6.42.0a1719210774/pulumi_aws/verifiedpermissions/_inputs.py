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
    'PolicyDefinitionArgs',
    'PolicyDefinitionStaticArgs',
    'PolicyDefinitionTemplateLinkedArgs',
    'PolicyDefinitionTemplateLinkedPrincipalArgs',
    'PolicyDefinitionTemplateLinkedResourceArgs',
    'PolicyStoreValidationSettingsArgs',
    'SchemaDefinitionArgs',
]

@pulumi.input_type
class PolicyDefinitionArgs:
    def __init__(__self__, *,
                 static: Optional[pulumi.Input['PolicyDefinitionStaticArgs']] = None,
                 template_linked: Optional[pulumi.Input['PolicyDefinitionTemplateLinkedArgs']] = None):
        """
        :param pulumi.Input['PolicyDefinitionStaticArgs'] static: The static policy statement. See Static below.
        :param pulumi.Input['PolicyDefinitionTemplateLinkedArgs'] template_linked: The template linked policy. See Template Linked below.
        """
        if static is not None:
            pulumi.set(__self__, "static", static)
        if template_linked is not None:
            pulumi.set(__self__, "template_linked", template_linked)

    @property
    @pulumi.getter
    def static(self) -> Optional[pulumi.Input['PolicyDefinitionStaticArgs']]:
        """
        The static policy statement. See Static below.
        """
        return pulumi.get(self, "static")

    @static.setter
    def static(self, value: Optional[pulumi.Input['PolicyDefinitionStaticArgs']]):
        pulumi.set(self, "static", value)

    @property
    @pulumi.getter(name="templateLinked")
    def template_linked(self) -> Optional[pulumi.Input['PolicyDefinitionTemplateLinkedArgs']]:
        """
        The template linked policy. See Template Linked below.
        """
        return pulumi.get(self, "template_linked")

    @template_linked.setter
    def template_linked(self, value: Optional[pulumi.Input['PolicyDefinitionTemplateLinkedArgs']]):
        pulumi.set(self, "template_linked", value)


@pulumi.input_type
class PolicyDefinitionStaticArgs:
    def __init__(__self__, *,
                 statement: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] statement: The statement of the static policy.
        :param pulumi.Input[str] description: The description of the static policy.
        """
        pulumi.set(__self__, "statement", statement)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def statement(self) -> pulumi.Input[str]:
        """
        The statement of the static policy.
        """
        return pulumi.get(self, "statement")

    @statement.setter
    def statement(self, value: pulumi.Input[str]):
        pulumi.set(self, "statement", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the static policy.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class PolicyDefinitionTemplateLinkedArgs:
    def __init__(__self__, *,
                 policy_template_id: pulumi.Input[str],
                 principal: Optional[pulumi.Input['PolicyDefinitionTemplateLinkedPrincipalArgs']] = None,
                 resource: Optional[pulumi.Input['PolicyDefinitionTemplateLinkedResourceArgs']] = None):
        """
        :param pulumi.Input[str] policy_template_id: The ID of the template.
        :param pulumi.Input['PolicyDefinitionTemplateLinkedPrincipalArgs'] principal: The principal of the template linked policy.
        :param pulumi.Input['PolicyDefinitionTemplateLinkedResourceArgs'] resource: The resource of the template linked policy.
        """
        pulumi.set(__self__, "policy_template_id", policy_template_id)
        if principal is not None:
            pulumi.set(__self__, "principal", principal)
        if resource is not None:
            pulumi.set(__self__, "resource", resource)

    @property
    @pulumi.getter(name="policyTemplateId")
    def policy_template_id(self) -> pulumi.Input[str]:
        """
        The ID of the template.
        """
        return pulumi.get(self, "policy_template_id")

    @policy_template_id.setter
    def policy_template_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_template_id", value)

    @property
    @pulumi.getter
    def principal(self) -> Optional[pulumi.Input['PolicyDefinitionTemplateLinkedPrincipalArgs']]:
        """
        The principal of the template linked policy.
        """
        return pulumi.get(self, "principal")

    @principal.setter
    def principal(self, value: Optional[pulumi.Input['PolicyDefinitionTemplateLinkedPrincipalArgs']]):
        pulumi.set(self, "principal", value)

    @property
    @pulumi.getter
    def resource(self) -> Optional[pulumi.Input['PolicyDefinitionTemplateLinkedResourceArgs']]:
        """
        The resource of the template linked policy.
        """
        return pulumi.get(self, "resource")

    @resource.setter
    def resource(self, value: Optional[pulumi.Input['PolicyDefinitionTemplateLinkedResourceArgs']]):
        pulumi.set(self, "resource", value)


@pulumi.input_type
class PolicyDefinitionTemplateLinkedPrincipalArgs:
    def __init__(__self__, *,
                 entity_id: pulumi.Input[str],
                 entity_type: pulumi.Input[str]):
        """
        :param pulumi.Input[str] entity_id: The entity ID of the principal.
        :param pulumi.Input[str] entity_type: The entity type of the principal.
        """
        pulumi.set(__self__, "entity_id", entity_id)
        pulumi.set(__self__, "entity_type", entity_type)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> pulumi.Input[str]:
        """
        The entity ID of the principal.
        """
        return pulumi.get(self, "entity_id")

    @entity_id.setter
    def entity_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "entity_id", value)

    @property
    @pulumi.getter(name="entityType")
    def entity_type(self) -> pulumi.Input[str]:
        """
        The entity type of the principal.
        """
        return pulumi.get(self, "entity_type")

    @entity_type.setter
    def entity_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "entity_type", value)


@pulumi.input_type
class PolicyDefinitionTemplateLinkedResourceArgs:
    def __init__(__self__, *,
                 entity_id: pulumi.Input[str],
                 entity_type: pulumi.Input[str]):
        """
        :param pulumi.Input[str] entity_id: The entity ID of the resource.
        :param pulumi.Input[str] entity_type: The entity type of the resource.
        """
        pulumi.set(__self__, "entity_id", entity_id)
        pulumi.set(__self__, "entity_type", entity_type)

    @property
    @pulumi.getter(name="entityId")
    def entity_id(self) -> pulumi.Input[str]:
        """
        The entity ID of the resource.
        """
        return pulumi.get(self, "entity_id")

    @entity_id.setter
    def entity_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "entity_id", value)

    @property
    @pulumi.getter(name="entityType")
    def entity_type(self) -> pulumi.Input[str]:
        """
        The entity type of the resource.
        """
        return pulumi.get(self, "entity_type")

    @entity_type.setter
    def entity_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "entity_type", value)


@pulumi.input_type
class PolicyStoreValidationSettingsArgs:
    def __init__(__self__, *,
                 mode: pulumi.Input[str]):
        """
        :param pulumi.Input[str] mode: The mode for the validation settings. Valid values: `OFF`, `STRICT`.
               
               The following arguments are optional:
        """
        pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter
    def mode(self) -> pulumi.Input[str]:
        """
        The mode for the validation settings. Valid values: `OFF`, `STRICT`.

        The following arguments are optional:
        """
        return pulumi.get(self, "mode")

    @mode.setter
    def mode(self, value: pulumi.Input[str]):
        pulumi.set(self, "mode", value)


@pulumi.input_type
class SchemaDefinitionArgs:
    def __init__(__self__, *,
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] value: A JSON string representation of the schema.
        """
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        A JSON string representation of the schema.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


