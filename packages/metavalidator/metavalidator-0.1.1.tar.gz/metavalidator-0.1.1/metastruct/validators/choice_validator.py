from typing import List, Set


def is_valid_choice(
    choice: str,
    options: Set[str]
) -> bool:
    return choice in options


def are_all_valid_choices(
    choices: List[str],
    options: Set[str]
) -> bool:
    return all(is_valid_choice(choice, options) for choice in choices)
