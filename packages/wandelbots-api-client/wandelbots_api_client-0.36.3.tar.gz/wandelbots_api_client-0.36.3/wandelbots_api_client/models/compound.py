# coding: utf-8

"""
    Wandelbots Nova Public API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 1.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set
from typing_extensions import Self

class Compound(BaseModel):
    """
    Describes a collision shape compounded from multiple collision objects. All objects are described in the compounds reference frame.
    """ # noqa: E501
    child_geometries: List[Geometry] = Field(description="A list of geometries sharing the same reference frame.")
    __properties: ClassVar[List[str]] = ["child_geometries"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Compound from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in child_geometries (list)
        _items = []
        if self.child_geometries:
            for _item in self.child_geometries:
                if _item:
                    _items.append(_item.to_dict())
            _dict['child_geometries'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Compound from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "child_geometries": [Geometry.from_dict(_item) for _item in obj["child_geometries"]] if obj.get("child_geometries") is not None else None
        })
        return _obj

from wandelbots_api_client.models.geometry import Geometry
# TODO: Rewrite to not use raise_errors
Compound.model_rebuild(raise_errors=False)

