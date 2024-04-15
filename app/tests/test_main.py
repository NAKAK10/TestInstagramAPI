import pytest
from main import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_influencer_average(client):
    res = client.post('/api/influencer/average', json={'influencer_id': '1'})
    assert res.status_code == 200
    assert res.json['influencer_id'] == '1'
    assert isinstance(res.json['likes'], float)
    assert isinstance(res.json['comments'], float)


def test_ranking_likes(client):
    res = client.post(
        '/api/ranking/likes',
        json={'limit': 3}
    )
    res_dict = res.json
    assert res.status_code == 200
    assert len(res_dict) == 3
    for data in res_dict:
        assert isinstance(data['influencer_id'], str)
        assert isinstance(data['avg_likes'], float)


def test_ranking_comments(client):
    res = client.post(
        '/api/ranking/comments',
        json={'limit': 3}
    )
    res_dict = res.json
    assert res.status_code == 200
    assert len(res_dict) == 3
    for data in res_dict:
        assert isinstance(data['influencer_id'], str)
        assert isinstance(data['avg_comments'], float)


def test_influencer_nouns(client):
    res = client.post(
        '/api/influencer/nouns',
        json={'influencer_id': '1', 'limit': 3}
    )
    res_dict = res.json
    assert res.status_code == 200
    assert res_dict['influencer_id'] == '1'
    assert len(res_dict['data']) == 3
    for data in res_dict['data']:
        assert isinstance(data['nouns'], str)
        assert isinstance(data['count'], int)
