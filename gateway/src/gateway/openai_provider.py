from openai import OpenAI

from gateway.models import GenerateRequest, GenerateResponse, Usage
from gateway.provider import ModelProvider


class OpenAIProvider(ModelProvider):
    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    async def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        response = self._client.responses.create(
            model=self._model,
            input=request.prompt,
        )

        if response.usage is None:
            raise RuntimeError("OpenAI response did not contain usage data")

        return GenerateResponse(
            text=response.output_text,
            usage=Usage(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
            ),
        )
