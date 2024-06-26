# %%
import ast
import astor


class AssignmentPrinter(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        new_body = []
        for stmt in node.body:
            new_body.append(stmt)
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        print_stmt = ast.Expr(
                            value=ast.Call(
                                func=ast.Name(id="print", ctx=ast.Load()),
                                args=[ast.Constant(f"{target.id} ="), target],
                                keywords=[],
                            )
                        )
                        new_body.append(print_stmt)
        node.body = new_body
        return node


def modify_and_print_assignments(source_code):
    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Transform the AST to add print statements
    transformer = AssignmentPrinter()
    transformed_tree = transformer.visit(tree)

    # Convert the modified AST back to source code
    modified_code = astor.to_source(transformed_tree)

    return modified_code


source_code = """
def calculate_total(price, quantity, tax_rate=0.05, discount=0.1):
    subtotal = price * quantity
    tax = subtotal * tax_rate
    discount_amount = subtotal * discount
    total = subtotal + tax - discount_amount
    return total
"""

modified_code = modify_and_print_assignments(source_code)
print(modified_code)

# Optional: Execute the modified code
exec(modified_code)

# Call the function to see the prints
calculate_total(100, 5)
