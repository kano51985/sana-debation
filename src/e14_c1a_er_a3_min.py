"""Pure verifier for the E14 C1a ER-A3-MIN semantic-source package.

The verifier validates supplied bytes only.  It deliberately has no package builder, filesystem
source resolver, network client, clock, persistence, authority check, compatibility evaluator, or
operational effect.  A successful result proves package shape and declared schema/reader parity;
it does not prove source truth or source authority.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import hashlib
import json
import re
from types import MappingProxyType
from typing import Any, Final


SCHEMA: Final = "sana.e14.c1a.er-a3-min.v1"
PROFILE: Final = "C1A_ER_A3_MIN_READ_ONLY_V1"
CANDIDATE: Final = "A"
ANCHOR_ALIASES: Final = frozenset({"A1", "H1"})
CANONICAL_PROFILE_ALIAS: Final = "J1"
CANONICAL_PROFILE_ID: Final = "RFC8785_JCS_IJSON_V1"
MAX_RAW_BYTES: Final = 131_072
MAX_SAFE_INTEGER: Final = 9_007_199_254_740_991

FAILURE_CODES: Final = (
    "ER_A3_RAW_TOO_LARGE",
    "ER_A3_JSON_BOM",
    "ER_A3_JSON_INVALID_UTF8",
    "ER_A3_JSON_INVALID",
    "ER_A3_JSON_DUPLICATE_KEY",
    "ER_A3_PACKAGE_FIELD_SET",
    "ER_A3_SCHEMA_UNSUPPORTED",
    "ER_A3_PROFILE_UNSUPPORTED",
    "ER_A3_CANDIDATE_UNSUPPORTED",
    "ER_A3_PACKAGE_INVALID",
    "ER_A3_ANCHOR_SET_INVALID",
    "ER_A3_SOURCE_INVALID",
    "ER_A3_FIELD_SCHEMA_INVALID",
    "ER_A3_READER_CONTRACT_INVALID",
    "ER_A3_SCHEMA_READER_MISMATCH",
)

__all__ = (
    "ANCHOR_ALIASES",
    "CANONICAL_PROFILE_ALIAS",
    "CANONICAL_PROFILE_ID",
    "CANDIDATE",
    "FAILURE_CODES",
    "MAX_RAW_BYTES",
    "PROFILE",
    "SCHEMA",
    "ERA3MinError",
    "VerifiedERA3MinPackageV1",
    "verify_package",
)


_SHA256_RE = re.compile(r"^[0-9A-F]{64}$")
_IDENTIFIER_RE = re.compile(r"^[A-Z][A-Z0-9_]*(?:\.v[1-9][0-9]*)?$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_WIRE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_RELATIVE_PATH_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
_TOKEN = object()


class ERA3MinError(ValueError):
    """Stable typed verification error."""

    def __init__(self, code: str, *, pointer: str = "", detail: str = "") -> None:
        if code not in FAILURE_CODES:
            raise ValueError(f"unknown ER-A3-MIN failure code {code!r}")
        self.code = code
        self.pointer = pointer
        self.detail = detail
        message = code
        if pointer:
            message += f" at {pointer}"
        if detail:
            message += f": {detail}"
        super().__init__(message)


@dataclass(frozen=True, slots=True, init=False)
class VerifiedERA3MinPackageV1:
    """Nominal immutable result created only by :func:`verify_package`."""

    payload: Mapping[str, Any]
    raw_sha256: str
    package_shape: str
    declared_schema_reader_parity: str
    source_truth: str
    source_authority: str
    compatibility: str
    authority_effect: str
    next_stage_authorized: bool

    def __init__(self, payload: Mapping[str, Any], raw_sha256: str, *, _token: object) -> None:
        if _token is not _TOKEN:
            raise TypeError("VerifiedERA3MinPackageV1 is created only by verify_package")
        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "raw_sha256", raw_sha256)
        object.__setattr__(self, "package_shape", "VALID")
        object.__setattr__(self, "declared_schema_reader_parity", "MATCHED")
        object.__setattr__(self, "source_truth", "NOT_PROVEN_BY_VALIDATOR")
        object.__setattr__(self, "source_authority", "NOT_PROVEN_BY_VALIDATOR")
        object.__setattr__(self, "compatibility", "UNASSESSED")
        object.__setattr__(self, "authority_effect", "NONE")
        object.__setattr__(self, "next_stage_authorized", False)


def _fail(code: str, pointer: str, detail: str) -> None:
    raise ERA3MinError(code, pointer=pointer, detail=detail)


def _json_pointer(parent: str, key: str | int) -> str:
    token = str(key).replace("~", "~0").replace("/", "~1")
    return f"{parent}/{token}" if parent else f"/{token}"


def _object(value: object, pointer: str, code: str) -> dict[str, Any]:
    if type(value) is not dict:
        _fail(code, pointer or "/", "expected object")
    return value


def _exact_fields(
    value: dict[str, Any], expected: tuple[str, ...], pointer: str, code: str
) -> None:
    actual = set(value)
    required = set(expected)
    if actual != required:
        missing = sorted(required - actual)
        extra = sorted(actual - required)
        _fail(code, pointer or "/", f"field set mismatch; missing={missing}, extra={extra}")


def _string(
    value: object,
    pointer: str,
    code: str,
    *,
    minimum: int = 1,
    maximum: int = 2048,
) -> str:
    if type(value) is not str or not minimum <= len(value) <= maximum:
        _fail(code, pointer, f"expected string length {minimum}..{maximum}")
    return value


def _boolean(value: object, pointer: str, code: str) -> bool:
    if type(value) is not bool:
        _fail(code, pointer, "expected boolean")
    return value


def _integer(value: object, pointer: str, code: str, *, minimum: int, maximum: int) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        _fail(code, pointer, f"expected integer in {minimum}..{maximum}")
    return value


def _identifier(value: object, pointer: str, code: str) -> str:
    text = _string(value, pointer, code, maximum=128)
    if not _IDENTIFIER_RE.fullmatch(text):
        _fail(code, pointer, "invalid identifier")
    return text


def _version(value: object, pointer: str, code: str) -> str:
    text = _string(value, pointer, code, maximum=64)
    if not _VERSION_RE.fullmatch(text):
        _fail(code, pointer, "invalid version")
    return text


def _sha256(value: object, pointer: str, code: str) -> str:
    text = _string(value, pointer, code, minimum=64, maximum=64)
    if not _SHA256_RE.fullmatch(text):
        _fail(code, pointer, "expected 64 uppercase hexadecimal characters")
    return text


def _relative_path(value: object, pointer: str, code: str) -> str:
    text = _string(value, pointer, code, maximum=512)
    if (
        not _RELATIVE_PATH_RE.fullmatch(text)
        or "\\" in text
        or text.startswith("/")
        or ":" in text
        or any(segment in {"", ".", ".."} for segment in text.split("/"))
    ):
        _fail(code, pointer, "expected normalized repository-relative path")
    return text


def _string_list(
    value: object,
    pointer: str,
    code: str,
    *,
    maximum_items: int,
    maximum_length: int,
) -> tuple[str, ...]:
    if type(value) is not list or not 1 <= len(value) <= maximum_items:
        _fail(code, pointer, f"expected array length 1..{maximum_items}")
    result = tuple(
        _string(item, _json_pointer(pointer, index), code, maximum=maximum_length)
        for index, item in enumerate(value)
    )
    if len(set(result)) != len(result):
        _fail(code, pointer, "duplicate array value")
    return result


def _source_span(value: object, pointer: str) -> tuple[str, str, int, int]:
    node = _object(value, pointer, "ER_A3_SOURCE_INVALID")
    _exact_fields(
        node,
        ("path", "sha256", "start_line", "end_line"),
        pointer,
        "ER_A3_SOURCE_INVALID",
    )
    path = _relative_path(node["path"], f"{pointer}/path", "ER_A3_SOURCE_INVALID")
    digest = _sha256(node["sha256"], f"{pointer}/sha256", "ER_A3_SOURCE_INVALID")
    start = _integer(
        node["start_line"], f"{pointer}/start_line", "ER_A3_SOURCE_INVALID", minimum=1, maximum=1_000_000
    )
    end = _integer(
        node["end_line"], f"{pointer}/end_line", "ER_A3_SOURCE_INVALID", minimum=1, maximum=1_000_000
    )
    if end < start:
        _fail("ER_A3_SOURCE_INVALID", pointer, "end_line precedes start_line")
    return path, digest, start, end


def _spans(value: object, pointer: str, *, maximum_items: int) -> tuple[tuple[str, str, int, int], ...]:
    if type(value) is not list or not 1 <= len(value) <= maximum_items:
        _fail("ER_A3_SOURCE_INVALID", pointer, f"expected array length 1..{maximum_items}")
    result = tuple(_source_span(item, _json_pointer(pointer, index)) for index, item in enumerate(value))
    if len(set(result)) != len(result):
        _fail("ER_A3_SOURCE_INVALID", pointer, "duplicate source span")
    return result


def _accountable_source(value: object, pointer: str) -> None:
    node = _object(value, pointer, "ER_A3_SOURCE_INVALID")
    _exact_fields(
        node,
        ("source_id", "authority_status", "authority_scope", "spans", "limitations"),
        pointer,
        "ER_A3_SOURCE_INVALID",
    )
    _identifier(node["source_id"], f"{pointer}/source_id", "ER_A3_SOURCE_INVALID")
    if node["authority_status"] != "ACCOUNTABLE_SOURCE_IDENTIFIED":
        _fail("ER_A3_SOURCE_INVALID", f"{pointer}/authority_status", "source authority not identified")
    _string(node["authority_scope"], f"{pointer}/authority_scope", "ER_A3_SOURCE_INVALID", maximum=1024)
    _spans(node["spans"], f"{pointer}/spans", maximum_items=32)
    _string_list(
        node["limitations"],
        f"{pointer}/limitations",
        "ER_A3_SOURCE_INVALID",
        maximum_items=32,
        maximum_length=1024,
    )


def _legal_domain(value: object, pointer: str, code: str) -> tuple[Any, ...]:
    node = _object(value, pointer, code)
    kind = node.get("kind")
    if kind == "STRING_ENUM":
        _exact_fields(node, ("kind", "values"), pointer, code)
        values = _string_list(
            node["values"], pointer + "/values", code, maximum_items=128, maximum_length=256
        )
        return kind, values
    if kind == "INTEGER_RANGE":
        _exact_fields(node, ("kind", "minimum", "maximum"), pointer, code)
        minimum = _integer(
            node["minimum"], pointer + "/minimum", code, minimum=-MAX_SAFE_INTEGER, maximum=MAX_SAFE_INTEGER
        )
        maximum = _integer(
            node["maximum"], pointer + "/maximum", code, minimum=-MAX_SAFE_INTEGER, maximum=MAX_SAFE_INTEGER
        )
        if maximum < minimum:
            _fail(code, pointer, "maximum is less than minimum")
        return kind, minimum, maximum
    if kind == "BOOLEAN":
        _exact_fields(node, ("kind",), pointer, code)
        return (kind,)
    if kind == "OBJECT_SCHEMA_REF":
        _exact_fields(node, ("kind", "schema_id", "schema_version", "schema_sha256"), pointer, code)
        return (
            kind,
            _identifier(node["schema_id"], pointer + "/schema_id", code),
            _version(node["schema_version"], pointer + "/schema_version", code),
            _sha256(node["schema_sha256"], pointer + "/schema_sha256", code),
        )
    _fail(code, pointer + "/kind", "unsupported legal-domain kind")


def _field_schema(value: object, pointer: str) -> dict[str, Any]:
    code = "ER_A3_FIELD_SCHEMA_INVALID"
    node = _object(value, pointer, code)
    _exact_fields(
        node,
        ("schema_version", "wire_name", "json_type", "required", "default_behavior", "legal_domain"),
        pointer,
        code,
    )
    schema_version = _version(node["schema_version"], pointer + "/schema_version", code)
    wire_name = _string(node["wire_name"], pointer + "/wire_name", code, maximum=64)
    if not _WIRE_NAME_RE.fullmatch(wire_name):
        _fail(code, pointer + "/wire_name", "invalid wire name")
    json_type = node["json_type"]
    if json_type not in {"STRING", "INTEGER", "BOOLEAN", "OBJECT"}:
        _fail(code, pointer + "/json_type", "unsupported JSON type")
    required = _boolean(node["required"], pointer + "/required", code)
    if node["default_behavior"] != "NO_DEFAULT":
        _fail(code, pointer + "/default_behavior", "defaults are forbidden")
    domain = _legal_domain(node["legal_domain"], pointer + "/legal_domain", code)
    expected_domain = {
        "STRING": "STRING_ENUM",
        "INTEGER": "INTEGER_RANGE",
        "BOOLEAN": "BOOLEAN",
        "OBJECT": "OBJECT_SCHEMA_REF",
    }[json_type]
    if domain[0] != expected_domain:
        _fail(code, pointer + "/legal_domain", "legal domain does not match JSON type")
    return {
        "schema_version": schema_version,
        "wire_name": wire_name,
        "json_type": json_type,
        "required": required,
        "default_behavior": "NO_DEFAULT",
        "legal_domain": domain,
    }


def _reader_contract(value: object, pointer: str) -> dict[str, Any]:
    code = "ER_A3_READER_CONTRACT_INVALID"
    node = _object(value, pointer, code)
    _exact_fields(
        node,
        (
            "reader_id",
            "reader_version",
            "consumes_schema_version",
            "wire_name",
            "json_type",
            "required",
            "default_behavior",
            "legal_domain",
            "unknown_input_behavior",
            "interpretation",
        ),
        pointer,
        code,
    )
    reader_id = _identifier(node["reader_id"], pointer + "/reader_id", code)
    reader_version = _version(node["reader_version"], pointer + "/reader_version", code)
    consumes = _version(node["consumes_schema_version"], pointer + "/consumes_schema_version", code)
    wire_name = _string(node["wire_name"], pointer + "/wire_name", code, maximum=64)
    if not _WIRE_NAME_RE.fullmatch(wire_name):
        _fail(code, pointer + "/wire_name", "invalid wire name")
    json_type = node["json_type"]
    if json_type not in {"STRING", "INTEGER", "BOOLEAN", "OBJECT"}:
        _fail(code, pointer + "/json_type", "unsupported JSON type")
    required = _boolean(node["required"], pointer + "/required", code)
    if node["default_behavior"] != "NO_DEFAULT":
        _fail(code, pointer + "/default_behavior", "defaults are forbidden")
    domain = _legal_domain(node["legal_domain"], pointer + "/legal_domain", code)
    expected_domain = {
        "STRING": "STRING_ENUM",
        "INTEGER": "INTEGER_RANGE",
        "BOOLEAN": "BOOLEAN",
        "OBJECT": "OBJECT_SCHEMA_REF",
    }[json_type]
    if domain[0] != expected_domain:
        _fail(code, pointer + "/legal_domain", "legal domain does not match JSON type")
    if node["unknown_input_behavior"] != "REJECT":
        _fail(code, pointer + "/unknown_input_behavior", "unknown input must be rejected")
    _string(node["interpretation"], pointer + "/interpretation", code, maximum=2048)
    return {
        "reader_id": reader_id,
        "reader_version": reader_version,
        "schema_version": consumes,
        "wire_name": wire_name,
        "json_type": json_type,
        "required": required,
        "default_behavior": "NO_DEFAULT",
        "legal_domain": domain,
    }


def _anchor(value: object, pointer: str) -> tuple[str, str, str]:
    node = _object(value, pointer, "ER_A3_PACKAGE_INVALID")
    _exact_fields(
        node,
        (
            "alias",
            "canonical_field_id",
            "semantic_class",
            "meaning",
            "fact_preference_boundary",
            "accountable_source",
            "field_schema",
            "reader_contract",
        ),
        pointer,
        "ER_A3_PACKAGE_INVALID",
    )
    alias = node["alias"]
    if alias not in ANCHOR_ALIASES:
        _fail("ER_A3_ANCHOR_SET_INVALID", pointer + "/alias", "expected A1 or H1")
    field_id = _identifier(
        node["canonical_field_id"], pointer + "/canonical_field_id", "ER_A3_PACKAGE_INVALID"
    )
    if field_id in ANCHOR_ALIASES or field_id == CANONICAL_PROFILE_ALIAS:
        _fail("ER_A3_ANCHOR_SET_INVALID", pointer + "/canonical_field_id", "alias is not a canonical field id")
    if node["semantic_class"] not in {"VERIFIED_FACT", "PRESCRIPTIVE_PREFERENCE", "MIXED"}:
        _fail("ER_A3_PACKAGE_INVALID", pointer + "/semantic_class", "unsupported semantic class")
    _string(node["meaning"], pointer + "/meaning", "ER_A3_PACKAGE_INVALID", maximum=2048)
    _string(
        node["fact_preference_boundary"],
        pointer + "/fact_preference_boundary",
        "ER_A3_PACKAGE_INVALID",
        maximum=2048,
    )
    _accountable_source(node["accountable_source"], pointer + "/accountable_source")
    field_schema = _field_schema(node["field_schema"], pointer + "/field_schema")
    reader = _reader_contract(node["reader_contract"], pointer + "/reader_contract")
    parity_fields = (
        "schema_version",
        "wire_name",
        "json_type",
        "required",
        "default_behavior",
        "legal_domain",
    )
    for name in parity_fields:
        if field_schema[name] != reader[name]:
            _fail(
                "ER_A3_SCHEMA_READER_MISMATCH",
                pointer + "/reader_contract/" + ("consumes_schema_version" if name == "schema_version" else name),
                f"reader {name} does not match field schema",
            )
    return alias, field_id, field_schema["wire_name"]


def _source_spec(value: object, pointer: str) -> None:
    node = _object(value, pointer, "ER_A3_SOURCE_INVALID")
    _exact_fields(
        node,
        ("path", "sha256", "declared_version", "status", "authority_effect"),
        pointer,
        "ER_A3_SOURCE_INVALID",
    )
    _relative_path(node["path"], pointer + "/path", "ER_A3_SOURCE_INVALID")
    _sha256(node["sha256"], pointer + "/sha256", "ER_A3_SOURCE_INVALID")
    _version(node["declared_version"], pointer + "/declared_version", "ER_A3_SOURCE_INVALID")
    if node["status"] != "SPECIFICATION_ONLY":
        _fail("ER_A3_SOURCE_INVALID", pointer + "/status", "source specification must remain specification-only")
    if node["authority_effect"] != "NONE":
        _fail("ER_A3_SOURCE_INVALID", pointer + "/authority_effect", "source specification grants no authority")


def _canonical_profile(value: object, pointer: str) -> None:
    node = _object(value, pointer, "ER_A3_PACKAGE_INVALID")
    _exact_fields(node, ("alias", "profile_id", "scope", "source_spans"), pointer, "ER_A3_PACKAGE_INVALID")
    if node["alias"] != CANONICAL_PROFILE_ALIAS:
        _fail("ER_A3_PACKAGE_INVALID", pointer + "/alias", "canonical profile alias must be J1")
    if node["profile_id"] != CANONICAL_PROFILE_ID:
        _fail("ER_A3_PACKAGE_INVALID", pointer + "/profile_id", "unsupported canonical profile")
    if node["scope"] != "SERIALIZATION_ONLY":
        _fail("ER_A3_PACKAGE_INVALID", pointer + "/scope", "J1 scope must remain serialization-only")
    _spans(node["source_spans"], pointer + "/source_spans", maximum_items=8)


def _freeze(value: Any) -> Any:
    if type(value) is dict:
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if type(value) is list:
        return tuple(_freeze(item) for item in value)
    return value


def _parse(raw: bytes) -> dict[str, Any]:
    if type(raw) is not bytes:
        raise TypeError("raw package must be bytes")
    if len(raw) > MAX_RAW_BYTES:
        _fail("ER_A3_RAW_TOO_LARGE", "/", f"maximum is {MAX_RAW_BYTES} bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        _fail("ER_A3_JSON_BOM", "/", "UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        _fail("ER_A3_JSON_INVALID_UTF8", "/", f"invalid byte at offset {exc.start}")

    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                _fail("ER_A3_JSON_DUPLICATE_KEY", "/", f"duplicate key {key!r}")
            result[key] = value
        return result

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=no_duplicates,
            parse_constant=lambda token: (_fail("ER_A3_JSON_INVALID", "/", f"forbidden number {token}")),
        )
    except ERA3MinError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        _fail("ER_A3_JSON_INVALID", "/", str(exc))
    return _object(parsed, "/", "ER_A3_JSON_INVALID")


def verify_package(raw: bytes) -> VerifiedERA3MinPackageV1:
    """Validate package shape and declared schema/reader parity without resolving sources."""

    package = _parse(raw)
    _exact_fields(
        package,
        (
            "schema",
            "profile",
            "candidate",
            "source_spec",
            "anchors",
            "canonical_profile",
            "compatibility",
            "authority_effect",
            "next_stage_authorized",
            "limitations",
        ),
        "/",
        "ER_A3_PACKAGE_FIELD_SET",
    )
    if package["schema"] != SCHEMA:
        _fail("ER_A3_SCHEMA_UNSUPPORTED", "/schema", "unsupported schema")
    if package["profile"] != PROFILE:
        _fail("ER_A3_PROFILE_UNSUPPORTED", "/profile", "unsupported profile")
    if package["candidate"] != CANDIDATE:
        _fail("ER_A3_CANDIDATE_UNSUPPORTED", "/candidate", "only Candidate A is in scope")
    _source_spec(package["source_spec"], "/source_spec")

    anchors = package["anchors"]
    if type(anchors) is not list or len(anchors) != 2:
        _fail("ER_A3_ANCHOR_SET_INVALID", "/anchors", "expected exactly A1 and H1")
    identities = tuple(_anchor(anchor, f"/anchors/{index}") for index, anchor in enumerate(anchors))
    aliases = {item[0] for item in identities}
    canonical_ids = {item[1] for item in identities}
    wire_names = {item[2] for item in identities}
    if aliases != ANCHOR_ALIASES or len(canonical_ids) != 2 or len(wire_names) != 2:
        _fail(
            "ER_A3_ANCHOR_SET_INVALID",
            "/anchors",
            "aliases, canonical field IDs, and wire names must each be distinct",
        )

    _canonical_profile(package["canonical_profile"], "/canonical_profile")
    if package["compatibility"] != "UNASSESSED":
        _fail("ER_A3_PACKAGE_INVALID", "/compatibility", "compatibility must remain unassessed")
    if package["authority_effect"] != "NONE":
        _fail("ER_A3_PACKAGE_INVALID", "/authority_effect", "package grants no authority")
    if _boolean(
        package["next_stage_authorized"],
        "/next_stage_authorized",
        "ER_A3_PACKAGE_INVALID",
    ):
        _fail("ER_A3_PACKAGE_INVALID", "/next_stage_authorized", "next stage is not authorized")
    _string_list(
        package["limitations"],
        "/limitations",
        "ER_A3_PACKAGE_INVALID",
        maximum_items=32,
        maximum_length=1024,
    )

    return VerifiedERA3MinPackageV1(
        _freeze(package), hashlib.sha256(raw).hexdigest().upper(), _token=_TOKEN
    )
