"""Exclusive durable guard records; no scientific operations."""
import json,os,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]

def write(out,name,value):
    path=out/name; temporary=out/(name+'.tmp')
    if path.exists() or temporary.exists(): raise RuntimeError('No record overwrite: '+name)
    with temporary.open('x',encoding='utf-8',newline=chr(10)) as f:
        json.dump(value,f,indent=2,allow_nan=False); f.write(chr(10)); f.flush(); os.fsync(f.fileno())
    temporary.rename(path)

def read(path): return json.loads(path.read_text(encoding='utf-8'))

def wait_record(out,name,seconds=5):
    deadline=time.perf_counter()+seconds
    while time.perf_counter()<deadline:
        if (out/name).exists(): return read(out/name)
        time.sleep(.002)
    raise RuntimeError('Guard IPC timeout: '+name)
