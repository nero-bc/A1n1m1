from Config import TOKEN 
from telegram import Bot , Update , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler , ContextTypes , CallbackQueryHandler , MessageHandler , filters
from Plugins.Commands import  start_command , latest_command , popular_command ,broadcast_command , restart_per_2_hours , post_command , anime_command ,  airing_command , schedule_command , feedback_command , help_command , ping_command , character_command , manga_command , top_anime_command , browse_command
from Handlers import handle_message , handle_buttons
from Plugins.Anime import start_check_updates
from telegram.constants import ChatAction
import subprocess
import os 
import time
import asyncio
from warnings import filterwarnings

filterwarnings(action='ignore',category=DeprecationWarning)


async def main(TOKEN):
    bot = Bot(TOKEN)
#    await bot.log_out()
#    await bot.delete_webhook()
    task = await start_check_updates()
    await restart_per_2_hours(bot,task)

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pid = os.getpid()
    await update.message.reply_text(f'BaseUrl: {context.bot.base_url} \nPID: {pid} ')


async def ping(update: Update, context):
    start = time.time()
    m = await update.message.reply_text('.')
    ping = time.time() - start
    await m.edit_text(f'Ping: {ping * 1000:.2f} ms') 



def is_api_running():
    try:
        result = subprocess.run(
            ["pgrep", "-f", "telegram-bot-api"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(result)
        return result.stdout.strip() != b"" 
    except Exception as e:
        print(f"Error checking if API is running: {e}")
        return False


def start_local_api():
    command = ["./telegram-bot-api/bin/telegram-bot-api", "--local", "--api-id=17426055", "--api-hash=7ed73b9d1b9e0d58dcf734d37290f57c"]
    process = subprocess.Popen(command)
    print("starting Local server ...")
    return process

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(TOKEN))
    if not is_api_running():
        api_process = start_local_api()
        time.sleep(5) 

    app = ApplicationBuilder().token(TOKEN).base_url('http://localhost:8081/bot').build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('cast', broadcast_command))
    app.add_handler(CommandHandler('post', post_command))
    app.add_handler(CommandHandler('anime', anime_command))
    app.add_handler(CommandHandler('gogosearch', anime_command))
    app.add_handler(CommandHandler('airing', airing_command))
    app.add_handler(CommandHandler('schedule', schedule_command))
    app.add_handler(CommandHandler('feedback', feedback_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('character', character_command))
    app.add_handler(CommandHandler('manga', manga_command))
    app.add_handler(CommandHandler('top', top_anime_command))
    app.add_handler(CommandHandler('browse', browse_command))
    app.add_handler(CommandHandler('latest', latest_command))
    app.add_handler(CommandHandler('popular', popular_command))
    app.add_handler(CommandHandler('check', check))
    app.add_handler(CommandHandler('ping', ping))

    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))


    try:
        print("Bot is running...")
        app.run_polling(poll_interval=0.1)
    except KeyboardInterrupt:
        print("Bot stopped.")
    finally:
        pass
        api_process.terminate()


