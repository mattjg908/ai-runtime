from .models import (
    GenerateRequest,
    GenerateResponse,
    Usage,
)


class FakeProvider:
    def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        return GenerateResponse(
            text=f"Echo: {request.prompt}",
            usage=Usage(
                input_tokens=0,
                output_tokens=0,
            ),
        )
