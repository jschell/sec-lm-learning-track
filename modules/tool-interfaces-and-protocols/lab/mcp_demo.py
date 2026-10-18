"""Run the same proposals through a real local MCP subprocess and record messages.

The stream taps copy decoded SDK JSON-RPC messages, not raw byte framing.
No model, HTTP listener, credentials or remote server is used.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import asynccontextmanager
import json
from pathlib import Path
import sys
from typing import AsyncIterator, TextIO

from anyio.abc import ObjectReceiveStream, ObjectSendStream
from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.shared.message import SessionMessage

from contract import feedback_example, load_calls, write_json

HERE = Path(__file__).resolve().parent


class MessageLog:
    """Record at the SDK stream boundary; outgoing records are dispatch intent."""
    def __init__(self, path: Path) -> None:
        self.handle = path.open('x', encoding='utf-8')
        self.sequence = 0

    def record(self, direction: str, item: SessionMessage | Exception) -> None:
        self.sequence += 1
        value = ({'transport_error': str(item)} if isinstance(item, Exception)
                 else item.message.model_dump(mode='json', by_alias=True, exclude_none=True))
        self.handle.write(json.dumps({'seq': self.sequence, 'direction': direction, 'message': value}) + '\n')
        self.handle.flush()

    def close(self) -> None:
        self.handle.close()


class RecordedRead(ObjectReceiveStream[SessionMessage | Exception]):
    """Delegate reads and copy decoded messages without changing their content."""
    def __init__(self, stream: ObjectReceiveStream[SessionMessage | Exception], log: MessageLog) -> None:
        self.stream, self.log = stream, log

    async def receive(self) -> SessionMessage | Exception:
        item = await self.stream.receive()
        self.log.record('server_to_client', item)
        return item

    async def aclose(self) -> None:
        await self.stream.aclose()


class RecordedWrite(ObjectSendStream[SessionMessage]):
    """An outgoing record alone is not evidence that a function executed."""
    def __init__(self, stream: ObjectSendStream[SessionMessage], log: MessageLog) -> None:
        self.stream, self.log = stream, log

    async def send(self, item: SessionMessage) -> None:
        self.log.record('client_to_server', item)
        await self.stream.send(item)

    async def aclose(self) -> None:
        await self.stream.aclose()


@asynccontextmanager
async def recorded_stdio(parameters: StdioServerParameters, log: MessageLog, errlog: TextIO) -> AsyncIterator[tuple[RecordedRead, RecordedWrite]]:
    """Use SDK subprocess lifecycle; wrap only its decoded read/write streams."""
    async with stdio_client(parameters, errlog=errlog) as (read, write):
        yield RecordedRead(read, log), RecordedWrite(write, log)


async def run(output: Path) -> dict:
    """Start and close one server; preserve artifacts even when a request fails."""
    output.mkdir(parents=True, exist_ok=False)
    output = output.resolve()
    parameters = StdioServerParameters(command=sys.executable,
        args=[str(HERE / 'server.py'), '--audit', str(output / 'executions.jsonl')])
    log = MessageLog(output / 'messages.jsonl')
    calls = load_calls()
    try:
        with (output / 'server-stderr.txt').open('x', encoding='utf-8') as errors:
            async with Client(recorded_stdio(parameters, log, errors), cache=None,
                              read_timeout_seconds=5) as client:
                connection = {'protocol_version': client.protocol_version,
                              'server_info': client.server_info.model_dump(mode='json', by_alias=True) if client.server_info else None}
                definition = await client.list_tools()
                write_json(output / 'discovered-tools.json', definition.model_dump(mode='json', by_alias=True, exclude_none=True))
                rows = []
                for proposal in calls:
                    result = await client.call_tool(proposal['name'], proposal['arguments'])
                    rows.append({'proposal': proposal, 'outcome': result.structured_content,
                                 'mcp_result': result.model_dump(mode='json', by_alias=True, exclude_none=True)})
    finally:
        log.close()
    # This audit was written inside the separate server process, at function entry.
    executions = [json.loads(line) for line in (output / 'executions.jsonl').read_text(encoding='utf-8').splitlines()]
    report = {'mode': 'local stdio MCP; fixed calls, no model', 'connection': connection,
              'calls': rows, 'execution_count': len(executions)}
    write_json(output / 'report.json', report)
    write_json(output / 'feedback-example.json', feedback_example(calls[0], rows[0]['outcome']))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        report = asyncio.run(asyncio.wait_for(run(args.output), timeout=20))
    except Exception as exc:
        # Top-level CLI failure boundary, including SDK ExceptionGroups: retain the
        # original type/message and artifacts; never retry or manufacture results.
        print(f'MCP lab failed ({type(exc).__name__}): {exc}', file=sys.stderr)
        return 2
    print(f"Protocol {report['connection']['protocol_version']}; {len(report['calls'])} proposals; "
          f"{report['execution_count']} function entries. Artifacts: {args.output.resolve()}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
