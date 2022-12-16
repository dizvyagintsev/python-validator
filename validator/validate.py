import ast
from string import ascii_lowercase, ascii_uppercase
from typing import Union, Generator

_Node = Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]


def validate_file(filename: str) -> bool:
    return validate(open(filename, encoding="utf-8").read())


def validate(code: str) -> bool:
    """
    Checks code syntax and style

    Style guide:
    1. Name of function outside of class must start with uppercase letter
    2. Name of function inside of class must start with lowercase letter
    3. Name of class must start with uppercase letter

    :param code: python code
    :return: bool if code syntax and style is valid
    """
    try:
        node = ast.parse(code)
    except SyntaxError:
        return False

    for child_node in _needs_validation(node):
        if not _validate_node(child_node, in_class=False):
            return False

    return True


def _validate_node(
    node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef],
    in_class: bool,
) -> bool:
    if _is_function(node):
        if not _validate_function_name(node.name, in_class):
            return False
    else:
        in_class = True

        if not _validate_class_name(node.name):
            return False

    for child_node in _needs_validation(node):
        if not _validate_node(child_node, in_class):
            return False

    return True


def _validate_function_name(name: str, in_class: bool) -> bool:
    if in_class:
        return name[0] in ascii_lowercase

    return name[0] in ascii_uppercase


def _validate_class_name(name: str) -> bool:
    return name[0] in ascii_uppercase


def _is_function(node: _Node) -> bool:
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))


def _needs_validation(
    node: Union[
        ast.Module,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
    ],
) -> Generator[_Node, None, None]:
    for child_node in node.body:
        if isinstance(
            child_node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            yield child_node
