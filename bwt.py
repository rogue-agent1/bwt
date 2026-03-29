#!/usr/bin/env python3
"""Burrows-Wheeler Transform. Zero dependencies."""
import sys

def transform(data):
    if not data: return b"", 0
    n = len(data)
    doubled = data + data
    indices = sorted(range(n), key=lambda i: doubled[i:i+n])
    last_col = bytes(doubled[i+n-1] for i in indices)
    orig_idx = indices.index(0)
    return last_col, orig_idx

def inverse(bwt, idx):
    if not bwt: return b""
    n = len(bwt)
    table = sorted(range(n), key=lambda i: bwt[i])
    result = bytearray()
    j = idx
    for _ in range(n):
        result.append(bwt[j])
        j = table[j]
    return bytes(result)

def transform_text(text):
    if not text: return "", 0
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    sorted_rot = sorted(rotations)
    last = "".join(r[-1] for r in sorted_rot)
    idx = sorted_rot.index(text)
    return last, idx

def inverse_text(bwt, idx):
    if not bwt: return ""
    n = len(bwt)
    table = sorted(range(n), key=lambda i: bwt[i])
    result = []
    j = idx
    for _ in range(n):
        result.append(bwt[j])
        j = table[j]
    return "".join(result)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Burrows-Wheeler Transform")
    p.add_argument("action", choices=["transform","inverse"])
    p.add_argument("text", nargs="?")
    args = p.parse_args()
    if args.action == "transform":
        t = args.text or sys.stdin.read().rstrip(chr(10))
        bwt, idx = transform_text(t)
        print(f"{bwt} (index: {idx})")
    else:
        parts = args.text.rsplit(" ", 2)
        print(inverse_text(parts[0], int(parts[-1].rstrip(")"))))
