# -*-coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel
import enum


class RspType(enum.Enum):
    CONTENT = 1
    EXIT = 2
    JUMP_TO = 3


class AgentMessage(BaseModel):
    type: RspType
    content: Optional[str] = None  # CONTENT
    target_agent: Optional[str] = None # JUMP_TO


