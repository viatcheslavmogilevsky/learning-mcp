# Docker MCP server

## Installation with lima 

1. Install python, [uv](https://github.com/astral-sh/uv), [lima](https://github.com/lima-vm/lima)
    * Get full path to `uvx`: `which uvx`
2. Launch lima vm instance with docker runtime, for example: `limactl start --name=docker-runtime --tty=false --disk=32 template://docker`
    * Get docker runtime's sock path, for example: `unix:///HOME-DIR/.lima/docker-runtime/sock/docker.sock`
3. Configure Claude Desktop (on macOS, the config file path usually is `~/Library/Application\ Support/Claude/claude_desktop_config.json`):

```json
{
    "mcpServers": {
        "mcp-server-docker": {
            "command": "/path/to/uvx",
            "args": [
                "mcp-server-docker",
            ],
            "env": {
                "DOCKER_HOST": "unix:///HOME-DIR/.lima/docker-runtime/sock/docker.sock"
            }
        }
    }
}
```

4. Restart Claude Desktop app
    * make sure there aren't any errors
4. Example prompt: `Launch a nginx docker container`

## References

* [Docker MCP server](https://github.com/ckreiling/mcp-server-docker)
