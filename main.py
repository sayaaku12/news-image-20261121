#!/usr/bin/env python3
"""news-image-20261121 entrypoint.

Copies the bundled front page (entry.png, rendered with PIL for
Saturday 21 November 2026) to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output). Standard library only, no network, fully
deterministic: the same input bytes always produce the same output
bytes, so the grader's two runs write identical files.
"""
import hashlib
import os
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
MAX_BYTES = 1_048_576  # competition gate: image at most 1 MiB

# PNG signature: the first 8 bytes of any valid PNG file.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

# Pinned digest of the bundled image, measured from the first
# render and verified on every run below.
EXPECTED_SHA256 = (
    "4dba1d2b679151360f9e6792701bd61e1bcb121e1d8ebf7b9912359137cb1963"
)


def source_path():
    """Absolute path of the bundled image next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def output_dir():
    """Output directory from the environment, defaulting to /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR


def read_source(path):
    """Read the bundled image bytes, failing loudly if absent."""
    if not os.path.isfile(path):
        raise SystemExit(f"bundled image missing: {path}")
    with open(path, "rb") as handle:
        return handle.read()


def write_output(data, directory):
    """Write the image bytes to <directory>/entry.png atomically.

    The bytes go to a temp file in the same directory first and are
    then moved into place, so a reader never sees a half-written
    entry.png, and a failed run leaves no corrupt output behind.
    """
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"bundled image too large: {len(data)} bytes > {MAX_BYTES}")
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, OUTPUT_NAME)
    tmp = target + ".tmp"
    with open(tmp, "wb") as handle:
        handle.write(data)
    os.replace(tmp, target)
    return target


def check_digest(data):
    """Fail loudly unless the bundled bytes match the pinned hash."""
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(
            f"bundled image hash mismatch: got {digest}, "
            f"expected {EXPECTED_SHA256}")
    return digest


def validated_source():
    """Read the bundled image and check it end to end: it must be a
    PNG, under the 1 MiB cap, and match the pinned digest. Returns
    the bytes; any failure exits loudly before anything is written.
    """
    data = read_source(source_path())
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("bundled image is not a PNG")
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"bundled image too large: {len(data)} bytes > {MAX_BYTES}")
    return data, check_digest(data)


def self_test():
    """Run the entry twice into fresh temp dirs; both outputs must
    be byte-identical and match the pinned hash. Returns 0 on pass.
    """
    import shutil
    import tempfile

    digests = []
    for _ in range(2):
        tmp = tempfile.mkdtemp(prefix="news-image-selftest-")
        try:
            data, digest = validated_source()
            digests.append(digest)
            target = write_output(data, tmp)
            with open(target, "rb") as handle:
                written = handle.read()
            if hashlib.sha256(written).hexdigest() != digests[-1]:
                raise SystemExit("written output differs from source")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    if digests[0] != digests[1]:
        raise SystemExit("self-test FAILED: two runs differ")
    print(f"self-test PASSED (two runs byte-identical, "
          f"sha256 {digests[0]})")
    return 0


def main(argv=None):
    if argv and "--self-test" in argv:
        return self_test()
    data, digest = validated_source()
    target = write_output(data, output_dir())
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
