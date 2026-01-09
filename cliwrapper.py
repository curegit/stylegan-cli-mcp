import subprocess as sp
from dataclasses import dataclass
from collections.abc import Iterable
from string.templatelib import Template
from mcp.server.fastmcp import FastMCP
from utils import which, build_cmds


@dataclass(frozen=True, kw_only=True)
class CLIResult:
	stdout: str
	stderr: str
	return_code: int


def run_command(command: list[str], stdin: str | None = None) -> CLIResult:
	result = sp.run(command, input=stdin, capture_output=True, text=True, check=False)
	return CLIResult(stdout=result.stdout, stderr=result.stderr, return_code=result.returncode)


def add_cli_tool(
	mcp: FastMCP,
	name: str,
	command: str | Iterable[str] | Template,
	description: str = "",
	help: str = "",
	help_command: str | Iterable[str] | Template | None = None,
) -> None:
	cmdline = build_cmds(command)
	which(cmdline[0])
	description_ = description + help
	if help_command is not None:
		help_command_ = build_cmds(help_command)
		r = run_command(help_command_)
		if r.return_code == 0:
			description_ += "\n\n" + r.stdout
		else:
			raise RuntimeError(f"Failed to run help command: {help_command_}")

	@mcp.tool(name=name, description=description_)
	def cli_tool(args: list[str], stdin: str | None = None) -> CLIResult:
		return run_command(cmdline + args, stdin)
