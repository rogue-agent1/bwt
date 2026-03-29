#!/usr/bin/env python3
"""bwt: Burrows-Wheeler Transform."""
import sys

def transform(text):
    if not text: return "", 0
    sentinel = "\x00"
    s = text + sentinel
    n = len(s)
    rotations = sorted(range(n), key=lambda i: s[i:] + s[:i])
    bwt = "".join(s[(r + n - 1) % n] for r in rotations)
    idx = rotations.index(0)
    return bwt, idx

def inverse(bwt, idx):
    if not bwt: return ""
    n = len(bwt)
    # Build first column (sorted)
    order = sorted(range(n), key=lambda i: bwt[i])
    # Follow the chain
    result = []
    j = idx
    for _ in range(n):
        j = order[j]
        result.append(bwt[j])
    # Remove sentinel
    text = "".join(result)
    if text.endswith("\x00"):
        text = text[:-1]
    return text

def test():
    text = "banana"
    bwt, idx = transform(text)
    assert inverse(bwt, idx) == text
    # Round-trip various
    for t in ["abracadabra", "mississippi", "hello world", "aaaa", "a"]:
        b, i = transform(t)
        assert inverse(b, i) == t, f"Failed for {t}"
    # Empty
    b, i = transform("")
    assert inverse(b, i) == ""
    # BWT should group similar chars
    bwt_banana, _ = transform("banana")
    assert bwt_banana.count("a") == "banana\x00".count("a")
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: bwt.py test")
