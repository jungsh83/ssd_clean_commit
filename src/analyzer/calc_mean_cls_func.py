import os
import ast
import subprocess
import re
from pathlib import Path

# src/analyzer/a.py → src/
SRC_DIR = Path(__file__).resolve().parent.parent


def get_all_py_files(directory: Path):
    """재귀적으로 .py 파일 찾기"""
    return [f for f in directory.rglob("*.py") if f.is_file()]


def count_functions_and_classes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        func_count = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
        class_count = sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
        print(f"{str(file_path):<60} | Classes: {class_count:<3} | Functions: {func_count:<3}")
        return func_count, class_count
    except Exception as e:
        print(f"{str(file_path):<60} | Error parsing AST: {e}")
        return 0, 0


def parse_radon_lloc():
    result = subprocess.run(["radon", "raw", str(SRC_DIR)], capture_output=True, text=True)
    llocs = [int(m.group(1)) for m in re.finditer(r'LLOC:\s+(\d+)', result.stdout)]
    return sum(llocs)


def calculate_avg_length_per_func_or_class():
    total_lloc = parse_radon_lloc()
    py_files = get_all_py_files(SRC_DIR)
    total_funcs, total_classes = 0, 0

    print("\n[파일별 클래스/함수 수]")
    print("-" * 80)
    for f in py_files:
        funcs, classes = count_functions_and_classes(f)
        total_funcs += funcs
        total_classes += classes
    total_entities = total_funcs + total_classes
    print("-" * 80)
    print(f"총 함수 수: {total_funcs}")
    print(f"총 클래스 수: {total_classes}")
    print(f"총 LLOC: {total_lloc}")
    print(f"함수/클래스 평균 길이 (LLOC 기준): {total_lloc / total_entities:.2f}" if total_entities > 0 else "측정 불가")


if __name__ == "__main__":
    calculate_avg_length_per_func_or_class()
