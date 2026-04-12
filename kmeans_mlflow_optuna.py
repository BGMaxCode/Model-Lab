"""
Dummy KMeans clustering experiment for practicing MLflow + Optuna.

Dataset : sklearn's make_blobs (synthetic, reproducible)
Tune    : n_clusters, init strategy, max_iter
Metric  : silhouette score (higher = better)

Usage
-----
pip install scikit-learn mlflow optuna

# (optional) start the MLflow UI in another terminal:
#   mlflow ui --port 5000

python kmeans_mlflow_optuna.py
"""

import mlflow
import optuna
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# ── reproducible synthetic dataset ──────────────────────────────────────────
X, _ = make_blobs(n_samples=500, centers=5, cluster_std=1.2, random_state=42)
X = StandardScaler().fit_transform(X)

EXPERIMENT_NAME = "kmeans-optuna-demo"
mlflow.set_experiment(EXPERIMENT_NAME)


# ── objective: one Optuna trial == one MLflow run ────────────────────────────
def objective(trial: optuna.Trial) -> float:
    n_clusters = trial.suggest_int("n_clusters", 2, 10)
    init       = trial.suggest_categorical("init", ["k-means++", "random"])
    max_iter   = trial.suggest_int("max_iter", 100, 500, step=100)
    n_init     = trial.suggest_int("n_init", 5, 20, step=5)

    with mlflow.start_run(run_name=f"trial-{trial.number}"):
        # log every hyperparameter
        mlflow.log_params({
            "n_clusters": n_clusters,
            "init":       init,
            "max_iter":   max_iter,
            "n_init":     n_init,
        })

        model = KMeans(
            n_clusters=n_clusters,
            init=init,
            max_iter=max_iter,
            n_init=n_init,
            random_state=42,
        )
        labels = model.fit_predict(X)

        sil   = silhouette_score(X, labels)
        inert = model.inertia_

        mlflow.log_metrics({
            "silhouette_score": sil,
            "inertia":          inert,
            "n_iter":           model.n_iter_,
        })

        # tag so you can filter runs easily in the UI
        mlflow.set_tags({
            "optuna_trial": trial.number,
            "dataset":      "make_blobs(500, centers=5)",
        })

    return sil   # Optuna maximises this


# ── run the study ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    study = optuna.create_study(
        direction="maximize",
        study_name=EXPERIMENT_NAME,
        sampler=optuna.samplers.TPESampler(seed=42),
    )
    study.optimize(objective, n_trials=30, show_progress_bar=True)

    best = study.best_trial
    print("\n── Best trial ──────────────────────────────")
    print(f"  Silhouette score : {best.value:.4f}")
    print(f"  Params           : {best.params}")
    print("\nOpen the MLflow UI:  mlflow ui --port 5000")
    print(f"Experiment name  :  {EXPERIMENT_NAME}")
