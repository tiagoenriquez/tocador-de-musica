import re
from mutagen.mp3 import MP3
import os

from src.models.Album import Album


class MusicaDao:
    def listar_musicas(self, diretorio: str) -> Album:
        musicas: list[MP3] = []
        for arquivo in os.listdir(diretorio):
            partes = arquivo.split(".")
            if partes[len(partes) - 1] == "mp3":
                musicas.append(MP3(f"{diretorio}/{arquivo}"))
        def extrair_numero(musica) -> int | float:
            match = re.search(r'^\d+', os.path.basename(musica.filename))
            return int(match.group()) if match else float('inf')
        musicas.sort(key=extrair_numero)
        return Album(diretorio, musicas)