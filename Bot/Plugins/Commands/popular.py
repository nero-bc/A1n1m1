from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import ContextTypes , CallbackContext 
from Easy_Bot import Inline_reply_markup
from Config import  LOG_CHAT , ERROR_TEXT , POPULAR_ANIME_TEXT
from _help_functions_ import mention_html
from Plugins.Web_search import GoGoAnime
import asyncio

__command__ = 'popular'
__description__ = 'Use this cmd to get popular anime'
__category__ = 'anilist'

async def popular_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(popular_command_task(update,context))

async def popular_command_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.message.reply_text('proccessing...')
    anime = GoGoAnime().get_popular_anime()
    keyboard = []
    for item in anime:
        keyboard.append([InlineKeyboardButton(item.title,callback_data=f"FP:S:{item.id}:{update.effective_user.id}")])
    await m.edit_text(text=POPULAR_ANIME_TEXT,reply_markup=InlineKeyboardMarkup(keyboard),parse_mode='HTML')
