from bwt import transform, inverse, transform_text, inverse_text
text = "banana"
bwt, idx = transform_text(text)
assert inverse_text(bwt, idx) == text
data = b"abracadabra"
bwt2, idx2 = transform(data)
assert inverse(bwt2, idx2) == data
print("BWT tests passed")