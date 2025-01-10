from telegram import Update , InputMedia , ForceReply
from telegram.ext import ContextTypes , CallbackContext 
from Easy_Bot import Inline_reply_markup
from Config import  LOG_CHAT , ERROR_TEXT
from _help_functions_ import mention_html
from Plugins.Web_search import anilist
import asyncio

__command__ = 'airing'
__description__ = 'Use this cmd to get info on airing status of anime'
__category__ = 'anilist'

async def airing_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(airing_command_task(update,context))

async def airing_message_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = (update.effective_message.text)
    asyncio.create_task(send_reply_task(update,context,query))
    
async def airing_command_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = (update.effective_message.text)
    query = ' '.join(query.split(' ')[1:])
    if query == '':return await update.message.reply_text(text="Please give a query to search about airing",parse_mode='HTML',reply_markup=ForceReply())
    asyncio.create_task(send_reply_task(update,context,query))

async def send_reply_task(update: Update, context: ContextTypes.DEFAULT_TYPE,query):
    mg = await update.message.reply_text(text="<code>Processing....</code>",parse_mode='HTML')
    result = anilist().get_airing(query,1)
    if result:
        text = f"""
<b>{result.title}</b>

<b>ID:</b> <code>{result.anilist_id}</code>
<b>Status:</b> <code>{result.status}</code>
"""
        if result.status == "RELEASING":
            text += f"\n<b>Next Airing Episode:</b>\n<code>{result.episode}{result.hat_notation} in {result.airing}</code>"
        keyboard = {
          1 : {"More Info" : result.url},
          2 : {"Next" : f"NXAIR:N:1:{update.effective_user.id}"}
        }
        reply_markup = Inline_reply_markup(keyboard)
        await mg.delete()
        await update.effective_message.reply_photo(photo=result.image,caption=text,parse_mode='HTML',quote=True,reply_markup=reply_markup)
    else:await mg.edit_text(text="<code>No results found</code>",parse_mode='HTML')
        

async def TG654(update: Update, context: CallbackContext):
    query = update.callback_query
    data = (query.data).split(':')
    user_id = int(data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return

    change = data[1]
    page = int(data[2])
    query = (' '.join(str(query.message.reply_to_message.text).split(' ')[1:])) if query.message.reply_to_message.text.startswith('/') else query.message.reply_to_message.text
    if change == 'N':
        page = page + 1
    else:
        page = page - 1

    result = anilist().get_airing(term,page)
    if result == None:return await query.answer("No more results available !",show_alert=True)

    if page == 1 and change == 'P':
        keyboard = {
            1 : {"More Info" : result.url},
            2 : {"Next" : f"NXAIR:N:{page}:{update.effective_user.id}"}
        }
    else:
        keyboard = {
            1 : {"More Info" : result.url},
            2 : {"Prev" : f"NXAIR:P:{page}:{update.effective_user.id}","Next" : f"NXAIR:N:{page}:{update.effective_user.id}"}
        }
    if result:
        text = f"""
<b>{result.title}</b>

<b>ID:</b> <code>{result.anilist_id}</code>
<b>Status:</b> <code>{result.status}</code>
"""
        if result.status == "RELEASING":
            text += f"\n<b>Next Airing Episode:</b>\n<code>{result.episode}{result.hat_notation} in {result.airing}</code>"
        reply_markup = Inline_reply_markup(keyboard)
        image = InputMedia(media_type='photo', media=result.image,caption=text,parse_mode='HTML')
        await query.edit_message_media(media=image,reply_markup=reply_markup)
        
