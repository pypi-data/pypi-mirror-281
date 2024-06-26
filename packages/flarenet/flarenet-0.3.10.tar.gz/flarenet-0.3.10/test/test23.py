class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y


# Example usage
point = Point(1, 2)
x, y = point
print(x)  # Output: 1
print(y)  # Output: 2
