from mutagen.mp3 import MP3


class Album:
    def __init__(self, diretorio: str, musicas: list[MP3]) -> None:
        self.diretorio = diretorio
        self.nome = diretorio.split("/")[-1]
        self.musicas = musicas