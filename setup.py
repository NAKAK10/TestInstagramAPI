import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))  # noqa


import pandas as pd
from db import InstagramPostTable


if __name__ == '__main__':
    db = InstagramPostTable()
    db._delete_all_influencer_posts()

    # テストデータの作成
    csv_path = './t_influencer_posts_202401121334.csv'

    # CSVファイルを読み込む
    df = pd.read_csv(csv_path)

    print('データの保存を開始します...')

    db._save_influencer_posts(df)

    print('データの保存が完了しました。')
