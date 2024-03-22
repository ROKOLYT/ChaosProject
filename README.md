# Lost Ark Daily Chaos Dungeon Bot

This bot is designed to automate daily chaos dungeon runs in Lost Ark on all characters seamlessly. It utilizes a combination of OCR (Optical Character Recognition), color detection, pattern detection, and inputs to perform its tasks efficiently. The bot operates independently from the game's code, ensuring undetectability.
# Features

+ Automated Chaos Dungeon Runs: Perform daily chaos dungeon runs on all characters automatically.
+ Automated Guild Daily: Perform daily guild donation.
+ Undetectable Operation: The bot operates separately from the game's code, ensuring undetectability.
+ Smart Logic and Checks: Implements logic and checks to ensure smooth operation and adaptability to changes.

# Requirements

+ Python 3.11
+ PyTorch >= 2.2.1

# Installation

```
    git clone https://github.com/ROKOLYT/ChaosProject.git
    cd ChaosProject
    pip install -r requirements.txt
```

# WARNING
You have to change the code of pyautogui not to raise ImageNotFoundException.
Find pyautogui/__init__ and change

    raise ImageNotFoundException -> return None
    
# Usage
```
python bot.py
```
Ensure your screen resolution is set to 1920x1080 and the aspect ratio is 21:9.
Launch Lost Ark and navigate to the first character.
Start the bot.
The bot will perform chaos dungeon runs on all characters.

# Disclaimer

This bot is intended for educational purposes only. Use at your own risk. We do not take responsibility for any consequences resulting from the use of this bot. Always abide by the terms of service and rules set forth by the game developers.
# Contributing

Contributions are welcome! If you have any suggestions, improvements, or feature requests, feel free to open an issue or submit a pull request.
# License

This project is licensed under the MIT License.
