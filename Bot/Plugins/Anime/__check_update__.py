from telegram import Bot
from Easy_Bot import Inline_reply_markup
import asyncio
from Config import TOKEN , UPDATE_CHANNEL , LOG_CHAT , ERROR_TEXT , START_IMG

from Databae import get_temp , add_note , edit_note 
from Plugins.Web_search import GoGoAnime , get_image_for_post ,  get_post_from_gogo , anilist , anilist_id_2_gogo_id , get_scheduled , get_estimated_time_of_arrival

async def start_check_updates():
    bot = Bot(TOKEN)
    asyncio.create_task(start_check_schedule(bot))
    return asyncio.create_task(check_updates(bot))
    
async def check_updates(bot:Bot):
    while True:
        try:
            last_update =  await get_temp("gogo")
            if last_update:
                last_update_id = last_update["text"]
            else:
                last_update_id = 'testDate'
                add_note("gogo",last_update_id)
                
            new_id = GoGoAnime().get_anime_new_update_id().replace("/","")
            
            if new_id and str(new_id) != str(last_update_id):
                new_id = new_id.replace("/","")
                status = edit_note("gogo",new_id)
                await send_update_for_channel(bot,new_id)
    
        except Exception as e:
            text = ERROR_TEXT.format(f"Getting update : {str(e)}",None,None,(await bot.get_me()).username) 
            await bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')
        await asyncio.sleep(60)
            
async def send_update_for_channel(bot: Bot, new_id: str):
    bot_ = await bot.get_me()
    try:
        image = get_image_for_post(new_id.split('-episode')[0].replace("-"," "))
        id = int(image.split('/')[-1])
        gogo_id = new_id.split('-episode')[0]
        episode = int(new_id.split('-episode-')[-1])
        try:
            data = get_post_from_gogo(gogo_id)
            if data == None:return
            title = data.title
            type = data.type
            released = data.release
            status = data.status
            episodes = data.total_episodes
            genres = data.genres
            description = anilist().get_description(id)
        except Exception as e:
            print(e)
            return
        text = f"""
<b><i>☘ Tιтle : {title}</i></b>
<b><i>🎭 Tʏᴘᴇ ➜  {type}</i></b>
<b><i>🧩 Rᴇʟᴇᴀꜱᴇ ➜ {released}</i></b>
<b><i>✨️ Sᴛᴀᴛᴜꜱ ➜  {status}</i></b>
<b><i>🌼 Eᴘɪꜱᴏᴅᴇꜱ ➜ {episodes}</i></b>
<b><i>📖 Gᴇɴʀᴇꜱ ➜ {genres}</i></b>
    """
        description = f"\n<b><i>📚 Description : <blockquote>{description}</blockquote></i></b>"
        trailer = anilist().get_trailer(id)
        keyboard = {}
        if trailer:
            keyboard[1] = {"▫️ Trailer ▫️" : trailer, "▫️ More Info ▫️" : f"https://t.me/{bot_.username}?start=view-{id}"}
        else:
            keyboard[1] = {"▫️ More Info ▫️" : f"https://t.me/{bot_.username}?start=view-{id}"}
        keyboard[2] = {f"▫️ Episode {new_id.split('-episode-')[-1]} ▫️" : f"https://t.me/{bot_.username}?start=New-{id}_{episode}"}
        
        reply_markup = Inline_reply_markup(keyboard)
        try:await bot.send_photo(photo=image,chat_id=UPDATE_CHANNEL,caption=text + description,parse_mode='HTML',reply_markup=reply_markup)
        except:await bot.send_photo(photo=image,chat_id=UPDATE_CHANNEL,caption=text,parse_mode='HTML',reply_markup=reply_markup)
        
    except Exception as e:
        
        text = ERROR_TEXT.format(f"Sending updare post : {str(e)}",None,None,bot_.username) 
        await bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')


async def start_check_schedule(bot):
    time = get_estimated_time_of_arrival()
    await asyncio.sleep(time)
    await send_schedule_to_channel(bot)
    
async def send_schedule_to_channel(bot):
    tet , schedules = get_scheduled()
    text = f'<blockquote>🧩   <code>T o d a y  A i r i n g</code>   🧩</blockquote>\n\n'
    for item in schedules:
        text += f"⭕️  <code>{item}</code>\n\n"

    msg = await bot.send_message(chat_id=UPDATE_CHANNEL,text=text,parse_mode='HTML')
    await bot.pin_chat_message(chat_id=UPDATE_CHANNEL,message_id=msg.message_id,disable_notification=False)


