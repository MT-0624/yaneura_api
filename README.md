# yaneura_api

やねうらお様によるコンピューター将棋ソフトやねうら王をサーバ上で駆動させて<br>
形勢や最善手、読み筋を返すAPIを製作中です<br>

httpリクエストのたびにやねうら王を起動させるのではなく<br>
間にMysqlなどのDBを挟むことで、キャッシュとロードバランサーと待ち行列的な役割を担ってくれるのではないかと考えています。<br>

VPSに正常に動作するかを検証をしています、十分な形勢判断に必要なdepthと思考時間のトレードがいい感じだったら<br>
限定的にも公開しようかなという状態です<br>
やねうら王 -> https://yaneuraou.yaneu.com/ <br>
やねうらお様リポジトリ -> https://github.com/yaneurao/YaneuraOu


###追記issue（2021-08-18）
・非同期処理でスレッドを立てて解析すると正しく完了せずプロセスが残ることがある<br>


## 現構成
docker-composeで<br>
【dbコンテナ】（定跡・キャッシュ・リクエストを持つデータベース）<br>
【apiコンテナ】（webリクエストにて局面を受け付けるand形勢を返す）<br>
【AIコンテナ】（ビルドしたやねうら王）<br>
## 自分用イメージ
![image](https://user-images.githubusercontent.com/41203239/125211429-40589c00-e2e1-11eb-8ffc-51d68347872d.png)
