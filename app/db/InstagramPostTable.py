import mysql.connector
import pandas as pd
import MeCab

from db import InstagramDB
from utils import (delete_emoji, delete_username,
                   sort_kanji_kana_hira, is_all_number)

from typing import Optional,  List
import dataclasses


@dataclasses.dataclass
class InstagramPost:
    """
    Instagram の投稿データを表すクラス

    influencer_id: str
        インフルエンサーID
    post_id: str
        投稿ID
    shortcode: str
        ショートコード
    likes: int
        いいね数
    comments: int
        コメント数
    thumbnail: str
        サムネイルURL
    text: str
        投稿文
    post_date: str
        投稿日
    """
    influencer_id: str
    post_id: str
    shortcode: str
    likes: int
    comments: int
    thumbnail: str
    text: str
    post_date: str


@dataclasses.dataclass
class InfluencerLikes:
    """
    Influencer平均いいね数を表すクラス

    influencer_id: str
        インフルエンサーID
    avg_likes: float # 小数第2位まで
        平均いいね数
    """
    influencer_id: str
    avg_likes: float

    def __init__(self, influencer_id: str, avg_likes: float):
        self.influencer_id = influencer_id
        self.avg_likes = float(round(avg_likes, 2))


@dataclasses.dataclass
class InfluencerComments:
    """
    Influencer平均コメント数を表すクラス

    influencer_id: str
        インフルエンサーID
    avg_comments: float # 小数第2位まで
        平均コメント数
    """
    influencer_id: str
    avg_comments: float

    def __init__(self, influencer_id: str, avg_comments: float):
        self.influencer_id = influencer_id
        self.avg_comments = float(round(avg_comments, 2))


@dataclasses.dataclass
class PostsNouns:
    """
    名詞とカウントを表すクラス

    nouns: str
        名詞
    count: int
        カウント
    """
    nouns: str
    count: int


