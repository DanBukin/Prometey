"""
Главный модуль программы `Prometey`

Запускает графический интерфейс и управляет всеми этапами расчёта:
- Окна `Window_1` … `Window_7` — каждый этап расчёта охладителя.
- Загружает данные из Excel (Dedal и Ikar).
- Использует модули: функций, таблиц, графиков и Cantera.
- Хранит глобальный класс `user` с параметрами расчёта.

Все действия пользователя (ввод, кнопки, выбор компонентов) реализованы здесь.
"""

from tkinter import filedialog
import tkinter.messagebox as messagebox
import sys
import warnings
from prometey_customtkinter import *
from prometey_cantera import *
from prometey_tabl import *
from prometey_graph_programm import *

file1 = None
file2 = None
FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", FR_PRIVATE, 0)
else:
    pass

font0 = ("Futura PT Book", 18)  # Настройка пользовательского шрифта 1
font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 2
font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 3

warnings.filterwarnings("ignore", category=UserWarning)


class user:
    def __init__(self):
        self.p_ohl_0 = None  # Давление охладителя (считаются термодинамические параметры охладителя по таблице)
        self.p_ohl = None
        self.m_ohl = None  # Расход суммарный охладителя
        self.T_nach = None  # Начальная температура охладителя
        self.phi = None  # Поправка на пристенок (зависит от доли расхода, идущего на пристенок)
        self.eps_g = None  # Излучательная способность газа (надо самому посчитать, извините)
        self.cooler = None  # Охладитель
        self.matarial_vn = None  # Материал внутренней стенки
        self.h = None  # Высота ребра (в метрах)
        self.delta_st = None  # Толщина стенок (в метрах)
        self.delta_reb = None  # Толщина ребра (в метрах)
        self.delta_st_nar = None  # Толщина наружней стенки (не учитывается в расчёте, нужна для визуализации)
        self.beta_reb = None  # Угол наклона рёбер (в градусах)
        self.variant = None  # Вариант охлаждения
        self.T_usl = None  # Температура стенки условная (потом превращается в массив и пересчитывается)
        self.lambda_st_vn = 245  # Коэффициент теплопроводности внутренней стенки, пересчитывается
        self.lambda_st_vn_1 = 19
        self.delta_sheroh = 0.00575 * 0.001  # Cтальная стенка = 0,02…0,10 мм; стенка из меди и медных сплавов = 0,0015…0,01 мм
        self.result_dedal = None  # Некоторые параметры из Дедала, нужны для пересчёта
        self.result_ikar = None  # Некоторые параметры из Икара, нужны для пересчёта
        self.c_p_T_st = None  # Теплоёмкость стенки условная, пересчитывается
        self.m_ohl_1 = None  # Расход 1 (Вариант 1)
        self.m_ohl_2 = None  # Расход 2 (Вариант 1)
        self.index_peret_1 = None  # Индекс перетечки 1 (Вариант 1)
        self.index_peret_2 = None  # Индекс перетечки 1 (Вариант 1)
        self.ind_peret = None  # Индекс перетечки (Вариант 3 и Вариант 4)
        self.ind_smena = None
        self.X = None
        self.Y = None
        self.d_kp = None
        self.D = None
        self.number = None
        self.n_r_array = None
        self.t = None
        self.t_N = None
        self.f = None
        self.d_g = None
        self.T_og = None
        self.R_og = None
        self.c_p_T_0g = None
        self.mu_og = None
        self.T_st_g = None
        self.D_otn = None
        self.F_otn = None
        self.q_kon = None
        self.q_l = None
        self.q_sum = None
        self.X = None
        self.betta = None
        self.T_st_otn = None
        self.lambd = None
        self.S_1 = None
        self.delta_S = None
        self.T_aray = None
        self.p_aray = None
        self.rho_aray = None
        self.C_aray = None
        self.mu_aray = None
        self.lambda_aray = None
        self.K_aray = None
        self.u_ohl = None
        self.T_ohl = None
        self.C_p_raznitsa = None
        self.C_p_ohl = None
        self.lambda_ohl = None
        self.mu_ohl = None
        self.K_ohl = None
        self.rho_ohl = None
        self.alpha_ohl = None
        self.E = None
        self.kpd_r = None
        self.T_st_g = None
        self.T_st_ohl =None
        self.p_ohl_v_kontse = None
        self.delta_x_s=None
        self.delta_p=None
        self.p_itog =None
        self.Re =None
        self.delta_sheroh_otn =None
        self.Re_gr =None
        self.epsilon =None
        self.l =None
        self.c_p_T_st_new=None
        self.F = None
        self.delta_x = None
        self.a=1
        self.b=1
        self.c=1
        self.d=1
        self.p_aray_2 = None
        self.T_aray_2 =None
        self.rho_aray_2 = None
        self.C_aray_2 = None
        self.mu_aray_2 = None
        self.lambda_aray_2 = None
        self.K_aray_2 = None
        self.T_nach_1 = None
        self.T_nach_2 = None
        self.p_ohl_v_kontse_2=None
