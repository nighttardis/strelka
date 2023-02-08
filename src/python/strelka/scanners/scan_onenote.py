# Authors: Ryan Borre

import binascii
import hashlib
import re

from strelka.cstructs.onenote import FileDataStoreObject

from strelka import strelka


class ScanOnenote(strelka.Scanner):
    """Extracts embedded files in OneNote files."""

    def scan(self, data, file, options, expire_at):
        # For every embedded file, extract payload and submit back into Strelka pipeline
        for match in re.finditer(
            binascii.unhexlify(b"e716e3bd65261145a4c48d4d0b7a9eac"), data
        ):
            obj = FileDataStoreObject.parse(data[match.span(0)[0] :])
            payload = obj.FileData

            # Send extracted file back to Strelka
            self.emit_file(self.name, name=hashlib.sha256(payload).hexdigest())