from telegram import Update 
from telegram.ext import ContextTypes
from Config import UPDATE_CHANNEL

async def check_is_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    member = (await context.bot.get_chat_member(UPDATE_CHANNEL,user_id)).status
    if member in ('kicked' , 'left' , 'restricted') :
        return False
    else:
      return True
    
