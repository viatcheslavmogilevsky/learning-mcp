# Weather example server

## Installation

1. Install python, uv
2. Configure Claude Desktop (on macOS, the config file path usually is `~/Library/Application\ Support/Claude/claude_desktop_config.json`)

config example:

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
