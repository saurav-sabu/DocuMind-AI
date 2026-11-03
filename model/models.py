from pydantic import BaseModel, Field
from typing import List, Optional

class Metadata(BaseModel):
    Summary: List[str] = Field(default_factory=list,description="Summary of the documents")
    Title: str = Field(default="",description="Title of the document")
    Author: str = Field(default="",description="Author of the document")
    DateCreated: str = Field(default="",description="Date the document was created")
    LastModifiedDate: str = Field(default="",description="Date the document was last modified")
    Publisher: str = Field(default="",description="Publisher of the document")
    Language: str = Field(default="",description="Language of the document")
    PageCount: int | str = Field(default="",description="Page count of the document")
    SentimentTone: str = Field(default="",description="Sentiment tone of the document")