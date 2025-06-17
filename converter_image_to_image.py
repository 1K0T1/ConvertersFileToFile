from PIL import (
    Image,
    ImageFilter,
    ImageFont,
    ImageDraw,
    ImageEnhance,
    ImageOps,
    ExifTags,
)  # модули и библиотеки
import tkinter as tk  # модули и библиотеки
from tkinter import ttk, filedialog  # модули и библиотеки
from tkinterdnd2 import DND_FILES, TkinterDnD  # модули и библиотеки
from pathlib import Path  # модули и библиотеки


class ImageToImage(tk.Frame):  # фрейм класс
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # список с форматами
        self.options = [
            "JPEG",
            "JPG",
            "PNG",
            "BMP",
            "GIF",
            "TIFF",
            "ICO",
            "WEBP",
            "PPM",
            "PGM",
            "PDF",
            "EPS",
            "DDS",
            "XBM",
            "TGA",
            "IM",
        ]
        # ключи для конвертации
        self.format_to_mode = {
            "JPEG": "RGB",
            "JPG": "RGB",
            "PNG": "RGBA",
            "BMP": "RGB",
            "GIF": "P",
            "TIFF": "RGBA",
            "ICO": "RGBA",
            "WEBP": "RGBA",
            "PPM": "RGB",
            "PGM": "L",
            "PDF": "RGB",
            "EPS": "RGB",
            "DDS": "RGBA",
            "XBM": "1",
            "TGA": "RGBA",
            "IM": "RGB",
        }

        self.ban_symbols = r"\/:*?\"<>|\'"

        # вернутся назад
        tk.Button(
            self, text="Назад", command=lambda: controller.show_frame("StartWindow")
        ).place(relx=0.9, rely=0.1, anchor="center")

        def log_error(self, text_log=None):
            self.label_error.config(text=text_log)
            # Убераем каждые 5 сек
            self.after(5000, lambda: self.label_error.config(text=""))

        # если название не введено или есть запрещенный символ то название будет первоначальным
        def button_click():
            try:
                self.default_name = self.entry.get()
                if self.entry.get() == "":
                    self.default_name = Path(
                        self.dropped_file
                    ).stem  # берем только название файла
                for ban_symbol in self.ban_symbols:
                    for symbol in self.default_name:
                        if ban_symbol == symbol:
                            self.default_name = Path(
                                self.dropped_file
                            ).stem  # берем только название файла
                            self.label_error.config(
                                text=r"Нельзя ставить запрещенные символы (\/:*?\"<>|\')"
                            )
                            # Убераем каждые 5 сек
                            self.after(5000, lambda: self.label_error.config(text=""))
            except:
                self.label_error.config(text="Для начала перетащите файл")
                # Убераем каждые 5 сек
                self.after(5000, lambda: self.label_error.config(text=""))

        # функция работает если не перетащили файл
        def not_convert():
            self.label_info.config(text="Для начала перетащите файл")

        # функция для виджета куда можно переташить файл
        def DandD(event):  # функция работае тогда когда файл переташили

            self.dropped_file = event.data.strip(
                "{}"
            )  # убираем фигурные скобки (если путь содержит пробелы)
            self.label_drop.config(
                text=f"Файл: {self.dropped_file}"
            )  # меняем text на путь к файлу
            try:
                self.img = Image.open(self.dropped_file)  # отыкрываем файл

                if self.entry.get() == "":
                    self.default_name = Path(self.dropped_file).stem

                for (
                    key,
                    value,
                ) in self.format_to_mode.items():  # перебераем форматы до нужного
                    if self.list_format.get() == key:

                        def convert_button():
                            try:
                                self.img = self.img.convert(
                                    f"{value}"
                                )  # сохраняем в выбраный формат
                                # того или иного формата то меняем на её режим
                                self.img.save(
                                    f"{self.default_name}.{self.list_format.get().lower()}"
                                )
                                log_error(
                                    self,
                                    f"Файл конвертирован в {self.default_name}.{self.list_format.get().lower()}",
                                )
                            except:
                                log_error(
                                    self,
                                    "Не возможно конвертировать файл!\nФайл поврежден или не поддерживаемый формат",
                                )

                        self.label_info.config(text="Можно конвертировать")
                        self.convert.config(command=convert_button)
            except:
                log_error(
                    self,
                    "Не возможно конвертировать файл!\nФайл поврежден или не поддерживаемый формат",
                )
            # для консоли
            print(self.dropped_file)

        self.but_name = tk.Button(self, text="сохранить название", command=button_click)
        self.but_name.place(relx=0.2, rely=0.95, anchor="center", width=200, height=30)

        self.list_format = tk.StringVar(value=self.options[0])
        self.dropdown = tk.OptionMenu(self, self.list_format, *self.options)
        self.dropdown.place(relx=0.17, rely=0.16, anchor="center")
        self.label_dropdown = tk.Label(
            self, text="Выберите формат файла:", font=("Helvetica", 14)
        )  # виджет с текстом
        self.label_dropdown.place(relx=0.18, rely=0.1, anchor="center")

        self.entry = tk.Entry(
            self, font=("Helvetica", 14), cursor="xterm", justify="center"
        )  # поле для названия
        self.entry.place(relx=0.6, rely=0.95, anchor="center", width=300, height=30)
        self.label_name = tk.Label(
            self,
            text="Введи название для конвертированного файла:",
            font=("Helvetica", 14),
        )
        self.label_name.place(relx=0.6, rely=0.88, anchor="center")

        self.label_drop = tk.Label(
            self,
            text="Перетащи сюда файл",
            bg="#ffffff",
            width=40,
            height=10,
            relief="ridge",
        )  # виджет с характеристиками
        self.label_drop.place(relx=0.4, rely=0.01, width=300, height=100)

        # виджет с информацие об конвертации
        self.label_info = tk.Label(self, text="Перетащите файл")
        self.label_info.place(relx=0.4, rely=0.3)

        # кнопка конвертации
        self.convert = tk.Button(self, text="Конвертировать", command=not_convert)
        self.convert.place(relx=0.4, rely=0.22)

        self.label_error = tk.Label(self, text="", font=("Helvetica", 14))
        self.label_error.place(relx=0.7, rely=0.5, anchor="center")

        # Регистрируем виджет `label` как цель для Drag and Drop файлов (тип DND_FILES означает, что можно перетаскивать файлы)
        self.label_drop.drop_target_register(DND_FILES)
        # Привязываем обработчик `DandD` к событию "<<Drop>>", которое возникает, когда пользователь отпускает файл на виджет
        self.label_drop.dnd_bind("<<Drop>>", DandD)
