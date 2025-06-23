import ast
import os

def count_guard_clauses(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=filepath)

    guard_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            body = node.body
            if len(body) == 1:
                stmt = body[0]
                if isinstance(stmt, (ast.Return, ast.Raise, ast.Continue, ast.Break)):
                    guard_count += 1

    return guard_count

total_guards = 0
for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            total_guards += count_guard_clauses(path)

print(f"총 guard clause 수: {total_guards}")
