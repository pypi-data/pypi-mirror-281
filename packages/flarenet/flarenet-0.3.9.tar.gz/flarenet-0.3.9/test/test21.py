import ast
import inspect


# Step 1: Define the original function
def original_function(x, y):
    assert False
    return x + y


# Step 2: Parse the function's source code into an AST
source_code = inspect.getsource(original_function)
tree = ast.parse(source_code)


# Step 3: Modify the AST
class Transformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Add):
            node.op = ast.Sub()
        return node


transformer = Transformer()
modified_tree = transformer.visit(tree)
ast.fix_missing_locations(modified_tree)

# Step 4: Compile and execute the modified AST
code = compile(modified_tree, filename="<ast>", mode="exec")
exec(code)

# Step 5: Test the modified function
result = original_function(10, 5)
print(result)  # Output should be 5 instead of 15

# Crozet
