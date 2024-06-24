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

from iparapheur_internal.models.page_folder_listable_dto import PageFolderListableDto

class TestPageFolderListableDto(unittest.TestCase):
    """PageFolderListableDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PageFolderListableDto:
        """Test PageFolderListableDto
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PageFolderListableDto`
        """
        model = PageFolderListableDto()
        if include_optional:
            return PageFolderListableDto(
                total_elements = 56,
                total_pages = 56,
                size = 56,
                content = [
                    iparapheur_internal.models.folder_listable_dto.FolderListableDto(
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
            return PageFolderListableDto(
        )
        """

    def testPageFolderListableDto(self):
        """Test PageFolderListableDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
