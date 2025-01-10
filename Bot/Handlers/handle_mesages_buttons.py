from telegram import Update 
from telegram.ext import CallbackContext
from .functions import *
import asyncio

QUERY_DICT = {
    "Q3N8D" : G5V1K,
    "J4P6L" : A9X2F,
    "M7T5Z" : X24DF,
    "FP" : FG547X,
    "VG" : FG527X,
    "X3DS2" : FG465X,
    "TR265D" : GF265X,
    "FRT34" : GF5615X,
    "S54FT" : X24DE,
    "CH56X" : FG3XAD,
    "LS45X" : HS53C,
    "NXAIR" : TG654,
    "NC12S" :TH654,
    "SCHD2X" : FYC245,
    "NEXT43" : TG154,
    "BRX23" : TH154,
    "SLPX16" : SLPX32,
}

async def handle_buttons(update: Update , context: CallbackContext):
    query = update.callback_query
    button = query.data
    if ':' in str(button):
        func = button.split(":")[0]
        function = QUERY_DICT.get(func)
        if func == 'NO':
            await query.answer()
        if func ==  "ERX45":
            await query.answer("unknown error occurred",show_alert=True)
        elif function:
            asyncio.create_task(function(update,context))
        else:
            await query.answer("This Feature is not availabel yet !",show_alert=True)

        
