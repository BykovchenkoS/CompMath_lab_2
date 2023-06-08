import numpy as np


def system1(x):
    return np.array([
        x[0]**2 + x[1]**2 - 4,
        x[0] - x[1] + 1
    ])


def system2(x):
    return np.array([
        x[0]**2 + x[1]**2 - 4,
        x[0]**2 - x[1]**2 - 1
    ])


def system3(x):
    return np.array([
        np.sin(x[0]) + np.cos(x[1]) - 1,
        np.exp(x[0]) - x[1] - 1
    ])


def system4(x):
    return np.array([
        x[0]**2 - 3*x[1] + 2*np.exp(x[0]-1),
        x[0]**2 + x[1]**2 - 9
    ])


def iteration_method(f, x0, e=1e-6, cnt_iter=100):
    x = x0.copy()
    n = len(x)
    iteration_table = []
    for i in range(cnt_iter):
        fx = f(x)
        dx = np.zeros((n, n))
        for j in range(n):
            dx[:, j] = (f(x + 1e-8*np.eye(n)[:, j]) - fx) / 1e-8
        x = x - np.linalg.solve(dx, fx)
        iteration_table.append([x[0], x[1], fx[0], fx[1], np.linalg.norm(fx)])
        if np.linalg.norm(fx) < e:
            return x, iteration_table
    print("Итерационный метод не сходится")
    return x, iteration_table


print("Выберите систему уравнений:")
print("1. x^2 + y^2 = 4, x - y = -1")
print("2. x^2 + y^2 = 4, x^2 - y^2 = 1")
print("3. sin(x) + cos(y) = 1, e^x - y = 1")
print("4. x^2 - 3y + 2e^(x-1) = 0,  x^2 + y^2 = 9")
system_choice = input("Введите номер системы: ")

if system_choice == '1':
    f = system1
    x0 = np.array([1, 1])
elif system_choice == '2':
    f = system2
    x0 = np.array([1, 1])
elif system_choice == '3':
    f = system3
    x0 = np.array([1, 1])
elif system_choice == '4':
    f = system4
    x0 = np.array([1, 1])
else:
    print("Неверный выбор")
    exit()


x, iteration_table = iteration_method(f, x0)

print("\nРешение:")
print(x)
print("\nТаблица итераций:")
print("{:<10} {:<10} {:<15} {:<15} {:<15}".format("x", "y", "f1", "f2", "norm(f)"))
for row in iteration_table:
    print("{:<10.6f} {:<10.6f} {:<15.6f} {:<15.6f} {:<15.6f}".format(*row))

