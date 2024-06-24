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

from iparapheur_internal.models.signature_proof import SignatureProof

class TestSignatureProof(unittest.TestCase):
    """SignatureProof unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SignatureProof:
        """Test SignatureProof
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SignatureProof`
        """
        model = SignatureProof()
        if include_optional:
            return SignatureProof(
                id = '',
                name = '',
                index = 56,
                page_count = 56,
                content_length = 56,
                media_type = iparapheur_internal.models.media_type.MediaType(
                    type = '', 
                    subtype = '', 
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
                        signature_number = 0, 
                        template_type = 'MAIL_NOTIFICATION_SINGLE', )
                    ],
                signature_tags = {
                    'key' : iparapheur_internal.models.pdf_signature_position.PdfSignaturePosition(
                        x = 1.337, 
                        y = 1.337, 
                        page = 56, 
                        template_type = 'MAIL_NOTIFICATION_SINGLE', )
                    },
                seal_tags = {
                    'key' : iparapheur_internal.models.pdf_signature_position.PdfSignaturePosition(
                        x = 1.337, 
                        y = 1.337, 
                        page = 56, 
                        template_type = 'MAIL_NOTIFICATION_SINGLE', )
                    },
                detached_signatures = [
                    iparapheur_internal.models.detached_signature.DetachedSignature(
                        id = '', 
                        name = '', 
                        content_length = 56, 
                        media_type = iparapheur_internal.models.media_type.MediaType(
                            type = '', 
                            subtype = '', 
                            parameters = {
                                'key' : ''
                                }, 
                            quality_value = 1.337, 
                            wildcard_type = True, 
                            wildcard_subtype = True, 
                            subtype_suffix = '', 
                            charset = '', 
                            concrete = True, ), 
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
                proof_target_task_id = '',
                error_message = '',
                internal = True,
                signature_proof = True,
                deletable = True,
                is_main_document = True
            )
        else:
            return SignatureProof(
        )
        """

    def testSignatureProof(self):
        """Test SignatureProof"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
