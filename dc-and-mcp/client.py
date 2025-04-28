import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

import re

load_dotenv()  # load environment variables from .env

# Example MCP client from the guide
class StdioMCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.tools = []

    async def connect_to_server(self, cwd, cmd, cmd_args=[]) -> list:
        server_params = StdioServerParameters(
            command=cmd,
            args=cmd_args,
            cwd=cmd,
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        response = await self.session.list_tools()
        self.tools = response.tools
        # print("\nConnected to server with tools:", [tool.name for tool in self.tools])
        return self.tools

    def have_the_tool(tool_name) -> bool:
        return tool_name in [tool.name for tool in self.tools]

    async def process_tool(tool_name, tool_args) -> str:
        result = await self.session.call_tool(tool_name, tool_args)

        return result.content


# Simple dummy Claude client with no tools
class ClaudeClient:
    def __init__(self):
        self.anthropic = Anthropic()


    async def process_query(self, query: str, tools=[]) -> str:
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=tools
        )

        final_text = [content.text for content in response.content]
        return "\n".join(final_text)


async def main():
    claude_client = ClaudeClient()

    all_tools = []

    # describe_tool_pattern = r'^/describe_tool\s+(.+)'
    # enable_tool_pattern = r'^/enable_tool\s+(stdio|generate)\s+(.+)'
    # delete_tool_pattern = r'^/disable_tool\s+(.+)'

    cmd_with_args_pattern = r'^/(describe|enable|disable)_tool\s+(.+)'
    enable_tool_args_pattern = r'^(stdio|generate)\s+(.+)'

    # TODO: Garbage collection for stdio processes


    print("\nSimple dummy Claude client Started!")
    print("Type your queries or '/quit' to exit.")
    while True:
        try:
            query = input("\nQuery: ").strip()

            lower_query = query.lower()

            if lower_query == '/quit':
                break

            if lower_query == '/list_tools'
                print("\n".join([tool.name for tool in all_tools]))
                continue

            match = re.search(cmd_with_args_pattern, lower_query)
            cmd = match.group(1)
            cmd_args = match.group(2)

            if cmd == 'describe':
                found = [tool for tool in all_tools if tool.name == cmd_args]
                if len(found) > 0:
                    print(found[0])
                else:
                    print(f"Tool with name \"{cmd_args}\" not found")
                continue


            # TODO: if cmd == 'enable':
            # TODO: if cmd == 'disable'



            response = await claude_client.process_query(query)
            print("\n" + response)

        except Exception as e:
            print(f"\nError: {str(e)}")


	# print("Hello!")
    # client = MCPClient()
    # try:
    #     await client.connect_to_server(sys.argv[1])
    #     await client.chat_loop()
    # finally:
    #     await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())