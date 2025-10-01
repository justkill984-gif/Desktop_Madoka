import random
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QScrollArea, QFrame,
                             QApplication, QFileDialog, QGridLayout, QScrollBar,
                             QMenu, QAction, QMessageBox)
from PyQt5.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QMouseEvent, QFont, QPixmap, QMovie, QIcon
from PyQt5.Qt import QSize
from utils import get_available_punishment, get_available_emojis

class LockScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.showFullScreen()
        
    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        central_widget = QWidget()
        central_widget.setStyleSheet("background: rgba(0, 0, 0, 0.95);")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # Случайная картинка из доступных
        punishment_path = random.choice(get_available_punishment())
        image_label = QLabel()
        
        pixmap = self.create_punishment_image(punishment_path)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("background: transparent;")
        
        message_label = QLabel("🔒 Доигрался, Лоликонщик несчастный!")
        message_label.setStyleSheet("""
            color: red;
            font-size: 36px;
            font-weight: bold;
            background: transparent;
            padding: 30px;
            border: 3px solid red;
            border-radius: 20px;
        """)
        message_label.setAlignment(Qt.AlignCenter)
        
        timer_label = QLabel("Разблокировка через: 60 секунд")
        timer_label.setObjectName("timer_label")
        timer_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            background: transparent;
            margin-top: 10px;
        """)
        timer_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(image_label)
        layout.addWidget(message_label)
        layout.addWidget(timer_label)
        
        # Таймер для обратного отсчета
        self.seconds_remaining = 60
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
   
    def create_punishment_image(self, punishment_path):
        """Загружает изображение из файла"""
        pixmap = QPixmap(punishment_path)
        if pixmap.isNull():
            # Если файл не найден, создаем простую картинку
            size = QSize(300, 200)
            fallback_pixmap = QPixmap(size)
            fallback_pixmap.fill(Qt.red)
            return fallback_pixmap
        
        # Масштабируем до нужного размера
        return pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
    def update_timer(self):
        self.seconds_remaining -= 1
        timer_label = self.findChild(QLabel, "timer_label")
        if timer_label:
            timer_label.setText(f"Разблокировка через: {self.seconds_remaining} секунд")
        
        if self.seconds_remaining <= 0:
            self.timer.stop()
            self.animate_close()
            
    def animate_close(self):
        """Анимация исчезновения окна"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.finished.connect(self.close)
        self.animation.start()

class ChatMessageWidget(QWidget):
    def __init__(self, content, is_user=True, timestamp=None, content_type="text"):
        super().__init__()
        self.content = content
        self.is_user = is_user
        self.content_type = content_type  # "text", "emoji", "gif"
        self.timestamp = timestamp or datetime.now()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        if self.is_user:
            layout.addStretch()
            
        message_frame = QFrame()
        message_frame.setObjectName("message_frame")
        message_layout = QVBoxLayout(message_frame)
        message_layout.setContentsMargins(12, 8, 12, 8)
        message_layout.setAlignment(Qt.AlignCenter)
        
        # В зависимости от типа контента создаем разные виджеты
        if self.content_type == "text":
            content_widget = QLabel(self.content)
            content_widget.setWordWrap(True)
            content_widget.setMaximumWidth(300)
            content_widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
            content_widget.setStyleSheet("color: white; background: transparent; font-size: 12px;")
        elif self.content_type == "emoji":
            content_widget = QLabel()
            content_widget.setAlignment(Qt.AlignCenter)
            content_widget.setMaximumSize(100, 100)
            
            # Загружаем изображение эмодзи
            pixmap = QPixmap(self.content)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                content_widget.setPixmap(pixmap)
            else:
                # Если не удалось загрузить, показываем текстовый эмодзи
                content_widget.setText("😊")
                content_widget.setStyleSheet("font-size: 24px; color: white; background: transparent;")
        elif self.content_type == "gif":
            content_widget = QLabel()
            content_widget.setAlignment(Qt.AlignCenter)
            content_widget.setMaximumSize(200, 150)
            
            # Загружаем GIF
            movie = QMovie(self.content)
            movie.setScaledSize(QSize(150, 100))
            content_widget.setMovie(movie)
            movie.start()
        
        time_label = QLabel(self.timestamp.strftime("%H:%M"))
        time_label.setAlignment(Qt.AlignRight)
        time_label.setStyleSheet("color: rgba(255, 255, 255, 180); font-size: 10px; background: transparent;")
        
        message_layout.addWidget(content_widget)
        message_layout.addWidget(time_label)
        
        if self.is_user:
            message_frame.setStyleSheet("""
                QFrame#message_frame {
                    background: rgba(0, 123, 255, 180);
                    border-radius: 15px;
                    border-bottom-right-radius: 5px;
                    border: 1px solid rgba(255, 255, 255, 100);
                }
            """)
        else:
            message_frame.setStyleSheet("""
                QFrame#message_frame {
                    background: rgba(255, 255, 255, 120);
                    border-radius: 15px;
                    border-bottom-left-radius: 5px;
                    border: 1px solid rgba(255, 255, 255, 80);
                }
                QLabel {
                    color: black;
                }
            """)
        
        layout.addWidget(message_frame)
        
        if not self.is_user:
            layout.addStretch()
            
        self.setLayout(layout)

