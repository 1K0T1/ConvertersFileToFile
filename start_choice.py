import tkinter as tk


class StartWindow(tk.Frame):  # фрейм класс
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Экран выбора").pack(pady=10)
        # кнопка перехода на новый экран
        tk.Button(
            self,
            text="Конвертировать картинки",
            command=lambda: controller.show_frame("ImageToImage"),
        ).pack()
        tk.Button(
            self,
            text="Конвертировать звуки",
            command=lambda: controller.show_frame("SoundConverter"),
        ).pack()
        tk.Button(
            self,
            text="Конвертировать видео",
            command=lambda: controller.show_frame("VideoConverter"),
        ).pack()
