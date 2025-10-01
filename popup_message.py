import random
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QPixmap
from config import POPUP_MESSAGES
from utils import get_available_memes, get_screen_geometry

class PopupMessage(QMainWindow):
    def __init__(self, on_close=None, pet_position=None, pet_size=None):
        super().__init__()
        self.on_close_callback = on_close
        self.pet_position = pet_position  # QPoint с позицией питомца
        self.pet_size = pet_size          # QSize с размером питомца
        self.content_type = None
        self.content = None
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Определяем тип контента
        self.determine_content()
        
        # Создаем центральный виджет
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        central_widget.setStyleSheet("""
            QWidget#central_widget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(255, 105, 180, 180), 
                                            stop:1 rgba(186, 85, 211, 180));
                border-radius: 15px;
                border: 2px solid rgba(255, 105, 180, 200);
            }
        """)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Добавляем контент в зависимости от типа
        if self.content_type == "image":
            self.setup_image_content(layout)
        else:
            self.setup_text_content(layout)
            
        # Автоматически подстраиваем размер окна под содержимое
        self.adjust_size()
        
    def determine_content(self):
        """Определяет тип контента для всплывающего сообщения"""
        if random.random() < 0.3 and get_available_memes():
            self.content_type = "image"
            self.content = random.choice(get_available_memes())
        else:
            self.content_type = "text"
            self.content = random.choice(POPUP_MESSAGES)
            
    def setup_image_content(self, layout):
        """Настраивает содержимое с изображением"""
        image_label = QLabel()
        pixmap = QPixmap(self.content)
        
        if not pixmap.isNull():
            # Масштабируем изображение, чтобы высота не превышала 400px
            original_size = pixmap.size()
            max_height = 400
            
            if original_size.height() > max_height:
                # Вычисляем новую ширину с сохранением пропорций
                scaled_width = int(original_size.width() * max_height / original_size.height())
                scaled_pixmap = pixmap.scaled(scaled_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image_label.setPixmap(scaled_pixmap)
            else:
                # Используем оригинальный размер, если он меньше максимального
                image_label.setPixmap(pixmap)
        else:
            # Если изображение не загрузилось, показываем текст
            self.content_type = "text"
            self.content = "Не удалось загрузить изображение 😢"
            self.setup_text_content(layout)
            return
            
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("background: transparent;")
        image_label.setMinimumSize(1, 1)  # Минимальный размер для корректного отображения
        layout.addWidget(image_label)
        
        # Добавляем подпись к изображению
        caption_label = QLabel("Смотри какой смешной мем! 😄")
        caption_label.setAlignment(Qt.AlignCenter)
        caption_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                background: transparent;
                padding: 5px;
                text-shadow: 0 0 5px rgba(255, 105, 180, 150);
            }
        """)
        caption_label.setWordWrap(True)
        layout.addWidget(caption_label)
        
    def setup_text_content(self, layout):
        """Настраивает текстовое содержимое"""
        text_label = QLabel(self.content)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background: transparent;
                padding: 10px;
                text-shadow: 0 0 5px rgba(255, 105, 180, 150);
            }
        """)
        text_label.setWordWrap(True)
        text_label.setMinimumWidth(200)  # Минимальная ширина для текстовых сообщений
        text_label.setMaximumWidth(500)  # Максимальная ширина для текстовых сообщений
        layout.addWidget(text_label)
        
    def adjust_size(self):
        """Автоматически подстраивает размер окна под содержимое"""
        # Даем время на отрисовку виджетов
        QTimer.singleShot(50, self._perform_adjust_size)
        
    def _perform_adjust_size(self):
        """Выполняет подстройку размера после отрисовки виджетов"""
        # Получаем размер содержимого
        content_size = self.centralWidget().sizeHint()
        
        # Добавляем отступы и рамки
        margin = 30  # Отступы + рамки
        new_width = content_size.width() + margin
        new_height = content_size.height() + margin
        
        # Устанавливаем минимальные и максимальные размеры
        min_width = 250
        max_width = 600
        min_height = 100
        max_height = 500  # Максимальная высота с учетом ограничения изображений
        
        # Ограничиваем размеры
        new_width = max(min_width, min(new_width, max_width))
        new_height = max(min_height, min(new_height, max_height))
        
        self.setFixedSize(new_width, new_height)
        
        # После установки размера позиционируем окно относительно питомца
        self.position_relative_to_pet()
        
    def position_relative_to_pet(self):
        """Позиционирует окно относительно питомца с учетом границ экрана"""
        if not self.pet_position or not self.pet_size:
            return
            
        screen_geometry = get_screen_geometry()
        popup_width = self.width()
        popup_height = self.height()
        
        # Вычисляем позицию справа от питомца, выровненную по "голове" (примерно 60px от верха)
        target_x = self.pet_position.x() + self.pet_size.width() + 10
        target_y = self.pet_position.y() + 60  # Выравнивание по "голове" питомца
        
        # Проверяем, не выходит ли окно за правую границу экрана
        if target_x + popup_width > screen_geometry.width():
            # Если выходит, показываем слева от питомца
            target_x = self.pet_position.x() - popup_width - 10
        
        # Проверяем, не выходит ли окно за нижнюю границу экрана
        if target_y + popup_height > screen_geometry.height():
            # Поднимаем окно выше
            target_y = screen_geometry.height() - popup_height - 10
        
        # Проверяем, не выходит ли окно за верхнюю границу экрана
        if target_y < 0:
            # Опускаем окно ниже
            target_y = 10
            
        # Убеждаемся, что окно не выходит за левую границу
        if target_x < 0:
            target_x = 10
            
        self.move(target_x, target_y)
        
    def setup_animation(self):
        # Анимация появления
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        self.animation.start()
        
        # После появления запускаем таймер для исчезновения
        self.animation.finished.connect(
            lambda: QTimer.singleShot(4000, self.fade_out)
        )
        
    def fade_out(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InBack)
        self.animation.finished.connect(self.close)
        self.animation.start()
        
    def closeEvent(self, event):
        if self.on_close_callback:
            self.on_close_callback()
        super().closeEvent(event)