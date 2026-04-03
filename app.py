import sys
from PySide6 import QtWidgets, QtUiTools, QtCore
import pyqtgraph as pg

import Lab2

class PlotWindow(QtWidgets.QWidget):
    def __init__(self, title, position):
        super().__init__()
        self.setWindowTitle(title)

        window_width = 800
        window_height = 600
        self.setGeometry(100,100,window_width,window_height)

        if position=="Top-left":
            self.move(0,0)
        elif position=="Bot-center":
            screen = QtWidgets.QApplication.instance().primaryScreen()
            geometry = screen.availableGeometry()
            screen_width = geometry.width()
            screen_height = geometry.height()
            self.move((screen_width-window_width)//2, screen_height - window_height)
        else:
            screen = QtWidgets.QApplication.instance().primaryScreen()
            geometry = screen.availableGeometry()
            screen_width = geometry.width()
            screen_height = geometry.height()
            self.move(screen_width-window_width, 0)

        layout=QtWidgets.QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.getPlotItem().addLegend()
        self.plot_widget.getPlotItem().showGrid(x=True,y=True)
        layout.addWidget(self.plot_widget)
        

    def draw_plot(self, spline, mode):
        self.plot_widget.getPlotItem().clear()
        if mode=="Spline":
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="purple", width=2.0), name='Сплайн')
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine), name='Функция')
            self.plot_widget.getPlotItem().plot([],[],pen=pg.mkPen(color="blue", width=2.0), name='Разность F(x) и S(x)')

            (x_space, spline_i) = spline.calculate_spline_values()

            self.plot_widget.getPlotItem().plot(x=x_space, y=spline_i, pen=pg.mkPen(color="purple", width=2.0))
            func_i = [spline.func.func(x) for x in x_space]
            self.plot_widget.getPlotItem().plot(x=x_space, y=func_i, pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine))
            
            (x_space, _, error_i) = spline.calculate_spline_error()
            self.plot_widget.getPlotItem().plot(x_space, error_i, pen=pg.mkPen(color="blue", width=2.0))

        elif mode == "Spline derivative":
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="purple", width=2.0), name="S'(x)")
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine), name="F'(x)")
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="blue", width=2.0), name="Разность F'(x) и S'(x)")

            (x_space, spline_i) = spline.calculate_derivative_values()
            self.plot_widget.getPlotItem().plot(x_space, spline_i, pen=pg.mkPen(color="purple", width=2.0))
            func_i = [spline.func.derivative(x) for x in x_space]
            self.plot_widget.getPlotItem().plot(x_space, func_i, pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine))

            (x_space, _, error_i) = spline.calculate_derivative_error()
            self.plot_widget.getPlotItem().plot(x_space, error_i, pen=pg.mkPen(color="blue", width=2.0))

        elif mode == "Spline 2derivative":
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="purple", width=2.0), name="S'(x)")
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine), name="F'(x)")
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="blue", width=2.0), name="Разность F'(x) и S'(x)")

            (x_space, spline_i) = spline.calculate_second_derivative_values()
            self.plot_widget.getPlotItem().plot(x_space, spline_i, pen=pg.mkPen(color="purple", width=2.0))
            func_i = [spline.func.derivative_2(x) for x in x_space]
            self.plot_widget.getPlotItem().plot(x_space, func_i, pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine))

            (x_space, _, error_i) = spline.calculate_second_derivative_error()
            self.plot_widget.getPlotItem().plot(x_space, error_i, pen=pg.mkPen(color="blue", width=2.0))

class SplineApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load("Lab_Splines_GUI.ui")
        
        self.setCentralWidget(self.ui.centralWidget())
        screen = QtWidgets.QApplication.instance().primaryScreen()
        geometry = screen.availableGeometry()
        screen_width = geometry.width()
        window_height = 600
        self.setGeometry(0,0,screen_width,window_height)
        
        #reactivity
        self.ui.DrawBtn.clicked.connect(self.run_calculation)
        self.ui.comboBox_table.currentIndexChanged.connect(self.change_table)
        self.ui.comboBox_func.currentIndexChanged.connect(self.change_workspace)

        #default values 
        self.ui.plainTextEdit.setPlainText("Справка\nТестовая функция\n")
        self.ui.spinBox_n.setValue(10)
        self.ui.spinBox_N.setValue(20)

        self.spline = None

    def change_workspace(self):
        self.spline = None
        self.change_table()

        #closing plot windows
        for w in QtWidgets.QApplication.instance().topLevelWidgets():
            if isinstance(w, PlotWindow):
                w.close()

        self.ui.spinBox_n.setValue(10)
        self.ui.spinBox_N.setValue(20)

        if self.ui.comboBox_func.currentIndex() == 0:
            self.ui.plainTextEdit.setPlainText("Справка\nТестовая функция\n")
        elif self.ui.comboBox_func.currentIndex() == 1:
            self.ui.plainTextEdit.setPlainText("Справка\nФункция: sin(x+1)/x\n")
        else:
            self.ui.plainTextEdit.setPlainText("Справка\nФункция: sin(x)/(1+x^2)\n")

    def change_table(self):
        self.ui.tableWidget.clear()
        if self.ui.comboBox_table.currentIndex()==0:
            headers = ['i', 'x_{i-1}','x_i', 'a_i','b_i','c_i','d_i']
        else:
            headers = ['j','x_j', 'F(x_j)', 'S(x_j)','F(x_j-S(x_j)',"F'(x_j)","S'(x_j)","F'(x_j)-S'(x_j)",'F"(x_j)', 'S"(x_j)','F"(x_j)-S"(x_j)']
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.update_table()

    def update_table(self):
        if self.spline is None:
            return
        if self.ui.comboBox_table.currentIndex()==0:
            self.ui.tableWidget.setRowCount(self.spline.n)
            for i, data in enumerate(zip(self.spline.av[1:], self.spline.bv[1:], self.spline.cv[1:], self.spline.dv[1:])):
                x_left = self.spline.main_grid[i]
                x_right = self.spline.main_grid[i+1]
                self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i+1)))
                self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{x_left:.4e}"))
                self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{x_right:.4e}"))
                self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{data[0]:.4e}"))
                self.ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(f"{data[1]:.4e}"))
                self.ui.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(f"{data[2]:.4e}"))
                self.ui.tableWidget.setItem(i, 6, QtWidgets.QTableWidgetItem(f"{data[3]:.4e}"))
        else:
            self.ui.tableWidget.setRowCount(self.spline.N+1)

            (aux_grid, spline_vals, spline_error) = self.spline.calculate_spline_error()
            (_, derivative_vals, derivative_error) = self.spline.calculate_derivative_error()
            (_, second_derivative_vals, second_derivative_error) = self.spline.calculate_second_derivative_error()
            func = [self.spline.func.func(x) for x in aux_grid]
            d_func = [self.spline.func.derivative(x) for x in aux_grid]
            d2_func = [self.spline.func.derivative_2(x) for x in aux_grid]


            for j, (x_j, f, s, s_e, df, ds, d_e, sdf, sds, sd_e) in enumerate(zip(aux_grid, func, spline_vals, spline_error, d_func, derivative_vals, derivative_error, d2_func, second_derivative_vals, second_derivative_error)):
                self.ui.tableWidget.setItem(j, 0, QtWidgets.QTableWidgetItem(str(j)))
                self.ui.tableWidget.setItem(j, 1, QtWidgets.QTableWidgetItem(f"{x_j:.4e}"))
                self.ui.tableWidget.setItem(j, 2, QtWidgets.QTableWidgetItem(f"{f:.4e}")) 
                self.ui.tableWidget.setItem(j, 3, QtWidgets.QTableWidgetItem(f"{s:.4e}"))
                self.ui.tableWidget.setItem(j, 4, QtWidgets.QTableWidgetItem(f"{s_e:.4e}"))
                self.ui.tableWidget.setItem(j, 5, QtWidgets.QTableWidgetItem(f"{df:.4e}"))
                self.ui.tableWidget.setItem(j, 6, QtWidgets.QTableWidgetItem(f"{ds:.4e}"))
                self.ui.tableWidget.setItem(j, 7, QtWidgets.QTableWidgetItem(f"{d_e:.4e}"))
                self.ui.tableWidget.setItem(j, 8, QtWidgets.QTableWidgetItem(f"{sdf:.4e}"))
                self.ui.tableWidget.setItem(j, 9, QtWidgets.QTableWidgetItem(f"{sds:.4e}"))
                self.ui.tableWidget.setItem(j, 10, QtWidgets.QTableWidgetItem(f"{sd_e:.4e}"))

    def update_info(self):
        (aux_grid,_,spline_errors) = self.spline.calculate_spline_error()
        max_error = max(map(abs,spline_errors))
        max_error_idx = spline_errors.index(max_error)

        (_,_, derivative_errors) = self.spline.calculate_derivative_error()
        max_derivative_error = max(map(abs,derivative_errors))
        max_derivative_error_idx = derivative_errors.index(max_derivative_error)

        (_,_, second_derivative_errors) = self.spline.calculate_second_derivative_error()
        max_second_derivative_error = max(map(abs,second_derivative_errors))
        max_second_derivative_error_idx = second_derivative_errors.index(max_second_derivative_error)

        self.ui.plainTextEdit.setPlainText(
            self.ui.plainTextEdit.toPlainText() + f"Сетка сплайна: n = {self.spline.n}\nКонтрольная сетка: N = {self.spline.N}\nПогрешность сплайна на контрольной сетке\nmax|F-S| = {max_error:.4e} при x = {aux_grid[max_error_idx]:.4e}\nПргрешность производной на контрольной сетке\nmax|F'-S'| = {max_derivative_error:.4e} при x = {aux_grid[max_derivative_error_idx]:.4e}\nПогрешность второй производной на контрольной сетке\nmax|F''-S''| = {max_second_derivative_error:.4e} при x = {aux_grid[max_second_derivative_error_idx]:.4e}"
            )
       

    def run_calculation(self):
        try:
            n = self.ui.spinBox_n.value()
            N = self.ui.spinBox_N.value()
            if self.ui.comboBox_func.currentIndex() == 0:
                func = Lab2.Phi()
                a = -1
                b = 1
            elif self.ui.comboBox_func.currentIndex() == 1:
                func = Lab2.Main_func()
                a = 1
                b = Lab2.np.pi
            elif self.ui.comboBox_func.currentIndex() == 2:
                func = Lab2.Main_Func()
                a = 1
                b = Lab2.np.pi

            self.spline = Lab2.Spline(n, N, a, b, func)
            self.spline.count_coeffs()

            #Drawing
            if not hasattr(self, "plot_win_Spline"):
                self.plot_win_Spline = PlotWindow('График F(x), S(x)', position= "Top-left")
            self.plot_win_Spline.draw_plot(self.spline, mode="Spline")
            self.plot_win_Spline.show()
            if not hasattr(self, "plot_win_Spline_deriv"):
                self.plot_win_Spline_deriv = PlotWindow("График F'(x), S'(x)", position= "Bot-center")
            self.plot_win_Spline_deriv.draw_plot(self.spline, mode="Spline derivative")
            self.plot_win_Spline_deriv.show()
            if not hasattr(self, "plot_win_Spline_deriv_2"):
                self.plot_win_Spline_deriv_2 = PlotWindow('График F"(x), S"(x)', position= "Top-right")
            self.plot_win_Spline_deriv_2.draw_plot(self.spline, mode="Spline 2derivative")
            self.plot_win_Spline_deriv_2.show()

            self.update_table()

            self.update_info()


        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SplineApp()
    window.show()
    sys.exit(app.exec())
