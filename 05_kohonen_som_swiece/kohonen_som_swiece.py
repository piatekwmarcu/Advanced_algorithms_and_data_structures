"""
Sieć Kohonena / SOM do klasyfikacji typów świec japońskich giełdowych.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score

def download_stock_data():

    tickers = [
        "7203.T",  # Toyota
        "6758.T",  # Sony
        "9984.T",  # SoftBank
        "8306.T",  # Mitsubishi UFJ
        "9432.T",  # Nippon Telegraph and Telephone
    ]

    all_data = []

    for ticker in tickers:
        print(f"Pobieranie danych dla: {ticker}")

        df = yf.download(
            ticker,
            period="3y",
            interval="1d",
            auto_adjust=False,
            progress=False
        )

        if df.empty:
            print(f"Brak danych dla: {ticker}")
            continue

        # yfinance czasem zwraca kolumny wielopoziomowe,
        # np. ('Open', '7203.T'). Tutaj spłaszczamy je do zwykłych nazw.
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        df["Ticker"] = ticker

        required_columns = ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]
        df = df[required_columns]

        df = df.dropna()

        all_data.append(df)

    if not all_data:
        raise ValueError("Nie udało się pobrać żadnych danych giełdowych.")

    data = pd.concat(all_data, ignore_index=True)

    return data

def create_candle_features(df):

    df = df.copy()

    df["range"] = df["High"] - df["Low"]
    df = df[df["range"] > 0].copy()

    df["body"] = abs(df["Close"] - df["Open"])

    df["upper_shadow"] = (
        df["High"] - df[["Open", "Close"]].max(axis=1)
    )

    df["lower_shadow"] = (
        df[["Open", "Close"]].min(axis=1) - df["Low"]
    )

    df["direction"] = np.where(df["Close"] >= df["Open"], 1, -1)

    df["body_ratio"] = df["body"] / df["range"]
    df["upper_ratio"] = df["upper_shadow"] / df["range"]
    df["lower_ratio"] = df["lower_shadow"] / df["range"]

    features = df[
        [
            "body_ratio",
            "upper_ratio",
            "lower_ratio",
            "direction"
        ]
    ]

    return df, features

def candle_type(row):

    body = row["body_ratio"]
    upper = row["upper_ratio"]
    lower = row["lower_ratio"]
    direction = row["direction"]

    if body < 0.15 and upper > 0.3 and lower > 0.3:
        return "Doji"

    if body < 0.3 and lower > 0.55:
        if direction == 1:
            return "Hammer bullish"
        else:
            return "Hammer bearish"

    if body < 0.3 and upper > 0.55:
        if direction == 1:
            return "Shooting star bullish"
        else:
            return "Shooting star bearish"

    if body > 0.7:
        if direction == 1:
            return "Strong bullish candle"
        else:
            return "Strong bearish candle"

    if direction == 1:
        return "Normal bullish candle"
    else:
        return "Normal bearish candle"

class KohonenSOM:

    def __init__(
        self,
        grid_size=(10, 10),
        input_dim=4,
        learning_rate=0.5,
        sigma=3.0,
        epochs=60,
        random_state=None
    ):
        self.grid_size = grid_size
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.sigma = sigma
        self.epochs = epochs
        self.random_state = random_state

        self.rng = np.random.default_rng(random_state)

        self.weights = self.rng.random(
            (grid_size[0], grid_size[1], input_dim)
        )

    def _find_bmu(self, x):

        distances = np.linalg.norm(self.weights - x, axis=2)
        bmu_index = np.unravel_index(
            np.argmin(distances),
            distances.shape
        )

        return bmu_index

    def _neighborhood_function(self, bmu, epoch):

        sigma_t = self.sigma * np.exp(-epoch / self.epochs)
        sigma_t = max(sigma_t, 0.1)

        grid_x, grid_y = np.meshgrid(
            np.arange(self.grid_size[0]),
            np.arange(self.grid_size[1]),
            indexing="ij"
        )

        distance_sq = (
            (grid_x - bmu[0]) ** 2
            + (grid_y - bmu[1]) ** 2
        )

        h = np.exp(-distance_sq / (2 * sigma_t ** 2))

        return h

    def fit(self, X):

        X = np.array(X)

        for epoch in range(self.epochs):
            learning_rate_t = self.learning_rate * np.exp(
                -epoch / self.epochs
            )

            indices = self.rng.permutation(len(X))

            for idx in indices:
                x = X[idx]

                bmu = self._find_bmu(x)
                h = self._neighborhood_function(bmu, epoch)

                for i in range(self.grid_size[0]):
                    for j in range(self.grid_size[1]):
                        self.weights[i, j] += (
                            learning_rate_t
                            * h[i, j]
                            * (x - self.weights[i, j])
                        )

        return self

    def predict(self, X):

        labels = []

        for x in X:
            bmu = self._find_bmu(x)
            label = bmu[0] * self.grid_size[1] + bmu[1]
            labels.append(label)

        return np.array(labels)

    def quantization_error(self, X):
 

        errors = []

        for x in X:
            bmu = self._find_bmu(x)
            w = self.weights[bmu]
            errors.append(np.linalg.norm(x - w))

        return np.mean(errors)

def run_experiments(X, data_features, n_runs=10, sample_size=800):

    results = []
    trained_models = []

    for run in range(1, n_runs + 1):
        print(f"\nStart próby {run}/{n_runs}")

        random_state = 100 + run
        rng = np.random.default_rng(random_state)

        sample_indices = rng.choice(
            len(X),
            size=min(sample_size, len(X)),
            replace=False
        )

        X_sample = X[sample_indices]
        data_sample = data_features.iloc[sample_indices].copy()

        som = KohonenSOM(
            grid_size=(10, 10),
            input_dim=X.shape[1],
            learning_rate=0.5,
            sigma=3.0,
            epochs=60,
            random_state=random_state
        )

        som.fit(X_sample)

        labels = som.predict(X_sample)
        quant_error = som.quantization_error(X_sample)

        unique_labels = len(set(labels))

        if unique_labels > 1 and unique_labels < len(X_sample):
            try:
                sil_score = silhouette_score(X_sample, labels)
            except Exception:
                sil_score = -1
        else:
            sil_score = -1

        data_sample["Cluster"] = labels

        results.append({
            "Run": run,
            "Random_State": random_state,
            "Sample_Size": len(X_sample),
            "Quantization_Error": quant_error,
            "Silhouette_Score": sil_score,
            "Active_Neurons": unique_labels
        })

        trained_models.append({
            "run": run,
            "model": som,
            "labels": labels,
            "data": data_sample,
            "X_sample": X_sample
        })

        print(
            f"Próba {run}: "
            f"błąd kwantyzacji = {quant_error:.4f}, "
            f"silhouette = {sil_score:.4f}, "
            f"aktywne neurony = {unique_labels}"
        )

    results_df = pd.DataFrame(results)

    return results_df, trained_models

def create_cluster_summary(best_data):

    cluster_summary = (
        best_data
        .groupby("Cluster")["Candle_Type"]
        .agg(lambda x: Counter(x).most_common(1)[0][0])
        .reset_index()
        .rename(columns={"Candle_Type": "Dominant_Candle_Type"})
    )

    cluster_counts = (
        best_data
        .groupby("Cluster")
        .size()
        .reset_index(name="Count")
    )

    cluster_summary = cluster_summary.merge(
        cluster_counts,
        on="Cluster"
    )

    cluster_summary = cluster_summary.sort_values(
        by="Count",
        ascending=False
    )

    return cluster_summary

def plot_results(results_df):

    plt.figure(figsize=(10, 5))
    plt.plot(
        results_df["Run"],
        results_df["Quantization_Error"],
        marker="o"
    )
    plt.xlabel("Numer próby")
    plt.ylabel("Błąd kwantyzacji")
    plt.title("Porównanie błędu kwantyzacji dla 10 prób")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(
        results_df["Run"],
        results_df["Silhouette_Score"],
        marker="o"
    )
    plt.xlabel("Numer próby")
    plt.ylabel("Silhouette score")
    plt.title("Porównanie jakości klasteryzacji dla 10 prób")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_kohonen_map(best_model_data, best_run_number):
    """
    Rysuje mapę Kohonena dla najlepszej próby.
    Pokazuje, ile świec zostało przypisanych do danego neuronu.
    """

    best_labels = best_model_data["labels"]

    map_counts = np.zeros((10, 10))

    for label in best_labels:
        i = label // 10
        j = label % 10
        map_counts[i, j] += 1

    plt.figure(figsize=(8, 8))
    plt.imshow(map_counts)
    plt.colorbar(label="Liczba przypisanych świec")
    plt.title(f"Mapa Kohonena - najlepsza próba nr {best_run_number}")
    plt.xlabel("Kolumna neuronu")
    plt.ylabel("Wiersz neuronu")
    plt.tight_layout()
    plt.show()

def main():
    print("SIEĆ KOHONENA DO KLASYFIKACJI ŚWIEC JAPOŃSKICH")
    print("=" * 60)

    # Pobieranie danych.
    data = download_stock_data()

    print("\nPrzykładowe dane giełdowe:")
    print(data.head())
    print(f"\nLiczba pobranych rekordów: {len(data)}")

    # Tworzenie cech świec.
    data_features, X_raw = create_candle_features(data)

    # Dodanie opisowego typu świecy.
    data_features["Candle_Type"] = data_features.apply(
        candle_type,
        axis=1
    )

    print("\nPrzykładowe cechy świec:")
    print(X_raw.head())

    print("\nPrzykładowe typy świec:")
    print(
        data_features[
            [
                "Date",
                "Ticker",
                "Open",
                "High",
                "Low",
                "Close",
                "Candle_Type"
            ]
        ].head()
    )

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X_raw)

    results_df, trained_models = run_experiments(
        X,
        data_features,
        n_runs=10,
        sample_size=800
    )

    results_df["Score"] = (
        results_df["Silhouette_Score"]
        - results_df["Quantization_Error"]
    )

    best_row = results_df.sort_values(
        by="Score",
        ascending=False
    ).iloc[0]

    best_run_number = int(best_row["Run"])
    best_model_data = trained_models[best_run_number - 1]

    print("\n" + "=" * 60)
    print("WYNIKI WSZYSTKICH PRÓB")
    print("=" * 60)
    print(results_df)

    print("\n" + "=" * 60)
    print("NAJLEPSZA PRÓBA")
    print("=" * 60)
    print(f"Najlepsza była próba numer: {best_run_number}")
    print(best_row)

    # Podsumowanie klastrów dla najlepszej próby.
    best_data = best_model_data["data"]
    cluster_summary = create_cluster_summary(best_data)

    print("\n" + "=" * 60)
    print("PODSUMOWANIE KLASTRÓW NAJLEPSZEJ PRÓBY")
    print("=" * 60)
    print(cluster_summary.head(20))

    print("\n" + "=" * 60)
    print("PRZYKŁADOWE PRZYPISANIE ŚWIEC DO KLASTRÓW")
    print("=" * 60)
    print(
        best_data[
            [
                "Date",
                "Ticker",
                "Open",
                "High",
                "Low",
                "Close",
                "Candle_Type",
                "Cluster"
            ]
        ].head(30)
    )

    # Zapis wyników do plików CSV.
    results_df.to_csv(
        "wyniki_prob_kohonen.csv",
        index=False,
        encoding="utf-8-sig"
    )

    cluster_summary.to_csv(
        "podsumowanie_klastrow.csv",
        index=False,
        encoding="utf-8-sig"
    )

    best_data.to_csv(
        "najlepsza_proba_dane.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nZapisano pliki:")
    print("- wyniki_prob_kohonen.csv")
    print("- podsumowanie_klastrow.csv")
    print("- najlepsza_proba_dane.csv")

    # Wykresy.
    plot_results(results_df)
    plot_kohonen_map(best_model_data, best_run_number)


if __name__ == "__main__":
    main()