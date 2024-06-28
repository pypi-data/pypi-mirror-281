from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Literal, Optional, Union

import pytest
from pydantic import BaseModel, Field, ValidationError

from datachain.lib.feature import Feature
from datachain.lib.feature_registry import Registry
from datachain.lib.feature_utils import pydantic_to_feature
from datachain.sql.types import (
    JSON,
    Array,
    Binary,
    Boolean,
    DateTime,
    Int64,
    String,
)


class FileBasic(Feature):
    parent: str = Field(default="")
    name: str
    size: int = Field(default=0)


class TestFileInfo(FileBasic):
    location: dict = Field(default={})


class FileInfoEx(Feature):
    f_info: TestFileInfo
    type_id: int


class MyNestedClass(Feature):
    type: int
    Name: str = Field(default="test1")


class MyTest(Feature):
    ThisIsName: str
    subClass: MyNestedClass  # noqa: N815


def test_flatten_schema():
    schema = TestFileInfo._to_udf_spec()

    assert len(schema) == 4
    assert [item[0] for item in schema] == ["parent", "name", "size", "location"]
    assert [item[1] for item in schema] == [String, String, Int64, JSON]


def test_type_datatype():
    class _Test(Feature):
        d: datetime

    schema = _Test._to_udf_spec()
    assert schema[0][1] == DateTime


def test_type_optional_int():
    class _Test(Feature):
        d: Optional[int] = 23

    schema = _Test._to_udf_spec()
    assert schema[0][1] == Int64


def test_type_bytes():
    class _Test(Feature):
        d: bytes

    schema = _Test._to_udf_spec()
    assert schema[0][1] == Binary


def test_type_array():
    class _Test(Feature):
        d: list[int]

    schema = _Test._to_udf_spec()
    assert type(schema[0][1]) == Array


def test_type_arrays():
    class _Test(Feature):
        d1: list[int]
        d2: list[float]

    schema = _Test._to_udf_spec()

    assert schema[0][1].to_dict() == {"item_type": {"type": "Int64"}, "type": "Array"}
    assert schema[1][1].to_dict() == {"item_type": {"type": "Float"}, "type": "Array"}


def test_type_array_of_arrays():
    class _Test(Feature):
        d1: list[list[int]]

    schema = _Test._to_udf_spec()

    type1 = schema[0][1]
    assert list == type1.python_type
    assert list == type1.impl.item_type.python_type
    assert int == type1.impl.item_type.impl.item_type.python_type


def test_type_json():
    class _Test(Feature):
        d: dict

    schema = _Test._to_udf_spec()
    assert schema[0][1] == JSON


def test_type_bool():
    class _Test(Feature):
        d: bool

    schema = _Test._to_udf_spec()
    assert schema[0][1] == Boolean


def test_type_typed_json():
    class _Test(Feature):
        d: Optional[dict[str, int]]

    schema = _Test._to_udf_spec()
    assert schema[0][1] == JSON


def test_unknown_type():
    class _Test(Feature):
        d: Optional[Decimal]

    with pytest.raises(TypeError):
        _Test._to_udf_spec()


def test_flatten_nested_schema():
    schema = FileInfoEx._to_udf_spec()

    assert len(schema) == 5
    assert [item[0] for item in schema] == [
        "f_info__parent",
        "f_info__name",
        "f_info__size",
        "f_info__location",
        "type_id",
    ]
    assert [item[1] for item in schema] == [String, String, Int64, JSON, Int64]


def test_flatten_nested_schema_shallow():
    class _MyTest1(Feature):
        a: int = Field(default=33)

    class _MyTest2(Feature):
        next2: _MyTest1

    class _MyTest3(Feature):
        next3: _MyTest2

    schema = _MyTest3(next3=_MyTest2(next2=_MyTest1()))._to_udf_spec()
    assert [item[0] for item in schema] == ["next3__next2__a"]


def test_flatten_nested_schema_shallow_1st_squashed():
    class _MyTest1(Feature):
        a: int = Field(default=1237)

    class _MyTest2(Feature):
        _is_shallow: ClassVar[bool] = True

        next2: _MyTest1

    class _MyTest3(Feature):
        next3: _MyTest2

    shallow_schema = _MyTest3(next3=_MyTest2(next2=_MyTest1()))._to_udf_spec()
    assert [item[0] for item in shallow_schema] == ["next2__a"]


