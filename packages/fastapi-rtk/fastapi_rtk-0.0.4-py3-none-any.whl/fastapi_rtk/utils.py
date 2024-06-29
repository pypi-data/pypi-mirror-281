import csv
import inspect
import logging
from typing import Dict, Type

from fastapi import Depends
from pydantic import BaseModel, Field, create_model

log = logging.getLogger(__name__)


class Line(object):
    def __init__(self):
        self._line = None

    def write(self, line):
        self._line = line

    def read(self):
        return self._line


def both_are_filled_or_empty(v1: str, v2: str) -> None:
    """
    Checks if both values are either filled or empty.

    Args:
        v1 (str): The first value to check.
        v2 (str): The second value to check.

    Raises:
        ValueError: If one value is filled and the other is empty.

    Returns:
        None
    """
    if bool(v1) != bool(v2):
        raise ValueError("Both values must be filled or empty")


def dump_schema(schema: BaseModel):
    """
    Dump the given schema into a dictionary and remove any nested dictionaries that should be ignored.

    Args:
        schema (BaseModel): The schema to be dumped.

    Returns:
        dict: The dumped schema.
    """
    from .schemas import IgnoredData

    data = schema.model_dump()
    for key in list(data.keys()):
        if isinstance(data[key], dict):
            try:
                IgnoredData.model_validate(data[key], strict=True)
                del data[key]
            except:
                pass
    return data


async def generate_report(data, list_columns, label_columns):
    line = Line()
    writer = csv.writer(line, delimiter=",")

    # header
    labels = []
    for key in list_columns:
        labels.append(label_columns[key])

    # rows
    writer.writerow(labels)
    yield line.read()

    async for chunk in data:
        for item in chunk:
            row = []
            for key in list_columns:
                value = getattr(item, key)
                # if value is a function, call it
                if callable(value):
                    try:
                        value = value()
                    except Exception as e:
                        value = "Error calling function"
                if value is None:
                    value = ""
                row.append(str(value))
            writer.writerow(row)
            yield line.read()


def merge_schema(
    schema: BaseModel,
    fields: Dict[str, tuple[type, Field]],
    only_update=False,
    name: str | None = None,
) -> Type[BaseModel]:
    """
    Replace or add fields to the given schema.

    Args:
        schema (BaseModel): The schema to be updated.
        fields (Dict[str, tuple[type, Field]]): The fields to be added or updated.
        only_update (bool): If True, only update the fields with the same name. Otherwise, add new fields.
        name (str, optional): The name of the new schema. Defaults to None.

    Returns:
        BaseModel: The updated schema.
    """
    name = name or schema.__name__
    new_fields = dict()
    if only_update:
        for key, value in schema.model_fields.items():
            if key in fields:
                val = fields[key]
                if isinstance(val, tuple):
                    new_fields[key] = val
                else:
                    new_fields[key] = (value.annotation, val)
    else:
        new_fields = fields

    return create_model(
        name,
        **new_fields,
        __base__=schema,
    )


def update_self_signature(cls, f):
    """
    Update the signature of a function to replace the first parameter with 'self' as a dependency.

    Args:
        cls (class): The class that the function belongs to.
        f (function): The function to be updated.

    Returns:
        None
    """
    # Get the function's parameters
    old_signature = inspect.signature(f)
    old_parameters = list(old_signature.parameters.values())
    old_first_parameter = old_parameters[0]

    # If the first parameter is self, replace it
    if old_first_parameter.name == "self":
        new_first_parameter = old_first_parameter.replace(default=Depends(lambda: cls))

        new_parameters = [new_first_parameter] + [
            parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
            for parameter in old_parameters[1:]
        ]
        new_signature = old_signature.replace(parameters=new_parameters)

        setattr(
            f, "__signature__", new_signature
        )  # Set the new signature to the function
