import numpy as np


def chord_method(a, b, f, e, cnt_iter=100):

    if f(b) * derivative(2, a, f) < 0:
        point_0 = a
        x = b
    elif f(a) * derivative(2, a, f) < 0:
        point_0 = b
        x = a
    else:
        x = a - (b - a) / (f(b) - f(a)) * f(a)
        point_0 = None

    x_flag = x + 2*e
    table_iter = [['a', 'b', 'x', 'f(a)', 'f(b)', 'f(x)', 'd'], [a, b, x, f(a), f(b), f(x), abs(x - x_flag)]]
    current_cnt = 0

    while current_cnt < cnt_iter and abs(x - x_flag) > e:
        if point_0 is None:
            if f(a) * f(x) < 0:
                b = x
            else:
                a = x
            x, x_flag = a - (b - a) / (f(b) - f(a)) * f(a), x
            table_iter.append([a, b, x, f(a), f(b), f(x), abs(x - x_flag)])
        else:
            x, x_flag = x - (point_0 - x) / (f(point_0) - f(x)) * f(x), x
            if point_0 == a:
                table_iter.append([point_0, x, x, f(point_0), f(x), f(x), abs(x - x_flag)])
            else:
                table_iter.append([x, point_0, x, f(x), f(point_0), f(x), abs(x - x_flag)])
        current_cnt += 1

    return x, f(x), current_cnt, table_iter


def iteration_method(x0, f, e, cnt_iter=100):
    def g(g_x):
        return g_x + (-1 / derivative(1, g_x, f)) * f(g_x)

    x = g(x0)
    table_iter = [['x0', 'f(x0)', 'x', 'g(x0)', 'd'], [x0, f(x0), x, g(x0), abs(x - x0)]]

    current_cnt = 0
    while abs(x - x0) > e and current_cnt < cnt_iter:
        if derivative(1, x, g) >= 1:
            return None
        x0, x = x, g(x)
        table_iter.append([x0, f(x0), x, g(x0), abs(x - x0)])
        current_cnt += 1

    return x, f(x), current_cnt, table_iter


def choose_func(function_num):
    if function_num == '1':
        return np.linspace(-12, 12), lambda x: x ** 3 + 2 * x - 1
    elif function_num == '2':
        return np.linspace(-1, 1.1), lambda x: np.sin(x) + 0.1
    else:
        return None


def derivative(order, x, f):
    h = 1e-8

    if order == 1:
        return (f(x + h) - f(x)) / h
    elif order > 0:
        return (derivative(order - 1, x + h, f) - derivative(order - 1, x, f)) / h
    return None


def get_func():
    print("\nВыберите f(x)")
    print(" 1: x^3 + 2x - 1")
    print(" 2: sin(x) + 0.1")
    my_function = choose_func(input("\nФункция: "))

    my_function_dict = {}

    while my_function is None:
        print("Выберите f(x) ->")
        my_function = choose_func(input("\nФункция: "))

    x, function = my_function
    my_function_dict['function'] = function

    while True:
        try:
            a, b = map(float, input("Введите границы интервала для Метода хорд: ").split())
            if a > b:
                a, b = b, a
            elif a == b:
                raise ArithmeticError
            elif function(a) * function(b) > 0:
                raise AttributeError
            break
        except ValueError:
            print("Границы интервала должны быть числами, введенными через пробел.")
        except ArithmeticError:
            print("Границы интервала не могут быть равны.")
        except AttributeError:
            print("Интервал содержит ноль или несколько корней.")
    my_function_dict['a'] = a
    my_function_dict['b'] = b

    while True:
        try:
            x0 = float(input("\nВведите начальное приближение для Метода простой итерации: "))
            break
        except ValueError:
            print("Введите число!")
    my_function_dict['x0'] = x0

    while True:
        try:
            error = float(input("\nВведите погрешность вычисления: "))
            if error <= 0:
                raise ArithmeticError
            break
        except (ValueError, ArithmeticError):
            print("Число должно быть положительным!")
    my_function_dict['error'] = error

    return my_function_dict


def print_table(table):
    for j in range(len(table[3][0])):
        print('%10s' % table[3][0][j], end='')
    print()

    for i in range(1, len(table[3])):
        for j in range(len(table[3][i])):
            print('%10.5f' % table[3][i][j], end='')

        print()


function = get_func()
try:
    answer_1 = chord_method(function['a'], function['b'], function['function'], function['error'])
    answer_2 = iteration_method(function['x0'], function['function'], function['error'])

    print(f"\nКорень уравнения Методом хорд: {answer_1[0]}")
    print(f"Значение функции: {answer_1[1]}")
    print(f"Число итераций: {answer_1[2]}")
    print("Таблица итераций для Метода хорд: ")
    print_table(answer_1)

    print(f"\nКорень уравнения Методом простой итерации: {answer_2[0]}")
    print(f"Значение функции: {answer_2[1]}")
    print(f"Число итераций: {answer_2[2]}")
    print("Таблица итераций для Метода простой итерации: ")
    print_table(answer_2)

    print('\nРазница между результатами при использовании Метода хорд и Метода простой итерации: ',
          abs(answer_2[0] - answer_1[1]))

except ValueError:
    pass

