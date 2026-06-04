# 05_kohonen_som_swiece

## Sieć Kohonena - klasyfikacja typów świec japońskich

### Opis zadania

Projekt przedstawia implementację sieci Kohonena, czyli samoorganizującej się mapy neuronowej SOM, do klasyfikacji i grupowania typów świec japońskich na podstawie dziennych danych giełdowych.

Dane wejściowe pobierane są dla wybranych japońskich spółek giełdowych. Każda świeca dzienna opisana jest wartościami OHLC:

- Open
- High
- Low
- Close

Na podstawie tych danych program wyznacza cechy opisujące kształt świecy, a następnie wykorzystuje je jako dane wejściowe do sieci Kohonena.

### Cel zadania

Celem zadania jest zastosowanie sieci Kohonena do nienadzorowanego grupowania świec japońskich według podobieństwa ich kształtu.

Program wykonuje 10 niezależnych prób uczenia. W każdej próbie:

- losowany jest inny zbiór danych początkowych,
- stosowana jest inna inicjalizacja wag sieci,
- trenowana jest osobna mapa Kohonena,
- obliczane są miary jakości wyniku,
- wybierana jest najlepsza próba.

### Dane wejściowe

Program pobiera dzienne dane giełdowe z okresu 3 lat dla pięciu spółek notowanych na giełdzie w Tokio:

- `7203.T` - Toyota
- `6758.T` - Sony
- `9984.T` - SoftBank
- `8306.T` - Mitsubishi UFJ
- `9432.T` - Nippon Telegraph and Telephone

Dane zawierają wartości:

- `Date`
- `Ticker`
- `Open`
- `High`
- `Low`
- `Close`
- `Volume`

### Cechy świec japońskich

Każda świeca zostaje przekształcona do wektora cech:

```text
x = [body_ratio, upper_ratio, lower_ratio, direction]
```

gdzie:

- `body_ratio` - względna długość korpusu świecy,
- `upper_ratio` - względna długość górnego cienia,
- `lower_ratio` - względna długość dolnego cienia,
- `direction` - kierunek świecy:
  - `1` dla świecy wzrostowej,
  - `-1` dla świecy spadkowej.

Dane przed uczeniem są normalizowane do przedziału od 0 do 1.

### Zastosowany algorytm

W zadaniu zastosowano sieć Kohonena SOM o rozmiarze `10 x 10`, czyli 100 neuronów.

Dla każdego wektora wejściowego wybierany jest neuron zwycięski, czyli BMU - Best Matching Unit. Jest to neuron, którego wektor wag znajduje się najbliżej aktualnego wektora wejściowego.

Po wybraniu neuronu zwycięskiego aktualizowane są jego wagi oraz wagi neuronów sąsiednich.

Aktualizacja wag odbywa się zgodnie ze wzorem:

```text
w(k+1) = w(k) + eta * h * (x(k) - w(k))
```

gdzie:

- `w(k)` - aktualny wektor wag neuronu,
- `w(k+1)` - nowy wektor wag po aktualizacji,
- `eta` - współczynnik uczenia,
- `h` - funkcja sąsiedztwa,
- `x(k)` - aktualny wektor wejściowy.

### Parametry programu

| Parametr | Wartość |
|---|---:|
| Liczba prób | 10 |
| Liczba próbek w jednej próbie | 800 |
| Rozmiar mapy Kohonena | 10 x 10 |
| Liczba neuronów | 100 |
| Liczba cech wejściowych | 4 |
| Liczba epok | 60 |
| Learning rate | 0.5 |
| Sigma | 3.0 |

### Ocena wyników

Do oceny jakości działania sieci wykorzystano:

- `Quantization Error` - błąd kwantyzacji,
- `Silhouette Score` - jakość separacji klastrów,
- `Active Neurons` - liczba aktywnych neuronów,
- `Score` - łączna miara jakości wyniku.

Najlepsza próba wybierana jest jako kompromis między wysokim `Silhouette Score` a niskim błędem kwantyzacji.

### Wymagane biblioteki

Do uruchomienia programu potrzebne są biblioteki:

```text
numpy
pandas
matplotlib
scikit-learn
yfinance
```

Można je zainstalować poleceniem:

```bash
python3 -m pip install -r requirements.txt
```

### Uruchomienie programu

Aby uruchomić program, należy przejść do folderu zadania:

```bash
cd 05_kohonen_som_swiece
```

Następnie zainstalować wymagane biblioteki:

```bash
python3 -m pip install -r requirements.txt
```

I uruchomić program:

```bash
python3 kohonen_som_swiece.py
```

### Wynik działania programu

Program wypisuje w terminalu:

- pobrane dane giełdowe,
- przykładowe cechy świec,
- wyniki wszystkich 10 prób,
- najlepszą próbę,
- podsumowanie klastrów,
- przykładowe przypisanie świec do klastrów.

Dodatkowo program generuje pliki CSV:

- `wyniki_prob_kohonen.csv`
- `podsumowanie_klastrow.csv`
- `najlepsza_proba_dane.csv`

### Otrzymane wyniki

Najlepsza była próba numer 2.

| Parametr | Wartość |
|---|---:|
| Run | 2 |
| Random State | 102 |
| Sample Size | 800 |
| Quantization Error | 0.088750 |
| Silhouette Score | 0.251412 |
| Active Neurons | 83 |
| Score | 0.162662 |

### Przykładowe klastry

W najlepszej próbie program utworzył klastry odpowiadające różnym typom świec japońskich, między innymi:

- Shooting star bearish,
- Strong bearish candle,
- Strong bullish candle,
- Shooting star bullish,
- Normal bearish candle,
- Doji.

Sieć Kohonena nie otrzymywała etykiet klas podczas uczenia. Typy świec zostały użyte dopiero po zakończeniu uczenia do interpretacji powstałych klastrów.

### Wnioski

Zaimplementowana sieć Kohonena poprawnie wykonała zadanie nienadzorowanego grupowania świec japońskich.

Najważniejsze wnioski:

- dane giełdowe OHLC można przekształcić do cech opisujących kształt świecy,
- sieć Kohonena potrafi grupować podobne świece bez wcześniejszych etykiet klas,
- wykonanie 10 prób pozwala porównać jakość działania algorytmu,
- najlepsza próba została wybrana na podstawie miar jakości,
- algorytm SOM dobrze nadaje się do analizy danych, w których klasy nie są jednoznacznie znane z góry.

### Autor

Emilia Piotrowska
