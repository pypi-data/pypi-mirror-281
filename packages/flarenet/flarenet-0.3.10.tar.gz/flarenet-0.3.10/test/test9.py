import ast
import inspect
import textwrap


class LogTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Create a logging statement
        log_statement = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="print", ctx=ast.Load()),
                args=[ast.Constant(value=f"Entering function {node.name}")],
                keywords=[],
            )
        )

        # Set lineno and col_offset for the new statement
        log_statement.lineno = node.body[0].lineno
        log_statement.col_offset = node.body[0].col_offset

        # Insert the logging statement at the beginning of the function body
        node.body.insert(0, log_statement)
        return node


def wrap_with_logging(func):
    # Get the source code of the function
    source = inspect.getsource(func)
    source = textwrap.dedent(source)

    # Parse the source code into an AST
    tree = ast.parse(source)

    # Transform the AST to add logging
    transformer = LogTransformer()
    tree = transformer.visit(tree)

    # Fix the line numbers and column offsets
    ast.fix_missing_locations(tree)

    # Compile the modified AST
    code = compile(tree, filename="<ast>", mode="exec")

    # Extract the modified function from the compiled code
    namespace = {}
    exec(code, func.__globals__, namespace)

    # Return the modified function
    return namespace[func.__name__]


def assert_false():
    assert False


def wrap_id(func):
    return func


def wrap(func):
    func = wrap_id(func)
    func = wrap_with_logging(func)
    return func


# Define the function you want to wrap
@wrap
def my_function(x, y):
    false = assert_false()
    return x + y


# Wrap the function with logging
# my_function = wrap_with_logging(my_function)

# Call the modified function
result = my_function(2, 3)
print(result)
