#!/usr/bin/env python3
"""bwt - Burrows-Wheeler Transform for compression preprocessing."""
import sys

def bwt_encode(text, sentinel="$"):
    s = text + sentinel
    n = len(s)
    rotations = sorted(range(n), key=lambda i: s[i:] + s[:i])
    encoded = "".join(s[(i + n - 1) % n] for i in rotations)
    idx = rotations.index(0)
    return encoded, idx

def bwt_decode(encoded, idx):
    n = len(encoded)
    table = [""] * n
    for _ in range(n):
        table = sorted(encoded[i] + table[i] for i in range(n))
    for row in table:
        if row.endswith("$"):
            return row[:-1]
    return table[idx][:-1]

def move_to_front_encode(text):
    alphabet = list(sorted(set(text)))
    result = []
    for ch in text:
        idx = alphabet.index(ch)
        result.append(idx)
        alphabet.pop(idx)
        alphabet.insert(0, ch)
    return result

def move_to_front_decode(codes, alphabet):
    alphabet = list(alphabet)
    result = []
    for idx in codes:
        ch = alphabet[idx]
        result.append(ch)
        alphabet.pop(idx)
        alphabet.insert(0, ch)
    return "".join(result)

def test():
    text = "banana"
    encoded, idx = bwt_encode(text)
    assert len(encoded) == len(text) + 1
    decoded = bwt_decode(encoded, idx)
    assert decoded == text
    for s in ["abracadabra", "mississippi", "hello", "a", "aaa"]:
        e, i = bwt_encode(s)
        assert bwt_decode(e, i) == s
    mtf = move_to_front_encode("banana")
    assert len(mtf) == 6
    orig_alpha = sorted(set("banana"))
    assert move_to_front_decode(mtf, orig_alpha) == "banana"
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("bwt: Burrows-Wheeler Transform. Use --test")
