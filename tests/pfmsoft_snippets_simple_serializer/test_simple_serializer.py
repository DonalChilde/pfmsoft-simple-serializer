from dataclasses import dataclass, field
from typing import TypedDict

from pfmsoft.snippets.simple_serializer.simple_serializer import DataclassSerializer


@dataclass
class DCTestClass:
    name: str
    items: list[str] = field(default_factory=list)


class DCTestClassTD(TypedDict):
    name: str
    items: list[str]


def test_to_simple():
    serializer = DataclassSerializer[DCTestClass, DCTestClassTD](DCTestClass)
    dc = DCTestClass(name="bob", items=["chair", "table"])
    dctd: DCTestClassTD = {"name": "bob", "items": ["chair", "table"]}
    simplified_dc = serializer.to_simple(dc)
    assert simplified_dc == dctd
    recomplicated_dc = serializer.from_simple(simplified_dc)
    assert recomplicated_dc == dc
