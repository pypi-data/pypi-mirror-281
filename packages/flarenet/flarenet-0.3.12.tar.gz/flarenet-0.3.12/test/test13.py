from typing import Generator


def f():
    yield 1
    x = yield 2
    return x


def g():
    x = (yield from f()) if isinstance(f(), Generator) else f()
    return x


def run_generator(gen):
    try:
        x = next(gen)
        print("received", x)

        while True:
            # print("sending None")
            x = gen.send("message")
            print("received", x)
    except StopIteration as e:
        print("return value", e.value)


r = run_generator(g())