class EmojiPicker(QMainWindow):
    def __init__(self, messenger_window):
        super().__init__()
        self.messenger_window = messenger_window
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(300, 200)
        
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)
        
        self.setStyleSheet("""
            QMainWindow {
                background: transparent;
            }
            QWidget#central_widget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(255, 105, 180, 200), 
                                            stop:1 rgba(186, 85, 211, 200));
                border-radius: 15px;
                border: 2px solid rgba(255, 105, 180, 220);
            }
        """)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_label = QLabel("Выберите эмодзи:")
        title_label.setStyleSheet("""
            color: white; 
            font-size: 14px; 
            font-weight: bold;
            background: transparent;
            text-shadow: 0 0 5px rgba(255, 105, 180, 150);
        """)
        layout.addWidget(title_label)
        
        # Сетка для эмодзи
        emoji_grid = QGridLayout()
        emoji_grid.setSpacing(5)
        
        available_emojis = get_available_emojis()
        
        # Показываем до 12 эмодзи (3x4)
        for i, emoji_path in enumerate(available_emojis[:12]):
            row = i // 4
            col = i % 4
            
            emoji_btn = QPushButton()
            emoji_btn.setFixedSize(50, 50)
            emoji_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 120);
                    border: 1px solid rgba(255, 255, 255, 80);
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: rgba(255, 193, 7, 180);
                    border: 1px solid rgba(255, 193, 7, 220);
                }
            """)
            
            # Загружаем изображение эмодзи
            pixmap = QPixmap(emoji_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QIcon(pixmap)
                emoji_btn.setIcon(icon)
                emoji_btn.setIconSize(QSize(30, 30))
            
            emoji_btn.clicked.connect(lambda checked, path=emoji_path: self.send_emoji(path))
            emoji_grid.addWidget(emoji_btn, row, col)
        
        layout.addLayout(emoji_grid)
        
        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 105, 180, 180);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 105, 180, 220);
                border: 1px solid white;
            }
        """)
        close_btn.clicked.connect(self.close_window)
        layout.addWidget(close_btn)
        
    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        
    def close_window(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.finished.connect(self.close)
        self.animation.start()
        
    def send_emoji(self, emoji_path):
        if self.messenger_window:
            self.messenger_window.add_message(emoji_path, True, "emoji")
            QTimer.singleShot(1000, self.messenger_window.pet_response)
        self.close_window()

class ChatHistoryManager:
    """Менеджер для работы с историей чата"""
    
    def __init__(self, filename="chat_history.json"):
        self.filename = filename
        self.history = []
        self.max_history_size = 1000  # Максимальное количество сообщений в истории
        self.load_history()
    
    def load_history(self):
        """Загружает историю чата из файла"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                # Ограничиваем размер истории
                if len(self.history) > self.max_history_size:
                    self.history = self.history[-self.max_history_size:]
            else:
                self.history = []
        except Exception as e:
            print(f"Ошибка загрузки истории чата: {e}")
            self.history = []
    
    def save_history(self):
        """Сохраняет историю чата в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения истории чата: {e}")
    
    def add_message(self, message):
        """Добавляет сообщение в историю"""
        # Преобразуем datetime в строку для сериализации
        if 'timestamp' in message and isinstance(message['timestamp'], datetime):
            message['timestamp'] = message['timestamp'].isoformat()
        
        self.history.append(message)
        
        # Ограничиваем размер истории
        if len(self.history) > self.max_history_size:
            self.history = self.history[-self.max_history_size:]
        
        self.save_history()
    
    def clear_history(self):
        """Очищает историю чата"""
        self.history = []
        try:
            if os.path.exists(self.filename):
                os.remove(self.filename)
        except Exception as e:
            print(f"Ошибка удаления файла истории: {e}")
        self.save_history()
    
    def get_recent_messages(self, count=100):
        """Возвращает последние сообщения из истории"""
        return self.history[-count:] if self.history else []

class AIChatBot:
    def __init__(self):
        self.responses = [
            "Привет! Как твои дела? 💖",
            "Мяу! Я так рада тебя видеть! 🐾",
            "Расскажи мне что-нибудь интересное! 🌟",
            "Ты сегодня особенно мил! 😊",
            "Мурр... Я обожаю с тобой говорить! 💕",
            "Что нового у тебя? 🎀",
            "Ты лучший хозяин на свете! 🌈",
            "Мне так весело с тобой! 🎉"
        ]
        
        # Ответы на плохие слова
        self.bad_word_responses = [
            "Ой-ой, так нельзя говорить! 😾",
            "Мяу! Не ругайся! 🚫",
            "Фу-фу, такие слова некрасиво! 👿",
            "Я обижусь, если ты будешь так говорить! 😿"
        ]
        
    def get_response(self, user_message):
        user_message_lower = user_message.lower()
        # Проверяем на плохие слова
        if self.contains_bad_words(user_message_lower):
            return {"type": "text", "content": random.choice(self.bad_word_responses)}
    
        # С вероятностью 30% отвечаем графическим эмодзи
        if random.random() < 0.3:
            emojis = get_available_emojis()
            if emojis:
                return {"type": "emoji", "content": random.choice(emojis)}
    
        # Контекстные ответы
        if any(word in user_message_lower for word in ['привет', 'здравствуй', 'hello', 'hi']):
            responses = [
                "Привет, хозяин! 💖 Как твои дела?",
                "Мяу! Приветствую тебя! 🐾",
                "О, ты здесь! Я так рада тебя видеть! 😊"
            ]
            return {"type": "text", "content": random.choice(responses)}
    
        elif any(word in user_message_lower for word in ['как дела', 'как ты', 'самочувствие']):
            responses = [
                "У меня все прекрасно, особенно когда ты рядом! 💕",
                "Чувствую себя отлично! Готова играть и обниматься! 🎀",
                "Мур-мур... Я счастлива, когда ты со мной говоришь! 😸"
        ]
            return {"type": "text", "content": random.choice(responses)}
    
        elif any(word in user_message_lower for word in ['красив', 'мил', 'хорош', 'люблю']):
            responses = [
                "Ой, ты меня смущаешь! 😳💖",
                "Спасибо! Ты тоже самый лучший! 🌸",
                "Мурр... Ты делаешь меня такой счастливой! 💕"
            ]
            return {"type": "text", "content": random.choice(responses)}
    
        elif any(word in user_message_lower for word in ['пока', 'до свидания', 'спокойной']):
            responses = [
                "Пока-пока! Возвращайся скорее! 😘",
                "До встречи! Буду скучать! 💔",
                "Спокойной ночи, сладких снов! 🌙✨"
            ]
            return {"type": "text", "content": random.choice(responses)}
    
        elif any(word in user_message_lower for word in ['еда', 'кушать', 'голоден', 'есть']):
            responses = [
                "Я уже покушала, спасибо! Но печенек никогда не бывает много! 🍪",
                "Ммм... Я люблю рыбку и сливочки! 🐟🥛",
                "Я не голодна, но с удовольствием составлю тебе компанию! 😊"
            ]
            return {"type": "text", "content": random.choice(responses)}
    
        else:
            responses = [
                "Интересно! Расскажи мне больше об этом! 💭",
                "Мяу! Я слушаю внимательно! 🐾",
                "Как здорово! Ты всегда рассказываешь такие интересные вещи! 🌟",
                "Правда? Это так увлекательно! 😮",
                "Мурр... Я думаю над твоими словами! 💖",
                "Очень интересно! Что еще ты хочешь рассказать? 🎀"
            ]
            return {"type": "text", "content": random.choice(responses)}
    
    def contains_bad_words(self, text):
        bad_words = [
            'мат', 'плохоеслово', 'ругательство',
            'бля', 'хуй', 'пизда', 'ебать', 'нахуй'
        ]
        text_lower = text.lower()
        return any(bad_word in text_lower for bad_word in bad_words)
        
class MessengerWindow(QMainWindow):
    def __init__(self, on_close=None):
        super().__init__()
        self.on_close_callback = on_close
        self.ai_bot = AIChatBot()
        self.messages = []
        self.dragging = False
        self.drag_position = QPoint()
        self.history_manager = ChatHistoryManager()
        self.setup_ui()
        self.setup_animations()
        self.load_chat_history()
        
    def setup_ui(self):
        self.setWindowTitle("Чат с питомцем")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)
        
        self.setStyleSheet("""
            QMainWindow {
                background: transparent;
            }
            QWidget#central_widget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(255, 105, 180, 180), 
                                            stop:0.5 rgba(186, 85, 211, 180),
                                            stop:1 rgba(138, 43, 226, 180));
                border-radius: 15px;
                border: 2px solid rgba(255, 105, 180, 200);
            }
        """)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Заголовок с градиентом
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 rgba(255, 105, 180, 200), 
                                        stop:1 rgba(186, 85, 211, 200));
            border-top-left-radius: 13px;
            border-top-right-radius: 13px;
        """)
        title_bar.mousePressEvent = self.title_mouse_press_event
        title_bar.mouseMoveEvent = self.title_mouse_move_event
        title_bar.mouseReleaseEvent = self.title_mouse_release_event
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        
        title_label = QLabel("💬 Чат с питомцем")
        title_label.setStyleSheet("""
            color: white; 
            font-weight: bold; 
            font-size: 14px;
            background: transparent;
            text-shadow: 0 0 10px rgba(255, 105, 180, 150);
        """)
        
        # Кнопка меню истории
        history_btn = QPushButton("📋")
        history_btn.setFixedSize(25, 25)
        history_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 193, 7, 180);
                color: white;
                font-size: 14px;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 193, 7, 220);
                border: 1px solid white;
            }
        """)
        history_btn.clicked.connect(self.show_history_menu)
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(25, 25)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 105, 180, 180);
                color: white;
                font-size: 18px;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 105, 180, 220);
                border: 1px solid white;
            }
        """)
        close_btn.clicked.connect(self.close_window)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(history_btn)
        title_layout.addWidget(close_btn)
        
        # Область чата
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("scroll_widget")
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.addStretch()
        
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        
        # Стили для области прокрутки
        self.scroll_area.setStyleSheet("""
            QScrollArea#scroll_area {
                background: rgba(255, 255, 255, 50);
                border: none;
            }
            QWidget#scroll_widget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 80);
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 105, 180, 160);
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 105, 180, 200);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Панель ввода
        input_widget = QWidget()
        input_widget.setFixedHeight(60)
        input_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 rgba(186, 85, 211, 200), 
                                        stop:1 rgba(138, 43, 226, 200));
            border-bottom-left-radius: 13px;
            border-bottom-right-radius: 13px;
        """)
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(15, 10, 15, 10)
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Введите сообщение...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 120);
                color: white;
                border: 1px solid rgba(255, 255, 255, 80);
                border-radius: 15px;
                padding: 8px 15px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255, 105, 180, 200);
                background: rgba(255, 255, 255, 150);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 180);
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        
        # Кнопка для выбора эмодзи
        emoji_btn = QPushButton("😊")
        emoji_btn.setFixedSize(40, 40)
        emoji_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 193, 7, 180);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: rgba(255, 193, 7, 220);
                border: 1px solid white;
            }
        """)
        emoji_btn.clicked.connect(self.show_emoji_picker)
        
        # Кнопка для отправки GIF
        gif_btn = QPushButton("GIF")
        gif_btn.setFixedSize(40, 40)
        gif_btn.setStyleSheet("""
            QPushButton {
                background: rgba(156, 39, 176, 180);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(156, 39, 176, 220);
                border: 1px solid white;
            }
        """)
        gif_btn.clicked.connect(self.send_gif)
        
        send_btn = QPushButton("➤")
        send_btn.setFixedSize(40, 40)
        send_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 105, 180, 180);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 105, 180, 220);
                border: 1px solid white;
            }
        """)
        send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(emoji_btn)
        input_layout.addWidget(gif_btn)
        input_layout.addWidget(send_btn)
        
        layout.addWidget(title_bar)
        layout.addWidget(self.scroll_area)
        layout.addWidget(input_widget)
        
    def setup_animations(self):
        # Анимация появления
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def title_mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()

    def title_mouse_move_event(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def title_mouse_release_event(self, event):
        self.dragging = False
        self.setCursor(Qt.ArrowCursor)
        event.accept()
        
    def close_window(self):
        # Анимация закрытия
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.finished.connect(self.close)
        self.animation.start()

    def show_history_menu(self):
        """Показывает меню управления историей"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(255, 105, 180, 200), 
                                            stop:1 rgba(186, 85, 211, 200));
                color: white;
                border: 2px solid rgba(255, 105, 180, 200);
                border-radius: 10px;
                padding: 8px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 5px;
                background: transparent;
            }
            QMenu::item:selected {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        
        # Статистика истории
        stats_action = QAction(f"📊 Сообщений в истории: {len(self.history_manager.history)}", self)
        stats_action.setEnabled(False)
        menu.addAction(stats_action)
        
        menu.addSeparator()
        
        # Экспорт истории
        export_action = QAction("💾 Экспорт истории", self)
        export_action.triggered.connect(self.export_history)
        menu.addAction(export_action)
        
        # Очистка истории
        clear_action = QAction("🗑️ Очистить историю", self)
        clear_action.triggered.connect(self.clear_history)
        menu.addAction(clear_action)
        
        # Показать меню
        menu.exec_(self.mapToGlobal(self.sender().pos()))
        
    def load_chat_history(self):
        """Загружает историю чата и отображает последние сообщения"""
        recent_messages = self.history_manager.get_recent_messages(50)  # Последние 50 сообщений
        
        for message_data in recent_messages:
            # Восстанавливаем datetime из строки
            if 'timestamp' in message_data and isinstance(message_data['timestamp'], str):
                try:
                    message_data['timestamp'] = datetime.fromisoformat(message_data['timestamp'])
                except:
                    message_data['timestamp'] = datetime.now()
            
            # Создаем виджет сообщения
            message_widget = ChatMessageWidget(
                message_data['content'],
                message_data['is_user'],
                message_data['timestamp'],
                message_data['content_type']
            )
            
            # Добавляем в интерфейс
            if message_data['is_user']:
                self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, message_widget)
            else:
                self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, message_widget)
            
            # Сохраняем в текущие сообщения
            self.messages.append(message_data)
        
        # Прокручиваем вниз
        if recent_messages:
            QTimer.singleShot(100, self.scroll_to_bottom)

    def export_history(self):
        """Экспортирует историю чата в файл"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт истории чата", "chat_history.json", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                # Копируем историю в выбранный файл
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.history_manager.history, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "Успех", "История чата успешно экспортирована!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать историю: {str(e)}")
                
    def clear_history(self):
        """Очищает историю чата"""
        reply = QMessageBox.question(
            self, 
            "Подтверждение", 
            "Вы уверены, что хотите очистить всю историю чата? Это действие нельзя отменить.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Очищаем историю
            self.history_manager.clear_history()
            
            # Очищаем интерфейс
            for i in reversed(range(self.scroll_layout.count() - 1)):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            
            # Очищаем список сообщений
            self.messages.clear()
            
            QMessageBox.information(self, "Успех", "История чата очищена!")

    def send_message(self):
        text = self.message_input.text().strip()
        if text:
            # Проверяем на плохие слова
            if self.contains_very_bad_words(text):
                self.add_message("⚠️ Использование запрещенных слов!", True, "text")
                self.message_input.clear()
                QTimer.singleShot(1000, self.activate_lock_screen)
                return
                
            self.add_message(text, True, "text")
            self.message_input.clear()
            QTimer.singleShot(1000, self.pet_response)
            
    def show_emoji_picker(self):
        """Показывает окно выбора эмодзи"""
        self.emoji_picker = EmojiPicker(self)
        # Позиционируем окно рядом с кнопкой эмодзи
        emoji_btn_pos = self.sender().mapToGlobal(QPoint(0, 0))
        self.emoji_picker.move(emoji_btn_pos.x() - 250, emoji_btn_pos.y() - 200)
        self.emoji_picker.show()
        
    def send_gif(self):
        """Открывает диалог выбора GIF"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите GIF", "", "GIF Files (*.gif)"
        )
        if file_path:
            self.add_message(file_path, True, "gif")
            QTimer.singleShot(1000, self.pet_response)
            
    def contains_very_bad_words(self, text):
        very_bad_words = [
            'бля', 'хуй', 'пизда', 'ебать', 'нахуй', 'еблан',
            'сука', 'мудак', 'гондон', 'залупа', 'дрочить'
        ]
        text_lower = text.lower()
        return any(bad_word in text_lower for bad_word in very_bad_words)
        
    def activate_lock_screen(self):
        """Активирует экран блокировки"""
        self.lock_screen = LockScreen()
        self.lock_screen.show()
        
        # Добавляем сообщение от питомца
        punishment_responses = [
            "Я очень расстроена твоим поведением! 😾",
            "Так с тобой никто не будет играть! 👿",
            "Мне нужно время, чтобы прочить тебя... 😿",
            "Ты огорчил меня своими словами! 💔"
        ]
        punishment_message = random.choice(punishment_responses)
        self.add_message(punishment_message, False, "text")
            
    def add_message(self, content, is_user, content_type):
        # Создаем данные сообщения
        message_data = {
            'content': content,
            'is_user': is_user,
            'content_type': content_type,
            'timestamp': datetime.now()
        }
        
        # Создаем виджет сообщения
        message_widget = ChatMessageWidget(
            content, is_user, message_data['timestamp'], content_type
        )
        
        # Добавляем в интерфейс
        if is_user:
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, message_widget)
        else:
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, message_widget)
            
        # Сохраняем в текущие сообщения
        self.messages.append(message_data)
        
        # Сохраняем в историю
        self.history_manager.add_message(message_data)
        
        # Прокручиваем вниз
        QTimer.singleShot(100, self.scroll_to_bottom)
        
    def pet_response(self):
        # Получаем последнее сообщение пользователя для контекста
        user_message = ""
        if self.messages:
            last_msg = self.messages[-1]
            if last_msg['is_user'] and last_msg['content_type'] == "text":
                user_message = last_msg['content']
                
        response = self.ai_bot.get_response(user_message)
        self.add_message(response["content"], False, response["type"])
        
    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def closeEvent(self, event):
        if self.on_close_callback:
            self.on_close_callback()
        super().closeEvent(event)