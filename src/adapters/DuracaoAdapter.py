class DuracaoAdapter:
    def __init__(self, duracao: int) -> None:
        self.duracao = duracao

    def to_str(self) -> str:
        horas = int(self.duracao / 3600)
        minutos = int(self.duracao / 60 - horas * 60)
        segundos = int(self.duracao % 60)
        return f"{str(horas).zfill(2)}:{str(minutos).zfill(2)}:{str(segundos).zfill(2)}"