# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from iparapheur_provisioning.models.metadata_type import MetadataType
from typing import Optional, Set
from typing_extensions import Self

class MetadataDto(BaseModel):
    """
    body
    """ # noqa: E501
    id: Optional[StrictStr] = None
    name: Annotated[str, Field(min_length=2, strict=True, max_length=255)]
    key: Annotated[str, Field(min_length=1, strict=True, max_length=128)]
    index: Optional[StrictInt] = None
    type: Optional[MetadataType] = None
    restricted_values: Optional[List[Optional[StrictStr]]] = Field(default=None, alias="restrictedValues")
    __properties: ClassVar[List[str]] = ["id", "name", "key", "index", "type", "restrictedValues"]

    @field_validator('name')
    def name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[^\r\n ]*$", value):
            raise ValueError(r"must validate the regular expression /^[^\r\n ]*$/")
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of MetadataDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "id",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if index (nullable) is None
        # and model_fields_set contains the field
        if self.index is None and "index" in self.model_fields_set:
            _dict['index'] = None

        # set to None if restricted_values (nullable) is None
        # and model_fields_set contains the field
        if self.restricted_values is None and "restricted_values" in self.model_fields_set:
            _dict['restrictedValues'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MetadataDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "key": obj.get("key"),
            "index": obj.get("index"),
            "type": obj.get("type"),
            "restrictedValues": obj.get("restrictedValues")
        })
        return _obj


