from .start import start_command , X24DF , X24DE
from .post import post_command
from .broadcast import broadcast_command
from .anime import anime_command , anime_message_task
from .airing import airing_command , airing_message_task , TG654
from .schedule import schedule_command , FYC245
from .feedback import feedback_command
from .help import help_command
from .ping import ping_command
from .character import character_command , character_message_task , TH654
from .manga import manga_command , manga_message_task
from .top import top_anime_command , TG154
from .browse import browse_command , TH154
from .latest import latest_command , SLPX32
from .popular import popular_command

from Config import LOG_CHAT , RESTART_MSG

import asyncio
import os
import sys

async def restart_per_2_hours(bot,task):
    asyncio.create_task(restart_per_2_hours_task(bot,task))

async def restart_per_2_hours_task(bot,task):
    await asyncio.sleep(7200)
    task.cancel()
    await bot.send_message(chat_id=LOG_CHAT,text=RESTART_MSG.format((await bot.get_me()).username),parse_mode='HTML')
    os.execl(sys.executable, sys.executable, *sys.argv)
