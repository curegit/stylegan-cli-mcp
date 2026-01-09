import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from cliwrapper import add_cli_tool

python = sys.executable

scripts = ["generate.py", "combine.py", "mix.py", "animate.py"]

with open(Path(__file__).parent / "core" / "README.md", "rb") as fp:
	readme = fp.read().decode()
readme = f"""
This is MCP Server wrapping following CLI scripts:
{scripts}

Please see the original README for more details:
{readme}
"""



mcp = FastMCP(
	name="Tool Example",
	instructions=readme,
)


for script in scripts:
	script_path = str((Path(__file__).parent / "core" / script).resolve())
	add_cli_tool(
		mcp,
		script,
		t"{python} {script_path}",
		help_command=t"{python} {script_path} -h"
	)


def main() -> int:
	mcp.run(transport='stdio')
	return 0


if __name__ == "__main__":
	sys.exit(main())
