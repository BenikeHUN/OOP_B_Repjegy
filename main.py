from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Jarat(ABC):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: int, indulas: datetime, kapacitas: int):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar
        self.indulas = indulas
        self.kapacitas = kapacitas

    @property
    def jaratszam(self):
        return self.__jaratszam

    @jaratszam.setter
    def jaratszam(self, ertek):
        if not ertek or not isinstance(ertek, str):
            raise ValueError("A járatszám nem lehet üres.")
        self.__jaratszam = ertek

    @property
    def celallomas(self):
        return self.__celallomas

    @celallomas.setter
    def celallomas(self, ertek):
        if not ertek or not isinstance(ertek, str):
            raise ValueError("A célállomás nem lehet üres.")
        self.__celallomas = ertek

    @property
    def jegyar(self):
        return self.__jegyar

    @jegyar.setter
    def jegyar(self, ertek):
        if not isinstance(ertek, int) or ertek <= 0:
            raise ValueError("A jegyárnak pozitív egész számnak kell lennie.")
        self.__jegyar = ertek

    @property
    def indulas(self):
        return self.__indulas

    @indulas.setter
    def indulas(self, ertek):
        if not isinstance(ertek, datetime):
            raise ValueError("Az indulásnak datetime típusúnak kell lennie.")
        self.__indulas = ertek

    @property
    def kapacitas(self):
        return self.__kapacitas

    @kapacitas.setter
    def kapacitas(self, ertek):
        if not isinstance(ertek, int) or ertek <= 0:
            raise ValueError("A kapacitásnak pozitív egész számnak kell lennie.")
        self.__kapacitas = ertek

    @abstractmethod
    def jarat_tipusa(self):
        pass

    def __str__(self):
        indulas_szoveg = self.indulas.strftime("%Y-%m-%d %H:%M")
        return (
            f"{self.jaratszam} | {self.jarat_tipusa()} | "
            f"Cél: {self.celallomas} | Ár: {self.jegyar} Ft | "
            f"Indulás: {indulas_szoveg} | Kapacitás: {self.kapacitas}"
        )


class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: int, indulas: datetime, kapacitas: int):
        super().__init__(jaratszam, celallomas, jegyar, indulas, kapacitas)

    def jarat_tipusa(self):
        return "Belföldi járat"


class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam: str, celallomas: str, jegyar: int, indulas: datetime, kapacitas: int, orszag: str):
        super().__init__(jaratszam, celallomas, jegyar, indulas, kapacitas)
        self.orszag = orszag

    @property
    def orszag(self):
        return self.__orszag

    @orszag.setter
    def orszag(self, ertek):
        if not ertek or not isinstance(ertek, str):
            raise ValueError("Az ország nem lehet üres.")
        self.__orszag = ertek

    def jarat_tipusa(self):
        return f"Nemzetközi járat ({self.orszag})"


class LegiTarsasag:
    def __init__(self, nev: str):
        self.nev = nev
        self.__jaratok = {}

    @property
    def nev(self):
        return self.__nev

    @nev.setter
    def nev(self, ertek):
        if not ertek or not isinstance(ertek, str):
            raise ValueError("A légitársaság neve nem lehet üres.")
        self.__nev = ertek

    def jarat_hozzaadasa(self, jarat: Jarat):
        if not isinstance(jarat, Jarat):
            raise ValueError("Csak Jarat típusú objektum adható hozzá.")

        if jarat.jaratszam in self.__jaratok:
            raise ValueError("Már létezik ilyen járatszám.")

        self.__jaratok[jarat.jaratszam] = jarat

    def jarat_keresese(self, jaratszam: str):
        return self.__jaratok.get(jaratszam)

    def jaratok_listazasa(self):
        return list(self.__jaratok.values())


class JegyFoglalas:
    def __init__(self, foglalas_id: int, utas_nev: str, jarat: Jarat):
        self.foglalas_id = foglalas_id
        self.utas_nev = utas_nev
        self.jarat = jarat
        self.__foglalas_ideje = datetime.now()

    @property
    def foglalas_id(self):
        return self.__foglalas_id

    @foglalas_id.setter
    def foglalas_id(self, ertek):
        if not isinstance(ertek, int) or ertek <= 0:
            raise ValueError("A foglalás azonosítójának pozitív egész számnak kell lennie.")
        self.__foglalas_id = ertek

    @property
    def utas_nev(self):
        return self.__utas_nev

    @utas_nev.setter
    def utas_nev(self, ertek):
        if not ertek or not isinstance(ertek, str):
            raise ValueError("Az utas neve nem lehet üres.")
        self.__utas_nev = ertek

    @property
    def jarat(self):
        return self.__jarat

    @jarat.setter
    def jarat(self, ertek):
        if not isinstance(ertek, Jarat):
            raise ValueError("A foglaláshoz érvényes járat szükséges.")
        self.__jarat = ertek

    @property
    def foglalas_ideje(self):
        return self.__foglalas_ideje

    def __str__(self):
        foglalas_ido = self.foglalas_ideje.strftime("%Y-%m-%d %H:%M")
        return (
            f"Foglalás ID: {self.foglalas_id} | "
            f"Utas: {self.utas_nev} | "
            f"Járat: {self.jarat.jaratszam} | "
            f"Cél: {self.jarat.celallomas} | "
            f"Ár: {self.jarat.jegyar} Ft | "
            f"Foglalás ideje: {foglalas_ido}"
        )


