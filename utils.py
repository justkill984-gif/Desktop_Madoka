# Вспомогательные функции
import os
import random
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication
from config import ANIMATIONS_DIR, MEMES_DIR, PUNISMENT_DIR, EMOJIS_DIR

def get_screen_geometry():
    """Получить геометрию экрана"""
    return QApplication.primaryScreen().availableGeometry()

def get_random_position(width, height, margin=50):
    """Получить случайную позицию на экране"""
    screen_geometry = get_screen_geometry()
    x = random.randint(margin, max(margin, screen_geometry.width() - width - margin))
    y = random.randint(margin, max(margin, screen_geometry.height() - height - margin))
    return QRect(x, y, width, height)

def load_pixmap(filename, directories, default_size=(150, 150)):
    """Загрузить изображение с резервными вариантами"""
    for directory in directories:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            pixmap = QPixmap(filepath)
            if not pixmap.isNull():
                return pixmap.scaled(default_size[0], default_size[1], 
                                   aspectRatioMode=1, transformMode=1)
    return None

def get_available_memes():
    """Получить список доступных мемов"""
    memes = []
    if os.path.exists(MEMES_DIR):
        for file in os.listdir(MEMES_DIR):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                memes.append(os.path.join(MEMES_DIR, file))
    return memes
    
def get_available_punishment():
    """Получить список доступных блокировок"""
    punishment = []
    if os.path.exists(PUNISMENT_DIR):
        for file in os.listdir(PUNISMENT_DIR):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                punishment.append(os.path.join(PUNISMENT_DIR, file))
    return punishment

def get_available_emojis():
    """Получить список доступных графических эмодзи"""
    emojis = []
    if os.path.exists(EMOJIS_DIR):
        for file in os.listdir(EMOJIS_DIR):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                emojis.append(os.path.join(EMOJIS_DIR, file))
    return emojis