class Window_1(ctk.CTk):
    '''--------------------Первое окно с вводом данных--------------------'''

    def __init__(self):
        super().__init__()
        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2
        self.title("Prometey")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.geometry(f"{1305}x{734}+{10}+{10}")  # Установка размеров окна
        ctk.set_default_color_theme("green")  # Загрузка пользовательской темы
        self.fg_color = 'white'
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов
        self.iconbitmap('data/prometey.ico')  # Установка иконки окна
        self.configure(bg_color="black")  # Установка цвета фона окна
        ctk.set_appearance_mode("dark")

        self.variant = 2
        self.material_in = "БрХ0,8"

        self.print_label()
        self.print_button()
        self.print_entry()
        toggle_info_frame(self)
        self.setup_combobox()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def print_label(self):
        """Визуализация текста в окне"""
        self.label1 = create_label(self, "Добро пожаловать в программу 'Прометей' !", 50, 2)
        self.label2 = create_label(self, "• Введите давление охладителя, МПа:", 10, 30)
        self.label3 = create_label(self, "• Введите расход охладителя, кг/с:", 10, 60)
        self.label4 = create_label(self, "• Введите начальную температуру охладителя, К:", 10, 90)
        self.label5 = create_label(self, "• Введите значение поправки на пристенок:", 10, 120)
        self.label6 = create_label(self, "• Введите излучательную способность газа:", 10, 150)
        self.label7 = create_label(self, "• Выберите охладитель:", 10, 180)
        self.label8 = create_label(self, "• Выберите материал внутренней стенки:", 10, 210)

        self.label9 = create_label(self, "• Высота стенок, мм:", 10, 270)
        self.label10 = create_label(self, "• Толщина огневой стенки, мм:", 10, 300)
        self.label11 = create_label(self, "• Толщину ребер, мм:", 10, 330)
        self.label12 = create_label(self, "• Толщина наружной стенки, мм:", 10, 360)
        self.label13 = create_label(self, "• Угол наклона рёбер, град.:", 10, 390)

        self.label14 = create_label(self, "• Вариант охлаждения:", 10, 450)

    def print_button(self):
        """Создание кнопок"""
        self.button1 = ctk.CTkButton(self, text="Загрузить Дедал", command=lambda: self.select_file1(),
                                     fg_color="#242424", border_width=2, border_color="white", font=font1)
        self.button1.place(x=455, y=450)

        self.button2 = ctk.CTkButton(self, text="Загрузить Икар", command=lambda: self.select_file2(),
                                     fg_color="#242424", border_width=2, border_color="white", font=font1)
        self.button2.place(x=600, y=450)
        self.close_button = create_button(self, "Выбрать", lambda: self.close_window(), self.font1, 100, 760, 450)
        self.info_button = create_button(self, "?", lambda: toggle_info_frame(self), self.font1, 20, 840, 5)
        self.cooling_button = create_button(self, "Варианты", lambda: toggle_cooling_frame(self), self.font1, 100, 735,
                                            5)

    def print_entry(self):
        """Создание окон с вводом чисел"""
        self.entry1_value = ctk.StringVar()
        self.Entry1 = create_entry(self, 80, self.entry1_value, 275, 30)
        self.entry2_value = ctk.StringVar()
        self.Entry2 = create_entry(self, 80, self.entry2_value, 260, 60)
        self.entry3_value = ctk.StringVar()
        self.Entry3 = create_entry(self, 80, self.entry3_value, 350, 90)
        self.entry4_value = ctk.StringVar()
        self.Entry4 = create_entry(self, 80, self.entry4_value, 310, 120)
        self.entry5_value = ctk.StringVar()
        self.Entry5 = create_entry(self, 80, self.entry5_value, 310, 150)

        self.entry6_value = ctk.StringVar()
        self.Entry6 = create_entry(self, 80, self.entry6_value, 160, 270)
        self.entry7_value = ctk.StringVar()
        self.Entry7 = create_entry(self, 80, self.entry7_value, 225, 300)
        self.entry8_value = ctk.StringVar()
        self.Entry8 = create_entry(self, 80, self.entry8_value, 170, 330)
        self.entry9_value = ctk.StringVar()
        self.Entry9 = create_entry(self, 80, self.entry9_value, 235, 360)
        self.entry10_value = ctk.StringVar()
        self.Entry10 = create_entry(self, 80, self.entry10_value, 210, 390)

        self.entry6_value.set(5)
        self.entry7_value.set(2)
        self.entry8_value.set(2)
        self.entry9_value.set(4)
        self.entry10_value.set(15)

    def setup_combobox(self):
        """=====Создание ячеек с компонентами====="""
        self.combobox1 = ctk.CTkComboBox(self, values=["", "Аммиак", "АТ", "Аэрозин-50", "Вода", "Водород", "Гелий",
                                                       "Керосин-Т1", "Кислород", "Метан", "НДМГ", "Этанол", 'АТ+НДМГ'],
                                         command=self.combobox_callback1,
                                         font=("Futura PT Book", 14), dropdown_font=("Futura PT Book", 14), width=100)
        self.combobox2 = ctk.CTkComboBox(self, values=["", "БрХ0,8"], command=self.combobox_callback2,
                                         font=("Futura PT Book", 14), dropdown_font=("Futura PT Book", 14), width=100)
        self.combobox3 = ctk.CTkComboBox(self, values=["", "1", "2", "3", "4",'5','6'], command=self.combobox_callback3,
                                         font=("Futura PT Book", 14), dropdown_font=("Futura PT Book", 14), width=70)
        self.combobox1.place(x=180, y=180)
        self.combobox2.place(x=290, y=210)
        self.combobox3.place(x=180, y=450)
        self.combobox2.set("БрХ0,8")
        self.combobox3.set(str(self.variant))

    def combobox_callback1(self, value):
        """=====Функиця, связанная с сохранением выбранного окислителя====="""
        self.cooler = value

    def combobox_callback2(self, value):
        """=====Функиця, связанная с сохранением выбранного горючего====="""
        self.material_in = value

    def combobox_callback3(self, value):
        """=====Функиця, связанная с сохранением выбранного горючего====="""
        self.variant = value

    def select_file1(self):
        global file1
        file1 = filedialog.askopenfilename(title="Выберите первый Excel файл")
        if file1:
            try:
                self.result_dedal = find_dedal_ikar(file_path_1=file1)
                self.button1.configure(fg_color="#2FA572", hover_color="#106A43", text="Дедал ✅")
            except Exception as e:
                messagebox.showerror("Ошибка в Дедале", f"{e}")
                self.button1.configure(fg_color="red", hover_color="darkred", text="Дедал ❌")
        print(self.result_dedal)
        self.combobox1.set(self.result_dedal["cooler_mb"])
        self.cooler = self.result_dedal["cooler_mb"]

    def select_file2(self):
        global file2
        file2 = filedialog.askopenfilename(title="Выберите второй Excel файл")
        if file2:
            try:
                self.result_ikar = find_dedal_ikar(file_path_2=file2)
                self.button2.configure(fg_color="#2FA572", hover_color="#106A43", text="Икар ✅")
            except Exception as e:
                messagebox.showerror("Ошибка в Икаре", f"{e}")
                self.button2.configure(fg_color="red", hover_color="darkred", text="Икар ❌")
        self.entry4_value.set(self.result_ikar["phi_pr"])
        self.entry2_value.set(self.result_ikar["m_gor"])
        if self.result_ikar.get("K2"):
            self.entry1_value.set(self.result_ikar["K2"])

        if self.result_ikar.get("K3"):
            self.entry3_value.set(self.result_ikar["K3"])

        if self.result_ikar.get("K4"):
            self.entry5_value.set(self.result_ikar["K4"])

        if self.result_ikar.get("K5"):
            user.p_ohl_v_kontse=float(self.result_ikar["K5"])
        else:
            user.p_ohl_v_kontse=float(self.result_dedal["p"])+1.5
        if self.result_ikar.get("K6"):
            user.p_ohl_v_kontse_2=float(self.result_ikar["K6"])
        else:
            user.p_ohl_v_kontse_2=float(self.result_dedal["p"])+1.5
        if self.result_ikar.get("L2"):
            user.a=float(self.result_ikar["L2"])
        else:
            self.result_ikar["L2"]=1
        if self.result_ikar.get("L3"):
            user.b=float(self.result_ikar["L3"])
        else:
            self.result_ikar["L3"] = 1
        if self.result_ikar.get("L4"):
            user.c=float(self.result_ikar["L4"])
        else:
            self.result_ikar["L4"] = 1
        if self.result_ikar.get("L5"):
            user.d=float(self.result_ikar["L5"])
        else:
            self.result_ikar["L5"] = 1
        print(self.result_ikar)


    def close_window(self):
        """Закрытие окна. Запись всех переменных в класс user"""
        try:
            self.destroy()
            user.T_og, user.R_og, user.c_p_T_0g, user.mu_og = find_params_tog(self.result_dedal["k_m0"],
                                                                              self.result_ikar["k_m_pr"] /
                                                                              self.result_dedal["k_m0"],
                                                                              self.result_dedal["H_gor"],
                                                                              self.result_dedal["H_ox"],
                                                                              self.result_dedal["form_gor"],
                                                                              self.result_dedal["form_ox"],
                                                                              self.result_dedal["p"])
            print(user.T_og, user.R_og, user.c_p_T_0g, user.mu_og)
            user.p_ohl_0 = float(self.entry1_value.get())
            user.m_ohl = float(self.entry2_value.get())
            user.T_nach = float(self.entry3_value.get())
            user.phi = float(self.entry4_value.get())
            user.eps_g = float(self.entry5_value.get())
            user.cooler = self.cooler
            user.matarial_vn = self.material_in
            user.h = float(self.entry6_value.get()) / 1000
            user.delta_st = float(self.entry7_value.get()) / 1000
            user.delta_reb = float(self.entry8_value.get()) / 1000
            user.delta_st_nar = float(self.entry9_value.get()) / 1000
            user.beta_reb = float(self.entry10_value.get()) * math.pi / 180
            user.variant = int(self.variant)
            user.result_dedal = self.result_dedal
            user.result_ikar = self.result_ikar
            if user.matarial_vn == 'БрХ0,8':
                user.T_usl = 600
                user.lambda_st_vn = 245
            user.c_p_T_st = find_params_proverka(float(self.result_dedal["k_m0"]),
                                                 float(self.result_ikar["k_m_pr"]) / float(self.result_dedal["k_m0"]),
                                                 float(self.result_dedal["H_gor"]), float(self.result_dedal["H_ox"]),
                                                 self.result_dedal["form_gor"], self.result_dedal["form_ox"],
                                                 float(self.result_dedal["p"]),
                                                 user.T_usl)  # Поиск теплоёмкости при Т_ст_усл
            print(user.c_p_T_st)
            window_2 = Window_2()
            window_2.mainloop()
        except Exception as e:
            # Если произошла ошибка, показываем сообщение
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")
class Window_2(ctk.CTk):
    '''--------------------Окно с уточнением варианта охлаждения (Таблица 1)--------------------'''

    def __init__(self):
        super().__init__()
        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2
        self.title("Сопло. Таблица 1")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.geometry(f"{1305}x{734}+{10}+{10}")  # Установка размеров окна
        ctk.set_default_color_theme("green")  # Загрузка пользовательской темы
        self.fg_color = 'white'
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов
        self.iconbitmap('data/prometey.ico')  # Установка иконки окна
        self.configure(bg_color="black")  # Установка цвета фона окна
        ctk.set_appearance_mode("dark")
        self.mono_font = ctk.CTkFont(family="Consolas", size=14)  # или "Courier New"

        print(user.a,user.b,user.c,user.d)
        self.place_scrollbar()
        self.setup_frame()
        self.print_entry()
        self.params_tabl_1()
        self.create_scrollable_table()
        self.print_label()
        self.print_button()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def place_scrollbar(self):
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=845, height=470, fg_color='#242424')  # 171717
        self.scrollbar_frame_0.place(x=1, y=1)

    def setup_frame(self):
        """--------------------Создание мини-окон--------------------"""
        self.frame2 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=845, height=850, fg_color="#242424",
                                   bg_color="transparent")
        self.frame2.grid(row=0, column=0, sticky='w', padx=1, pady=1)

    def print_label(self):
        """Визуализация текста в окне"""
        self.label1 = create_label(self.frame2, "Таблица 1", 20, 460)
        self.label1 = create_label(self.frame2, "- Минимальный шаг оребрения (мм)", 540, 30)
        self.label1 = create_label(self.frame2, "- Максимальный шаг оребрения (мм)", 540, 60)

    def print_entry(self):
        """Создание окон с вводом чисел"""
        self.entry1_value = ctk.StringVar()
        self.entry2_value = ctk.StringVar()
        self.Entry1 = create_entry(self.frame2, 50, self.entry1_value, 480, 30)
        self.Entry2 = create_entry(self.frame2, 50, self.entry2_value, 480, 60)
        self.entry1_value.set(7)  # 2.5
        self.entry2_value.set(12)  # 7.5
        if user.variant == 1:
            self.entry3_value = ctk.StringVar()
            self.entry4_value = ctk.StringVar()
            self.entry5_value = ctk.StringVar()
            self.Entry3 = create_entry(self.frame2, 80, self.entry3_value, 700, 90)
            self.Entry4 = create_entry(self.frame2, 80, self.entry4_value, 750, 120)
            self.Entry5 = create_entry(self.frame2, 80, self.entry5_value, 700, 150)
            self.label3 = create_label(self.frame2, "Координата разветвления (м):", 480, 90)
            self.label4 = create_label(self.frame2, "Координата встречи магистралей (м):", 480, 120)
            self.label5 = create_label(self.frame2, "Расход, идущий на срез (кг/с):", 480, 150)
        elif user.variant == 3 or user.variant == 4:
            self.entry6_value = ctk.StringVar()
            self.Entry6 = create_entry(self.frame2, 80, self.entry6_value, 700, 90)
            self.label3 = create_label(self.frame2, "Координата разветвления (м):", 480, 90)
        elif user.variant == 5:
            self.entry8_value = ctk.StringVar()
            self.entry9_value = ctk.StringVar()
            self.entry10_value = ctk.StringVar()
            self.Entry9 = create_entry(self.frame2, 80, self.entry8_value, 750, 90)
            self.Entry10 = create_entry(self.frame2, 80, self.entry9_value, 750, 120)
            self.Entry11 = create_entry(self.frame2, 80, self.entry10_value, 700, 150)
            self.label3 = create_label(self.frame2, "Координата выхода охладителя (м):", 480, 90)
            self.label4 = create_label(self.frame2, "Координата разветвления (м):", 480, 120)
            self.label5 = create_label(self.frame2, "Расход, идущий на срез (кг/с):", 480, 150)
            self.button_var5=create_button(self.frame2,'Ввод',lambda: self.entry_var5(),self.font1, 100,480,180)
        elif user.variant == 6:
            self.entry11_value = ctk.StringVar()
            self.entry12_value = ctk.StringVar()
            self.entry13_value = ctk.StringVar()
            self.entry14_value = ctk.StringVar()
            self.entry15_value = ctk.StringVar()
            self.Entry11 = create_entry(self.frame2, 80, self.entry11_value, 750, 90)
            self.Entry12 = create_entry(self.frame2, 80, self.entry12_value, 750, 120)
            self.Entry13 = create_entry(self.frame2, 80, self.entry13_value, 700, 150)
            self.Entry14 = create_entry(self.frame2, 80, self.entry14_value, 750, 180)
            self.Entry15 = create_entry(self.frame2, 80, self.entry15_value, 700, 210)
            self.label3 = create_label(self.frame2, "Координата смены охладителя (м):", 480, 90)
            self.label4 = create_label(self.frame2, "Расход 1 (АТ),кг/с:", 480, 120)
            self.label5 = create_label(self.frame2, "Расход 2 (НДМГ),кг/с:", 480, 150)
            self.label5 = create_label(self.frame2, "Начальная температура 1, К:", 480, 180)
            self.label5 = create_label(self.frame2, "Начальная температура 2, К:", 480, 210)
        self.label3 = create_label(self.frame2, "Укажите (если надо) координату смены", 480, 350)
        self.label3 = create_label(self.frame2, "материала на сталь (м):", 480, 375)
        self.entry7_value = ctk.StringVar()
        self.Entry7 = create_entry(self.frame2, 80, self.entry7_value, 480, 400)
    def entry_var5(self):
        user.index_peret_1 = find_nearest_index(self.X, float(self.entry8_value.get()))
        user.index_peret_2 = find_nearest_index(self.X, float(self.entry9_value.get()))
        user.m_ohl_1 = float(self.entry10_value.get())
        user.m_ohl_2 = user.m_ohl - user.m_ohl_1
        print(user.index_peret_1, user.index_peret_2, user.m_ohl_1, user.m_ohl_2)
        self.X_new, self.Y_new = reflect_tail(self.X, self.Y, len(self.X)-user.index_peret_1)
        print(self.X_new)
        self.X=self.X_new
        self.Y=self.Y_new
        self.T_st_g = [user.T_usl] * len(self.Y)  # Первичное заполнение массива температурой стенки условной
        self.c_p_T_st = [user.c_p_T_st] * len(self.Y)  # Первичное заполнение массива удельной теплоёмкости при температуре стенки условной
        self.lambda_st_vn=[245]*len(self.Y)
        self.number, self.X, self.D, self.D_otn, self.F, self.F_otn, self.delta_x, self.delta_x_s, self.d_kp, self.delta_S = tabl_1(
            self.X, self.Y)  # Вывод таблицы №1
        print_nozzle_window(self.X, self.Y, self.frame2)
    def params_tabl_1(self):
        if user.cooler!="АТ+НДМГ":
            if user.cooler == 'НДМГ' or user.cooler == 'Аэрозин-50' or user.cooler == 'Вода' or user.cooler == 'Керосин-Т1' or user.cooler == 'Этанол':
                self.p_aray = []  # Если параметры охладителя не зависят от давления
                self.T_aray, self.rho_aray, self.C_aray, self.mu_aray, self.lambda_aray, self.K_aray = find_params_ohl(
                    user.cooler)  # Создание массивов с параметрами охладителя
            else:
                self.T_aray, self.p_aray, self.rho_aray, self.C_aray, self.mu_aray, self.lambda_aray, self.K_aray = find_params_ohl(
                    user.cooler)
        else:
            self.T_aray, self.p_aray, self.rho_aray, self.C_aray, self.mu_aray, self.lambda_aray, self.K_aray = find_params_ohl(
                'АТ')
            self.p_aray_2 = []  # Если параметры охладителя не зависят от давления
            self.T_aray_2, self.rho_aray_2, self.C_aray_2, self.mu_aray_2, self.lambda_aray_2, self.K_aray_2 = find_params_ohl('НДМГ')  # Создание массивов с параметрами охладителя

        self.start_row_index, self.end_row_index = find_index_x_y(file1)  # Поиск индексов координат в документе
        self.X, self.Y = save_coord_x_y(self.start_row_index, self.end_row_index,
                                        file1)  # Сохранение координат в массивы
        self.X, self.Y = filtred_array(self.X, self.Y)  # Фильтрация совпадающих значений
        self.T_st_g = [user.T_usl] * len(self.Y)  # Первичное заполнение массива температурой стенки условной
        self.c_p_T_st = [user.c_p_T_st] * len(
            self.Y)  # Первичное заполнение массива удельной теплоёмкости при температуре стенки условной
        self.lambda_st_vn = [245] * len(self.Y)
        self.number, self.X, self.D, self.D_otn, self.F, self.F_otn, self.delta_x, self.delta_x_s, self.d_kp, self.delta_S = tabl_1(
            self.X, self.Y)  # Вывод таблицы №1
        print_nozzle_window(self.X, self.Y, self.frame2)

    def create_scrollable_table(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=700, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=490)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=700, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=10, pady=10)

        # Заголовки таблицы
        headers = ['№', 'X, мм', 'D, мм', 'D отн', 'F, мм²', 'F отн', 'Δx, мм', 'Δx_s, мм', 'ΔS, мм²']
        header_line = "{:<6}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}{:<12}{:<12}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(self.number)):
            x = self.X[i] * 1000
            d = self.D[i] * 1000
            d_otn = self.D_otn[i]
            f = self.F[i] * 1e6
            f_otn = self.F_otn[i]
            delta_x = self.delta_x[i] * 1000
            delta_x_s = self.delta_x_s[i] * 1000
            delta_s = self.delta_S[i] * 1e6
            number = self.number[i]

            # Функция для форматирования с заменой nan на "-"
            def fmt(value):
                return "-" if value is None or (isinstance(value, float) and math.isnan(value)) else f"{value:.2f}"

            # Используем безопасную версию
            line = "{:<6}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}{:<12}{:<12}".format(
                int(number),
                fmt(x),
                fmt(d),
                fmt(d_otn),
                fmt(f),
                fmt(f_otn),
                fmt(delta_x),
                fmt(delta_x_s),
                fmt(delta_s)
            )
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")

    def print_button(self):
        self.close_button = create_button(self.frame2, "Далее", lambda: self.close_window(), self.font1, 100, 730, 820)

    def close_window(self):
        self.value = self.entry7_value.get().strip()
        try:
            self.ind_smena_0 = float(self.value) if self.value else 10000
            user.ind_smena = find_nearest_index(self.X, self.ind_smena_0)
            user.lambda_st_vn_1=[19]*len(self.X)
        except ValueError:
            user.ind_smena = 10000  # если ввели текст или мусор
            user.lambda_st_vn_1 = [19]*len(self.X)
        user.t_n_min = float(self.entry1_value.get())
        user.t_n_max = float(self.entry2_value.get())
        user.p_ohl = [user.p_ohl_0] * len(self.X)
        user.X = self.X
        user.Y = self.Y
        user.d_kp = self.d_kp
        user.D = self.D
        user.number = self.number
        user.T_st_g = self.T_st_g
        user.D_otn = self.D_otn
        user.F_otn = self.F_otn
        user.F=self.F
        user.delta_x=self.delta_x
        user.c_p_T_st = self.c_p_T_st
        user.delta_x_s=self.delta_x_s
        user.delta_S = self.delta_S
        user.T_aray = self.T_aray
        user.p_aray = self.p_aray
        user.rho_aray = self.rho_aray
        user.C_aray = self.C_aray
        user.mu_aray = self.mu_aray
        user.lambda_aray = self.lambda_aray
        user.K_aray = self.K_aray
        user.lambda_st_vn=self.lambda_st_vn
        if user.variant==6:
            user.p_aray_2 =self.p_aray_2
            user.T_aray_2=self.T_aray_2
            user.rho_aray_2=self.rho_aray_2
            user.C_aray_2=self.C_aray_2
            user.mu_aray_2=self.mu_aray_2
            user.lambda_aray_2=self.lambda_aray_2
            user.K_aray_2=self.K_aray_2

        print(user.ind_smena)
        if user.variant == 1:
            user.index_peret_1 = find_nearest_index(self.X, float(self.entry3_value.get()))
            user.index_peret_2 = find_nearest_index(self.X, float(self.entry4_value.get()))
            user.m_ohl_1 = float(self.entry5_value.get())
            user.m_ohl_2 = user.m_ohl - user.m_ohl_1
            print(user.index_peret_1, user.index_peret_2, user.m_ohl_1, user.m_ohl_2)
        elif user.variant == 3 or user.variant == 4:
            user.ind_peret = find_nearest_index(self.X, float(self.entry6_value.get()))
        elif user.variant == 6:
            user.ind_peret = find_nearest_index(self.X, float(self.entry11_value.get()))
            user.m_ohl_1 = float(self.entry12_value.get())
            user.m_ohl_2 = float(self.entry13_value.get())
            user.T_nach_1 = float(self.entry14_value.get())
            user.T_nach_2 = float(self.entry15_value.get())
        self.destroy()
        window_3 = Window_3()
        window_3.mainloop()
