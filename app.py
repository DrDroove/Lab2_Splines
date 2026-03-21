import sys
from PySide6 import QtWidgets, QtUiTools, QtCore
import pyqtgraph as pg

import Lab2

class PlotWindow(QtWidgets.QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100,100,800,600)

        layout=QtWidgets.QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.getPlotItem().addLegend()
        self.plot_widget.getPlotItem().showGrid(x=True,y=True)
        layout.addWidget(self.plot_widget)

    def draw_plot(self, Spline, N, mode):
        self.plot_widget.getPlotItem().clear()
        if mode=="Spline":
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="purple", width=2.0), name='Сплайн')
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine), name='Функция')
            self.plot_widget.getPlotItem().plot([],[],pen=pg.mkPen(color="blue", width=2.0), name='Разность F(x) и S(x)')

            Spline.error_spline = []
            for i in range(1, Spline.n + 1):
                x_left = Spline.a + Spline.h * (i - 1)
                x_right = x_left + Spline.h
                x_space = Lab2.np.linspace(x_left, x_right, Spline.n)
                spline_i = [Spline.av[i] + Spline.bv[i] * (x - x_right) + Spline.cv[i] / 2 * \
                            (x - x_right) ** 2 + Spline.dv[i] / 6 * (x - x_right) ** 3 for x in x_space]
                self.plot_widget.getPlotItem().plot(x=x_space, y=spline_i, pen=pg.mkPen(color="purple", width=2.0))
                func_i = [Spline.func.func(x) for x in x_space]
                self.plot_widget.getPlotItem().plot(x=x_space, y=func_i, pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine))
                x_space = Lab2.np.linspace(x_left, x_right, N)
                spline_i = [Spline.av[i] + Spline.bv[i] * (x - x_right) + Spline.cv[i] / 2 * \
                            (x - x_right) ** 2 + Spline.dv[i] / 6 * (x - x_right) ** 3 for x in x_space]
                func_i = [Spline.func.func(x) for x in x_space]
                error_i = Lab2.np.absolute(Lab2.np.array(spline_i) - Lab2.np.array(func_i))
                self.plot_widget.getPlotItem().plot(x_space, error_i, pen=pg.mkPen(color="blue", width=2.0))
                Spline.error_spline.append(zip(x_space,func_i, spline_i, error_i))
        elif mode == "Spline derivative":
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="purple", width=2.0), name="S'(x)")
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine), name="F'(x)")
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="blue", width=2.0), name="Разность F'(x) и S'(x)")

            Spline.error_derivative = []
            for i in range(1, Spline.n + 1):
                x_left = Spline.a + Spline.h * (i - 1)
                x_right = x_left + Spline.h
                x_space = Lab2.np.linspace(x_left, x_right, Spline.n)
                spline_i = [Spline.bv[i]  + Spline.cv[i] * (x - x_right) + Spline.dv[i] / 2 * (x - x_right) ** 2 for x in x_space]
                self.plot_widget.getPlotItem().plot(x_space, spline_i, pen=pg.mkPen(color="purple", width=2.0))
                func_i = [Spline.func.derivative(x) for x in x_space]
                self.plot_widget.getPlotItem().plot(x_space, func_i, pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine))

                x_space = Lab2.np.linspace(x_left, x_right, N)
                spline_i = [Spline.bv[i]  + Spline.cv[i] * (x - x_right) + Spline.dv[i] / 2 * (x - x_right) ** 2 for x in x_space]
                func_i = [Spline.func.derivative(x) for x in x_space]
                error_i = Lab2.np.absolute(Lab2.np.array(spline_i) - Lab2.np.array(func_i))
                self.plot_widget.getPlotItem().plot(x_space, error_i, pen=pg.mkPen(color="blue", width=2.0))
                Spline.error_derivative.append(zip(x_space,func_i, spline_i, error_i))

        elif mode == "Spline 2derivative":
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="purple", width=2.0), name="S'(x)")
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine), name="F'(x)")
            self.plot_widget.getPlotItem().plot([],[], pen=pg.mkPen(color="blue", width=2.0), name="Разность F'(x) и S'(x)")

            Spline.error_derivative_2 = []
            for i in range(1, Spline.n + 1):
                x_left = Spline.a + Spline.h * (i - 1)
                x_right = x_left + Spline.h
                x_space = Lab2.np.linspace(x_left, x_right, Spline.n)
                spline_i = [Spline.cv[i] + Spline.dv[i] * (x - x_right) for x in x_space]
                self.plot_widget.getPlotItem().plot(x_space, spline_i, pen=pg.mkPen(color="purple", width=2.0))
                func_i = [Spline.func.derivative_2(x) for x in x_space]
                self.plot_widget.getPlotItem().plot(x_space, func_i, pen=pg.mkPen(color="yellow", width=2.0, style=QtCore.Qt.DashLine))


                x_space = Lab2.np.linspace(x_left, x_right, N)
                spline_i = [Spline.cv[i] + Spline.dv[i] * (x - x_right) for x in x_space]
                func_i = [Spline.func.derivative_2(x) for x in x_space]
                error_i = Lab2.np.absolute(Lab2.np.array(spline_i) - Lab2.np.array(func_i))
                self.plot_widget.getPlotItem().plot(x_space, error_i, pen=pg.mkPen(color="blue", width=2.0))
                Spline.error_derivative_2.append(zip(x_space,func_i, spline_i, error_i))


class SplineApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load("Lab_Splines_GUI.ui")
        
        self.setCentralWidget(self.ui.centralWidget())
        self.setGeometry(100,100,1200,600)
        
        self.ui.DrawBtn.clicked.connect(self.run_calculation)
        self.ui.comboBox_table.currentIndexChanged.connect(self.changeTable)

    def changeTable(self):
        self.ui.tableWidget.clear()
        if self.ui.comboBox_table.currentIndex()==0:
            headers = ['i', 'x_{i-1}','x_i', 'a_i','b_i','c_i','d_i']
        else:
            headers = ['j','x_j', 'F(x_j)', 'S(x_j)','F(x_j-S(x_j)',"F'(x_j)","S'(x_j)","F'(x_j)-S'(x_j)",'F"(x_j)', 'S"(x_j)','F"(x_j)-S"(x_j)']
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

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

            spline = Lab2.Spline(n, a, b, func)
            spline.count_coeffs()

            #Drawing
            if not hasattr(self, "plot_win_Spline"):
                self.plot_win_Spline = PlotWindow('График F(x), S(x)')
            self.plot_win_Spline.draw_plot(spline, N//n, mode="Spline")
            self.plot_win_Spline.show()
            if not hasattr(self, "plot_win_Spline_deriv"):
                self.plot_win_Spline_deriv = PlotWindow("График F'(x), S'(x)")
            self.plot_win_Spline_deriv.draw_plot(spline, N//n, mode="Spline derivative")
            self.plot_win_Spline_deriv.show()
            if not hasattr(self, "plot_win_Spline_deriv_2"):
                self.plot_win_Spline_deriv_2 = PlotWindow('График F"(x), S"(x)')
            self.plot_win_Spline_deriv_2.draw_plot(spline, N//n, mode="Spline 2derivative")
            self.plot_win_Spline_deriv_2.show()

            if self.ui.comboBox_table.currentIndex()==0:
                self.ui.tableWidget.setRowCount(spline.n)
                for i,data in enumerate(zip(spline.av, spline.bv, spline.cv, spline.dv)):
                    x_left = spline.a + spline.h * (i - 1)
                    x_right = x_left + spline.h
                    self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
                    self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(x_left)))
                    self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(x_right)))
                    self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(data[0])))
                    self.ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(str(data[1])))
                    self.ui.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(str(data[2])))
                    self.ui.tableWidget.setItem(i, 6, QtWidgets.QTableWidgetItem(str(data[3])))
            else:
                self.ui.tableWidget.setRowCount(N)
                for j, (es, ed, ed2) in enumerate(zip(spline.error_spline, spline.error_derivative, spline.error_derivative_2)):
                    x_j = spline.a + spline.h*j
                    self.ui.tableWidget.setItem(j, 0, QtWidgets.QTableWidgetItem(str(j)))
                    self.ui.tableWidget.setItem(j, 1, QtWidgets.QTableWidgetItem(str(x_j)))
                    if x_j != es[0]:
                        print("Пиздос!")
                    self.ui.tableWidget.setItem(j, 2, QtWidgets.QTableWidgetItem(str(es[1]))) 
                    self.ui.tableWidget.setItem(j, 3, QtWidgets.QTableWidgetItem(str(es[2])))
                    self.ui.tableWidget.setItem(j, 4, QtWidgets.QTableWidgetItem(str(es[3])))
                    self.ui.tableWidget.setItem(j, 5, QtWidgets.QTableWidgetItem(str(ed[1])))
                    self.ui.tableWidget.setItem(j, 6, QtWidgets.QTableWidgetItem(str(ed[2])))
                    self.ui.tableWidget.setItem(j, 7, QtWidgets.QTableWidgetItem(str(ed[3])))
                    self.ui.tableWidget.setItem(j, 8, QtWidgets.QTableWidgetItem(str(ed2[1])))
                    self.ui.tableWidget.setItem(j, 9, QtWidgets.QTableWidgetItem(str(ed2[2])))
                    self.ui.tableWidget.setItem(j, 10, QtWidgets.QTableWidgetItem(str(ed2[3])))

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SplineApp()
    window.show()
    sys.exit(app.exec())
