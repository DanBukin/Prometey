"""
Модуль определяет пользовательские виджеты и стили на базе `customtkinter`.

Используется для:
- Создания кнопок, полей ввода и других элементов UI,
- Применения единого визуального стиля ко всем окнам программы,
- Управления цветами, шрифтами, тенями, размерами.

Позволяет быстро стилизовать интерфейс приложения под нужды пользователя.
"""
import customtkinter as ctk
import os
from PIL import Image
from ctypes import windll
from matplotlib.ticker import FuncFormatter


formatter = FuncFormatter(lambda x, _: f"{x:.0f}")

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", FR_PRIVATE, 0)
else:
    pass

font0 = ("Futura PT Book", 18)  # Настройка пользовательского шрифта 1
font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 2
font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 3
canvas_widget = None
k_1=0
FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", FR_PRIVATE, 0) # Загрузка пользовательского шрифта
else:
    pass
def create_frame(parent,wight, height, x, y, fg_color, bg_color):
    frame = ctk.CTkFrame(master=parent,width=wight, height=height, fg_color=fg_color, bg_color=bg_color)
    frame.place(x=x, y=y)
    return frame
def create_entry(parent, wight, textvariable, x, y):
    Entry = ctk.CTkEntry(master=parent, width=wight, textvariable=textvariable)
    Entry.place(x=x, y=y)
def create_label(parent, text, x, y):
    label = ctk.CTkLabel(parent, text=text, font=font1)
    label.place(x=x, y=y)
    return label
def create_label_left(parent, text, x, y):
    label = ctk.CTkLabel(parent, text=text, font=font1, justify='left')
    label.place(x=x, y=y)
    return label
def create_label_red(parent, text, x, y):
    label = ctk.CTkLabel(parent, text=text, font=font1,fg_color="#B62626", corner_radius=10)
    label.place(x=x, y=y)
    return label
def create_button(parent, text, command, font, width, x, y):
    button = ctk.CTkButton(master=parent, text=text, command=command, font=font, width=width)
    button.place(x=x, y=y)
    return button
def toggle_cooling_frame(self):
    if hasattr(self, "cooling_frame_visible") and self.cooling_frame_visible:
        self.scrollbar_frame_1.place_forget()
        self.cooling_frame_visible = False
    else:
        if not hasattr(self, "scrollbar_frame_1"):
            self.scrollbar_frame_1 = ctk.CTkScrollableFrame(self, width=400, height=390, fg_color='#1A1A1A')
            self.scrollbar_frame_1.place(x=435, y=40)

            image_path = os.path.join("data", "scheme", "all_variants.png")
            image = Image.open(image_path)
            image = image.resize((round(796), round(2039)))
            self.cooling_image = ctk.CTkImage(light_image=image, size=(round(796 * 0.45), round(3028 * 0.45)))

            self.image_label = ctk.CTkLabel(self.scrollbar_frame_1, image=self.cooling_image, text="")
            self.image_label.pack(padx=10, pady=10)
        else:
            self.scrollbar_frame_1.place(x=435, y=40)

        self.cooling_frame_visible = True
def toggle_info_frame(self):
    if hasattr(self, "info_frame_visible") and self.info_frame_visible:
        self.frame_2.place_forget()
        self.info_frame_visible = False
    else:
        if not hasattr(self, "frame_2"):
            self.frame_2 = ctk.CTkFrame(self, width=500, height=500, fg_color='#1A1A1A')
            self.frame_2.place(x=435, y=40)
            image_path = os.path.join("data", "scheme", "info.png")
            image = Image.open(image_path)
            image = image.resize((793, 785))
            self.info_image = ctk.CTkImage(light_image=image, size=(round(793 * 0.5), round(785 * 0.5)))

            self.image_label = ctk.CTkLabel(self.frame_2, image=self.info_image, text="")
            self.image_label.pack(padx=2, pady=2)
        else:
            self.frame_2.place(x=435, y=40)

        self.info_frame_visible = True