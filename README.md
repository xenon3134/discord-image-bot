# discord-image-bot

## 概要
- 指定したフォルダにある画像を定期的にランダムにDiscordに投稿してくれるBotです。
- ※ちゃんとテストしていないので、バグが残っているかもです。

## 導入
- pythonをインストールしていなければしてください。
  - https://www.python.org/downloads/
- discordライブラリインストール
  - `pip install discord.py`
- discord bot作成
  - https://discordpy.readthedocs.io/ja/stable/discord.html
  - botのtokenをメモ
  - 自分のdiscordサーバーにbot追加
- bot.py書き換え
  - `TOKEN`を上記のbotのtokenにする。
  - `TARGET_DIR`を投稿対象のフォルダにする。
  - `INTERVAL`（投稿間隔）を変更。デフォルトは1時間ごと。
  - `IS_ADMIN_ONLY` 管理者のみがbotのコマンドを実行できるようにする。デフォルトはTrue。(未テスト)
- bot_start.batを叩いて、bot起動

## コマンド
- `画像投稿Bot開始`
  - 定期ランダム投稿開始
- `画像投稿Bot終了`
  - 定期ランダム投稿終了
- `画像投稿Botファイル数`
  - 投稿対象のファイル数表示
- `画像投稿Botリロード`
  - 投稿対象ファイル再読み込み
