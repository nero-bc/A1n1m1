from telegram import Update , InlineKeyboardButton , InlineKeyboardMarkup , WebAppInfo
from telegram.ext import ContextTypes , CallbackContext
from Easy_Bot import Inline_reply_markup
from Config import TEMP_CHAT , FORCE_SUB_TEXT , UPDATE_CHANNEL_INVITE_LINK , LOG_CHAT , START_IMG , ERROR_TEXT
from _help_functions_ import check_is_member , mention_html
from _Classes import TempData
from Plugins.Web_search import (
    GoGoAnime,
    # get_image_for_post,
    get_episodes_from_gogo,
    # get_post_from_gogo,
    check_dub,
    # get_id,
    anilist_id_2_gogo_id,
    anilist_id_2_gogo_stream_download_id,
    anilist,
)

async def handle_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.effective_user or update.effective_user.id in [777000 ,1087968824 ,136817688]:return
        message = update.effective_message
        mg = await message.reply_text(text="<code>Processing....</code>",parse_mode='HTML')
        query = message.text.lower()
        results = GoGoAnime().get_search_results(query,1)
        if results != None and results != {}:
            try:results = sorted(results, key=lambda x: x.title)
            except Exception as e:print(e)
            x = 0  
            keyboard = {}
            for result in results:
                title = result.title
                id = result.id
                x = x + 1
                keyboard[str(x)] = {title : f"FP:S:{id}:{update.effective_user.id}"}       
            if x >= 20:
                keyboard[str(x+1)] = {"Next >>": f"next:{update.effective_user.id}"}
            text = f"<b>Search results for </b><code>{message.text}</code>"
            reply_markup = Inline_reply_markup(keyboard)
        if keyboard == {}:
            text = "<code>No results found</code>"
            reply_markup = None
    
        await mg.edit_text(text=text,parse_mode='HTML',reply_markup=reply_markup)
    except TimeoutError:
        pass
    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(update.effective_user.id,False)
        text = ERROR_TEXT.format(f"Getting Anime : {str(e)}",user,update.effective_user.id,bot_.username) 
        await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')


async def send_descritpion(update: Update , context: ContextTypes.DEFAULT_TYPE,id):
    Anime_data = anilist().get_anime(id)
    if Anime_data != None:
        description = Anime_data.description
        image = Anime_data.image
        title  = Anime_data.title
        text = f"""
    <b><i>📚 Description : <blockquote>{description}</blockquote></i></b>
    """
        try:await context.bot.send_photo(chat_id=update.effective_chat.id,photo=image,caption=text,parse_mode='HTML')
        except:
            msg = await context.bot.send_photo(chat_id=update.effective_chat.id,photo=image,parse_mode='HTML')
            await context.bot.send_message(chat_id=update.effective_chat.id,text=text,parse_mode='HTML')
            


