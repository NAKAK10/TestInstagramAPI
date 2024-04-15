from flask import Flask, request
from db import InstagramPostTable


def create_app():

    app = Flask(__name__)

    @app.route('/api/documentation')
    def index():
        return 'API Documentation', 200

    @app.route('/api/influencer/average', methods=['POST'])
    def influencer_average():
        """
        influencer_idをAPIのリクエストデータとして、平均いいね数、平均コメント数をJSON形式で返す

        Usage:
        ---
        curl -X POST http://localhost:4545/api/influencer/average -H 'Content-Type: application/json' -d '{"influencer_id": "1"}'

        Params:
        ---
        POST /api/influencer
        headers: {
            'Content-Type': 'application/json'
        }
        body: {
            'influencer_id': str
        }

        Returns:
        ---
        {
            'influencer_id': str,
            'likes': float,
            'comments': float
        }
        """

        influencer_id = request.json['influencer_id']

        if not influencer_id:
            return 'influencer_id is required', 400

        db = InstagramPostTable()

        try:
            posts = db.get_influencer_posts(influencer_id)
        except Exception as e:
            return f'Internal Server Error: {e}', 500

        res = {
            'influencer_id': influencer_id,
            'likes': round(sum([post.likes for post in posts]) / len(posts), 1),
            'comments': round(sum([post.comments for post in posts]) / len(posts), 1)
        }

        return res, 200

    @app.route('/api/influencer/nouns', methods=['POST'])
    def influencer_nouns():
        """
        influencer_id毎に、格納したデータのtextカラムに格納されたデータから名詞を抽出し、その使用回数を集計し、上位N件（NはAPIのリクエストデータ）をJSON形式で返す

        Usage:
        ---
        curl -X POST http://localhost:4545/api/influencer/nouns -H 'Content-Type: application/json' -d '{"influencer_id": "1", "limit": 10}'

        Params:
        ---
        POST /api/influencer/nouns
        headers: {
            'Content-Type': 'application/json'
        }
        body: {
            'influencer_id': str,
            'limit': Optional[int] # default 10
        }

        Returns:
        ---
        {
            'influencer_id': str
            'data': [
                {
                    'noun': str,
                    'count': int
                },
                ...
            ]

        }
        """

        influencer_id = request.json['influencer_id']
        limit = request.json.get('limit', 10)

        if not influencer_id:
            return 'influencer_id is required', 400

        if isinstance(limit, int) and limit <= 0:
            return 'limit must be greater than 0', 400

        db = InstagramPostTable()

        try:
            posts = db.get_influencer_nouns(influencer_id, limit)
        except Exception as e:
            return f'Internal Server Error: {e}', 500

        res = {
            'influencer_id': influencer_id,
            'data': [
                {
                    'nouns': post.nouns,
                    'count': post.count
                }
                for post in posts
            ]
        }

        return res, 200

    @app.route('/api/ranking/likes', methods=['POST'])
    def ranking_likes():
        """
        平均いいね数が多いinfluencer上位N件をJSON形式で返す

        Usage:
        ---
        curl -X POST http://localhost:4545/api/ranking/likes -H 'Content-Type: application/json' -d '{"limit": 10}'

        Params:
        ---
        POST /api/ranking/likes
        headers: {
            'Content-Type': 'application/json'
        }
        body: {
            'limit': Optional[int] # default 30
        }

        Returns:
        ---
        [
            {
                'influencer_id': str,
                'avg_likes': float
            },
            ...
        ]
        """

        limit = request.json.get('limit', None)

        if isinstance(limit, int) and limit <= 0:
            return 'limit must be greater than 0', 400

        db = InstagramPostTable()

        try:
            influencers = db.get_influencers_by_likes(limit)
        except Exception as e:
            return f'Internal Server Error: {e}', 500

        res = [
            {
                'influencer_id': influencer.influencer_id,
                'avg_likes': influencer.avg_likes
            }
            for influencer in influencers
        ]

        return res, 200

    @app.route('/api/ranking/comments', methods=['POST'])
    def ranking_comments():
        """
        平均コメント数が多いinfluencer上位N件をJSON形式で返す

        Usage:
        ---
        curl -X POST http://localhost:4545/api/ranking/comments -H 'Content-Type: application/json' -d '{"limit": 10}'

        Params:
        ---
        POST /api/ranking/comments
        headers: {
            'Content-Type': 'application/json'
        }
        body: {
            'limit': Optional[int] # default 30
        }

        Returns:
        ---
        [
            {
                'influencer_id': str,
                'avg_comments': float
            },
            ...
        ]
        """

        limit = request.json.get('limit', None)

        if isinstance(limit, int) and limit <= 0:
            return 'limit must be greater than 0', 400

        db = InstagramPostTable()
        try:
            influencers = db.get_influencers_by_comments(limit)
        except Exception as e:
            return f'Internal Server Error: {e}', 500

        res = [
            {
                'influencer_id': influencer.influencer_id,
                'avg_comments': influencer.avg_comments
            }
            for influencer in influencers
        ]

        return res, 200

    return app


app = create_app()


if __name__ == '__main__':
    port = 4545

    print('API Server is running...')
    print(f'http://localhost:{port}/api/documentation')
    print(f'http://localhost:{port}/api/influencer/average')
    print(f'http://localhost:{port}/api/influencer/nouns')
    print(f'http://localhost:{port}/api/ranking/likes')
    print(f'http://localhost:{port}/api/ranking/comments')

    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
