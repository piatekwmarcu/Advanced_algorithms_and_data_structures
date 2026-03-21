import random

LICZBA_ELEMENTOW = 100
MIN_WARTOSC = 10.0
MAX_WARTOSC = 90.0
POJEMNOSC = 2500.0

MAX_ITERACJI = 1000
MAX_NIEUDANYCH_PROB = 100
LICZBA_URUCHOMIEN = 10

def generuj_elementy(n, min_v, max_v):
    return [random.uniform(min_v, max_v) for _ in range(n)]

def losowy_osobnik(n):
    return [random.randint(0, 1) for _ in range(n)]

def suma_plecaka(osobnik, elementy):
    suma = 0.0
    for gen, wartosc in zip(osobnik, elementy):
        if gen == 1:
            suma += wartosc 
    return suma

def ocena(osobnik, elementy, pojemnosc):
    suma = suma_plecaka(osobnik, elementy)

    if suma <= pojemnosc:
        przeladowany = False
        roznica = pojemnosc - suma
    else:
        przeladowany = True
        roznica = suma - pojemnosc
    return suma, przeladowany, roznica

def czy_potomek_lepszy(rodzic, potomek, elementy, pojemnosc):
    suma_r, przel_r, roznica_r = ocena(rodzic, elementy, pojemnosc)
    suma_p, przel_p, roznica_p = ocena(potomek, elementy, pojemnosc)

    if przel_r and not przel_p:
        return True

    if not przel_r and przel_p:
        return False
    
    if not przel_r and not przel_p:
        return roznica_p < roznica_r

    return roznica_p < roznica_r

def mutacja_jednego_bitu(osobnik):
    potomek = osobnik.copy()
    indeks = random.randint(0, len(potomek) - 1)

    if potomek[indeks] == 0:
        potomek[indeks] = 1
    else:
        potomek[indeks] = 0
    return potomek

def mutacja_podwojna(osobnik):
    potomek = osobnik.copy()
    indeksy = random.sample(range(len(potomek)), 2)
    for indeks in indeksy:
        potomek[indeks] = 1 - potomek[indeks]
    return potomek

def mutacja_potrojna(osobnik):
    potomek = osobnik.copy()
    indeksy = random.sample(range(len(potomek)), 3)
    for indeks in indeksy:
        potomek[indeks] = 1 - potomek[indeks]
    return potomek

def algorytm_ewolucyjny(elementy, pojemnosc, max_iteracji, max_nieudanych_prob):
    rodzic = losowy_osobnik(len(elementy))

    najlepszy = rodzic.copy()
    iteracje = 0
    nieudane_proby = 0

    mutacje = [mutacja_jednego_bitu, mutacja_podwojna, mutacja_potrojna]

    while iteracje < max_iteracji and nieudane_proby < max_nieudanych_prob:
        mutacja = random.choice(mutacje)
        potomek = mutacja(rodzic)

        if czy_potomek_lepszy(rodzic, potomek, elementy, pojemnosc):
            rodzic = potomek
            nieudane_proby = 0
        else:
            nieudane_proby += 1
        
        if czy_potomek_lepszy(najlepszy, rodzic, elementy, pojemnosc):
            najlepszy = rodzic.copy()

        iteracje += 1
    
    suma, przeladowany, roznica = ocena(najlepszy, elementy, pojemnosc)

    return {
        "najlepszy_osobnik": najlepszy,
        "suma": suma, 
        "przeladowany": przeladowany,
        "roznica": roznica,
        "iteracje": iteracje,
        "nieudane_proby": nieudane_proby,
        "liczba_wybranych": sum(najlepszy)

    }

