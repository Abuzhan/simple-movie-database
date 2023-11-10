from dataclasses import dataclass


@dataclass(frozen=True)
class UpsertCommand:
    table: str
    rows: list[dict]
    index_elements: list[str]
    columns_to_update: list[str]


__all__ = ['UpsertCommand']
