import inspect


def get_var_name(value):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    var_name = [
        var_name for var_name, var_val in callers_local_vars if var_val is value
    ]
    return var_name


def example_function(x):
    var_name = get_var_name(x)
    print(f"The variable name is: {var_name[0] if var_name else 'Unknown'}")


# Example usage
a = 10
example_function(a)