class Window_3(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2
        self.title("Оребрение. Таблица 2")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.geometry(f"{1305}x{734}+{10}+{10}")  # Установка размеров окна
        ctk.set_default_color_theme("green")  # Загрузка пользовательской темы
        self.fg_color = 'white'
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов
        self.iconbitmap('data/prometey.ico')  # Установка иконки окна
        self.configure(bg_color="black")  # Установка цвета фона окна
        ctk.set_appearance_mode("dark")
        self.mono_font = ctk.CTkFont(family="Consolas", size=14)  # или "Courier New"

        self.place_scrollbar()
        self.setup_frame()
        self.solution_to_tabl2()
        self.print_tabl2()
        self.print_button()
        self.print_label()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def place_scrollbar(self):
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=845, height=470, fg_color='#242424')  # 171717
        self.scrollbar_frame_0.place(x=1, y=1)

    def setup_frame(self):
        """--------------------Создание мини-окон--------------------"""
        self.frame2 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=845, height=1210, fg_color="#242424",
                                   bg_color="transparent")
        self.frame2.grid(row=0, column=0, sticky='w', padx=1, pady=1)

    def print_label(self):
        """Визуализация текста в окне"""
        self.label1 = create_label(self.frame2, "Таблица 2", 20, 820)

    def solution_to_tabl2(self):
        self.n_r_kp_min = find_n_min(user.beta_reb, user.t_n_min, user.d_kp, user.delta_st,
                                     user.h)  # Поиск минимального количества рёбер (в критике)
        self.n_r_array = find_n_r_array(user.X, user.Y, self.n_r_kp_min, user.beta_reb, user.delta_st, user.h,
                                        user.t_n_max)  # Распределение рёбер по соплу
        self.n_r_array, self.t, self.t_N, self.f, self.d_g = tabl_2(user.D, user.delta_st, user.h, self.n_r_array,
                                                                    user.beta_reb, user.delta_reb)  # Вывод таблицы №2
        if user.variant==5:
            for i in range(len(user.D)):
                if i>=user.index_peret_1:
                    self.n_r_array[i]=self.n_r_array[i]/2
        print_cooling_fins(user.delta_st, user.delta_reb, user.delta_st_nar, user.h, self.n_r_array, user.D, 0, 5, 10,
                           'Камера Сгорания', self.frame2)
        print_cooling_fins(user.delta_st, user.delta_reb, user.delta_st_nar, user.h, self.n_r_array, user.D,
                           user.Y.index(min(user.Y)), 760, 10, 'Критическое сечение', self.frame2)
        print_cooling_fins_array(user.X, self.n_r_array, user.Y, self.frame2,2,780)

    def print_tabl2(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=500, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=850)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=500, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=10, pady=10)

        # Заголовки таблицы
        headers = ['№', 'n_р', 't, мм', 't_N, мм', 'f, мм²', 'd_г, мм']
        header_line = "{:<6}{:<10}{:<10}{:<10}{:<12}{:<10}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            n_r = self.n_r_array[i]
            t_0 = round(self.t[i], 3)
            t_N_0 = round(self.t_N[i], 3)
            f_0 = round(self.f[i] * 1e6, 3)
            d_g_0 = round(self.d_g[i], 3)
            number = user.number[i]

            line = "{:<6}{:<10}{:<10.3f}{:<10.3f}{:<12.3f}{:<10.3f}".format(
                int(number), n_r, t_0, t_N_0, f_0, d_g_0
            )
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")

    def print_button(self):
        self.close_button = create_button(self.frame2, "Далее", lambda: self.close_window(), self.font1, 100, 730,
                                          1150)

    def close_window(self):
        user.n_r_array = self.n_r_array
        user.t = self.t
        user.t_N = self.t_N
        user.f = self.f
        user.d_g = self.d_g

        self.destroy()
        window_4 = Window_4()
        window_4.mainloop()
