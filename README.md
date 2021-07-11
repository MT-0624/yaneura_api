# yaneura_flask

やねうらお様によるコンピューター将棋ソフトやねうら王をサーバ上で駆動させて<br>
形勢を返すAPI<br>
やねうら王 -> https://yaneuraou.yaneu.com/
<br>

## 現構成
docker-composeで<br>
【dbコンテナ】（定跡・キャッシュ・リクエストを持つデータベース）
【apiコンテナ】（webリクエストを）
【AIコンテナ】（ビルドしたやねうら王）
