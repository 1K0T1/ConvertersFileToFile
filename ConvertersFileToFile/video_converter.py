import tkinter as tk                                                                         #модули и библиотеки
from tkinterdnd2 import DND_FILES, TkinterDnD                                                #модули и библиотеки
from pydub import AudioSegment                                                               #модули и библиотеки
from moviepy import VideoFileClip, concatenate_videoclips                                    #модули и библиотеки
import imageio_ffmpeg as ffmpeg                                                              #модули и библиотеки
import os                                                                                    #модули и библиотеки

# Получаем путь к встроенному ffmpeg
ffmpeg_path = ffmpeg.get_ffmpeg_exe()

# Настраиваем pydub для использования этого ffmpeg
VideoFileClip.converter = ffmpeg_path

class VideoConverter(tk.Frame):
    def __init__(self, parent, controller):
        super(). __init__(parent)
        self.controller = controller

        self.formats = [
            "MP4", "AVI", 
            "MOV", "MKV", 
            "WebM", "FLV", 
            "OGV", "3GP", 
            "MPEG", "TS", 
            "MTS", "WMV", 
            "ASF", "F4V", 
            "RMVB", "MXF", 
            "AMV", "DVR-MS"
        ]
        
        self.audio_codec = {
            "MP4": ["aac", "libmp3lame", "ac3"],
            "AVI": ["libmp3lame", "pcm_s16le"],
            "MOV": ["aac", "pcm_s16le"],
            "MKV": ["libopus", "libvorbis", "aac"],
            "WebM": ["libopus", "libvorbis"],
            "FLV": ["libmp3lame", "aac"], 
            "OGV": ["libvorbis"],
            "3GP": ["libopencore_amrnb", "aac"], 
            "MPEG": ["mp2", "libmp3lame"],
            "TS": ["aac", "ac3"], 
            "MTS": ["pcm_s16le", "ac3"],
            "WMV": ["wmav2"], 
            "ASF": ["wmav2"],
            "F4V": ["aac"], 
            "RMVB": ["realaudio"],
            "MXF": ["pcm_s16le", "aac"], 
            "AMV": ["libopencore_amrnb"],
            "DVR-MS": ["mp2"]
        }
        
        self.video_codec = {
            "MP4": ["libx264", "libx265", "libaom-av1"],
            "AVI": ["mpeg4", "mjpeg", "rawvideo"], 
            "MOV": ["prores", "libx264", "libx265"],
            "MKV": ["libx264", "libx265", "libvpx", "libvpx-vp9", "libaom-av1"], 
            "WebM": ["libvpx", "libvpx-vp9", "libaom-av1"],
            "FLV": ["flv", "libx264"], 
            "OGV": ["libtheora"],
            "3GP": ["h263", "libx264"], 
            "MPEG": ["mpeg1video", "mpeg2video"],
            "TS": ["libx264", "mpeg2video"], 
            "MTS": ["libx264"],
            "WMV": ["wmv2"],
            "ASF": ["wmv2", "mpeg4"],
            "F4V": ["libx264"],
            "RMVB": ["realvideo"],
            "MXF": ["prores", "libx264", "mpeg2video"], 
            "AMV": ["amv"],
            "DVR-MS": ["mpeg2video"]
        }
        
        self.choice_codec = ["Для начала нужен формат"]
        
        # вернутся назад
        tk.Button(self, text="Назад", command=lambda: controller.show_frame("StartWindow")).place(relx=0.9, rely=0.1 ,anchor="center")
        
        def not_convert():        #функция работает если не перетащили файл
            self.label_info.config(text="Для начала перетащите файл")
            
        def log_error(self, text_log=None):
            self.label_error.config(text=text_log)
            #Убераем каждые 5 сек
            self.after(5000, lambda: self.label_error.config(text=""))
        
        def DandD(event): #функция работае тогда когда файл переташили
            self.dropped_file = event.data.strip("{}")                # убираем фигурные скобки (если путь содержит пробелы)
            self.label_drop.config(text=f"Файл: {self.dropped_file}") # меняем text на путь к файлу
            
            for key, value in self.video_codec.items():
                if key == self.list_format.get():
                    new_menu = value
                    menu = self.dropdown2['menu']  # Доступ к внутреннему меню
                    menu.delete(0, 'end')          # Очищаем старые опции
                    #меняем список
                    for option in new_menu:
                        menu.add_command(label=option, command=tk._setit(self.list_video, option))
                    self.list_video.set(value[0])
                    print(value)
                    print(f"формат {key}") 

            for key, value in self.audio_codec.items():
                if key == self.list_format.get():
                    new_menu = value
                    menu = self.dropdown3['menu']  # Доступ к внутреннему меню
                    menu.delete(0, 'end')          # Очищаем старые опции
                    #меняем список
                    for option in new_menu:
                        menu.add_command(label=option, command=tk._setit(self.list_audio, option))
                    self.list_audio.set(value[0])
                    print(value)
                    print(f"формат {key}") 
            try:
                def convert_button():
                    # Загружаем видео файл
                    self.clip = VideoFileClip(fr"{self.dropped_file}")
                    
                    # Конвертируем в MP4
                    self.clip.write_videofile(f"video.{self.list_format.get().lower()}", codec=f"{self.list_video.get()}", audio_codec=f"{self.list_audio.get()}")
                    log_error(self, f"Файл конвертирован в video.{self.list_format.get().lower()}")
                self.label_info.config(text="Можно конвертировать")
                self.convert.config(command=convert_button)
            except:
                log_error(self, "Не возможно конвертировать файл!")

        self.label_drop = tk.Label(self, text="Перетащи сюда файл", bg="#ffffff", width=40, height=10, relief="ridge")  #виджет с характеристиками
        self.label_drop.place(relx=0.4, rely=0.01, width=300, height=100)
        self.label_dropdown = tk.Label(self, text="Выберите формат и кодек файла:", font=("Helvetica", 14)) #виджет с текстом
        self.label_dropdown.place(relx=0.18, rely=0.1 ,anchor="center")
        
        self.label_error = tk.Label(self, text="", font=("Helvetica", 14))
        self.label_error.place(relx=0.7, rely=0.6, anchor="center")
        
        # виджет с информацие об конвертации
        self.label_info = tk.Label(self, text="Перетащите файл")
        self.label_info.place(relx=0.4, rely=0.3)
        
        # кнопка конвертации
        self.convert = tk.Button(self, text="Конвертировать", command=not_convert)
        self.convert.place(relx=0.4, rely=0.22)
        
        #Форматы
        self.list_format = tk.StringVar(value=self.formats[0])
        self.dropdown1 = tk.OptionMenu(self, self.list_format, *self.formats)
        self.dropdown1.place(relx=0.32, rely=0.16, anchor="center")
    
        #список видео кодеков
        self.list_video = tk.StringVar(value=self.choice_codec[0])
        self.dropdown2 = tk.OptionMenu(self, self.list_video, *self.choice_codec)
        self.dropdown2.place(relx=0.13, rely=0.16, anchor="center")   
        
        #список аудио кодеков
        self.list_audio = tk.StringVar(value=self.choice_codec[0])
        self.dropdown3 = tk.OptionMenu(self, self.list_audio, *self.choice_codec)
        self.dropdown3.place(relx=0.13, rely=0.2, anchor="center")    
        
        # Регистрируем виджет "label" как цель для Drag and Drop файлов (тип DND_FILES означает, что можно перетаскивать файлы)
        self.label_drop.drop_target_register(DND_FILES)
        # Привязываем обработчик "DandD" к событию "<<Drop>>", которое возникает, когда пользователь отпускает файл на виджет
        self.label_drop.dnd_bind("<<Drop>>", DandD)