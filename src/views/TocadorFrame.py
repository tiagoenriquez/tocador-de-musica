from functools import partial
from mutagen.mp3 import MP3
from pygame import mixer
import threading
import tkinter as tk
import time

from src.adapters.DuracaoAdapter import DuracaoAdapter
from src.controllers.MusicaController import MusicaController
from src.models.Album import Album
from src.views.MainFrame import MainFrame


class TocadorFrame:
    def __init__(self, frame: MainFrame, album: Album) -> None:
        self._my_frame = frame
        self._album = album
        self._tocando = False
        self._id_selecionado = 0
        self._musica_thread: threading.Thread | None = None
        self._tempo = 0
        self._contador_thread: threading.Thread | None = None
        self._my_frame.clean()
        self._window = frame.window
        self._window.title(f"Tocador de Música - {album.nome}")

        self._panel = tk.Frame(self._window)
        self._panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._static_panel = tk.Frame(self._panel)
        self._static_panel.grid(row=0, column=0, padx=8, pady=8)

        self._escolher_button = tk.Button(
            self._static_panel,
            text="Selecionar outra pasta",
            command=self._selecionar_pasta
        )
        self._escolher_button.grid(row=0, column=0, padx=8, pady=8)

        self._tocando_panel = tk.Frame(self._static_panel)
        self._tocando_panel.grid(row=1, column=0)

        self._tocando_label = tk.Label(self._tocando_panel, text="Tocando")
        self._tocando_label.grid(row=0, column=0, padx=8, pady=8)

        self._musica_label = tk.Label(self._tocando_panel, text=album.musicas[0].filename.split("/")[-1])
        self._musica_label.grid(row=0, column=1, padx=8, pady=8)
        
        self._play_button = tk.Button(self._tocando_panel, text="▶", command=self._criar_thread_musical)
        self._play_button.grid(row=0, column=2, padx=8, pady=8)
        
        self._pause_button = tk.Button(self._tocando_panel, text="⏸", command=self._parar_musica)
        self._pause_button.grid(row=0, column=3, padx=8, pady=8)

        self._volume_slider = tk.Scale(self._tocando_panel, orient="horizontal", command=self._controlar_volume)
        self._volume_slider.grid(row=0, column=4, padx=8, pady=8)
        self._volume_slider.set(50)

        self._tempo_label = tk.Label(self._tocando_panel, text=DuracaoAdapter(0).to_str())
        self._tempo_label.grid(row=0, column=5, padx=8, pady=8)

        self._canvas = tk.Canvas(self._panel, height=400, width=770)
        self._canvas.grid(row=1, column=0, padx=8, pady=8, sticky="news")
        self._vertical_scrollbar = tk.Scrollbar(self._panel, orient=tk.VERTICAL, command=self._canvas.yview, width=10)
        self._vertical_scrollbar.grid(row=1, column=1, sticky="ns")
        self._canvas.config(yscrollcommand=self._vertical_scrollbar.set)

        self._musicas_panel = tk.Frame(self._canvas)
        self._canvas.create_window((0, 0), window=self._musicas_panel, anchor="center")

        duracao_total = 0
        for i, musica in enumerate(album.musicas):
            nome_label = tk.Label(self._musicas_panel, text=musica.filename.split("/")[-1])
            nome_label.grid(row=i, column=0, padx=8, pady=8)
        
            select_button = tk.Button(
                self._musicas_panel,
                text="▶",
                command=partial(self._selecionar_musica, musica, i)
            )
            select_button.grid(row=i, column=1, padx=8, pady=8)

            duracao = musica.info.length
            duracao_total += duracao
            duracao_label = tk.Label(self._musicas_panel, text=DuracaoAdapter(duracao).to_str())
            duracao_label.grid(row=i, column=2, padx=8, pady=8)
        
        row = len(album.musicas)
        self._total_label = tk.Label(self._musicas_panel, text="Total")
        self._total_label.grid(row=row, column=0, padx=8, pady=8)

        self._duracao_total_label = tk.Label(self._musicas_panel, text=DuracaoAdapter(duracao_total).to_str())
        self._duracao_total_label.grid(row=row, column=2, padx=8, pady=8)
        
        self._musicas_panel.update_idletasks()
        self._canvas.create_window((self._canvas.winfo_width() / 2, 0), window=self._musicas_panel, anchor="n")
        self._canvas.yview_moveto(0)
        
        self._my_frame.keep_open()
    
    def _selecionar_pasta(self) -> None:
        MusicaController().abrir_seletor(self._my_frame)
    
    def _selecionar_musica(self, musica: MP3, id: int) -> None:
        self._musica_label["text"] = musica.filename.split("/")[-1]
        self._id_selecionado = id
        self._parar_musica()
    
    def _tocar(self) -> None:
        mixer.init()
        for i in range(self._id_selecionado, len(self._album.musicas)):
            self._musica_label["text"] = self._album.musicas[i].filename.split("/")[-1]
            self._tempo = 0
            self._tempo_label["text"] = DuracaoAdapter(0).to_str()
            if not self._tocando:
                break
            mixer.music.load(self._album.musicas[i].filename)
            mixer.music.play()
            self._controlar_volume(str(self._volume_slider.get()))
            while mixer.music.get_busy() and self._tocando:
                time.sleep(0.1)
            if not self._tocando:
                mixer.stop()
                break
            self._id_selecionado = i + 1
        mixer.quit()

    def _contar_tempo(self) -> None:
        while self._tocando:
            time.sleep(1)
            self._tempo += 1
            self._tempo_label["text"] = DuracaoAdapter(self._tempo).to_str()
        self._tempo_label["text"] = DuracaoAdapter(0).to_str()
    
    def _criar_contador_thread(self) -> None:
        self._contador_thread = threading.Thread(target=self._contar_tempo, daemon=True)
        self._contador_thread.start()
        
    def _criar_thread_musical(self) -> None:
        if not self._tocando:
            self._tocando = True
            self._criar_contador_thread()
            self._musica_thread = threading.Thread(target=self._tocar)
            self._musica_thread.start()
    
    def _parar_musica(self) -> None:
        self._tocando = False
        if mixer.get_init():
            mixer.music.stop()
        if self._musica_thread is not None:
            self._musica_thread.join()
            self._tempo_label["text"] = DuracaoAdapter(0).to_str()
            self._tempo = 0
    
    def _controlar_volume(self, value: str) -> None:
        if self._tocando:
            mixer.music.set_volume(float(value) / 100)