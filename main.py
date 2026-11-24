#!/usr/bin/env python3
"""news-23 b83 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.
Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

EXPECTED_W, EXPECTED_H = 1024, 1024
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error:", msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if not os.path.isfile(src):
        return fail("entry.png missing next to main.py")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        return fail("entry.png over 1 MiB")
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("not a PNG")
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("first PNG chunk is not IHDR")
    if len(data) < 1000:
        return fail("entry.png implausibly small")
    # Parse IHDR manually: width/height are big-endian uint32 at bytes 16..24.
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (EXPECTED_W, EXPECTED_H):
        return fail("entry.png is not 1024x1024")
    bit_depth, colour_type = data[24], data[25]
    if bit_depth != 8 or colour_type not in (2, 6):
        return fail("unexpected PNG bit depth / colour type")
    # Walk chunks: verify CRC of every chunk, require a non-empty IDAT and a
    # well-formed 12-byte IEND trailer at the end of the file.
    pos = 8
    seen_idat = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            return fail("truncated PNG chunk")
        chunk = data[pos + 4:end - 4]
        crc_stored = struct.unpack(">I", data[end - 4:end])[0]
        crc_calc = binascii.crc32(chunk) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            return fail("PNG chunk CRC mismatch: " + ctype.decode("latin-1"))
        if ctype == b"IDAT" and length > 0:
            seen_idat = True
        if ctype == b"IEND":
            if length != 0 or end != len(data):
                return fail("IEND is not the 12-byte trailer at end of file")
            break
        pos = end
    else:
        return fail("no IEND chunk found")
    if not seen_idat:
        return fail("PNG has no IDAT data")
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        out = f.read()
    if out != data:
        return fail("output does not match source byte-for-byte")
    print("sha256", hashlib.sha256(data).hexdigest())
    print("wrote", dst, len(data), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
