# Custom Tools Reference

This directory (`tools/`) is the hot-reload zone for standalone user-defined tools. Any `.py` file placed here that defines a `SwarmTool` subclass will be auto-discovered by the `ToolRegistry` on startup.

## Adding a Custom Tool

1. Create a new file here, e.g. `my_custom_tool.py`.
2. Subclass `SwarmTool` from `backend.app.tools.base`:

```python
import os
import json
from backend.app.tools.base import SwarmTool

class MyCustomTool(SwarmTool):
    name = "MyCustomTool"
    description = "Does something amazing. Input: text. Output: JSON."

    async def _run(self, input: str) -> str:
        if os.getenv("MOCK_TOOLS") == "true":
            return json.dumps({"mocked": True})
        return json.dumps({"result": f"Processed: {input}"})
```

3. Restart the backend server — the tool will auto-register.

## Available Built-in Tools

| Tool Name | Description |
|---|---|
| `KeywordSearchTool` | Postgres full-text search |
| `VectorSearchTool` | ChromaDB semantic similarity |
| `WebSearchTool` | Serper.dev web search |
| `FileWriteTool` | Writes files to `/workspace` |
| `HttpActionTool` | Makes outbound HTTP requests |
| `CodeExecutionTool` | Executes sandboxed Python snippets |
| `SystemDiagnosticsTool` | Returns disk stats and health |
| `WeatherTool` | Returns mocked weather data |
| `CalculatorTool` | Evaluates arithmetic expressions |

## Notes

- All tools **must** include the `MOCK_TOOLS` guard for test compatibility.
- Tools placed here override same-named tools in `backend/app/tools/` (last wins).
