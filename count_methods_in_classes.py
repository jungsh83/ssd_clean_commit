import os
import ast
from collections import defaultdict

def count_methods_in_classes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=filepath)

    class_methods = defaultdict(int)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            method_count = sum(isinstance(child, ast.FunctionDef) for child in node.body)
            class_methods[f"{os.path.basename(filepath)}::{node.name}"] += method_count

    return class_methods

all_class_method_counts = defaultdict(int)

for root, _, files in os.walk("src"):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            class_method_counts = count_methods_in_classes(path)
            for class_name, count in class_method_counts.items():
                all_class_method_counts[class_name] += count

# 출력
print("📦 클래스별 메서드 수:")
for class_name, count in all_class_method_counts.items():
    print(f"{class_name}: {count}개")

# 평균 계산
if all_class_method_counts:
    total_classes = len(all_class_method_counts)
    total_methods = sum(all_class_method_counts.values())
    print(f"\n총 클래스 수: {total_classes}")
    print(f"총 메서드 수: {total_methods}")
    print(f"클래스당 평균 메서드 수: {total_methods / total_classes:.2f}")
else:
    print("클래스를 찾을 수 없습니다.")
