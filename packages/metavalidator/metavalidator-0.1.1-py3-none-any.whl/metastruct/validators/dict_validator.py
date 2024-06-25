from metastruct.validators.item_constructor import any_from_text


def is_dict_of_list(rawtext: str) -> bool:
    data = any_from_text(rawtext)
    if isinstance(data, dict):
        return all(isinstance(v, list) for v in data.values())
    else:
        return False
