import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

import re
import json

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
            cwd=cwd,
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await asyncio.wait_for(self.session.initialize(), timeout=10)

        response = await self.session.list_tools()
        self.tools = response.tools
        # print("\nConnected to server with tools:", [tool.name for tool in self.tools])
        return self.tools

    def have_the_tool(self, tool_name) -> bool:
        return tool_name in [tool.name for tool in self.tools]

    async def process_tool(self, tool_name, tool_args) -> str:
        result = await self.session.call_tool(tool_name, tool_args)
        return result.content

    async def cleanup(self):
        await self.exit_stack.aclose()


# Simple dummy Claude client with no tools
class ClaudeClient:
    def __init__(self):
        self.anthropic = Anthropic()
        self.messages = []

    def append_to_messages(self, message):
        self.messages.append(message)

    def flush_messages(self):
        self.messages.clear()

    async def process_query(self, tools=[]) -> str:
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in tools]

        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=self.messages,
            tools=available_tools
        )

        return response.content

        # final_text = [content.text for content in response.content]
        # return "\n".join(final_text)



async def main():
    claude_client = ClaudeClient()
    all_tools = dict()
    stdio_clients = []

    tools_pattern = r'^/(describe|generate|call)_tool\s+([a-z_]+)(\s+.+)?'
    call_tool_arg_pattern = r'([a-z_]+)(:number)?=(.+)'
    launch_stdio_pattern = r'^/launch_stdio\s(.+)'
    args_delimeter = r'(?<!\\)\s+'

    print("\nSimple dummy Claude client Started!")
    print("Type your queries or '/quit' to exit.")
    try:
        while True:
            try:
                query = input("\nQuery: ").strip()

                lower_query = query.lower()

                if lower_query == '':
                    continue

                if lower_query == '/quit':
                    break

                if lower_query == '/list_tools':
                    print("\n".join(all_tools.keys()))
                    continue

                tools_match = re.search(tools_pattern, lower_query)

                if tools_match:
                    tools_cmd = tools_match.group(1)
                    tools_args = [tools_match.group(2), tools_match.group(3)]

                    if tools_cmd == 'describe':
                        if tools_args[0] in all_tools:
                            print("name:")
                            print(tools_args[0])
                            print("description:")
                            print(all_tools[tools_args[0]].description)
                            print("inputSchema:")
                            print(json.dumps(all_tools[tools_args[0]].inputSchema, indent=2))
                        else:
                            print(f"Tool with name \"{tools_args[0]}\" not found")

                    if tools_cmd == "call":
                        if tools_args[0] in all_tools:
                            call_input = dict()
                            call_tool_args = re.split(args_delimeter, tools_args[1].strip())
                            for call_tool_arg in call_tool_args:
                                call_tool_arg_match = re.search(call_tool_arg_pattern, call_tool_arg)
                                if call_tool_arg_match:
                                    input_name = call_tool_arg_match.group(1)
                                    input_value = call_tool_arg_match.group(3)
                                    if call_tool_arg_match.group(2):
                                        if "." in input_value:
                                            call_input[input_name] = float(input_value)
                                        else:
                                            call_input[input_name] = int(input_value)
                                    else:
                                        call_input[input_name] = input_value
                                else:
                                    print(f"\"{call_tool_arg}\" cannot be parsed for tool call input")

                            found_stdio_client = None
                            for stdio_client_elem in stdio_clients:
                                if stdio_client_elem.have_the_tool(tools_args[0]):
                                    found_stdio_client = stdio_client_elem
                                    break

                            if found_stdio_client:
                                result = await found_stdio_client.process_tool(tools_args[0], call_input)
                                print("type:")
                                print(result.type)
                                print("text:")
                                print(result.text)
                                print("annotations:")
                                print(result.annotations)
                            else:
                                print("No suitable stdio client found")

                        else:
                            print(f"Tool with name \"{tools_args[0]}\" not found")

                    if tools_cmd == "generate":
                        print("Tool generation is not supported yet :)")

                    continue

                launch_stdio_match = re.search(launch_stdio_pattern, lower_query)

                if launch_stdio_match:
                    launch_stdio_args = re.split(args_delimeter, launch_stdio_match.group(1))

                    if len(launch_stdio_args) < 2:
                        print("/launch_stdio command requires at least two additional agruments for stdio: /launch_stdio CWD CMD [CMD_ARG...]")
                    else:
                        new_stdio_client = StdioMCPClient()
                        try:
                            new_tools = await new_stdio_client.connect_to_server(launch_stdio_args[0], launch_stdio_args[1], launch_stdio_args[2:])
                            for new_tool in new_tools:
                                if new_tool.name in all_tools:
                                    raise Exception(f"Tool #{new_tool.name} is already exists")

                            for new_tool in new_tools:
                                all_tools[new_tool.name] = new_tool

                            stdio_clients.append(new_stdio_client)

                        except Exception as e:
                            print(f"Error occurred: {e}")
                            await new_stdio_client.cleanup()

                    continue

                # print(f"You're typed \"{lower_query}\"")
                # print("User prompts not supported yet :)")
                claude_client.append_to_messages({
                    "role": "user",
                    "content": query
                })
                response = await claude_client.process_query(all_tools.values())
                print("response:")
                print(response)
                # print(json.dumps(response, indent=2))
                claude_client.flush_messages()







            except Exception as e:
                print(f"\nError: {str(e)}")

    finally:
        for client in stdio_clients:
            await client.cleanup()


if __name__ == "__main__":
    import sys
    asyncio.run(main())