import sys
from PySide6 import QtWidgets, QtCore
from Lab_Splines_GUI import Ui_MainWindow 

class SplineApp(QtWidgets.QMainWindow):
    def init(self):
        super().init()
        self.ui = Ui_MainWindow()
        
        # Полный сброс: создаем чистый контейнер
        main_container = QtWidgets.QWidget()
        self.setCentralWidget(main_container)
        
        # Накатываем UI
        self.ui.setupUi(self)
        
        # ГЛАВНЫЙ ХАК: если кнопки не видно, мы берем основной лейаут 
        # из твоего файла и ПРИНУДИТЕЛЬНО ставим его в окно
        if hasattr(self.ui, 'verticalLayout_6'):
            main_container.setLayout(self.ui.verticalLayout_6)
        
        self.setWindowTitle("Lab Splines - Исправлено")
        self.resize(1100, 500) # Даем принудительный размер

        # Проверка кнопок по именам из твоего файла
        self.ui.pushButton.clicked.connect(self.run_calc)

    def run_calc(self):
        print("Кнопка Draw нажата!")
        n = self.ui.spinBox.value()
        self.ui.plainTextEdit.appendPlainText(f"Расчет для n={n}...")

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     # Фикс отрисовки для Mac Intel
#     app.setStyle('Fusion') 
    
#     window = SplineApp()
#     window.show()
#     sys.exit(app.exec())