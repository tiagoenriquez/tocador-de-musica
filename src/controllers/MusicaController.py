from src.daos.MusicaDao import MusicaDao
from src.views.MainFrame import MainFrame


class MusicaController:
    def abrir_seletor(self, frame: MainFrame) -> None:
        from src.views.SeletorFrame import SeletorFrame
        SeletorFrame(frame)
    
    def abrir_tocador(self, frame: MainFrame, diretorio: str) -> None:
        from src.views.TocadorFrame import TocadorFrame
        TocadorFrame(frame, MusicaDao().listar_musicas(diretorio))