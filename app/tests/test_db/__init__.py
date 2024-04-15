import sys
import os

# srcディレクトリをパッケージとして認識させるために、sys.pathに追加する
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app')))
