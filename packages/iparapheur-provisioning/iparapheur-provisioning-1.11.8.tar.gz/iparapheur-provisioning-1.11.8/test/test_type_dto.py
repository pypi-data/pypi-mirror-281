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

from iparapheur_provisioning.models.type_dto import TypeDto

class TestTypeDto(unittest.TestCase):
    """TypeDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TypeDto:
        """Test TypeDto
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TypeDto`
        """
        model = TypeDto()
        if include_optional:
            return TypeDto(
                id = '',
                name = 'jXAuKb%@;_5)#fEb-bx%oZ01',
                description = '012',
                signature_format = 'PKCS7',
                protocol = 'HELIOS',
                signature_visible = True,
                signature_position = iparapheur_provisioning.models.pdf_signature_position.PdfSignaturePosition(
                    x = 1.337, 
                    y = 1.337, 
                    page = 56, 
                    template_type = 'MAIL_NOTIFICATION_SINGLE', ),
                signature_location = '',
                signature_zip_code = ''
            )
        else:
            return TypeDto(
                name = 'jXAuKb%@;_5)#fEb-bx%oZ01',
        )
        """

    def testTypeDto(self):
        """Test TypeDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
