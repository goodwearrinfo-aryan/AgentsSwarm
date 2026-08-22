import os
import json
import shutil
from backend.app.tools.base import SwarmTool

class SystemDiagnosticsTool(SwarmTool):
    name = "SystemDiagnosticsTool"
    description = "Provides diagnostics regarding disk space and directory stats. Input: path to analyze. Output: JSON summary of space info."

    async def _run(self, input: str) -> str:
        if os.getenv("MOCK_TOOLS", "false").lower() == "true":
            return json.dumps({
                "disk_total_gb": 512.0,
                "disk_free_gb": 256.0,
                "path_queried": input,
                "status": "Healthy"
            })
        
        path = input if input else "."
        if not os.path.exists(path):
            return json.dumps({"error": f"Path '{path}' does not exist."})
            
        try:
            total, used, free = shutil.disk_usage(path)
            return json.dumps({
                "disk_total_gb": round(total / (2**30), 2),
                "disk_used_gb": round(used / (2**30), 2),
                "disk_free_gb": round(free / (2**30), 2),
                "path_queried": os.path.abspath(path),
                "status": "Healthy"
            })
        except Exception as e:
            return json.dumps({"error": str(e)})
