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

from iparapheur_internal.api.template_api import TemplateApi


class TestTemplateApi(unittest.TestCase):
    """TemplateApi unit test stubs"""

    def setUp(self) -> None:
        self.api = TemplateApi()

    def tearDown(self) -> None:
        pass

    def test_test_signature_template(self) -> None:
        """Test case for test_signature_template

        Test the tenant signature template
        """
        pass


if __name__ == '__main__':
    unittest.main()
