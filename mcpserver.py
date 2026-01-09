import sys
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

	instructions = f'''
	This is a MCP server wrapping the following CLI scripts: {scripts}.

	Please see the original README.md for more details:
	"""
	{readme}
	"""
	'''

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
			help_command=t"{python} {script_path} -h"
		)
	return mcp


def main() -> int:
	mcp = build_mcp()
	mcp.run(transport="stdio")
	return 0


if __name__ == "__main__":
	sys.exit(main())
