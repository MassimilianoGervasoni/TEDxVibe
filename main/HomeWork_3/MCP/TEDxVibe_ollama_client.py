import asyncio
import httpx
import json
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

OLLAMA_URL = "http://localhost:11434/api/chat"
MCP_URL = "https://54.92.197.147:8443/mcp"

async def main():
    async with streamablehttp_client(
        MCP_URL,
        httpx_client_factory=lambda **kwargs: httpx.AsyncClient(
            verify=False, **kwargs)
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()

            ollama_tools = []
            for t in tools.tools:
                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema
                    }
                })

            user_message = "Ho bisogno di motivazione prima della partita di calcio, consigliami 3 talk TED"
            print(f"\nUser: {user_message}\n")

            response = httpx.post(OLLAMA_URL, json={
                "model": "llama3.1",
                "messages": [{"role": "user", "content": user_message}],
                "tools": ollama_tools,
                "stream": False
            }, timeout=180)

            msg = response.json()["message"]

            if msg.get("tool_calls"):
                for tool_call in msg["tool_calls"]:
                    name = tool_call["function"]["name"]
                    args = tool_call["function"]["arguments"]
                    print(f"Ollama calls MCP tool: {name}({args})\n")

                    result = await session.call_tool(name, args)
                    tool_result = result.content[0].text

                    final = httpx.post(OLLAMA_URL, json={
                        "model": "llama3.1",
                        "messages": [
                            {"role": "user", "content": user_message},
                            {"role": "assistant", "content": "",
                             "tool_calls": msg["tool_calls"]},
                            {"role": "tool", "content": tool_result}
                        ],
                        "stream": False
                    }, timeout=180)
                    print(f"Ollama: {final.json()['message']['content']}")
            else:
                print(f"Ollama: {msg['content']}")

asyncio.run(main())