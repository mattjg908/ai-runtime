from pydantic import BaseModel


class Usage(BaseModel):
    input_tokens: int
    output_tokens: int


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    text: str
    usage: Usage


class ProviderError(BaseModel):
    message: str
