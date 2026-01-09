# StyleGAN CLI MCP

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
