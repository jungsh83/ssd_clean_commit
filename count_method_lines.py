import os
import ast

def count_method_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=filepath)

    method_lengths = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if hasattr(node, 'body') and len(node.body) > 0:
                start = node.lineno
                end = node.body[-1].lineno
                method_lengths.append(end - start + 1)
    print(filepath)
    print(method_lengths)

    return method_lengths

all_lengths = []
for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            all_lengths.extend(count_method_lines(path))

print(f"총 메서드 수: {len(all_lengths)}")
print(f"평균 라인 수: {sum(all_lengths) / len(all_lengths):.2f}")
