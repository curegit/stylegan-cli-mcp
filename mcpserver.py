#!/usr/bin/env python3

import sys
from textwrap import dedent, indent
from mcp.server.fastmcp import FastMCP
from cliwrapper import add_cli_tool
from utils import script_dir


python = sys.executable

name = "Precure StyleGAN ADA"

scripts = ["show.py", "generate.py", "combine.py", "mix.py", "animate.py"]


def build_instructions() -> str:
	readme_path = script_dir() / "core" / "README.md"
	with open(readme_path, "rb") as fp:
		readme = fp.read().decode()

	instructions = dedent(f'''\
	This is a MCP server wrapping the following CLI scripts: {scripts}.

	Please see the original README.md for more details to use these tools:
	"""
	{indent(readme, "\t").strip()}
	"""
	''')

	return instructions


def build_mcp() -> FastMCP:
	mcp = FastMCP(
		name=name,
		instructions=build_instructions(),
	)
	for script in scripts:
		script_path = str((script_dir() / "core" / script).resolve(strict=True))
		add_cli_tool(
			mcp,
			name=script,
			command=t"{python} {script_path}",
			help_command=t"{python} {script_path} -h",
		)
	return mcp


def main() -> int:
	mcp = build_mcp()
	mcp.run(transport="stdio")
	return 0


if __name__ == "__main__":
	sys.exit(main())
