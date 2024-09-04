from typing import NotRequired, TypedDict

from pydantic import BaseModel, ValidationError

class Meta(TypedDict):
    event_name: str
    custom_data: NotRequired[dict]

class Event(BaseModel):
    meta: Meta

def webhook_has_meta(obj):
    valid = True
    try:
        Event.model_validate(obj)
    except ValidationError:
        valid = False
    return valid
