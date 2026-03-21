import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
import pandas as pd
        
class Phi:
    def func(self, x):
        if (-1 <= x < 0):
            return x ** 3 + 3 * x ** 2
        elif (0 <= x <= 1):
            return -x ** 3 + 3 * x ** 2
    
    def derivative(self, x):
        if (-1 <= x < 0):
            return 3 * x ** 2 + 6 * x
        elif (0 <= x <= 1):
            return (-3) * x ** 2 + 6 * x
        
    def derivative_2(self, x):
        if (-1 <= x < 0):
            return 6 * x + 6
        elif (0 <= x <= 1):
            return (-6) * x + 6
        
class Main_func:
    def func(self, x):
        return np.sin(x+1)/x
    
    def derivative(self, x):
        return (np.cos(x+1)*x-np.sin(x))/(x*x)
        
    def derivative_2(self, x):
        return (-x*x*np.sin(x+1)-2*x*np.cos(x+1)+2*np.sin(x+1))/(x*x*x)

class Main_Func:
    def func(self, x):
        return Main_func().func(x) + np.cos(10 * x)
    
    def derivative(self, x):
        return Main_func().derivative(x) - 10 * np.sin(10 * x)
        
    def derivative_2(self, x):
        return Main_func().derivative_2(x) - 100 * np.cos(10 * x)
    

