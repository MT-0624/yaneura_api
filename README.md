# yaneura_api

やねうらお様によるコンピューター将棋ソフトやねうら王をサーバ上で駆動させて<br>
形勢や最善手、読み筋を返すAPIを製作中です<br>

VPSにて思考時間を検証をしています、十分な形勢判断に必要なdepthと思考時間のトレードがいい感じだったら
部分的にも公開しようかなという状態です
やねうら王 -> https://yaneuraou.yaneu.com/ <br>
やねうらお様リポジトリ -> https://github.com/yaneurao/YaneuraOu
<br>

## 現構成
docker-composeで<br>
【dbコンテナ】（定跡・キャッシュ・リクエストを持つデータベース）<br>
【apiコンテナ】（webリクエストにて局面を受け付けるand形勢を返す）<br>
【AIコンテナ】（ビルドしたやねうら王）<br>
## 自分用イメージ
![image](https://user-images.githubusercontent.com/41203239/125211429-40589c00-e2e1-11eb-8ffc-51d68347872d.png)
