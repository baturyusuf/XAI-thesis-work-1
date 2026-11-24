"""Remove directory entries from .docx ZIP archives (Word can refuse them via cloud co-editing)."""
import io
import sys
import zipfile
from pathlib import Path

for f in sys.argv[1:]:
    p = Path(f)
    with zipfile.ZipFile(p) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist() if not i.filename.endswith('/')]
        dirs = len(z.infolist()) - len(items)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as out:
        for info, data in items:
            out.writestr(info, data)
    p.write_bytes(buf.getvalue())
    print(p.name, 'removed dir entries:', dirs, 'files:', len(items))
