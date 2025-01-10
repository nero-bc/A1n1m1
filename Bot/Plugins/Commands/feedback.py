from telegram import Update
from telegram.ext import ContextTypes

__command__ = 'feedback'
__description__ = 'use this cmd to contact bot owner'
__category__ = 'basic'

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("For issues or queries please contact @Itzmecp")
