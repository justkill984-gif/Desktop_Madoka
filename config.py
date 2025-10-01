# Настройки приложения
import os

# Пути к ресурсам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
ANIMATIONS_DIR = os.path.join(ASSETS_DIR, 'animations')
MEMES_DIR = os.path.join(ASSETS_DIR, 'memes')
ICONS_DIR = os.path.join(ASSETS_DIR, 'icons')
PUNISMENT_DIR=os.path.join(ASSETS_DIR, 'punishment')
EMOJIS_DIR = os.path.join(ASSETS_DIR, "emojis")

# Настройки питомца
PET_SETTINGS = {
    'size': (200, 200),
    'movement_interval': 3000,
    'state_change_interval': 8000,
    'popup_interval': 1500,
}

# Настройки окон
WINDOW_SETTINGS = {
    'messenger_size': (400, 500),
    'about_size': (450, 600),
    'game_size': (400, 500),
}

# Сообщения питомца
POPUP_MESSAGES = [
    "Привет! Как твои дела? 💖",
    "Мяу! Я тут! 🐾",
    "Хочешь поиграть со мной? 🎮",
    "У меня есть секрет... 🤫",
    "Ты лучший хозяин! 🌟",
    "Мурр... Мне скучно! 💫",
     "Мяу! Поиграй со мной! 🐾",
    "Ты самый лучший хозяин! 💕",
    "Муррр... Мне так хорошо с тобой! 😊",
    "Скучаю по тебе! 💖",
    "Что будем делать сегодня? 🌟",
    "Ты мой самый любимый человек! 🥰",
    "Мне нужно твое внимание! 🎀",
    "Погладь меня за ушком! 🐱"
]