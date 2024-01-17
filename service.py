import bentoml

from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams
from typing import Optional, AsyncGenerator, List

SAMPLING_PARAM = SamplingParams(max_tokens=4096)
ENGINE_ARGS = AsyncEngineArgs(model='meta-llama/Llama-2-7b-chat-hf')

@bentoml.service(workers=1, resources={"gpu": "1"})
class VLLMService:
    def __init__(self) -> None:
        self.engine = AsyncLLMEngine.from_engine_args(ENGINE_ARGS)
        self.request_id = 0

    @bentoml.api
    async def generate(self, prompt: str = "Explain superconductors like I'm five years old", tokens: Optional[List[int]] = None) -> AsyncGenerator[str, None]:
        stream = await self.engine.add_request(self.request_id, prompt, SAMPLING_PARAM, prompt_token_ids=tokens)
        self.request_id += 1
        async for request_output in stream:
            yield request_output.outputs[0].text
