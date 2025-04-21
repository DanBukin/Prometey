"""
Модуль визуализации результатов внутри пользовательского интерфейса.

Содержит:
- Встроенную отрисовку графиков в окна `customtkinter`,
- Отображение геометрии сопла, распределения рёбер, тепловых потоков,
- Установку пользовательских шрифтов и цветовой схемы.

Интеграция matplotlib и tkinter в единую визуальную оболочку.
"""

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import AutoMinorLocator
from matplotlib.font_manager import FontProperties
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
import os
from ctypes import windll
from prometey_graph import *

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", FR_PRIVATE, 0)
else:
    pass

font0 = ("Futura PT Book", 18)  # Настройка пользовательского шрифта 1
font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 2
font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 3
font_path = 'data/ofont.ru_Futura PT.ttf'
font_props = font_manager.FontProperties(fname=font_path)
if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", 0x10, 0)
else:
    pass
custom_font = FontProperties(fname='data/ofont.ru_Futura PT.ttf', size=16)
formatter = FuncFormatter(lambda x, _: f"{x:.2f}")
def print_nozzle_window(X,Y,frame,x=2,y=2):
    fig = Figure(figsize=(9,9), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_facecolor('#242424') #242424#00DF7F
    ax.plot(X,Y, color='#00DF7F')
    ax.plot(X, [0]*len(X), color='white')
    ax.set_title("Сопло", fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('X, м', fontsize=16, fontproperties=font_props, color='white',)
    ax.set_ylabel("R, м", fontsize=16, rotation='horizontal',fontproperties=font_props, color='white', labelpad=60, va='bottom')
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.2f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.2f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#242424')
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x,y=y)

    canvas.draw()
def print_cooling_fins(delta_st,delta_reb,delta_nar_st,h,n,D,index, x,y, title, frame):
    delta_st = 1000 * delta_st
    delta_reb = 1000 * delta_reb
    delta_nar_st = 1000 * delta_nar_st
    h = 1000 * h
    n = n[index]
    D = 1000 * D[index]
    R_max = 0.5 * D + delta_st + h + delta_nar_st

    fig = Figure(figsize=(7.6, 7.6), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_facecolor('#242424')  #242424 #00DF7F

    circle = patches.Circle((0, 0), 0.5 * D + delta_st + h + delta_nar_st, hatch='/', facecolor='#242424',
                            edgecolor='#00DF7F')
    ax.add_patch(circle)
    circle = patches.Circle((0, 0), 0.5 * D + delta_st + h, facecolor='#242424', edgecolor='#00DF7F')
    ax.add_patch(circle)
    circle = patches.Circle((0, 0), 0.5 * D + delta_st, hatch='\\', facecolor='#242424', edgecolor='#00DF7F')
    ax.add_patch(circle)
    circle = patches.Circle((0, 0), D / 2, facecolor='#242424', edgecolor='#00DF7F')
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
            edgecolor='#00DF7F',
            hatch='\\'  # Штриховка: диагональная
        )
        ax.add_patch(rib_patch)

    ax.set_xlim(-5 * delta_reb, 5 * delta_reb)
    ax.set_ylim(D * 0.5 - 1, R_max + 1)

    ax.set_title(title, fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('X, м', fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel("R, м", fontsize=16, rotation='horizontal', fontproperties=font_props, color='white', labelpad=60,
                  va='bottom')
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.0f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#242424')
    fig.subplots_adjust(left=0.15, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x, y=y)
def print_cooling_fins_array(x,n,y,frame,x_0=2,y_0=370):
    fig = Figure(figsize=(15,8), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#242424')  # 242424#00DF7F
    ax.plot(x,n, color='#00DF7F')
    ax.set_title("Распределение рёбер по соплу", fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('X, м', fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel("n", fontsize=16, rotation='horizontal', fontproperties=font_props, color='white', labelpad=60,
                  va='bottom')
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.2f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#242424')
    fig.subplots_adjust(left=0.05, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x_0, y=y_0)

    canvas.draw()
def print_heat_flows(q_k,q_l,q_sum,x,frame,x_0=2,y_0=10):
    fig = Figure(figsize=(15,8), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#242424')  # 242424#00DF7F
    ax.plot(x,q_k, color='#1D6D45', label='q_к, МВт/м²')
    ax.plot(x, q_l, color='#9EFFD5', label='q_л, МВт/м²')
    ax.plot(x, q_sum, color='#00DF7F', label='q_сум, МВт/м²')
    ax.legend(loc='center right')
    ax.set_title("Тепловые потоки", fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('X, м', fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel("n", fontsize=16, rotation='horizontal', fontproperties=font_props, color='white', labelpad=60,
                  va='bottom')
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.2f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#242424')
    fig.subplots_adjust(left=0.05, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x_0, y=y_0)

    canvas.draw()
def print_temp_cooler(T,x,frame,x_0=2,y_0=10):
    fig = Figure(figsize=(15,8), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#242424')  # 242424#00DF7F
    ax.plot(x,T, color='#00DF7F')
    ax.set_title("Температура охладителя", fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('X, м', fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel("n", fontsize=16, rotation='horizontal', fontproperties=font_props, color='white', labelpad=60,
                  va='bottom')
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.2f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#242424')
    fig.subplots_adjust(left=0.05, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x_0, y=y_0)

    canvas.draw()
def wall_temperatures(T_st,T_ohl,x,frame,x_0=2,y_0=10):
    fig = Figure(figsize=(15, 8), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#242424')  # 242424#00DF7F
    ax.plot(x, T_st, color='#9EFFD5', label='Т_ст_газа, К')
    ax.plot(x, T_ohl, color='#00DF7F', label='Т_ст_охл, К')
    ax.legend(loc='center right')
    ax.set_title("Температуры стенки", fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('X, м', fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel("n", fontsize=16, rotation='horizontal', fontproperties=font_props, color='white', labelpad=60,
                  va='bottom')
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.2f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#242424')
    fig.subplots_adjust(left=0.05, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x_0, y=y_0)

    canvas.draw()
def print_local_pressure_losses(delta_p_0,x,frame,x_0,y_0,var):
    if var==2:
        delta_p=[]
        for p in delta_p_0:
            delta_p.append(p/1e6)
    else:
        delta_p=delta_p_0
    fig = Figure(figsize=(15, 8), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#242424')  # 242424#00DF7F
    ax.plot(x, delta_p, color='#00DF7F')
    if var == 2:
        ax.set_title("Потери по тракту охлаждения (итоговые), МПа", fontproperties=custom_font)
    else:
        ax.set_title("Потери по тракту охлаждения (локальные), Па", fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('X, м', fontsize=16, fontproperties=font_props, color='white', )
    if var == 2:
        ax.set_ylabel("МПа", fontsize=16, rotation='horizontal', fontproperties=font_props, color='white', labelpad=60,
                      va='bottom')
    else:
        ax.set_ylabel("Па", fontsize=16, rotation='horizontal', fontproperties=font_props, color='white', labelpad=60,
                      va='bottom')
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.2f}" for x in ax.get_xticks()], fontproperties=font_props)
    if var == 2:
        ax.set_yticklabels([f"{x:.2f}" for x in ax.get_yticks()], fontproperties=font_props)
    else:
        ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=16)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#242424')
    fig.subplots_adjust(left=0.05, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x_0, y=y_0)

    canvas.draw()
def print_all_images(X,Y,n_r_array,delta_st,delta_reb,delta_st_nar,h,D,q_l,q_kon,q_sum,T_ohl,T_st_g,T_st_ohl,delta_p,p_itog):
    plot_graph(X, Y, 'X, м', 'R, м', 'Сопло', 'Сопло')  # Визуализация Сопла
    plot_graph(X, n_r_array, 'X, мм', 'n', 'Количество рёбер', 'Рёбра')  # Визуализация n_r_array
    print_rebra(delta_st, delta_reb, delta_st_nar, h, n_r_array, D, 0)
    print_rebra(delta_st, delta_reb, delta_st_nar, h, n_r_array, D, Y.index(min(Y)))
    plot_graph_3(X, q_l, q_kon, q_sum)
    plot_graph(X, T_ohl, 'X, мм', 'T_охл, К', 'Температура охладителя',
               'Температура охладителя, К')  # Визуализация n_r_array
    plot_graph(X, T_st_g, 'м', 'T, К', 'Tемпература стенки со стороны газа',
               'Tемпература стенки со стороны газа')  # Визуализация n_r_array
    plot_graph(X, T_st_ohl, 'X, мм', 'T, К', 'Tемпература стенки со стороны охладителя',
               'Tемпература стенки со стороны охладителя')  # Визуализация n_r_array
    plot_graph(X, delta_p, 'X, мм', 'p, Па', 'Потери давления', 'Потери давления')  # Визуализация n_r_array
    plot_graph(X, p_itog, 'X, м', 'р, Па', 'Потери давления (относительно входного)',
               'Потери давления (относительно входного)')  # Визуализация Сопла
    plt.show()