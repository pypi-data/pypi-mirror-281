# pip install datamodel-code-generator
# pip install jmespath
#
import csv
import io
import json
import subprocess
import sys
import uuid
from collections.abc import Iterator
from typing import Any, Callable

import jmespath as jsp

from datachain.lib.feature_utils import pydantic_to_feature  # noqa: F401
from datachain.lib.file import File

# from datachain.lib.dc import C, DataChain


def generate_uuid():
    return uuid.uuid4()  # Generates a random UUID.


# JSON decoder
def load_json_from_string(json_string):
    try:
        data = json.loads(json_string)
        print("Successfully parsed JSON", file=sys.stderr)
        return data
    except json.JSONDecodeError:
        print("Failed to decode JSON: The string is not formatted correctly.")
    return None


# Read valid JSON and return a data object sample
def process_json(data_string, jmespath):
    json_dict = load_json_from_string(data_string)
    if jmespath:
        json_dict = jsp.search(jmespath, json_dict)
        # we allow non-list JSONs here to print the root schema
        # but if jmespath expression is given, we assume a list
        if not isinstance(json_dict, list):
            raise ValueError("JMESPATH expression must resolve to a list")
            return None
        json_dict = json_dict[0]  # sample the first object
    return json.dumps(json_dict)


# Print a dynamic datamodel-codegen output from JSON or CSV on stdout
def read_schema(source_file, data_type="csv", expr=None):
    data_string = ""
    uid_str = str(generate_uuid()).replace("-", "")  # comply with Python class names
    # using uiid to get around issue #1617
    model_name = f"Model{uid_str}"
    try:
        with source_file.open() as fd:  # CSV can be larger than memory
            if data_type == "csv":
                data_string += fd.readline().decode("utf-8", "ignore").replace("\r", "")
                data_string += fd.readline().decode("utf-8", "ignore").replace("\r", "")
            else:
                data_string = fd.read()  # other meta must fit into RAM
    except OSError as e:
        print(f"An unexpected file error occurred: {e}")
        return
    if data_type == "json":
        data_string = process_json(data_string, expr)
    command = [
        "datamodel-codegen",
        "--input-file-type",
        data_type,
        "--class-name",
        model_name,
    ]
    try:
        result = subprocess.run(
            command,  # noqa: S603
            input=data_string,
            text=True,
            capture_output=True,
            check=True,
        )
        model_output = (
            result.stdout
        )  # This will contain the output from datamodel-codegen
    except subprocess.CalledProcessError as e:
        model_output = f"An error occurred in datamodel-codegen: {e.stderr}"
    print(f"{model_output}")
    print("\n" + f"spec=pydantic_to_feature({model_name})" + "\n")


#
# UDF mapper which calls chain in the setup to infer the dynamic schema
#
def read_meta(
    spec=None, schema_from=None, meta_type="json", jmespath=None, show_schema=False
) -> Callable:
    from datachain.lib.dc import DataChain

    # ugly hack: datachain is run redirecting printed outputs to a variable
    if schema_from:
        captured_output = io.StringIO()
        current_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            chain = (
                DataChain.from_storage(schema_from)
                .limit(1)
                .map(  # dummy column created (#1615)
                    meta_schema=lambda file: read_schema(
                        file, data_type=meta_type, expr=jmespath
                    ),
                    output=str,
                )
            )
            # dummy executor (#1616)
            chain.save()
        finally:
            sys.stdout = current_stdout
        model_output = captured_output.getvalue()
        captured_output.close()
        if show_schema:
            print(f"{model_output}")
        # Below 'spec' should be a dynamically converted Feature from Pydantic datamodel
        if not spec:
            local_vars: dict[str, Any] = {}
            exec(model_output, globals(), local_vars)  # noqa: S102
            spec = local_vars["spec"]

    if not (spec) and not (schema_from):
        raise ValueError(
            "Must provide a static schema in spec: or metadata sample in schema_from:"
        )

    #
    # UDF mapper parsing a JSON or CSV file using schema spec
    #
    def parse_data(
        file: File, data_model=spec, meta_type=meta_type, jmespath=jmespath
    ) -> Iterator[spec]:
        if meta_type == "csv":
            with (
                file.open() as fd
            ):  # TODO: if schema is statically given, should allow CSV without headers
                reader = csv.DictReader(fd)
                for row in reader:  # CSV can be larger than memory
                    json_string = json.dumps(row)
                    yield data_model.model_validate_json(json_string)
        if meta_type == "json":
            try:
                with file.open() as fd:  # JSON must fit into RAM
                    data_string = fd.read()
            except OSError as e:
                print(f"An unexpected file error occurred: {e}")
            json_object = load_json_from_string(data_string)
            if jmespath:
                json_object = jsp.search(jmespath, json_object)
            if not isinstance(json_object, list):
                raise ValueError("JSON expression must resolve in a list of objects")
            for json_dict in json_object:
                json_string = json.dumps(json_dict)
                yield data_model.model_validate_json(json_string)

    return parse_data
