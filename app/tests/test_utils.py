from utils import (
    delete_emoji,
    delete_username,
    sort_kanji_kana_hira,
    is_all_number
)


def test_delete_emoji():
    assert delete_emoji('😅') == ''
    assert delete_emoji('こんにちは😅') == 'こんにちは'
    assert delete_emoji('🇯🇵') == ''
    assert delete_emoji('💍') == ''
    assert delete_emoji('🗺️') == ''


def test_delete_username():
    assert delete_username('@aaaa.sssss ありがとうございます') == 'ありがとうございます'
    assert delete_username('@aaaa_sssss__ ありがとうございます') == 'ありがとうございます'
    assert delete_username('@aaaa_sssss. ありがとうございます') == 'ありがとうございます'
    assert delete_username('@aaaa_sssbb\nありがとうございます') == 'ありがとうございます'


def test_sort_kanji_kana_hira():
    nanos = ['印刷', 'インサツ', 'インサツ']
    assert sort_kanji_kana_hira(nanos) == ['印刷', 'インサツ', 'インサツ']

    nanos = ['インサツ', 'インサツ', '印刷']
    assert sort_kanji_kana_hira(nanos) == ['印刷', 'インサツ', 'インサツ']

    nanos = ['白', 'シロ', 'しろ']
    assert sort_kanji_kana_hira(nanos) == ['白', 'シロ', 'しろ']


def test_is_all_number():
    nanos = ['1', '2', '3']
    assert is_all_number(nanos)

    nanos = ['1', '2', '3', 'a']
    assert not is_all_number(nanos)

    nanos = ['1', '2', '3', '']
    assert not is_all_number(nanos)
