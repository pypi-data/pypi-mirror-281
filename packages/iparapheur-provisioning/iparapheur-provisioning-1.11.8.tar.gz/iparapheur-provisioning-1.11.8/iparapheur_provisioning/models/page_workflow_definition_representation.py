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

from pydantic import BaseModel, Field, StrictBool, StrictInt
from typing import Any, ClassVar, Dict, List, Optional
from iparapheur_provisioning.models.pageable_object import PageableObject
from iparapheur_provisioning.models.sort_object import SortObject
from iparapheur_provisioning.models.workflow_definition_representation import WorkflowDefinitionRepresentation
from typing import Optional, Set
from typing_extensions import Self

class PageWorkflowDefinitionRepresentation(BaseModel):
    """
    PageWorkflowDefinitionRepresentation
    """ # noqa: E501
    total_elements: Optional[StrictInt] = Field(default=None, alias="totalElements")
    total_pages: Optional[StrictInt] = Field(default=None, alias="totalPages")
    size: Optional[StrictInt] = None
    content: Optional[List[WorkflowDefinitionRepresentation]] = None
    number: Optional[StrictInt] = None
    sort: Optional[SortObject] = None
    first: Optional[StrictBool] = None
    last: Optional[StrictBool] = None
    number_of_elements: Optional[StrictInt] = Field(default=None, alias="numberOfElements")
    pageable: Optional[PageableObject] = None
    empty: Optional[StrictBool] = None
    __properties: ClassVar[List[str]] = ["totalElements", "totalPages", "size", "content", "number", "sort", "first", "last", "numberOfElements", "pageable", "empty"]

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
        """Create an instance of PageWorkflowDefinitionRepresentation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in content (list)
        _items = []
        if self.content:
            for _item in self.content:
                if _item:
                    _items.append(_item.to_dict())
            _dict['content'] = _items
        # override the default output from pydantic by calling `to_dict()` of sort
        if self.sort:
            _dict['sort'] = self.sort.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pageable
        if self.pageable:
            _dict['pageable'] = self.pageable.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PageWorkflowDefinitionRepresentation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "totalElements": obj.get("totalElements"),
            "totalPages": obj.get("totalPages"),
            "size": obj.get("size"),
            "content": [WorkflowDefinitionRepresentation.from_dict(_item) for _item in obj["content"]] if obj.get("content") is not None else None,
            "number": obj.get("number"),
            "sort": SortObject.from_dict(obj["sort"]) if obj.get("sort") is not None else None,
            "first": obj.get("first"),
            "last": obj.get("last"),
            "numberOfElements": obj.get("numberOfElements"),
            "pageable": PageableObject.from_dict(obj["pageable"]) if obj.get("pageable") is not None else None,
            "empty": obj.get("empty")
        })
        return _obj


