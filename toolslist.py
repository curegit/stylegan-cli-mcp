import sys
import subprocess as sp
from utils import script_dir, build_cmds


python = sys.executable

stdin = """{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"python-client","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
"""


def main() -> int:
	mcpserver = script_dir() / "mcpserver.py"
	sp.run(build_cmds(t"{python} {mcpserver}"), input=stdin, text=True, check=True)
	return 0


if __name__ == "__main__":
	sys.exit(main())
