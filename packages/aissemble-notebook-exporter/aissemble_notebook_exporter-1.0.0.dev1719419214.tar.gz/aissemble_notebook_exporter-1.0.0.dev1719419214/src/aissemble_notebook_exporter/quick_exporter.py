###
# #%L
# Marimo Notebook
# %%
# Copyright (C) 2021 Booz Allen
# %%
# All Rights Reserved. You may not copy, reproduce, distribute, publish, display,
# execute, modify, create derivative works of, transmit, sell or offer for resale,
# or in any way exploit any part of this solution without Booz Allen Hamilton’s
# express written permission.
# #L%
###
import ast
import astor
import argparse

# =============================================================================
# This script provides the capabilities for extracting functions and imports
# (e.g. excluding inline code)
# from a Marimo notebook, so it can be used by an aiSSEMBLE pipeline
# HOW TO USE: (from the commandline)
# python quick_exporter.py <SOURCE>.py <TARGET>.py
# =============================================================================


def copy_function_defs_and_imports(node):
    clean_node = ast.Module(body=[], type_ignores=[])

    # Recursively copy only FunctionDef nodes and import statements
    for stmt in node.body:
        if isinstance(stmt, (ast.FunctionDef, ast.Import, ast.ImportFrom)):
            clean_node.body.append(stmt)
        elif isinstance(
            stmt,
            (
                ast.If,
                ast.For,
                ast.While,
                ast.With,
                ast.Try,
                ast.ClassDef,
                ast.AsyncFunctionDef,
            ),
        ):
            clean_node.body.extend(copy_function_defs_and_imports(stmt).body)

    return clean_node


def fix_ast_locations(node):
    # Required by the ast package to fix the line numbers in the tree
    for child in ast.walk(node):
        if isinstance(child, ast.AST):
            ast.fix_missing_locations(child)
    return node


def clean_export_file(source, target):
    with open(source, "r") as source_file:
        tree = ast.parse(source_file.read())

        functiondefs_and_exports_ast = copy_function_defs_and_imports(tree)
        fixed_clean_ast = fix_ast_locations(functiondefs_and_exports_ast)

        clean_export_source = astor.to_source(fixed_clean_ast)

        with open(target, "w") as f:
            f.write(clean_export_source)

    return clean_export_source


def notebook_exporter_cli():
    parser = argparse.ArgumentParser(description="Process notebook file")

    parser.add_argument("source", type=str, help="The source file to be processed")
    parser.add_argument(
        "target", type=str, help="The file you want the results to be save to"
    )

    args = parser.parse_args()

    clean_export_file(args.source, args.target)


if __name__ == "__main__":
    notebook_exporter_cli()