class Window_4(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2
        self.title("Тепловые потоки. Таблица 3")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.geometry(f"{1305}x{734}+{10}+{10}")  # Установка размеров окна
        ctk.set_default_color_theme("green")  # Загрузка пользовательской темы
        self.fg_color = 'white'

        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов
        self.iconbitmap('data/prometey.ico')  # Установка иконки окна
        self.configure(bg_color="black")  # Установка цвета фона окна
        ctk.set_appearance_mode("dark")
        self.mono_font = ctk.CTkFont(family="Consolas", size=14)  # или "Courier New"

        self.place_scrollbar()
        self.setup_frame()
        self.print_label()
        self.solution_to_tabl3()
        self.print_tabl3()
        self.print_button()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def place_scrollbar(self):
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=845, height=470, fg_color='#242424')  # 171717
        self.scrollbar_frame_0.place(x=1, y=1)

    def setup_frame(self):
        """--------------------Создание мини-окон--------------------"""
        self.frame2 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=845, height=320 + 455 + 20 + 10 + 10,
                                   fg_color="#242424", bg_color="transparent")
        self.frame2.grid(row=0, column=0, sticky='w', padx=1, pady=1)

    def print_label(self):
        """Визуализация текста в окне"""
        self.label1 = create_label(self.frame2, "Таблица 3", 20, 430)

    def solution_to_tabl3(self):
        self.q_kon, self.betta, self.T_st_otn, self.lambd, self.S_1 = find_q_kon(user.number, user.Y, user.c_p_T_0g,
                                                                                 user.c_p_T_st, user.T_st_g, user.T_og,
                                                                                 user.mu_og, user.R_og, user.D_otn,
                                                                                 user.d_kp, user.F_otn, user.b,
                                                                                 user.result_dedal['p'],
                                                                                 user.result_dedal['k'], 1)
        self.q_l = find_q_l(user.eps_g, user.result_dedal['T'], user.result_ikar['phi_pr'], user.D_otn, user.number,
                            user.Y)
        self.q_sum = find_q_sum(self.q_kon, self.q_l)
        self.q_kon_proshl = (max(self.q_kon))
        self.q_kon, self.q_l, self.q_sum, self.X, self.betta, self.T_st_otn, self.lambd, self.S_1 = tabl_3(self.q_kon,
                                                                                                           self.q_l,
                                                                                                           self.q_sum,
                                                                                                           user.X,
                                                                                                           self.betta,
                                                                                                           self.T_st_otn,
                                                                                                           self.lambd,
                                                                                                           self.S_1)  # Вывод таблицы №3
        print_heat_flows(self.q_kon, self.q_l, self.q_sum, self.X, self.frame2)

    def print_tabl3(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=750, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=455)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=750, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=10, pady=10)

        # Заголовки таблицы
        headers = ['№', 'X,мм', 'λ', 'β', 'S', 'T_ст_отн', 'q_к, МВт/м²', 'q_л, МВт/м²', 'q_сум, МВт/м²']
        header_line = "{:<6}{:<9}{:<9}{:<9}{:<10}{:<10}{:<12}{:<12}{:<12}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            q_kon_0 = round(self.q_kon[i], 3)
            q_l_0 = round(self.q_l[i], 3)
            q_sum_0 = round(self.q_sum[i], 3)
            X_0 = round(self.X[i] * 1000, 3)
            betta_0 = round(self.betta[i], 3)
            T_st_otn_0 = round(self.T_st_otn[i], 3)
            lambd_0 = round(self.lambd[i], 3)
            S_1_0 = round(self.S_1[i], 3)
            number = user.number[i]

            line = "{:<6}{:<9}{:<9}{:<9}{:<10}{:<10}{:<12}{:<12}{:<12}".format(
                int(number), X_0, lambd_0, betta_0, S_1_0, T_st_otn_0, q_kon_0, q_l_0, q_sum_0
            )
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")

    def print_button(self):
        self.close_button = create_button(self.frame2, "Далее", lambda: self.close_window(), self.font1, 100, 730,
                                          320 + 460)

    def close_window(self):
        user.q_kon = self.q_kon
        user.q_l = self.q_l
        user.q_sum = self.q_sum
        user.X = self.X
        user.betta = self.betta
        user.T_st_otn = self.T_st_otn
        user.lambd = self.lambd
        user.S_1 = self.S_1

        self.destroy()
        window_5 = Window_5()
        window_5.mainloop()
