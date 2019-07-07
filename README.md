# Sousei Flask

大阪大学電子情報工学科 2 年生での電子情報工学創生実験で使用される創成コイン(通称 SC)の管理 Web アプリです

このアプリは MIT ライセンスで公開しています

## Develop

開発環境の構築には python と python のパッケージ管理ツール pip が必要です

pip を使い依存パッケージをインストールします

```
$ pip install -r requirements.txt
```

アプリを起動します

```
$ cd app/
$ python main.py
```

以下の URL でアクセスできます

<http://127.0.0.1:5000/>

これは開発用サーバーですので本番環境で使用しないでください

ユーザーの購入履歴等、各種データは app/app.db に保存されています。このファイルを削除することでアプリを完全に初期化することができます

## Deploy on own server

あらかじめ SSL が設定されたサーバーを用意してください

variable.py にアプリ名、創成コインの初期分配値、管理者とユーザーのユーザー名・パスワード、品物リストを設定します

Docker を使ってアプリを起動します

公開するサーバーに [Docker Documentation](https://docs.docker.com/) を参考に Docker をインストールしてください

以下の Docker Image を使い、アプリを起動します

[tiangolo/uwsgi-nginx-flask-docker - Docker Hub](https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/)

以下のコマンドを実行すると 80 番ポートでアプリが起動します

```
$ docker build -t sousei_flask_image ./
$ docker run -d --name sousei_flask_container -p 80:80 sousei_flask_image
```

サーバー停止コマンドは

```
$ docker stop sousei_flask_container
```

です

その他各種コマンドは [Docker Documentation](https://docs.docker.com/) にて確認してください

## Deploy on AWS

### EC2

- EC2 インスタンスを立てる

- Docker をインストールし、アプリを実行

- ALB を HTTPS でセットアップする

  - インバウンドの HTTPS のソースを 133.1.0.0/16 にすることで大学ネットワーク内のみからアクセス可能となる

- EC2 インスタンスのインバウンド HTTP を ALB のセキュリティグループ ID にする

- Route53 で任意のドメインに A レコードで ALB を登録

### ECS

- ECR に Docker Image を登録

- ECS で ALB 付きでコンテナを起動

- ALB のリスナーに HTTPS を追加

  - ACM で SSL 証明書を追加する

- ALB のセキュリティグループでインバウンドのルールに HTTPS を追加

  - インバウンドの HTTPS のソースを 133.1.0.0/16 にすることで大学ネットワーク内のみからアクセス可能となる

- Route53 で任意のドメインに A レコードで ALB を登録
