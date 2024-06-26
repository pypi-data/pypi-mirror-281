def tuple_to_nested_dict(input_dict):
    def insert_nested_dict(d, keys, value):
        if len(keys) == 1:
            d[keys[0]] = value
        else:
            if keys[0] not in d:
                d[keys[0]] = {}
            insert_nested_dict(d[keys[0]], keys[1:], value)

    nested_dict = {}
    for k, v in input_dict.items():
        insert_nested_dict(nested_dict, k, v)

    return nested_dict


# Example usage
input_dict = {("a", "b", "c"): 1, ("a", "b", "d"): 2, ("a", "e"): 3, ("f",): 4}

nested_dict = tuple_to_nested_dict(input_dict)
print(nested_dict)
