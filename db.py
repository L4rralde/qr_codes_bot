import pandas as pd

class Amigo:
    amigos = []
    @staticmethod
    def add_amigo(name: str, curp: str) -> None:
        new_amigo = Amigo(name, curp)
        for amigo in Amigo.amigos:
            if amigo == new_amigo:
                return
        Amigo.amigos.append(new_amigo)

    @staticmethod
    def save_db(path: str = "data.csv") -> None:
        d = {
            "Name": [amigo.name for amigo in Amigo.amigos],
            "Curp": [amigo.curp for amigo in Amigo.amigos]
        }
        df = pd.DataFrame.from_dict(d)
        df.to_csv(path)

    @staticmethod
    def load_db(path: str = "data.csv") -> list:
        Amigo.amigos = []
        df = pd.read_csv(path)
        df.reset_index()
        for _, row in df.iterrows():
            Amigo.add_amigo(row["Name"], row["Curp"])
        return Amigo.amigos

    def __init__(self, name: str, curp: str) -> None:
        self.name = name
        self.curp = curp

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.curp == other.curp

    def __repr__(self) -> str:
        return self.name

DB = Amigo.load_db()
