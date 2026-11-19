import io
import struct
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def repaired_icon(content):
    corrected = bytearray(content)
    count = struct.unpack_from("<H", corrected, 4)[0]
    for index in range(count):
        entry = 6 + 16 * index
        offset = struct.unpack_from("<I", corrected, entry + 12)[0]
        if corrected[offset:offset + 8] != b"\x89PNG\r\n\x1a\n":
            bit_depth = struct.unpack_from("<H", corrected, offset + 14)[0]
            struct.pack_into("<H", corrected, entry + 6, bit_depth)
    with Image.open(io.BytesIO(corrected)) as original:
        original.load()
        pixels = original.convert("RGBA")
        output = io.BytesIO()
        pixels.save(output, format="ICO", sizes=[original.size])
    with Image.open(io.BytesIO(output.getvalue())) as result:
        result.load()
        if result.convert("RGBA").tobytes() != pixels.tobytes():
            raise ValueError("ICO repair changed the original pixels")
    return output.getvalue()


def main():
    for filename in ("favicon.ico", "images/favicon.ico"):
        target = ROOT / filename
        target.write_bytes(repaired_icon(target.read_bytes()))
        print(f"Repaired {filename} without changing pixels")


if __name__ == "__main__":
    main()
