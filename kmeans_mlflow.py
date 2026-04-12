"""
KMeans clustering with MLflow tracking only (no Optuna).

Manually define a parameter grid and log each run to MLflow.

Usage
-----
pip install scikit-learn mlflow

# (optional) start the MLflow UI in another terminal:
#   mlflow ui --port 5000

python kmeans_mlflow.py
"""

import mlflow
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# ── dataset ──────────────────────────────────────────────────────────────────
X, _ = make_blobs(n_samples=500, centers=5, cluster_std=1.2, random_state=42)
X = StandardScaler().fit_transform(X)

EXPERIMENT_NAME = "kmeans-mlflow-demo"
mlflow.set_experiment(EXPERIMENT_NAME)

# ── manual parameter grid ─────────────────────────────────────────────────────
param_grid = [
    {"n_clusters": 3, "init": "k-means++", "max_iter": 300, "n_init": 10},
    {"n_clusters": 5, "init": "k-means++", "max_iter": 300, "n_init": 10},
    {"n_clusters": 5, "init": "random",    "max_iter": 300, "n_init": 10},
    {"n_clusters": 5, "init": "k-means++", "max_iter": 100, "n_init": 10},
    {"n_clusters": 7, "init": "k-means++", "max_iter": 300, "n_init": 10},
    {"n_clusters": 5, "init": "k-means++", "max_iter": 300, "n_init": 20},
]

# ── run each config ───────────────────────────────────────────────────────────
for i, params in enumerate(param_grid):
    with mlflow.start_run(run_name=f"run-{i}"):

        mlflow.log_params(params)

        model = KMeans(**params, random_state=42)
        labels = model.fit_predict(X)

        sil   = silhouette_score(X, labels)
        inert = model.inertia_

        mlflow.log_metrics({
            "silhouette_score": sil,
            "inertia":          inert,
            "n_iter":           model.n_iter_,
        })

        mlflow.set_tag("dataset", "make_blobs(500, centers=5)")

        # log the model artifact
        mlflow.sklearn.log_model(model, artifact_path="model")

        print(f"run-{i} | n_clusters={params['n_clusters']:2d} | "
              f"silhouette={sil:.4f} | inertia={inert:.1f}")

print("\nOpen the MLflow UI:  mlflow ui --port 5000")
print(f"Experiment name  :  {EXPERIMENT_NAME}")