class InstagramPostTable:
    """
    Instagram の MySQLデータベースへの接続を管理するクラス
    """

    def __init__(self):
        pass

    def get_influencer_posts(self, influencer_id: str, limit: Optional[int] = None) -> List[InstagramPost]:
        """
        MySQL データベースから influencer_id に一致するデータを取得する

        Params:
        ---
        influencer_id: str
            取得したいデータの influencer_id
        limit: Optional[int]
            取得するデータの上限数
            新着順に取得するため、最新のデータから limit 件取得する

        Returns:
        ---
        List[InstagramPost]
        """

        # データを取得するためのクエリ
        select_query = f"""
        SELECT *
        FROM t_influencer_posts
        WHERE influencer_id = {influencer_id}
        ORDER BY post_date DESC
        """

        if isinstance(limit, int) and limit > 0:
            # 新着順
            select_query += f" LIMIT {limit}"

        # influencer_id に一致するデータを取得
        try:
            result = InstagramDB().get_data(select_query)
            res = [InstagramPost(*row) for row in result]
            return res

        except mysql.connector.Error:
            return []

    def get_influencer_nouns(self, influencer_id: str, limit: Optional[int] = 10) -> List[PostsNouns]:
        """
        Params:
        ---
        influencer_id: str
            取得したいデータの influencer_id
        limit: Optional[int]
            取得するデータの上限数
            default: 10

        Returns:
        ---
        List[PostsNouns]
        """

        tagger = MeCab.Tagger()

        influencer_data = self.get_influencer_posts(influencer_id)

        count_nouns = {}
        all_nouns: List[List[str]] = []

        for n in influencer_data:
            _text = n.text

            # 絵文字を削除
            _text = delete_emoji(_text)
            # ユーザ名を削除
            _text = delete_username(_text)

            result = tagger.parse(_text)
            result_line = result.split('\n')

            for _line in result_line:
                # 名詞を取得
                if '名詞' in _line:
                    nanos = sort_kanji_kana_hira(_line.split('\t')[:3])

                    if is_all_number(nanos):
                        continue

                    count_nouns[nanos[0]] = 0
                    all_nouns.append(nanos)

        # count_nounsにカウントを追加
        for nanos in count_nouns.keys():
            count_num = 0
            for n in all_nouns:
                if nanos in n:
                    count_num += 1
            count_nouns[nanos] = count_num

        # カウント数でソート List[PostsNouns]
        count_list = sorted(count_nouns.items(), key=lambda x: x[1], reverse=True)
        if limit:
            count_list = count_list[:limit]

        return [PostsNouns(nouns, count) for nouns, count in count_list]

    def get_influencers_by_likes(self, limit: int = 30) -> List[InfluencerLikes]:
        """
        平均いいね数が多いinfluencer上位N件を取得

        Params:
        ---
        limit: int
            取得するデータの上限数
            default: 30

        Returns:
        ---
        List[InstagramPost]
        """

        # データを取得するためのクエリ
        select_query = f"""
        SELECT influencer_id, AVG(likes) as avg_likes
        FROM t_influencer_posts
        GROUP BY influencer_id
        ORDER BY avg_likes DESC
        LIMIT {limit}
        """

        # influencer_id に一致するデータを取得
        try:
            result = InstagramDB().get_data(select_query)
            return [InfluencerLikes(*row) for row in result]
        except mysql.connector.Error:
            return []

    def get_influencers_by_comments(self, limit: int = 30) -> List[InfluencerComments]:
        """
        平均コメント数が多いinfluencer上位N件を取得

        Params:
        ---
        limit: int
            取得するデータの上限数
            default: 30

        Returns:
        ---
        List[InstagramPost]
        """

        # データを取得するためのクエリ
        select_query = f"""
        SELECT influencer_id, AVG(comments) as avg_comments
        FROM t_influencer_posts
        GROUP BY influencer_id
        ORDER BY avg_comments DESC
        LIMIT {limit}
        """

        # influencer_id に一致するデータを取得
        try:
            result = InstagramDB().get_data(select_query)
            return [InfluencerComments(*row) for row in result]
        except mysql.connector.Error:
            return []

    def _save_influencer_posts(self, df: pd.DataFrame):
        """
        ## セットアップ用のメソッドであり、通常は使用しない
        DataFrameのデータを MySQL データベースに保存する
        """

        # t_influencer_posts テーブルが存在しない場合は作成
        tables = InstagramDB().get_data("SHOW TABLES")

        if ('t_influencer_posts',) not in tables:
            insert_query = """
            CREATE TABLE IF NOT EXISTS t_influencer_posts (
                influencer_id VARCHAR(255),
                post_id VARCHAR(255),
                shortcode VARCHAR(255),
                likes INT,
                comments INT,
                thumbnail TEXT,
                text TEXT,
                post_date DATE,
                PRIMARY KEY (post_id)
            )
            """
            InstagramDB().commit_data(insert_query)

        # データを挿入するためのクエリ
        insert_query = """
        INSERT INTO t_influencer_posts
        (influencer_id, post_id, shortcode, likes, comments, thumbnail, text, post_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # データと列名の整合性を確認
        columns = df.columns
        if not all([col in columns for col in ['influencer_id', 'post_id', 'shortcode', 'likes', 'comments', 'thumbnail', 'text', 'post_date']]):
            raise ValueError("DataFrameに必要な列が存在しません。")

        # データの値を整形
        df = df.where(pd.notnull(df), None)
        df['post_date'] = pd.to_datetime(df['post_date']).dt.date

        InstagramDB().commit_data(insert_query, df)

        return "success"

    def _delete_all_influencer_posts(self):
        """
        ## セットアップ用のメソッドであり、通常は使用しない
        t_influencer_posts テーブルを削除
        """
        tables = InstagramDB().get_data("SHOW TABLES")

        if ('t_influencer_posts',) in tables:
            print("t_influencer_posts テーブルを削除しますか？ (Y/n)")
            answer = input()

            if answer.lower() != "y":
                print("処理を中断します。")
                return
        else:
            return

        # テーブルを削除するためのクエリ
        delete_query = "DROP TABLE IF EXISTS t_influencer_posts"

        InstagramDB().commit_data(delete_query)

        return "success"
