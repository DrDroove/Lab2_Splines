from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

app = QApplication([])
loader = QUiLoader()
window = loader.load("Lab_Splines_GUI.ui")  # ← ВАЖНО
window.show()

app.exec()