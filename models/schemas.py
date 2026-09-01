from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Source(BaseModel):
    type: str
    name: str
    reference: Optional[str] = None


class AgentResultData(BaseModel):
    classification: str
    confidence: float = Field(ge=0.0, le=1.0)
    score: float = Field(ge=-1.0, le=1.0)
    summary: str
    reasoning: List[str]


class AgentResult(BaseModel):
    agent_name: str
    status: str
    input: Dict[str, Any]
    result: AgentResultData
    sources: List[Source] = []
    metadata: Dict[str, Any] = {}