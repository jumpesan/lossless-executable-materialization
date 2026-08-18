from __future__ import annotations

import base64
import gzip
import hashlib
import json
from pathlib import Path

FIXTURE_ID = "lem-reference-fixture-v0.1"
CHUNK_SIZE = 4096

EXPECTED_SOURCE_SIZE = 12123
EXPECTED_SOURCE_SHA256 = "31594021147f13e6d824cc61c083d3fdd674bf79ee5eda590d5a4b7fe6b1123d"
EXPECTED_SOURCE_GIT_BLOB = "8fcd8da1dbbb09e1cea2c565a7abc27d7363ff7a"
EXPECTED_GZIP_SIZE = 6321
EXPECTED_GZIP_SHA256 = "ec5839b3636ef7d5d03b362f781c676c0812f96e80d138b4e358dba32376da08"
EXPECTED_BASE64_CHARS = 8428


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def build_source() -> bytes:
    vectors = [
        hashlib.sha256(f"lem-reference-fixture-{i:03d}".encode("utf-8")).hexdigest()
        for i in range(128)
    ]

    lines = [
        '"""Reference executable fixture for Lossless Executable Materialization research.',
        "",
        "This fixture is intentionally deterministic and includes opaque test vectors",
        "so the compressed representation spans multiple transport chunks.",
        "It is not a production validator.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "import hashlib",
        "import json",
        "import sys",
        "",
        "",
        'FIXTURE_VERSION = "lem-reference-fixture-v0.1"',
        "",
        "PADDING_VECTORS = [",
    ]
    lines.extend(f'    "{value}",' for value in vectors)
    lines.extend(
        [
            "]",
            "",
            "",
            "def _canonical_json(value: object) -> bytes:",
            '    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
            "",
            "",
            "def validate(payload: object) -> dict[str, object]:",
            "    reasons: list[str] = []",
            "",
            "    if not isinstance(payload, dict):",
            "        return {",
            '            "status": "invalid",',
            '            "fixture_version": FIXTURE_VERSION,',
            '            "reasons": ["payload_must_be_object"],',
            "        }",
            "",
            '    mode = payload.get("mode")',
            '    if mode not in {"alpha", "beta"}:',
            '        reasons.append("mode_must_be_alpha_or_beta")',
            "",
            '    values = payload.get("values")',
            "    if not isinstance(values, list):",
            '        reasons.append("values_must_be_list")',
            "        values = []",
            "",
            "    if any(isinstance(v, bool) or not isinstance(v, int) for v in values):",
            '        reasons.append("values_must_contain_only_integers")',
            "",
            "    integer_values = [v for v in values if isinstance(v, int) and not isinstance(v, bool)]",
            "    total = sum(integer_values)",
            "    count = len(integer_values)",
            "",
            '    expected_total = payload.get("expected_total")',
            "    if expected_total is not None and expected_total != total:",
            '        reasons.append("expected_total_mismatch")',
            "",
            '    vector_index = payload.get("vector_index", 0)',
            "    if isinstance(vector_index, bool) or not isinstance(vector_index, int):",
            '        reasons.append("vector_index_must_be_integer")',
            "        vector_index = 0",
            "    if not 0 <= vector_index < len(PADDING_VECTORS):",
            '        reasons.append("vector_index_out_of_range")',
            "        vector_index = 0",
            "",
            "    payload_digest = hashlib.sha256(_canonical_json(payload)).hexdigest()",
            "",
            "    return {",
            '        "status": "valid" if not reasons else "invalid",',
            '        "fixture_version": FIXTURE_VERSION,',
            '        "mode": mode,',
            '        "count": count,',
            '        "total": total,',
            '        "selected_vector": PADDING_VECTORS[vector_index],',
            '        "payload_sha256": payload_digest,',
            '        "reasons": reasons,',
            "    }",
            "",
            "",
            "def main() -> int:",
            "    try:",
            "        payload = json.load(sys.stdin)",
            "    except Exception as exc:",
            "        result = {",
            '            "status": "invalid",',
            '            "fixture_version": FIXTURE_VERSION,',
            '            "reasons": [f"input_json_error:{type(exc).__name__}"],',
            "        }",
            '        print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False))',
            "        return 2",
            "",
            "    result = validate(payload)",
            '    print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False))',
            '    return 0 if result["status"] == "valid" else 1',
            "",
            "",
            'if __name__ == "__main__":',
            "    raise SystemExit(main())",
            "",
        ]
    )

    return "\n".join(lines).encode("utf-8")


