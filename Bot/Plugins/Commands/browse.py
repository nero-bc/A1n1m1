from telegram import Update , InputMedia , ForceReply
from telegram.ext import ContextTypes , CallbackContext 
from Easy_Bot import Inline_reply_markup
from Config import  LOG_CHAT , ERROR_TEXT
from _help_functions_ import mention_html
from Plugins.Web_search import anilist
import asyncio

__command__ = 'browse'
__description__ = 'Use this cmd to get trending or popularity anime'
__category__ = 'anilist'

async def browse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(send_reply_task(update,context))

async def send_reply_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mg = await update.message.reply_text(text="<code>Processing....</code>",parse_mode='HTML')
    result = anilist().browse("trending")
    text = f"<b>{result.title}</b>\n\n"
    if result:
        keyboard = {
            1 : {"⚬ Trending ⚬" : f"BRX23:N:{update.effective_user.id}" , "Popular" : f"BRX23:p:{update.effective_user.id}" , "Upcoming" : f"BRX23:u:{update.effective_user.id}"}
        }
        reply_markup = Inline_reply_markup(keyboard)
        text += "".join([f"⚬ <code>{anime}</code>\n" for anime in result.anime])
        await mg.edit_text(text=text,parse_mode='HTML',reply_markup=reply_markup)
    else:await mg.edit_text(text="<code>No results found</code>",parse_mode='HTML')


async def TH154(update: Update, context: CallbackContext):
    query = update.callback_query
    data = (query.data).split(':')
    user_id = int(data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
            
    tkeyboad = {
        1 : {"⚬ Trending ⚬" : f"BRX23:N:{update.effective_user.id}" , "Popular" : f"BRX23:p:{update.effective_user.id}", "Upcoming" : f"BRX23:u:{update.effective_user.id}"}
        }
    pkeyboard = {
        1 : {"Trending" : f"BRX23:t:{update.effective_user.id}" , "⚬ Popular ⚬" : f"BRX23:N:{update.effective_user.id}", "Upcoming" : f"BRX23:u:{update.effective_user.id}"}
        }
    ukeyboard = {
        1 : {"Trending" : f"BRX23:t:{update.effective_user.id}" , "Popular" : f"BRX23:p:{update.effective_user.id}", "⚬ Upcoming ⚬" : f"BRX23:N:{update.effective_user.id}"}
        }
        
    change = data[1]
    if change == "N":return await query.answer()
        
    squery = "trending" if change == 't' else "popularity" if change == 'p' else "upcoming"
    keyboard = tkeyboad if change == 't' else pkeyboard if change == 'p' else ukeyboard
    result = anilist().browse(squery)
    
    if result == None:return await query.answer("No more results available !",show_alert=True)
    text = f"<b>{result.title}</b>\n\n"
    text += "".join([f"⚬ <code>{anime}</code>\n" for anime in result.anime])
    reply_markup = Inline_reply_markup(keyboard)
    await query.edit_message_text(text=text,parse_mode='HTML',reply_markup=reply_markup)
