from typing import Any, Type

from metastruct.basetypes import ErrEnum
from metastruct.utils import JSONTool


def any_from_text(rawtext: str) -> Any:
    """Validate the raw text."""
    try:
        data = JSONTool.from_raw(rawtext)
    except Exception as _:
        return ErrEnum.BAD_RESP
    return data


def contruct_item_from_text(rawtext: str, constructor: Type) -> ErrEnum:
    """Validate the raw text."""
    try:
        data = any_from_text(rawtext)
        if data == ErrEnum.BAD_RESP:
            return ErrEnum.BAD_RESP
        if isinstance(data, list):
            for item in data:
                constructor(**item)
        else:
            constructor(**data)
    except Exception as err:
        print(err)
        return ErrEnum.BAD_SCHEMA
    return ErrEnum.NO_ERR
