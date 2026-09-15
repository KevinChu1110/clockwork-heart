import struct
import sys
from pathlib import Path

def list_pck(pck_path: Path):
    with open(pck_path, 'rb') as f:
        magic = f.read(4)
        if magic != b'GDPC':
            print("Invalid magic:", magic)
            return []
        fmt = struct.unpack('<I', f.read(4))[0]
        major, minor, patch = struct.unpack('<III', f.read(12))
        flags = struct.unpack('<I', f.read(4))[0]
        file_base = struct.unpack('<Q', f.read(8))[0]
        
        # In Godot 4 (fmt >= 2), directory offset is at offset 32
        f.seek(32)
        dir_offset = struct.unpack('<Q', f.read(8))[0]
        f.seek(dir_offset)
        file_count = struct.unpack('<I', f.read(4))[0]
        
        files = []
        for _ in range(file_count):
            path_len = struct.unpack('<I', f.read(4))[0]
            path_bytes = f.read(path_len)
            path = path_bytes.decode('utf-8', errors='replace').rstrip('\x00')
            pad = (4 - (path_len % 4)) % 4
            f.read(pad)
            offset, size = struct.unpack('<QQ', f.read(16))
            md5 = f.read(16)
            file_flags = struct.unpack('<I', f.read(4))[0] if fmt >= 2 else 0
            files.append((size, path, offset))
    return files

if __name__ == '__main__':
    pck = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/opt/side/bravesoul-game/dist/android/core.pck')
    files = list_pck(pck)
    files.sort(key=lambda x: x[0], reverse=True)
    print(f"PCK File: {pck}")
    print(f"Total files: {len(files)}")
    total_size = sum(x[0] for x in files)
    print(f"Total file size sum: {total_size} bytes ({total_size / (1024*1024):.2f} MB)")
    print("-" * 75)
    for i, (size, path, offset) in enumerate(files[:35], 1):
        print(f"{i:2d}. {size:10d} bytes ({size / (1024*1024):.2f} MB)  {path}")
