# TestInstagramAPI

## Setup

### ファイルのコピー

- t_influencer_posts_202401121334.csv をダウンロード
- t_influencer_posts_202401121334.csv を root に作成する

### Docker イメージのビルド

```bash
docker compose up -d --build
```

### Docker コンテナに入る

```bash
docker compose exec app bash
```

### データベースの作成

```bash
python setup.py
```

## Test

- Docker コンテナに入る

```bash
docker compose exec app bash
```

- app ディレクトリに移動

```bash
cd app
```

- テストを実行

```bash
pytest -s
```
