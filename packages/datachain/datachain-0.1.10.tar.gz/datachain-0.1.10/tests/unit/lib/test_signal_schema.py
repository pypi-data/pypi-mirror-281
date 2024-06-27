import json
from typing import Optional

import pytest

from datachain.lib.feature import Feature
from datachain.lib.file import File
from datachain.lib.signal_schema import (
    SignalResolvingError,
    SignalSchema,
    SignalSchemaError,
)
from datachain.sql.types import Float, Int64, String


class MyType1(Feature):
    aa: int
    bb: str


class MyType2(Feature):
    name: str
    deep: MyType1


def test_deserialize_basic():
    stored = {"name": "str", "count": "int", "file": "File@1"}
    signals = SignalSchema.deserialize(stored)

    assert len(signals.values) == 3
    assert signals.values.keys() == stored.keys()
    assert list(signals.values.values()) == [str, int, File]


def test_deserialize_error():
    SignalSchema.deserialize({})

    with pytest.raises(SignalSchemaError):
        SignalSchema.deserialize(json.dumps({"name": "str"}))

    with pytest.raises(SignalSchemaError):
        SignalSchema.deserialize({"name": [1, 2, 3]})

    with pytest.raises(SignalSchemaError):
        SignalSchema.deserialize({"name": "unknown"})


def test_serialize_basic():
    schema = {
        "name": str,
        "age": float,
        "f": File,
    }
    signals = SignalSchema(schema).serialize()

    assert len(signals) == 3
    assert signals["name"] == "str"
    assert signals["age"] == "float"
    assert signals["f"] == "File@1"


def test_feature_schema_serialize_optional():
    schema = {
        "name": Optional[str],
        "feature": Optional[MyType1],
    }
    signals = SignalSchema(schema).serialize()

    assert len(signals) == 2
    assert signals["name"] == "str"
    assert signals["feature"] == "MyType1"


def test_serialize_from_column():
    signals = SignalSchema.from_column_types({"age": Float, "name": String}).values

    assert len(signals) == 2
    assert signals["name"] == str
    assert signals["age"] == float


def test_serialize_from_column_error():
    with pytest.raises(SignalSchemaError):
        SignalSchema.from_column_types({"age": Float, "wrong_type": File})


def test_to_udf_spec():
    signals = SignalSchema.deserialize(
        {
            "age": "float",
            "address": "str",
            "f": "File@1",
        }
    )

    spec = SignalSchema.to_udf_spec(signals)

    assert len(spec) == 2 + len(File.model_fields)

    assert "age" in spec
    assert spec["age"] == Float

    assert "address" in spec
    assert spec["address"] == String

    assert "f__name" in spec
    assert spec["f__name"] == String

    assert "f__size" in spec
    assert spec["f__size"] == Int64


def test_select():
    schema = SignalSchema.deserialize(
        {
            "age": "float",
            "address": "str",
            "f": "MyType1@1",
        }
    )

    new = schema.resolve("age", "f.aa", "f.bb")
    assert isinstance(new, SignalSchema)

    signals = new.values
    assert len(signals) == 3
    assert {"age", "f.aa", "f.bb"} == signals.keys()
    assert signals["age"] == float
    assert signals["f.aa"] == int
    assert signals["f.bb"] == str


def test_select_nested_names():
    schema = SignalSchema.deserialize(
        {
            "address": "str",
            "fr": "MyType2@1",
        }
    )

    fr_signals = schema.resolve("fr.deep").values
    assert "fr.deep" in fr_signals
    assert fr_signals["fr.deep"] == MyType1

    basic_signals = schema.resolve("fr.deep.aa", "fr.deep.bb").values
    assert "fr.deep.aa" in basic_signals
    assert "fr.deep.bb" in basic_signals
    assert basic_signals["fr.deep.aa"] == int
    assert basic_signals["fr.deep.bb"] == str


def test_prefix_tree():
    schema = SignalSchema.deserialize(
        {
            "address": "str",
            "fr": "MyType2@1",
        }
    )

    schema = schema.resolve("fr.deep.aa", "fr.deep.bb")
    tree = schema._get_prefix_tree()

    assert tree == {"fr": {"deep": {"aa": int, "bb": str}}}


def test_select_nested_errors():
    schema = SignalSchema.deserialize(
        {
            "address": "str",
            "fr": "MyType2@1",
        }
    )

    schema = schema.resolve("fr.deep.aa", "fr.deep.bb")

    with pytest.raises(SignalResolvingError):
        schema.resolve("some_random")

    with pytest.raises(SignalResolvingError):
        schema.resolve("fr")

    with pytest.raises(SignalResolvingError):
        schema.resolve("fr.deep")

    with pytest.raises(SignalResolvingError):
        schema.resolve("fr.deep.not_exist")


def test_get_file_signals_basic():
    schema = {
        "name": str,
        "age": float,
        "f": File,
    }
    assert SignalSchema(schema).get_file_signals() == ["f"]


def test_get_file_signals_nested():
    class _MyFile(File):
        ref: str
        nested_file: File

    schema = {"name": str, "age": float, "f": File, "my_f": _MyFile}

    assert SignalSchema(schema).get_file_signals() == ["f", "my_f", "my_f.nested_file"]
