from typing import TypedDict

from pydantic import BaseModel, ValidationError

class CustomData(TypedDict):
    user_id: str

class Meta(TypedDict):
    event_name: str
    custom_data: CustomData

class EventMetaAttribute(BaseModel):
    meta: Meta

class EventDataAttribute(BaseModel):
    data: dict

def webhook_has_meta(obj):
    valid = True
    try:
        EventMetaAttribute.model_validate(obj)
    except ValidationError:
        valid = False
    return valid

def webhook_has_data(obj):
    valid = True
    try:
        EventDataAttribute.model_validate(obj)
    except ValidationError:
        valid = False
    return valid
