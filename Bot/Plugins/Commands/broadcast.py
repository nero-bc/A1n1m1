from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import asyncio
import telegram.error
from Config import SUDO_USERS
from Databae import get_served_users , remove_served_user 

__command__ = 'cast'
__description__ = 'use this cmd to broadcast a message'
__category__ = 'sudo'

async def broadcast_command(update: Update, context: CallbackContext):
    asyncio.create_task(broadcast_command_task(update,context))

async def broadcast_command_task(update: Update, context: CallbackContext):
    successful_broadcasts = 0
    failed_broadcasts = 0
    blocked_broadcasts = 0
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message
    if user.id not in SUDO_USERS:
        return
    else:
        replied_message = update.message.reply_to_message
        if not replied_message:
            await message.reply_text("Please reply to a message")
            return
        await context.bot.delete_message(chat_id=chat.id, message_id=message.message_id)
        photo = replied_message.photo
        sticker = replied_message.sticker
        caption = replied_message.caption
        message_entity = replied_message.entities or replied_message.caption_entities
        message_text = replied_message.text
        reply_markup = replied_message.reply_markup
        users = get_served_users()
        msg = await context.bot.send_message(chat_id=user.id, text="sᴛᴀʀᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ...",parse_mode="HTML")
        for user_id in users:
            
            await asyncio.sleep(0.2)
            try:
                if photo:
                    await context.bot.send_photo(chat_id=user_id, photo=photo[0].file_id, caption=caption,caption_entities=message_entity, reply_markup=reply_markup)
                elif sticker:
                    await context.bot.send_sticker(chat_id=user_id, sticker=sticker.file_id)
                else:
                    await context.bot.send_message(chat_id=user_id, text=message_text,entities=message_entity, reply_markup=reply_markup)
                successful_broadcasts = successful_broadcasts + 1
            except telegram.error.BadRequest as e:
                failed_broadcasts = failed_broadcasts + 1
            except telegram.error.Forbidden as e:
                failed_broadcasts = failed_broadcasts + 1
                blocked_broadcasts = blocked_broadcasts + 1
                try:remove_served_user(int(user_id))
                except Exception as e:print("Remove user failed")
                  
            except telegram.error.RetryAfter as e:
                await asyncio.sleep(30)
                try:
                    if photo:
                        await context.bot.send_photo(chat_id=user_id, photo=photo[0].file_id, caption=caption,caption_entities=message_entity, reply_markup=reply_markup)
                    elif sticker:
                        await context.bot.send_sticker(chat_id=user_id, sticker=sticker.file_id)
                    else:
                        await context.bot.send_message(chat_id=user_id, text=message_text,entities=message_entity, reply_markup=reply_markup)
                    successful_broadcasts = successful_broadcasts + 1
                except:
                    failed_broadcasts = failed_broadcasts + 1
                    try:remove_served_user(int(user_id))
                    except Exception as e:print("Remove user failed")
                    pass
        
        text = f"""<b><i>ʙʀᴏᴀᴅᴄᴀsᴛ ғɪɴɪsʜᴇᴅ</i></b> 
 ┬────────────────────
 ├ <i>sᴜᴄᴄᴇssғᴜʟ : {successful_broadcasts} </i>
 ├ <i>ғᴀɪʟᴇᴅ : {failed_broadcasts} </i>
 └ <i>ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs : {blocked_broadcasts}</i>
"""
        try:
            await asyncio.sleep(20)
            await context.bot.edit_message_text(chat_id=user.id, message_id=msg.message_id,text=text,parse_mode="HTML")
        except:
            pass
                
