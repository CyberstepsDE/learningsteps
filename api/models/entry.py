from pydantic import BaseModel, Field, field_validator, model_validator, ClassVar
from typing import Optional, ClassVar
from datetime import datetime
from uuid import uuid4

class EntryCreate(BaseModel):
    """Model for creating a new journal entry (user input)."""
    work: str = Field(
        max_length=256,
        description="What did you work on today?",
        json_schema_extra={"example": "Studied FastAPI and built my first API endpoints"}
    )
    struggle: str = Field(
        max_length=256,
        description="What's one thing you struggled with today?",
        json_schema_extra={"example": "Understanding async/await syntax and when to use it"}
    )
    intention: str = Field(
        max_length=256,
        description="What will you study/work on tomorrow?",
        json_schema_extra={"example": "Practice PostgreSQL queries and database design"}
    )

class Entry(BaseModel):
    # TODO: Add field validation rules

    # TODO: Add schema versioning
    schema_version: ClassVar[int] = 1
    
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the entry (UUID).",
        min_length=36, # Enforce UUID format length
        max_length=36
    )
    work: str = Field(
        ...,
        min_length=5, # Ensure work is not too short
        max_length=256,
        description="What did you work on today?"
    )
    struggle: str = Field(
        ...,
        min_length=5, # Ensure struggle is not too short
        max_length=256,
        description="What’s one thing you struggled with today?"
    )
    intention: str = Field(
        ...,
        min_length=5, # Ensures intention is not too short
        max_length=256,
        description="What will you study/work on tomorrow?"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the entry was created."
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the entry was last updated."
    )
    
    # TODO: Add custom validators
    @field_validator('id', mode='before')
    @classmethod
    def validate_uuid_format(cls, v: str):
        """Custom validator to ensure the ID is a valid UUID string."""
        if v is not None and len(v) != 36:
             raise ValueError('ID must be a 36-character UUID string.')
        return v
    
    @model_validator(mode='after')
    def check_intention_for_tomorrow(self) -> 'Entry':
        """Custom model validator to check a business rule across fields."""
        if "sleep" in self.intention.lower():
            # This is an example of checking a rule across fields
            print("Warning: Intention includes 'sleep'. Ensure productive work is planned.")
        return self
    
    # TODO: Add data sanitization methods
    @field_validator('work', 'struggle', 'intention', mode='before')
    @classmethod
    def sanitize_input(cls, v: str):
        """Sanitization: Strip whitespace from input fields."""
        if isinstance(v, str):
            # Strip leading/trailing whitespace from user input
            v = v.strip()
        return v

    @field_validator('work', 'struggle', 'intention', mode='after')
    @classmethod
    def normalize_case(cls, v: str):
        """Sanitization: Normalize text to sentence case (Capitalize first letter)."""
        if v:
            return v[0].upper() + v[1:]
        return v
    
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }