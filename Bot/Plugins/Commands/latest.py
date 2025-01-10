from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import ContextTypes , CallbackContext 
from Easy_Bot import Inline_reply_markup
from Config import  LOG_CHAT , ERROR_TEXT , LATEST_ANIME_TEXT
from _help_functions_ import mention_html
from Plugins.Web_search import GoGoAnime
from Plugins.Anime import send_update_post
from typing import Union
import asyncio

__command__ = 'latest'
__description__ = 'Use this cmd to get leatest anime episodes'
__category__ = 'anilist'

async def latest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(latest_command_task(update,context))

async def latest_command_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.message.reply_text('proccessing...')
    anime = GoGoAnime().get_new_release_anime()
    keyboard = []
    for item in anime:
        keyboard.append([InlineKeyboardButton(f"{item.title}",callback_data=f"SLPX16:{item.id}_{item.episode}:{update.effective_user.id}")])

    await m.edit_text(text='Here is the results',reply_markup=InlineKeyboardMarkup(keyboard))

async def SLPX32(update: Update, context: Union[CallbackContext, ContextTypes.DEFAULT_TYPE]):
    query = update.callback_query
    data = query.data.split(':')
    edata = data[-2]
    await send_update_post(update,context,edata)
