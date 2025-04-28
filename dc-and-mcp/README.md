# Delimited continuations and MCP

## Idea

What usually MCP server do? Mostly, things with side-effects (I/O) thus impure (sometimes not safe).

How AI (agents?) can deal with then? One of the answers is to "delimit" them, so here are "Delimited continuations"

So user can conveniently control all impure stuff (IO) on its level, while prompting an AI-service with MCP support.


## Status

Not ready :)


## Usage

1. Install python, [uv](https://github.com/astral-sh/uv)
2. Get Anthropic API key: https://console.anthropic.com/settings/keys
    * save they in `.env` file (ignored for git): `ANTHROPIC_API_KEY=<KEY>`
3. Make sure that credit balance isn't too low to access the Anthropic API
4. Run client: `uv run client.py`
5. Example prompt: _TBD_


## References

* [MCP Quickstart guide (client)](https://modelcontextprotocol.io/quickstart/client)
* [Konstantin Nazarov: Purity, delimited continuations and I/O](https://knazarov.com/posts/purity_delimited_continuations_and_io/)