def wykonaj_10_uruchomien():
    elementy = generuj_elementy(LICZBA_ELEMENTOW, MIN_WARTOSC, MAX_WARTOSC)
    suma_wszystkich = sum(elementy)
    print("Suma wszytskich elementów:", round(suma_wszystkich, 2))
    print("Pojemność plecaka:", POJEMNOSC)
    print()

    wyniki = []

    for i in range(LICZBA_URUCHOMIEN):
        wynik = algorytm_ewolucyjny(
            elementy,
            POJEMNOSC,
            MAX_ITERACJI,
            MAX_NIEUDANYCH_PROB
        )
        wyniki.append(wynik)

        print(f"URUCHOMIENIE {i + 1}")
        print("Suma w plecaku:", round(wynik["suma"], 2))
        print("Przeładowany:", wynik["przeladowany"])
        print("Róznica:", round(wynik["roznica"], 2))
        print("Liczba wybranych elementów:", wynik["liczba_wybranych"])
        print("Iteracje:", wynik["iteracje"])
        print("-" * 40)

    najlepszy_wynik = wyniki[0]
    for wynik in wyniki[1:]:
        if czy_potomek_lepszy(
            najlepszy_wynik["najlepszy_osobnik"],
            wynik["najlepszy_osobnik"],
            elementy,
            POJEMNOSC
        ):
            najlepszy_wynik = wynik
    print()
    print("NAJLEPSZY WYNIK Z 10 URUCHOMIEŃ")
    print("Suma w plecaku:", round(najlepszy_wynik["suma"], 2))
    print("Przeładowany:", najlepszy_wynik["przeladowany"])
    print("Różnica:", round(najlepszy_wynik["roznica"], 2))
    print("Liczba wybranych elementów:", najlepszy_wynik["liczba_wybranych"])
    print()

    # Obliczanie średnich
    srednia_suma = sum(w["suma"] for w in wyniki) / len(wyniki)
    srednia_roznica = sum(w["roznica"] for w in wyniki) / len(wyniki)
    srednia_liczba_wybranych = sum(w["liczba_wybranych"] for w in wyniki) / len(wyniki)
    srednia_iteracje = sum(w["iteracje"] for w in wyniki) / len(wyniki)
    min_roznica = min(w["roznica"] for w in wyniki)
    max_roznica = max(w["roznica"] for w in wyniki)

    print("ŚREDNIE Z 10 URUCHOMIEŃ")
    print("Średnia suma w plecaku:", round(srednia_suma, 2))
    print("Średnia różnica:", round(srednia_roznica, 2))
    print("Min różnica:", round(min_roznica, 2))
    print("Max różnica:", round(max_roznica, 2))
    print("Średnia liczba wybranych elementów:", round(srednia_liczba_wybranych, 2))
    print("Średnia liczba iteracji:", round(srednia_iteracje, 2))

    with open("wyniki_plecaka.txt", "w") as f:
        f.write(f"Suma wszystkich elementów: {round(suma_wszystkich, 2)}\n")
        f.write(f"Pojemność plecaka: {POJEMNOSC}\n\n")
        
        for i, wynik in enumerate(wyniki, 1):
            f.write(f"URUCHOMIENIE {i}\n")
            f.write(f"Suma w plecaku: {round(wynik['suma'], 2)}\n")
            f.write(f"Przeładowany: {wynik['przeladowany']}\n")
            f.write(f"Róznica: {round(wynik['roznica'], 2)}\n")
            f.write(f"Liczba wybranych elementów: {wynik['liczba_wybranych']}\n")
            f.write(f"Iteracje: {wynik['iteracje']}\n")
            f.write("-" * 40 + "\n")
        
        f.write("\nNAJLEPSZY WYNIK Z 10 URUCHOMIEŃ\n")
        f.write(f"Suma w plecaku: {round(najlepszy_wynik['suma'], 2)}\n")
        f.write(f"Przeładowany: {najlepszy_wynik['przeladowany']}\n")
        f.write(f"Różnica: {round(najlepszy_wynik['roznica'], 2)}\n")
        f.write(f"Liczba wybranych elementów: {najlepszy_wynik['liczba_wybranych']}\n\n")
        
        f.write("ŚREDNIE Z 10 URUCHOMIEŃ\n")
        f.write(f"Średnia suma w plecaku: {round(srednia_suma, 2)}\n")
        f.write(f"Średnia różnica: {round(srednia_roznica, 2)}\n")
        f.write(f"Min różnica: {round(min_roznica, 2)}\n")
        f.write(f"Max różnica: {round(max_roznica, 2)}\n")
        f.write(f"Średnia liczba wybranych elementów: {round(srednia_liczba_wybranych, 2)}\n")
        f.write(f"Średnia liczba iteracji: {round(srednia_iteracje, 2)}\n")
    
    print("\nWyniki zostały zapisane do pliku 'wyniki_plecaka.txt'")

if __name__ == "__main__":
    wykonaj_10_uruchomien()
