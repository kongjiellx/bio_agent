# -*-coding: utf-8 -*-
from openai import OpenAI
import sys

client = OpenAI()
model = "gpt-4-1106-preview"


def call_openai_stream(msgs, functions=None, function_call="auto"):
    params = {}
    if functions:
        params["functions"] = functions
        params["function_call"] = function_call
    # print(msgs)
    response = client.chat.completions.create(
        model=model,
        messages=msgs,
        stream=True,
        **params,
    )
    function_call = {"name": "", "arguments": ""}
    for chunk in response:
        if not chunk.choices:
            continue
        chunk_message = chunk.choices[0]
        delta = chunk_message.delta
        if chunk_message.finish_reason and chunk_message.finish_reason not in ("stop", "function_call"):
            sys.stderr.write(f"[WARN] finish reason is {chunk_message.finish_reason}")
            sys.stderr.flush()
        if chunk_message.finish_reason == "stop":
            if function_call["name"]:
                yield function_call
        elif chunk_message.finish_reason == "function_call":
            # print(function_call)
            yield function_call
        elif not chunk_message.finish_reason:
            if delta.function_call:
                func = delta.function_call
                if func.name:
                    function_call["name"] += func.name
                if func.arguments:
                    function_call["arguments"] += func.arguments
            else:
                if delta.content:
                    yield delta.content


def call_openai(msgs, functions=None, function_call="auto"):
    params = {}
    if functions:
        params["functions"] = functions
        params["function_call"] = function_call
    response = client.chat.completions.create(
        model=model,
        messages=msgs,
        **params,
    )
    message = response.choices[0].message
    if message.function_call:
        return dict(name=message.function_call.name, arguments=message.function_call.arguments)
    else:
        return message["content"]


if __name__ == "__main__":
    print(call_openai(
            [{"role": "user", "content": "你好"}],
        [{
            "name": "test_function",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "请假信"
                    }
                },
                "required": ["content"],
            },
        }],
            {"name": "test_function"}
    ))
    # for c in call_openai_stream(
    #         [{"role": "user", "content": "你好"}],
    #     [{
    #         "name": "test_function",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "content": {
    #                     "type": "string",
    #                     "description": "请假信"
    #                 }
    #             },
    #             "required": ["content"],
    #         },
    #     }],
    #         {"name": "test_function"}
    # ):
    #     print(c)