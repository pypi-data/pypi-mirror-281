# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from iparapheur_internal.models.page_folder_dto import PageFolderDto

class TestPageFolderDto(unittest.TestCase):
    """PageFolderDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PageFolderDto:
        """Test PageFolderDto
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PageFolderDto`
        """
        model = PageFolderDto()
        if include_optional:
            return PageFolderDto(
                total_elements = 56,
                total_pages = 56,
                size = 56,
                content = [
                    iparapheur_internal.models.folder_dto.FolderDto(
                        id = '', 
                        name = '01', 
                        due_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        metadata = {
                            'key' : ''
                            }, 
                        draft_creation_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        type = iparapheur_internal.models.type_dto.TypeDto(
                            id = '', 
                            name = 'jXAuKb%@;_5)#fEb-bx%oZ01', 
                            description = '012', 
                            signature_format = 'PKCS7', 
                            protocol = 'HELIOS', 
                            signature_visible = True, 
                            signature_position = iparapheur_internal.models.pdf_signature_position.PdfSignaturePosition(
                                x = 1.337, 
                                y = 1.337, 
                                page = 56, 
                                template_type = 'MAIL_NOTIFICATION_SINGLE', ), 
                            signature_location = '', 
                            signature_zip_code = '', ), 
                        subtype = iparapheur_internal.models.subtype_dto.SubtypeDto(
                            id = '', 
                            name = 'jXAuKb%@;_5)#fEb-bx%oZ01', 
                            description = '012', 
                            creation_workflow_id = '', 
                            validation_workflow_id = '', 
                            workflow_selection_script = '', 
                            annotations_allowed = True, 
                            external_signature_automatic = True, 
                            secure_mail_server_id = 56, 
                            seal_certificate_id = '', 
                            seal_certificate = iparapheur_internal.models.seal_certificate_representation.SealCertificateRepresentation(
                                id = '', 
                                name = 'Example certificate', 
                                expiration_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                usage_count = 56, ), 
                            subtype_metadata_list = [
                                iparapheur_internal.models.subtype_metadata_dto.SubtypeMetadataDto(
                                    metadata_id = '', 
                                    default_value = '', 
                                    mandatory = True, 
                                    editable = True, )
                                ], 
                            subtype_layers = [
                                iparapheur_internal.models.subtype_layer_dto.SubtypeLayerDto(
                                    layer_id = '', 
                                    layer = iparapheur_internal.models.layer_representation.LayerRepresentation(
                                        id = '', 
                                        name = 'jXAuKb%@;_5)#fEb-bx%oZ01', ), 
                                    association = 'ALL', )
                                ], 
                            external_signature_config_id = '', 
                            external_signature_config = iparapheur_internal.models.external_signature_config_representation.ExternalSignatureConfigRepresentation(
                                id = '', 
                                name = '01', 
                                service_name = 'YOUSIGN_V2', 
                                url = '', 
                                login = '', ), 
                            creation_permitted_desk_ids = [
                                ''
                                ], 
                            creation_permitted_desks = [
                                iparapheur_internal.models.desk_representation.DeskRepresentation(
                                    id = '', 
                                    name = 'jXAuKb%@;_5)#fEb-bx%oZ01', 
                                    tenant_id = '', )
                                ], 
                            filterable_by_desk_ids = [
                                ''
                                ], 
                            filterable_by_desks = [
                                iparapheur_internal.models.desk_representation.DeskRepresentation(
                                    id = '', 
                                    name = 'jXAuKb%@;_5)#fEb-bx%oZ01', 
                                    tenant_id = '', )
                                ], 
                            max_main_documents = 56, 
                            multi_documents = True, 
                            annexe_included = True, 
                            digital_signature_mandatory = True, 
                            reading_mandatory = True, 
                            seal_automatic = True, ), 
                        origin_desk = , 
                        final_desk = , 
                        is_read_by_current_user = True, 
                        legacy_id = '', 
                        type_id = '', 
                        subtype_id = '', 
                        step_list = [
                            iparapheur_internal.models.task.Task(
                                id = '', 
                                action = 'VISA', 
                                performed_action = 'VISA', 
                                external_state = 'FORM', 
                                state = 'DRAFT', 
                                desks = [
                                    
                                    ], 
                                delegated_by_desk = , 
                                user = iparapheur_internal.models.user_representation.UserRepresentation(
                                    id = '', 
                                    user_name = '0', 
                                    first_name = '', 
                                    last_name = '', 
                                    email = '', 
                                    privilege = 'NONE', 
                                    is_ldap_synchronized = True, ), 
                                read_by_user_ids = [
                                    ''
                                    ], 
                                public_certificate_base64 = '', 
                                external_signature_procedure_id = '', 
                                begin_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                draft_creation_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                public_annotation = '', 
                                private_annotation = '', 
                                notified_desks = [
                                    
                                    ], 
                                workflow_index = 56, 
                                step_index = 56, 
                                mandatory_validation_metadata = [
                                    ''
                                    ], 
                                mandatory_rejection_metadata = [
                                    ''
                                    ], 
                                instance_name = '', )
                            ], 
                        document_list = [
                            iparapheur_internal.models.document_dto.DocumentDto(
                                id = '', 
                                name = '', 
                                index = 56, 
                                page_count = 56, 
                                content_length = 56, 
                                media_type = iparapheur_internal.models.media_type.MediaType(
                                    parameters = {
                                        'key' : ''
                                        }, 
                                    quality_value = 1.337, 
                                    wildcard_type = True, 
                                    wildcard_subtype = True, 
                                    subtype_suffix = '', 
                                    charset = '', 
                                    concrete = True, ), 
                                pages_properties = {
                                    'key' : iparapheur_internal.models.page_info.PageInfo(
                                        width = 1.337, 
                                        height = 1.337, 
                                        rotation = 56, )
                                    }, 
                                pdf_visual_id = '', 
                                signature_placement_annotations = [
                                    iparapheur_internal.models.signature_placement.SignaturePlacement(
                                        id = '', 
                                        page = 1, 
                                        width = 15, 
                                        height = 15, 
                                        x = 56, 
                                        y = 56, 
                                        page_rotation = 0, 
                                        page_width = 276, 
                                        page_height = 308, 
                                        rectangle_origin = 'TOP_RIGHT', 
                                        signature_number = 0, )
                                    ], 
                                signature_tags = {
                                    'key' : iparapheur_internal.models.pdf_signature_position.PdfSignaturePosition(
                                        x = 1.337, 
                                        y = 1.337, 
                                        page = 56, )
                                    }, 
                                seal_tags = {
                                    'key' : 
                                    }, 
                                detached_signatures = [
                                    iparapheur_internal.models.detached_signature.DetachedSignature(
                                        id = '', 
                                        name = '', 
                                        content_length = 56, 
                                        target_document_id = '', 
                                        target_task_id = '', )
                                    ], 
                                embedded_signature_infos = [
                                    iparapheur_internal.models.signature_info.SignatureInfo(
                                        signature_date_time = 56, 
                                        is_signature_valid = True, 
                                        name = '', 
                                        issuer_name = '', )
                                    ], 
                                signature_proof = True, 
                                deletable = True, 
                                is_main_document = True, )
                            ], 
                        signature_proof_list = [
                            iparapheur_internal.models.signature_proof.SignatureProof(
                                id = '', 
                                name = '', 
                                index = 56, 
                                page_count = 56, 
                                content_length = 56, 
                                pdf_visual_id = '', 
                                proof_target_task_id = '', 
                                error_message = '', 
                                internal = True, 
                                signature_proof = True, 
                                deletable = True, 
                                is_main_document = True, )
                            ], 
                        read_by_user_ids = [
                            ''
                            ], 
                        read_by_current_user = True, )
                    ],
                number = 56,
                sort = iparapheur_internal.models.sort_object.SortObject(
                    empty = True, 
                    sorted = True, 
                    unsorted = True, ),
                first = True,
                last = True,
                number_of_elements = 56,
                pageable = iparapheur_internal.models.pageable_object.PageableObject(
                    offset = 56, 
                    sort = iparapheur_internal.models.sort_object.SortObject(
                        empty = True, 
                        sorted = True, 
                        unsorted = True, ), 
                    page_size = 56, 
                    paged = True, 
                    page_number = 56, 
                    unpaged = True, ),
                empty = True
            )
        else:
            return PageFolderDto(
        )
        """

    def testPageFolderDto(self):
        """Test PageFolderDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
