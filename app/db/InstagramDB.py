import mysql.connector
from mysql.connector.connection import MySQLConnection
from config import INSTAGRAM_DB_CONFIG
import pandas as pd

from typing import Optional, Callable, List


class InstagramDB:
    """
    INSTAGRAM_DB_CONFIGの設定を元に、MySQLデータベースへの接続を管理するクラス
    """

    def __init__(self):
        self._config = INSTAGRAM_DB_CONFIG
        self.conn: Optional[MySQLConnection] = None

    @property
    def config(self):
        return self._config

    def _connection(func: Callable):
        def wrapper(self, *args, **kwargs):
            conn = mysql.connector.connect(**self._config)
            try:
                if conn.is_connected():
                    self.conn = conn
                    print("\033[90mMySQLデータベースへの接続が成功しました。\033[0m")
                else:
                    print("\033[91mMySQLデータベースへの接続が失敗しました。\033[0m")
            except mysql.connector.Error as err:
                raise err

            res = func(self, *args, **kwargs)

            if conn.is_connected():
                conn.close()
                self.conn = None

            return res

        return wrapper

    @_connection
    def get_data(self, query: str) -> List[mysql.connector.types.RowType]:
        """
        MySQL データベースからデータを取得する

        Params:
        ---
        query: str
            取得したいデータのクエリ

        Returns:
        ---
        List[RowType]

        Raises:
        ---
        mysql.connector.Error: MySQL データベースでエラーが発生した場合
        """
        cursor = self.conn.cursor()

        cursor.execute(query)
        result = cursor.fetchall()

        return result

    @_connection
    def commit_data(self, query: str, data: Optional[pd.DataFrame] = None) -> str:
        """
        MySQL データベースにデータを挿入する

        Params:
        ---
        query: str
            データを挿入するためのクエリ
        data: Optional[pd.DataFrame]
            挿入するデータ

        Returns:
        ---
        str: "success"

        Raises:
        ---
        ValueError: DataFrameに必要な列が存在しない場合
        mysql.connector.Error: MySQL データベースでエラーが発生した場合
        """
        cursor = self.conn.cursor()

        if data is None:
            cursor.execute(query)
            self.conn.commit()
            return "success"

        for row in data.itertuples(index=False):
            cursor.execute(query, tuple(row))
        self.conn.commit()

        return "success"

    @_connection
    def is_already_table(self, table_name: str) -> bool:
        """
        MySQL データベースにテーブルが存在するか確認する

        Params:
        ---
        table_name: str
            テーブル名

        Returns:
        ---
        bool
        """
        cursor = self.conn.cursor()

        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()

        return True if result else False
