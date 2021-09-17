import os

import onso_aligner


def test_model_downloader() -> None:
    model_path = onso_aligner.model.retrieve()
    assert os.path.exists(model_path)


def test_align() -> None:
    results = onso_aligner.align(
        "./tests/fixtures/meian_1413.wav", "あねむすめのつぎこわ"
    )

    assert len(results) == 21
    assert results[0] == (0, 1525000, "silB")
    assert results[1] == (1525000, 3025000, "a")
    assert results[-1] == (14125000, 16425000, "silE")
