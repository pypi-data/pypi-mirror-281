from collections.abc import AsyncGenerator
from typing import Any, Literal, cast

from anthropic._types import NOT_GIVEN, NotGiven
from anthropic.types import MessageParam

from llm_taxi.clients.anthropic import Anthropic as AnthropicClient
from llm_taxi.conversation import Message, Role
from llm_taxi.llms.base import LLM


class Anthropic(AnthropicClient, LLM):
    def _convert_messages(self, messages: list[Message]) -> list[Any]:
        return [
            MessageParam(
                role=cast(Literal["user", "assistant"], message.role.value),
                content=message.content,
            )
            for message in messages
            if message.role in {Role.User, Role.Assistant}
        ]

    def _get_system_message_content(
        self,
        messages: list[Message],
    ) -> str | NotGiven:
        if message := next(
            (x for x in reversed(messages) if x.role == Role.System),
            NOT_GIVEN,
        ):
            return message.content

        return NOT_GIVEN

    async def _streaming_response(self, response):
        async for chunk in response:
            if chunk.type == "content_block_delta":
                yield chunk.delta.text

    async def streaming_response(
        self,
        messages: list[Message],
        max_tokens: int = 4096,
        **kwargs,
    ) -> AsyncGenerator:
        system_message = self._get_system_message_content(messages)
        messages = self._convert_messages(messages)

        response = await self.client.messages.create(
            system=system_message,
            messages=messages,
            stream=True,
            **self._get_call_kwargs(max_tokens=max_tokens, **kwargs),
        )

        return self._streaming_response(response)

    async def response(
        self,
        messages: list[Message],
        max_tokens: int = 4096,
        **kwargs,
    ) -> str:
        system_message = self._get_system_message_content(messages)
        messages = self._convert_messages(messages)

        response = await self.client.messages.create(
            system=system_message,
            messages=messages,
            **self._get_call_kwargs(max_tokens=max_tokens, **kwargs),
        )

        return response.content[0].text
