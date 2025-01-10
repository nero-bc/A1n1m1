from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import CallbackContext
import asyncio


async def G5V1K(update: Update, context: CallbackContext):
    asyncio.create_task(change_to_about_task(update,context))
async def change_to_about_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
        return
    bot_ = await context.bot.get_me()
    bot_name = f"<a href='https://t.me/{bot_.username}'>{bot_.first_name}</a>"
    bot_username = f"<a href='https://t.me/{bot_.username}'>@{bot_.username}</a>"
    caption = f""" 
ᴀʙᴏᴜᴛ ᴍᴇ
┬───────────────────────
├ ɴᴀᴍᴇ : {bot_name}
│ 
├ ᴜsᴇʀɴᴀᴍᴇ : {bot_username}
│ 
├ ᴡʀɪᴛᴛᴇɴ ɪɴ : ᴘʏᴛʜᴏɴ 𝟹.𝟷𝟷
│ 
├ ʟɪʙʀᴀʀɪᴇs : 
│      └ ᴘʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ
│  
├ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/About_Pamod'>ᴘᴀᴍᴏᴅ ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ</a>      
│ 
└ ᴠᴇʀsɪᴏɴ : ᴠ1
"""
    keyboard = [[InlineKeyboardButton(" Back ",callback_data=f"M7T5Z:{user_id}")]]
    await query.edit_message_caption(caption=caption,parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))


async def A9X2F(update: Update, context: CallbackContext):
    asyncio.create_task(change_to_about_dev_task(update,context))
async def change_to_about_dev_task(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
        return
    bot_ = await context.bot.get_me()
    bot_name = f"<a href='https://t.me/{bot_.username}'>{bot_.first_name}</a>"
    bot_username = f"<a href='https://t.me/{bot_.username}'>@{bot_.username}</a>"
    caption = f""" 
ᴀʙᴏᴜᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ
┬───────────────────────
├ ɴᴀᴍᴇ : ᴘᴀᴍᴏᴅ ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ
│   
├ ᴜsᴇʀɴᴀᴍᴇ : @pamod_madubashana
│
└ ᴘʀᴏғɪʟᴇs :
          ├ ᴄᴏᴅᴇᴘᴇɴ : <a href='https://codepen.io/Pamod-Madubashana'>ᴘᴀᴍᴏᴅ-ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ</a>
          ├ ɢɪᴛʜᴜʙ : <a href='https://github.com/CP2003'>ᴘᴀᴍᴏᴅ_ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ</a>
          └ ᴄss ʙᴀᴛᴛʟᴇ : <a href='https://cssbattle.dev/player/pamod_madubashana'>ᴘᴀᴍᴏᴅ_ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ</a>
"""
    keyboard = [[InlineKeyboardButton(" Back ",callback_data=f"M7T5Z:{user_id}")]]
    await query.edit_message_caption(caption=caption,parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))