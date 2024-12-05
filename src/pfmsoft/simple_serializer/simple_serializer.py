"""A simple serializer."""

from abc import ABC, abstractmethod
from collections.abc import Callable, Generator, Iterable
from dataclasses import asdict, is_dataclass
from json import dump as json_dump
from json import load as json_load
from pathlib import Path
from typing import (
    Generic,
    TypeVar,
)

from pfmsoft.simple_serializer.snippets.file.check_file import check_file

COMPLEX_OBJ = TypeVar("COMPLEX_OBJ")
SIMPLE_OBJ = TypeVar("SIMPLE_OBJ")


class SimpleSerializerABC(ABC, Generic[COMPLEX_OBJ, SIMPLE_OBJ]):
    """SimpleSerializerABC."""

    def __init__(
        self,
        simple_factory: Callable[[COMPLEX_OBJ], SIMPLE_OBJ] | None = None,
        complex_factory: Callable[[SIMPLE_OBJ], COMPLEX_OBJ] | None = None,
    ) -> None:
        """_summary_.

        _extended_summary_

        Args:
            simple_factory (_type_, optional): _description_. Defaults to None.
            complex_factory (_type_, optional): _description_. Defaults to None.
        """
        super().__init__()
        self.simple_factory = simple_factory
        self.complex_factory = complex_factory

    @abstractmethod
    def to_simple(self, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ:
        """Convert a complex object to a simple one."""

    @abstractmethod
    def from_simple(self, simple_obj: SIMPLE_OBJ) -> COMPLEX_OBJ:
        """Convert a simple object to a complex one."""

    def from_simple_gen(
        self, simple_objs: Iterable[SIMPLE_OBJ]
    ) -> Generator[COMPLEX_OBJ]:
        """A generator for converting simple to complex."""
        for item in simple_objs:
            yield self.from_simple(item)

    def to_simple_gen(
        self, complex_obj: Iterable[COMPLEX_OBJ]
    ) -> Generator[SIMPLE_OBJ]:
        """A generator for converting complex to simple."""
        for item in complex_obj:
            yield self.to_simple(item)

    def save_as_json(
        self,
        path_out: Path,
        complex_obj: COMPLEX_OBJ,
        indent: int = 1,
        overwrite: bool = False,
    ):
        """Save a complex object as json."""
        check_file(path_out=path_out, overwrite=overwrite, ensure_parents=True)
        data = self.to_simple(complex_obj=complex_obj)
        with open(path_out, "w") as file:
            json_dump(obj=data, fp=file, indent=indent)

    def save_iter_as_json(
        self,
        path_out: Path,
        complex_obj: Iterable[COMPLEX_OBJ],
        indent: int = 1,
        overwrite: bool = False,
    ):
        """Save an Iterable complex obj to a json list."""
        check_file(path_out=path_out, overwrite=overwrite, ensure_parents=True)
        data = list(self.to_simple_gen(complex_obj=complex_obj))
        with open(path_out, "w") as file:
            json_dump(obj=data, fp=file, indent=indent)

    def load_from_json(self, path_in: Path) -> COMPLEX_OBJ:
        """Load a complex object from json."""
        with open(path_in) as file:
            return self.from_simple(json_load(file))

    def load_from_json_list(self, path_in: Path) -> list[COMPLEX_OBJ]:
        """Load a json list of complex objects."""
        with open(path_in) as file:
            json_data = json_load(file)
            return list(self.from_simple_gen(simple_objs=json_data))

    def save_as_yaml(
        self,
        path_out: Path,
        complex_obj: COMPLEX_OBJ,
        indent: int = 1,
        overwrite: bool = False,
    ):
        """Save a complex object to yaml."""
        try:
            from yaml import safe_dump

            check_file(path_out=path_out, overwrite=overwrite, ensure_parents=True)
            with open(path_out, "w") as file:
                safe_dump(data=self.to_simple(complex_obj), stream=file, indent=indent)
        except ModuleNotFoundError as e:
            raise ValueError("PyYaml not found.") from e

    def save_iter_as_yaml(
        self,
        path_out: Path,
        complex_obj: Iterable[COMPLEX_OBJ],
        indent: int = 1,
        overwrite: bool = False,
    ):
        """Save an Iterable complex obj to a yaml list."""
        try:
            from yaml import safe_dump

            check_file(path_out=path_out, overwrite=overwrite, ensure_parents=True)
            with open(path_out, "w") as file:
                safe_dump(
                    data=list(self.to_simple_gen(complex_obj)),
                    stream=file,
                    indent=indent,
                )
        except ModuleNotFoundError as e:
            raise ValueError("PyYaml not found.") from e

    def load_from_yaml(self, path_in: Path) -> COMPLEX_OBJ:
        """Load a complex object from yaml."""
        try:
            from yaml import safe_load

            with open(path_in) as file:
                return self.from_simple(safe_load(file))
        except ModuleNotFoundError as e:
            raise ValueError("PyYaml not found.") from e

    def load_from_yaml_list(self, path_in: Path) -> list[COMPLEX_OBJ]:
        """Load a yaml list of complex objects."""
        try:
            from yaml import safe_load

            with open(path_in) as file:
                yaml_data = safe_load(file)
            return list(self.from_simple_gen(yaml_data))
        except ModuleNotFoundError as e:
            raise ValueError("PyYaml not found.") from e


class DataclassSerializer(SimpleSerializerABC[COMPLEX_OBJ, SIMPLE_OBJ]):
    """A simple dataclass serializer."""

    def __init__(
        self,
        simple_factory: Callable[[COMPLEX_OBJ], SIMPLE_OBJ] | None = None,
        complex_factory: Callable[[SIMPLE_OBJ], COMPLEX_OBJ] | None = None,
    ) -> None:
        """A simple dataclass serializer.

        To serialize, the default arguments are enough.
        Default behavior for the simple factory is `asdict(value)`

        To deserialize, provide a complex factory.

        ```
        # For simple cases:
        lambda x: YourDataclass(**x)
        ```

        Args:
            simple_factory : The dataclass to simple object factory. Defaults to None.
            complex_factory : The simple object to dataclass factory. Defaults to None.
        """
        if simple_factory is None:
            simple_factory = self._to_simple_default

        self.simple_factory = simple_factory
        self.complex_factory = complex_factory
        super().__init__(
            simple_factory=simple_factory,
            complex_factory=complex_factory,
        )

    def to_simple(self, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ:
        """Convert a dataclass to a simple object."""
        return self.simple_factory(complex_obj)

    def from_simple(self, simple_obj: SIMPLE_OBJ) -> COMPLEX_OBJ:
        """Convert a simple object to a dataclass."""
        if self.complex_factory is None:
            raise ValueError("SimpleSerializer was not provided a complex factory.")
        return self.complex_factory(simple_obj)

    @staticmethod
    def _to_simple_default(data_cls: COMPLEX_OBJ) -> SIMPLE_OBJ:
        if is_dataclass(data_cls):
            return asdict(data_cls)  # type: ignore
        else:
            raise ValueError(
                f"complex_obj is not a dataclass, its type name is {type(data_cls).__name__}"
            )
