from telegram import Bot
from Config import TOKEN 

BOT = Bot(TOKEN)

def block_text(text):
    text = str(text.lower())
    text = text.replace('a', 'ᴀ').replace('b', 'ʙ').replace('c', 'ᴄ').replace('d', 'ᴅ').replace('e', 'ᴇ').replace('f', 'ғ').replace('g', 'ɢ').replace('h', 'ʜ').replace('i', 'ɪ').replace('j', 'ᴊ').replace('k', 'ᴋ').replace('l', 'ʟ').replace('m', 'ᴍ').replace('n', 'ɴ').replace('o', 'ᴏ').replace('p', 'ᴘ').replace('q', 'ǫ').replace('r', 'ʀ').replace('s', 's').replace('t', 'ᴛ').replace('u', 'ᴜ').replace('v', 'ᴠ').replace('w', 'ᴡ').replace('x', 'x').replace('y', 'ʏ').replace('z', 'ᴢ').replace('1', '𝟷').replace('2', '𝟸').replace('3', '𝟹').replace('4', '𝟺').replace('5', '𝟻').replace('6', '𝟼').replace('7', '𝟽').replace('8', '𝟾').replace('9', '𝟿').replace('0', '𝟶')
    return text

async def get_user_first_name(user_id,block_text):
    user  = await BOT.get_chat(user_id)
    if block_text:
        return block_text(user.first_name)
    return user.first_name

async def mention_markdown(user_id,block_text):
    first_name = await get_user_first_name(user_id,block_text)
    first_name = first_name.replace("[", "")
    first_name = first_name.replace("]", "")
    first_name = first_name.replace("(", "")
    first_name = first_name.replace(")", "")
    mention = f"[{first_name}](tg://user?id={user_id})"
    return mention

async def mention_html(user_id: int,block_text: bool):
    first_name = await get_user_first_name(user_id,block_text)
    mention = f"<a href ='tg://user?id={user_id}'>{first_name}</a>"
    return mention
