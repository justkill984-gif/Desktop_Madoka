import random
import math
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QGridLayout, QFrame)
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QMouseEvent

class GemButton(QPushButton):
    def __init__(self, gem_type, size, row, col):
        super().__init__()
        self.gem_type = gem_type
        self.size = size
        self.row = row
        self.col = col
        self.selected = False
        
        self.colors = [
            "#ff595e", "#ffca3a", "#8ac926", 
            "#1982c4", "#6a4c93", "#ff9d81"
        ]
        
        self.setFixedSize(size, size)
        self.update_style()
        
    def update_style(self):
        color = self.colors[self.gem_type]
        if self.selected:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: 3px solid white;
                    border-radius: {self.size//2}px;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    border: 4px solid #ffeb3b;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: 2px solid #cccccc;
                    border-radius: {self.size//2}px;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    border: 3px solid white;
                }}
            """)

class SimpleThreeInRowGame(QMainWindow):
    def __init__(self, on_close=None):
        super().__init__()
        self.on_close_callback = on_close
        self.dragging = False
        self.drag_position = QPoint()
        self.score = 0
        self.selected_gem = None
        self.grid_size = 8
        self.cell_size = 60
        
        self.setup_ui()
        self.setup_game()
        self.setup_animations()
        
    def setup_ui(self):
        self.setWindowTitle("Jewel Matcher - 3 в ряд")
        self.setFixedSize(600, 700)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 rgba(255, 105, 180, 0.9), 
                                        stop:0.5 rgba(186, 85, 211, 0.9),
                                        stop:1 rgba(138, 43, 226, 0.9));
            border-radius: 15px;
            border: 2px solid #ff69b4;
        """)
        self.setCentralWidget(central_widget)
        
        # Добавляем неоновое свечение с помощью эффекта тени
        self.setStyleSheet("""
            SimpleThreeInRowGame {
                background: transparent;
            }
            QWidget#central {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(255, 105, 180, 0.85), 
                                            stop:0.5 rgba(186, 85, 211, 0.85),
                                            stop:1 rgba(138, 43, 226, 0.85));
                border-radius: 15px;
                border: 2px solid #ff69b4;
            }
            QWidget#central {
                border: 2px solid #ff69b4;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(255, 105, 180, 0.85), 
                                            stop:0.5 rgba(186, 85, 211, 0.85),
                                            stop:1 rgba(138, 43, 226, 0.85));
            }
        """)
        
        # Создаем внутренний виджет для контента
        content_widget = QWidget()
        content_widget.setObjectName("central")
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(content_widget)
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        # Заголовок
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
        
        title_label = QLabel("💎 Jewel Matcher")
        title_label.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 16px;
            background: transparent;
            text-shadow: 0 0 10px #ff69b4, 0 0 20px #ff69b4;
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
        
        self.score_label = QLabel("Счет: 0")
        self.score_label.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 14px;
            background: transparent;
            text-shadow: 0 0 5px #ff69b4;
        """)
        title_layout.addWidget(self.score_label)
        title_layout.addWidget(close_btn)
        
        content_layout.addWidget(title_bar)
        
        # Игровое поле
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(5)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        
        self.grid_widget.setStyleSheet("""
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            border: 1px solid rgba(255, 105, 180, 0.5);
        """)
        
        content_layout.addWidget(self.grid_widget)
        
        # Нижняя панель
        bottom_widget = QWidget()
        bottom_widget.setFixedHeight(40)
        bottom_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 rgba(186, 85, 211, 0.9), 
                                        stop:1 rgba(138, 43, 226, 0.9));
            border-bottom-left-radius: 13px;
            border-bottom-right-radius: 13px;
        """)
        
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(15, 5, 15, 5)
        
        # Инструкция
        instruction = QLabel("Собери 3 или более одинаковых камня в ряд!")
        instruction.setStyleSheet("""
            color: white; 
            font-size: 12px;
            background: transparent;
            text-shadow: 0 0 5px #ff69b4;
        """)
        instruction.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(instruction)
        
        content_layout.addWidget(bottom_widget)
        
    def setup_animations(self):
        # Анимация появления
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        
    def setup_game(self):
        self.gems = []
        self.create_grid()
        
    def create_grid(self):
        # Очищаем сетку
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        self.gems = []
        
        # Создаем камни
        for row in range(self.grid_size):
            row_gems = []
            for col in range(self.grid_size):
                gem = GemButton(random.randint(0, 5), self.cell_size - 10, row, col)
                gem.clicked.connect(lambda checked, r=row, c=col: self.handle_gem_click(r, c))
                self.grid_layout.addWidget(gem, row, col)
                row_gems.append(gem)
            self.gems.append(row_gems)
        
    def handle_gem_click(self, row, col):
        if self.selected_gem is None:
            # Выбираем первый камень
            self.selected_gem = (row, col)
            self.gems[row][col].selected = True
            self.gems[row][col].update_style()
        else:
            # Проверяем, является ли клик соседним камнем
            prev_row, prev_col = self.selected_gem
            
            if ((abs(row - prev_row) == 1 and col == prev_col) or 
                (abs(col - prev_col) == 1 and row == prev_row)):
                
                # Меняем камни местами
                self.swap_gems(prev_row, prev_col, row, col)
                
                # Проверяем совпадения
                if not self.find_matches():
                    # Если нет совпадений, возвращаем обратно
                    self.swap_gems(row, col, prev_row, prev_col)
            
            # Снимаем выделение
            self.gems[prev_row][prev_col].selected = False
            self.gems[prev_row][prev_col].update_style()
            self.selected_gem = None
    
    def swap_gems(self, row1, col1, row2, col2):
        # Обмен типами камней
        type1 = self.gems[row1][col1].gem_type
        type2 = self.gems[row2][col2].gem_type
        
        self.gems[row1][col1].gem_type = type2
        self.gems[row2][col2].gem_type = type1
        
        self.gems[row1][col1].update_style()
        self.gems[row2][col2].update_style()
    
    def find_matches(self):
        found_matches = False
        
        # Проверка горизонтальных совпадений
        for row in range(self.grid_size):
            for col in range(self.grid_size - 2):
                if (self.gems[row][col].gem_type == self.gems[row][col+1].gem_type == 
                    self.gems[row][col+2].gem_type):
                    # Увеличиваем счет
                    self.score += 30
                    self.score_label.setText(f"Счет: {self.score}")
                    
                    # Заменяем совпадающие камни
                    for i in range(3):
                        self.gems[row][col+i].gem_type = random.randint(0, 5)
                        self.gems[row][col+i].update_style()
                    
                    found_matches = True
        
        # Проверка вертикальных совпадений
        for row in range(self.grid_size - 2):
            for col in range(self.grid_size):
                if (self.gems[row][col].gem_type == self.gems[row+1][col].gem_type == 
                    self.gems[row+2][col].gem_type):
                    # Увеличиваем счет
                    self.score += 30
                    self.score_label.setText(f"Счет: {self.score}")
                    
                    # Заменяем совпадающие камни
                    for i in range(3):
                        self.gems[row+i][col].gem_type = random.randint(0, 5)
                        self.gems[row+i][col].update_style()
                    
                    found_matches = True
        
        return found_matches
    
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
        
    def closeEvent(self, event):
        if self.on_close_callback:
            self.on_close_callback()
        super().closeEvent(event)

# Используем простую версию для надежности
ThreeInRowGame = SimpleThreeInRowGame