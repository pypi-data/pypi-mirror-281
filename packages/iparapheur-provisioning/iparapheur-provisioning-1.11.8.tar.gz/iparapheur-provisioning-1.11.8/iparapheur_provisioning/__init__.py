# coding: utf-8

# flake8: noqa

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


__version__ = "1.11.8"

# import apis into sdk package
from iparapheur_provisioning.api.admin_all_users_api import AdminAllUsersApi
from iparapheur_provisioning.api.admin_desk_api import AdminDeskApi
from iparapheur_provisioning.api.admin_metadata_api import AdminMetadataApi
from iparapheur_provisioning.api.admin_seal_certificate_api import AdminSealCertificateApi
from iparapheur_provisioning.api.admin_template_api import AdminTemplateApi
from iparapheur_provisioning.api.admin_tenant_api import AdminTenantApi
from iparapheur_provisioning.api.admin_tenant_user_api import AdminTenantUserApi
from iparapheur_provisioning.api.admin_typology_api import AdminTypologyApi
from iparapheur_provisioning.api.admin_workflow_definition_api import AdminWorkflowDefinitionApi

# import ApiClient
from iparapheur_provisioning.api_response import ApiResponse
from iparapheur_provisioning.api_client import ApiClient
from iparapheur_provisioning.configuration import Configuration
from iparapheur_provisioning.exceptions import OpenApiException
from iparapheur_provisioning.exceptions import ApiTypeError
from iparapheur_provisioning.exceptions import ApiValueError
from iparapheur_provisioning.exceptions import ApiKeyError
from iparapheur_provisioning.exceptions import ApiAttributeError
from iparapheur_provisioning.exceptions import ApiException

# import models into sdk package
from iparapheur_provisioning.models.certificate_informations import CertificateInformations
from iparapheur_provisioning.models.create_seal_certificate_request import CreateSealCertificateRequest
from iparapheur_provisioning.models.desk_dto import DeskDto
from iparapheur_provisioning.models.desk_representation import DeskRepresentation
from iparapheur_provisioning.models.error_response import ErrorResponse
from iparapheur_provisioning.models.external_signature_config_representation import ExternalSignatureConfigRepresentation
from iparapheur_provisioning.models.external_signature_config_sort_by import ExternalSignatureConfigSortBy
from iparapheur_provisioning.models.external_signature_provider import ExternalSignatureProvider
from iparapheur_provisioning.models.internal_metadata import InternalMetadata
from iparapheur_provisioning.models.layer_representation import LayerRepresentation
from iparapheur_provisioning.models.layer_sort_by import LayerSortBy
from iparapheur_provisioning.models.metadata_dto import MetadataDto
from iparapheur_provisioning.models.metadata_representation import MetadataRepresentation
from iparapheur_provisioning.models.metadata_sort_by import MetadataSortBy
from iparapheur_provisioning.models.metadata_type import MetadataType
from iparapheur_provisioning.models.page_desk_representation import PageDeskRepresentation
from iparapheur_provisioning.models.page_metadata_representation import PageMetadataRepresentation
from iparapheur_provisioning.models.page_seal_certificate_representation import PageSealCertificateRepresentation
from iparapheur_provisioning.models.page_subtype_representation import PageSubtypeRepresentation
from iparapheur_provisioning.models.page_tenant_representation import PageTenantRepresentation
from iparapheur_provisioning.models.page_type_representation import PageTypeRepresentation
from iparapheur_provisioning.models.page_user_representation import PageUserRepresentation
from iparapheur_provisioning.models.page_workflow_definition_representation import PageWorkflowDefinitionRepresentation
from iparapheur_provisioning.models.pageable_object import PageableObject
from iparapheur_provisioning.models.pdf_signature_position import PdfSignaturePosition
from iparapheur_provisioning.models.seal_certificate_dto import SealCertificateDto
from iparapheur_provisioning.models.seal_certificate_representation import SealCertificateRepresentation
from iparapheur_provisioning.models.seal_certificate_sort_by import SealCertificateSortBy
from iparapheur_provisioning.models.signature_format import SignatureFormat
from iparapheur_provisioning.models.signature_protocol import SignatureProtocol
from iparapheur_provisioning.models.sort_object import SortObject
from iparapheur_provisioning.models.step_definition_dto import StepDefinitionDto
from iparapheur_provisioning.models.step_definition_parallel_type import StepDefinitionParallelType
from iparapheur_provisioning.models.step_definition_type import StepDefinitionType
from iparapheur_provisioning.models.subtype_dto import SubtypeDto
from iparapheur_provisioning.models.subtype_layer_association import SubtypeLayerAssociation
from iparapheur_provisioning.models.subtype_layer_dto import SubtypeLayerDto
from iparapheur_provisioning.models.subtype_metadata_dto import SubtypeMetadataDto
from iparapheur_provisioning.models.subtype_representation import SubtypeRepresentation
from iparapheur_provisioning.models.template_info import TemplateInfo
from iparapheur_provisioning.models.template_type import TemplateType
from iparapheur_provisioning.models.tenant_dto import TenantDto
from iparapheur_provisioning.models.tenant_representation import TenantRepresentation
from iparapheur_provisioning.models.tenant_sort_by import TenantSortBy
from iparapheur_provisioning.models.type_dto import TypeDto
from iparapheur_provisioning.models.type_representation import TypeRepresentation
from iparapheur_provisioning.models.typology_sort_by import TypologySortBy
from iparapheur_provisioning.models.update_seal_certificate_request import UpdateSealCertificateRequest
from iparapheur_provisioning.models.user_dto import UserDto
from iparapheur_provisioning.models.user_privilege import UserPrivilege
from iparapheur_provisioning.models.user_representation import UserRepresentation
from iparapheur_provisioning.models.user_sort_by import UserSortBy
from iparapheur_provisioning.models.workflow_definition_dto import WorkflowDefinitionDto
from iparapheur_provisioning.models.workflow_definition_representation import WorkflowDefinitionRepresentation
from iparapheur_provisioning.models.workflow_definition_sort_by import WorkflowDefinitionSortBy
