def validate_fullname(value: str):
    number_spaces = value.count(" ")
    if 1 <= number_spaces <= 2:
        fullname = value.split(" ")
        for names in fullname:
            if names[0].isupper():
                continue
            else:
                raise ValueError
        return value
    raise ValueError
