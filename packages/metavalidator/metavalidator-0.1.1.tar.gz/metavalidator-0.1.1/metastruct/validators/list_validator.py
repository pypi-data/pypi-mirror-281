from metastruct.validators.item_constructor import any_from_text


def is_list_of_str(rawtext: str) -> bool:
    data = any_from_text(rawtext)
    if isinstance(data, list):
        return all(isinstance(v, str) for v in data)
    else:
        return False
