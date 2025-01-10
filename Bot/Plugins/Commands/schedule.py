from telegram import Update 
from datetime import datetime, timedelta, timezone , date
from telegram.ext import ContextTypes , CallbackContext
from Plugins.Web_search import get_scheduled , day_
from Easy_Bot import Inline_reply_markup
import asyncio

__command__ = 'schedule'
__description__ = 'use this cmd to get today airing list'
__category__ = 'anilist'


async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(schedule_command_task(update,context))

async def schedule_command_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date , schedules = get_scheduled()
    today = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date().weekday()
    text = f'Scheduled animes for Today\n\n'
    for item in schedules:
        text += f"• <code>{item}</code>\n"
    
    if today == 0:keyboard = {1 : {"Tomorrow" : f"SCHD2X:{today + 1}:{update.effective_user.id}"}}
    elif today == 6:keyboard = {1 : {"Yesterday" : f"SCHD2X:{today - 1}:{update.effective_user.id}"}}
    else:keyboard = {1 : {"Yesterday" : f"SCHD2X:{today - 1}:{update.effective_user.id}" , }}
    await update.message.reply_text(text=text,parse_mode='HTML',reply_markup=Inline_reply_markup(keyboard))

async def FYC245(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
        return
    await query.answer("Processing....")
    date = int(data[1])
    title , schedules = get_scheduled(date)
    today = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date().weekday()
    text = title
    for item in schedules:
        text += f"• <code>{item}</code>\n"
    
    keyboard = {}
    if today == 0:keyboard[1] = {day_(today+1).capitalize() : f"SCHD2X:{today + 1}:{update.effective_user.id}"}
    elif today == 6:keyboard[1] = {day_(today-1).capitalize()  : f"SCHD2X:{today - 1}:{update.effective_user.id}"}
    else:keyboard[1] = {day_((date-1) , today).capitalize()  : f"SCHD2X:{date - 1}:{update.effective_user.id}",day_((date+1) , today).capitalize()  : f"SCHD2X:{date + 1}:{update.effective_user.id}"}
    
    await query.edit_message_text(text=text,parse_mode='HTML',reply_markup=Inline_reply_markup(keyboard))
    