async def FG547X(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_keyboard = (query.message.reply_markup.inline_keyboard)
    data = str(query.data).split(":")
    user_id =int(data[-1])
    id = data[2]
    task = data[1]
    _bot = (await context.bot.get_me()).username
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    await query.answer("processing...")

    def get_details(id):
        try:Anime_data = anilist().get_anime(id)
        except:Anime_data = anilist().get_manga(id)
        if Anime_data != None:
            title = getattr(Anime_data, 'title', '')
            if title == '':title = Anime_data.name
            image = Anime_data.image 
            mail_id =  getattr(Anime_data, 'mail_id', '')
            type = getattr(Anime_data, 'type', '') 
            if type =='':type = Anime_data.format
            score = getattr(Anime_data, 'score', '') 
            episodes = getattr(Anime_data, 'episodes', '') 
            duration = getattr(Anime_data, 'duration', '') 
            status = getattr(Anime_data, 'status', '') 
            genres = getattr(Anime_data, 'genres', '') 
            tags = getattr(Anime_data, 'tags', '') 
            description = getattr(Anime_data, 'description', '')
        else:return None 
        try:episodes = int(get_episodes_from_gogo(anilist_id_2_gogo_id(id)))
        except:return
        trialer = anilist().get_trailer(id)
        text = f"""
<b><i>☘️ Tιтle : {title}</i></b>

<b><i>🔖 ID | MAL ID ➜ {id} | {mail_id}</i></b>

<b><i>🎭 Tʏᴘᴇ ➜  {type}</i></b>
<b><i>🧩 Sᴄᴏʀᴇ ➜ {score}% </i></b>
<b><i>🔖 Eᴘɪꜱᴏᴅᴇꜱ ➜ {episodes}</i></b>
<b><i>⏰ Dᴜʀᴀᴛɪᴏɴ ➜ {duration} min/ep</i></b>
<b><i>✨️ Sᴛᴀᴛᴜꜱ ➜  {status}</i></b>
<b><i>📖 Gᴇɴʀᴇꜱ ➜ {genres}</i></b>
<b><i>🔮 Tᴀɢꜱ ➜ {tags}</i></b>
"""
        description = f"\n<b><i>📚 Description : <blockquote>{description}</blockquote></i></b>"
        
        
        return TempData(image=image,trialer=trialer,text=text,description=description)

    def genarate_mesage(id):
        data = get_details(id)
        if data == None:return None
        image = data.image
        trialer = data.trialer
        text = data.text
        description = data.description
        
        keyboard = []
        temp = []
        if trialer:
            temp.append(InlineKeyboardButton("Watch Trailer",url=trialer))
        temp.append(InlineKeyboardButton("Characters",callback_data=f"CH56X:1:{id}:{query.from_user.id}"))
        temp.append(InlineKeyboardButton("Series List",callback_data=f"LS45X:{id}:{query.from_user.id}"))
        keyboard.append(temp)
        keyboard.append([InlineKeyboardButton("Sub",callback_data=f"VG:S:{id}:{query.from_user.id}"),InlineKeyboardButton("Dub",callback_data=f"VG:D:{id}:{query.from_user.id}") ])
        return TempData(image=image,text=text,description=description,keyboard=keyboard)
    

    data = genarate_mesage(id)
    description2 = f"\n<b>📚 <a href='https://t.me/{_bot}/?start=des-{id}'>View Description :</a></b>"
    if data == None:return
    image = data.image
    text = data.text
    description = data.description
    keyboard = data.keyboard
    try:
        if task == "E":
            try:await query.edit_message_caption(caption=text + description,parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
            except:await query.edit_message_caption(caption=text + description2,parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            try:await context.bot.send_photo(chat_id=update.effective_chat.id,photo=image,caption=text + description,parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
            except:await context.bot.send_photo(chat_id=update.effective_chat.id,photo=image,caption=text + description2,parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(user_id,False)
        text = ERROR_TEXT.format(f"Send Post: {str(e)}",user,user_id,bot_.username)
        await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')


async def HS53C(update: Update, context: CallbackContext):
    query = update.callback_query
    data = str(query.data).split(':')
    print(data)
    id = int(data[1])
    user_id = int(data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    try:
        await query.answer("processing...")
        result = anilist().get_series_list(id)
        title = '<b>Series List:</b>\n\n'
        if result:
            keyboard = [[InlineKeyboardButton('<< Back ',callback_data=f"FP:E:{id}:{query.from_user.id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_caption(caption=title + result,parse_mode='HTML',reply_markup=reply_markup)
    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(user_id,False)
        text = ERROR_TEXT.format(f"view list series : {str(e)}",user,user_id,bot_.username)
        await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')

async def FG3XAD(update: Update, context: CallbackContext):
    query = update.callback_query
    data = str(query.data).split(':')
    print(data)
    page = int(data[1])
    if page == 0:
        return
    id = int(data[2])
    user_id = int(data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    
    try:
        await query.answer("processing...")
        print(id,page)
        result , page_info = anilist().get_characters(id,page)
        title = '<b>Characters List:</b>\n\n'
        keyboard = []
        if result:
            if page_info['hasNextPage'] and page == 1:
                keyboard.append([InlineKeyboardButton('Next',callback_data=f"CH56X:{page+1}:{id}:{query.from_user.id}")])

            elif page_info['hasNextPage']:
                keyboard.append([InlineKeyboardButton('Prev',callback_data=f"CH56X:{page-1}:{id}:{query.from_user.id}"),InlineKeyboardButton('Next',callback_data=f"CH56X:{page+1}:{id}:{query.from_user.id}")])
            elif page != 1:
                keyboard.append([InlineKeyboardButton('Prev',callback_data=f"CH56X:{page-1}:{id}:{query.from_user.id}")])
            keyboard.append([InlineKeyboardButton('<< Back ',callback_data=f"FP:E:{id}:{query.from_user.id}")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_caption(caption=title + result,parse_mode='HTML',reply_markup=reply_markup)
    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(user_id,False)
        text = ERROR_TEXT.format(f"view characters : {str(e)}",user,user_id,bot_.username)
        await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')



async def send_post(update: Update, context: ContextTypes.DEFAULT_TYPE,id):
    image = f"https://img.anili.st/media/{id}"
    msg = await context.bot.send_message(chat_id=update.effective_chat.id,text="<code>Processing...</code>",parse_mode='HTML')
    try:
        Anime_data = anilist().get_anime(id)
        if Anime_data != None:
            title  = Anime_data.title
            image = Anime_data.image
            mail_id =  Anime_data.mail_id
            type = Anime_data.type
            score = Anime_data.score
            episodes = Anime_data.episodes
            duration = Anime_data.duration
            status = Anime_data.status
            genres = Anime_data.genres
            tags = Anime_data.tags
            description = Anime_data.description
        else:return None 
        trialer = anilist().get_trailer(id)
        text = f"""
<b><i>☘️ Tιтle : {title}</i></b>

<b><i>🔖 ID | MAL ID ➜ {id} | {mail_id}</i></b>

<b><i>🎭 Tʏᴘᴇ ➜  {type}</i></b>
<b><i>🧩 Sᴄᴏʀᴇ ➜ {score}% </i></b>
<b><i>🔖 Eᴘɪꜱᴏᴅᴇꜱ ➜ {episodes}</i></b>
<b><i>⏰ Dᴜʀᴀᴛɪᴏɴ ➜ {duration} min/ep</i></b>
<b><i>✨️ Sᴛᴀᴛᴜꜱ ➜  {status}</i></b>
<b><i>📖 Gᴇɴʀᴇꜱ ➜ {genres}</i></b>
<b><i>🔮 Tᴀɢꜱ ➜ {tags}</i></b>
"""
        description = f"\n<b><i>📚 Description : <blockquote>{description}</blockquote></i></b>"
        
        keyboard = []
        temp = []
        if trialer:
            temp.append(InlineKeyboardButton("Watch Trailer",url=trialer))
        temp.append(InlineKeyboardButton("Characters",callback_data=f"CH56X:1:{id}:{update.effective_user.id}"))
        temp.append(InlineKeyboardButton("Series List",callback_data=f"LS45X:{id}:{update.effective_user.id}"))
        keyboard.append(temp)
        keyboard.append([InlineKeyboardButton("View Episodes",callback_data=f"VG:{id}:{update.effective_user.id}")])
        try:await context.bot.send_photo(photo=image,chat_id=update.effective_chat.id,caption=text + description,parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
        except:await context.bot.send_photo(photo=image,chat_id=update.effective_chat.id,caption=text,parse_mode='HTML',reply_markup=InlineKeyboardMarkup(keyboard))
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"Error: {str(e)}")

async def send_update_post(update: Update, context: CallbackContext,data):
    user_id = update.effective_user.id
    e_data = data.split("_")
    anilist_id = int(e_data[0])
    episode = int(e_data[-1])
    id = anilist_id_2_gogo_stream_download_id(anilist_id)
    title = id.title()

    image = f"https://img.anili.st/media/{anilist_id}"

    mg = await context.bot.send_message(chat_id=update.effective_chat.id,text="<code>Processing...</code>",parse_mode='HTML')
    try:
        stream_links = GoGoAnime().get_stram_links(id,episode)
        print('Stream Links :\n',stream_links,"\n====================================")
     
        download_links = GoGoAnime().get_download_links(id,episode)
        print('Download Links :\n',download_links,"\n====================================")
    
        watch_online ={}
        if stream_links != None:
            for link in stream_links:
                watch_online[link.quality] = link.link
 
        download_now = {}
        if download_links != None:
            for link in download_links:
                download_now[link.quality] = link.link
                
        keyboard = {
                1 : {"Watch Online" : "NO:NO"},
                2 : watch_online,
                3 : {"Download" : "NO:NO"},
                4 : download_now,
            }
        if stream_links == None:
            del keyboard[1]
    
        edited = False
        if len(watch_online) == 4:
            button_lin_1 = dict(list(watch_online.items())[:3])
            button_lin_2 = dict(list(watch_online.items())[3:])
            keyboard[2] = button_lin_1
            keyboard[3] = button_lin_2
            edited = True
    
    
        if len(download_now) == 4:
            button_lin_1 = dict(list(download_now.items())[:3])
            button_lin_2 = dict(list(download_now.items())[3:])
            if edited:
                keyboard[4] = {"Download": "NO:NO"}
                keyboard[5] = button_lin_1
                keyboard[6] = button_lin_2
            else:
                keyboard[4] = button_lin_1
                keyboard[5] = button_lin_2
        elif download_now == None:
            if not edited:
                del keyboard[3]
                
        elif edited:
            keyboard[4] = {"Download": "NO:NO"}
            keyboard[5] = dict(list(download_now.items()))
            
        reply_markup = Inline_reply_markup(keyboard)
        text = f"""<b>Download and Stream Links for episode </b><code>{episode}</code><b> of </b><code>{title}</code>"""
        if image != None:
            await mg.delete()
            await context.bot.send_photo(photo=image,chat_id=update.effective_chat.id,caption=text,parse_mode='HTML',reply_markup=reply_markup)
        else:
            await mg.edit_text(text=text,parse_mode='HTML',reply_markup=reply_markup)

    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(update.effective_user.id,False)
        text = ERROR_TEXT.format(f"send update episodes: {str(e)}",user,update.effective_user.id,bot_.username)
        await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')

async def FG527X(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        button = query.data
        data = button.split(":")
        user_id =int(data[-1])
        if update.effective_chat.type != 'private': 
            if user_id != query.from_user.id:
                await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
                return

        episodes= str(query.message.caption).split("\n")[6].split(" ")[-1]
        id = (data[2])
        is_dub = True if data[1] == 'D' else False
        if is_dub:
            try:episodes = int(get_episodes_from_gogo(anilist_id_2_gogo_id(id)+ "-dub" ))
            except:episodes = episodes
            dub_available = check_dub(anilist_id_2_gogo_id(id))
            if not dub_available:return await query.answer('Not FOund',show_alert=True)
        
        await query.answer("processing...")
        if int(episodes) > 50:
            ep = list(range(1, 51))
        else:
            ep = list(range(1, int(episodes)+1))
        temp1 = [ep[i:i + 4] for i in range(0, len(ep), 4)]
        keyboard = []
        for temp in temp1:
            button = []
            for tem in temp:
                button.append(InlineKeyboardButton(tem,callback_data=f"TR265D:{tem}:{query.from_user.id}"))
            keyboard.append(button)
        if len(ep) >= 50:
            keyboard.append([InlineKeyboardButton("<< Previous",callback_data=f'NO:{query.from_user.id}'),InlineKeyboardButton("Page 1",callback_data=f'NO:{data[1]}:{id}'),InlineKeyboardButton("Next >>",callback_data=f'X3DS2:N:{query.from_user.id}')])
        else:
            keyboard.append([InlineKeyboardButton("<< Previous",callback_data=f'NO:{query.from_user.id}'),InlineKeyboardButton("Page 1",callback_data=f'NO:{data[1]}:{id}'),InlineKeyboardButton("Next >>",callback_data=f'NO:{query.from_user.id}')])
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(user_id,False)
        text = ERROR_TEXT.format(f"load episodes: {str(e)}",user,user_id,bot_.username)
        await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')

async def FG465X(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        button = query.data
        data = button.split(":")
        user_id =int(data[-1])
        if update.effective_chat.type != 'private': 
            if user_id != query.from_user.id:
                await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
                return
        await query.answer()
    
        episodes= str(query.message.caption).split("\n")[6].split(" ")[-1]
        reply_keyboard = (query.message.reply_markup.inline_keyboard)
        button = int(reply_keyboard[0][0].text)
        page = int((reply_keyboard[-1][1].text).split(" ")[-1])
        page_data = (reply_keyboard[-1][1].callback_data).split(":")
        id = (page_data[-1])
        is_dub = True if page_data[1] == 'D' else False
        if is_dub:
            try:episodes = int(get_episodes_from_gogo(anilist_id_2_gogo_id(id)+ "-dub" ))
            except:episodes = episodes
        ep = []
        if page == 1 and data[1] == 'P':
            return
        if data[1] == 'N':
            if int(episodes) > button+100:
                end_epi = button+100     
            else:
                end_epi = int(episodes) + 1
            ep = list(range(button+50, end_epi))
        else:
            ep = list(range(button-50, button))
        temp1 = [ep[i:i + 4] for i in range(0, len(ep), 4)]
        keyboard = []
        for temp in temp1:
            buttons = []
            for tem in temp:
                buttons.append(InlineKeyboardButton(tem,callback_data=f"TR265D:{tem}:{query.from_user.id}"))
            keyboard.append(buttons)
        if len(ep) >= 49:
            if page == 2 and data[1] == 'P':
                keyboard.append([InlineKeyboardButton("<< Previous",callback_data=f'NO:{query.from_user.id}'),InlineKeyboardButton("Page 1",callback_data=f'NO:{page_data[1]}:{id}'),InlineKeyboardButton("Next >>",callback_data=f'X3DS2:N:{query.from_user.id}')]) 
            elif data[1] == 'N':
                keyboard.append([InlineKeyboardButton("<< Previous",callback_data=f'X3DS2:P:{query.from_user.id}'),InlineKeyboardButton(f"Page {page+1}",callback_data=f'NO:{page_data[1]}:{id}'),InlineKeyboardButton("Next >>",callback_data=f'X3DS2:N:{query.from_user.id}')])
            else:
                keyboard.append([InlineKeyboardButton("<< Previous",callback_data=f'X3DS2:P:{query.from_user.id}'),InlineKeyboardButton(f"Page {page-1}",callback_data=f'NO:{page_data[1]}:{id}'),InlineKeyboardButton("Next >>",callback_data=f'X3DS2:N:{query.from_user.id}')])
    
        elif data[1] == 'N':
            keyboard.append([InlineKeyboardButton("<< Previous",callback_data=f'X3DS2:P:{query.from_user.id}'),InlineKeyboardButton(f"Page {page+1}",callback_data=f'NO:{page_data[1]}:{id}'),InlineKeyboardButton("Next >>",callback_data=f'NO:{query.from_user.id}')])
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
        
    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(user_id,False)
        text = ERROR_TEXT.format(f"change pages: {str(e)}",user,user_id,bot_.username)
        await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')

async def GF265X(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    await query.answer("Processing....")
    reply_keyboard = (query.message.reply_markup.inline_keyboard)
    button = int(data[1])
    page = (reply_keyboard[-1][1].callback_data).split(":")
    id = (page[-1])
    new_id = anilist_id_2_gogo_stream_download_id(id)

    Title = str((query.message.caption).split("\n")[0]).replace("☘️ Tιтle : ","")
    is_dub = True if page[1] == 'D' else False
    if is_dub:
        Title = Title + " (Dub)"
        
    try:
        stream_links = GoGoAnime().get_stram_links(new_id,button,is_dub)
        print('Stream Links :\n',stream_links,"\n====================================")
     
        download_links = GoGoAnime().get_download_links(new_id,button,is_dub)
        print('Download Links :\n',download_links,"\n====================================")
    
        watch_online ={}
        if stream_links != None:
            for link in stream_links:
                watch_online[link.quality] = link.link
 
        download_now = {}
        if download_links != None:
            for link in download_links:
                download_now[link.quality] = link.link

        total_episodes= int(str(query.message.caption).split("\n")[6].split(" ")[-1])
        keyboard = {
            1 : {"Watch Online" : "NO:NO"},
            2 : watch_online,
            3 : {"Download" : "NO:NO"},
            4 : download_now,
        }
        if stream_links == None:
            del keyboard[1]
        edited = False
        if len(watch_online) == 4:
            button_lin_1 = dict(list(watch_online.items())[:3])
            button_lin_2 = dict(list(watch_online.items())[3:])
            keyboard[2] = button_lin_1
            keyboard[3] = button_lin_2
            edited = True
    
    
        if len(download_now) == 4:
            button_lin_1 = dict(list(download_now.items())[:3])
            button_lin_2 = dict(list(download_now.items())[3:])
            if edited:
                keyboard[4] = {"Download": "NO:NO"}
                keyboard[5] = button_lin_1
                keyboard[6] = button_lin_2
            else:
                keyboard[4] = button_lin_1
                keyboard[5] = button_lin_2
                
        keyboard[8] = {"<< Previous" : f"FRT34:P:{query.from_user.id}" , f"Episode {button}" : f"NO:{page[1]}:{id}:{button}:{total_episodes}", "Next >>" : f"FRT34:N:{query.from_user.id}" }
                
        
        reply_markup = Inline_reply_markup(keyboard)
        text = f"""<b>Download and Stream Links for episode </b><code>{button}</code><b> of </b><code>{Title}</code>"""
        umsg = await context.bot.send_message(chat_id=query.message.chat.id,text=text,parse_mode='HTML',reply_markup=reply_markup)
    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(user_id,False)
        text = ERROR_TEXT.format(f"View episode : {str(e)}",user,user_id,bot_.username) 
        await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')
        msg = await context.bot.send_message(chat_id=6880594191,text=text,parse_mode='HTML')
        await context.bot.send_message(chat_id=6880594191,text=f"https://anilist.co/anime/{id}",parse_mode='HTML',reply_to_message_id=msg.message_id)
    
async def GF5615X(update: Update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    await query.answer("Processing....")
    reply_keyboard = (query.message.reply_markup.inline_keyboard)
    button_data = (reply_keyboard[-1][1].callback_data).split(":")
    change = data[1]

    is_dub = True if button_data[1] == 'D' else False
    Title = str((query.message.text).split("of")[-1]).lstrip(' ')
    id = button_data[2]
    new_id = anilist_id_2_gogo_stream_download_id(id)
    episode = int(button_data[-2])
    total_episod = int(button_data[-1])
    
    if change == "N":
        episode_number = episode + 1
        if episode == total_episod - 1:
            final_button =  {"<< Previous" : f"FRT34:P:{query.from_user.id}" , f"Episode {episode_number}" : f"NO:{button_data[2]}:{id}:{episode_number}:{total_episod}", "Next >>" : "NO:No"}
        elif  episode == total_episod:
            return
        else:
            final_button =  {"<< Previous" : f"FRT34:P:{query.from_user.id}" , f"Episode {episode_number}" : f"NO:{button_data[2]}:{id}:{episode_number}:{total_episod}", "Next >>" : f"FRT34:N:{query.from_user.id}"}
    else:
        episode_number = episode - 1
        if episode == 2:
            final_button =  {"<< Previous" : "NO:No" , f"Episode {episode_number}" : f"NO:{button_data[2]}:{id}:{episode_number}:{total_episod}", "Next >>" : f"FRT34:N:{query.from_user.id}" }
        else:
            final_button =  {"<< Previous" : f"FRT34:P:{query.from_user.id}" , f"Episode {episode_number}" : f"NO:{button_data[2]}:{id}:{episode_number}:{total_episod}", "Next >>" : f"FRT34:N:{query.from_user.id}"}

    try:

        stream_links = GoGoAnime().get_stram_links(new_id,episode_number,is_dub)
        print('Stream Links :\n',stream_links,"\n====================================")
     
        download_links = GoGoAnime().get_download_links(new_id,episode_number,is_dub)
        print('Download Links :\n',download_links,"\n====================================")
    
        watch_online ={}
        if stream_links != None:
            for link in stream_links:
                watch_online[link.quality] = link.link
 
        download_now = {}
        if download_links != None:
            for link in download_links:
                download_now[link.quality] = link.link
    
        
        
        text = f"""<b>Download and Stream Links for episode </b><code>{episode_number}</code><b> of </b><code>{Title}</code>"""
        episode_link = f"https://aniplayer.onrender.com/watch/{id}?episode={episode_number}"
        keyboard = {
            1 : {"Watch Online" : "NO:NO"},
            2 : watch_online,
            3 : {"Download" : "NO:NO"},
            4 : download_now,
        }
        if stream_links == None:
            del keyboard[1]
        edited = False
        if len(watch_online) == 4:
            button_lin_1 = dict(list(watch_online.items())[:3])
            button_lin_2 = dict(list(watch_online.items())[3:])
            keyboard[2] = button_lin_1
            keyboard[3] = button_lin_2
            edited = True
    
    
        if len(download_now) == 4:
            button_lin_1 = dict(list(download_now.items())[:3])
            button_lin_2 = dict(list(download_now.items())[3:])
            if edited:
                keyboard[4] = {"Download": "NO:NO"}
                keyboard[5] = button_lin_1
                keyboard[6] = button_lin_2
            else:
                keyboard[4] = button_lin_1
                keyboard[5] = button_lin_2
                
        keyboard[8] = final_button
        reply_markup = Inline_reply_markup(keyboard)
        await query.edit_message_text(text=text,reply_markup=reply_markup,parse_mode='HTML')
    except Exception as e:
        bot_ = await context.bot.get_me()
        user = await mention_html(user_id,False)
        text = ERROR_TEXT.format(f"change episode : {str(e)}",user,user_id,bot_.username)
        # await context.bot.send_message(chat_id=LOG_CHAT,text=text,parse_mode='HTML')
        msg = await context.bot.send_message(chat_id=6880594191,text=text,parse_mode='HTML')
        await context.bot.send_message(chat_id=6880594191,text=f"https://anilist.co/anime/{id}",parse_mode='HTML',reply_to_message_id=msg.message_id)
