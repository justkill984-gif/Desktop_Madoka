# Главный файл приложения
import sys
import os
from PyQt5.QtWidgets import QApplication
from desktop_pet import DesktopPet

def main():
    # Создание необходимых директорий
    os.makedirs('assets/animations', exist_ok=True)
    os.makedirs('assets/memes', exist_ok=True)
    os.makedirs('assets/icons', exist_ok=True)
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Создание и отображение питомца
    pet = DesktopPet()
    pet.show()
    
    # Запуск приложения
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
