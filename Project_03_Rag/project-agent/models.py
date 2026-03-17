from pydantic import BaseModel, Field
from typing import List, Optional

class SourceInfo(BaseModel):
    tool: str = Field(description="הכלי שבו נעשה שימוש, למשל cursor, claude_code")
    file: str = Field(description="הנתיב המלא לקובץ")
    anchor: Optional[str] = Field(None, description="כותרת או עוגן בתוך הקובץ")
    line_range: Optional[List[int]] = Field(None, description="טווח שורות [התחלה, סוף]")

class DecisionItem(BaseModel):
    id: str
    title: str
    summary: str
    tags: List[str]
    source: SourceInfo
    observed_at: str

class RuleItem(BaseModel):
    id: str
    rule: str
    scope: str
    notes: Optional[str] = None
    source: SourceInfo
    observed_at: str

class WarningItem(BaseModel):
    id: str
    area: str
    message: str
    severity: str
    source: SourceInfo
    observed_at: str

class ExtractionResult(BaseModel):
    decisions: List[DecisionItem]
    rules: List[RuleItem]
    warnings: List[WarningItem]