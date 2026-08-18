"""
Code Execution Tool - DISABLED FOR SECURITY
WARNING: This tool is DISABLED due to security risks.
Code execution should be done in isolated containers (Docker/gVisor).
"""

from crewai.tools import tool


@tool("CodeExecutionTool")
class CodeExecutionTool:
    """
    Executes Python code snippets.
    
    WARNING: This tool is currently DISABLED for security reasons.
    To enable, implement proper sandboxing with Docker or gVisor.
    """
    
    def _run(self, code: str) -> str:
        raise NotImplementedError(
            "Code execution tool is disabled for security reasons. "
            "To enable, implement a sandboxed container environment."
        )
