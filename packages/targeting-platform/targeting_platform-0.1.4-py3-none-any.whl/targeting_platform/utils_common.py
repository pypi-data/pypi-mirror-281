"""Utils module."""

from typing import Generator, List, Any


def generate_batches(iterable: List[Any], batch_size_limit: int) -> Generator[Any, Any, Any]:
    """Generate lists of length size batch_size_limit containing objects yielded by the iterable."""
    batch: List[Any] = []

    for item in iterable:
        if len(batch) == batch_size_limit:
            yield batch
            batch = []
        batch.append(item)

    if len(batch):
        yield batch
