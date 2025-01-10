from telegram import Update , InputFile , InputMedia , ForceReply
from telegram.ext import ContextTypes , CallbackContext
from Easy_Bot import Inline_reply_markup
from Config import  LOG_CHAT , ERROR_TEXT
from _help_functions_ import mention_html
from Plugins.Web_search import anilist
import asyncio

__command__ = 'character'
__description__ = 'Use this cmd to get info on character'
__category__ = 'anilist'

async def character_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(character_command_task(update,context))

async def character_message_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = (update.effective_message.text)
    asyncio.create_task(send_reply_text(update,context,query))

async def character_command_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join((update.effective_message.text).split(' ')[1:])
    if query == '':return await update.message.reply_text(text="Please give a query to search about characters",parse_mode='HTML',reply_markup=ForceReply())
    asyncio.create_task(send_reply_text(update,context,query))

async def send_reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE,query):
    mg = await update.message.reply_text(text="<code>Processing....</code>",parse_mode='HTML')
    result = anilist().get_character(query,1)
    if result:
        text = f"""
<b>Name :</b> <code>{result.name}</code>
<b>ID :</b> <code>{result.id}</code>

"""
        if result.voice_actors:
            text += f"Voice Actors : {', '.join(actors for actors in result.voice_actors)}"
        text += f"\n\n<a href='{result.url}'>Visit website</a>"
        keyboard = {
            1 : {'Next' : f"NC12S:N:1:{update.effective_user.id}"}
        }
        await mg.delete()
        await update.message.reply_photo(photo=result.image,caption=text,parse_mode='HTML',reply_markup=Inline_reply_markup(keyboard),quote=True)
    else:await mg.edit_text(text="<code>No results found</code>",parse_mode='HTML')
        

async def TH654(update: Update, context: CallbackContext):
    query = update.callback_query
    data = (query.data).split(':')
    user_id = int(data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return

    change = data[1]
    page = int(data[2])
    term = (' '.join(str(query.message.reply_to_message.text).split(' ')[1:])) if query.message.reply_to_message.text.startswith('/') else query.message.reply_to_message.text
    if change == 'N':
        page = page + 1
    else:
        page = page - 1

    result = anilist().get_character(term,page)
    if result == None:return await query.answer("No more results available !",show_alert=True)
    if page == 1 and change == 'P':
        keyboard = {
            1 : {"Next" : f"NC12S:N:{page}:{update.effective_user.id}"}
        }
    else:
        keyboard = {
            1 : {"Prev" : f"NC12S:P:{page}:{update.effective_user.id}","Next" : f"NC12S:N:{page}:{update.effective_user.id}"}
        }
    if result:
        text = f"""
<b>Name :</b> <code>{result.name}</code>
<b>ID :</b> <code>{result.id}</code>

"""
        if result.voice_actors:
            text += f"Voice Actors : {', '.join(actors for actors in result.voice_actors)}"
        text += f"\n\n<a href='{result.url}'>Visit website</a>"
        reply_markup = Inline_reply_markup(keyboard)
        image = InputMedia(media_type='photo', media=result.image,caption=text,parse_mode='HTML')
        await query.edit_message_media(media=image,reply_markup=reply_markup)
