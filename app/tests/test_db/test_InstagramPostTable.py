from db import InstagramPostTable
import pytest  # noqa


class TestInstagramPostTable_get_influencer_posts:
    """
    InstagramPostTable().get_influencer_postsのテスト
    """

    def test_get_all(self):
        """influencer_idに一致するデータを全て取得する"""
        instagram_db = InstagramPostTable()
        influencer_id = '1'
        posts = instagram_db.get_influencer_posts(influencer_id)
        assert len(posts) == 12

    def test_get_all_not_found(self):
        """存在しないinfluencer_idのデータを取得する"""
        instagram_db = InstagramPostTable()
        influencer_id = '77777777'
        posts = instagram_db.get_influencer_posts(influencer_id)
        assert len(posts) == 0

    def test_get_limit(self):
        """limitの数だけデータを取得する"""
        instagram_db = InstagramPostTable()
        influencer_id = '1'
        limit = 3
        posts = instagram_db.get_influencer_posts(influencer_id, limit)
        assert len(posts) == limit


class TestInstagramPostTable_get_influencer_nouns:
    """
    InstagramPostTable().get_influencer_nounsのテスト
    """

    def test_get_all(self):
        """
        influencer_idに一致するデータを全て取得する

        influencer_idのデータは以下の通り↓

        隠れてピンプリ撮ってきたっす
        印刷待ってる間のハラハラがつらい
        温泉♨️
        「なえなののブカピなの」の収録の時にガチで寝てしまいました😀
        すぐ起こされたけど笑笑

        #ブレインスリープ
        #ブレインスリープピロー
        #脳が眠る枕
        #お気に入り
        #寝心地最高
        #pr
        趣味はUFOキャッチャー😵‍💫✌️
        お知らせです📢！

        なんとテレビ番組のMCをさせてもらえることになりました！
        なんてこった〜！！

        10/5(火)〜
        「部活ピーポー全力応援！ブカピ！」

        がんばりますのでよろしくお願いします☁️☁️
        新入りくまさん🐻‍❄️
        モデルさせていただきました🤍
        お洋服ぜ〜んぶかわいい

        @romansual_official
        LARME 050 発売日です❕
        記念の50号、もうすでにゲットしたよ〜って報告してくれた方ありがとう
        今回も可愛いが詰まりに詰まってますんです
        是非に☺️
        @larmemagazine
        猛暑の中での撮影でめためた大変だったオモヒデ😵‍💫
        スウェットとか可愛いのたくさん！チェックしてね〜
        @wego_official
        ブラックコーデ🥱
        VANSの白ステッチがかわいい〜
        急いでる時にスッてはけるのが◎！
        何と合わせてもかわいいね
        @vansjapan
        #vansjapan
        #vansmule
        #PR
        毎回お洋服が可愛くて撮影スタッフさんだいすきで本当に楽しい現場😵‍💫🤍
        WEGO Magazine最新号の限定カバーなど秋ビジュアルに登場させていただきました🍄
        是非チェックを〜！！ #wego
        夕日きれ〜☁️

        昨日お知らせしましたが、 @sooogood.s.k さんの新曲のMVに出させていただいてます！
        なえのYouTubeのBGMを作ってくださったアーティストさんです☺️

        是非に！見てください！

        """
        instagram_db = InstagramPostTable()
        influencer_id = '1'
        posts = instagram_db.get_influencer_nouns(
            influencer_id=influencer_id,
            limit=10
        )
        assert len(posts) == 10

        posts = instagram_db.get_influencer_nouns(
            influencer_id=influencer_id,
            limit=20
        )
        assert len(posts) == 20


class TestInstagramPostTable_get_influencers_by_likes:
    """
    InstagramPostTable().get_influencers_by_likesのテスト
    """

    def test_get_limit_30(self):
        """全てのデータを取得する"""
        instagram_db = InstagramPostTable()
        limit = 30
        posts = instagram_db.get_influencers_by_likes(limit)
        assert len(posts) == limit
        assert posts[0].influencer_id == '71'

    def test_get_limit_3(self):
        """limitの数だけデータを取得する"""
        instagram_db = InstagramPostTable()
        limit = 3
        posts = instagram_db.get_influencers_by_likes(limit)
        assert len(posts) == limit
        assert posts[0].influencer_id == '71'


class TestInstagramPostTable_get_influencers_by_comments:
    """
    InstagramPostTable().get_influencers_by_commentsのテスト
    """

    def test_get_all(self):
        """全てのデータを取得する"""
        instagram_db = InstagramPostTable()
        limit = 5
        posts = instagram_db.get_influencers_by_comments(limit)
        assert len(posts) == limit
        assert posts[0].influencer_id == '1'

    def test_get_limit(self):
        """limitの数だけデータを取得する"""
        instagram_db = InstagramPostTable()
        limit = 3
        posts = instagram_db.get_influencers_by_comments(limit)
        assert len(posts) == limit
        assert posts[0].influencer_id == '1'
