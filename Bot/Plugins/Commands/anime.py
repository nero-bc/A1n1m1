from telegram import Update , ForceReply
from telegram.ext import ContextTypes 
from Easy_Bot import Inline_reply_markup
from Config import FORCE_SUB_TEXT , UPDATE_CHANNEL_INVITE_LINK , LOG_CHAT , ERROR_TEXT
from _help_functions_ import check_is_member , mention_html
from Plugins.Web_search import GoGoAnime
import asyncio

__command__ = 'search'
__description__ = 'Use this cmd to get anime'
__category__ = 'anilist'

async def anime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(anime_command_task(update,context))

async def anime_message_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = (update.effective_message.text)
    asyncio.create_task(send_reply_text(update,context,query))

async def anime_command_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join((update.effective_message.text).split(' ')[1:])
    if query == '':return await update.message.reply_text(text="Please respond with the anime name you want to search for.",parse_mode='HTML',reply_markup=ForceReply())
    asyncio.create_task(send_reply_text(update,context,query))

async def send_reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE,query):
    mg = await update.message.reply_text(text="<code>Processing....</code>",parse_mode='HTML')
    try:
        results = GoGoAnime().get_search_results(query,1)
        if results != None and results != {}:
            try:results = sorted(results, key=lambda x: x.title)
            except Exception as e:print(e)
            x = 0  
            keyboard = {}
            for result in results:
                title = result.title
                id = result.id
                x = x + 1
                keyboard[str(x)] = {title : f"FP:S:{id}:{update.effective_user.id}"}       
            if x >= 20:
                keyboard[str(x+1)] = {"Next >>": f"next:{update.effective_user.id}"}
            text = f"<b>Search results for </b><code>{query}</code>"
            reply_markup = Inline_reply_markup(keyboard)
        if keyboard == {}:
            text = "<code>No results found</code>"
            reply_markup = None
    
        await mg.edit_text(text=text,parse_mode='HTML',reply_markup=reply_markup)
    except TimeoutError:
        pass
    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(update.effective_user.id,False)
        text = ERROR_TEXT.format(f"Getting Anime : {str(e)}",user,update.effective_user.id,bot_.username) 
        await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')
