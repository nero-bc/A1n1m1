from Config import TOKEN, WEBHOOK_URL, PORT
from Easy_Bot import _powerup_bot_, commnders, Messengers, Callbacker, Filters
from Plugins.Commands import (
    start_command, latest_command, popular_command, broadcast_command, restart_per_2_hours,
    post_command, anime_command, airing_command, schedule_command, feedback_command,
    help_command, ping_command, character_command, manga_command, top_anime_command,
    browse_command
)
from Handlers import handle_message, handle_buttons
from Plugins.Anime import start_check_updates
from telegram import Bot
import asyncio
import os
from warnings import filterwarnings

filterwarnings(action='ignore', category=DeprecationWarning)

async def main(WEBHOOK_URL, TOKEN):
    bot = Bot(TOKEN)
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL + "/" + TOKEN)
    task = await start_check_updates()
    await restart_per_2_hours(bot, task)

Handlers = {
    commnders: {
        'start': start_command,
        'cast': broadcast_command,
        'post': post_command,
        'anime': anime_command,
        'gogosearch': anime_command,
        'airing': airing_command,
        'schedule': schedule_command,
        'feedback': feedback_command,
        'help': help_command,
        'ping': ping_command,
        'character': character_command,
        'manga': manga_command,
        'top': top_anime_command,
        'browse': browse_command,
        'latest': latest_command,
        'popular': popular_command,
    },
    Messengers: {
        Filters.TEXT: handle_message,
    },
    Callbacker: {
        None: handle_buttons
    }
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(WEBHOOK_URL, TOKEN))
    _powerup_bot_(
        TOKEN=TOKEN,
        Handlers=Handlers,
        Webhook_url=WEBHOOK_URL,
        PORT=PORT
    )
