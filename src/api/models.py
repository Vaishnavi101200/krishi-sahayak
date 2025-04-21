from pydantic import BaseModel
from typing import Optional, Dict, List

class SchemeBase(BaseModel):
    scheme_name: str
    scheme_level: str
    description: Optional[str] = None
    eligibility: Optional[str] = None
    benefits: Optional[str] = None
    application_process: Optional[str] = None
    deadline: Optional[str] = None
    source_link: Optional[str] = None
    category: Optional[str] = None

class SchemeResponse(BaseModel):
    scheme_id: str
    details: SchemeBase 