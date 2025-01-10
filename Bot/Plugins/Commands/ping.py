from telegram import Update 
from telegram.ext import ContextTypes 
from datetime import datetime

__command__ = 'ping'
__description__ = 'use this cmd to check if bot is online'
__category__ = 'basic'

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    st = datetime.now()
    x = await update.message.reply_text("...")
    et = datetime.now()
    pt = (et-st).microseconds / 1000
    await x.edit_text(text=f"<i>Pong !!</i> \n<code>{pt} ms</code> ",parse_mode='HTML')
    
