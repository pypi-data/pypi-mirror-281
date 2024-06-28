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


def f1():
    print("yielding 1 from f1")
    x = yield 1
    print("got", x)
    print("yielding 2 from f2")
    yield 2
    return 3


def f2(x):
    print("yielding 3 from f2")
    yield 3
    print("yielding 4 from f2")
    yield 4


def f3():
    a = yield from f1()
    print(f"{a=}")
    return a


# def generator_to_function(gen):


r = run_generator(f3())
# print(r)
