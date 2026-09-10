import ast


async def analyze_python_code(code: str) -> str:
    try:
        tree = ast.parse(code)
        lines = code.split("\n")
        total_lines = len(lines)

        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        func_names = [f.name for f in functions]
        class_names = [c.name for c in classes]

        imports = await extract_imports(code)
        complexity = await count_complexity(code)

        output = f"Code Analysis:\n"
        output += f"  Total lines: {total_lines}\n"
        output += f"  Functions: {len(functions)} ({', '.join(func_names) if func_names else 'none'})\n"
        output += f"  Classes: {len(classes)} ({', '.join(class_names) if class_names else 'none'})\n"
        output += f"  Imports: {len(imports)}\n"
        output += f"  Cyclomatic complexity: {complexity}\n"
        return output
    except SyntaxError as e:
        return f"Syntax error in code: {str(e)}"
    except Exception as e:
        return f"Error analyzing code: {str(e)}"


async def extract_imports(code: str) -> list[str]:
    try:
        tree = ast.parse(code)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        imports.append(f"{node.module}.{alias.name}")
        return imports
    except SyntaxError:
        return []
    except Exception:
        return []


async def count_complexity(code: str) -> int:
    try:
        tree = ast.parse(code)
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity
    except SyntaxError:
        return 0
    except Exception:
        return 0
