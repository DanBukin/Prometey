"""
Модуль построения графиков с использованием matplotlib.

Включает:
- Стандартные графики (`plot_graph`, `plot_graph_2`, `plot_graph_3`),
- Визуализацию сечения сопла с рёбрами охлаждения (`print_rebra`),
- Отображение результатов расчёта тепловых потоков.

Все графики стилизованы в едином стиле (Times New Roman, подписи, сетки).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
def plot_graph(x, y, xlabel='Ось X', ylabel='Ось Y', title='График',label1='Данные'):
    """
    Рисует график по двум массивам X и Y.

    Параметры:
    x (list или numpy.array): Массив значений по оси X.
    y (list или numpy.array): Массив значений по оси Y.
    xlabel (str): Название оси X.
    ylabel (str): Название оси Y.
    title (str): Название графика.
    """
    # Установка шрифта Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 12
    # Создание графика
    plt.figure(figsize=(14, 6)) # Ширина и высота
    plt.plot(x, y, linestyle='-', color='black', label=label1)

    # Настройка осей
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    fig = plt.gcf()  # get current figure
    fig.canvas.manager.set_window_title(title)

    # Вычисление отступов
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)

    # Установка отступов
    # plt.xlim(x_min, x_max + 1.1)
    # plt.ylim(y_min - 1.1, y_max + 1.1)
    # Добавление основной сетки
    plt.grid(True)

    # Добавление дополнительной сетки
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    # Добавление сетки и легенды
    plt.grid(True)
    plt.legend()
    # Показ графика
    # plt.show()
def plot_graph_2(x, y,y_2,xlabel='Ось X', ylabel='Ось Y', title='График',label1='Данные',label2='Данные'):
    """
    Рисует график по двум массивам X и Y.

    Параметры:
    x (list или numpy.array): Массив значений по оси X.
    y (list или numpy.array): Массив значений по оси Y.
    xlabel (str): Название оси X.
    ylabel (str): Название оси Y.
    title (str): Название графика.
    """
    # Создание графика
    plt.figure(figsize=(14, 6)) # Ширина и высота
    plt.plot(x, y, linestyle='-', color='black', label=label1)
    plt.plot(x, y_2, linestyle='-', color='black', label=label2)

    # Настройка осей
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    fig = plt.gcf()  # get current figure
    fig.canvas.manager.set_window_title(title)

    # Вычисление отступов
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)

    # Установка отступов
    # plt.xlim(x_min, x_max + 1.1)
    # plt.ylim(y_min - 1.1, y_max + 1.1)

    # Добавление сетки и легенды
    plt.grid(True)
    plt.legend()
def plot_graph_3(x, y,y_2,y_3,xlabel='X, мм', ylabel='q, МВт/м2', title='Тепловые потоки'):

    # Создание графика
    plt.figure(figsize=(14, 6)) # Ширина и высота
    plt.plot(x, y, linestyle='-', color='red', label='Лучистый тепловой поток')
    plt.plot(x, y_2, linestyle='-', color='blue', label='Конвективный тепловой поток')
    plt.plot(x, y_3, linestyle='-', color='black', label='Суммарный тепловой поток')

    # Настройка осей
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    fig = plt.gcf()  # get current figure
    fig.canvas.manager.set_window_title(title)

    # Вычисление отступов
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)

    # Установка отступов
    # plt.xlim(x_min, x_max + 1.1)
    # plt.ylim(y_min - 1.1, y_max + 1.1)
    # Добавление основной сетки
    plt.grid(True)

    # Добавление дополнительной сетки
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    # Добавление сетки и легенды
    plt.grid(True)
    plt.legend()
def print_rebra(delta_st,delta_reb,delta_nar_st,h,n,D,index):
    delta_st=1000*delta_st
    delta_reb=1000*delta_reb
    delta_nar_st=1000*delta_nar_st
    h=1000*h
    n=n[index]
    D=1000*D[index]
    R_max = 0.5 * D + delta_st + h + delta_nar_st
    # Настройка графика
    fig, ax = plt.subplots(figsize=(14, 6))
    if index==0:
        fig.canvas.manager.set_window_title("Рубашка охлаждения (сечение в КС)")
    else:
        fig.canvas.manager.set_window_title("Рубашка охлаждения (сечение в критической точке)")
    ax.set_aspect('equal')
    fig.patch.set_facecolor('white')  # Цвет фона окна
    ax.set_facecolor('white')  # Цвет области графика

    circle = patches.Circle((0, 0), 0.5 * D + delta_st + h + delta_nar_st, hatch='/',facecolor='white', edgecolor='black')
    ax.add_patch(circle)
    circle = patches.Circle((0, 0), 0.5 * D + delta_st + h, facecolor='white', edgecolor='black')
    ax.add_patch(circle)
    circle = patches.Circle((0, 0), 0.5 * D + delta_st, hatch='\\',facecolor='white', edgecolor='black')
    ax.add_patch(circle)
    circle = patches.Circle((0, 0), D / 2, facecolor='white', edgecolor='black')
    ax.add_patch(circle)


    # Описание одного ребра до поворота
    base_rib = np.array([
        [-0.5 * delta_reb, 0.5 * D + delta_st],
        [-0.5 * delta_reb, 0.5 * D + delta_st + h],
        [0.5 * delta_reb, 0.5 * D + delta_st + h],
        [0.5 * delta_reb, 0.5 * D + delta_st]
    ])

    for i in range(n):
        theta = 2 * np.pi * i / n
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        rotated_rib = base_rib @ rotation_matrix.T
        rib_patch = patches.Polygon(
            rotated_rib,
            facecolor='none',  # Убираем заливку
            edgecolor='black',
            hatch='\\'  # Штриховка: диагональная
        )
        ax.add_patch(rib_patch)

    ax.tick_params(colors='black', labelsize=10)  # Цвет меток делений
    ax.set_xlim(-5*delta_reb, 5*delta_reb)
    ax.set_ylim(D*0.5-1, R_max+1)
    # Включаем сетку — как на миллиметровке
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
    ax.minorticks_on()  # включаем второстепенные деления
    ax.tick_params(which='both', direction='in', length=4, color='gray')
    # Настройка осей
    plt.xlabel('мм')
    plt.ylabel('мм')
    if index == 0:
        plt.title('Рубашка охлаждения (сечение в КС)')
    else:
        plt.title('Рубашка охлаждения (сечение в критической точке)')
