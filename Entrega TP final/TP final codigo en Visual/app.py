# Mini API local (Flask – archivo app.py)
from flask import Flask, jsonify
import pandas as pd
from pathlib import Path

# Crear endpoints que devuelven los datos en formato JSON
app = Flask(__name__)

# Cargar los JSON generados por el análisis
BASE_DIR = Path(__file__).resolve().parent
SALIDAS = BASE_DIR / "salidas"

roi = pd.read_json(SALIDAS / "roi_by_genre.json")
runtime = pd.read_json(SALIDAS / "runtime_by_decade.json")
budget_rating = pd.read_json(SALIDAS / "budget_rating.json")

# Endpoints
@app.get("/roi")
def get_roi():
    return jsonify(roi.to_dict(orient="records"))

@app.get("/runtime")
def get_runtime():
    return jsonify(runtime.to_dict(orient="records"))

@app.get("/budget_rating")
def get_budget_rating():
    return jsonify(budget_rating.to_dict(orient="records"))

# Levantar la API local
if __name__ == "__main__":
    app.run(debug=True)

# Para demostrar endpoints http://127.0.0.1:5000/roi o http://127.0.0.1:5000/runtime o http://127.0.0.1:5000/budget_rating
