from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Thesis(BaseModel):
    id: Optional[int] = Field(default=None, description="Unique identifier for the thesis")
    theme_id: str = Field(..., description="ID of the associated theme")
    thesis_text: str = Field(..., description="Core thesis sentence extracted from the post")
    post_title: str = Field(..., description="Title of the original blog post")
    post_url: str = Field(..., description="Canonical URL of the blog post")
    published_at: datetime = Field(..., description="When the blog post was originally published")
    ingested_at: datetime = Field(..., description="When the post was ingested by the system")