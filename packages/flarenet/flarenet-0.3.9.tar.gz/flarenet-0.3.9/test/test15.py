from greenlet import greenlet


class Bias:
    def __call__(self, x):
        return x + 1


class Linear:
    def __call__(self, x):
        return x * 2


class Affine:
    def __init__(self):
        self.bias = Bias()
        self.linear = Linear()

    def __call__(self, x):
        x = self.linear(x)
        x = self.bias(x)
        return x


class Sequential:
    def __init__(self, *layers):
        self.layers = layers

    def __call__(self, x):
        for layer in self.layers:
            x = greenlet.getcurrent().parent.switch(x)
            print(x)
            x = layer(x)

        print("done")
        return x


model = Sequential(Affine(), Affine())

green = greenlet(model)
r = green.switch("hello")
r = green.switch(1)

print(r)
