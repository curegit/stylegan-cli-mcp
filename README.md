# StyleGAN CLI MCP

Experimental MCP server setup for the StyleGAN CLI tools

This is an experimental MCP server wrapping [Precure StyleGAN ADA](https://github.com/curegit/precure-stylegan-ada).
The aim of this project is to demonstrate abilities that MCP servers can wrap roughly arbitrary CLI tools approximately as organized tool definitions for LLMs.

## Setup

Python 3.14 or later is required.
Use the `requirements.txt` to install the minimal dependencies for serving and inferencing, including the dependencies of [Precure StyleGAN ADA](https://github.com/curegit/precure-stylegan-ada).

```sh
git clone --recursive https://github.com/curegit/stylegan-cli-mcp.git
cd stylegan-cli-mcp
pip3 install -r requirements.txt
```

## Run MCP Server

```sh
python3 mcpserver.py
```

## Test (`tools/list`)

```sh
python3 toolslist.py
```

## MCP Host Setup Example

### `mcp.json` (Cursor)

```json
{
  "mcpServers": {
    "stylegan": {
      "command": "./venv/bin/python3",
      "args": ["-B", "${workspaceFolder}/mcpserver.py"]
    }
  }
}
```

## License

[CC BY-NC 4.0](LICENSE)