def test_flatten_nested_schema_shallow_2nd_squashed():
    class _MyTest1(Feature):
        _is_shallow: ClassVar[bool] = True

        a: int = Field(default=33)

    class _MyTest2(Feature):
        next2: _MyTest1

    class _MyTest3(Feature):
        next3: _MyTest2

    shallow_schema = _MyTest3(next3=_MyTest2(next2=_MyTest1()))._to_udf_spec()
    assert [item[0] for item in shallow_schema] == ["a"]


def test_flatten_schema_list():
    t1 = TestFileInfo(name="test1")
    t2 = TestFileInfo(name="t2", parent="pp1")
    res = Feature._features_to_udf_spec([t1, t2])
    assert len(t1.model_dump()) == len(res)


def test_flatten_basic():
    vals = FileBasic(parent="hello", name="world", size=123)._flatten()
    assert vals == ("hello", "world", 123)


def test_flatten_with_json():
    t1 = TestFileInfo(parent="prt4", name="test1", size=42, location={"ee": "rr"})
    assert t1._flatten() == ("prt4", "test1", 42, {"ee": "rr"})


def test_flatten_with_empty_json():
    with pytest.raises(ValidationError):
        TestFileInfo(parent="prt4", name="test1", size=42, location=None)


def test_flatten_with_accepted_empty_json():
    class _Test(Feature):
        d: Optional[dict]

    assert _Test(d=None)._flatten() == (None,)


def test_flatten_nested():
    t0 = TestFileInfo(parent="sfo", name="sf", size=567, location={"42": 999})
    t1 = FileInfoEx(f_info=t0, type_id=1849)

    assert t1._flatten() == ("sfo", "sf", 567, {"42": 999}, 1849)


def test_flatten_list():
    t1 = TestFileInfo(parent="p1", name="n4", size=3, location={"a": "b"})
    t2 = TestFileInfo(parent="p2", name="n5", size=2, location={"c": "d"})

    vals = t1._flatten_list([t1, t2])
    assert vals == ("p1", "n4", 3, {"a": "b"}, "p2", "n5", 2, {"c": "d"})


def test_registry():
    class MyTestRndmz(Feature):
        name: str
        count: int

    assert Registry.get(MyTestRndmz.__name__) == MyTestRndmz
    assert Registry.get(MyTestRndmz.__name__, version=1) == MyTestRndmz
    Registry.remove(MyTestRndmz)


def test_registry_versioned():
    class MyTestXYZ(Feature):
        _version: ClassVar[int] = 42
        name: str
        count: int

    assert Registry.get(MyTestXYZ.__name__) == MyTestXYZ
    assert Registry.get(MyTestXYZ.__name__, version=1) is None
    assert Registry.get(MyTestXYZ.__name__, version=42) == MyTestXYZ
    Registry.remove(MyTestXYZ)


def test_inheritance():
    class SubObject(Feature):
        subname: str

    class SoMyTest1(Feature):
        name: str
        sub: SubObject

    class SoMyTest2(SoMyTest1):
        pass

    try:
        with pytest.raises(ValueError):
            SoMyTest2()

        obj = SoMyTest2(name="name", sub=SubObject(subname="subname"))
        assert obj._flatten() == ("name", "subname")
    finally:
        Registry.remove(SubObject)
        Registry.remove(SoMyTest1)
        Registry.remove(SoMyTest2)


def test_naming_transform():
    assert [name for name, _ in MyTest._to_udf_spec()] == [
        "this_is_name",
        "sub_class__type",
        "sub_class__name",
    ]


def test_capital_letter_naming():
    class CAPLetterTEST(Feature):
        AAA_id: str

    vals = [name for name, _ in CAPLetterTEST._to_udf_spec()]
    assert vals == ["aaa_id"]


def test_delimiter_in_name():
    with pytest.raises(RuntimeError):

        class _MyClass(Feature):
            var__name: str


def test_custom_delimiter_in_name():
    with pytest.raises(RuntimeError):

        class _MyClass(Feature):
            _delimiter = "EE"
            is_ieee_member: bool


def test_naming_delimiter():
    class MyTestNew(Feature):
        _delimiter = "+++"

        this_is_name: str
        sub_class1: MyNestedClass

    schema = MyTestNew._to_udf_spec()

    assert [name for name, _ in schema] == [
        "this_is_name",
        "sub_class1+++type",
        "sub_class1+++name",
    ]


