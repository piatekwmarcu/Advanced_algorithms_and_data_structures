# PSO (Particle Swarm Optimization) Implementation

import numpy as np
import math

def funkcja(x, y):
    """
    f(x,y) = |sin(x) + sin(2x) + sin(4x) + sin(8x)|
           + |cos(y) + cos(2y) + cos(4y) + cos(8y)|

    Funkcja jest okresowa:
    Tx = 2*pi
    Ty = 2*pi
    """
    czesc_x = np.sin(x) + np.sin(2 * x) + np.sin(4 * x) + np.sin(8 * x)
    czesc_y = np.cos(y) + np.cos(2 * y) + np.cos(4 * y) + np.cos(8 * y)

    return np.abs(czesc_x) + np.abs(czesc_y)

def uruchom_pso(
    numer_proby,
    liczba_czastek=100,
    liczba_iteracji=100000,
    predkosc=0.001,
    seed=12345,
    x_poczatkowe=None,
    y_poczatkowe=None
):
    # RNG dla tej konkretnej próby - daje losowe wektory prędkości
    rng = np.random.default_rng(seed + numer_proby)

    x_min = 0
    x_max = 2 * math.pi
    y_min = 0
    y_max = 2 * math.pi

    # Użyj przekazanych początkowych pozycji lub wygeneruj nowe
    if x_poczatkowe is not None and y_poczatkowe is not None:
        x = x_poczatkowe.copy()
        y = y_poczatkowe.copy()
    else:
        x = rng.uniform(x_min, x_max, liczba_czastek)
        y = rng.uniform(y_min, y_max, liczba_czastek)

    katy = rng.uniform(0, 2 * math.pi, liczba_czastek)

    vx = predkosc * np.cos(katy)
    vy = predkosc * np.sin(katy)

    wartosci = funkcja(x, y)

    indeks_najlepszej = np.argmax(wartosci)

    najlepsze_x = x[indeks_najlepszej]
    najlepsze_y = y[indeks_najlepszej]
    najlepsza_wartosc = wartosci[indeks_najlepszej]

    for iteracja in range(liczba_iteracji):

        dx = najlepsze_x - x
        dy = najlepsze_y - y

        odleglosc = np.sqrt(dx ** 2 + dy ** 2)

        maska = odleglosc > 0

        vx[maska] = predkosc * dx[maska] / odleglosc[maska]
        vy[maska] = predkosc * dy[maska] / odleglosc[maska]

        if np.any(~maska):
            losowy_kat = rng.uniform(0, 2 * math.pi)
            vx[~maska] = predkosc * math.cos(losowy_kat)
            vy[~maska] = predkosc * math.sin(losowy_kat)

        x = x + vx
        y = y + vy

        x = np.mod(x, 2 * math.pi)
        y = np.mod(y, 2 * math.pi)

        wartosci = funkcja(x, y)

        indeks_najlepszej_iteracji = np.argmax(wartosci)
        wartosc_iteracji = wartosci[indeks_najlepszej_iteracji]

        if wartosc_iteracji > najlepsza_wartosc:
            najlepsza_wartosc = wartosc_iteracji
            najlepsze_x = x[indeks_najlepszej_iteracji]
            najlepsze_y = y[indeks_najlepszej_iteracji]

    wynik = {
        "proba": numer_proby,
        "x": najlepsze_x,
        "y": najlepsze_y,
        "f": najlepsza_wartosc
    }

    return wynik

def main():
    LICZBA_PROB = 10
    LICZBA_CZASTEK = 100
    LICZBA_ITERACJI = 100000
    PREDKOSC = 0.001
    SEED = 12345

    wyniki = []

    print("ALGORYTM PSO - PARTICLE SWARM OPTIMISATION")
    print("-" * 70)
    print("Funkcja:")
    print("f(x,y) = |sin(x) + sin(2x) + sin(4x) + sin(8x)|")
    print("       + |cos(y) + cos(2y) + cos(4y) + cos(8y)|")
    print()
    print(f"Liczba cząstek: {LICZBA_CZASTEK}")
    print(f"Liczba iteracji w jednej próbie: {LICZBA_ITERACJI}")
    print(f"Liczba prób: {LICZBA_PROB}")
    print(f"Prędkość cząstki: {PREDKOSC}")
    print(f"Zakres x: [0, 2*pi]")
    print(f"Zakres y: [0, 2*pi]")
    print("-" * 70)

    # Wygeneruj początkowe pozycje cząstek (będą takie same dla każdej próby)
    rng_init = np.random.default_rng(SEED)
    x_poczatkowe = rng_init.uniform(0, 2 * math.pi, LICZBA_CZASTEK)
    y_poczatkowe = rng_init.uniform(0, 2 * math.pi, LICZBA_CZASTEK)

    print("WYGENEROWANE POZYCJE POCZĄTKOWE CZĄSTEK")
    print("=" * 70)
    print(f"Cząstka | X (początkowe)  | Y (początkowe)")
    print("-" * 70)
    for i in range(min(10, LICZBA_CZASTEK)):
        print(f"{i+1:6d} | {x_poczatkowe[i]:15.6f} | {y_poczatkowe[i]:15.6f}")
    
    if LICZBA_CZASTEK > 10:
        print(f"... ({LICZBA_CZASTEK - 10} pozostałych cząstek)")
    print("=" * 70)
    print("(Te pozycje będą TAKIE SAME dla wszystkich prób)")
    print("(Ale wektory prędkości będą LOSOWE dla każdej próby)")
    print("=" * 70)
    print()

    for proba in range(1, LICZBA_PROB + 1):
        wynik = uruchom_pso(
            numer_proby=proba,
            liczba_czastek=LICZBA_CZASTEK,
            liczba_iteracji=LICZBA_ITERACJI,
            predkosc=PREDKOSC,
            seed=SEED,
            x_poczatkowe=x_poczatkowe,
            y_poczatkowe=y_poczatkowe
        )

        wyniki.append(wynik)

        print(f"PRÓBA {proba}")
        print(f"Najlepsze x: {wynik['x']:.6f}")
        print(f"Najlepsze y: {wynik['y']:.6f}")
        print(f"Najlepsza wartość f(x,y): {wynik['f']:.6f}")
        print("-" * 70)

    najlepszy_wynik = max(wyniki, key=lambda wynik: wynik["f"])

    print()
    print("PODSUMOWANIE KOŃCOWE")
    print("=" * 70)

    for wynik in wyniki:
        print(
            f"Próba {wynik['proba']:2d}: "
            f"x = {wynik['x']:.6f}, "
            f"y = {wynik['y']:.6f}, "
            f"f(x,y) = {wynik['f']:.6f}"
        )

    print("=" * 70)
    print("NAJLEPSZY WYNIK ZE WSZYSTKICH PRÓB:")
    print(f"Próba: {najlepszy_wynik['proba']}")
    print(f"x = {najlepszy_wynik['x']:.6f}")
    print(f"y = {najlepszy_wynik['y']:.6f}")
    print(f"f(x,y) = {najlepszy_wynik['f']:.6f}")
    print("=" * 70)


if __name__ == "__main__":
    main()