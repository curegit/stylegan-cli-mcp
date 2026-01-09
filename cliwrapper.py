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
	assert which(cmdline[0])
	how_to_use = description
	if help:
		how_to_use += "\n\n" + help
	if help_command is not None:
		help_cmdline = build_cmds(help_command)
		help_result = run_command(help_cmdline)
		if help_result.return_code == 0:
			help_stdout = help_result.stdout
			if not help_stdout:
				raise RuntimeError(f"Help command returned empty output: {help_cmdline} -> {help_result}")
			how_to_use += "\n\n" + help_stdout
		else:
			raise RuntimeError(f"Failed to run help command: {help_cmdline} -> {help_result}")

	@mcp.tool(name=name, description=how_to_use)
	def cli_tool(args: list[str], stdin: str | None = None) -> CLIResult:
		return run_command(cmdline + args, stdin)
