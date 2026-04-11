import random

POJEMNOSC = 250.0
LICZBA_PRZEDMIOTOW = 100
ZIARNO_PRZEDMIOTOW = 12345
LICZBA_PRZEBIEGOW = 10
MAKS_NIEUDANYCH_PROB = 100
PROG_ADAPTACYJNY = 20

def generuj_przedmioty(n, ziarno):
    generator_losowy = random.Random(ziarno)
    przedmioty = [round(generator_losowy.uniform(1.0, 10.0), 2) for _ in range(n)]

    if sum(przedmioty) <= POJEMNOSC:
        raise ValueError("Ograniczenie nie spełnione: suma objętości przedmiotów musi być > 250.")

    return przedmioty

def losowe_rozwiazanie(n, generator_losowy):
    return [generator_losowy.randint(0, 1) for _ in range(n)]


def oceniaj(rozwiazanie, przedmioty):
    return sum(bit * objetosc for bit, objetosc in zip(rozwiazanie, przedmioty))


def mutuj(rozwiazanie, generator_losowy, nieudane_proby):
    dziecko = rozwiazanie[:]
    n = len(rozwiazanie)

    if nieudane_proby > PROG_ADAPTACYJNY:
        k = generator_losowy.choice([2, 3])
    else:
        k = 1

    indeksy = generator_losowy.sample(range(n), k)
    for indeks in indeksy:
        dziecko[indeks] = 1 - dziecko[indeks]

    return dziecko


def czy_lepsze(objetosc_rodzica, objetosc_dziecka, pojemnosc):
    rodzic_wykonalny = objetosc_rodzica <= pojemnosc
    dziecko_wykonalne = objetosc_dziecka <= pojemnosc
    if (not rodzic_wykonalny) and dziecko_wykonalne:
        return True
    if rodzic_wykonalny and dziecko_wykonalne and objetosc_dziecka > objetosc_rodzica:
        return True
    if (not rodzic_wykonalny) and (not dziecko_wykonalne):
        nadmiar_rodzica = objetosc_rodzica - pojemnosc
        nadmiar_dziecka = objetosc_dziecka - pojemnosc
        if nadmiar_dziecka < nadmiar_rodzica:
            return True
    return False


def uruchom_es_1plus1(przedmioty, pojemnosc, ziarno_przebiegu):
    generator_losowy = random.Random(ziarno_przebiegu)

    rodzic = losowe_rozwiazanie(len(przedmioty), generator_losowy)
    objetosc_rodzica = oceniaj(rodzic, przedmioty)

    nieudane_proby = 0
    iteracje = 0

    while nieudane_proby < MAKS_NIEUDANYCH_PROB:
        iteracje += 1

        dziecko = mutuj(rodzic, generator_losowy, nieudane_proby)
        objetosc_dziecka = oceniaj(dziecko, przedmioty)

        if czy_lepsze(objetosc_rodzica, objetosc_dziecka, pojemnosc):
            rodzic = dziecko
            objetosc_rodzica = objetosc_dziecka
            nieudane_proby = 0
        else:
            nieudane_proby += 1

    status = "Wykonalne" if objetosc_rodzica <= pojemnosc else "Przeładowane"

    return {
        "ostateczna_objetosc": round(objetosc_rodzica, 2),
        "iteracje": iteracje,
        "status": status
    }


def glowna():
    przedmioty = generuj_przedmioty(LICZBA_PRZEDMIOTOW, ZIARNO_PRZEDMIOTOW)

    print("STAŁE OBJĘTOŚCI PRZEDMIOTÓW:")
    print(przedmioty)
    print("\nCałkowita suma wszystkich objętości przedmiotów:", round(sum(przedmioty), 2))
    print("Sprawdzenie ograniczenia (suma > 250):", sum(przedmioty) > POJEMNOSC)
    print("-" * 70)
    wyniki = []

    for id_przebiegu in range(1, LICZBA_PRZEBIEGOW + 1):
        # Różne ziarno dla mutacji / inicjalizacji w każdym przebiegu
        ziarno_przebiegu = 1000 + id_przebiegu

        wynik = uruchom_es_1plus1(przedmioty, POJEMNOSC, ziarno_przebiegu)
        wyniki.append(wynik)

        print(f"PRZEBIEG {id_przebiegu}")
        print(f"Ostateczna całkowita objętość: {wynik['ostateczna_objetosc']}")
        print(f"Liczba iteracji: {wynik['iteracje']}")
        print(f"Status: {wynik['status']}")
        print("-" * 70)

    print("\nPODSUMOWANIE WSZYSTKICH 10 PRZEBIEGÓW")
    print("{:<6} {:<18} {:<15} {:<12}".format("Przebieg", "Ostateczna objętość", "Iteracje", "Status"))
    print("-" * 60)

    for i, wynik in enumerate(wyniki, start=1):
        print("{:<6} {:<18} {:<15} {:<12}".format(
            i,
            wynik["ostateczna_objetosc"],
            wynik["iteracje"],
            wynik["status"]
        ))

    najlepsze_wykonalne = [w for w in wyniki if w["status"] == "Wykonalne"]
    if najlepsze_wykonalne:
        najlepsze = max(najlepsze_wykonalne, key=lambda x: x["ostateczna_objetosc"])
        print("\nNajlepsze wykonalne rozwiązanie:")
        print(najlepsze)
    else:
        print("\nNie znaleziono wykonalnego rozwiązania w żadnym przebiegu.")


if __name__ == "__main__":
    glowna()