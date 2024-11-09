import tkinter as tk
from tkinter.filedialog import askdirectory

from src.controllers.MusicaController import MusicaController
from src.views.MainFrame import MainFrame


class SeletorFrame:
    def __init__(self, frame: MainFrame) -> None:
        self._my_frame = frame
        self._my_frame.clean()
        self._window = frame.window
        self._window.title("Tocador de Música - Seletor de Diretório")

        self._panel = tk.Frame(self._window)
        self._panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._escolher_pasta_button = tk.Button(self._panel, text="Escolha uma pasta", command=self._escolher_pasta)
        self._escolher_pasta_button.grid(row=0, column=0, padx=8, pady=8)

        self._entry = tk.Entry(self._panel, width=32)
        self._entry.grid(row=0, column=1, padx=8, pady=8)

        self._tocar_button = tk.Button(self._panel, text="Tocar", command=self._tocar)
        self._tocar_button.grid(row=0, column=2, padx=8, pady=8)
        
        self._my_frame.keep_open()
    
    def _escolher_pasta(self) -> None:
        self._entry.insert(0, askdirectory(initialdir="/home/tiago/Música"))
    
    def _tocar(self) -> None:
        MusicaController().abrir_tocador(self._my_frame, self._entry.get())