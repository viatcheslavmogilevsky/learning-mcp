# MCP client example

## Usage

1. Install python, [uv](https://github.com/astral-sh/uv)
2. Get Anthropic API key: https://console.anthropic.com/settings/keys
    * save they in `.env` file (ignored for git): `ANTHROPIC_API_KEY=<KEY>`
3. Make sure that credit balance isn't too low to access the Anthropic API
4. Run client with `../weather` as MCP server: `uv run client.py ../weather/weather.py`
5. Example prompt: `What’s the weather in Palo Alto, CA?`


## References

* [MCP Quickstart guide (client)](https://modelcontextprotocol.io/quickstart/client)
