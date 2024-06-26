import itertools
from collections.abc import AsyncGenerator
from typing import Any, ClassVar

from llm_taxi.clients.google import Google as GoogleClient
from llm_taxi.conversation import Message, Role
from llm_taxi.llms.base import LLM


class Google(GoogleClient, LLM):
    call_kwargs_mapping: ClassVar[dict[str, str]] = {
        "max_tokens": "max_output_tokens",
    }

    def _convert_messages(self, messages: list[Message]) -> list[Any]:
        role_mappping = {
            Role.System: "user",
            Role.User: "user",
            Role.Assistant: "model",
        }
        groups = itertools.groupby(
            messages,
            key=lambda x: role_mappping[Role(x.role)],
        )

        return [
            {
                "role": role,
                "parts": [x.content for x in parts],
            }
            for role, parts in groups
        ]

    async def _streaming_response(self, response):
        async for chunk in response:
            yield chunk.text

    def _get_call_kwargs(self, **kwargs) -> dict:
        kwargs = super()._get_call_kwargs(**kwargs)

        if self.call_kwargs_mapping:
            return {self.call_kwargs_mapping.get(k, k): v for k, v in kwargs.items()}

        return kwargs

    async def streaming_response(
        self,
        messages: list[Message],
        **kwargs,
    ) -> AsyncGenerator:
        from google import generativeai as genai

        messages = self._convert_messages(messages)

        response = await self.client.generate_content_async(
            messages,
            stream=True,
            generation_config=genai.types.GenerationConfig(
                **self._get_call_kwargs(**kwargs),
            ),
        )

        return self._streaming_response(response)

    async def response(self, messages: list[Message], **kwargs) -> str:
        from google import generativeai as genai

        messages = self._convert_messages(messages)

        response = await self.client.generate_content_async(
            messages,
            generation_config=genai.types.GenerationConfig(
                **self._get_call_kwargs(**kwargs),
            ),
        )

        return response.text