class Window_5(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2
        self.title("Температура охладителя. Таблица 4")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.geometry(f"{1305}x{734}+{10}+{10}")  # Установка размеров окна
        ctk.set_default_color_theme("green")  # Загрузка пользовательской темы
        self.fg_color = 'white'

        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов
        self.iconbitmap('data/prometey.ico')  # Установка иконки окна
        self.configure(bg_color="black")  # Установка цвета фона окна
        ctk.set_appearance_mode("dark")
        self.mono_font = ctk.CTkFont(family="Consolas", size=13)  # или "Courier New"

        self.place_scrollbar()
        self.setup_frame()
        self.print_label()
        self.solution_to_tabl4()
        self.print_tabl4()
        self.print_button()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def place_scrollbar(self):
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=845, height=470, fg_color='#242424')  # 171717
        self.scrollbar_frame_0.place(x=1, y=1)

    def setup_frame(self):
        """--------------------Создание мини-окон--------------------"""
        self.frame2 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=845, height=320 + 455 + 20 + 10 + 10,
                                   fg_color="#242424", bg_color="transparent")
        self.frame2.grid(row=0, column=0, sticky='w', padx=1, pady=1)

    def print_label(self):
        """Визуализация текста в окне"""
        self.label1 = create_label(self.frame2, "Таблица 4", 20, 430)

    def raschet_temperatury(self):
        if int(user.variant) == 1:
            T_ohl, C_p_ohl, C_p_raznitsa, m_ohl_array = find_temp_slosh_tema(user.m_ohl_1, user.m_ohl_2,
                                                                             user.index_peret_1, user.index_peret_2,
                                                                             user.delta_S,
                                                                             user.q_sum, user.number, user.p_ohl, user.a,
                                                                             user.T_nach, user.cooler, user.T_aray,
                                                                             user.p_aray, user.C_aray)
        elif int(user.variant) == 2:
            m_ohl_array = [user.m_ohl] * len(user.X)
            T_ohl, C_p_ohl, C_p_raznitsa = find_temp(user.number, user.delta_S, user.p_ohl, user.q_sum, user.m_ohl, user.a,
                                                     user.T_nach, user.cooler, user.T_aray,
                                                     user.p_aray, user.C_aray)
        elif int(user.variant) == 3:
            m_ohl_array = [user.m_ohl] * len(user.X)
            T_ohl, C_p_ohl, C_p_raznitsa = find_temp_slozh_2(user.ind_peret, user.delta_S, user.q_sum, user.a, user.number,
                                                             user.p_ohl, user.m_ohl, user.T_nach,
                                                             user.cooler, user.T_aray, user.p_aray, user.C_aray)
        elif int(user.variant) == 5:
            T_ohl, C_p_ohl, C_p_raznitsa, m_ohl_array = find_temp_slozh_5(user.m_ohl_1, user.m_ohl_2,
                                                                             user.index_peret_1, user.index_peret_2,
                                                                             user.delta_S,
                                                                             user.q_sum, user.number, user.p_ohl,
                                                                             user.a,
                                                                             user.T_nach, user.cooler, user.T_aray,
                                                                             user.p_aray, user.C_aray)
        elif int(user.variant) == 6:
            T_ohl, C_p_ohl, C_p_raznitsa, m_ohl_array=find_temp_slozh_6(user.m_ohl_1,user.m_ohl_2,user.ind_peret,user.delta_S,
                                                                        user.q_sum,user.number,user.p_ohl,user.a,user.T_nach_1,
                                                                        user.T_nach_2,user.T_aray,user.p_aray,user.C_aray,
                                                                        user.T_aray_2,user.p_aray_2,user.C_aray_2)

        else:
            m_ohl_array = [user.m_ohl] * len(user.X)
            T_ohl, C_p_ohl, C_p_raznitsa = find_temp_slozh_1(user.ind_peret, user.delta_S, user.q_sum, user.a, user.number,
                                                             user.p_ohl, user.m_ohl, user.T_nach,
                                                             user.cooler, user.T_aray, user.p_aray, user.C_aray)
        return T_ohl, C_p_ohl, C_p_raznitsa, m_ohl_array

    def solution_to_tabl4(self):
        self.T_ohl, self.C_p_ohl, self.C_p_raznitsa, self.m_ohl_array = self.raschet_temperatury()
        print_temp_cooler(self.T_ohl, user.X, self.frame2)
        if user.variant==6:
            self.u_ohl, self.T_ohl, self.C_p_raznitsa, self.C_p_ohl, self.lambda_ohl, self.mu_ohl, self.K_ohl, self.rho_ohl, self.alpha_ohl, self.E, self.kpd_r = tabl_4_AT_NDMG(user.ind_peret,
                self.T_ohl,self.C_p_raznitsa,self.C_p_ohl,user.p_ohl,user.f,self.m_ohl_array,user.d_g,user.delta_reb,
                user.h,user.beta_reb,user.t,user.lambda_st_vn,user.T_aray, user.p_aray, user.rho_aray, user.C_aray,
                user.mu_aray, user.lambda_aray, user.K_aray,user.T_aray_2, user.p_aray_2, user.rho_aray_2, user.C_aray_2,
                user.mu_aray_2, user.lambda_aray_2, user.K_aray_2,user.cooler)
            print(len(self.rho_ohl))
        else:
            self.u_ohl, self.T_ohl, self.C_p_raznitsa, self.C_p_ohl, self.lambda_ohl, self.mu_ohl, self.K_ohl, self.rho_ohl, self.alpha_ohl, self.E, self.kpd_r = tabl_4(
                self.T_ohl,
                self.C_p_raznitsa, self.C_p_ohl, user.p_ohl, user.f, self.m_ohl_array, user.d_g, user.delta_reb,
                user.h, user.beta_reb,
                user.t, user.lambda_st_vn, user.T_aray, user.p_aray, user.rho_aray, user.C_aray, user.mu_aray,
                user.lambda_aray, user.K_aray, user.cooler)

    def print_tabl4(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=750, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=455)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=750, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=10, pady=10)
        # Заголовки таблицы
        headers = ['№', 'T_охл', 'ΔC,%', 'C_p_охл', 'λ_охл', 'μ_охл⋅10⁴', 'K_охл', 'ρ_охл', 'u_охл', 'α_охл⋅10⁻³',
                   '  E', ' η_р']
        header_line = "{:<5}{:<8}{:<6}{:<9}{:<7}{:<11}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            u_ohl_0 = round(self.u_ohl[i], 2)
            T_ohl_0 = round(self.T_ohl[i], 2)
            C_p_raznitsa_0 = round(self.C_p_raznitsa[i], 3)
            C_p_ohl_0 = round(self.C_p_ohl[i], 2)
            lambda_ohl_0 = round(self.lambda_ohl[i], 2)
            mu_ohl_0 = round(self.mu_ohl[i] * 10000, 4)
            K_ohl_0 = round(self.K_ohl[i], 2)
            rho_ohl_0 = round(self.rho_ohl[i], 2)
            alpha_ohl_0 = round(self.alpha_ohl[i] / 1000, 3)
            E_0 = round(self.E[i], 3)
            kpd_r_0 = round(self.kpd_r[i], 3)
            number = user.number[i]

            line = "{:<5}{:<8}{:<6}{:<9}{:<7}{:<11}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}".format(
                int(number), T_ohl_0, C_p_raznitsa_0, C_p_ohl_0, lambda_ohl_0, mu_ohl_0, K_ohl_0, rho_ohl_0, u_ohl_0,
                alpha_ohl_0, E_0, kpd_r_0)
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")

    def print_button(self):
        self.close_button = create_button(self.frame2, "Далее", lambda: self.close_window(), self.font1, 100, 730,
                                          320 + 460)

    def close_window(self):
        user.u_ohl = self.u_ohl
        user.T_ohl = self.T_ohl
        user.C_p_raznitsa = self.C_p_raznitsa
        user.C_p_ohl = self.C_p_ohl
        user.lambda_ohl = self.lambda_ohl
        user.mu_ohl = self.mu_ohl
        user.K_ohl = self.K_ohl
        user.rho_ohl = self.rho_ohl
        user.alpha_ohl = self.alpha_ohl
        user.E = self.E
        user.kpd_r = self.kpd_r

        self.destroy()
        window_6 = Window_6()
        window_6.mainloop()
class Window_6(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2
        self.title("Температура стенки. Таблица 5")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.geometry(f"{1305}x{734}+{10}+{10}")  # Установка размеров окна
        ctk.set_default_color_theme("green")  # Загрузка пользовательской темы
        self.fg_color = 'white'

        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов
        self.iconbitmap('data/prometey.ico')  # Установка иконки окна
        self.configure(bg_color="black")  # Установка цвета фона окна
        ctk.set_appearance_mode("dark")
        self.mono_font = ctk.CTkFont(family="Consolas", size=15)  # или "Courier New"

        self.place_scrollbar()
        self.setup_frame()
        self.print_label()
        self.solution_to_tabl5()
        self.print_tabl5()
        self.print_button()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def place_scrollbar(self):
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=845, height=470, fg_color='#242424')  # 171717
        self.scrollbar_frame_0.place(x=1, y=1)

    def setup_frame(self):
        """--------------------Создание мини-окон--------------------"""
        self.frame2 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=845, height=320 + 455 + 20 + 10 + 10,
                                   fg_color="#242424", bg_color="transparent")
        self.frame2.grid(row=0, column=0, sticky='w', padx=1, pady=1)

    def print_label(self):
        """Визуализация текста в окне"""
        self.label1 = create_label(self.frame2, "Таблица 5", 20, 430)

    def solution_to_tabl5(self):
        self.T_st_g, self.T_st_ohl,user.lambda_st_vn,user.lambda_st_vn_1 = find_temp_st_g(user.T_og, user.T_st_g, user.T_ohl, user.alpha_ohl, user.kpd_r, user.q_kon, user.q_l, user.delta_st, user.lambda_st_vn, user.d,
                                          user.number, user.ind_smena, user.lambda_st_vn_1)
        if user.variant==5:
            self.T_st_g, self.T_st_ohl=clone_temp_st(self.T_st_g, self.T_st_ohl,len(user.X)-user.index_peret_1,user.X)
        wall_temperatures(self.T_st_g, self.T_st_ohl,user.X,self.frame2)
    def print_tabl5(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=300, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=455)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=300, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=10, pady=10)
        # Заголовки таблицы
        headers = ['№', 'T_ст_г', 'T_ст_охл']
        header_line = "{:<6}{:<10}{:<10}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            T_st_g_0 = round(self.T_st_g[i], 2)
            T_st_ohl_0 = round(self.T_st_ohl[i], 2)
            number = user.number[i]

            line = "{:<6}{:<10}{:<10}".format(
                int(number), T_st_g_0, T_st_ohl_0)
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")

    def print_button(self):
        self.close_button = create_button(self.frame2, "Далее", lambda: self.close_window(), self.font1, 100, 730,
                                          320 + 460)

    def close_window(self):
        user.T_st_g=self.T_st_g
        user.T_st_ohl=self.T_st_ohl

        self.destroy()
        window_7 = Window_7()
        window_7.mainloop()
