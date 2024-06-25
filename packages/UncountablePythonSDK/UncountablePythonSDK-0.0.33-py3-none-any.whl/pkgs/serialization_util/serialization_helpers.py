import datetime
import enum
from collections.abc import Callable, Mapping, Sequence
from decimal import Decimal
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Protocol,
    TypeVar,
    Union,
    overload,
)

from pkgs.argument_parser import snake_to_camel_case
from pkgs.serialization import (
    MISSING_SENTRY,
    OpaqueKey,
    get_serial_class_data,
)

from ._get_type_for_serialization import SerializationType, get_serialization_type

# Inlined types which otherwise would import from types/base.py
JsonScalar = Union[str, float, bool, Decimal, None, datetime.datetime, datetime.date]
if TYPE_CHECKING:
    JsonValue = Union[JsonScalar, Mapping[str, "JsonValue"], Sequence["JsonValue"]]
else:
    JsonValue = Union[JsonScalar, dict[str, Any], list[Any]]

T = TypeVar("T")


class Dataclass(Protocol):
    __dataclass_fields__: ClassVar[dict]  # type: ignore[type-arg,unused-ignore]


def identity(x: T) -> T:
    return x


def key_convert_to_camelcase(o: Any) -> str:
    if isinstance(o, OpaqueKey):
        return o
    if isinstance(o, enum.Enum):
        return o.value  # type: ignore[no-any-return]
    if isinstance(o, str):
        return snake_to_camel_case(o)
    return o  # type: ignore[no-any-return]


def _convert_dict(d: dict[str, Any]) -> dict[str, JsonValue]:
    return {
        key_convert_to_camelcase(k): serialize_for_api(v)
        for k, v in d.items()
        if v != MISSING_SENTRY
    }


def _serialize_dict(d: dict[str, Any]) -> dict[str, JsonValue]:
    return {k: serialize_for_storage(v) for k, v in d.items() if v != MISSING_SENTRY}


def _convert_dataclass(d: Dataclass) -> dict[str, JsonValue]:
    dct = type(d)
    scd = get_serial_class_data(dct)

    def key_convert(key: str) -> str:
        if scd.has_unconverted_key(key):
            return key
        return key_convert_to_camelcase(key)

    def value_convert(key: str, value: Any) -> JsonValue:
        if scd.has_to_string_value(key):
            # Limit to types we know we need to support to avoid surprises
            # Generics, like List/Dict would need to be per-value stringified
            assert isinstance(value, (Decimal, int))
            return str(value)
        if scd.has_unconverted_value(key):
            return value  # type: ignore[no-any-return]
        return serialize_for_api(value)  # type: ignore[no-any-return,unused-ignore]

    return {
        key_convert(k): (value_convert(k, v) if v is not None else None)
        for k, v in d.__dict__.items()
        if v != MISSING_SENTRY
    }


_SERIALIZATION_FUNCS_STANDARD = {
    SerializationType.ENUM: lambda x: str(x.value),
    SerializationType.DATE: lambda x: x.isoformat(),
    SerializationType.TIMEDELTA: lambda x: x.total_seconds(),
    SerializationType.UNKNOWN: identity,
}

_CONVERSION_SERIALIZATION_FUNCS: dict[SerializationType, Callable[[Any], JsonValue]] = {
    **_SERIALIZATION_FUNCS_STANDARD,
    SerializationType.NAMED_TUPLE: lambda x: _convert_dict(x._asdict()),
    SerializationType.ITERABLE: lambda x: [serialize_for_api(v) for v in x],
    SerializationType.DICT: _convert_dict,
    SerializationType.DATACLASS: _convert_dataclass,
}


@overload
def serialize_for_api(obj: None) -> None: ...


@overload
def serialize_for_api(obj: dict[str, Any]) -> dict[str, JsonValue]: ...


@overload
def serialize_for_api(obj: Dataclass) -> dict[str, JsonValue]: ...


@overload
def serialize_for_api(obj: Any) -> JsonValue: ...


def serialize_for_api(obj: Any) -> JsonValue:
    """
    Serialize to a parsed-JSON format suitably encoded for API output.

    Use the CachedParser.parse_api to parse this data.
    """
    serialization_type = get_serialization_type(type(obj))  # type: ignore
    return _CONVERSION_SERIALIZATION_FUNCS[serialization_type](obj)


_SERIALIZATION_FUNCS_DICT: dict[
    SerializationType, Callable[[Any], dict[str, JsonValue]]
] = {
    SerializationType.DICT: _serialize_dict,
    SerializationType.DATACLASS: lambda x: _serialize_dict(x.__dict__),
}


_SERIALIZATION_FUNCS: dict[SerializationType, Callable[[Any], JsonValue]] = {
    **_SERIALIZATION_FUNCS_STANDARD,
    **_SERIALIZATION_FUNCS_DICT,
    SerializationType.NAMED_TUPLE: lambda x: _serialize_dict(x._asdict()),
    SerializationType.ITERABLE: lambda x: [serialize_for_storage(v) for v in x],
}


def serialize_for_storage(obj: Any) -> JsonValue:
    """
    Convert a value into the pseudo-JSON form for
    storage in the DB, file, or other non-API use.

    Use the CachedParser.parse_storage to parse this data.
    """
    serialization_type = get_serialization_type(type(obj))  # type: ignore
    return _SERIALIZATION_FUNCS[serialization_type](obj)


def serialize_for_storage_dict(obj: dict | Dataclass) -> dict[str, JsonValue]:  # type: ignore[type-arg]
    """
    Same as serialize for storage but guarantees outer object is a dictionary
    """
    serialization_type = get_serialization_type(type(obj))
    return _SERIALIZATION_FUNCS_DICT[serialization_type](obj)
