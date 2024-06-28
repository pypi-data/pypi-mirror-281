import dis
import functools
import jax

import sys


def trace_assignments(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bytecode = dis.Bytecode(func)
        assignment_ops = {"STORE_NAME", "STORE_FAST", "STORE_GLOBAL"}

        def trace(frame, event, _):
            if event == "line":
                for instr in bytecode:
                    if instr.opname in assignment_ops:
                        varname = instr.argval
                        if varname in frame.f_locals:
                            print(f"Assignment: {varname} = {frame.f_locals[varname]}")

            return trace

        sys.settrace(trace)
        try:
            result = func(*args, **kwargs)
        finally:
            sys.settrace(None)
        return result

    return wrapper


# Example usage
@trace_assignments
@jax.vmap
def example_function(x):
    # x = 10
    y = 5
    z = x + y
    return z


example_function(jax.numpy.zeros((32, 3)))