def test_deserialize_nested():
    class Child(Feature):
        type: int
        name: str = Field(default="test1")

    class Parent(Feature):
        name: str
        child: Child

    in_db_map = {
        "name": "a1",
        "child__type": 42,
        "child__name": "a2",
    }

    p = Parent._unflatten(in_db_map)

    assert p.name == "a1"
    assert p.child.type == 42
    assert p.child.name == "a2"


def test_deserialize_squashed():
    class Child1(Feature):
        type: int
        child_name: str = Field(default="test1")

    class Parent1(Feature):
        _is_shallow: ClassVar[bool] = True

        name: str
        child: Child1

    in_db_map = {
        "child_name": "a1",
        "type": 42,
        "name": "a2",
    }

    p = Parent1._unflatten(in_db_map)

    assert p.name == "a2"
    assert p.child.type == 42
    assert p.child.child_name == "a1"


def test_deserialize_nested_with_name_normalization():
    class ChildClass(Feature):
        type: int
        name: str = Field(default="test1")

    class Parent2(Feature):
        name: str
        childClass11: ChildClass  # noqa: N815

    in_db_map = {
        "name": "name1",
        "child_class11__type": 12,
        "child_class11__name": "n2",
    }

    p = Parent2._unflatten(in_db_map)

    assert p.name == "name1"
    assert p.childClass11.type == 12
    assert p.childClass11.name == "n2"


def test_type_array_of_floats():
    class _Test(Feature):
        d: list[float]

    dict_ = {"d": [1, 3, 5]}
    t = _Test(**dict_)
    assert t.d == [1, 3, 5]


def test_class_attr_resolver_basic():
    class _MyTest(Feature):
        val1: list[float]
        pp: int

    assert _MyTest.val1.name == "val1"
    assert _MyTest.pp.name == "pp"
    assert type(_MyTest.pp.type) == Int64
    assert type(_MyTest.val1.type) == Array


def test_class_attr_resolver_shallow():
    class _MyTest(Feature):
        val1: list[float]
        pp: int

    assert _MyTest.val1.name == "val1"
    assert _MyTest.pp.name == "pp"
    assert type(_MyTest.pp.type) == Int64
    assert type(_MyTest.val1.type) == Array


def test_class_attr_resolver_nested():
    assert MyTest.subClass.type.name == "sub_class__type"
    assert MyTest.subClass.Name.name == "sub_class__name"
    assert type(MyTest.subClass.type.type) == Int64
    assert type(MyTest.subClass.Name.type) == String


def test_class_attr_resolver_nested_3levels():
    class _MyTest1(Feature):
        a: int

    class _MyTest2(Feature):
        b: _MyTest1

    class _MyTest3(Feature):
        c: _MyTest2

    assert _MyTest3.c.b.a.name == "c__b__a"
    assert type(_MyTest3.c.b.a.type) == Int64


def test_class_attr_resolver_nested_with_squashing():
    class _MyTest1(Feature):
        a: str

    class _MyTest2(Feature):
        _is_shallow: ClassVar[bool] = True

        b: _MyTest1

    class _MyTest3(Feature):
        c: _MyTest2

    assert _MyTest3.c.b.a.name == "c__a"
    assert type(_MyTest3.c.b.a.type) == String


def test_class_attr_resolver_partial():
    class _MyTest1(Feature):
        a: str

    class _MyTest2(Feature):
        b: _MyTest1

    class _MyTest3(Feature):
        c: _MyTest2

    assert _MyTest3.c.b.name == "c__b"


def test_list_of_dicts_as_dict():
    class _MyTest(Feature):
        val1: Union[dict, list[dict]]
        val2: Optional[Union[list[dict], dict]]

    schema = Feature._features_to_udf_spec([_MyTest])
    assert len(schema) == 2
    assert next(iter(schema.values())) == JSON
    assert list(schema.values())[1] == JSON


def test_literal():
    class _MyTextBlock(Feature):
        id: int
        type: Literal["text"]

    schema = Feature._features_to_udf_spec([_MyTextBlock])
    assert len(schema) == 2
    assert next(iter(schema.values())) == Int64
    assert list(schema.values())[1] == String


