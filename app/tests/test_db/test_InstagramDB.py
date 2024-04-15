import pytest

import pandas as pd
from db import InstagramDB


@pytest.fixture
def instagram_db():
    instagram_db = InstagramDB()
    yield instagram_db


@pytest.fixture
def test_data() -> pd.DataFrame:
    """
    テスト用のデータ
    """
    return pd.DataFrame({
        'id': [1, 2],
        'name': ['John', 'Doe']
    })


def test_is_already_table(instagram_db):
    # テスト用のテーブル名
    table_name = "test_table_test_table"
    # テーブル存在確認テスト
    result = instagram_db.is_already_table(table_name)
    assert not result


def test_commit_data(instagram_db, test_data):
    result = instagram_db.is_already_table('test_table')
    if result:
        pytest.skip('テーブルが存在しているためスキップ')
    else:
        # test_tableを作成
        query = """
        CREATE TABLE IF NOT EXISTS test_table (
            id INT,
            name VARCHAR(255),
            PRIMARY KEY (id)
        )
        """
        instagram_db.commit_data(query)

    # テスト用のクエリ
    query = "INSERT INTO test_table (id, name) VALUES (%s, %s)"

    # データ挿入テスト
    try:
        result = instagram_db.commit_data(query, test_data)
    except ValueError as err:
        print(err)
        result = "error"

    assert result == "success"


def test_get_data(instagram_db):
    # テスト用のクエリ
    query = "SELECT * FROM test_table"
    # データ取得テスト
    result = instagram_db.get_data(query)

    assert len(result) == 2
