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
    def __init__(self, n, N, a, b, func):
        self.n = n
        self.N = N
        self.a = a
        self.b = b
        self.h = (b - a) / n
        self.h_aux = (b - a) / N
        self.av = np.zeros(n + 1)
        self.bv = np.zeros(n + 1)
        self.cv = np.zeros(n + 1)
        self.dv = np.zeros(n + 1)
        self.func = func
        
        self.main_grid = []
        self.auxilary_grid = []
            
        for i in range(n + 1):
            xi = self.a + self.h * i
            self.av[i] = func.func(xi)
            self.main_grid.append(xi)
        
        for i in range(N+1):
            xi = self.a + self.h_aux * i
            self.auxilary_grid.append(xi)
            
    def count_coeffs(self):
        alpha = np.zeros(self.n) 
        beta = np.zeros(self.n)
        
        for i in range (1, self.n):
            alpha[i] = -self.h / (self.h * alpha[i - 1] + 4 * self.h)
            x = self.main_grid[i]
            x_prev = self.main_grid[i-1]
            x_next = self.main_grid[i+1]
            Fi = 6 * (self.func.func(x_next) - 2 * self.func.func(x) + self.func.func(x_prev)) / self.h
            beta[i] = (Fi - self.h * beta[i - 1]) / (self.h * alpha[i - 1] + 4 * self.h)
            
        for i in reversed(range(1, self.n)):
            self.cv[i] = alpha[i] * self.cv[i + 1] + beta[i]
        
        for i in range (1, self.n + 1):
            self.dv[i] = (self.cv[i] - self.cv[i - 1]) / self.h
            self.bv[i] = (self.av[i] - self.av[i - 1]) / self.h + self.cv[i] * self.h / 3 + self.cv[i - 1] * self.h / 6 

    def calculate_spline_values(self):
        if hasattr(self, 'spline_values') and hasattr(self, 'visualizer_spline_space'):
            return (self.visualizer_spline_space, self.spline_values)
        result = []
        x_space = []
        for i in range(1, self.n + 1):
            x_left = self.main_grid[i-1]
            x_right = self.main_grid[i]
            endpoint = (i==self.n)
            x_local_space = np.linspace(x_left, x_right, self.n, endpoint=endpoint)
            spline_i = [self.av[i] + self.bv[i] * (x - x_right) + self.cv[i] / 2 * \
                        (x - x_right) ** 2 + self.dv[i] / 6 * (x - x_right) ** 3 for x in x_local_space]
            result.extend(spline_i)
            x_space.extend(x_local_space)

        self.spline_values = result
        self.visualizer_spline_space = x_space
        return (x_space, result)
    
    def calculate_derivative_values(self):
        if hasattr(self, 'derivative_values') and hasattr(self, 'visualizer_derivative_space'):
            return (self.visualizer_derivative_space, self.derivative_values)
        result = []
        x_space = []
        for i in range(1, self.n + 1):
            x_left = self.main_grid[i-1]
            x_right = self.main_grid[i]
            endpoint = (i==self.n)
            x_local_space = np.linspace(x_left, x_right, self.n, endpoint=endpoint)
            spline_i = [self.bv[i]  + self.cv[i] * (x - x_right) + self.dv[i] / 2 * (x - x_right) ** 2 for x in x_local_space]
            result.extend(spline_i)
            x_space.extend(x_local_space)

        self.derivative_values = result
        self.visualizer_derivative_space = x_space
        return (x_space, result)
    
    def calculate_second_derivative_values(self):
        if hasattr(self, 'second_derivative_values') and hasattr(self, 'visualizer_second_derivative_space'):
            return (self.visualizer_second_derivative_space, self.second_derivative_values)
        result = []
        x_space = []
        for i in range(1, self.n + 1):
            x_left = self.main_grid[i-1]
            x_right = self.main_grid[i]
            endpoint = (i==self.n)
            x_local_space = np.linspace(x_left, x_right, self.n, endpoint=endpoint)
            spline_i = [self.cv[i] + self.dv[i] * (x - x_right) for x in x_local_space]
            result.extend(spline_i)
            x_space.extend(x_local_space)

        self.second_derivative_values = result
        self.visualizer_second_derivative_space = x_space
        return (x_space, result)
    
    def calculate_spline_error(self):
        if hasattr(self, 'spline_errors_values') and hasattr(self, 'visualizer_spline_errors_space') and hasattr(self, 'spline_values_at_auxilary_grid'):
            return (self.visualizer_spline_errors_space, self.spline_values_at_auxilary_grid, self.spline_errors_values)
        errors = []
        indicies = np.searchsorted(self.auxilary_grid, self.main_grid)
        self.spline_values_at_auxilary_grid = []
        for i in range(1, self.n+1):
            x_right = self.main_grid[i]
            x_segment = self.auxilary_grid[indicies[i-1]:indicies[i]]
            spline_i = [self.av[i] + self.bv[i] * (x - x_right) + self.cv[i] / 2 * \
                        (x - x_right) ** 2 + self.dv[i] / 6 * (x - x_right) ** 3 for x in x_segment]
            func_i = [self.func.func(x) for x in x_segment]
            error_i = np.absolute(np.array(spline_i) - np.array(func_i))
            
            self.spline_values_at_auxilary_grid.extend(spline_i)
            errors.extend(error_i)

        spline_last = lambda x: self.av[-1] + self.bv[-1] * (x - x_right) + self.cv[-1] / 2 * \
                        (x - x_right) ** 2 + self.dv[-1] / 6 * (x - x_right) ** 3
        errors.append(np.absolute(spline_last(self.auxilary_grid[-1])-self.func.func(self.auxilary_grid[-1])))
        self.spline_values_at_auxilary_grid.append(spline_last(self.auxilary_grid[-1]))

        self.spline_errors_values = errors
        self.visualizer_spline_errors_space = self.auxilary_grid
        

        return (self.auxilary_grid, self.spline_values_at_auxilary_grid, errors)
    
    def calculate_derivative_error(self):
        if hasattr(self, 'derivative_errors_values') and hasattr(self, 'visualizer_derivative_errors_space') and hasattr(self, 'derivative_values_at_auxilary_grid'):
            return (self.visualizer_derivative_errors_space, self.derivative_values_at_auxilary_grid, self.derivative_errors_values)
        errors = []
        indicies = np.searchsorted(self.auxilary_grid, self.main_grid)
        self.derivative_values_at_auxilary_grid = []
        for i in range(1, self.n+1):
            x_right = self.main_grid[i]
            x_segment = self.auxilary_grid[indicies[i-1]:indicies[i]]
            derivative_i = [self.bv[i]  + self.cv[i] * (x - x_right) + self.dv[i] / 2 * (x - x_right) ** 2 for x in x_segment]
            func_i = [self.func.derivative(x) for x in x_segment]
            error_i = np.absolute(np.array(derivative_i) - np.array(func_i))

            errors.extend(error_i)
            self.derivative_values_at_auxilary_grid.extend(derivative_i)

        derivative_last = lambda x: self.bv[i]  + self.cv[i] * (x - x_right) + self.dv[i] / 2 * (x - x_right) ** 2

        errors.append(np.absolute(derivative_last(self.auxilary_grid[-1])-self.func.derivative(self.auxilary_grid[-1])))
        self.derivative_values_at_auxilary_grid.append(derivative_last(self.auxilary_grid[-1]))

        self.derivative_errors_values = errors
        self.visualizer_derivative_errors_space = self.auxilary_grid

        return (self.auxilary_grid, self.derivative_values_at_auxilary_grid, errors)

    def calculate_second_derivative_error(self):
        if hasattr(self, 'second_derivative_errors_values') and hasattr(self, 'visualizer_second_derivative_errors_space') and hasattr(self, 'second_derivative_values_at_auxilary_grid'):
            return (self.visualizer_second_derivative_errors_space, self.second_derivative_values_at_auxilary_grid, self.second_derivative_errors_values)
        errors = []
        indicies = np.searchsorted(self.auxilary_grid, self.main_grid)
        self.second_derivative_values_at_auxilary_grid = []
        for i in range(1, self.n+1):
            x_right = self.main_grid[i]
            x_segment = self.auxilary_grid[indicies[i-1]:indicies[i]]
            second_derivative_i = [self.cv[i] + self.dv[i] * (x - x_right) for x in x_segment]
            func_i = [self.func.derivative_2(x) for x in x_segment]
            error_i = np.absolute(np.array(second_derivative_i) - np.array(func_i))

            errors.extend(error_i)
            self.second_derivative_values_at_auxilary_grid.extend(second_derivative_i)


        second_derivative_last = lambda x: self.cv[i] + self.dv[i] * (x - x_right)

        errors.append(np.absolute(second_derivative_last(self.auxilary_grid[-1])-self.func.derivative_2(self.auxilary_grid[-1])))
        self.second_derivative_values_at_auxilary_grid.append(second_derivative_last(self.auxilary_grid[-1]))

        self.second_derivative_errors_values = errors
        self.visualizer_second_derivative_errors_space = self.auxilary_grid

        return (self.auxilary_grid, self.second_derivative_values_at_auxilary_grid, errors)
            
