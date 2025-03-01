# python-telegram-black-plague-rat

A Telegram bot for remote system monitoring and control.

## Features
- System information gathering
- Screenshot capture
- Chrome password extraction
- Directory listing
- File download
- Message box display
- Self-destruct capability
- Logging system

## Prerequisites
- Windows operating system
- Python 3.6+
- Required Python packages:
  ```
  telebot
  autopy
  requests
  pywin32
  pathlib
  ```

## Installation
1. Install required packages:
```bash
pip install telebot autopy requests pywin32 pathlib
```

2. Configure the bot:
- Edit the script and replace `TOKEN` with your Telegram Bot token
- Replace `ADMIN_ID` with your Telegram user ID

3. Run the bot:
```bash
python python-telegram-black-plague-rat.py
```

## Usage
### Available Commands
```
/start - Initialize connection and show command list
/target_info - Get the target system and IP information
/screen - Capture and send a screenshot
/dis - Disconnect the bot
/msg <message> - Display a message box on target
/psw - Extract and send Chrome passwords
/dir <path> - List contents of specified directory
/dfile <path> - Download file from target
/show_dir - Show current working directory
/self_des - Delete the bot from the system
```

### Command Examples
1. Get system info:
```
/target_info
```

2. Take a screenshot:
```
/screen
```

3. Show message on target:
```
/msg Hello from remote!
```

4. List directory contents:
```
/dir C:\Users
```

5. Download a file:
```
/dfile C:\Users\file.txt
```

## Security Notes
- The bot only responds to commands from the configured ADMIN_ID
- All operations are logged to `bot.log`
- Temporary files are cleaned up after use
- Sensitive operations require admin privileges

## Logging
- All operations are logged to `bot.log` with timestamps
- Log levels: INFO, ERROR
- Useful for debugging and tracking activities

## Persistence
- Automatically copies itself to Windows Startup folder
- Runs on system boot

## Troubleshooting
1. Bot not responding:
   - Check the Telegram token
   - Verify internet connection
   - Check bot.log for errors

2. Commands failing:
   - Ensure proper permissions
   - Verify file paths exist
   - Check error messages in Telegram

## Limitations
- Windows-only due to win32 dependencies
- Requires admin privileges for some operations
- Chrome password extraction works only with a default profile

## Disclaimer
This software is for educational purposes only. You can use it responsibly and with permission on systems you own or have explicit authorisation to access. The author is not responsible for any misuse or damage caused by this software.
```
