from onso_aligner.yomi_to_voca import yomi_to_voca


def test_yomi_to_voca() -> None:
    assert yomi_to_voca("こんにちわ") == "k o N n i ch i w a"
    assert (
        yomi_to_voca("ヴァイオリンソーシャヴィクトリア")
        == "b a i o r i N s o: sh a b i k u t o r i a"
    )
    assert yomi_to_voca("こ、、こんにちわ。") == "k o sp k o N n i ch i w a"
    assert yomi_to_voca("ひゃくじゅーのおー") == "hy a k u j u: n o o:"
    assert yomi_to_voca("あーーーー") == "a:"
    assert yomi_to_voca("んー") == "N N"
    assert yomi_to_voca("テュー") == "ch u:"