def test_pydantic_to_feature():
    class _MyTextBlock(BaseModel):
        id: int
        type: Literal["text"]

    cls = pydantic_to_feature(_MyTextBlock)
    assert Feature.is_feature(cls)

    schema = Feature._features_to_udf_spec([cls])
    assert len(schema) == 2
    assert next(iter(schema.values())) == Int64
    assert list(schema.values())[1] == String


def test_pydantic_to_feature_nested():
    class _MyTextBlock(BaseModel):
        id: int
        type: Literal["text"]

    class _MyMessage3(BaseModel):
        val1: Optional[str]
        val2: _MyTextBlock

    cls = pydantic_to_feature(_MyMessage3)
    assert Feature.is_feature(cls)

    schema = Feature._features_to_udf_spec([cls])
    assert len(schema) == 3
    assert list(schema.values()) == [String, Int64, String]


def test_flatten_schema_with_list_of_objects():
    class FileDir(Feature):
        name: str
        files: list[FileBasic]

    schema = FileDir._to_udf_spec()

    assert len(schema) == 2
    assert [item[0] for item in schema] == ["name", "files"]

    assert schema[0][1] == String
    assert schema[1][1].to_dict() == {"item_type": {"type": "JSON"}, "type": "Array"}


def test_flatten_schema_with_list_of_ints():
    class SomeInfo(Feature):
        name: str
        vals: list[int]

    schema = SomeInfo._to_udf_spec()

    assert len(schema) == 2
    assert [item[0] for item in schema] == ["name", "vals"]

    assert schema[0][1] == String
    assert schema[1][1].to_dict() == {"item_type": {"type": "Int64"}, "type": "Array"}


def test_unflatten_to_json():
    class _Child(Feature):
        type: int
        name: str = Field(default="test1")

    class _Parent(Feature):
        name: str
        child: _Child

    p = _Parent(name="parent1", child=_Child(type=12, name="child1"))

    flatten = p._flatten()
    assert _Parent._unflatten_to_json(flatten) == {
        "name": "parent1",
        "child": {"type": 12, "name": "child1"},
    }


def test_unflatten_to_json_list():
    class _Child(Feature):
        type: int
        name: str = Field(default="test1")

    class _Parent(Feature):
        name: str
        children: list[_Child]

    p = _Parent(
        name="parent1",
        children=[_Child(type=12, name="child1"), _Child(type=13, name="child2")],
    )

    flatten = p._flatten()
    json = _Parent._unflatten_to_json(flatten)
    assert json == {
        "name": "parent1",
        "children": [{"type": 12, "name": "child1"}, {"type": 13, "name": "child2"}],
    }


def test_unflatten_to_json_dict():
    class _Child(Feature):
        type: int
        address: str = Field(default="test1")

    class _Parent(Feature):
        name: str
        children: dict[str, _Child]

    p = _Parent(
        name="parent1",
        children={
            "child1": _Child(type=12, address="sf"),
            "child2": _Child(type=13, address="nyc"),
        },
    )

    flatten = p._flatten()
    json = _Parent._unflatten_to_json(flatten)
    assert json == {
        "name": "parent1",
        "children": {
            "child1": {"type": 12, "address": "sf"},
            "child2": {"type": 13, "address": "nyc"},
        },
    }


def test_unflatten_to_json_list_of_int():
    class _Child(Feature):
        types: list[int]
        name: str = Field(default="test1")

    child1 = _Child(name="n1", types=[14])
    assert _Child._unflatten_to_json(child1._flatten()) == {"name": "n1", "types": [14]}

    child2 = _Child(name="qwe", types=[1, 2, 3, 5])
    assert _Child._unflatten_to_json(child2._flatten()) == {
        "name": "qwe",
        "types": [1, 2, 3, 5],
    }


def test_unflatten_to_json_list_of_lists():
    class _Child(Feature):
        type: int
        name: str = Field(default="test1")

    class _Parent(Feature):
        name: str
        children: list[_Child]

    class _Company(Feature):
        name: str
        parents: list[_Parent]

    p = _Company(
        name="Co",
        parents=[_Parent(name="parent1", children=[_Child(type=12, name="child1")])],
    )

    assert _Company._unflatten_to_json(p._flatten()) == {
        "name": "Co",
        "parents": [{"name": "parent1", "children": [{"type": 12, "name": "child1"}]}],
    }
