import random

LICZBA_MIAST = 100
ZIARNO_MACIERZY = 12345
LICZBA_PRZEBIEGOW = 10
MAKS_NIEUDANYCH_PROB = 10000
PROG_ADAPTACYJNY = 500


def generuj_macierz_kosztow(n, ziarno):
    generator_losowy = random.Random(ziarno)
    macierz = []

    for i in range(n):
        wiersz = []
        for j in range(n):
            if i == j:
                wiersz.append(0.0)
            else:
                wiersz.append(round(generator_losowy.uniform(10.0, 90.0), 2))
        macierz.append(wiersz)

    return macierz


def wypisz_fragment_macierzy(macierz, ile_wierszy=5, ile_kolumn=5):
    print("FRAGMENT MACIERZY KOSZTÓW:")
    for i in range(min(ile_wierszy, len(macierz))):
        print(macierz[i][:ile_kolumn])


def losowa_trasa(n, generator_losowy):
    trasa = list(range(1, n + 1))
    generator_losowy.shuffle(trasa)
    return trasa


def oblicz_koszt_trasy(trasa, macierz):
    koszt = 0.0
    n = len(trasa)

    for i in range(n - 1):
        miasto_a = trasa[i] - 1
        miasto_b = trasa[i + 1] - 1
        koszt += macierz[miasto_a][miasto_b]

    ostatnie = trasa[-1] - 1
    pierwsze = trasa[0] - 1
    koszt += macierz[ostatnie][pierwsze]

    return round(koszt, 4)


def mutuj(trasa, generator_losowy, nieudane_proby):
    dziecko = trasa[:]
    n = len(dziecko)

    if nieudane_proby > PROG_ADAPTACYJNY:
        liczba_zamian = 2
    else:
        liczba_zamian = 1

    for _ in range(liczba_zamian):
        indeks = generator_losowy.randint(0, n - 1)
        nastepny = (indeks + 1) % n
        dziecko[indeks], dziecko[nastepny] = dziecko[nastepny], dziecko[indeks]

    return dziecko


def uruchom_strategie_ewolucyjna(macierz, ziarno_przebiegu):
    generator_losowy = random.Random(ziarno_przebiegu)

    rodzic = losowa_trasa(len(macierz), generator_losowy)
    koszt_rodzica = oblicz_koszt_trasy(rodzic, macierz)

    iteracje = 0
    nieudane_proby = 0

    while nieudane_proby < MAKS_NIEUDANYCH_PROB:
        iteracje += 1

        dziecko = mutuj(rodzic, generator_losowy, nieudane_proby)
        koszt_dziecka = oblicz_koszt_trasy(dziecko, macierz)

        if koszt_dziecka < koszt_rodzica:
            rodzic = dziecko
            koszt_rodzica = koszt_dziecka
            nieudane_proby = 0
        else:
            nieudane_proby += 1

    return {
        "trasa": rodzic,
        "koszt": round(koszt_rodzica, 4),
        "iteracje": iteracje
    }


def glowna():
    macierz_kosztow = generuj_macierz_kosztow(LICZBA_MIAST, ZIARNO_MACIERZY)

    print("PODSUMOWANIE DANYCH POCZĄTKOWYCH")
    print(f"Liczba miast: {LICZBA_MIAST}")
    print(f"Ziarno macierzy: {ZIARNO_MACIERZY}")
    print("Macierz jest asymetryczna, koszty są typu float z zakresu (10, 90).")
    print("Na przekątnej znajdują się zera.")
    print("-" * 80)

    wypisz_fragment_macierzy(macierz_kosztow, 5, 5)
    print("-" * 80)
    wyniki = []

    for numer_przebiegu in range(1, LICZBA_PRZEBIEGOW + 1):
        ziarno_przebiegu = 1000 + numer_przebiegu
        wynik = uruchom_strategie_ewolucyjna(macierz_kosztow, ziarno_przebiegu)
        wyniki.append(wynik)

        print(f"PRZEBIEG {numer_przebiegu}")
        print(f"Ostateczny koszt trasy K: {wynik['koszt']}")
        print(f"Liczba iteracji: {wynik['iteracje']}")
        print(f"Początek końcowej trasy (pierwsze 15 miast): {wynik['trasa'][:15]}")
        print("-" * 80)
    print("\nPODSUMOWANIE WSZYSTKICH 10 PRZEBIEGÓW")
    print("{:<10} {:<20} {:<20}".format("Przebieg", "Ostateczny koszt K", "Liczba iteracji"))
    print("-" * 60)

    for i, wynik in enumerate(wyniki, start=1):
        print("{:<10} {:<20} {:<20}".format(
            i,
            wynik["koszt"],
            wynik["iteracje"]
        ))

    najlepszy_wynik = min(wyniki, key=lambda x: x["koszt"])

    print("\nNAJLEPSZY WYNIK SPOŚRÓD WSZYSTKICH 10 PRZEBIEGÓW")
    print(f"Najniższy koszt K: {najlepszy_wynik['koszt']}")
    print(f"Liczba iteracji: {najlepszy_wynik['iteracje']}")
    print(f"Najlepsza trasa (pierwsze 20 miast): {najlepszy_wynik['trasa'][:20]}")
    print(f"Pełna długość trasy: {len(najlepszy_wynik['trasa'])} miast")


if __name__ == "__main__":
    glowna()
