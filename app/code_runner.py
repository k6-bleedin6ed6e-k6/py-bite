import ast
import subprocess
import sys
import tempfile
import os


# Blacklist of dangerous AST node types
FORBIDDEN_NODES = {
    "Import",
    "ImportFrom",
    "Delete",
    "With",
    "AsyncWith",
    "AsyncFor",
    "Try",
    "TryStar",
    "ClassDef",
    "FunctionDef",
    "AsyncFunctionDef",
    "Global",
    "Nonlocal",
    "Exec",
}

FORBIDDEN_BUILTINS = {
    "open",
    "eval",
    "exec",
    "compile",
    "__import__",
    "input",
    "raw_input",
    "exit",
    "quit",
}


def _check_ast_safety(source: str) -> tuple[bool, str]:
    """Basic AST-based safety check for simple expressions."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return False, f"Syntax error: {e}"

    for node in ast.walk(tree):
        node_type = type(node).__name__
        if node_type in FORBIDDEN_NODES:
            return False, f"Forbidden construct: {node_type}"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_BUILTINS:
                return False, f"Forbidden builtin: {node.func.id}"
    return True, ""


def run_code(source: str, mode: str = "safe") -> dict:
    """
    Execute Python code safely.

    mode='safe': AST-checked exec in isolated namespace (no I/O).
    mode='full':  Runs in a subprocess with timeout (allows prints, functions, etc).
    """
    result = {"stdout": "", "stderr": "", "success": False}

    if not source.strip():
        result["stderr"] = "No code provided."
        return result

    if mode == "safe":
        safe, msg = _check_ast_safety(source)
        if not safe:
            result["stderr"] = f"Security block: {msg}"
            return result

        namespace = {"__builtins__": {k: v for k, v in __builtins__.items() if k not in FORBIDDEN_BUILTINS}}
        try:
            exec(source, namespace)
            result["success"] = True
            result["stdout"] = "Code executed successfully. (Safe mode does not capture print output.)"
        except Exception as e:
            result["stderr"] = str(e)

    elif mode == "full":
        # Run in subprocess with timeout for true isolation
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(source)
                tmp_path = f.name

            proc = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True,
                text=True,
                timeout=5,
            )
            result["stdout"] = proc.stdout
            result["stderr"] = proc.stderr
            result["success"] = proc.returncode == 0
        except subprocess.TimeoutExpired:
            result["stderr"] = "Code execution timed out after 5 seconds."
        except Exception as e:
            result["stderr"] = str(e)
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
    else:
        result["stderr"] = f"Unknown mode: {mode}"

    return result