class Spline:
    def __init__(self, n, a, b, func):
        self.n = n
        self.a = a
        self.b = b
        self.h = (b - a) / n
        self.av = np.zeros(n + 1)
        self.bv = np.zeros(n + 1)
        self.cv = np.zeros(n + 1)
        self.dv = np.zeros(n + 1)
        self.func = func
        
            
        for i in range(n + 1):
            self.av[i] = func.func(self.a + self.h * i)
            
    def count_coeffs(self):
        alpha = np.zeros(self.n) 
        beta = np.zeros(self.n)
        
        for i in range (1, self.n):
            alpha[i] = -self.h / (self.h * alpha[i - 1] + 4 * self.h)
            x = self.a + self.h * i
            x_prev = x - self.h
            x_next = x + self.h
            Fi = 6 * (self.func.func(x_next) - 2 * self.func.func(x) + self.func.func(x_prev)) / self.h
            beta[i] = (Fi - self.h * beta[i - 1]) / (self.h * alpha[i - 1] + 4 * self.h)
            
        for i in reversed(range(1, self.n)):
            self.cv[i] = alpha[i] * self.cv[i + 1] + beta[i]
        
        for i in range (1, self.n + 1):
            self.dv[i] = (self.cv[i] - self.cv[i - 1]) / self.h
            self.bv[i] = (self.av[i] - self.av[i - 1]) / self.h + self.cv[i] * self.h / 3 + self.cv[i - 1] * self.h / 6      
            
    def plot_spline(self, ticks):
        for i in range(1, self.n + 1):
            x_left = self.a + self.h * (i - 1)
            x_right = x_left + self.h
            x_space = np.linspace(x_left, x_right, ticks)
            spline_i = [self.av[i] + self.bv[i] * (x - x_right) + self.cv[i] / 2 * \
                        (x - x_right) ** 2 + self.dv[i] / 6 * (x - x_right) ** 3 for x in x_space]
            plt.plot(x_space, spline_i, color="purple", linewidth=1.0)
            func_i = [self.func.func(x) for x in x_space]
            plt.plot(x_space, func_i, color="yellow", alpha=0.5)
            
        xticks = [self.a + i * self.h for i in range(self.n + 1)]
        plt.xticks(xticks if n < 10 else None)
        plt.grid()
        plt.title("F(x) vs S(x)")
        plt.show()
    
    def plot_derivative(self, ticks):
        for i in range(1, self.n + 1):
            x_left = self.a + self.h * (i - 1)
            x_right = x_left + self.h
            x_space = np.linspace(x_left, x_right, ticks)
            spline_i = [self.bv[i]  + self.cv[i] * (x - x_right) + self.dv[i] / 2 * (x - x_right) ** 2 for x in x_space]
            plt.plot(x_space, spline_i, color="purple", linewidth=1.0)
            func_i = [self.func.derivative(x) for x in x_space]
            plt.plot(x_space, func_i, color="yellow", alpha=0.5)
            
        xticks = [self.a + i * self.h for i in range(self.n + 1)]
        plt.xticks(xticks if n < 10 else None)
        plt.grid()
        plt.title("F'(x) vs S'(x)")
        plt.show()
        
    def plot_derivative_2(self, ticks):
        for i in range(1, self.n + 1):
            x_left = self.a + self.h * (i - 1)
            x_right = x_left + self.h
            x_space = np.linspace(x_left, x_right, ticks)
            spline_i = [self.cv[i] + self.dv[i] * (x - x_right) for x in x_space]
            plt.plot(x_space, spline_i, color="purple", linewidth=1.0)
            func_i = [self.func.derivative_2(x) for x in x_space]
            plt.plot(x_space, func_i, color="yellow", alpha=0.5)
            
        xticks = [self.a + i * self.h for i in range(self.n + 1)]
        plt.xticks(xticks if n < 10 else None)
        plt.grid()
        plt.title("F''(x) vs S''(x)")
        plt.show()
        
    def coeffs_to_table(self):
        grid = [self.a + i * self.h for i in range(self.n + 1)]
        coeffs = {'Xi-1': grid[0:-1], 'Xi': grid[1:], 'a': self.av[1:], \
                  'b': self.bv[1:], 'c': self.cv[1:], 'd': self.dv[1:]}
        self.df_coeffs = pd.DataFrame(coeffs)
       
    def plot_error_spline(self, ticks):
        self.max_error_spline = []
        for i in range(1, self.n + 1):
            x_left = self.a + self.h * (i - 1)
            x_right = x_left + self.h
            x_space = np.linspace(x_left, x_right, ticks)
            spline_i = [self.av[i] + self.bv[i] * (x - x_right) + self.cv[i] / 2 * \
                        (x - x_right) ** 2 + self.dv[i] / 6 * (x - x_right) ** 3 for x in x_space]
            func_i = [self.func.func(x) for x in x_space]
            error_i = np.absolute(np.array(spline_i) - np.array(func_i))
            plt.plot(x_space, error_i, color="purple")
            self.max_error_spline.append(np.max(error_i))
            
        xticks = [self.a + i * self.h for i in range(self.n + 1)]
        plt.xticks(xticks if n < 10 else None)
        plt.grid()
        plt.title("Погрешность |F(x) - S(x)|")
        plt.show()
        
    def plot_error_derivative(self, ticks):
        self.max_error_derivative = []
        for i in range(1, self.n + 1):
            x_left = self.a + self.h * (i - 1)
            x_right = x_left + self.h
            x_space = np.linspace(x_left, x_right, ticks)
            spline_i = [self.bv[i]  + self.cv[i] * (x - x_right) + self.dv[i] / 2 * (x - x_right) ** 2 for x in x_space]
            func_i = [self.func.derivative(x) for x in x_space]
            error_i = np.absolute(np.array(spline_i) - np.array(func_i))
            plt.plot(x_space, error_i, color="purple")
            self.max_error_derivative.append(np.max(error_i))
            
        xticks = [self.a + i * self.h for i in range(self.n + 1)]
        plt.xticks(xticks if n < 10 else None)
        plt.grid()
        plt.title("Погрешность |F'(x) - S'(x)|")
        plt.show()
        
    def plot_error_derivative_2(self, ticks):
        self.max_error_derivative_2 = []
        for i in range(1, self.n + 1):
            x_left = self.a + self.h * (i - 1)
            x_right = x_left + self.h
            x_space = np.linspace(x_left, x_right, ticks)
            spline_i = [self.cv[i] + self.dv[i] * (x - x_right) for x in x_space]
            func_i = [self.func.derivative_2(x) for x in x_space]
            error_i = np.absolute(np.array(spline_i) - np.array(func_i))
            plt.plot(x_space, error_i, color="purple")
            self.max_error_derivative_2.append(np.max(error_i))
            
        xticks = [self.a + i * self.h for i in range(self.n + 1)]
        plt.xticks(xticks if n < 10 else None)
        plt.grid()
        plt.title("Погрешность |F''(x) - S''(x)|")
        plt.show()

    def print_results(self, ticks):
        self.plot_spline(ticks)
        self.plot_derivative(ticks)
        self.plot_derivative_2(ticks)
        self.plot_error_spline(ticks)
        self.plot_error_derivative(ticks)
        self.plot_error_derivative_2(ticks)
        
        self.coeffs_to_table()
        np.set_printoptions(formatter={'float_kind':'{:e}'.format})
        print(f"Ceтка сплайна: n = {self.n}")
        print(f"Контрольная сетка: n = {self.n * 4}")
        print(f"max|F(x) - S(x)| = {np.array(self.max_error_spline).max():e}")
        print(f"max|F'(x) - S'(x)| = {np.array(self.max_error_derivative).max():e}")
        print(f"max|F''(x) - S''(x)| = {np.array(self.max_error_derivative_2).max():e}")
        
        
# n = 50
# ifTest = False # Тестовая - True, Основные - False
# func = Main_func() # Тестовая - Phi, Основные - Main_func и Main_Func

# a, b = 1, np.pi # 1, pi


# if (ifTest):
#     func = Phi()
#     a, b = -1, 1
    
# eps = 1e-8
# spline = Spline(n, a, b, func)
# spline.count_coeffs()
# spline.print_results(150)