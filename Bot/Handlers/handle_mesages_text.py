from telegram import Update 
from Plugins.Anime import handle_anime
from telegram.ext import ContextTypes
from Config import MAIN_GROUP , TOKEN
from Plugins.Commands import airing_message_task , anime_message_task , character_message_task , manga_message_task
import asyncio

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat = update.effective_chat
    if message.text.startswith('/'):return
    if chat.id == MAIN_GROUP:
        asyncio.create_task(handle_anime(update, context))
    try:    
        if update.effective_message.reply_to_message.from_user.id == int(str(TOKEN).split(':')[0]):
            text = update.effective_message.reply_to_message.text
            
            if text.endswith('airing'):asyncio.create_task(airing_message_task(update, context))
            
            elif text == "Please respond with the anime name you want to search for.":asyncio.create_task(anime_message_task(update, context))
    
            elif text.endswith('characters'):asyncio.create_task(character_message_task(update, context))    

            elif text.endswith('manga'):asyncio.create_task(manga_message_task(update, context))    
                
    except:pass
            
            
    
