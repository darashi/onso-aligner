# onso-aligner

Get the forced alignment of phonemes. It does almost the same thing as [segment-kit](https://github.com/julius-speech/segmentation-kit), but is written in Python, wrapping Julius.

```python
>>> import onso_aligner

>>> onso_aligner.align('tests/fixtures/meian_1413.wav', 'あねむすめのつぎこわ')
[(0, 1525000, 'silB'), (1525000, 3025000, 'a'), (3025000, 3325000, 'n'), (3325000, 3725000, 'e'), (3725000, 4325000, 'm'), (4325000, 4625000, 'u'), (4625000, 5625000, 's'), (5625000, 5925000, 'u'), (5925000, 6225000, 'm'), (6225000, 6625000, 'e'), (6625000, 7225000, 'n'), (7225000, 8225000, 'o'), (8225000, 9325000, 'ts'), (9325000, 9625000, 'u'), (9625000, 9925000, 'g'), (9925000, 10325000, 'i'), (10325000, 11225000, 'k'), (11225000, 11725000, 'o'), (11725000, 12725000, 'w'), (12725000, 14125000, 'a'), (14125000, 16425000, 'silE')]

>>> print("\n".join([f"{r[0]} {r[1]} {r[2]}" for r in onso_aligner.align('tests/fixtures/meian_1413.wav', 'あねむすめのつぎこわ')]))
0 1525000 silB
1525000 3025000 a
3025000 3325000 n
3325000 3725000 e
3725000 4325000 m
4325000 4625000 u
4625000 5625000 s
5625000 5925000 u
5925000 6225000 m
6225000 6625000 e
6625000 7225000 n
7225000 8225000 o
8225000 9325000 ts
9325000 9625000 u
9625000 9925000 g
9925000 10325000 i
10325000 11225000 k
11225000 11725000 o
11725000 12725000 w
12725000 14125000 a
14125000 16425000 silE
```

You need to have `julius` installed at `/usr/bin/julius`. If you have in another location, specify the path at `julius_path=` parameter of `align()`.