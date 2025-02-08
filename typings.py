from pydantic import BaseModel
from typing import List, Literal

class URLList(BaseModel):
    urls: List[str]


class AskQuestionRequest(BaseModel):
    question: str
    resource_ids: List[str]
    table: bool = False


class GenerateFile(BaseModel):
    IDs: List[str]
    format: Literal["PDF", "PPT"] 
    layout: Literal["1perpage", "2perpage"] 
    heading: str
    subheading:str


