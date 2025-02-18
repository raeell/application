"""
Prediction de la survie d'un individu sur le Titanic
"""

import os
from dotenv import load_dotenv
import argparse

import pandas as pd

from import_data import split_and_count
from build_pipeline import split_train_test, create_pipeline
from train_evaluate import evaluate_model

# ENVIRONMENT CONFIGURATION ---------------------------

load_dotenv()

parser = argparse.ArgumentParser(description="Paramètres du random forest")
parser.add_argument(
    "--n_trees", type=int, default=20, help="Nombre d'arbres"
)
args = parser.parse_args()

n_trees = args.n_trees
jeton_api = os.environ.get("JETON_API", "")
data_path = os.environ.get("DATA_PATH", "data.csv")
MAX_DEPTH = None
MAX_FEATURES = "sqrt"

if jeton_api.startswith("$"):
    print("API token has been configured properly")
else:
    print("API token has not been configured")


# IMPORT ET EXPLORATION DONNEES --------------------------------

TrainingData = pd.read_csv("data.csv")


# Usage example:
ticket_count = split_and_count(TrainingData, "Ticket", "/")
name_count = split_and_count(TrainingData, "Name", ",")


# SPLIT TRAIN/TEST --------------------------------

X_train, X_test, y_train, y_test = split_train_test(TrainingData, test_size=0.1)


# PIPELINE ----------------------------


# Create the pipeline
pipe = create_pipeline(
    n_trees, max_depth=MAX_DEPTH, max_features=MAX_FEATURES
)


# ESTIMATION ET EVALUATION ----------------------

pipe.fit(X_train, y_train)


# Evaluate the model
score, matrix = evaluate_model(pipe, X_test, y_test)
print(f"{score:.1%} de bonnes réponses sur les données de test pour validation")
print(20 * "-")
print("matrice de confusion")
print(matrix)
