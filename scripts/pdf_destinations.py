#!/usr/bin/env python3
"""Read actual PDF page destinations; shared by numbered contents and library."""
import json
import sys
from urllib.parse import unquote
from pypdf import PdfReader

reader = PdfReader(sys.argv[1])
result = {}
for name, destination in reader.named_destinations.items():
    number = reader.get_destination_page_number(destination) + 1
    if not 1 <= number <= len(reader.pages):
        raise ValueError(f"Invalid destination: {name}")
    # Chromium can encode a destination as a PDF Name (/id) or a string.
    result[unquote(str(name).lstrip("/"))] = number
print(json.dumps({"pages": len(reader.pages), "destinations": result}, sort_keys=True))
