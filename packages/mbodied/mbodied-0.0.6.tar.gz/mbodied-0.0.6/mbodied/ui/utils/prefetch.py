from typing import NoReturn


class Prefetchable:
    def __init__(self, prefetch: bool = False):
        self.prefetch = prefetch
        if self.prefetch:
            self.prefetch_resources()

    def prefetch_resources(self) -> NoReturn:
        """Method to prefetch resources. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses should implement this method.")
