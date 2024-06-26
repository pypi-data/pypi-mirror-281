import ast
import inspect
from ast import fix_missing_locations


def print_nodes(target: ast.Name | ast.Tuple, node: ast.Assign):
    if isinstance(target, ast.Tuple):
        exprs = []

        for t in target.elts:
            if not isinstance(t, ast.Name):
                print(f"Skipping target of type {type(t)}")
                continue

            exprs.extend(print_nodes(t, node))

        return exprs

    if not isinstance(target, ast.Name):
        error = f"Expected target to be an ast.Name, got {type(target)}"
        raise ValueError(error)

    value = ast.Constant(f"variable {target.id} is assigned the value")
    acall = ast.Call(
        func=ast.Name(id="print", ctx=ast.Load()),
        args=[value, target],
        keywords=[],
    )
    expr = ast.Expr(value=acall)
    return [expr]


class AddPrints(ast.NodeTransformer):
    def visit_Assign(self, node):
        new_nodes = []

        for target in node.targets:
            # if isinstance(target, ast.Tuple):
            #     for t in target.elts:
            #         if not isinstance(t, ast.Name):
            #             print(f"Skipping target of type {type(t)}")
            #             continue

            #         new_nodes.append(print_nodes(t, node))

            # if not isinstance(target, ast.Name):
            #     print(f"Skipping target of type {type(target)}")
            #     continue

            if not isinstance(target, ast.Name | ast.Tuple):
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
    fix_missing_locations(tree)

    # turn transformed AST back into code
    new_func_code = compile(tree, filename="<ast>", mode="exec")

    # Create a new dictionary for the function's local namespace
    new_func_namespace = {}
    exec(new_func_code, new_func_namespace)

    # Return the function from the new namespace
    return new_func_namespace[func.__name__]


# Test function
def test():
    a = 1
    b = 2
    c, d = 3, 4

    *e, f = [1, 2, 3, 4, 5]


# Add two more assignments into the function
test_transformed = add_prints(test)
test_transformed()