def build_representation(source: bytes) -> tuple[bytes, str, list[str]]:
    compressed = gzip.compress(source, compresslevel=9, mtime=0)
    encoded = base64.b64encode(compressed).decode("ascii")
    parts = [encoded[i : i + CHUNK_SIZE] for i in range(0, len(encoded), CHUNK_SIZE)]
    return compressed, encoded, parts


def verify(source: bytes, compressed: bytes, encoded: str) -> None:
    observed = {
        "source_size": len(source),
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "source_git_blob": git_blob_sha1(source),
        "gzip_size": len(compressed),
        "gzip_sha256": hashlib.sha256(compressed).hexdigest(),
        "base64_chars": len(encoded),
    }
    expected = {
        "source_size": EXPECTED_SOURCE_SIZE,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "source_git_blob": EXPECTED_SOURCE_GIT_BLOB,
        "gzip_size": EXPECTED_GZIP_SIZE,
        "gzip_sha256": EXPECTED_GZIP_SHA256,
        "base64_chars": EXPECTED_BASE64_CHARS,
    }
    if observed != expected:
        raise SystemExit(json.dumps({"status": "identity_mismatch", "observed": observed, "expected": expected}, indent=2))


def main() -> int:
    root = Path(__file__).resolve().parent
    canonical_dir = root / "canonical"
    representation_dir = root / "representation"
    canonical_dir.mkdir(parents=True, exist_ok=True)
    representation_dir.mkdir(parents=True, exist_ok=True)

    source = build_source()
    compressed, encoded, parts = build_representation(source)
    verify(source, compressed, encoded)

    canonical_path = canonical_dir / "reference_fixture.py"
    canonical_path.write_bytes(source)

    operands = []
    for index, part in enumerate(parts, start=1):
        filename = f"reference_fixture.gzip-base64.part-{index:03d}.b64"
        path = representation_dir / filename
        path.write_text(part, encoding="ascii", newline="")
        operands.append(
            {
                "order": index,
                "path": f"fixtures/representation/{filename}",
                "characters": len(part),
                "sha256": hashlib.sha256(part.encode("ascii")).hexdigest(),
            }
        )

    descriptor = {
        "schema": "lem-materialization-descriptor",
        "schema_version": "0.1-draft",
        "fixture_id": FIXTURE_ID,
        "authority": {
            "role": "PUBLIC_REFERENCE_FIXTURE",
            "canonical_path": "fixtures/canonical/reference_fixture.py",
        },
        "representation": {
            "profile": "deterministic-gzip-v1+base64",
            "assembly": "ordered_ascii_concatenation",
            "compression": {"algorithm": "gzip", "level": 9, "mtime": 0},
            "transport_encoding": "base64",
            "operands": operands,
            "compressed_identity": {
                "size_bytes": len(compressed),
                "sha256": hashlib.sha256(compressed).hexdigest(),
            },
        },
        "canonical_identity": {
            "size_bytes": len(source),
            "sha256": hashlib.sha256(source).hexdigest(),
            "git_blob_sha1": git_blob_sha1(source),
        },
        "execution": {
            "interface": "python-script-stdin-json",
            "sample_input": {"mode": "alpha", "values": [1, 2, 3], "expected_total": 6, "vector_index": 7},
        },
        "failure": {
            "semantic_repair_allowed": False,
            "alternate_representation_after_terminal_failure_allowed": False,
        },
    }

    (representation_dir / "reference_fixture.descriptor.json").write_text(
        json.dumps(descriptor, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )

    print(json.dumps({"status": "generated", "parts": len(parts), "canonical_identity": descriptor["canonical_identity"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())