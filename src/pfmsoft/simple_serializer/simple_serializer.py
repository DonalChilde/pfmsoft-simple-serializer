from abc import ABC, abstractmethod
from dataclasses import asdict, is_dataclass
from json import dump as json_dump
from json import load as json_load
from pathlib import Path
from typing import (
    Callable,
    Generator,
    Generic,
    Iterable,
    Optional,
    TypeVar,
)

try:
    from yaml import safe_dump, safe_load

    YAML_PRESENT = True
except ModuleNotFoundError:
    YAML_PRESENT = False  # type: ignore


COMPLEX_OBJ = TypeVar("COMPLEX_OBJ")
SIMPLE_OBJ = TypeVar("SIMPLE_OBJ")


# class SimpleConverter(Protocol[COMPLEX_OBJ, SIMPLE_OBJ]):
#     def to_simple(self, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ: ...

#     def from_simple(self, simple_obj: SIMPLE_OBJ) -> COMPLEX_OBJ: ...

#     def from_simple_gen(
#         self, simple_objs: Iterable[SIMPLE_OBJ]
#     ) -> Generator[COMPLEX_OBJ, None, None]: ...

#     def to_simple_gen(
#         self,
#         complex_objs: Iterable[COMPLEX_OBJ],
#     ) -> Generator[SIMPLE_OBJ, None, None]: ...


# class SimpleSerializer(Protocol[COMPLEX_OBJ]):
#     def save_json(
#         self,
#         path_out: Path,
#         complex_obj: COMPLEX_OBJ,
#         indent: int = 1,
#         overwrite: bool = False,
#     ): ...

#     def load_json(self, path_in: Path) -> COMPLEX_OBJ: ...

#     def save_yaml(
#         self,
#         path_out: Path,
#         complex_obj: COMPLEX_OBJ,
#         indent: int = 1,
#         overwrite: bool = False,
#     ): ...

#     def load_yaml(self, path_in: Path) -> COMPLEX_OBJ: ...


class SimpleSerializerABC(ABC, Generic[COMPLEX_OBJ, SIMPLE_OBJ]):
    def __init__(
        self,
        # complex_cls: Type[COMPLEX_OBJ],
        simple_factory: Optional[Callable[[COMPLEX_OBJ], SIMPLE_OBJ]] = None,
        complex_factory: Optional[Callable[[SIMPLE_OBJ], COMPLEX_OBJ]] = None,
    ) -> None:
        super().__init__()
        # self.complex_cls = complex_cls
        self.simple_factory = simple_factory
        self.complex_factory = complex_factory

    @abstractmethod
    def to_simple(self, complex_obj: COMPLEX_OBJ) -> SIMPLE_OBJ:
        pass

    @abstractmethod
    def from_simple(self, simple_obj: SIMPLE_OBJ) -> COMPLEX_OBJ:
        pass

    def from_simple_gen(
        self, simple_objs: Iterable[SIMPLE_OBJ]
    ) -> Generator[COMPLEX_OBJ, None, None]:
        for item in simple_objs:
            yield self.from_simple(item)

    def to_simple_gen(
        self, complex_obj: Iterable[COMPLEX_OBJ]
    ) -> Generator[SIMPLE_OBJ, None, None]:
        for item in complex_obj:
            yield self.to_simple(item)

    def save_as_json(
        self,
        path_out: Path,
        complex_obj: COMPLEX_OBJ,
        indent: int = 1,
        overwrite: bool = False,
    ):
        check_file(path_out=path_out, overwrite=overwrite)
        path_out.parent.mkdir(exist_ok=True, parents=True)
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
        check_file(path_out=path_out, overwrite=overwrite)
        path_out.parent.mkdir(exist_ok=True, parents=True)
        data = list(self.to_simple_gen(complex_obj=complex_obj))
        with open(path_out, "w") as file:
            json_dump(obj=data, fp=file, indent=indent)

    def load_from_json(self, path_in: Path) -> COMPLEX_OBJ:
        with open(path_in, "r") as file:
            return self.from_simple(json_load(file))

    def load_from_json_list(self, path_in: Path) -> list[COMPLEX_OBJ]:
        with open(path_in, "r") as file:
            json_data = json_load(file)
            return list(self.from_simple_gen(simple_objs=json_data))

    def save_as_yaml(
        self,
        path_out: Path,
        complex_obj: COMPLEX_OBJ,
        indent: int = 1,
        overwrite: bool = False,
    ):
        if not YAML_PRESENT:
            raise ValueError("PyYaml not found.")
        check_file(path_out=path_out, overwrite=overwrite)
        path_out.parent.mkdir(exist_ok=True, parents=True)
        with open(path_out, "w") as file:
            safe_dump(data=self.to_simple(complex_obj), stream=file, indent=indent)

    def save_iter_as_yaml(
        self,
        path_out: Path,
        complex_obj: Iterable[COMPLEX_OBJ],
        indent: int = 1,
        overwrite: bool = False,
    ):
        if not YAML_PRESENT:
            raise ValueError("PyYaml not found.")
        check_file(path_out=path_out, overwrite=overwrite)
        path_out.parent.mkdir(exist_ok=True, parents=True)
        with open(path_out, "w") as file:
            safe_dump(
                data=list(self.to_simple_gen(complex_obj)),
                stream=file,
                indent=indent,
            )

    def load_from_yaml(self, path_in: Path) -> COMPLEX_OBJ:
        if not YAML_PRESENT:
            raise ValueError("PyYaml not found.")
        with open(path_in, "r") as file:
            return self.from_simple(safe_load(file))

    def load_from_yaml_list(self, path_in: Path) -> list[COMPLEX_OBJ]:
        if not YAML_PRESENT:
            raise ValueError("PyYaml not found.")
        with open(path_in, "r") as file:
            yaml_data = safe_load(file)
            return list(self.from_simple_gen(yaml_data))


def check_file(path_out: Path, overwrite: bool = False) -> bool:
    if path_out.exists():
        if path_out.is_dir():
            raise ValueError(f"Output path exists and it is a directory. {path_out}")
        if path_out.is_file():
            if not overwrite:
                raise ValueError(
                    f"Output path exists and overwrite is false. {path_out}"
                )
    return True


class DataclassSerializer(SimpleSerializerABC[COMPLEX_OBJ, SIMPLE_OBJ]):
    def __init__(
        self,
        simple_factory: Optional[Callable[[COMPLEX_OBJ], SIMPLE_OBJ]] = None,
        complex_factory: Optional[Callable[[SIMPLE_OBJ], COMPLEX_OBJ]] = None,
    ) -> None:
        """
        A simple dataclass serializer.

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
        return self.simple_factory(complex_obj)

    def from_simple(self, simple_obj: SIMPLE_OBJ) -> COMPLEX_OBJ:
        if self.complex_factory is None:
            raise ValueError("SimpleSerializer was not provided a complex factory.")
        return self.complex_factory(simple_obj)

    def _to_simple_default(self, data_cls: COMPLEX_OBJ) -> SIMPLE_OBJ:
        if is_dataclass(data_cls):
            return asdict(data_cls)  # type: ignore
        else:
            raise ValueError(
                f"complex_obj is not a dataclass, its type name is {type(data_cls).__name__}"
            )
