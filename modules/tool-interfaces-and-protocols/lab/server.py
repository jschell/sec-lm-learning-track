"""One local stdio MCP tool, backed by the exact same dispatcher as direct.py."""
import argparse
import asyncio
import json
from pathlib import Path

import mcp_types as types
from mcp.server import Server
from mcp.server.context import ServerRequestContext
from mcp.server.stdio import stdio_server

from contract import DEFINITION, EventLookup, dispatch


def make_server(lookup: EventLookup) -> Server:
    """Keep validation visible instead of relying on inferred/coercing arguments."""
    async def list_tools(ctx: ServerRequestContext, params: types.PaginatedRequestParams | None) -> types.ListToolsResult:
        return types.ListToolsResult(tools=[types.Tool(**DEFINITION)])

    async def call_tool(ctx: ServerRequestContext, params: types.CallToolRequestParams) -> types.CallToolResult:
        outcome = dispatch(lookup, params.name, params.arguments)
        error = outcome['status'] in {'invalid_arguments', 'unknown_tool', 'execution_error'}
        return types.CallToolResult(content=[types.TextContent(type='text', text=json.dumps(outcome))],
                                    structured_content=outcome, is_error=error)

    return Server('synthetic-event-lookup', version='1', on_list_tools=list_tools, on_call_tool=call_tool)


async def serve(audit: Path) -> None:
    """Run one explicitly launched subprocess; stdout is reserved for protocol."""
    server = make_server(EventLookup(audit))
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit', required=True, type=Path)
    asyncio.run(serve(parser.parse_args().audit))
