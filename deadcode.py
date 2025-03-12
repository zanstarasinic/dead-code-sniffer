# deadcode.py
import ast
import argparse
import os
from colorama import Fore, Style, init


class Sniffer(ast.NodeVisitor):
    def __init__(self):
        self.defined = {}  # {name: line_number}
        self.used = set()

    def visit_FunctionDef(self, node):
        self.defined[node.name] = node.lineno
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined[node.id] = node.lineno
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        for name in node.names:
            self.defined[name.name.split('.')[0]] = node.lineno
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for name in node.names:
            self.defined[name.name] = node.lineno
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            self.used.add(node.value.id)
        self.generic_visit(node)

    def get_unused(self):
        return {name: line for name, line in self.defined.items() if name not in self.used}


def scan_file(file_path):
    try:
        with open(file_path, "r") as f:
            code = f.read()
        tree = ast.parse(code)
        sniffer = Sniffer()
        sniffer.visit(tree)
        return sniffer.get_unused()
    except SyntaxError:
        print(Fore.RED, f"Skipping {file_path}: Invalid syntax")
        return {}
    except FileNotFoundError:
        print(Fore.RED, f"Skipping {file_path}: File not found")
        return {}

def scan_path(path):
    results = {}
    if os.path.isfile(path) and path.endswith(".py"):
        unused = scan_file(path)
        if unused:
            results[path] = unused
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":  # Skip __init__.py
                    file_path = os.path.join(root, file)
                    unused = scan_file(file_path)
                    if unused:
                        results[file_path] = unused
    return results

def generate_report(results):
    init(autoreset=True)
    if not results:
        print(Fore.GREEN + "No dead code found.")
        return
    print("Dead Code Sniffer Report:")
    for file_path in sorted(results.keys()):
        print(Style.BRIGHT + f"\n{file_path}:")
        for name, line in sorted(results[file_path].items(), key=lambda x: x[1]):
            print(f"  Line {line}: '{name}' is unused")
    print("\nConsider reviewing these for removal.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect unused code in Python files")
    parser.add_argument("path", help="File or folder to scan")
    parser = argparse.ArgumentParser(
    description="Detect unused code in Python files",
    epilog="Example: python sniffer.py myproject/")
    args = parser.parse_args()
    results = scan_path(args.path)
    generate_report(results)




