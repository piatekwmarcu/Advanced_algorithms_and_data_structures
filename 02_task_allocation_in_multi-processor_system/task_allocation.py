import random

MOCE_PROCESOROW = {
    1: 1.0,
    2: 1.25,
    3: 1.5,
    4: 1.75
}

LICZBA_ZADAN = 100
ZIARNO_ZADAN = 54321
LICZBA_PRZEBIEGOW = 10
MAKS_NIEUDANYCH_PROB = 10000
PROG_ADAPTACYJNY = 100

def generuj_zadania(n, ziarno):
    generator_losowy = random.Random(ziarno)
    zadania = [round(generator_losowy.uniform(10.0, 90.0), 2) for _ in range(n)]
    return zadania

def losowe_rozwiazanie(n, generator_losowy):
    return [generator_losowy.randint(1,4) for _ in range(n)]

def oblicz_obciazeia(rozwiazanie, zadania, moce_procesorow):
    obciazenia = {1: 0.0, 2:0.0, 3: 0.0, 4: 0.0}
    for czas_zadania, procesor in zip(zadania, rozwiazanie):
        obciazenia[procesor] += czas_zadania / moce_procesorow[procesor]
    return obciazenia

def oblicz_delta_t(rozwiazanie, zadania, moce_procesorow):
    obciazenia = oblicz_obciazeia(rozwiazanie, zadania, moce_procesorow)
    return max(obciazenia.values())

def policz_liczbe_zadan_na_procesorach(rozwiazanie):
    licznik = {1: 0, 2: 0, 3: 0, 4: 0}
    for procesor in rozwiazanie:
        licznik[procesor] += 1
    return licznik

def mutuj(rozwiazanie, generator_losowy, nieudane_proby):
    dziecko = rozwiazanie[:]
    n = len(rozwiazanie)
    if nieudane_proby > PROG_ADAPTACYJNY:
        ile_zmienic = generator_losowy.choice([2, 3])
    else:
        ile_zmienic = 1
    indeksy = generator_losowy.sample(range(n), ile_zmienic)
    for indeks in indeksy:
        obecny_procesor = dziecko[indeks]
        mozliwe_procesory = [1, 2, 3, 4]
        mozliwe_procesory.remove(obecny_procesor)
        nowy_procesor = generator_losowy.choice(mozliwe_procesory)
        dziecko[indeks] = nowy_procesor

    return dziecko

def uruchom_strategie_ewolucyjna(zadania, moce_procesorow, ziarno_przebiegu):
    generator_losowy = random.Random(ziarno_przebiegu)
    rodzic = losowe_rozwiazanie(len(zadania), generator_losowy)
    delta_t_rodzica = oblicz_delta_t(rodzic, zadania, moce_procesorow)
    nieudane_proby = 0
    iteracje = 0
    while nieudane_proby < MAKS_NIEUDANYCH_PROB:
        iteracje += 1
        dziecko = mutuj(rodzic, generator_losowy, nieudane_proby)
        delta_t_dziecka = oblicz_delta_t(dziecko, zadania, moce_procesorow)
        if delta_t_dziecka < delta_t_rodzica:
            rodzic = dziecko
            delta_t_rodzica = delta_t_dziecka
            nieudane_proby = 0
        else:
            nieudane_proby += 1
    koncowe_obciazenia = oblicz_obciazeia(rodzic, zadania, moce_procesorow)
    koncowe_przydzial = policz_liczbe_zadan_na_procesorach(rodzic)
    return {
        "rozwiazanie": rodzic,
        "delta_t": round(delta_t_rodzica, 4),
        "iteracje": iteracje,
        "przydzial": koncowe_przydzial,
        "obciazenia": {p: round(o, 4) for p, o in koncowe_obciazenia.items()}
    }
    
def glowna():
    print("Start programu")
    zadania = generuj_zadania(LICZBA_ZADAN, ZIARNO_ZADAN)

    print("STAŁA LISTA ZADAŃ:")
    print(zadania)
    print("\nLiczba zadań:", len(zadania))
    print("Moce procesorów:", MOCE_PROCESOROW)
    print("-" * 50)

    wyniki = []
    for numer_przebiegu in range (1, LICZBA_PRZEBIEGOW+1):
        ziarno_przebiegu = 1000 + numer_przebiegu
        wynik = uruchom_strategie_ewolucyjna(zadania, MOCE_PROCESOROW, ziarno_przebiegu)
        wyniki.append(wynik)
        print(f"PRZEBIEG: {numer_przebiegu}")
        print(f"Ostateczne delta t: {wynik['delta_t']}")
        print(f"Końcowy przydział liczby zdań: {wynik['przydzial']}")
        print("-" * 50)
    
    print("\nPODSUMOWANIE WSZYSTKICH 10 PRZEBIEGÓW")
    print("{:<10} {:<20} {:<15} {:<30}".format(
        "Przebieg", "Ostateczne Δt", "Iteracje", "Przydział zadań"
    ))
    print("-" * 95)

    for i, wynik in enumerate(wyniki, start=1):
        print("{:<10} {:<20} {:<15} {}".format(
            i,
            wynik["delta_t"],
            wynik["iteracje"],
            str(wynik["przydzial"])
        ))

    najlepszy_wynik = min(wyniki, key=lambda x: x["delta_t"])

    print("\nNAJLEPSZY WYNIK SPOŚRÓD WSZYSTKICH 10 PRZEBIEGÓW")
    print(f"Najlepsze delta t: {najlepszy_wynik['delta_t']}")
    print(f"Liczba iteracji: {najlepszy_wynik['iteracje']}")
    print(f"Przydział zadań: {najlepszy_wynik['przydzial']}")

    wypisz_obciazenia_najlepszego(najlepszy_wynik["obciazenia"])

def wypisz_obciazenia_najlepszego(obciazenia):
    print("Obciążenia procesorów:")
    for procesor, obciazenie in obciazenia.items():
        print(f"Procesor {procesor}: {obciazenie}")

if __name__ == "__main__":
    glowna()