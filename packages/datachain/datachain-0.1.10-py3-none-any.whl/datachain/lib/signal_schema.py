import copy
from collections.abc import Sequence
from typing import Any, Optional, Union, get_args, get_origin

from datachain.catalog import Catalog
from datachain.lib.feature import (
    DATACHAIN_TO_TYPE,
    DEFAULT_DELIMITER,
    NAMES_TO_TYPES,
    Feature,
    FeatureType,
    convert_type_to_datachain,
)
from datachain.lib.feature_registry import Registry
from datachain.lib.file import File
from datachain.lib.utils import DataChainParamsError


class SignalSchemaError(DataChainParamsError):
    pass


class SignalResolvingError(SignalSchemaError):
    def __init__(self, path: Optional[list[str]], msg: str):
        name = " '" + ".".join(path) + "'" if path else ""
        super().__init__(f"cannot resolve signal name{name}: {msg}")


class SignalResolvingTypeError(SignalResolvingError):
    def __init__(self, method: str, field):
        super().__init__(
            None,
            f"{method} supports only `str` type"
            f" while '{field}' has type '{type(field)}'",
        )


class SignalSchema:
    def __init__(self, values: dict[str, FeatureType]):
        self.values = values

    @staticmethod
    def from_column_types(col_types: dict[str, Any]) -> "SignalSchema":
        signals: dict[str, FeatureType] = {}
        for field, type_ in col_types.items():
            type_ = DATACHAIN_TO_TYPE.get(type_, None)
            if type_ is None:
                raise SignalSchemaError(
                    f"signal schema cannot be obtained for column '{field}':"
                    f" unsupported type '{type_}'"
                )
            signals[field] = type_
        return SignalSchema(signals)

    def serialize(self) -> dict[str, str]:
        signals = {}
        for name, fr_type in self.values.items():
            if Feature.is_feature(fr_type):
                signals[name] = fr_type._name()  # type: ignore[union-attr]
            else:
                orig = get_origin(fr_type)
                args = get_args(fr_type)
                # Check if fr_type is Optional
                if orig == Union and len(args) == 2 and (type(None) in args):
                    fr_type = args[0]
                signals[name] = fr_type.__name__
        return signals

    @staticmethod
    def deserialize(schema: dict[str, str]) -> "SignalSchema":
        if not isinstance(schema, dict):
            raise SignalSchemaError(f"cannot deserialize signal schema: {schema}")

        signals: dict[str, FeatureType] = {}
        for signal, type_name in schema.items():
            try:
                fr = NAMES_TO_TYPES.get(type_name, None)
                if not fr:
                    type_name, version = Registry.parse_name_version(type_name)
                    fr = Registry.get(type_name, version)
            except TypeError as err:
                raise SignalSchemaError(
                    f"cannot deserialize '{signal}': {err}"
                ) from err

            if not fr:
                raise SignalSchemaError(
                    f"cannot deserialize '{signal}': unsupported type '{type_name}'"
                )
            signals[signal] = fr

        return SignalSchema(signals)

    def to_udf_spec(self) -> dict[str, Any]:
        res = {}
        for signal, fr_type in self.values.items():
            signal_path = signal.split(".")

            if Feature.is_feature(fr_type):
                delimiter = fr_type._delimiter  # type: ignore[union-attr]
                if fr_type._is_shallow:  # type: ignore[union-attr]
                    signal_path = []
                spec = fr_type._to_udf_spec()  # type: ignore[union-attr]
                for attr, value in spec:
                    name_path = [*signal_path, attr]
                    res[delimiter.join(name_path)] = value
            else:
                delimiter = DEFAULT_DELIMITER
                try:
                    type_ = convert_type_to_datachain(fr_type)
                except TypeError as err:
                    raise SignalSchemaError(
                        f"unsupported type '{fr_type}' for signal '{signal}'"
                    ) from err
                res[delimiter.join(signal_path)] = type_
        return res

    def row_to_objs(self, row: Sequence[Any]) -> list[FeatureType]:
        objs = []
        pos = 0
        for fr_type in self.values.values():
            if Feature.is_feature(fr_type):
                j, pos = fr_type._unflatten_to_json_pos(row, pos)  # type: ignore[union-attr]
                objs.append(fr_type(**j))
            else:
                objs.append(row[pos])
                pos += 1
        return objs  # type: ignore[return-value]

    def contains_file(self) -> bool:
        return any(
            fr._is_file  # type: ignore[union-attr]
            for fr in self.values.values()
            if Feature.is_feature(fr)
        )

    def slice(self, keys: Sequence[str]) -> "SignalSchema":
        return SignalSchema({k: v for k, v in self.values.items() if k in keys})

    def row_to_features(self, row: Sequence, catalog: Catalog) -> list[FeatureType]:
        res = []
        pos = 0
        for fr_cls in self.values.values():
            if not Feature.is_feature(fr_cls):
                res.append(row[pos])
                pos += 1
            else:
                json, pos = fr_cls._unflatten_to_json_pos(row, pos)  # type: ignore[union-attr]
                obj = fr_cls(**json)
                if isinstance(obj, File):
                    obj._set_stream(catalog)
                res.append(obj)
        return res

    def db_signals(self) -> list[str]:
        res = []
        for name, fr_cls in self.values.items():
            prefixes = name.split(".")

            if not Feature.is_feature(fr_cls):
                res.append(DEFAULT_DELIMITER.join(prefixes))
            else:
                if fr_cls._is_shallow:  # type: ignore[union-attr]
                    prefixes = []
                spec = fr_cls._to_udf_spec()  # type: ignore[union-attr]
                new_db_signals = [
                    DEFAULT_DELIMITER.join([*prefixes, name]) for name, type_ in spec
                ]
                res.extend(new_db_signals)
        return res

    def resolve(self, *names: str) -> "SignalSchema":
        schema = {}
        tree = self._get_prefix_tree()
        for field in names:
            if not isinstance(field, str):
                raise SignalResolvingTypeError("select()", field)

            path = field.split(".")
            cls, position = self._find_feature_in_prefix_tree(tree, path)
            schema[field] = self._find_in_feature(cls, path, position)

        return SignalSchema(schema)

    def select_except_signals(self, *args: str) -> "SignalSchema":
        schema = copy.deepcopy(self.values)
        for field in args:
            if not isinstance(field, str):
                raise SignalResolvingTypeError("select_except()", field)

            if field not in self.values:
                raise SignalResolvingError(
                    field.split("."),
                    "select_except() error - the feature name does not exist or "
                    "inside of feature (not supported)",
                )
            del schema[field]

        return SignalSchema(schema)

    def _get_prefix_tree(self) -> dict[str, Any]:
        tree: dict[str, Any] = {}
        for name, fr_cls in self.values.items():
            prefixes = name.split(".")

            curr_tree = {}
            curr_prefix = ""
            for prefix in prefixes:
                if not curr_prefix:
                    curr_prefix = prefix
                    curr_tree = tree
                else:
                    new_tree = curr_tree.get(curr_prefix, {})  #
                    curr_tree[curr_prefix] = new_tree
                    curr_tree = new_tree
                    curr_prefix = prefix

            curr_tree[curr_prefix] = fr_cls
        return tree

    def _find_feature_in_prefix_tree(
        self, tree: dict, path: list[str]
    ) -> tuple[FeatureType, int]:
        for i in range(len(path)):
            prefix = path[i]
            if prefix not in tree:
                raise SignalResolvingError(path, f"'{prefix}' is not found")
            val = tree[prefix]
            if not isinstance(val, dict):
                return val, i + 1
            tree = val

        next_keys = ", ".join(tree.keys())
        raise SignalResolvingError(
            path,
            f"it's not a terminal value or feature, next item might be '{next_keys}'",
        )

    def _find_in_feature(
        self, cls: FeatureType, path: list[str], position: int
    ) -> FeatureType:
        if position == len(path):
            return cls

        name = path[position]
        field_info = cls.model_fields.get(name, None)  # type: ignore[union-attr]
        if field_info is None:
            raise SignalResolvingError(
                path, f"field '{name}' is not found in Feature '{cls.__name__}'"
            )

        return self._find_in_feature(field_info.annotation, path, position + 1)  # type: ignore[arg-type]

    def clone_without_file_signals(self) -> "SignalSchema":
        schema = copy.deepcopy(self.values)

        for signal in File._datachain_column_types:
            if signal in schema:
                del schema[signal]
        return SignalSchema(schema)

    def merge(
        self,
        right_schema: "SignalSchema",
        rname: str,
    ) -> "SignalSchema":
        schema_right = {
            rname + key if key in self.values else key: type_
            for key, type_ in right_schema.values.items()
        }

        return SignalSchema(self.values | schema_right)

    def get_file_signals(self) -> list[str]:
        res = []
        for name, fr in self.values.items():
            if Feature.is_feature(fr):
                signals = fr.get_file_signals([name])  # type: ignore[union-attr]
                for signal in signals:
                    res.append(".".join(signal))
        return res
