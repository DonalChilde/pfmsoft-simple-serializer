"""Tests for the simple serializer."""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict

import pytest

from pfmsoft.simple_serializer.simple_serializer import DataclassSerializer

logger = logging.getLogger(__name__)


@dataclass
class DCTestClass:
    """Dataclass test data holder."""

    name: str
    items: list[str] = field(default_factory=list)


class DCTestClassTD(TypedDict):
    """TypedDict test data holder."""

    name: str
    items: list[str]


def test_to_simple():
    """Test roundtrip to simple."""
    serializer = DataclassSerializer[DCTestClass, DCTestClassTD](
        complex_factory=lambda x: DCTestClass(**x)
    )
    dc = DCTestClass(name="bob", items=["chair", "table"])
    dctd: DCTestClassTD = {"name": "bob", "items": ["chair", "table"]}
    simplified_dc = serializer.to_simple(dc)
    assert simplified_dc == dctd
    recomplicated_dc = serializer.from_simple(simplified_dc)
    assert recomplicated_dc == dc


# def test_to_json(test_output_dir: Path):
#     # logger.info("trying to save json")
#     dc = DCTestClass(name="bob", items=["chair", "table"])
#     serializer = DataclassSerializer[DCTestClass, DCTestClassTD](
#         complex_factory=lambda x: DCTestClass(**x)
#     )
#     path_out = test_output_dir / "test_to_json" / "output.json"
#     serializer.save_as_json(path_out=path_out, complex_obj=dc, overwrite=True)


# def test_list_to_json(test_output_dir: Path):
#     # logger.info("trying to save json")
#     dc = DCTestClass(name="bob", items=["chair", "table"])
#     dc2 = DCTestClass(name="Richard", items=["Billard balls", "cue stick"])
#     items = [dc, dc2]
#     serializer = DataclassSerializer[DCTestClass, DCTestClassTD](
#         complex_factory=lambda x: DCTestClass(**x)
#     )
#     path_out = test_output_dir / "test_list_to_json" / "output.json"
#     serializer.save_iter_as_json(path_out=path_out, complex_obj=items, overwrite=True)


def test_list_from_json(test_output_dir: Path):
    """Test roundtrip json."""
    dc = DCTestClass(name="bob", items=["chair", "table"])
    dc2 = DCTestClass(name="Richard", items=["Billard balls", "cue stick"])
    items = [dc, dc2]
    serializer = DataclassSerializer[DCTestClass, DCTestClassTD](
        complex_factory=lambda x: DCTestClass(**x)
    )
    path_out = test_output_dir / "test_list_from_json" / "output.json"
    serializer.save_iter_as_json(path_out=path_out, complex_obj=items, overwrite=True)
    loaded_items = serializer.load_from_json_list(path_in=path_out)
    assert loaded_items == items


def test_list_from_yaml(test_output_dir: Path):
    """Test round trip to yaml."""
    try:
        import yaml  # type: ignore
    except ImportError:
        pytest.skip("yaml not installed.")
    dc = DCTestClass(name="bob", items=["chair", "table"])
    dc2 = DCTestClass(name="Richard", items=["Billard balls", "cue stick"])
    items = [dc, dc2]
    serializer = DataclassSerializer[DCTestClass, DCTestClassTD](
        complex_factory=lambda x: DCTestClass(**x)
    )
    path_out = test_output_dir / "test_list_from_yaml" / "output.yaml"

    serializer.save_iter_as_yaml(path_out=path_out, complex_obj=items, overwrite=True)
    loaded_items = serializer.load_from_yaml_list(path_in=path_out)
    assert loaded_items == items
