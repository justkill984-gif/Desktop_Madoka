# desktop_pet.py (обновленное контекстное меню)
import os
import random
from PyQt5.QtWidgets import (QMainWindow, QLabel, QMenu, QAction, QApplication)
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation
from PyQt5.QtGui import QMovie, QMouseEvent
from config import PET_SETTINGS, ANIMATIONS_DIR
from utils import get_random_position, get_screen_geometry
from popup_message import PopupMessage
from about_window import AboutWindow
from messenger import MessengerWindow
from qt_three_in_row import ThreeInRowGame

class DesktopPet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.open_windows = []
        self.is_moving = True
        self.movement_paused = False
        self.dragging = False
        self.offset = QPoint()
        self.direction = 1
        
        self.setup_ui()
        self.setup_animations()
        self.setup_movement()
        self.setup_context_menu()
        self.setup_popups()
        
    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(*PET_SETTINGS['size'])
        
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, *PET_SETTINGS['size'])
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background: transparent;")
        
        screen_geometry = get_screen_geometry()
        start_x = 50
        start_y = screen_geometry.height() - PET_SETTINGS['size'][1] - 50
        self.move(start_x, start_y)
        
    def setup_animations(self):
        self.animations = {}
        animation_files = {
            'idle': 'idle_animation.gif',
            'right': 'right_animation.gif', 
            'left': 'left_animation.gif'
        }
        
        for name, filename in animation_files.items():
            path = os.path.join(ANIMATIONS_DIR, filename)
            if os.path.exists(path):
                self.animations[name] = QMovie(path)
                
        if 'idle' in self.animations:
            self.current_animation = self.animations['idle']
            self.label.setMovie(self.current_animation)
            self.current_animation.start()
            
    def setup_movement(self):
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_pet)
        self.move_timer.start(PET_SETTINGS['movement_interval'])
        
        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.change_state)
        self.state_timer.start(PET_SETTINGS['state_change_interval'])
        
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(2000)
        
    def setup_popups(self):
        self.popup_timer = QTimer(self)
        self.popup_timer.timeout.connect(self.show_popup)
        self.popup_timer.start(PET_SETTINGS['popup_interval'])
        
    def setup_context_menu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(255, 105, 180, 0.95), 
                                            stop:1 rgba(186, 85, 211, 0.95));
                color: white;
                border: 2px solid #ff69b4;
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
            QMenu::separator {
                height: 1px;
                background: rgba(255, 255, 255, 0.3);
                margin: 5px 10px;
            }
        """)
        
        actions = [
            ("💬 Чат с питомцем", self.open_messenger),
            ("🎮 Играть в 3 в ряд", self.open_game),
            ("ℹ️ О программе", self.open_about),
            ("---", None),
            ("🚪 Выход", self.close)
        ]
        
        for text, callback in actions:
            if text == "---":
                menu.addSeparator()
            else:
                action = QAction(text, self)
                if callback:
                    action.triggered.connect(callback)
                menu.addAction(action)
                
        menu.exec_(self.mapToGlobal(pos))
        
    # ... остальные методы desktop_pet.py остаются без изменений
        
    def open_messenger(self):
        self.pause_movement()
        window = MessengerWindow(
            on_close=self.resume_movement
        )
        self.position_window_near_pet(window)
        window.show()
        self.open_windows.append(window)
        
    def open_game(self):
        self.pause_movement()
        window = ThreeInRowGame(
            on_close=self.resume_movement
        )
        self.position_window_near_pet(window)
        window.show()
        self.open_windows.append(window)
        
    def open_about(self):
        self.pause_movement()
        window = AboutWindow(
            on_close=self.resume_movement
        )
        self.position_window_near_pet(window)
        window.show()
        self.open_windows.append(window)
        
    def position_window_near_pet(self, window):
        pet_pos = self.pos()
        screen_geometry = get_screen_geometry()
        
        window_x = pet_pos.x() + self.width() + 10
        window_y = pet_pos.y()
        
        if window_x + window.width() > screen_geometry.width():
            window_x = pet_pos.x() - window.width() - 10
            
        if window_y + window.height() > screen_geometry.height():
            window_y = screen_geometry.height() - window.height() - 10
            
        window.move(window_x, window_y)
        
    def pause_movement(self):
        self.movement_paused = True
        self.is_moving = False
        self.animation.stop()
        self.switch_animation('idle')
        
    def resume_movement(self):
        self.movement_paused = False
        self.is_moving = True
        
   # desktop_pet.py (обновленный метод show_popup)
    def show_popup(self):
        if random.random() < 0.3 and not self.movement_paused:
            self.pause_movement()
        
            # Создаем popup с передачей позиции и размера питомца
            popup = PopupMessage(
                on_close=self.resume_movement,
                pet_position=self.pos(),  # Текущая позиция питомца
                pet_size=self.size()      # Размер питомца
            )
            popup.show()
            
    def move_pet(self):
        if not self.is_moving or self.dragging or self.movement_paused:
            return
            
        new_geometry = get_random_position(*PET_SETTINGS['size'])
        
        current_x = self.geometry().x()
        new_x = new_geometry.x()
        self.direction = 1 if new_x > current_x else -1
        
        animation_name = 'right' if self.direction == 1 else 'left'
        self.switch_animation(animation_name)
        
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(new_geometry)
        self.animation.start()
        
    def change_state(self):
        if self.movement_paused:
            return
            
        if random.random() < 0.7:
            self.is_moving = True
            if not self.animation.state():
                self.move_pet()
        else:
            self.is_moving = False
            self.animation.stop()
            self.switch_animation('idle')
            
    def switch_animation(self, name):
        if name in self.animations and self.animations[name] != self.current_animation:
            if self.current_animation:
                self.current_animation.stop()
            self.current_animation = self.animations[name]
            self.label.setMovie(self.current_animation)
            self.current_animation.start()
            
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.pause_movement()
            self.offset = event.globalPos() - self.pos()
            self.setCursor(Qt.ClosedHandCursor)
            
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.dragging:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)
            if not self.movement_paused:
                self.resume_movement()
                QTimer.singleShot(2000, self.move_pet)
                
    def closeEvent(self, event):
        for window in self.open_windows:
            try:
                window.close()
            except:
                pass
        super().closeEvent(event)