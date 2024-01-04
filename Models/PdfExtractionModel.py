from pydantic import BaseModel

class ExtractionRequest(BaseModel):
    URL: str

