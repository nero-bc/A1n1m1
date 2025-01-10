from telegram import Update , InputFile , InputMedia , ForceReply
from telegram.ext import ContextTypes , CallbackContext
from Easy_Bot import Inline_reply_markup
from Config import  LOG_CHAT , ERROR_TEXT
from _help_functions_ import mention_html
from Plugins.Web_search import anilist
import asyncio

__command__ = 'manga'
__description__ = 'Use this cmd to get info of manga'
__category__ = 'anilist'

async def manga_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(manga_command_task(update,context))

async def manga_message_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = (update.effective_message.text)
    asyncio.create_task(send_reply_task(update,context,query))

async def manga_command_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join((update.effective_message.text).split(' ')[1:])
    if query == '':return await update.message.reply_text(text="Please give a query to search about manga",parse_mode='HTML',reply_markup=ForceReply())
    asyncio.create_task(send_reply_task(update,context,query))

async def send_reply_task(update: Update , context: ContextTypes.DEFAULT_TYPE, query):
    mg = await update.message.reply_text(text="<code>Processing....</code>",parse_mode='HTML')
    result = anilist().get_manga(query,1)
    if result:
        text = f"""
<b><i>☘ Tιтle : {result.name}</i></b>

<b><i>🔖 ID ➜ {result.id}</i></b>

<b><i>🎭 Tʏᴘᴇ ➜ {result.format}</i></b>
<b><i>🧩 Sᴄᴏʀᴇ ➜ {result.score}</i></b>
<b><i>✨️ Sᴛᴀᴛᴜꜱ ➜ {result.status}</i></b>
<b><i>📕 Sᴏᴜʀᴄᴇ ➜ {result.source}</i></b>
<b><i>🔖 Vᴏʟᴜᴍᴇꜱ ➜ {result.volumes}</i></b>
<b><i>❄️ Cʜᴀᴘᴛᴇʀꜱ ➜ {result.chapters}</i></b>

"""
        description = f"<b><i>📚 Description :<blockquote>{result.description}</blockquote></i></b>"

        keyboard = {
          1 : {"More Info" : result.url},
        }
        reply_markup = Inline_reply_markup(keyboard)
        await mg.delete()
        try:await update.effective_message.reply_photo(photo=result.image,caption=text + description,parse_mode='HTML',quote=True,reply_markup=reply_markup)
        except:await update.effective_message.reply_photo(photo=result.image,caption=text,parse_mode='HTML',quote=True,reply_markup=reply_markup)
    else:await mg.edit_text(text="<code>No results found</code>",parse_mode='HTML')
        