class Window_7(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2
        self.title("Потери. Таблица 6")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.geometry(f"{1305}x{734}+{10}+{10}")  # Установка размеров окна
        ctk.set_default_color_theme("green")  # Загрузка пользовательской темы
        self.fg_color = 'white'

        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов
        self.iconbitmap('data/prometey.ico')  # Установка иконки окна
        self.configure(bg_color="black")  # Установка цвета фона окна
        ctk.set_appearance_mode("dark")
        self.mono_font = ctk.CTkFont(family="Consolas", size=15)  # или "Courier New"

        user.delta_sheroh = 0.00575 * 0.001

        self.place_scrollbar()
        self.setup_frame()
        self.solution_to_tabl6()
        self.print_tabl6()
        self.print_button()
        self.print_label()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def place_scrollbar(self):
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=845, height=470, fg_color='#242424')  # 171717
        self.scrollbar_frame_0.place(x=1, y=1)

    def setup_frame(self):
        """--------------------Создание мини-окон--------------------"""
        self.frame2 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=845, height=1220,
                                   fg_color="#242424", bg_color="transparent")
        self.frame2.grid(row=0, column=0, sticky='w', padx=1, pady=1)

    def print_label(self):
        """Визуализация текста в окне"""
        self.label1 = create_label(self.frame2, "Таблица 6", 20, 840)

    def rashet_poteri(self):
        if user.variant == 1:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c, user.delta_sheroh, user.u_ohl, user.rho_ohl, user.d_g, user.mu_ohl, user.t_N, user.delta_reb, user.h, user.delta_x_s,
                                     user.beta_reb,
                                     user.p_ohl_v_kontse, user.variant, user.index_peret_1)  # Вывод таблицы №5
        elif user.variant == 2:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c,  user.delta_sheroh,  user.u_ohl,  user.rho_ohl,  user.d_g,  user.mu_ohl,  user.t_N,  user.delta_reb,  user.h,  user.delta_x_s,
                                    user.beta_reb, user.p_ohl_v_kontse,  user.variant)
        elif user.variant == 3:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c, user.delta_sheroh, user.u_ohl, user.rho_ohl, user.d_g, user.mu_ohl, user.t_N, user.delta_reb, user.h, user.delta_x_s,
                                     user.beta_reb,
                                     user.p_ohl_v_kontse,  user.variant,  user.ind_peret)
        elif user.variant == 5:
            delta_p, p_itog, Re, delta_sheroh_otn, Re_gr, epsilon, l = tabl_5(user.c, user.delta_sheroh, user.u_ohl,
                                                                              user.rho_ohl, user.d_g, user.mu_ohl,
                                                                              user.t_N, user.delta_reb, user.h,
                                                                              user.delta_x_s,
                                                                              user.beta_reb,
                                                                              user.p_ohl_v_kontse, user.variant,
                                                                              user.index_peret_2)  # Вывод таблицы №5
        elif user.variant == 6:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c, user.delta_sheroh, user.u_ohl, user.rho_ohl, user.d_g, user.mu_ohl, user.t_N, user.delta_reb, user.h, user.delta_x_s,
                                     user.beta_reb,
                                     user.p_ohl_v_kontse,  user.variant,  user.ind_peret,user.p_ohl_v_kontse_2)
        else:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c,  user.delta_sheroh,  user.u_ohl,  user.rho_ohl,  user.d_g,  user.mu_ohl,  user.t_N,  user.delta_reb,  user.h,  user.delta_x_s,
                                    user.beta_reb,user.p_ohl_v_kontse,  user.variant,  user.ind_peret)
        return delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l
    def solution_to_tabl6(self):
        gas = ct.Solution('gri30.yaml')  # один раз
        self.c_p_T_st = find_params_ks(gas, user.result_dedal["k_m0"], user.result_ikar["k_m_pr"] / user.result_dedal["k_m0"], user.result_dedal["H_gor"],
                                           user.result_dedal["H_ox"], user.result_dedal["form_gor"], user.result_dedal["form_ox"], user.result_dedal["p"], user.T_st_g)
        self.delta_p, self.p_itog,self.Re,self.delta_sheroh_otn,self.Re_gr,self.epsilon,self.l = self.rashet_poteri()
        print_local_pressure_losses(self.delta_p,user.X,self.frame2,50,10,1)
        print_local_pressure_losses(self.p_itog, user.X, self.frame2, 50, 800,2)

    def print_tabl6(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=700, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=870)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=700, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=2, pady=2)
        # Заголовки таблицы
        headers = ['№', 'Re', 'Δ_отн','Re_гр','ξ','l, мм','Δ_p, Па']
        header_line = "{:<6}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            delta_p_0 = round(self.delta_p[i], 2)
            Re_0 = round(self.Re[i], 1)
            delta_sheroh_otn_0 = round(self.delta_sheroh_otn[i], 6)
            Re_gr_0 = round(self.Re_gr[i], 1)
            l_0 = round(self.l[i]*1000, 3)
            epsilon_0 = round(self.epsilon[i], 6)
            number = user.number[i]

            line = "{:<6}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                int(number), Re_0,delta_sheroh_otn_0,Re_gr_0,epsilon_0,l_0,delta_p_0)
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")

    def print_button(self):
        self.close_button = create_button(self.frame2, "Далее", lambda: self.close_window(), self.font1, 100, 730,
                                          1185)

    def close_window(self):
        user.delta_p=self.delta_p
        user.p_itog=self.p_itog
        user.Re=self.Re
        user.delta_sheroh_otn=self.delta_sheroh_otn
        user.Re_gr=self.Re_gr
        user.epsilon=self.epsilon
        user.l=self.l
        user.c_p_T_st=self.c_p_T_st

        self.destroy()
        window_8 = Window_8()
        window_8.mainloop()
