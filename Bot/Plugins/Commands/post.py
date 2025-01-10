from telegram import Update ,Bot , InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes 
from Config import SUDO_USERS , UPDATE_CHANNEL
import asyncio

__command__ = 'post'
__description__ = 'use this cmd to post a message to channel'
__category__ = 'sudo'

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(post_command_task(update,context))

async def post_command_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in SUDO_USERS or not update.effective_message.reply_to_message:
        return
    try:
        message = update.effective_message.reply_to_message
        past_keyboard = message.reply_markup.inline_keyboard
        Anilist_id = str(past_keyboard[-1][0].callback_data).split(':')[2]
        trailer = str(past_keyboard[0][0].url)
        bot_ = await context.bot.get_me()
        keyboard = [
            [InlineKeyboardButton("Trailer",url=trailer)],
            [InlineKeyboardButton("View Info",url=f"https://t.me/{bot_.username}?start=view-{Anilist_id}")]
        ] 
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = await context.bot.copy_message(from_chat_id=update.effective_chat.id,chat_id=UPDATE_CHANNEL,message_id=message.message_id,reply_markup=reply_markup)
        await context.bot.pin_chat_message(chat_id=UPDATE_CHANNEL,message_id=msg.message_id,disable_notification=False)
    except:pass
