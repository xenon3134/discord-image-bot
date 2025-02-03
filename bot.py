import discord
from discord.ext import commands
import random
from pathlib import Path
import asyncio
import os

TOKEN = 'My discord bot token' # Discord Botを作成して、そのTokenに書き換えてください。

TARGET_DIR = r"C:\Users\Public\Pictures" # 投稿対象のフォルダ名（指定したフォルダ以下の全画像を投稿対象にする）
COMMAND_PREFIX = "画像投稿Bot" # Botを呼び出す時に文頭に付けるキーワード（例：画像投稿Bot開始、画像投稿B終了など）
TARGET_FILE_SUFFIXES = {".png", ".jpg"} # 対象ファイルの拡張子
MAX_FILE_COUNT = 1e6 # 100万枚 # 対象ファイルの上限
MAX_FILE_SIZE = 1e7 # 10MB # 対象ファイルのサイズ上限。上限を超えたファイルはスキップ。無課金のDiscordサーバーだと上限は10MB。
INTERVAL = 60 * 60 # 1時間 #　自動投稿の間隔
IS_ADMIN_ONLY = True # 管理者のみ実行可能か

file_paths = []
stop_event = None

bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    intents=discord.Intents.all(),
)

@bot.event
async def on_ready():
    # Botの準備完了時に呼び出されるイベント
    print('We have logged in as {0}'.format(bot.user))
    _load_files()

@bot.command(name='開始')
async def start(ctx):
    # 「画像投稿Bot開始」と入力すると、定期ランダム投稿開始。
    if not await _validate(ctx):
        return
    
    global stop_event
    if stop_event:
        await ctx.send("既に画像投稿を開始しています。")
    else:
        stop_event = asyncio.Event()
        while not stop_event.is_set():
            if not file_paths:
                await ctx.send("対象のファイルがありません。")
                break

            choice_file_path = None
            while not choice_file_path:
                if not file_paths:
                    break
                tmp_path = random.choice(file_paths)
                file_paths.remove(tmp_path)
                file_size = os.path.getsize(tmp_path)
                if file_size > MAX_FILE_SIZE:
                    print(f"ファイルサイズが大きすぎるのでスキップします。ファイル名: {tmp_path}, サイズ: {file_size}B")
                else:
                    choice_file_path = tmp_path

            if choice_file_path:
                await ctx.send(file=discord.File(choice_file_path))
                tasks = [
                    asyncio.create_task(asyncio.sleep(INTERVAL)),
                    asyncio.create_task(stop_event.wait())
                ]
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in pending:
                    task.cancel()

        stop_event = None
        await ctx.send("画像投稿を終了しました。")

@bot.command(name='終了')
async def end(ctx):
    # 「画像投稿Bot開始」と入力すると、定期ランダム投稿終了。
    if not await _validate(ctx):
        return
    if stop_event:
        stop_event.set()
    else:
        await ctx.send("画像投稿を開始していません。")

@bot.command(name='ファイル数')
async def ramdom(ctx):
    # 「画像投稿Botファイル数」と入力すると、投稿対象のファイル数を表示。
    if not await _validate(ctx):
        return
    await ctx.send(f"残りのファイル数は{len(file_paths)}です。")

@bot.command(name='リロード')
async def reload(ctx):
    # 「画像投稿Botリロード」と入力すると、投稿対象のファイルを再度読込。
    if not await _validate(ctx):
        return
    _load_files()
    await ctx.send(f"リロードしました。残りのファイル数は{len(file_paths)}です。")

def _load_files() -> list:
    file_paths.clear()
    path_ite = (str(f) for f in Path(TARGET_DIR).rglob("*") if f.suffix.lower() in TARGET_FILE_SUFFIXES)
    for i, p in enumerate(path_ite):
        if i >= MAX_FILE_COUNT:
            break
        file_paths.append(p)

async def _validate(ctx) -> bool:
    if ctx.author == bot.user:
        return False
    perms = ctx.author.guild_permissions
    if IS_ADMIN_ONLY and not perms.administrator:
        await ctx.send("管理者しか実行できません。")
        return False
    return True
    
if __name__ == '__main__':
    bot.run(TOKEN)
