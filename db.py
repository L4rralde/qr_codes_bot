"""
Handles all data required to idenfity a passenger
"""

import pandas as pd

class Amigo:
    """
    Class of a Passenger friend
    """
    amigos = []
    @staticmethod
    def add_amigo(name: str, curp: str) -> None:
        """
        Adds another Amigo to the database
        """
        new_amigo = Amigo(name, curp)
        for amigo in Amigo.amigos:
            if amigo == new_amigo:
                return
        Amigo.amigos.append(new_amigo)
        Amigo.save_db()

    @staticmethod
    def save_db(path: str = "data.csv") -> None:
        """Saves list of Amigos into a csv file (database)"""
        d = {
            "Name": [amigo.name for amigo in Amigo.amigos],
            "Curp": [amigo.curp for amigo in Amigo.amigos]
        }
        df = pd.DataFrame.from_dict(d)
        df.to_csv(path)

    @staticmethod
    def load_db(path: str = "data.csv") -> list:
        """Loads list of Amigos from csv file (database)"""
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
        return self.name == other.name

    def __repr__(self) -> str:
        return self.name

AMIGOS = Amigo.load_db()
