import ast
from collections import defaultdict
from pathlib import Path

def extract_function_bodies(file_path: Path):
    try:
        source = file_path.read_text(encoding='utf-8')
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
        return []

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    bodies = []
    for func in functions:
        try:
            body_src = ast.unparse(func)
            bodies.append((func.name, body_src.strip()))
        except Exception:
            continue
    return bodies

def scan_directory(directory: Path):
    code_map = defaultdict(list)
    for file_path in directory.rglob("*.py"):
        funcs = extract_function_bodies(file_path)
        for func_name, body in funcs:
            code_map[body].append(f"{file_path}::{func_name}")
    return code_map

# src/analyzer 기준 → src/
SRC_DIR = Path(__file__).resolve().parent.parent

dups = scan_directory(SRC_DIR)
print("🔁 중복 함수:")
for body, locations in dups.items():
    if len(locations) > 1:
        print(f"\n📌 중복된 코드 블록:\n{body[:100]}...\n↪ 위치:")
        for loc in locations:
            print(" -", loc)
