from telegram import Update 
from telegram.ext import ContextTypes , CallbackContext
from Easy_Bot import Inline_reply_markup
from Config import START_TEXT , START_IMG , START_TIME , LOG_CHAT , NEW_USER_TEXT
from _help_functions_ import mention_html
from Databae import is_served_user , add_served_user , count_users
from Plugins.Anime import send_update_post , send_post , send_descritpion
import asyncio
import time

__command__ = 'start'
__description__ = 'use this cmd to start bot in group or pm'
__category__ = 'basic'


def start_keyboard(bot_username,user_id):
    return {
        1 : {"✨ Sᴛᴀᴛᴜꜱ" : f"S54FT:{user_id}","🎭 Aʙᴏᴜᴛ" : f"Q3N8D:{user_id}"},
    }

async def start_command(update: Update , context: ContextTypes.DEFAULT_TYPE) -> None:
    asyncio.create_task(start_command_task(update, context))
    
async def start_command_task(update: Update , context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    command = context.args[0] if context.args else ''
    if command != '':
        await context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.effective_message.message_id)
        command = command.split("-")
        if command[0] == 'New':
            asyncio.create_task(send_update_post(update,context,str(context.args[0]).replace("New-","")))
        elif command[0] == 'view':
            asyncio.create_task(send_post(update,context,int(str(context.args[0]).replace("view-",""))))
        elif command[0] == 'des':
            asyncio.create_task(send_descritpion(update,context,int(str(context.args[0]).replace("des-",""))))
        return
    saved = is_served_user(user_id)
    user_mention = await mention_html(user_id,False)
    bot_ = await context.bot.get_me()
    if not saved:
        add_served_user(user_id)
        await context.bot.send_message(text=NEW_USER_TEXT.format(user_mention,user_id,update.effective_user.username,bot_.username),chat_id=LOG_CHAT,parse_mode='HTML')
    bot_name = f"<a href='https://t.me/{bot_.username}'>{bot_.first_name}</a>"
    reply_markup = Inline_reply_markup(start_keyboard(bot_.username,user_id))
    msg = await update.message.reply_photo(photo=START_IMG,caption=START_TEXT.format(user_mention,bot_name),reply_markup=reply_markup,parse_mode='HTML')

async def X24DF(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
        return
    user_mention = await mention_html(user_id,False)
    bot_ = await context.bot.get_me()
    bot_name = f"<a href='https://t.me/{bot_.username}'>{bot_.first_name}</a>"
    reply_markup = Inline_reply_markup(start_keyboard(bot_.username,user_id))
    await query.edit_message_caption(caption=START_TEXT.format(user_mention,bot_name),reply_markup=reply_markup,parse_mode='HTML')


def format_time(elapsed):
    hours = int(elapsed / (60 * 60))
    minutes = int((elapsed % (60 * 60)) / 60)
    seconds = int(elapsed % 60)
    rval = ""
    if hours:
        rval += "{0}h ".format(hours)
    if elapsed > 60:
        rval += "{0}m ".format(minutes)
    rval += "{0}s ".format(seconds)
    return rval

async def X24DE(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
        return
    users = count_users()
    uptime = format_time(int(time.time()) - START_TIME)
    
    text= f""" 
<b>Users </b>: <code>{users}</code>    
<b>Uptime </b>: <code>{uptime}</code>
"""   
    keyboard = {
        1 : {"<< Back" : f"M7T5Z:{query.from_user.id}"}
    }
    reply_markup = Inline_reply_markup(keyboard)
    await query.edit_message_caption(caption=text,reply_markup=reply_markup,parse_mode='HTML')
