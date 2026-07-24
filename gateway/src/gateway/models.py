from pydantic import BaseModel


class Usage(BaseModel):
    input_tokens: int
    output_tokens: int


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    text: str
    usage: Usage


class ProviderError(Exception):
    def __init__(
        self,
        message: str,
        retryable: bool,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.retryable = retryable
