from telegram import Update 
from telegram.ext import ContextTypes 
from Config import SUDO_USERS
import asyncio

import os
import glob
import importlib.util
from collections import defaultdict

__command__ = 'help'
__description__ = 'use this cmd to get all instructions'
__category__ = 'basic'


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(help_command_task(update, context))

async def help_command_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    sudo_user = user_id in SUDO_USERS
    commands_dir = os.path.dirname(os.path.abspath(__file__))
    help_text = "This is small guide on how to use me\n\n"
    categorized_commands = defaultdict(list)
    
    for command_file in glob.glob(os.path.join(commands_dir, "*.py")):
        command_name = os.path.splitext(os.path.basename(command_file))[0]
        if command_name == "__init__":
            continue
        spec = importlib.util.spec_from_file_location(command_name, command_file)
        module = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(module)
        except ImportError as e:
            categorized_commands["Errors"].append((command_name, f"ImportError - {str(e)}"))
            continue
        
        category = getattr(module, "__category__", "Uncategorized")
        command = getattr(module, "__command__", command_name)
        description = getattr(module, "__description__", "No description available")
        categorized_commands[category].append((command, description))
    
    categorys = ['basic', 'anilist', 'sudo']
    
    for category in categorys:
        if category in categorized_commands:
            if not sudo_user and category == 'sudo':
                continue
            help_text += f"{str(category).capitalize()} commands:\n<blockquote>"
            sorted_commands = sorted(categorized_commands[category], key=lambda x: x[0])
            for command, description in sorted_commands:
                help_text += f"/{command} - {description}\n\n"
            help_text += "</blockquote>\n"

    await update.message.reply_text(text=help_text, parse_mode='HTML')
