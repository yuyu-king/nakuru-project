from collections import namedtuple
from pydantic import BaseModel
from .enums import ExternalEventTypes

InternalEvent = namedtuple("Event", ("name", "body"))


class ExternalEvent(BaseModel):
    type: ExternalEventTypes
