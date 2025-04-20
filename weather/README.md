# Weather example server

## Installation

1. Install python, [uv](https://github.com/astral-sh/uv)
    * Get full path to `uv`: `which uv`
2. Configure Claude Desktop (on macOS, the config file path usually is `~/Library/Application\ Support/Claude/claude_desktop_config.json`)

```json
{
    "mcpServers": {
        "weather": {
            "command": "/path/to/uv",
            "args": [
                "--directory",
                "/path/to/learning-mcp-repo/learning-mcp/weather",
                "run",
                "weather.py"
            ]
        }
    }
}
```

3. Restart Claude Desktop app
    * make sure there aren't any errors
4. Example prompt: `What’s the weather in Palo Alto, CA?`


## References

* [MCP Quickstart guide (server)](https://modelcontextprotocol.io/quickstart/server)
