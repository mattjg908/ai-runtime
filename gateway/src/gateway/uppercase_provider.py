from .models import (
    GenerateRequest,
    GenerateResponse,
    Usage,
)


class UppercaseProvider:
    async def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        return GenerateResponse(
            text=request.prompt.upper(),
            usage=Usage(
                input_tokens=0,
                output_tokens=0,
            ),
        )
