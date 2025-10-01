# about_window.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QMouseEvent
from config import WINDOW_SETTINGS

class AboutWindow(QMainWindow):
    def __init__(self, on_close=None):
        super().__init__()
        self.on_close_callback = on_close
        self.dragging = False
        self.drag_position = QPoint()
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        self.setWindowTitle("О программе")
        self.setFixedSize(*WINDOW_SETTINGS['about_size'])
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        central_widget = QWidget()
        central_widget.setObjectName("central")
        central_widget.setStyleSheet("""
            QWidget#central {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(255, 105, 180, 0.9), 
                                            stop:0.5 rgba(186, 85, 211, 0.9),
                                            stop:1 rgba(138, 43, 226, 0.9));
                border-radius: 15px;
                border: 2px solid #ff69b4;
            }
        """)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Заголовок с градиентом
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 rgba(255, 105, 180, 0.9), 
                                        stop:1 rgba(186, 85, 211, 0.9));
            border-top-left-radius: 13px;
            border-top-right-radius: 13px;
        """)
        title_bar.mousePressEvent = self.title_mouse_press_event
        title_bar.mouseMoveEvent = self.title_mouse_move_event
        title_bar.mouseReleaseEvent = self.title_mouse_release_event
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        
        title_label = QLabel("💖 О программе")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                text-shadow: 0 0 10px #ff69b4, 0 0 20px #ff69b4;
            }
        """)
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(25, 25)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 105, 180, 0.8);
                color: white;
                font-size: 18px;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 105, 180, 1);
                border: 1px solid white;
            }
        """)
        close_btn.clicked.connect(self.close_window)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)
        layout.addWidget(title_bar)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background: rgba(255, 255, 255, 0.3);")
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        
        # Контент
        content_widget = QWidget()
        content_widget.setStyleSheet("background: rgba(255, 255, 255, 0.1); border-radius: 10px;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        
        content = """
        <div style='color: white; font-size: 12px; line-height: 1.5;'>
        <p style='text-align: center;'><b>Виртуальный питомец-девушка v1.0</b></p>
        <p style='text-align: center;'>Умный спутник для вашего рабочего стола!</p>
        <br>
        <p><b>Возможности:</b></p>
        <ul>
            <li>🤖 ИИ-чат с эмоциональными ответами</li>
            <li>🎮 Мини-игра "3 в ряд"</li>
            <li>💬 Всплывающие сообщения и мемы</li>
            <li>🎬 Плавные анимации движений</li>
            <li>🖱️ Полная интерактивность</li>
        </ul>
        <br>
        <p><b>Технологии:</b> Python, PyQt5</p>
        <p style='color: rgba(255, 255, 255, 0.7); font-size: 10px; text-align: center;'>
            Сделано с ❤️ для хорошего настроения!
        </p>
        </div>
        """
        
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("background: transparent;")
        content_layout.addWidget(content_label)
        
        layout.addWidget(content_widget)
        layout.addStretch()
        
        # Нижняя панель
        bottom_widget = QWidget()
        bottom_widget.setFixedHeight(30)
        bottom_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 rgba(186, 85, 211, 0.9), 
                                        stop:1 rgba(138, 43, 226, 0.9));
            border-bottom-left-radius: 13px;
            border-bottom-right-radius: 13px;
        """)
        layout.addWidget(bottom_widget)
        
    def setup_animations(self):
        # Анимация появления
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        
    def close_window(self):
        # Анимация закрытия
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.finished.connect(self.close)
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
        
    def closeEvent(self, event):
        if self.on_close_callback:
            self.on_close_callback()
        super().closeEvent(event)