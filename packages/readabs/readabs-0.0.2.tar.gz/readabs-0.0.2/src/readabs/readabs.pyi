"""Stubs for readabs."""

from typing import Any, Sequence
from pandas import DataFrame, Series


# TO DO: metacol

def catalogue_map() -> DataFrame: ...
def print_abs_catalogue() -> None: ...

def get_data_links(
    url: str, inspect_file_name="", **kwargs: Any,
) -> dict[str, list[str]]: ...

def read_abs_cat(
    cat: str, **kwargs: Any,
) -> tuple[dict[str, DataFrame], DataFrame]: ...

def read_abs_series(
    cat: str,
    series_id: str | Sequence[str],
    **kwargs: Any,
) -> tuple[DataFrame, DataFrame]: ...


