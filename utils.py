import inspect
import shutil
from pathlib import Path
from collections.abc import Iterable
from string.templatelib import Template, Interpolation, convert


def script_dir() -> Path:
	filename = inspect.stack()[1].filename
	return Path(filename).parent


def which(cmd: str) -> str:
	match shutil.which(cmd):
		case None:
			raise RuntimeError(f"Command not found: `{cmd}`")
		case path:
			return path


def iformat(interpolation: Interpolation, /) -> str:
	obj = convert(interpolation.value, interpolation.conversion)
	return format(obj, interpolation.format_spec)


def template_to_cmds(template: Template) -> list[str]:
	args: list[str] = []
	pre_continuation, post_interpolation = False, False
	for part in template:
		match part:
			case str() as static_part:
				cmds = build_cmds(static_part)
				continuation = ("\0" + static_part).split()[0] != "\0"
				if post_interpolation and continuation:
					args[-1] = args[-1] + cmds[0]
					args.extend(cmds[1:])
				else:
					args.extend(cmds)
				pre_continuation = (static_part + "\0").split()[-1] != "\0"
				post_interpolation = False
			case interpolation:
				fstr = iformat(interpolation)
				if pre_continuation:
					args[-1] = args[-1] + fstr
				else:
					args.append(fstr)
				post_interpolation = True
	return args


def build_cmds(*cmdline_or_arglist: str | Iterable[str] | Template) -> list[str]:
	args: list[str] = []
	for arg in cmdline_or_arglist:
		match arg:
			case Template() as template:
				args.extend(template_to_cmds(template))
			case str() as cmdline:
				cmds = cmdline.split()
				args.extend(cmds)
			case Iterable():
				args.extend(arg)
			case _:
				raise TypeError(f"Invalid argument: {arg!r}")
	return args
