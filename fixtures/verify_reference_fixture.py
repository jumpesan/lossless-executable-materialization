from __future__ import annotations

import base64
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def require_equal(label: str, observed: object, expected: object) -> None:
    if observed != expected:
        raise RuntimeError(f"{label}: observed={observed!r} expected={expected!r}")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    descriptor_path = root / "fixtures/representation/reference_fixture.descriptor.json"
    descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))

    encoded_parts: list[str] = []
    for operand in sorted(descriptor["representation"]["operands"], key=lambda item: item["order"]):
        path = root / operand["path"]
        raw = path.read_bytes()
        require_equal(f"{path.name}.characters", len(raw), operand["characters"])
        require_equal(
            f"{path.name}.sha256",
            hashlib.sha256(raw).hexdigest(),
            operand["sha256"],
        )
        text = raw.decode("ascii")
        if any(ch.isspace() for ch in text):
            raise RuntimeError(f"{path.name}: unexpected ASCII whitespace")
        encoded_parts.append(text)

    joined = "".join(encoded_parts)
    require_equal(
        "assembled_characters",
        len(joined),
        descriptor["representation"]["assembled_characters"],
    )

    compressed = base64.b64decode(joined, validate=True)
    compressed_identity = descriptor["representation"]["compressed_identity"]
    require_equal("compressed.size_bytes", len(compressed), compressed_identity["size_bytes"])
    require_equal(
        "compressed.sha256",
        hashlib.sha256(compressed).hexdigest(),
        compressed_identity["sha256"],
    )

    source = gzip.decompress(compressed)
    canonical_identity = descriptor["canonical_identity"]
    require_equal("canonical.size_bytes", len(source), canonical_identity["size_bytes"])
    require_equal(
        "canonical.sha256",
        hashlib.sha256(source).hexdigest(),
        canonical_identity["sha256"],
    )
    require_equal(
        "canonical.git_blob_sha1",
        git_blob_sha1(source),
        canonical_identity["git_blob_sha1"],
    )

    compile(source.decode("utf-8"), "reference_fixture.py", "exec")

    with tempfile.TemporaryDirectory(prefix="lem-reference-") as tmp:
        script_path = Path(tmp) / "reference_fixture.py"
        script_path.write_bytes(source)
        execution = descriptor["execution"]
        completed = subprocess.run(
            [sys.executable, "-S", str(script_path)],
            input=json.dumps(execution["sample_input"]),
            text=True,
            capture_output=True,
            check=False,
        )
        require_equal("execution.exit_code", completed.returncode, execution["expected_exit_code"])
        if completed.stderr:
            raise RuntimeError(f"execution.stderr was not empty: {completed.stderr!r}")
        result = json.loads(completed.stdout)
        require_equal("execution.status", result.get("status"), execution["expected_status"])

    print(
        json.dumps(
            {
                "status": "verified",
                "fixture_id": descriptor["fixture_id"],
                "operand_count": len(encoded_parts),
                "assembled_characters": len(joined),
                "compressed_size": len(compressed),
                "canonical_identity": {
                    "size_bytes": len(source),
                    "sha256": hashlib.sha256(source).hexdigest(),
                    "git_blob_sha1": git_blob_sha1(source),
                },
                "execution_status": result["status"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
