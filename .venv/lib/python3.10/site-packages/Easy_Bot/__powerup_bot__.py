from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application , ContextTypes , CallbackContext
from telegram.ext import CommandHandler as commnders
from telegram.ext import MessageHandler as Messengers
from telegram.ext import CallbackQueryHandler as Callbacker
from telegram.ext import filters as Filters

import os 

LOGO = """........................................
.#####...####...##...##...####...#####..
.##..##.##..##..###.###..##..##..##..##.
.#####..######..##.#.##..##..##..##..##.
.##.....##..##..##...##..##..##..##..##.
.##.....##..##..##...##...####...#####..
........................................    
   ├ ᴄᴏᴘʏʀɪɢʜᴛ © 𝟸𝟶𝟸𝟹-𝟸𝟶𝟸𝟺 ᴘᴀᴍᴏᴅ ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ. ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
   ├ ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ  ɢᴘʟ-𝟹.𝟶 ʟɪᴄᴇɴsᴇ.
   └ ʏᴏᴜ ᴍᴀʏ ɴᴏᴛ ᴜsᴇ ᴛʜɪs ғɪʟᴇ ᴇxᴄᴇᴘᴛ ɪɴ ᴄᴏᴍᴘʟɪᴀɴᴄᴇ ᴡɪᴛʜ ᴛʜᴇ ʟɪᴄᴇɴsᴇ.
"""


def _powerup_bot_(TOKEN: str , Handlers: dict , Webhook_url: str ,PORT: str) -> None:
    print(LOGO)
    app = Application.builder().token(TOKEN).build()

    for handler , command_and_function in Handlers.items():
        handler_list = [] 
        for command , function in dict(command_and_function).items():
            if handler == "Error":
                app.add_error_handler(function)
            elif command != None:
                app.add_handler(handler(command , function))
            else:    
                app.add_handler(handler(function))
            handler_list.append(handler)

    
    print("Bot v5 Started !")
    if Webhook_url != None:
        app.run_webhook(port=PORT,listen="0.0.0.0",webhook_url=Webhook_url)
    else:
        app.run_polling()

def Inline_reply_markup(keyboard: dict) -> InlineKeyboardMarkup:
    """Create a Reply Markup easy 

    Args:

        keyboard (dict): keyboard
            A dict to create keyboard with line by line 

            

        Example:
                keyboard = {
                    1 : {
                        "text1" : "https://www.youtube.com/watch?v=Qk9FQjYpVXk",
                        "text2" : "https://www.youtube.com/watch?v=Qk9FQjYpVas"

                    },
                    2 : {
                        "button" : "data"
                    },
                    3 : {
                        "button" : "inline:query"
                    },
            }
    """
    Inline_Keyboard = []
    for _ , data in keyboard.items():
        button_line = []
        for text , bdata in dict(data).items():
            if str(bdata).startswith("http"):
                button_line.append(InlineKeyboardButton(text,url=bdata))
            elif str(bdata).startswith("inline"):
                bdata = bdata.split(":")[1]
                button_line.append(InlineKeyboardButton(text,switch_inline_query_current_chat=bdata))
                
            else:
                button_line.append(InlineKeyboardButton(text,callback_data=bdata))
        
        Inline_Keyboard.append(button_line)
    return InlineKeyboardMarkup(Inline_Keyboard)


