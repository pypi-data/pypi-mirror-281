import ast
import inspect
from ast import fix_missing_locations

import warnings


def repr_node(node):
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Subscript):
        return f"{repr_node(node.value)}[{repr_node(node.slice)}]"

    if isinstance(node, ast.Starred):
        return f"*{repr_node(node.value)}"

    warnings.warn(f"Unknown node type {type(node)}")
    return "<Unknown>"


def print_nodes(target: ast.expr, node):
    value = ast.Constant(f"variable {repr_node(target)}")
    acall = ast.Call(
        func=ast.Name(id="print", ctx=ast.Load()),
        args=[value, node.value],
        keywords=[],
    )
    expr = ast.Expr(value=acall)
    return [expr]


class AddPrints(ast.NodeTransformer):
    def visit_Assign(self, node):
        new_nodes = []
        stack = list(node.targets)

        while stack:
            target = stack.pop()

            if isinstance(target, ast.Tuple):
                # print(type(node))
                # print(dir(target), target.dims)
                stack.extend(target.elts[::-1])
                continue

            new_nodes.extend(print_nodes(target, node))

        return [node, *new_nodes]


def add_prints(func):
    # Inspect gets the source, then parse into an AST
    source = inspect.getsource(func)
    tree = ast.parse(source)

    # Transform the AST
    AddPrints().visit(tree)

    # fix location info
    # print(tree)
    # print(fix_missing_locations(tree), "hello")
    tree = fix_missing_locations(tree)

    # turn transformed AST back into code
    new_func_code = compile(tree, filename="<ast>", mode="exec")

    # Create a new dictionary for the function's local namespace
    new_func_namespace = {}
    exec(new_func_code, new_func_namespace)

    # Return the function from the new namespace
    return new_func_namespace[func.__name__]


# Test function
# @add_prints
def test():
    a = 1
    b = 2
    c, d = 3, 4

    # assert False
    *e, f = [1, 2, 3, 4, 5]
    a = 3

    e[1] = 5


# Add two more assignments into the function
test_transformed = add_prints(test)
test_transformed()
