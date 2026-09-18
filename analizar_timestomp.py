import os
import zlib
import struct
import datetime

# Archivo de entrada
e01_path = os.path.join(os.path.dirname(__file__), 'retos_archivos', '06 _ Alguien tocó el reloj_file6.E01')

print("==================================================================")
print("     ANÁLISIS FORENSE DE TIMESTOMPING EN NTFS (MFT INSPECTOR)     ")
print("==================================================================")
print(f"Cargando imagen: {e01_path} ...\n")

# 1. Descompresión de la imagen E01 (Expert Witness Format)
with open(e01_path, 'rb') as f:
    e01_data = f.read()

disk = bytearray()
remaining = e01_data[1551:152544]

while remaining:
    d = zlib.decompressobj()
    disk.extend(d.decompress(remaining))
    unused = d.unused_data
    if not unused.startswith(b'\x78') and len(unused) > 0:
        idx = unused.find(b'\x78')
        if idx != -1:
            unused = unused[idx:]
    remaining = unused

print(f"[+] Imagen NTFS descomprimida en memoria: {len(disk) / (1024*1024):.2f} MB")

# 2. Localizar entrada MFT de 'New Text Document.txt'
target_name = "New Text Document.txt"
mft_offset = 203776
mft_record = disk[mft_offset : mft_offset + 1024]

def filetime_to_dt(ft):
    epoch = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)
    return epoch + datetime.timedelta(microseconds=ft // 10)

# Parsing de atributos
first_attr = int.from_bytes(mft_record[0x14:0x16], 'little')
pos = first_attr

si_times = None
fn_times = None

while pos < len(mft_record):
    attr_type = int.from_bytes(mft_record[pos:pos+4], 'little')
    if attr_type in (0, 0xffffffff): break
    attr_len = int.from_bytes(mft_record[pos+4:pos+8], 'little')
    if attr_len == 0: break
    
    non_resident = mft_record[pos+8]
    if non_resident == 0:
        content_offset = int.from_bytes(mft_record[pos+20:pos+22], 'little')
        content = mft_record[pos+content_offset:]
        if attr_type == 0x10: # $STANDARD_INFORMATION
            c, m, mft, a = struct.unpack('<QQQQ', content[:32])
            si_times = (filetime_to_dt(c), filetime_to_dt(m), filetime_to_dt(mft), filetime_to_dt(a))
        elif attr_type == 0x30: # $FILE_NAME
            c, m, mft, a = struct.unpack('<QQQQ', content[8:40])
            fn_times = (filetime_to_dt(c), filetime_to_dt(m), filetime_to_dt(mft), filetime_to_dt(a))
            
    pos += attr_len

print(f"\n[+] Archivo analizado: '{target_name}'")
print("-" * 66)
print(f"{'Campo':<20} | {'$STANDARD_INFORMATION (Alterado)':<30} | {'$FILE_NAME (Original / Kernel)':<30}")
print("-" * 66)
labels = ["Creación (C)", "Modificación (M)", "MFT Altered (B)", "Último Acceso (A)"]
for i in range(4):
    si_str = si_times[i].strftime('%Y-%m-%d %H:%M:%S.%f') if si_times else 'N/A'
    fn_str = fn_times[i].strftime('%Y-%m-%d %H:%M:%S.%f') if fn_times else 'N/A'
    marca = "  <-- FLAG ORIGINAL" if i == 1 else ""
    print(f"{labels[i]:<20} | {si_str:<30} | {fn_str:<30}{marca}")
print("-" * 66)

print(f"\n>> FLAG / RESPUESTA FINAL: {fn_times[1].strftime('%Y-%m-%d %H:%M:%S.%f')}\n")
