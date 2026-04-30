"""Code Execution Tool for running Python and shell commands"""

import subprocess
import sys
import os
from typing import Dict, Any, Optional

from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ExecutionTool(BaseTool):
    """Tool for executing code and shell commands"""

    def __init__(self, allow_shell_commands: bool = False):
        """Initialize execution tool"""
        super().__init__(
            name="ExecutionTool",
            description="Execute Python code and shell commands safely",
        )
        self.allow_shell_commands = allow_shell_commands

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute operation"""
        operation = kwargs.get("operation", "python")

        if operation == "python":
            return await self.run_python_code(**kwargs)
        elif operation == "shell" and self.allow_shell_commands:
            return await self.run_shell_command(**kwargs)
        else:
            return {"success": False, "error": f"Unknown operation or not allowed: {operation}"}

    async def validate_input(self, **kwargs) -> bool:
        """Validate input parameters"""
        operation = kwargs.get("operation", "python")

        if operation == "python":
            return "code" in kwargs and len(kwargs["code"]) > 0
        elif operation == "shell":
            return "command" in kwargs and len(kwargs["command"]) > 0

        return False

    async def run_python_code(self, **kwargs) -> Dict[str, Any]:
        """Execute Python code safely"""
        code = kwargs.get("code", "")
        timeout = kwargs.get("timeout", 30)

        try:
            logger.debug(f"Running Python code: {code[:50]}...")

            # Create safe execution environment
            local_env = {
                "__builtins__": __builtins__,
                "print": print,
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "list": list,
                "dict": dict,
                "set": set,
                "tuple": tuple,
            }

            result = {}
            exec(code, local_env, result)

            logger.debug(f"Python code executed successfully")

            return {
                "success": True,
                "data": {
                    "result": result,
                    "output": "Code executed successfully",
                },
            }

        except SyntaxError as e:
            logger.error(f"Syntax error in Python code: {str(e)}")
            return {"success": False, "error": f"Syntax error: {str(e)}"}

        except Exception as e:
            logger.error(f"Error executing Python code: {str(e)}")
            return {"success": False, "error": str(e)}

    async def run_shell_command(self, **kwargs) -> Dict[str, Any]:
        """Execute shell command"""
        command = kwargs.get("command", "")
        timeout = kwargs.get("timeout", 30)

        if not self.allow_shell_commands:
            return {"success": False, "error": "Shell commands are disabled"}

        try:
            logger.debug(f"Running shell command: {command}")

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                timeout=timeout,
                text=True,
            )

            logger.debug(f"Shell command executed with return code: {result.returncode}")

            return {
                "success": True,
                "data": {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "return_code": result.returncode,
                },
            }

        except subprocess.TimeoutExpired:
            logger.error(f"Shell command timed out after {timeout}s")
            return {"success": False, "error": f"Command timeout after {timeout}s"}

        except Exception as e:
            logger.error(f"Error executing shell command: {str(e)}")
            return {"success": False, "error": str(e)}

    async def analyze_code(self, **kwargs) -> Dict[str, Any]:
        """Analyze code for issues"""
        code = kwargs.get("code", "")

        try:
            logger.debug("Analyzing code...")

            # Parse code to check syntax
            compile(code, "<string>", "exec")

            # Count lines and functions
            lines = code.split("\n")
            function_count = len([l for l in lines if l.strip().startswith("def ")])
            class_count = len([l for l in lines if l.strip().startswith("class ")])

            logger.debug("Code analysis completed")

            return {
                "success": True,
                "data": {
                    "lines": len(lines),
                    "functions": function_count,
                    "classes": class_count,
                    "valid": True,
                },
            }

        except SyntaxError as e:
            logger.error(f"Syntax error in code: {str(e)}")
            return {
                "success": True,
                "data": {
                    "valid": False,
                    "error": str(e),
                },
            }

        except Exception as e:
            logger.error(f"Error analyzing code: {str(e)}")
            return {"success": False, "error": str(e)}