class FoglalasiRendszer:
    def __init__(self, legitarsasag: LegiTarsasag):
        self.__legitarsasag = legitarsasag
        self.__foglalasok = {}
        self.__kovetkezo_id = 1

    @property
    def legitarsasag(self):
        return self.__legitarsasag

    def foglalt_helyek_szama(self, jaratszam: str):
        db = 0

        for foglalas in self.__foglalasok.values():
            if foglalas.jarat.jaratszam == jaratszam:
                db += 1

        return db

    def szabad_helyek_szama(self, jaratszam: str):
        jarat = self.legitarsasag.jarat_keresese(jaratszam)

        if jarat is None:
            raise ValueError("Nem létezik ilyen járat.")

        return jarat.kapacitas - self.foglalt_helyek_szama(jaratszam)

    def jegy_foglalasa(self, jaratszam: str, utas_nev: str):
        jarat = self.legitarsasag.jarat_keresese(jaratszam)

        if jarat is None:
            raise ValueError("Nem található ilyen járat.")

        if jarat.indulas <= datetime.now():
            raise ValueError("Erre a járatra már nem lehet foglalni, mert elindult vagy lejárt.")

        if self.szabad_helyek_szama(jaratszam) <= 0:
            raise ValueError("Nincs több szabad hely ezen a járaton.")

        foglalas = JegyFoglalas(self.__kovetkezo_id, utas_nev, jarat)
        self.__foglalasok[self.__kovetkezo_id] = foglalas
        self.__kovetkezo_id += 1

        return foglalas

    def foglalas_lemondasa(self, foglalas_id: int):
        if foglalas_id not in self.__foglalasok:
            raise ValueError("Nem létezik ilyen foglalás.")

        torolt_foglalas = self.__foglalasok.pop(foglalas_id)
        return torolt_foglalas

    def foglalasok_listazasa(self):
        return list(self.__foglalasok.values())


def osfeltoltes():
    legitarsasag = LegiTarsasag("SkyStudent Airlines")

    jarat1 = BelfoldiJarat(
        "HU101",
        "Debrecen",
        18000,
        datetime.now() + timedelta(days=3),
        8
    )

    jarat2 = BelfoldiJarat(
        "HU202",
        "Pécs",
        16000,
        datetime.now() + timedelta(days=5),
        8
    )

    jarat3 = NemzetkoziJarat(
        "INT303",
        "London",
        65000,
        datetime.now() + timedelta(days=10),
        10,
        "Egyesült Királyság"
    )

    legitarsasag.jarat_hozzaadasa(jarat1)
    legitarsasag.jarat_hozzaadasa(jarat2)
    legitarsasag.jarat_hozzaadasa(jarat3)

    rendszer = FoglalasiRendszer(legitarsasag)

    rendszer.jegy_foglalasa("HU101", "Kiss Anna")
    rendszer.jegy_foglalasa("HU101", "Nagy Péter")
    rendszer.jegy_foglalasa("HU202", "Tóth Bence")
    rendszer.jegy_foglalasa("HU202", "Varga Réka")
    rendszer.jegy_foglalasa("INT303", "Szabó Márk")
    rendszer.jegy_foglalasa("INT303", "Horváth Lilla")

    return rendszer


def jaratok_kiirasa(rendszer: FoglalasiRendszer):
    print("\n--- Elérhető járatok ---")

    for jarat in rendszer.legitarsasag.jaratok_listazasa():
        szabad_helyek = rendszer.szabad_helyek_szama(jarat.jaratszam)
        print(f"{jarat} | Szabad helyek: {szabad_helyek}")


def foglalasok_kiirasa(rendszer: FoglalasiRendszer):
    print("\n--- Aktuális foglalások ---")

    foglalasok = rendszer.foglalasok_listazasa()

    if len(foglalasok) == 0:
        print("Jelenleg nincs aktív foglalás.")
        return

    for foglalas in foglalasok:
        print(foglalas)


def jegy_foglalasa_menu(rendszer: FoglalasiRendszer):
    jaratok_kiirasa(rendszer)

    jaratszam = input("\nAdd meg a járatszámot: ").strip()
    utas_nev = input("Add meg az utas nevét: ").strip()

    foglalas = rendszer.jegy_foglalasa(jaratszam, utas_nev)

    print("\nSikeres foglalás!")
    print(f"Foglalás azonosítója: {foglalas.foglalas_id}")
    print(f"Fizetendő összeg: {foglalas.jarat.jegyar} Ft")


def foglalas_lemondasa_menu(rendszer: FoglalasiRendszer):
    foglalasok_kiirasa(rendszer)

    foglalas_id = int(input("\nAdd meg a lemondandó foglalás ID-ját: "))

    torolt_foglalas = rendszer.foglalas_lemondasa(foglalas_id)

    print("\nA foglalás sikeresen le lett mondva.")
    print(f"Lemondott foglalás: {torolt_foglalas}")


def menu():
    rendszer = osfeltoltes()

    while True:
        print("----------------- Repülőjegy Foglalási Rendszer -----------------")
        print("1. Járatok listázása")
        print("2. Jegy foglalása")
        print("3. Foglalás lemondása")
        print("4. Foglalások listázása")
        print("0. Kilépés")

        valasztas = input("Válassz egy menüpontot: ").strip()

        try:
            if valasztas == "1":
                jaratok_kiirasa(rendszer)

            elif valasztas == "2":
                jegy_foglalasa_menu(rendszer)

            elif valasztas == "3":
                foglalas_lemondasa_menu(rendszer)

            elif valasztas == "4":
                foglalasok_kiirasa(rendszer)

            elif valasztas == "0":
                print("Kilépés a programból.")
                break

            else:
                print("Érvénytelen menüpont, próbáld újra.")

        except ValueError as hiba:
            print(f"Hiba: {hiba}")

        except ValueError as hiba:
            print(f"Adatbeviteli hiba: {hiba}")

        except Exception as hiba:
            print(f"Váratlan hiba történt: {hiba}")


if __name__ == "__main__":
    menu()