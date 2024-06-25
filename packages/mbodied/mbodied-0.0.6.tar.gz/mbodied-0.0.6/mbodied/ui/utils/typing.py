from enum import Enum


def create_enum_from_list(name, string_list) -> Enum:
    """Dynamically create an Enum type from a list of strings.

    Args:
        name (str): The name of the Enum class.
        string_list (list[str]): The list of strings to be converted into Enum members.

    Returns:
        Enum: A dynamically created Enum type with members based on the string list.
    """
    return Enum(value=name, names=[(item.replace(" ", "_").upper(), item) for item in string_list])
