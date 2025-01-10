from telegram import Update , InputMedia , ForceReply
from telegram.ext import ContextTypes , CallbackContext 
from Easy_Bot import Inline_reply_markup
from Config import  LOG_CHAT , ERROR_TEXT
from _help_functions_ import mention_html
from Plugins.Web_search import anilist
import asyncio

__command__ = 'top'
__description__ = 'Use this cmd to get info on of top anime'
__category__ = 'anilist'

async def top_anime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(send_reply_task(update,context))

async def send_reply_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mg = await update.message.reply_text(text="<code>Processing....</code>",parse_mode='HTML')
    result = anilist().get_top_anime(1)
    text = "<b>Top animes:</b>\n\n"
    if result:
        keyboard = {
            1 : {"Next" : f"NEXT43:N:1:{update.effective_user.id}"}
        }
        reply_markup = Inline_reply_markup(keyboard)
        text += "".join([f"⚬ <code>{anime}</code>\n" for anime in result.anime])
        await mg.edit_text(text=text,parse_mode='HTML',reply_markup=reply_markup)
    else:await mg.edit_text(text="<code>No results found</code>",parse_mode='HTML')


async def TG154(update: Update, context: CallbackContext):
    query = update.callback_query
    data = (query.data).split(':')
    user_id = int(data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return

    change = data[1]
    page = int(data[2])
    if change == 'N':
        page = page + 1
    else:
        page = page - 1

    result = anilist().get_top_anime(page)
    if result == None:return await query.answer("No more results available !",show_alert=True)
    
    if page == 1 and change == 'P':
        keyboard = {
            1 : {"Next" : f"NEXT43:N:{page}:{update.effective_user.id}"}
        }
    else:
        if result.has_next_page:
            keyboard = {
                1 : {"Prev" : f"NEXT43:P:{page}:{update.effective_user.id}","Next" : f"NEXT43:N:{page}:{update.effective_user.id}"}
            }
        else:
            keyboard = {
                1 : {"Prev" : f"NEXT43:P:{page}:{update.effective_user.id}"}
            }
    reply_markup = Inline_reply_markup(keyboard)
    text = "<b>Top animes:</b>\n\n"
    text += "".join([f"⚬ <code>{anime}</code>\n" for anime in result.anime])
    await query.edit_message_text(text=text,parse_mode='HTML',reply_markup=reply_markup)

