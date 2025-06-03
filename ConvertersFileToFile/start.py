from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageEnhance, ImageOps, ExifTags   #модули и библиотеки
import tkinter as tk                                                                         #модули и библиотеки
from tkinter import ttk, filedialog                                                          #модули и библиотеки
from tkinterdnd2 import DND_FILES, TkinterDnD                                                #модули и библиотеки
import os                                                                                    #модули и библиотеки
from start_choice import StartWindow                                                         #импорт класса скрипта начала
from converter_image_to_image import ImageToImage                                            #импорт класса скрипта конвертера форматов картинок
from sound_converter import SoundConverter                                                   #импорт класса скрипта конвертера форматов звуков
from video_converter import VideoConverter                                                   #импорт класса скрипта конвертера форматов видео
import subprocess                                                                            #модули и библиотеки
from moviepy import VideoFileClip, concatenate_videoclips                                    #модули и библиотеки
import imageio_ffmpeg as ffmpeg                                                              #модули и библиотеки

class Foundation(TkinterDnD.Tk): # класс как tk только для tkinterdnd2
    def __init__(self):
        super().__init__()
        self.title("Конвертатор")
        self.geometry("800x700")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        
        self.frames = {}
        # cоздаём объект каждого и добавляем его в словарь
        for F in (StartWindow, ImageToImage, SoundConverter, VideoConverter):
            name = F.__name__
            try:
                print(f"Инициализация: {name}")
                frame = F(container, self)
                self.frames[name] = frame
                #помещаем каждый экран точно в то же место, чтобы потом можно было просто их "поднимать"
                frame.place(relx=0, rely=0, relwidth=1, relheight=1) 
            except Exception as e:
                print(f"Ошибка при инициализации {name}: {e}")

        self.show_frame("StartWindow")
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

if __name__ == "__main__":
    app = Foundation()
    app.mainloop()
