import re

from typing import List


def delete_emoji(text):
    """
    絵文字を削除する
    """
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # 笑顔の顔文字
        u"\U0001F300-\U0001F5FF"  # シンボルと絵文字
        u"\U0001F680-\U0001F6FF"  # トランスポートと地図の絵文字
        u"\U0001F1E0-\U0001F1FF"  # 国旗（iOS）の絵文字
        u"\ufe0f"
        "]+",
        flags=re.UNICODE
    )

    return emoji_pattern.sub(r'', text)


def delete_username(text):
    """
    テキストからユーザーネームを削除する
    """
    username_pattern = re.compile(r'@\w+[\w.]*\s*')
    return username_pattern.sub(r'', text)


def sort_kanji_kana_hira(nanos: List[str]) -> List[str]:
    """
    漢字、カタカナ、ひらがな、ローマ字の順にソートする
    """
    kanji = []
    kana = []
    hira = []
    roma = []

    for nano in nanos:
        if re.search(r'[\u4E00-\u9FFF]', nano):
            kanji.append(nano)
        elif re.search(r'[\u30A0-\u30FF]', nano):
            kana.append(nano)
        elif re.search(r'[\u3040-\u309F]', nano):
            hira.append(nano)
        else:
            roma.append(nano)

    return kanji + kana + hira + roma


def is_all_number(nanos: List[str]) -> bool:
    """
    テキストが全て数字かどうかを判定する
    """
    for nano in nanos:
        if not nano.isdecimal():
            return False
    return True
