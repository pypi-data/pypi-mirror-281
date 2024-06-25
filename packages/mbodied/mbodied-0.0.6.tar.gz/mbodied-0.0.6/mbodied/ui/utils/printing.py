def print_green(text: str, end: str = "\n") -> None:
    print("\x1b[32m" + str(text) + "\x1b[0m", end=end)  # noqa: T201


def print_red(text: str, end: str = "\n") -> None:
    print("\x1b[31m" + str(text) + "\x1b[0m", end=end)  # noqa: T201


def print_yellow(text: str, end: str = "\n") -> None:
    print("\x1b[33m" + str(text) + "\x1b[0m", end=end)  # noqa: T201


def print_blue(text: str, end: str = "\n") -> None:
    print("\x1b[34m" + str(text) + "\x1b[0m", end=end)  # noqa: T201