class Window_8(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2
        self.title("Пересчёт. Все таблицы и графики")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.geometry(f"{1305}x{734}+{10}+{10}")  # Установка размеров окна
        ctk.set_default_color_theme("green")  # Загрузка пользовательской темы
        self.fg_color = 'white'

        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов
        self.iconbitmap('data/prometey.ico')  # Установка иконки окна
        self.configure(bg_color="black")  # Установка цвета фона окна
        ctk.set_appearance_mode("dark")
        self.mono_font = ctk.CTkFont(family="Consolas", size=13)  # или "Courier New"
        self.variant = user.variant
        self.pogresh=100
        self.c_p_T_st=user.c_p_T_st
        self.q_kon_proshl=max(user.q_kon)
        self.number=user.number
        self.X=user.X
        self.Y=user.Y
        self.c_p_T_0g=user.c_p_T_0g
        self.T_st_g=user.T_st_g
        self.T_og=user.T_og
        self.mu_og=user.mu_og
        self.R_og=user.R_og
        self.D_otn=user.D_otn
        self.d_kp=user.d_kp
        self.F_otn=user.F_otn
        self.eps_g=user.eps_g
        self.q_kon=user.q_kon
        self.q_l=user.q_l
        self.q_sum=user.q_sum
        self.betta=user.betta
        self.T_st_otn=user.T_st_otn
        self.lambd=user.lambd
        self.S_1=user.S_1
        self.T_ohl=user.T_ohl
        self.C_p_raznitsa=user.C_p_raznitsa
        self.C_p_ohl=user.C_p_ohl
        self.f=user.f
        self.d_g=user.d_g
        self.delta_reb=user.delta_reb
        self.h=user.h
        self.beta_reb=user.beta_reb
        self.t=user.t
        self.lambda_st_vn=user.lambda_st_vn
        self.T_aray=user.T_aray
        self.p_aray=user.p_aray
        self.rho_aray=user.rho_aray
        self.C_aray=user.C_aray
        self.mu_aray=user.mu_aray
        self.lambda_aray=user.lambda_aray
        self.K_aray=user.K_aray
        self.cooler=user.cooler
        self.alpha_ohl=user.alpha_ohl
        self.kpd_r=user.kpd_r
        self.delta_st=user.delta_st
        self.ind_smena=user.ind_smena
        if self.variant==1 or self.variant==5:
            self.m_ohl_1 = user.m_ohl_1
            self.m_ohl_2 = user.m_ohl_2
            self.index_peret_1 = user.index_peret_1
            self.index_peret_2 = user.index_peret_2
        self.m_ohl=user.m_ohl
        self.lambda_st_vn_1=user.lambda_st_vn
        self.delta_S=user.delta_S
        self.p_ohl=[]
        ooo=0
        for p in user.p_itog:
            self.p_ohl.append(p/1000000)
            print(p/1000000,ooo)
            ooo+=1
        print(len(user.p_ohl),len(self.p_ohl))
        print("------------------------------------------------------------")
        self.T_nach=user.T_nach
        if self.variant == 3 or self.variant == 4:
            self.ind_peret=user.ind_peret
        if self.variant==6:
            self.ind_peret = user.ind_peret
            self.m_ohl_1 = user.m_ohl_1
            self.m_ohl_2 = user.m_ohl_2
            self.T_nach_1=user.T_nach_1
            self.T_nach_2=user.T_nach_2
            self.T_aray_2=user.T_aray_2
            self.p_aray_2=user.p_aray_2
            self.C_aray_2=user.C_aray_2
            self.rho_aray_2=user.rho_aray_2
            self.mu_aray_2=user.mu_aray_2
            self.lambda_aray_2=user.lambda_aray_2
            self.K_aray_2=user.K_aray_2
            self.p_ohl_v_kontse_2=user.p_ohl_v_kontse_2
        self.p_ohl_v_kontse=min(user.p_itog)/1000000
        self.delta_sheroh=0.00575*0.001
        self.t_N=user.t_N
        self.delta_x_s=user.delta_x_s
        self.D=user.D
        self.F = user.F
        self.F_otn=user.F_otn
        self.delta_x=user.delta_x

        self.place_scrollbar()
        self.setup_frame()
        self.solution_to_itog()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def place_scrollbar(self):
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=845, height=470, fg_color='#242424')  # 171717
        self.scrollbar_frame_0.place(x=1, y=1)

    def setup_frame(self):
        """--------------------Создание мини-окон--------------------"""
        self.frame2 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=845, height=5180,
                                   fg_color="#242424", bg_color="transparent")
        self.frame2.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    def raschet_temperatury(self):
        if int(user.variant) == 1:
            T_ohl, C_p_ohl, C_p_raznitsa, m_ohl_array = find_temp_slosh_tema(self.m_ohl_1, self.m_ohl_2,
                                                                             self.index_peret_1, self.index_peret_2,
                                                                             self.delta_S,
                                                                             self.q_sum, self.number, self.p_ohl, user.a,
                                                                             self.T_nach, self.cooler, self.T_aray,
                                                                             self.p_aray, self.C_aray)
        elif int(user.variant) == 5:
            T_ohl, C_p_ohl, C_p_raznitsa, m_ohl_array = find_temp_slozh_5(self.m_ohl_1, self.m_ohl_2,
                                                                             self.index_peret_1, self.index_peret_2,
                                                                             self.delta_S,
                                                                             self.q_sum, self.number, self.p_ohl, user.a,
                                                                             self.T_nach, self.cooler, self.T_aray,
                                                                             self.p_aray, self.C_aray)
        elif int(user.variant) == 2:
            m_ohl_array = [user.m_ohl] * len(user.X)
            T_ohl, C_p_ohl, C_p_raznitsa = find_temp(self.number, self.delta_S, self.p_ohl, self.q_sum, self.m_ohl, user.a,
                                                     self.T_nach, self.cooler, self.T_aray,
                                                     self.p_aray, self.C_aray)
        elif int(user.variant) == 3:
            m_ohl_array = [user.m_ohl] * len(user.X)
            T_ohl, C_p_ohl, C_p_raznitsa = find_temp_slozh_2(self.ind_peret, self.delta_S, self.q_sum, user.a, self.number,
                                                             self.p_ohl, self.m_ohl, self.T_nach,
                                                             self.cooler, self.T_aray, self.p_aray, self.C_aray)
        elif int(user.variant) == 6:
            T_ohl, C_p_ohl, C_p_raznitsa, m_ohl_array=find_temp_slozh_6(self.m_ohl_1,self.m_ohl_2,self.ind_peret,self.delta_S,
                                                                        self.q_sum,self.number,self.p_ohl,user.a,self.T_nach_1,
                                                                        self.T_nach_2,self.T_aray,self.p_aray,self.C_aray,
                                                                        self.T_aray_2,self.p_aray_2,self.C_aray_2)
        else:
            m_ohl_array = [user.m_ohl] * len(user.X)
            T_ohl, C_p_ohl, C_p_raznitsa = find_temp_slozh_1(self.ind_peret, self.delta_S, self.q_sum, user.a, self.number,
                                                             self.p_ohl, self.m_ohl, self.T_nach,
                                                             self.cooler, self.T_aray, self.p_aray, self.C_aray)
        return T_ohl, C_p_ohl, C_p_raznitsa, m_ohl_array
    def rashet_poteri(self):
        if user.variant == 1:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c, self.delta_sheroh, self.u_ohl, self.rho_ohl, self.d_g, self.mu_ohl, self.t_N, self.delta_reb, self.h, self.delta_x_s,
                                     self.beta_reb,
                                     self.p_ohl_v_kontse, self.variant, self.index_peret_1)  # Вывод таблицы №5
        elif user.variant == 5:
            delta_p, p_itog, Re, delta_sheroh_otn, Re_gr, epsilon, l = tabl_5(user.c, self.delta_sheroh, self.u_ohl, self.rho_ohl, self.d_g, self.mu_ohl, self.t_N, self.delta_reb, self.h, self.delta_x_s,
                                     self.beta_reb,
                                     self.p_ohl_v_kontse, self.variant, self.index_peret_2)  # Вывод таблицы №5
        elif user.variant == 2:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c,  self.delta_sheroh,  self.u_ohl,  self.rho_ohl,  self.d_g,  self.mu_ohl,  self.t_N,  self.delta_reb,  self.h,  self.delta_x_s,
                                    self.beta_reb, self.p_ohl_v_kontse,  self.variant)
        elif user.variant == 3:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c, self.delta_sheroh, self.u_ohl, self.rho_ohl, self.d_g, self.mu_ohl, self.t_N, self.delta_reb, self.h, self.delta_x_s,
                                     self.beta_reb,
                                     self.p_ohl_v_kontse,  self.variant,  self.ind_peret)
        elif user.variant == 6:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c, self.delta_sheroh, self.u_ohl, self.rho_ohl, self.d_g, self.mu_ohl, self.t_N, self.delta_reb, self.h, self.delta_x_s,
                                     self.beta_reb,
                                     self.p_ohl_v_kontse,  self.variant,  self.ind_peret,self.p_ohl_v_kontse_2)
        else:
            delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l = tabl_5(user.c,  self.delta_sheroh,  self.u_ohl,  self.rho_ohl,  self.d_g,  self.mu_ohl,  self.t_N,  self.delta_reb,  self.h,  self.delta_x_s,
                                    self.beta_reb,self.p_ohl_v_kontse,  self.variant,  self.ind_peret)
        return delta_p, p_itog,Re,delta_sheroh_otn,Re_gr,epsilon,l
    def solution_to_itog(self):
        gas = ct.Solution('gri30.yaml')  # один раз
        while self.pogresh >= 2:
            self.q_kon, self.betta, self.T_st_otn, self.lambd, self.S_1 = find_q_kon(self.number, self.Y, self.c_p_T_0g,
                                                                                 self.c_p_T_st, self.T_st_g, self.T_og,
                                                                                 self.mu_og, self.R_og, self.D_otn,
                                                                                 self.d_kp, self.F_otn, user.b,
                                                                                 user.result_dedal['p'],
                                                                                 user.result_dedal['k'], 2)
            self.q_l = find_q_l(self.eps_g, user.result_dedal['T'], user.result_ikar['phi_pr'], self.D_otn, self.number,
                            self.Y)
            self.q_sum = find_q_sum(self.q_kon, self.q_l)
            self.q_kon, self.q_l, self.q_sum, user.X, self.betta, self.T_st_otn, self.lambd, self.S_1 = tabl_3(self.q_kon,self.q_l,self.q_sum,self.X,self.betta,self.T_st_otn,self.lambd,self.S_1)  # Вывод таблицы №3
            self.T_ohl, self.C_p_ohl, self.C_p_raznitsa, self.m_ohl_array = self.raschet_temperatury()
            if user.variant == 6:
                self.u_ohl, self.T_ohl, self.C_p_raznitsa, self.C_p_ohl, self.lambda_ohl, self.mu_ohl, self.K_ohl, self.rho_ohl, self.alpha_ohl, self.E, self.kpd_r = tabl_4_AT_NDMG(
                    self.ind_peret,self.T_ohl, self.C_p_raznitsa, self.C_p_ohl, self.p_ohl, self.f, self.m_ohl_array, self.d_g,
                    self.delta_reb,self.h, self.beta_reb, self.t, self.lambda_st_vn, self.T_aray, self.p_aray, self.rho_aray,
                    self.C_aray, self.mu_aray, self.lambda_aray, self.K_aray, self.T_aray_2, self.p_aray_2, self.rho_aray_2,
                    self.C_aray_2,self.mu_aray_2, self.lambda_aray_2, self.K_aray_2, self.cooler)
            else:
                self.u_ohl, self.T_ohl, self.C_p_raznitsa, self.C_p_ohl, self.lambda_ohl, self.mu_ohl, self.K_ohl, self.rho_ohl, self.alpha_ohl, self.E, self.kpd_r = tabl_4(
                self.T_ohl,self.C_p_raznitsa, self.C_p_ohl, self.p_ohl, self.f, self.m_ohl_array, self.d_g, self.delta_reb,
                self.h, self.beta_reb,self.t, self.lambda_st_vn, self.T_aray, self.p_aray, self.rho_aray, self.C_aray, self.mu_aray,
                self.lambda_aray, self.K_aray, self.cooler)  # Вывод таблицы №4
            self.T_st_g, self.T_st_ohl,self.lambda_st_vn,self.lambda_st_vn = find_temp_st_g(self.T_og, self.T_st_g, self.T_ohl, self.alpha_ohl, self.kpd_r,
                                                        self.q_kon, self.q_l, self.delta_st, self.lambda_st_vn, user.d,
                                                        self.number, self.ind_smena, self.lambda_st_vn)
            if user.variant == 5:
                self.T_st_g, self.T_st_ohl = clone_temp_st(self.T_st_g, self.T_st_ohl, len(self.X) - self.index_peret_1,self.X)
            print(f'self.T_st_g={len(self.T_st_g)}')
            self.c_p_T_st = find_params_ks(gas, user.result_dedal["k_m0"],
                                               user.result_ikar["k_m_pr"] / user.result_dedal["k_m0"],
                                               user.result_dedal["H_gor"],
                                               user.result_dedal["H_ox"], user.result_dedal["form_gor"],
                                               user.result_dedal["form_ox"], user.result_dedal["p"], self.T_st_g)
            self.delta_p, self.p_itog,self.Re,self.delta_sheroh_otn,self.Re_gr,self.epsilon,self.l = self.rashet_poteri()
            self.q_kon_nast = (max(self.q_kon))
            self.pogresh = abs(self.q_kon_proshl - self.q_kon_nast) * 100 / self.q_kon_proshl
            print(f'Погрешность с прошлым расчётом составляет: {self.pogresh:.2f} %')
            self.q_kon_proshl = (max(self.q_kon))
        self.print_all_images()
    def print_all_images(self):
        print_nozzle_window(self.X, self.Y, self.frame2,2,10)
        print_cooling_fins_array(user.X, user.n_r_array, user.Y, self.frame2,2,1550)
        print_heat_flows(self.q_kon, self.q_l, self.q_sum, self.X, self.frame2,2,3000)
        print_temp_cooler(self.T_ohl, user.X, self.frame2,2,4480)
        wall_temperatures(self.T_st_g, self.T_st_ohl, user.X, self.frame2,2,5950)
        print_local_pressure_losses(self.delta_p, user.X, self.frame2, 50, 7420, 1)
        print_local_pressure_losses(self.p_itog, user.X, self.frame2, 50, 8230, 2)
        self.print_tabl_1()
        self.print_tabl_2()
        self.print_tabl_3()
        self.print_tabl_4()
        self.print_tabl_5()
        self.print_tabl_6()
        self.print_labels()
        tabl_6(self.T_st_g, self.T_st_ohl)
        print_all_images(self.X, self.Y, user.n_r_array, self.delta_st, self.delta_reb, user.delta_st_nar, self.h,
                         user.D,
                         self.q_kon, self.q_l, self.q_sum, self.T_ohl, self.T_st_g, self.T_st_ohl, self.delta_p,
                         self.p_itog)
    def print_tabl_1(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=700, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=490)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=700, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=10, pady=10)

        # Заголовки таблицы
        headers = ['№', 'X, мм', 'D, мм', 'D отн', 'F, мм²', 'F отн', 'Δx, мм', 'Δx_s, мм', 'ΔS, мм²']
        header_line = "{:<6}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}{:<12}{:<12}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(self.number)):
            x = self.X[i] * 1000
            d = self.D[i] * 1000
            d_otn = self.D_otn[i]
            f = self.F[i] * 1e6
            f_otn = self.F_otn[i]
            delta_x = self.delta_x[i] * 1000
            delta_x_s = self.delta_x_s[i] * 1000
            delta_s = self.delta_S[i] * 1e6
            number = self.number[i]

            # Функция для форматирования с заменой nan на "-"
            def fmt(value):
                return "-" if value is None or (isinstance(value, float) and math.isnan(value)) else f"{value:.2f}"

            # Используем безопасную версию
            line = "{:<6}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}{:<12}{:<12}".format(
                int(number),
                fmt(x),
                fmt(d),
                fmt(d_otn),
                fmt(f),
                fmt(f_otn),
                fmt(delta_x),
                fmt(delta_x_s),
                fmt(delta_s)
            )
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")
    def print_tabl_2(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_2 = ctk.CTkFrame(self.frame2, width=500, height=320, fg_color='black')
        self.scrollbar_frame_2.place(x=30, y=1270)

        # Создание текстового поля
        textbox_2 = ctk.CTkTextbox(self.scrollbar_frame_2, width=500, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox_2.pack(padx=10, pady=10)

        # Заголовки таблицы
        headers = ['№', 'n_р', 't, мм', 't_N, мм', 'f, мм²', 'd_г, мм']
        header_line = "{:<6}{:<10}{:<10}{:<10}{:<12}{:<10}".format(*headers)
        textbox_2.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            n_r = user.n_r_array[i]
            t_0 = round(self.t[i], 3)
            t_N_0 = round(self.t_N[i], 3)
            f_0 = round(self.f[i] * 1e6, 3)
            d_g_0 = round(self.d_g[i], 3)
            number = user.number[i]

            line = "{:<6}{:<10}{:<10.3f}{:<10.3f}{:<12.3f}{:<10.3f}".format(
                int(number), n_r, t_0, t_N_0, f_0, d_g_0
            )
            textbox_2.insert("end", line + "\n")

        textbox_2.configure(state="disabled")
    def print_tabl_3(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=750, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=2050)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=750, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=10, pady=10)

        # Заголовки таблицы
        headers = ['№', 'X,мм', 'λ', 'β', 'S', 'T_ст_отн', 'q_к, МВт/м²', 'q_л, МВт/м²', 'q_сум, МВт/м²']
        header_line = "{:<6}{:<9}{:<9}{:<9}{:<10}{:<10}{:<12}{:<12}{:<12}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            q_kon_0 = round(self.q_kon[i], 3)
            q_l_0 = round(self.q_l[i], 3)
            q_sum_0 = round(self.q_sum[i], 3)
            X_0 = round(self.X[i] * 1000, 3)
            betta_0 = round(self.betta[i], 3)
            T_st_otn_0 = round(self.T_st_otn[i], 3)
            lambd_0 = round(self.lambd[i], 3)
            S_1_0 = round(self.S_1[i], 3)
            number = user.number[i]

            line = "{:<6}{:<9}{:<9}{:<9}{:<10}{:<10}{:<12}{:<12}{:<12}".format(
                int(number), X_0, lambd_0, betta_0, S_1_0, T_st_otn_0, q_kon_0, q_l_0, q_sum_0
            )
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")
    def print_tabl_4(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=750, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=2830)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=750, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=10, pady=10)
        # Заголовки таблицы
        headers = ['№', 'T_охл', 'ΔC,%', 'C_p_охл', 'λ_охл', 'μ_охл⋅10⁴', 'K_охл', 'ρ_охл', 'u_охл', 'α_охл⋅10⁻³',
                   '  E', ' η_р']
        header_line = "{:<5}{:<8}{:<6}{:<9}{:<7}{:<11}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            u_ohl_0 = round(self.u_ohl[i], 2)
            T_ohl_0 = round(self.T_ohl[i], 2)
            C_p_raznitsa_0 = round(self.C_p_raznitsa[i], 3)
            C_p_ohl_0 = round(self.C_p_ohl[i], 2)
            lambda_ohl_0 = round(self.lambda_ohl[i], 2)
            mu_ohl_0 = round(self.mu_ohl[i] * 10000, 4)
            K_ohl_0 = round(self.K_ohl[i], 2)
            rho_ohl_0 = round(self.rho_ohl[i], 2)
            alpha_ohl_0 = round(self.alpha_ohl[i] / 1000, 3)
            E_0 = round(self.E[i], 3)
            kpd_r_0 = round(self.kpd_r[i], 3)
            number = user.number[i]

            line = "{:<5}{:<8}{:<6}{:<9}{:<7}{:<11}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}".format(
                int(number), T_ohl_0, C_p_raznitsa_0, C_p_ohl_0, lambda_ohl_0, mu_ohl_0, K_ohl_0, rho_ohl_0, u_ohl_0,
                alpha_ohl_0, E_0, kpd_r_0)
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")
    def print_tabl_5(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=300, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=3610)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=300, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=10, pady=10)
        # Заголовки таблицы
        headers = ['№', 'T_ст_г', 'T_ст_охл']
        header_line = "{:<6}{:<10}{:<10}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            T_st_g_0 = round(self.T_st_g[i], 2)
            T_st_ohl_0 = round(self.T_st_ohl[i], 2)
            number = user.number[i]

            line = "{:<6}{:<10}{:<10}".format(
                int(number), T_st_g_0, T_st_ohl_0)
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")
    def print_tabl_6(self):
        # Создание скроллируемого текстового блока
        self.scrollbar_frame_1 = ctk.CTkFrame(self.frame2, width=700, height=320, fg_color='black')
        self.scrollbar_frame_1.place(x=30, y=4830)

        # Создание текстового поля
        textbox = ctk.CTkTextbox(self.scrollbar_frame_1, width=700, height=300, fg_color='black', text_color='white',
                                 font=self.mono_font)
        textbox.pack(padx=2, pady=2)
        # Заголовки таблицы
        headers = ['№', 'Re', 'Δ_отн', 'Re_гр', 'ξ', 'l, мм', 'Δ_p, Па']
        header_line = "{:<6}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(*headers)
        textbox.insert("end", header_line + "\n")
        for i in range(len(user.number)):
            delta_p_0 = round(self.delta_p[i], 2)
            Re_0 = round(self.Re[i], 1)
            delta_sheroh_otn_0 = round(self.delta_sheroh_otn[i], 6)
            Re_gr_0 = round(self.Re_gr[i], 1)
            l_0 = round(self.l[i] * 1000, 3)
            epsilon_0 = round(self.epsilon[i], 6)
            number = user.number[i]

            line = "{:<6}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                int(number), Re_0, delta_sheroh_otn_0, Re_gr_0, epsilon_0, l_0, delta_p_0)
            textbox.insert("end", line + "\n")

        textbox.configure(state="disabled")
    def print_labels(self):
        """Визуализация текста в окне"""
        self.label1 = create_label(self.frame2, "Таблица 1", 20, 460)
        self.label1 = create_label(self.frame2, "Таблица 2", 20, 1270-30)
        self.label1 = create_label(self.frame2, "Таблица 3", 20, 2050-30)
        self.label1 = create_label(self.frame2, "Таблица 4", 20, 2800)
        self.label1 = create_label(self.frame2, "Таблица 5", 20, 3610-30)
        self.label1 = create_label(self.frame2, "Таблица 6", 20, 4800)
if __name__ == "__main__":
    app = Window_1()
    app.mainloop()
