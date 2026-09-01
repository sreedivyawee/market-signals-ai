from dataclasses import dataclass
from typing import Literal


Signal = Literal["BULLISH", "BEARISH", "HOLD"]


@dataclass
class AgentResult:
    agent: str
    signal: Signal
    confidence: float
    reasoning: str